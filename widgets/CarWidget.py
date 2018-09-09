import numpy as np
from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


class Car(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    red_sensor = ObjectProperty(0)
    blue_sensor = ObjectProperty(0)
    yellow_sensor = ObjectProperty(0)

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

        if self.sensor_onborder(self.red_sensor):
            self.signal1 = 1.
        else:
            self.signal1 = self.sensor_sanddensity(self.red_sensor)

        if self.sensor_onborder(self.blue_sensor):
            self.signal2 = 1.
        else:
            self.signal2 = self.sensor_sanddensity(self.blue_sensor)

        if self.sensor_onborder(self.yellow_sensor):
            self.signal3 = 1.
        else:
            self.signal3 = self.sensor_sanddensity(self.yellow_sensor)

    def sensor_sanddensity(self, sensor):

        int_sensorx = int(sensor.center[0])
        int_sensory = int(sensor.center[1])

        return int(np.sum(self.sand[int_sensorx - 10:int_sensorx + 10, int_sensory - 10:int_sensory + 10])) / 400.

    def sensor_onborder(self, sensor):
        sensor_x = sensor.center[0]
        sensor_y = sensor.center[1]
        if sensor_x > self.sand_length - 10 or sensor_x < 10 or sensor_y > self.sand_width - 10 or sensor_y < 10:
            return True
        return False

    def get_carfront(self):
        return self.pos[0] + self.width, self.center[1]
