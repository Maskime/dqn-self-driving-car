from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import matplotlib.pyplot as plt

import numpy as np


class GraphWidget(BoxLayout):

    game_widget = None
    to_display = []
    graph_canvas = None
    fig = None
    ax = None

    nb_pointsdisplay = 100

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        # self.ax.set_ylabel('Last Scores')
        self.line1, = self.ax.plot(self.to_display)
        self.ax.set_xlim(0, self.nb_pointsdisplay)
        self.graph_canvas = FigureCanvasKivyAgg(figure=self.fig)

        self.add_widget(self.graph_canvas)

    def set_pointsdisplayed(self, points):
        self.nb_pointsdisplay = points
        self.ax.set_xlim(0, self.nb_pointsdisplay)

    def update(self, dt):
        if self.game_widget is None or len(self.game_widget.scores) == 0:
            pass

        nb_scores = len(self.game_widget.scores)
        nb_points = min(nb_scores, self.nb_pointsdisplay)
        start = nb_scores - nb_points
        last_scores = self.game_widget.scores[start:nb_scores]
        x_data = range(0, len(last_scores))
        # print(last_scores)
        self.line1.set_ydata(last_scores)
        self.line1.set_xdata(x_data)
        self.ax.set_ylim(np.min(last_scores), np.max(last_scores))
        self.graph_canvas.draw()
        # self.graph_canvas.flush_events()

