from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Sensor(Widget):
    angle = NumericProperty(0)

    def get_corners(self):
        return {
            'bottom_left': Vector(*self.pos),
            'top_left': Vector(self.pos[0], self.pos[1] + self.height),
            'top_right': Vector(self.pos[0] + self.width, self.pos[1] + self.height),
            'bottom_right': Vector(self.pos[0] + self.width, self.pos[1]),
        }


class Ball1(Sensor):
    pass


class Ball2(Sensor):
    pass


class Ball3(Sensor):
    pass
