from kivy.uix.widget import Widget

from kivy.graphics import Color, Line
import numpy as np


class PaintWidget(Widget):
    game = None
    length = 0
    n_points = 0
    last_x = 0
    last_y = 0

    def on_touch_down(self, touch):
        with self.canvas:
            Color(0.8, 0.7, 0)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
            self.last_x = int(touch.x)
            self.last_y = int(touch.y)
            self.n_points = 0
            self.length = 0
            self.game.sand[int(touch.x), int(touch.y)] = 1

# TODO remove global length, n_points, last_x, last_y
    def on_touch_move(self, touch):
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            self.length += np.sqrt(max((x - self.last_x) ** 2 + (y - self.last_y) ** 2, 2))
            self.n_points += 1.
            density = self.n_points / self.length
            touch.ud['line'].width = int(20 * density + 1)
            self.game.sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1
            self.last_x = x
            self.last_y = y