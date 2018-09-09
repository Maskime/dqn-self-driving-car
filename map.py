# Self Driving Car

# Importing the libraries
# Importing the Kivy packages
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Importing the Dqn object from our AI in ai.py
from kivy.uix.popup import Popup

from Configuration import Configuration
from ai import Dqn
# Importing widget that are outside this file for kivy
from widgets.ButtonsWidget import Buttons
from widgets.ConfigurationWidget import ConfigurationWidget
from widgets.GameWidget import Game
from widgets.GraphWidget import GraphWidget
from widgets.PaintWidget import PaintWidget
from widgets.ConfigValueWidget import ConfigValueWidget

# Adding this line if we don't want the right click to put a red point
from widgets.MapDialog import MapDialog
from widgets.StatsWidget import StatsWidget
from widgets.TopMenuWidget import TopMenuWidget
from widgets.TopPanel import TopPanel

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class RootWidget(BoxLayout):
    pass


# Adding the API Buttons (clear, save and load)
class CarApp(App):
    scores = []
    game_widget = None
    right_panel = None
    paused = False
    current_popup = None
    config_widget = None
    top_panel = None
    stats_widget = None
    map_dialog = None

    def __init__(self, **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.painter = PaintWidget()
        self.self_driving_config = Configuration()
        self.self_driving_config.load()
        self.brain = Dqn(6, 3, self.self_driving_config)

    def build(self):
        self.game_widget = Game()
        self.game_widget.driving_config = self.self_driving_config
        self.game_widget.brain = self.brain
        self.game_widget.scores = self.scores
        self.game_widget.serve_car()

        Clock.schedule_interval(self.game_widget.update, 1.0 / 60.0)
        self.painter.game = self.game_widget
        self.game_widget.add_widget(self.painter)

        self.top_panel = TopPanel()
        self.top_panel.graph_widget.game_widget = self.game_widget
        self.game_widget.stats_widget = self.top_panel.stats_widget

        action_bar = TopMenuWidget()
        action_bar.pause_btn.bind(on_release=self.pause_resume)
        action_bar.save_brain_button.bind(on_release=self.save_brain)
        action_bar.save_map_button.bind(on_release=self.show_save_map)
        action_bar.load_btn.bind(on_release=self.load)
        action_bar.load_map_btn.bind(on_release=self.show_load_map)
        action_bar.clear_btn.bind(on_release=self.clear_canvas)
        action_bar.config_btn.bind(on_release=self.show_configuration)

        root = RootWidget()
        root.add_widget(action_bar)
        root.add_widget(self.top_panel)
        root.add_widget(self.game_widget)

        return root

    def put_stats(self, dt):
        print("Checking for stats")
        if self.top_panel.stats_widget is None:
            return
        print("stats widget now available")

        return False

    def pause_resume(self, btn=None):
        self.paused = not self.paused
        self.game_widget.pause_resume()
        self.top_panel.graph_widget.pause_resume()
        if not self.paused:
            Clock.schedule_interval(self.game_widget.update, 1.0 / 60.0)

    def clear_canvas(self, obj=None):
        self.painter.canvas.clear()
        self.game_widget.reset_sand()

    def save_brain(self, obj):
        print("saving brain...")
        self.brain.save()

    def show_save_map(self, obj):
        self.pause_resume()
        self.map_dialog = MapDialog()
        self.current_popup = Popup(content=self.map_dialog, auto_dismiss=False, title='Save Map',
                                   size_hint=(None, None), size=(400, 200))
        self.map_dialog.save_btn.bind(on_release=self.map_dialog_action)
        self.map_dialog.cancel_btn.bind(on_release=self.close_popup)
        self.current_popup.open()

    def show_load_map(self, obj):
        self.pause_resume()
        self.map_dialog = MapDialog(save_mode=False)
        self.current_popup = Popup(content=self.map_dialog, auto_dismiss=False, title='Load Map',
                                   size_hint=(None, None), size=(400, 200))
        self.map_dialog.save_btn.bind(on_release=self.map_dialog_action)
        self.map_dialog.cancel_btn.bind(on_release=self.close_popup)
        self.current_popup.open()

    def map_dialog_action(self, btn):
        if self.map_dialog.save_mode:
            self.painter.save(self.map_dialog.filename_input.text)
        else:
            self.clear_canvas()
            self.painter.load(self.map_dialog.filename_input.text)
        self.current_popup.dismiss()
        self.pause_resume()

    def load(self, obj):
        print("loading last saved brain...")
        self.brain.load()

    def show_configuration(self, btn):
        self.pause_resume()
        self.config_widget = ConfigurationWidget()
        self.config_widget.set_config(self.self_driving_config)
        self.current_popup = Popup(content=self.config_widget, auto_dismiss=False, title='Configuration')
        self.current_popup.open()
        self.config_widget.save_btn.bind(on_release=self.save_configuration)
        self.config_widget.cancel_btn.bind(on_release=self.close_popup)

    def save_configuration(self, btn):
        self.pause_resume()
        self.self_driving_config.update(self.config_widget.get_dict())
        self.game_widget.update_config(self.self_driving_config)
        self.clear_canvas()
        self.current_popup.dismiss()

    def close_popup(self, btn):
        self.pause_resume()
        self.current_popup.dismiss()


# Running the whole thing
if __name__ == '__main__':
    Window.size = (1080, 1024)
    car_app = CarApp()
    CarApp().run()
