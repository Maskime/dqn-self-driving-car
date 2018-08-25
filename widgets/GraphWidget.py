from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import matplotlib.pyplot as plt


class GraphWidget(BoxLayout):

    game_widget = None
    to_display = []
    graph_canvas = None
    fig = None
    ax = None

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        plt.ylabel('Scores')
        plt.xlabel('Transitions')
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(self.to_display)
        self.graph_canvas = FigureCanvasKivyAgg(figure=self.fig)

        self.add_widget(self.graph_canvas)

    def update(self, dt):
        if self.game_widget is None or len(self.game_widget.scores) == 0:
            pass

        nb_scores = len(self.game_widget.scores)
        nb_points = min(nb_scores, 100)
        start = nb_scores - nb_points
        last_scores = self.game_widget.scores[start:nb_scores]
        print(last_scores)
        self.line1.set_ydata(last_scores)
        self.graph_canvas.draw()
        self.graph_canvas.flush_events()

