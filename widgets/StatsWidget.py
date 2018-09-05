from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class StatsWidget(GridLayout):
    steps_count = ObjectProperty(None)
    destination = ObjectProperty(None)
    distance = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(StatsWidget, self).__init__(**kwargs)

    def update_stats(self, steps, destination, distance):
        self.steps_count.text = str(steps)
        self.destination.text = destination
        self.distance.text = str(distance)
