from kivymd.uix.boxlayout import MDBoxLayout

class ChangeTransferitemContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ChangeTransferitemContent, self).__init__(**kwargs)

class SettingsDialogContent(MDBoxLayout):
    pass

class MoneyTransferDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(MoneyTransferDialogContent, self).__init__(**kwargs)

class Spacer_Vertical(MDBoxLayout):
    def __init__(self, height, **kwargs):
        super(Spacer_Vertical, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = height

class Spacer_Horizontal(MDBoxLayout):
    def __init__(self, width, **kwargs):
        super(Spacer_Horizontal, self).__init__(**kwargs)
        self.size_hint_x = width



