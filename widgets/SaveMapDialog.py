from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class SaveMapDialog(BoxLayout):
    filename_input = ObjectProperty(None)
    cancel_btn = ObjectProperty(None)
    save_btn = ObjectProperty(None)