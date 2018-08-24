from kivy.uix.gridlayout import GridLayout


class RightPanelWidget(GridLayout):
    def __init__(self, **kwargs):
        super(RightPanelWidget, self).__init__(**kwargs)
        self.rows = 3
        self.cols = 1
        self.size_hint = (0.3, 1)
