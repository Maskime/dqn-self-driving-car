# Self Driving Car

# Importing the libraries
import numpy as np
# Importing the Kivy packages
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector

import matplotlib.pyplot as plt
from kivy.properties import ObjectProperty

from CarWidget import Car

# Importing the Dqn object from our AI in ai.py
from ai import Dqn

# Adding this line if we don't want the right click to put a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Introducing last_x and last_y, used to keep the last point in memory when we draw the sand on the map
last_x = 0
last_y = 0
n_points = 0
length = 0


# Creating the car class

class Ball1(Widget):
    pass


class Ball2(Widget):
    pass


class Ball3(Widget):
    pass


# Creating the game class

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
        self.sand = np.zeros((self.width, self.height))
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

    def init(self):
        self.reset_sand()
        self.car.sand = self.sand
        self.car.sand_length = self.width
        self.car.sand_width = self.height
        self.first_update = False

    def update(self, dt):

        if self.first_update:
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


# Adding the painting tools

class MyPaintWidget(Widget):
    game = None

    def on_touch_down(self, touch):
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8, 0.7, 0)
            d = 10.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            self.game.sand[int(touch.x), int(touch.y)] = 1

    def on_touch_move(self, touch):
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - last_x) ** 2 + (y - last_y) ** 2, 2))
            n_points += 1.
            density = n_points / (length)
            touch.ud['line'].width = int(20 * density + 1)
            self.game.sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1
            last_x = x
            last_y = y


# Adding the API Buttons (clear, save and load)

class CarApp(App):
    brain = Dqn(5, 3, 0.9)
    scores = []
    game_widget = None

    def __init__(self, **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.painter = MyPaintWidget()

    def build(self):
        self.game_widget = Game()
        self.game_widget.brain = self.brain
        self.game_widget.scores = self.scores
        self.game_widget.serve_car()

        Clock.schedule_interval(self.game_widget.update, 1.0 / 60.0)
        self.painter.game = self.game_widget

        clearbtn = Button(text='clear')
        savebtn = Button(text='save', pos=(self.game_widget.width, 0))
        loadbtn = Button(text='load', pos=(2 * self.game_widget.width, 0))
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)

        self.game_widget.add_widget(self.painter)
        self.game_widget.add_widget(clearbtn)
        self.game_widget.add_widget(savebtn)
        self.game_widget.add_widget(loadbtn)

        return self.game_widget

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.game_widget.reset_sand()

    def save(self, obj):
        print("saving brain...")
        self.brain.save()
        plt.plot(self.scores)
        plt.show()

    def load(self, obj):
        print("loading last saved brain...")
        self.brain.load()


# TODO : Move the sand global var to its correct scope

# Running the whole thing
if __name__ == '__main__':
    Window.size = (1080, 1024)
    car_app = CarApp()
    CarApp().run()
