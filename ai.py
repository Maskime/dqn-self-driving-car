# AI for Self Driving Car

# Importing the libraries

import numpy as np
import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable


# Creating the architecure of the Neural Network

class Network(nn.Module):

    def __init__(self, input_size, nb_action, hidden_neurons):
        super(Network, self).__init__()
        self.input_size = input_size
        self.nb_action = nb_action
        self.fc1 = nn.Linear(input_size,
                             hidden_neurons)  # Declares that the first layer is fully connected to the second layer (fc stands for full connection)
        self.fc2 = nn.Linear(hidden_neurons, nb_action)

    def forward(self, state):  # Forward propagation
        x = F.relu(self.fc1(state))
        q_values = self.fc2(x)
        return q_values


# Implementing Experience Replay
class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)


# Implementaing Deep Q Learning

class Dqn:

    input_size = 0
    nb_action = 0

    driving_config = None

    def __init__(self, input_size, nb_action, config):

        self.driving_config = config

        self.gamma = self.driving_config.dqn_gamma
        self.reward_window = []
        self.input_size = input_size
        self.nb_action = nb_action

        self.model = Network(input_size, nb_action, self.driving_config.dqn_hidden_neurons)
        self.memory = ReplayMemory(100000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.driving_config.dqn_learning_rate)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0

    def reset(self, config):

        self.driving_config = config

        self.reward_window = []
        self.model = Network(self.input_size, self.nb_action, self.driving_config.dqn_hidden_neurons)
        self.memory = ReplayMemory(100000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.driving_config.dqn_learning_rate)
        self.last_state = torch.Tensor(self.input_size).unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0

    def select(self, state):
        probs = F.softmax(self.model(Variable(state, volatile=True)) * self.driving_config.dqn_temperature)
        action = probs.multinomial(num_samples=1)
        return action.data[0, 0]

    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        target = self.gamma * next_outputs + batch_reward
        td_loss = F.smooth_l1_loss(outputs, target)
        self.optimizer.zero_grad()
        td_loss.backward(retain_variables=True)
        self.optimizer.step()

    def update(self, reward, signal):
        new_state = torch.Tensor(signal).float().unsqueeze(0)
        last_action_tensor = torch.LongTensor([int(self.last_action)])  # converting an int to a tensor
        reward_tensor = torch.Tensor([self.last_reward])
        self.memory.push((self.last_state, new_state, last_action_tensor, reward_tensor))
        action = self.select(new_state)
        if len(self.memory.memory) > self.driving_config.dqn_sample_size:
            # print("sampling")
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(self.driving_config.dqn_sample_size)
            # print("learning")
            self.learn(batch_state, batch_next_state, batch_reward, batch_action)

        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.reward_window.append(reward)
        if len(self.reward_window) > 1000:
            del self.reward_window[0]

        # print("acting")
        return action

    def score(self):
        return sum(self.reward_window) / (len(self.reward_window) + 1)  # trick to avoid dividing by 0

    def save(self):
        torch.save({
            'state_dict': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict()
        }, 'last_brain.pth')

    def load(self):
        if os.path.isfile('last_brain.pth'):
            print("Loading last save")
            checkpoint = torch.load('last_brain.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("Loaded")
        else:
            print("No save to load")
