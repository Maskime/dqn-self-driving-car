from kivy.clock import Clock

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class MapDialog(BoxLayout):
    filename_input = ObjectProperty(None)
    cancel_btn = ObjectProperty(None)
    save_btn = ObjectProperty(None)

    save_mode = True

    def __init__(self, **kwargs):
        super(MapDialog, self).__init__(**kwargs)
        if 'save_mode' not in kwargs:
            return
        self.save_mode = kwargs['save_mode']
        if not self.save_mode:
            self.save_btn.text = 'Load'

