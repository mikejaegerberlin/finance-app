from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from datetime import datetime
from backend.demo_setup import DemoData as data
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar

class ManageAccountsDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ManageAccountsDialogContent, self).__init__(**kwargs)     
        self.amountfield = MDTextField()
        self.amountfield.hint_text               = "Start amount (€)"
        self.amountfield.line_color_normal       = Colors.button_disable_onwhite_color
        self.amountfield.line_color_focus        = Colors.bg_color
        self.amountfield.hint_text_color_normal  = Colors.bg_color
        self.amountfield.hint_text_color_focus   = Colors.bg_color
        self.amountfield.text_color_normal       = Colors.bg_color
        self.amountfield.text_color_focus        = Colors.bg_color
        self.datebox = MDBoxLayout(orientation='horizontal')
        self.datefield   = MDTextField()
        self.datefield.hint_text               = "Date"
        self.datefield.line_color_normal       = Colors.button_disable_onwhite_color
        self.datefield.line_color_focus        = Colors.bg_color
        self.datefield.hint_text_color_normal  = Colors.bg_color
        self.datefield.hint_text_color_focus   = Colors.bg_color
        self.datefield.text_color_normal       = Colors.bg_color
        self.datefield.text_color_focus        = Colors.bg_color
        self.datefield.disabled                = True
        self.datefield.text                    = data.today_str
        self.datebox.add_widget(self.datefield)
        button = MDIconButton()
        button.icon="calendar"
        button.theme_text_color="Custom"
        button.text_color=Colors.bg_color
        button.on_release = lambda x='i': self.open_dialog_date(x)
        self.datebox.add_widget(button)

        self.add_widget(self.amountfield)
        self.add_widget(self.datebox)
    
    def reset_dialog_after_dismiss(self):
        self.add_account_button_clicked()
      
    def open_dialog_date(self, instance):
        self.dialog_date.open()

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
            caller=MDFlatButton(),
            items=self.acc_menu_items,
            position="bottom",
            width_mult=4,
        )

        self.dialog_date = MDDatePicker(primary_color=Colors.primary_color, selector_color=Colors.primary_color, 
                                        text_button_color=Colors.primary_color, text_color=Colors.bg_color, specific_text_color=Colors.bg_color,
                                        size_hint_y=None, text_weekday_color=Colors.bg_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)

        
    def add_account_button_clicked(self):
        try:
            self.remove_widget(self.sudo_label1)
            self.remove_widget(self.sudo_label2)
            self.add_widget(self.amountfield)
            self.add_widget(self.datebox)
        except:
            pass
        self.height = "220dp"
        self.ids.accountfield.hint_text = 'Account name'
        self.ids.accountfield.text = ''
        self.ids.accountfield.keyboard_mode = 'auto'
        self.ids.accountfield.icon_right = ""
        self.amountfield.focus = False
        self.ids.accountfield.focus = False   
        if self.ids.add_account_button_icon.color[1] == 0:
            self.ids.add_account_button_icon.color = Colors.green_color
            self.ids.add_account_button_text.color = Colors.green_color
            self.ids.remove_account_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.remove_account_button_text.color = Colors.button_disable_onwhite_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass

    def accountfield_focus_function(self):
        if self.ids.accountfield.hint_text == 'Which account':
            self.acc_dropdown.caller = self.ids.accountfield
            self.acc_dropdown.open() 
        self.amountfield.focus = False

    def remove_account_button_clicked(self):

        if len(data.accounts)<1:
            message = Snackbar(text='No accounts yet.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.remove_widget(self.datebox)
            self.remove_widget(self.amountfield)
            self.sudo_label1 = MDLabel()
            self.sudo_label2 = MDLabel()
            self.add_widget(self.sudo_label1)
            self.add_widget(self.sudo_label2)

            self.ids.accountfield.hint_text = 'Which account'
            self.ids.accountfield.text = ''
            self.ids.accountfield.icon_right = "arrow-down-drop-circle-outline"
            self.ids.accountfield.keyboard_mode = 'managed'    
            self.amountfield.focus = False
            self.ids.accountfield.focus = False   

            if self.ids.remove_account_button_icon.color[0] == 0:
                self.ids.add_account_button_icon.color = Colors.button_disable_onwhite_color
                self.ids.add_account_button_text.color = Colors.button_disable_onwhite_color
                self.ids.remove_account_button_icon.color = Colors.error_color
                self.ids.remove_account_button_text.color = Colors.error_color
                try:
                    amount = float(self.ids.amountfield.text)
                    if amount>0:
                        self.ids.amountfield.text = str(-amount)
                except:
                    pass      

    def dialog_date_ok(self, instance, value, date_range):
        date = value.strftime('%Y-%m-%d')
        self.datefield.text = date
        self.amountfield.focus = False
        self.ids.accountfield.focus = False
    
    def dialog_date_cancel(self, instance, value):
        self.amountfield.focus = False
        self.ids.accountfield.focus = False

    def open_acc_dropdown(self, accountfield):
        accountfield.hide_keyboard()
        self.acc_dropdown.open()
        self.amountfield.focus      = False

    def set_acc_item(self, text_item):
        self.acc_dropdown.caller.text = text_item
        self.acc_dropdown.dismiss()
        self.acc_dropdown.caller.focus = False
        