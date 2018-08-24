from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt


class GraphWidget(BoxLayout):

    game_widget = None

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        plt.ylabel('Scores')
        plt.xlabel('Transitions')
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def update(self, dt):
        if self.game_widget is not None:
            print("Updated score length [{}]".format(len(self.game_widget.scores)))
            plt.plot(self.game_widget.scores)
            plt.draw()

