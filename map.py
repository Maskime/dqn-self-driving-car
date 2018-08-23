# Self Driving Car

# Importing the libraries
import numpy as np
# Importing the Kivy packages
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector

import matplotlib.pyplot as plt
from kivy.properties import ObjectProperty

# Importing widget that are outside this file for kivy
from CarWidget import Car
from PaintWidget import PaintWidget
from Balls import Ball1, Ball2, Ball3
from GameWidget import Game

# Importing the Dqn object from our AI in ai.py
from ai import Dqn

# Adding this line if we don't want the right click to put a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


# Adding the API Buttons (clear, save and load)
class CarApp(App):
    brain = Dqn(5, 3, 0.9)
    scores = []
    game_widget = None

    def __init__(self, **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.painter = PaintWidget()

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
