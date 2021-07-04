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
from screens.categories_screen import CategoriesScreen
from screens.transfers_screen import TransfersScreen
from screens.accounts_screen import AccountsScreen
from screens.overview_screen import MainScreen
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.screenmanager import FadeTransition

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (400,700)
        
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
        self.white_color                  = Colors.white_color
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name='Main'))
        sm.add_widget(TransfersScreen(name='Transfers'))
        sm.add_widget(StandingOrdersScreen(name='Standing order'))
        sm.add_widget(AccountsScreen(name='Accounts'))
        sm.add_widget(CategoriesScreen(name='Categories'))
        
        ### prepare data for start
        reset_date = datetime.strptime(data.standingorders['Reset date'], '%Y-%m-%d').date() 
        if data.today_date.month!=reset_date.month:
            data.reset_standingorders_monthlisted()
            data.standingorders['Reset date'] = data.today_str
            data.save_standingorders()
        for acc in data.accounts:
            data.check_standingorders(acc)
            data.fill_status_of_account(acc)
            data.check_todays_status(acc)  
        data.fill_total_status()          
        data.save_accounts()
        data.save_standingorders()

        self.screen = Builder.load_file("main.kv")
        
        ### Get relevant ids form kv file###
        self.on_kv_post_MainScreen()
        self.on_kv_post_AccountsScreen()
        self.on_kv_post_StandingOrdersScreen()
        

    def on_kv_post_MainScreen(self):
        self.screen.ids.main.update_plot()
        self.screen.ids.main.add_things_to_screen()

    def on_kv_post_AccountsScreen(self):
        self.screen.ids.accounts_screen.update_plot()
        self.screen.ids.accounts_screen.add_account_status_to_mainscreen()

    def on_kv_post_StandingOrdersScreen(self):
        self.screen.ids.standingorders_screen.create_screen()
        ID = self.screen.ids.standingorders_screen.dialog_add_standingorder.content_cls.ids.accountfield
        self.screen.ids.standingorders_screen.dialog_add_standingorder.content_cls.acc_dropdown.caller = ID
        
    def go_to_accounts(self):
        self.screen.ids.main.manager.transition = FadeTransition()
        self.screen.ids.main.manager.current = 'Accounts'

    def go_to_standingorders(self):
        self.screen.ids.main.manager.transition = FadeTransition()
        self.screen.ids.main.manager.current = 'Standing order'

    def go_to_main(self):
        self.screen.ids.main.manager.transition = FadeTransition()
        self.screen.ids.main.manager.current = 'Main' 

    def go_to_categories(self):
        self.screen.ids.main.manager.transition = FadeTransition()
        self.screen.ids.main.manager.current = 'Categories' 

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