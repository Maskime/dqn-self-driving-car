from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar


class TopMenuWidget(ActionBar):
    save_btn = ObjectProperty(None)
    load_btn = ObjectProperty(None)
    clear_btn = ObjectProperty(None)
    config_btn = ObjectProperty(None)