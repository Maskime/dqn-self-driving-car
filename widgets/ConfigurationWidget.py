from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty


class ConfigurationWidget(BoxLayout):

    gammarate_txt = ObjectProperty(None)
    save_btn = ObjectProperty(None)
    cancel_btn = ObjectProperty(None)
