from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class Buttons(GridLayout):
    clear_callback = None
    save_callback = None
    load_callback = None

    clear_btn = None
    save_btn = None
    load_btn = None

    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)
        self.cols = 3
        self.size_hint = (0.2, 1)

        self.clear_btn = Button(text='clear')
        self.save_btn = Button(text='save')
        self.load_btn = Button(text='load')

        # clearbtn.bind(on_release=self.clear_callback)
        # savebtn.bind(on_release=self.save_callback)
        # loadbtn.bind(on_release=self.load_callback)
        #

        self.add_widget(self.clear_btn)
        self.add_widget(self.save_btn)
        self.add_widget(self.load_btn)
