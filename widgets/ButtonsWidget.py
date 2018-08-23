from kivy.uix.widget import Widget


class Buttons(Widget):

    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)
        clearbtn = Button(text='clear')
        savebtn = Button(text='save', pos=(self.game_widget.width, 0))
        loadbtn = Button(text='load', pos=(2 * self.game_widget.width, 0))
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)

        self.add_widget(clearbtn)
        self.add_widget(savebtn)
        self.add_widget(loadbtn)