from kivymd.uix.boxlayout import MDBoxLayout

class AddValueDialogContent(MDBoxLayout):
    def __init__(self, Colors, **kwargs):
        super(AddValueDialogContent, self).__init__(**kwargs)
        self.Colors = Colors
        
    def income_button_clicked(self):
        if self.ids.dialog_income_button.text_color[1] == 0:
            self.ids.dialog_income_button.text_color = self.Colors.green_color
            self.ids.dialog_income_button.line_color = self.Colors.green_color
            self.ids.dialog_income_button.icon_color = self.Colors.green_color
            self.ids.dialog_expenditure_button.text_color = self.Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button.line_color = self.Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button.icon_color = self.Colors.button_disable_onwhite_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass
    def expenditure_button_clicked(self):
        if self.ids.dialog_expenditure_button.text_color[0] == 0:
            self.ids.dialog_income_button.text_color = self.Colors.button_disable_onwhite_color
            self.ids.dialog_income_button.line_color = self.Colors.button_disable_onwhite_color
            self.ids.dialog_income_button.icon_color = self.Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button.text_color = self.Colors.error_color
            self.ids.dialog_expenditure_button.line_color = self.Colors.error_color
            self.ids.dialog_expenditure_button.icon_color = self.Colors.error_color 
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass      
    def focus_function(self):
        self.ids.accountfield.focus = False
        if self.ids.dialog_income_button.text_color[1] == 0:
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass
        else:
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass