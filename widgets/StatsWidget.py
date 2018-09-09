from kivy.uix.label import Label

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class StatsWidget(GridLayout):

    first_update = True
    labels = {}

    def __init__(self, **kwargs):
        super(StatsWidget, self).__init__(**kwargs)

    def update_stats(self, stats):
        if self.first_update:
            self.first_update = False
            self.rows = len(stats)
            for key, value in stats.iteritems():
                self.labels[key] = Label(text=value)
                self.add_widget(Label(text=key))
                self.add_widget(self.labels[key])
        else:
            for key, value in stats.iteritems():
                self.labels[key].text = value