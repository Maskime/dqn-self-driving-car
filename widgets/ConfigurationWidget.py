from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty


class ConfigurationWidget(BoxLayout):
    dqn_gamma = ObjectProperty(None)
    dqn_neurons = ObjectProperty(None)
    dqn_learning = ObjectProperty(None)
    dqn_temperature = ObjectProperty(None)
    dqn_sample = ObjectProperty(None)

    reward_decay = ObjectProperty(None)
    reward_distance = ObjectProperty(None)

    save_btn = ObjectProperty(None)
    cancel_btn = ObjectProperty(None)

    self_driving_config = None

    def set_config(self, config):
        self.self_driving_config = config

        self.dqn_gamma.value = str(self.self_driving_config.dqn_gamma)
        self.dqn_neurons.value = str(self.self_driving_config.dqn_hidden_neurons)
        self.dqn_learning.value = str(self.self_driving_config.dqn_learning_rate)
        self.dqn_temperature.value = str(self.self_driving_config.dqn_temperature)
        self.dqn_sample.value = str(self.self_driving_config.dqn_sample_size)

        self.reward_decay.value = str(self.self_driving_config.reward_decay)
        self.reward_distance.value = str(self.self_driving_config.reward_distance)

    def get_dict(self):
        return {
            'dqn': {
                'gamma': self.dqn_gamma.inner_input.text,
                'nb_hidden_neurons': self.dqn_neurons.inner_input.text,
                'learning_rate': self.dqn_learning.inner_input.text,
                'temperature': self.dqn_temperature.inner_input.text,
                'sample_size': self.dqn_sample.inner_input.text
            },
            'rewards': {
                'decay_reward': self.reward_decay.inner_input.text,
                'distance_reward': self.reward_distance.inner_input.text
            }
        }
