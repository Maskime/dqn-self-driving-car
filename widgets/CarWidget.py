from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.properties import NumericProperty, ReferenceListProperty
import numpy as np


class Car(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Front sensor
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)

    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)

    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)

    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    sand = None

    sand_length = 0
    sand_width = 0

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation

        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle + 30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle - 30) % 360) + self.pos

        if self.sensor_onborder(self.sensor1_x, self.sensor1_y):
            self.signal1 = 1.
        else:
            self.signal1 = self.sensor_sanddensity(self.sensor1_x, self.sensor1_y)

        if self.sensor_onborder(self.sensor2_x, self.sensor2_y):
            self.signal2 = 1.
        else:
            self.signal2 = self.sensor_sanddensity(self.sensor2_x, self.sensor2_y)

        if self.sensor_onborder(self.sensor3_x, self.sensor3_y):
            self.signal3 = 1.
        else:
            self.signal3 = self.sensor_sanddensity(self.sensor3_x, self.sensor3_y)

        # print("New car position ({}), ({})".format(self.pos, self.to_local(self.pos[0], self.pos[1])))

    def sensor_sanddensity(self, sensor_x, sensor_y):

        int_sensorx = int(sensor_x)
        int_sensory = int(sensor_y)

        return int(np.sum(self.sand[int_sensorx - 10:int_sensorx + 10, int_sensory - 10:int_sensory + 10])) / 400.

    def sensor_onborder(self, sensor_x, sensor_y):
        if sensor_x > self.sand_length - 10 or sensor_x < 10 or sensor_y > self.sand_width - 10 or sensor_y < 10:
            return True
        return False
