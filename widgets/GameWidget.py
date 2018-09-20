# Creating the game class
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.vector import Vector

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

import numpy as np

from widgets.Balls import Ball1, Ball2, Ball3
from widgets.CarWidget import Car


class Game(RelativeLayout):
    car = ObjectProperty(None)
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
        changed = self.car.sand_width != 0 and self.car.sand_width != int(self.width)
        return changed or self.car.sand_height != 0 and self.car.sand_height != int(self.height)

    def init(self, window=None, width=None, height=None, reInit=False):
        if self.first_update or self.changed_size() or window is not None or reInit:
            self.first_update = False
            self.reset_sand()
            self.scores = []
            self.steps = 0
            self.car.center = (self.top_image.pos[0] + 100, self.top_image.pos[1])
            self.car.sand = self.sand
            self.car.sand_width = int(self.width)
            self.car.sand_height = int(self.height)
            self.set_goal()
            self.top_image.pos = (10, self.height - 110)
            self.bottom_image.pos = (self.width - 110, 10)
            self.brain.reset(self.driving_config)
            self.btw_goals = Vector(self.top_image.center).distance(self.bottom_image.center)
            print ("resetting, new size [{}x{}], goal_position ({};{})".format(self.width, self.height, self.goal_x,
                                                                               self.goal_y))

    def update_config(self, configuration):
        self.driving_config = configuration
        self.init(reInit=True)

    def pause_resume(self):
        self.paused = not self.paused

    points = None

    def update(self, dt):

        if self.paused:
            return False

        self.init()

        xx = self.goal_x - self.car.x
        yy = self.goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx, yy)) / 180.
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation, self.steps]
        # last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]
        action = self.brain.update(self.last_reward, last_signal)
        self.scores.append(self.brain.score())
        rotation = self.action2rotation[action]

        self.car.move(rotation)
        distance = Vector(self.car.get_carfront()).distance((self.goal_x, self.goal_y))

        if np.sum(self.sand[int(self.car.x):int(self.car.x) + 10, int(self.car.y): int(self.car.y) + 20]) > 0:
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            self.last_reward = -1
        else:  # otherwise
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            self.last_reward = self.driving_config.reward_decay
            distance_diff = self.last_distance - distance
            if distance < self.last_distance:
                self.last_reward = self.driving_config.reward_distance
            # else:
            #     self.last_reward = -self.driving_config.reward_distance
            # if distance_diff >= 0:
            #     self.last_reward = self.driving_config.reward_distance
            # elif distance_diff < 0 or distance_diff <= 6:
            #     self.last_reward = -self.driving_config.reward_distance
        reward = self.stay_inside()
        if reward is not None:
            self.last_reward = reward

        self.last_distance = distance
        if distance < 100:
            self.goal_istop = not self.goal_istop
            self.set_goal()
            self.steps = 0
        else:
            self.steps += 1
        if self.steps % 600 == 0:
            self.last_reward = -0.1 * (self.steps / 600.)
            print("Too long, reward [{0:.2f}]".format(self.last_reward))

        stats = {
            'Distance btw Goals': "{0:.2f}".format(self.btw_goals),
            'Destination': self.get_destination(),
            'Distance to Dest': "{0:.2f}".format(self.last_distance),
            'Steps': str(self.steps),
            'Car sensors': 'R [{0:.1f}] B [{1:.1f}] Y [{2:.1f}]'.format(self.car.signal1, self.car.signal2,
                                                                        self.car.signal3),
            'Last reward': "{0:.2f}".format(self.last_reward),
        }
        if self.stats_widget is not None:
            self.stats_widget.update_stats(stats)

    def stay_inside(self):
        corners = self.car.get_corners()
        last_pos_initial = -1.0
        margin = 10
        touched_border = False
        # left border
        last_pos = last_pos_initial
        for corner in corners.values():
            x_diff = margin - corner.x
            new_pos = self.car.x + x_diff
            if x_diff > 0 and new_pos > last_pos:
                last_pos = new_pos
        if last_pos != last_pos_initial:
            self.car.x = last_pos
            touched_border = True

        # right border
        last_pos = self.width + 100.0
        for corner in corners.values():
            x_diff = corner.x - (self.width - margin)
            new_pos = self.car.x - x_diff
            if x_diff > 0 and new_pos < last_pos:
                last_pos = new_pos
        if last_pos != (self.width + 100.0):
            self.car.x = last_pos
            touched_border = True

        # top border
        last_pos = self.height + 100.0
        for corner in corners.values():
            y_diff = corner.y - (self.height - margin)
            new_pos = self.car.y - y_diff
            if y_diff > 0 and new_pos < last_pos:
                last_pos = new_pos
        if last_pos != (self.height + 100.0):
            self.car.y = last_pos
            touched_border = True

        # bottom border
        last_pos = last_pos_initial
        for corner in corners.values():
            y_diff = margin - corner.y
            new_pos = self.car.y + y_diff
            if y_diff > 0 and new_pos > last_pos:
                last_pos = new_pos
        if last_pos != -1:
            self.car.y = margin
            touched_border = True

        if touched_border:
            return -1.0
        return None

    def get_destination(self):
        if self.goal_istop:
            return "1"
        return "2"
