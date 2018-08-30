import ConfigParser
import os

import SelfDrivingError


class Configuration:
    dqn_gamma = 0
    dqn_hidden_neurons = 0
    dqn_learning_rate = 0
    dqn_temperature = 0
    dqn_sample_size = 0

    reward_decay = 0
    reward_distance = 0

    config_parser = None
    file_location = ""

    def __init__(self):
        pass

    def load(self, config_filename="default.ini"):
        self.config_parser = ConfigParser.ConfigParser()
        self.file_location = os.path.join(os.path.dirname(__file__), 'config', config_filename)
        if not os.path.isfile(self.file_location):
            raise SelfDrivingError("Invalid configuration file location [{}]".format(self.file_location))
        self.config_parser.read(self.file_location)
        self.dqn_gamma = self.config_parser.get('dqn', 'gamma')
        self.dqn_hidden_neurons = self.config_parser.get('dqn', 'nb_hidden_neurons')
        self.dqn_learning_rate = self.config_parser.get('dqn', 'learning_rate')
        self.dqn_temperature = self.config_parser.get('dqn', 'temperature')
        self.dqn_sample_size = self.config_parser.get('dqn', 'sample_size')

        self.reward_decay = self.config_parser.get('rewards', 'decay_reward')
        self.reward_distance = self.config_parser.get('rewards', 'distance_reward')

    def update(self, widget_dict):
        self.dqn_gamma = widget_dict['dqn']['gamma']
        self.dqn_hidden_neurons = widget_dict['dqn']['nb_hidden_neurons']
        self.dqn_learning_rate = widget_dict['dqn']['learning_rate']
        self.dqn_temperature = widget_dict['dqn']['temperature']
        self.dqn_sample_size = widget_dict['dqn']['sample_size']

        self.reward_decay = widget_dict['rewards']['decay_reward']
        self.reward_distance = widget_dict['rewards']['distance_reward']
        self.save()

    def save(self):
        self.config_parser.set('dqn', 'gamma', self.dqn_gamma)
        self.config_parser.set('dqn', 'nb_hidden_neurons', self.dqn_hidden_neurons)
        self.config_parser.set('dqn', 'learning_rate', self.dqn_learning_rate)
        self.config_parser.set('dqn', 'temperature', self.dqn_temperature)
        self.config_parser.set('dqn', 'sample_size', self.dqn_sample_size)

        self.config_parser.set('rewards', 'decay_reward', self.reward_decay)
        self.config_parser.set('rewards', 'distance_reward', self.reward_distance)

        print("Saving config to [{}]".format(self.file_location))
        config_file = open(self.file_location, 'w+')
        self.config_parser.write(config_file)
        config_file.close()
