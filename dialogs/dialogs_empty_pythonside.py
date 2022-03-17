from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivymd.uix.snackbar import Snackbar
from backend.demo_setup import DemoData as data
from kivy.metrics import dp

class ChangeTransferitemContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ChangeTransferitemContent, self).__init__(**kwargs)

    def on_kv_post(self, instance):
        self.dialog_date = MDDatePicker(primary_color=Colors.primary_color, selector_color=Colors.primary_color, 
                                        text_button_color=Colors.primary_color, text_color=Colors.bg_color, specific_text_color=Colors.bg_color,
                                        size_hint_y=None, text_weekday_color=Colors.bg_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)
        
    def dialog_date_ok(self, instance, value, date_range):
        date_str = value.strftime('%Y-%m-%d')
        date_date = datetime.strptime(date_str, '%Y-%m-%d').date() 
        if date_date>data.today_date:
            message = Snackbar(text='Date cannot be higher than today.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.ids.datefield.text = data.today_str
        else:
            self.ids.datefield.text = date_str
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        
    
    def dialog_date_cancel(self, instance, value):
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        
    def open_dialog_date(self):
        self.dialog_date.open()

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



