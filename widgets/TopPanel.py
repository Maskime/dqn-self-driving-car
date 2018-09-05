from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from widgets.StatsWidget import StatsWidget


class TopPanel(BoxLayout):
    graph_widget = ObjectProperty(None)
    stats_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TopPanel, self).__init__(**kwargs)


