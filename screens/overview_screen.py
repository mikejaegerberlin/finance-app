from logging import root
from kivymd import app
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd import images_path
from kivymd.icon_definitions import md_icons
from kivymd.uix.dialog import MDDialog
from kivymd.font_definitions import theme_font_styles
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.graphics import *
from datetime import datetime
from dateutil.relativedelta import relativedelta 
from dialogs.custom_datepicker import DatePickerContent
from dialogs.add_value_dialog import AddValueDialogContent
from dialogs.dialogs_empty_pythonside import ChangeTransferitemContent
from dialogs.dialogs_empty_pythonside import SettingsDialogContent
from dialogs.dialogs_empty_pythonside import Spacer_Horizontal, Spacer_Vertical
from dialogs.dialogs_empty_pythonside import MoneyTransferDialogContent
from dialogs.add_transfer_dialog import AddTransferDialogContent
from kivymd.uix.picker import MDDatePicker
from backend.colors import Colors
from backend.totalplot import TotalPlot
from backend.demo_setup import DemoData as data
from backend.settings import Sizes
from backend.carditems import CardItemsBackend
from screens.standing_order_screen import StandingOrdersScreen
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from dialogs.add_value_dialog import AddValueDialogContent
from screens.transfers_screen import TransfersScreen

class OverviewScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super(OverviewScreen, self).__init__(**kwargs)
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']

    def on_kv_post(self, instance):
        self.filter_buttons = [self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        self.update_plot()
        self.add_things_to_screen()
        self.dialog_add_value = MDDialog(
                type="custom",
                content_cls=AddValueDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_add_value.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Add': self.add_value(x)
                    ),
                ],
            )

    
    def add_value(self, instance):  
        self.dialog_add_value.content_cls.focus_function()
        amount        = self.dialog_add_value.content_cls.ids.amountfield.text
        account       = self.dialog_add_value.content_cls.ids.accountfield.text
        purpose       = self.dialog_add_value.content_cls.ids.purposefield.text
        date          = self.dialog_add_value.content_cls.ids.datefield.text
        messagestring = ''
        try:
            amount = round(float(amount),2)
        except:
            messagestring += 'Amount field must be number. '
        messagestring += 'Account field is empty. ' if account=='' else ''
        messagestring += 'Purpose field is empty.' if purpose=='' else ''   
        if messagestring!='':
            message = Snackbar(text=messagestring)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_add_value.dismiss()
            message = Snackbar(text="Added {} € to {} for {}".format(amount, account, purpose))
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.dialog_add_value.content_cls.ids.amountfield.text  = ''
            self.dialog_add_value.content_cls.ids.accountfield.text = ''
            self.dialog_add_value.content_cls.ids.purposefield.text = ''
            self.dialog_add_value.content_cls.ids.datefield.text = data.today_str
            
            #insert transfer into transfers_list and update account status
            if date in data.accounts[account]['Transfers'].keys():
                data.accounts[account]['Transfers'][date].append([amount, purpose])
            else:
                data.accounts[account]['Transfers'][date] = []
                data.accounts[account]['Transfers'][date].append([amount, purpose])
            data.fill_status_of_account(account)
            data.fill_total_status()
            self.update_plot()
            self.add_things_to_screen()
            data.save_accounts()
        
        
    def button_clicked(self, instance):
        for button in self.filter_buttons:
            if button==instance:
                button.md_bg_color = Colors.text_color
                button.text_color  = Colors.bg_color
            else:
                button.md_bg_color = Colors.bg_color
                button.text_color  = Colors.text_color
        self.update_plot()
 
    def update_plot(self):
        canvas    = TotalPlot.make_plot(self.filter_buttons, data, set_xticks=False)
        canvas.size_hint_y = 0.75
        canvas.pos_hint = {'top': 0.98}

        canvas2 = TotalPlot.make_plot(self.filter_buttons, data, set_xticks=True)
        canvas2.size_hint_y = 0.35
        canvas2.pos_hint = {'top': 0.25}

        
        self.ids.assetview.clear_widgets()
        self.ids.assetview.add_widget(canvas)
        self.ids.assetview.add_widget(canvas2)
        label = MDLabel(text='Total status (monthly)', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 1})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)

        label2 = MDLabel(text='Monthly profit', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.08, halign='center', pos_hint={'top': 0.3})
        label2.color = Colors.text_color
        self.ids.assetview.add_widget(label2)
       
    def add_things_to_screen(self):
        self.ids.status_label.text = str(data.total['Status'][data.today_str])+' €'
        self.ids.status_label.color = Colors.green_color if data.total['Status'][data.today_str]>=0 else Colors.error_color

        self.ids.month_label.text = 'Status '+self.months[int(data.today_date.month)-1]+' '+str(data.today_date.year)
        profit = round(TotalPlot.profits_date[self.months[int(data.today_date.month)-1]+' '+str(data.today_date.year)], 2)

        self.ids.status_month_label.text = str(profit)+' €'
        self.ids.status_month_label.color = Colors.green_color if profit>=0 else Colors.error_color
   