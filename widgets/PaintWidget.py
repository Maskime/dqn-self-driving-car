import os
from itertools import izip
from kivy.uix.widget import Widget

from kivy.graphics import Color, Line
import json


class PaintWidget(Widget):
    game = None
    last_x = 0
    last_y = 0
    line_width = 10

    lines = []

    def get_sanddimensions(self):
        return len(self.game.sand[:, 0]), len(self.game.sand[0])

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

    def full_line(self, line_points):
        Color(0.8, 0.7, 0)
        Line(points=line_points, width=self.line_width)

    def on_touch_down(self, touch):
        with self.canvas:
            if not self.check_within_canvas(touch):
                return
            touch = self.init_line(touch)
            self.last_x = int(touch.x)
            self.last_y = int(touch.y)
            self.update_sand(self.last_x, self.last_y)

    def compute_ranges(self, x, y):
        int_x = int(x)
        x_start = max(0, int_x - self.line_width)
        x_end = min(int_x + self.line_width, len(self.game.sand[:, 0]))
        x_range = range(x_start, x_end)

        int_y = int(y)
        y_start = max(0, int_y - self.line_width)
        y_end = min(int_y + self.line_width, len(self.game.sand[0, :]))
        y_range = range(y_start, y_end)

        return x_range, y_range

    def update_sand(self, x, y):
        x_range, y_range = self.compute_ranges(x, y)
        for x in x_range:
            for y in y_range:
                self.game.sand[x, y] = 1

    def on_touch_move(self, touch):
        if touch.button == 'left':
            if not self.check_within_canvas(touch):
                return
            with self.canvas:
                touch = self.init_line(touch)
            touch.ud['line'].points += [touch.x, touch.y]

            touch.ud['line'].width = self.line_width
            self.update_sand(touch.x, touch.y)
            self.last_x = int(touch.x)
            self.last_y = int(touch.y)

    def on_touch_up(self, touch):
        if not self.check_within_canvas(touch):
            return
        self.lines.append(touch.ud['line'].points)

    def save(self, filename):
        sand_width, sand_height = self.get_sanddimensions()
        to_save = {
            'dimensions': [sand_width, sand_height],
            'lines': self.lines
        }
        file_location = os.path.join(os.path.dirname(__file__), '..', 'maps', filename)
        with open(file_location, 'w+') as map_file:
            map_file.write(json.dumps(to_save))

    @staticmethod
    def pairwise(iterable):
        a = iter(iterable)
        return izip(a, a)

    def load(self, filename):
        file_location = os.path.join(os.path.dirname(__file__), '..', 'maps', filename)
        if not os.path.isfile(file_location):
            print("No file at [{}]".format(file_location))
            return
        print("Loading file [{}]".format(file_location))
        map_definition = None
        with open(file_location, 'r') as map_file:
            map_definition = json.load(map_file)
        if map_definition is None:
            print("Could not load map at [{}]".format(file_location))
            return
        sand_width, sand_height = self.get_sanddimensions()
        map_width, map_height = map_definition['dimensions']
        sand_surface = sand_width * sand_height
        map_surface = map_width * map_height
        if sand_surface > map_surface:
            width_ratio = map_width / sand_width
            height_ratio = map_height / sand_height
        else:
            width_ratio = sand_width / map_width
            height_ratio = sand_height / map_height

        print("Ratio to be applied [{}, {}]".format(width_ratio, height_ratio))

        self.lines = []
        for line in map_definition['lines']:
            new_line = []
            for x, y in self.pairwise(line):
                sand_x = x * width_ratio
                sand_y = y * height_ratio
                new_line += [sand_x, sand_y]
                self.update_sand(sand_x, sand_y)
            with self.canvas:
                self.full_line(new_line)
