from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
import backend
Backend = backend.Backend()

class Spacer_Vertical(MDBoxLayout):
    def __init__(self, height, **kwargs):
        super(Spacer_Vertical, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = height

class Spacer_Horizontal(MDBoxLayout):
    def __init__(self, width, **kwargs):
        super(Spacer_Horizontal, self).__init__(**kwargs)
        self.size_hint_x = width

class AddValueDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AddValueDialogContent, self).__init__(**kwargs)
        
    def income_button_clicked(self):
        if self.ids.dialog_income_button.text_color[2] == 0:
            self.ids.dialog_income_button.text_color = Backend.green_color
            self.ids.dialog_income_button.line_color = Backend.green_color
            self.ids.dialog_income_button.icon_color = Backend.green_color
            self.ids.dialog_expenditure_button.text_color = Backend.button_disable_onwhite_color
            self.ids.dialog_expenditure_button.line_color = Backend.button_disable_onwhite_color
            self.ids.dialog_expenditure_button.icon_color = Backend.button_disable_onwhite_color
    def expenditure_button_clicked(self):
        if self.ids.dialog_expenditure_button.text_color[2] == 0:
            self.ids.dialog_income_button.text_color = Backend.button_disable_onwhite_color
            self.ids.dialog_income_button.line_color = Backend.button_disable_onwhite_color
            self.ids.dialog_income_button.icon_color = Backend.button_disable_onwhite_color
            self.ids.dialog_expenditure_button.text_color = Backend.error_color
            self.ids.dialog_expenditure_button.line_color = Backend.error_color
            self.ids.dialog_expenditure_button.icon_color = Backend.error_color       

class SettingsDialogContent(MDBoxLayout):
    pass
