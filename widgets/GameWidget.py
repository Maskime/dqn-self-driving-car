# Creating the game class
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.vector import Vector

from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

import numpy as np

from widgets.Balls import Ball1, Ball2, Ball3
from widgets.CarWidget import Car


class Game(RelativeLayout):
    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    top_image = ObjectProperty(None)
    bottom_image = ObjectProperty(None)

    brain = None
    sand = None
    stats_widget = None

    action2rotation = [0, 20, -20]
    scores = []

    last_reward = 0.0
    goal_x = 0.0
    goal_y = 0.0
    last_distance = 0.0
    steps = 0
    btw_goals = 0.0

    goal_istop = True
    first_update = True
    dirty = False
    paused = False

    driving_config = None

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        Window.bind(on_resize=self.init)

    def reset_sand(self):
        self.sand = np.zeros((int(self.width), int(self.height)))
        self.car.sand = self.sand

    def serve_car(self):
        self.set_goal()
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def set_goal(self):
        if self.goal_istop:
            self.goal_x = self.top_image.center[0]
            self.goal_y = self.top_image.center[1]
        else:
            self.goal_x = self.bottom_image.center[0]
            self.goal_y = self.bottom_image.center[1]

    def changed_size(self):
        changed = self.car.sand_length != 0 and self.car.sand_length != self.width
        return changed or self.car.sand_width != 0 and self.car.sand_width != self.height

    def init(self, window=None, width=None, height=None, reInit=False):
        if self.first_update or self.changed_size() or window is not None or reInit:
            self.first_update = False
            self.reset_sand()
            self.scores = []
            self.steps = 0
            self.car.center = (self.top_image.pos[0] + 100, self.top_image.pos[1])
            self.car.sand = self.sand
            self.car.sand_length = self.width
            self.car.sand_width = self.height
            self.set_goal()
            self.top_image.pos = (10, self.height - 110)
            self.bottom_image.pos = (self.width - 110, 10)
            self.brain.reset(self.driving_config)
            self.btw_goals = Vector(self.top_image.center).distance(self.bottom_image.center)
            print ("resetting, new size [{}x{}], goal_position ({};{})".format(self.width, self.height, self.goal_x,
                                                                               self.goal_y))
            print (self.pos, self.car.size)

    def update_config(self, configuration):
        self.driving_config = configuration
        self.init(reInit=True)

    def pause_resume(self):
        self.paused = not self.paused

    def update(self, dt):

        if self.paused:
            return False

        self.init()

        xx = self.goal_x - self.car.x
        yy = self.goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx, yy)) / 180.
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation, self.steps]
        action = self.brain.update(self.last_reward, last_signal)
        self.scores.append(self.brain.score())
        rotation = self.action2rotation[action]
        self.car.move(rotation)
        distance = Vector(self.car.get_carfront()).distance((self.goal_x, self.goal_y))
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

        if self.sand[int(self.car.x), int(self.car.y)] > 0:
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            self.last_reward = -1
        else:  # otherwise
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            self.last_reward = self.driving_config.reward_decay
            if distance < self.last_distance:
                self.last_reward = self.driving_config.reward_distance

        if self.car.x < 10:
            self.car.x = 10
            self.last_reward = -1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            self.last_reward = -1
        if self.car.y < 10:
            self.car.y = 10
            self.last_reward = -1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            self.last_reward = -1

        self.last_distance = distance
        if distance < 100:
            self.goal_istop = not self.goal_istop
            self.set_goal()
            self.steps = 0
        else:
            self.steps += 1
            if self.steps % 600 == 0:
                self.last_reward = -0.1 * (self.steps / 600)
                print("Too long, reward [{0:.2f}]".format(self.last_reward))

        stats = {
            'Distance btw Goals': "{0:.2f}".format(self.btw_goals),
            'Destination': self.get_destination(),
            'Distance to Dest': "{0:.2f}".format(self.last_distance),
            'Steps': str(self.steps)
        }
        if self.stats_widget is not None:
            self.stats_widget.update_stats(stats)

    def get_destination(self):
        if self.goal_istop:
            return "Serial SA"
        return "Pictet"
