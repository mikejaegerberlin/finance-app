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
from screens.transfers_screen import TransfersScreen
from screens.accounts_screen import AccountsScreen
from screens.overview_screen import OverviewScreen
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (400,700)
        #self.create_items_for_dropdowns_and_buttons()
        self.slider_labelsize_current = Sizes.labelsize
        self.slider_titlesize_current = Sizes.titlesize
        self.slider_linewidth_current = Sizes.linewidth
        self.slider_markersize_current = Sizes.markersize

        self.bg_color                     = Colors.bg_color
        self.bg_color_light               = Colors.bg_color_light
        self.text_color                   = Colors.text_color
        self.primary_color                = Colors.primary_color
        self.button_disable_onwhite_color = Colors.button_disable_onwhite_color
        self.error_color                  = Colors.error_color
        self.black_color                  = Colors.black_color
        self.green_color                  = Colors.green_color
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name='Main'))
        sm.add_widget(TransfersScreen(name='Transfers'))
        self.screen = Builder.load_file("main.kv")
        ### Get relevant ids form kv file###
        self.create_dialogs()

        #execute this block if demodata is load from json   
        reset_date = datetime.strptime(data.standingorders['Reset date'], '%Y-%m-%d').date() 
        if data.today_date.month!=reset_date.month:
            data.reset_standingorders_monthlisted()
            data.standingorders['Reset date'] = self.today_str
            data.save_standingorders()
        for acc in data.accounts:
            data.check_standingorders(acc)
            data.fill_status_of_account(acc)
            data.check_todays_status(acc)            
        data.save_accounts()
        data.save_standingorders()

    
    def create_dialogs(self):
        self.dialog_money_transfer = MDDialog(
                title="Money transfer",
                type="custom",
                content_cls=MoneyTransferDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_money_transfer.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Add': self.execute_money_transfer(x)
                    ),
                ],
            )               
        
    def execute_money_transfer(self, instance):
        amount        = self.money_transfer_amountfield.text
        account_from  = self.money_transfer_accountfield_from.text
        account_to    = self.money_transfer_accountfield_to.text
        date          = self.money_transfer_datefield.text
        messagestring = ''
        try:
            amount = round(float(amount),2)
        except:
            messagestring += 'Amount field must be number. '
        messagestring += 'Account field from is empty. ' if account_from=='' else ''
        messagestring += 'Account field to is empty.' if account_to=='' else ''   
        messagestring += 'Account field from and to are same. ' if account_from==account_to else ''
        if messagestring!='':
            message = Snackbar(text=messagestring)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_money_transfer.dismiss()
            message = Snackbar(text="Transfered {} € from {} to {}".format(amount, account_from, account_to))
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.money_transfer_amountfield.text  = ''
            self.money_transfer_accountfield_from.text = ''
            self.money_transfer_accountfield_to.text = ''
            self.money_transfer_datefield.text = data.today_str
            
            #insert transfer into transfers_list and update account status
            if date in data.accounts[account_to]['Transfers'].keys():
                data.accounts[account_to]['Transfers'][date].append([amount, 'From {} to {}'.format(account_from, account_to)])
            else:
                data.accounts[account_to]['Transfers'][date] = [[amount, 'From {} to {}'.format(account_from, account_to)]]
            if date in data.accounts[account_from]['Transfers'].keys():
                data.accounts[account_from]['Transfers'][date].append([-amount, 'From {} to {}'.format(account_from, account_to)])
            else:
                data.accounts[account_from]['Transfers'][date] = [[-amount, 'From {} to {}'.format(account_from, account_to)]] 

            data.fill_status_of_account(account_to)
            data.fill_status_of_account(account_from)
            self.update_main_accountview(account_to)
            self.update_main_accountview(account_from)
            data.save_accounts()

  

    def update_sizes(self):
        Sizes.labelsize = int(self.dialog_settings.content_cls.ids.slider_labelsize.value)
        Sizes.titlesize = int(self.dialog_settings.content_cls.ids.slider_titlesize.value)
        Sizes.linewidth = int(self.dialog_settings.content_cls.ids.slider_linewidth.value)
        Sizes.markersize = int(self.dialog_settings.content_cls.ids.slider_markersize.value)
        Sizes.save()
        self.update_plot()
            
    def build(self):
        return self.screen
        

     

    

App = DemoApp()
App.run()