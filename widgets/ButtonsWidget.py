from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


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
        self.size_hint = (0.5, 0.2)

        self.clear_btn = Button(text='clear')
        self.save_btn = Button(text='save')
        self.load_btn = Button(text='load')

        self.add_widget(self.clear_btn)
        self.add_widget(self.save_btn)
        self.add_widget(self.load_btn)

    def set_bindinds(self, clear_callback, save_callback, load_callback):
        self.clear_btn.bind(on_release=clear_callback)
        self.save_btn.bind(on_release=save_callback)
        self.load_btn.bind(on_release=load_callback)
