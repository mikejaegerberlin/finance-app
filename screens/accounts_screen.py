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
from kivymd.uix.picker import MDDatePicker
from backend.colors import Colors
from backend.accountplot import AccountPlot
from backend.demo_setup import DemoData as data
from backend.settings import Sizes
from backend.carditems import CardItemsBackend
from screens.standing_order_screen import StandingOrdersScreen
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from dialogs.add_value_dialog import AddValueDialogContent
from screens.transfers_screen import TransfersScreen

class AccountsScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super(AccountsScreen, self).__init__(**kwargs)

    def on_kv_post(self, instance):
        self.filter_buttons = [self.ids.onemonth_button, self.ids.threemonths_button, self.ids.sixmonths_button, 
                               self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        self.add_account_status_to_mainscreen()
        self.update_plot()
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

    def on_pre_enter(self):
        for acc in data.accounts:
            self.update_main_accountview(acc)
        self.update_plot()

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
            self.update_main_accountview(account)
            self.update_plot()
            data.fill_total_status()
            self.app.screen.ids.main.overview_screen.update_plot()
            self.app.screen.ids.main.overview_screen.add_things_to_screen()
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
        canvas    = AccountPlot.make_plot(self.filter_buttons, data)
        canvas.pos_hint = {'top': 1}
        self.ids.assetview.clear_widgets()
        self.ids.assetview.add_widget(canvas)
        label = MDLabel(text='Trend of each account', font_style='Subtitle1', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 1})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)

    def update_main_accountview(self, account):
            self.AmountLabels[account].text     = str(data.accounts[account]['Status'][data.today_str])+' €'
            if data.accounts[account]['Status'][data.today_str]<0:
                self.AmountLabels[account].color = Colors.error_color
            else:
                self.AmountLabels[account].color = Colors.green_color
           

    def go_to_account(self, acc):
        data.current_account = acc
        self.app.screen.ids.main.manager.current = 'Transfers'


    def generate_main_carditem(self, acc, color):
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, on_release=lambda x=acc:self.go_to_account(acc))
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[20,20,20,20])   

        subbox = MDBoxLayout(orientation='horizontal')
        icon = MDIcon(icon='vector-line', theme_text_color='Custom')
        icon.color=color
        icon.halign = 'right'
        label2 = MDLabel(text=acc, font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'left'
        subbox.add_widget(icon)
        subbox.add_widget(label2)   
        #acclabel   = MDLabel(text=acc, font_style='Subtitle2')
        #acclabel.color = Colors.text_color
        #acclabel.halign = 'center'
        contentbox.add_widget(subbox)
    
        last_date = list(data.accounts[acc]['Status'].keys())
        last_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
        last_date = last_date[-1]
        
        amlabel = MDLabel(text=str(data.accounts[acc]['Status'][last_date])+' €', font_style='Subtitle2')
        amlabel.color = Colors.error_color if data.accounts[acc]['Status'][last_date]<0 else Colors.green_color
        amlabel.halign = 'center'
        self.AmountLabels[acc] = amlabel
        contentbox.add_widget(amlabel)
        contentbox.add_widget(MDLabel())
        card.add_widget(contentbox)
        
        return card

    def add_account_status_to_mainscreen(self):

        canvas = AccountPlot.make_plot(self.filter_buttons, data)
        canvas.pos_hint = {'top': 1}
        self.ids.assetview.add_widget(canvas)
        label = MDLabel(text='Trend of each account', font_style='Subtitle1', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 1})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)
        self.AmountLabels = {}

        #header of table scrollview
        header = self.ids.accountsview_header
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(Spacer_Horizontal(0.05))
        
        labels = ['Account', 'Current Status', 'Month Status']
        for label in labels:
            header_label = MDLabel(text=label, font_style="Subtitle2")
            header_label.color = Colors.text_color
            header_label.halign = 'center'
            header.add_widget(header_label)

        #scrollview items
        for i, acc in enumerate(data.accounts):
            carditem = self.generate_main_carditem(acc, color=Colors.matplotlib_rgba[i])
            self.ids.accountsview.add_widget(carditem)
            self.ids.accountsview.add_widget(Spacer_Vertical('6dp'))
      
