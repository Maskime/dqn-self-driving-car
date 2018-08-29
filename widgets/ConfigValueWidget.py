from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class ConfigValueWidget(BoxLayout):

    inner_label = ObjectProperty(None)
    text = StringProperty(None)
    value = StringProperty(None)