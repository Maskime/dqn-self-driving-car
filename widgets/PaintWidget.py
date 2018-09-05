from kivy.uix.widget import Widget

from kivy.graphics import Color, Line
import numpy as np


class PaintWidget(Widget):
    game = None
    last_x = 0
    last_y = 0

    def check_within_canvas(self, touch):
        sand_width = len(self.game.sand[:, 0])
        sand_height = len(self.game.sand[0])
        if touch.x >= sand_width or touch.y >= sand_height:
            return False
        return True

    def init_line(self, touch):
        if not touch.ud or not touch.ud['line']:
            Color(0.8, 0.7, 0)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
        return touch

    def on_touch_down(self, touch):
        with self.canvas:
            if not self.check_within_canvas(touch):
                return
            touch = self.init_line(touch)
            self.last_x = int(touch.x)
            self.last_y = int(touch.y)
            self.game.sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1

    def on_touch_move(self, touch):
        if touch.button == 'left':
            if not self.check_within_canvas(touch):
                return
            touch = self.init_line(touch)
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            touch.ud['line'].width = 10
            self.game.sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1
            self.last_x = x
            self.last_y = y
