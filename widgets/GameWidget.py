# Creating the game class
from kivy.vector import Vector

from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

import numpy as np

from widgets.Balls import Ball1, Ball2, Ball3
from widgets.CarWidget import Car


class Game(Widget):
    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    brain = None
    action2rotation = [0, 20, -20]
    last_reward = 0
    scores = []
    sand = None
    goal_x = 0
    goal_y = 0
    goal_istop = True
    first_update = True
    last_distance = 0

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

    def reset_sand(self):
        self.sand = np.zeros((int(self.width), int(self.height)))
        self.car.sand = self.sand

    def serve_car(self):
        self.set_goal()
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def set_goal(self):
        if self.goal_istop:
            self.goal_x = 20
            self.goal_y = self.height - 20
        else:
            self.goal_x = self.width - 20
            self.goal_y = 20

    def changed_size(self):
        changed = self.car.sand_length != 0 and self.car.sand_length != self.width
        return changed or self.car.sand_width != 0 and self.car.sand_width != self.height

    def init(self):
        if self.first_update or self.changed_size():
            self.first_update = False
            self.reset_sand()
            self.car.sand = self.sand
            self.car.sand_length = self.width
            self.car.sand_width = self.height
            self.set_goal()
            self.brain.reset()
            print ("resetting, new size [{}x{}], goal_position ({};{})".format(self.width, self.height, self.goal_x, self.goal_y))

    def update(self, dt):

        self.init()

        xx = self.goal_x - self.car.x
        yy = self.goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx, yy)) / 180.
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]
        action = self.brain.update(self.last_reward, last_signal)
        self.scores.append(self.brain.score())
        rotation = self.action2rotation[action]
        self.car.move(rotation)
        distance = np.sqrt((self.car.x - self.goal_x) ** 2 + (self.car.y - self.goal_y) ** 2)
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

        if self.sand[int(self.car.x), int(self.car.y)] > 0:
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            self.last_reward = -1
        else:  # otherwise
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            self.last_reward = -0.2
            if distance < self.last_distance:
                self.last_reward = 0.1

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

        if distance < 100:
            self.goal_istop = not self.goal_istop
            self.set_goal()
        self.last_distance = distance
