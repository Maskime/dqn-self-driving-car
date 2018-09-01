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

    paused = False

    nb_pointsdisplay = 1000
    refresh_rate = 10

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / self.refresh_rate)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot([])
        self.ax.set_ylabel("Score Mean")
        self.ax.set_xlabel("Transition Number")
        self.graph_canvas = FigureCanvasKivyAgg(figure=self.fig)

        self.add_widget(self.graph_canvas)

    def update(self, dt):
        if self.paused:
            return False
        if self.game_widget is None or len(self.game_widget.scores) == 0:
            return

        nb_scores = min(len(self.game_widget.scores), self.nb_pointsdisplay)
        x_data = range(0, nb_scores)
        start = len(self.game_widget.scores) - nb_scores
        y_data = self.game_widget.scores[start:]
        self.line1.set_ydata(y_data)
        self.ax.set_ylim(np.min(y_data), np.max(y_data))

        self.line1.set_xdata(x_data)
        self.ax.set_xlim(0, nb_scores)

        self.graph_canvas.draw()
        # self.graph_canvas.flush_events()

    def pause_resume(self):
        self.paused = not self.paused
        if not self.paused:
            Clock.schedule_interval(self.update, 1.0 / self.refresh_rate)

