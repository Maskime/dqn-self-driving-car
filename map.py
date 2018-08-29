# Self Driving Car

# Importing the libraries
# Importing the Kivy packages
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Importing the Dqn object from our AI in ai.py
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from ai import Dqn
# Importing widget that are outside this file for kivy
from widgets.ButtonsWidget import Buttons
from widgets.ConfigurationWidget import ConfigurationWidget
from widgets.GameWidget import Game
from widgets.GraphWidget import GraphWidget
from widgets.PaintWidget import PaintWidget
from widgets.ConfigValueWidget import ConfigValueWidget

# Adding this line if we don't want the right click to put a red point
from widgets.TopMenuWidget import TopMenuWidget

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class RootWidget(BoxLayout):
    pass


# Adding the API Buttons (clear, save and load)
class CarApp(App):
    brain = Dqn(5, 3, 0.9)
    scores = []
    game_widget = None
    right_panel = None
    paused = False
    configuration_popup = None

    def __init__(self, **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.painter = PaintWidget()

    def build(self):
        self.game_widget = Game()
        self.game_widget.brain = self.brain
        self.game_widget.scores = self.scores
        self.game_widget.serve_car()

        Clock.schedule_interval(self.game_widget.update, 1.0 / 60.0)
        self.painter.game = self.game_widget
        self.game_widget.add_widget(self.painter)

        graph = GraphWidget()
        graph.size_hint = (1, 0.3)
        graph.game_widget = self.game_widget

        action_bar = TopMenuWidget()
        action_bar.pause_btn.bind(on_release=self.pause_resume)
        action_bar.save_btn.bind(on_release=self.save)
        action_bar.load_btn.bind(on_release=self.load)
        action_bar.clear_btn.bind(on_release=self.clear_canvas)
        action_bar.config_btn.bind(on_release=self.show_configuration)

        root = RootWidget()
        root.add_widget(action_bar)
        root.add_widget(graph)
        root.add_widget(self.game_widget)

        return root

    def pause_resume(self, btn=None):
        self.paused = not self.paused
        self.game_widget.pause_resume()
        if not self.paused:
            Clock.schedule_interval(self.game_widget.update, 1.0 / 60.0)

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

    def show_configuration(self, btn):
        self.pause_resume()
        content = ConfigurationWidget()
        self.configuration_popup = Popup(content=content, auto_dismiss=False, title='Configuration')
        self.configuration_popup.open()
        content.save_btn.bind(on_release=self.save_configuration)
        content.cancel_btn.bind(on_release=self.close_configuration)

    def save_configuration(self, btn):
        self.pause_resume()
        self.configuration_popup.dismiss()

    def close_configuration(self, btn):
        self.pause_resume()
        self.configuration_popup.dismiss()



# Running the whole thing
if __name__ == '__main__':
    Window.size = (1080, 1024)
    car_app = CarApp()
    CarApp().run()
