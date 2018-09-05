from kivy.uix.widget import Widget

from kivy.graphics import Color, Line
import numpy as np


class PaintWidget(Widget):
    game = None
    last_x = 0
    last_y = 0
    line_width = 10

    lines = []

    def check_within_canvas(self, touch):
        sand_width = len(self.game.sand[:, 0])
        sand_height = len(self.game.sand[0])
        if touch.x >= sand_width or touch.y >= sand_height:
            return False
        return True

    def init_line(self, touch):
        if not touch.ud or not touch.ud['line']:
            Color(0.8, 0.7, 0)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
        return touch

    def on_touch_down(self, touch):
        with self.canvas:
            if not self.check_within_canvas(touch):
                return
            touch = self.init_line(touch)
            self.last_x = int(touch.x)
            self.last_y = int(touch.y)
            self.update_sand(touch)

    def compute_ranges(self, touch):
        int_x = int(touch.x)
        x_start = max(0, int_x - self.line_width)
        x_end = min(int_x + self.line_width, len(self.game.sand[:, 0]))
        x_range = range(x_start, x_end)

        int_y = int(touch.y)
        y_start = max(0, int_y - self.line_width)
        y_end = min(int_y + self.line_width, len(self.game.sand[0, :]))
        y_range = range(y_start, y_end)

        return x_range, y_range

    def update_sand(self, touch):
        x_range, y_range = self.compute_ranges(touch)
        for x in x_range:
            for y in y_range:
                self.game.sand[x, y] = 1

    def on_touch_move(self, touch):
        if touch.button == 'left':
            if not self.check_within_canvas(touch):
                return
            touch = self.init_line(touch)
            touch.ud['line'].points += [touch.x, touch.y]

            touch.ud['line'].width = self.line_width
            self.update_sand(touch)
            self.last_x = int(touch.x)
            self.last_y = int(touch.y)
