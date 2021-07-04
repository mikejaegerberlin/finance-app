from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from backend.demo_setup import DemoData as data
from kivy.metrics import dp
from kivymd.uix.picker import MDDatePicker


class AddValueDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AddValueDialogContent, self).__init__(**kwargs)
        
    def update_acc_items(self):
        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]

        self.acc_dropdown.items = self.acc_menu_items


    def on_kv_post(self, instance):
        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]
        self.acc_dropdown = MDDropdownMenu(
            caller=self.ids.accountfield,
            items=self.acc_menu_items,
            position="bottom",
            width_mult=4,
        )

        self.dialog_date = MDDatePicker(primary_color=Colors.primary_color, selector_color=Colors.primary_color, 
                                        text_button_color=Colors.primary_color, text_color=Colors.bg_color, specific_text_color=Colors.bg_color,
                                        size_hint_y=None, text_weekday_color=Colors.bg_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)
        self.ids.datefield.text = self.dialog_date.today.strftime('%Y-%m-%d')
        

    def dialog_date_ok(self, instance, value, date_range):
        date = value.strftime('%Y-%m-%d')
        self.ids.datefield.text = date
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        self.ids.accountfield.focus = False
    
    def dialog_date_cancel(self, instance, value):
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        self.ids.accountfield.focus = False
    

    def open_acc_dropdown(self, accountfield):
        accountfield.hide_keyboard()
        self.acc_dropdown.caller = accountfield
        self.acc_dropdown.open()
        self.ids.purposefield.focus     = False
        self.ids.amountfield.focus      = False

    def set_acc_item(self, text_item):
        self.acc_dropdown.caller.text = text_item
        self.acc_dropdown.dismiss()
        self.acc_dropdown.caller.focus = False
        self.focus_function()

    def purposefield_function(self):
        if self.ids.purposefield.hint_text == "Purpose":
            self.focus_function()
        else:
            self.acc_dropdown.caller = self.ids.purposefield
            self.acc_dropdown.open()
            self.ids.amountfield.focus      = False
            self.ids.accountfield.focus     = False


        
    def income_button_clicked(self):
        self.ids.accountfield.hint_text = "Account"
        self.ids.purposefield.text = ""
        self.ids.purposefield.hint_text = "Purpose"
        self.ids.purposefield.icon_right = ""
        self.ids.purposefield.keyboard_mode = 'auto'

        if self.ids.dialog_income_button_icon.color[1] == 0:
            self.ids.dialog_income_button_icon.color = Colors.green_color
            self.ids.dialog_income_button_text.color = Colors.green_color
            self.ids.dialog_expenditure_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_text.color = Colors.button_disable_onwhite_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass
    def expenditure_button_clicked(self):
        self.ids.accountfield.hint_text = "Account"
        self.ids.purposefield.text = ""
        self.ids.purposefield.hint_text = "Purpose"
        self.ids.purposefield.icon_right = ""
        self.ids.purposefield.keyboard_mode = 'auto'

        if self.ids.dialog_expenditure_button_icon.color[0] == 0:
            self.ids.dialog_income_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_income_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button_text.color = Colors.error_color
            self.ids.dialog_expenditure_button_icon.color = Colors.error_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass      

    def transfer_button_clicked(self):
        self.ids.accountfield.hint_text = "Account (from)"
        self.ids.purposefield.text = ""
        self.ids.purposefield.hint_text = "Account (to)"
        self.ids.purposefield.icon_right = "arrow-down-drop-circle-outline"
        self.ids.purposefield.keyboard_mode = 'managed'

        if self.ids.dialog_transfer_button_icon.color[0] == 0:
            self.ids.dialog_transfer_button_icon.color = Colors.primary_color
            self.ids.dialog_transfer_button_text.color = Colors.primary_color
            self.ids.dialog_expenditure_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_income_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_income_button_text.color = Colors.button_disable_onwhite_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass     

    def focus_function(self):
        self.ids.accountfield.focus = False
        if self.ids.dialog_income_button_icon.color[1] == 0:
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