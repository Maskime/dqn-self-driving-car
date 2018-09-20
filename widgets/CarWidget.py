import numpy as np
from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.properties import NumericProperty, ReferenceListProperty


class Car(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    sand = None

    sand_width = 0
    sand_height = 0

    points = None

    red = None
    blue = None
    yellow = None

    def move(self, rotation):

        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation

        self.red = Vector(25, 0).rotate(self.angle) + self.pos
        self.blue = Vector(25, 0).rotate((self.angle + 30) % 360) + self.pos
        self.yellow = Vector(25, 0).rotate((self.angle - 30) % 360) + self.pos
        if self.sensor_onborder(self.red):
            self.signal1 = 1.
        else:
            self.signal1 = self.sensor_sanddensity(self.red)

        if self.sensor_onborder(self.blue):
            self.signal2 = 1.
        else:
            self.signal2 = self.sensor_sanddensity(self.blue)

        if self.sensor_onborder(self.yellow):
            self.signal3 = 1.
        else:
            self.signal3 = self.sensor_sanddensity(self.yellow)

    def sensor_sanddensity(self, vector):
        int_sensorx = int(vector[0])
        int_sensory = int(vector[1])

        return int(np.sum(self.sand[int_sensorx:int_sensorx + 10, int_sensory:int_sensory + 10])) / 100.

    def get_vec_corners(self, vector):
        return {
            'bottom_left': vector,
            'top_left': Vector(vector[0], vector[1] + 10),
            'top_right': Vector(vector[0] + 10, vector[1] + 10),
            'bottom_right': Vector(vector[0] + 10, vector[1]),
        }

    def sensor_onborder(self, vector):
        corners = self.get_vec_corners(vector)
        margin = 2
        # left border
        for corner in corners.values():
            x_diff = margin - corner.x
            if x_diff > 0:
                return True

        # right border
        for corner in corners.values():
            x_diff = corner.x - (self.sand_width - margin)
            if x_diff > 0:
                return True

        # top border
        for corner in corners.values():
            y_diff = corner.y - (self.sand_height - margin)
            if y_diff > 0:
                return True

        # bottom border
        for corner in corners.values():
            y_diff = margin - corner.y
            if y_diff > 0:
                return True

        return False

    def get_carfront(self):
        return Vector(self.pos[0] + self.width, self.center[1])

    def get_corners(self):
        return {
            'bottom_left': Vector(*self.pos),
            'top_left': Vector(self.pos[0], self.pos[1] + self.height),
            'top_right': Vector(self.pos[0] + self.width, self.pos[1] + self.height),
            'bottom_right': Vector(self.pos[0] + self.width, self.pos[1]),
        }
