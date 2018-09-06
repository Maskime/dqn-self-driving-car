from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar


class TopMenuWidget(ActionBar):
    save_map_button = ObjectProperty(None)
    save_brain_button = ObjectProperty(None)
    load_btn = ObjectProperty(None)
    clear_btn = ObjectProperty(None)
    config_btn = ObjectProperty(None)
