import os
from itertools import izip
from kivy.uix.widget import Widget

from kivy.graphics import Color, Line
import json
from kivy.vector import Vector

import numpy as np


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
        if not touch.ud or 'line' not in touch.ud:
            with self.canvas:
                Color(0.8, 0.7, 0)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width, cap='square')
        return touch

    def full_line(self, line_points):
        with self.canvas:
            Color(0.8, 0.7, 0)
            Line(points=line_points, width=self.line_width, cap='square')

    def on_touch_down(self, touch):
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
            touch = self.init_line(touch)
            touch.ud['line'].points += [touch.x, touch.y]

            touch.ud['line'].width = self.line_width
            self.update_sand(touch.x, touch.y)
            self.update_sandline([self.last_x, self.last_y], [touch.x, touch.y])
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
        fsand_width, fsand_height = float(sand_width), float(sand_height)
        fmap_width, fmap_height = float(map_width), float(map_height)
        '''
        If the sand box size is bigger than the map, then we need to scale up
        otherwise we need to scale down
        scale factor :
        '''
        width_ratio = fsand_width / fmap_width
        height_ratio = fsand_height / fmap_height

        print("Ratio to be applied [{}, {}]".format(width_ratio, height_ratio))

        self.lines = []
        for index, line in enumerate(map_definition['lines']):
            print("Line number [{}]".format(index))
            new_line = []
            previous_point = None
            for x, y in self.pairwise(line):
                sand_x = float(x * width_ratio)
                sand_y = float(y * height_ratio)
                print("Map ({};{}) Sand ({},{})".format(x, y, sand_x, sand_y))
                new_line += [sand_x, sand_y]
                self.update_sand(sand_x, sand_y)
                if previous_point is not None:
                    self.update_sandline(previous_point, [sand_x, sand_y])
                previous_point = [sand_x, sand_y]

            self.full_line(new_line)

    @staticmethod
    def get_points(quantity, p1, p2):
        return zip(np.linspace(p1[0], p2[0], quantity + 1), np.linspace(p1[1], p2[1], quantity + 1))

    def update_sandline(self, point_1, point_2):
        p1 = (point_1[0], point_1[1])
        p2 = (point_2[0], point_2[1])
        distance = Vector(p1).distance(p2)

        for point in self.get_points(int(distance), point_1, point_2):
            self.update_sand(point[0], point[1])
