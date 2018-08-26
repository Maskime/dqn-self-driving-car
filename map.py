# Self Driving Car

# Importing the libraries
# Importing the Kivy packages
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

# Importing the Dqn object from our AI in ai.py
from ai import Dqn
# Importing widget that are outside this file for kivy
from widgets.ButtonsWidget import Buttons
from widgets.GameWidget import Game
from widgets.GraphWidget import GraphWidget
from widgets.RightPanelWidget import RightPanelWidget
from widgets.PaintWidget import PaintWidget

# Adding this line if we don't want the right click to put a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class RootWidget(GridLayout):
    pass


# Adding the API Buttons (clear, save and load)
class CarApp(App):
    brain = Dqn(5, 3, 0.9)
    scores = []
    game_widget = None
    right_panel = None

    def __init__(self, **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.painter = PaintWidget()

    def on_resize(self):
        print("resized")

    def build(self):
        self.game_widget = Game()
        self.game_widget.brain = self.brain
        self.game_widget.scores = self.scores
        self.game_widget.serve_car()

        Clock.schedule_interval(self.game_widget.update, 1.0 / 60.0)
        self.painter.game = self.game_widget
        self.game_widget.add_widget(self.painter)

        # self.right_panel = RightPanelWidget()
        # buttons = Buttons()
        # buttons.set_bindinds(self.clear_canvas, self.save, self.load)
        graph = GraphWidget()
        graph.nb_pointsdisplay = 500
        graph.game_widget = self.game_widget
        # self.right_panel.add_widget(buttons)
        # self.right_panel.add_widget(graph)

        root = RootWidget()
        root.add_widget(self.game_widget)
        root.add_widget(graph)

        return root

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.game_widget.reset_sand()

    def save(self, obj):
        print("saving brain...")
        self.brain.save()
        # plt.plot(self.scores)
        # plt.show()

    def load(self, obj):
        print("loading last saved brain...")
        self.brain.load()


# Running the whole thing
if __name__ == '__main__':
    Window.size = (1080, 1024)
    car_app = CarApp()
    CarApp().run()
