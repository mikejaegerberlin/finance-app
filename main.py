import time
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.graphics import *
from datetime import datetime
from backend.colors import Colors
from backend.demo_setup import DemoData as data
from backend.settings import Sizes
from screens.standing_order_screen import StandingOrdersScreen
from screens.categories_screen import CategoriesScreen
from screens.transfers_screen import TransfersScreen
from screens.accounts_screen import AccountsScreen
from screens.overview_screen import MainScreen
from kivy.uix.screenmanager import FadeTransition
from backend.settings import ScreenSettings
from kivy.utils import platform
import threading


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.demo_mode = False
        self.Window = Window
        if platform != 'android':
            self.Window.size = (400,700)
        
     
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

        #data.today_str  = '2021-12-02'
        #data.today_date = datetime.strptime(data.today_str, '%Y-%m-%d').date()
        #data.reset_standingorders_monthlisted()
        ## prepare data for start
        for acc in data.accounts:
            data.check_standingorders(acc)
            data.fill_status_of_account(acc)
            data.check_todays_status(acc)  

        reset_date = datetime.strptime(data.standingorders['Reset date'], '%Y-%m-%d').date() 
        if data.today_date.month!=reset_date.month or data.today_date.year!=reset_date.year:
            data.reset_standingorders_monthlisted()
            data.standingorders['Reset date'] = data.today_str
            data.save_standingorders(self.demo_mode)
        
        data.fill_total_status()          
        data.save_accounts(self.demo_mode)
        data.save_standingorders(self.demo_mode)
        data.filter_categories_within_dates(data.first_of_month_date, data.today_date)   
     
        self.screen = Builder.load_file("main.kv")
        ### Get relevant ids form kv file###
        #screen1 = threading.Thread(target=self.on_kv_post_MainScreen())
        #screen2 = threading.Thread(target=self.on_kv_post_AccountsScreen())
        #screen3 = threading.Thread(target=self.on_kv_post_StandingOrdersScreen())
        #screen4 = threading.Thread(target=self.on_kv_post_CategoriesScreen())
        
        #screen1.start()
        #screen2.start()
        #screen3.start()
        #screen4.start()
        self.on_kv_post_MainScreen()
        self.on_kv_post_AccountsScreen()
        self.on_kv_post_StandingOrdersScreen()
        self.on_kv_post_CategoriesScreen() 
        
    def build(self):
        self.screen = Builder.load_file("main.kv")
        
        
        
    def get_start_and_end_date(self, year, month):
        start_date = datetime.strptime('{}-{}-01'.format(year, month), '%Y-%m-%d').date()
        days = ['31', '30', '29', '28']
        for day in days:
            try:
                end_date   = datetime.strptime('{}-{}-{}'.format(year, month, day), '%Y-%m-%d').date() 
                break
            except:
                pass
        return start_date, end_date


    def update_backend(self):
        for acc in data.accounts:
            data.fill_status_of_account(acc)
        data.fill_total_status() 
        data.save_accounts(self.demo_mode)
        ScreenSettings.save(self.demo_mode)

    def update_main_screen(self):
        self.update_backend()
        start_date, end_date = self.get_start_and_end_date(self.screen.ids.main.selected_year, self.screen.ids.main.selected_month)
        data.filter_categories_within_dates(start_date, end_date)  
        self.screen.ids.main.dialog_add_value.content_cls.update_acc_items()
        self.screen.ids.main.update_plot(filterbutton_clicked=False)
        self.screen.ids.main.add_things_to_screen()

    def update_accounts_screen(self):
        self.update_backend()
        self.screen.ids.accounts_screen.dialog_add_value.content_cls.update_acc_items()
        self.screen.ids.accounts_screen.update_plot()
        self.screen.ids.accounts_screen.dialog_manage_accounts.content_cls.update_acc_items()
        self.screen.ids.accounts_screen.dialog_graph_selection.content_cls.update_list()
        self.screen.ids.accounts_screen.add_account_status_to_mainscreen()
        
    def update_categories_screen(self):
        self.update_backend()
        self.screen.ids.categories_screen.dialog_add_category.content_cls.update_category_items()
        self.screen.ids.categories_screen.update_plot()
        self.screen.ids.categories_screen.dialog_graph_selection.content_cls.update_list()

    def update_standingorder_screen(self):
        self.update_backend()
        self.screen.ids.standingorders_screen.dialog_add_standingorder.content_cls.update_category_account_items()
        self.screen.ids.standingorders_screen.update_standingorder_list()


    def global_update(self):
        self.update_backend()
        self.update_main_screen()
        self.update_accounts_screen()
        self.update_categories_screen()
        self.update_standingorder_screen()
    
    def update_all(self):
        self.screen.ids.main.update_plot()
        self.screen.ids.accounts_screen.update_plot()
       
    def on_kv_post_MainScreen(self):
        self.screen.ids.main.update_plot(filterbutton_clicked=False)
        self.screen.ids.main.add_things_to_screen()

    def on_kv_post_AccountsScreen(self):
        self.screen.ids.accounts_screen.initialize_dialogs()
        self.screen.ids.accounts_screen.update_plot()
        self.screen.ids.accounts_screen.add_account_status_to_mainscreen()
        

    def on_kv_post_StandingOrdersScreen(self):
        self.screen.ids.standingorders_screen.create_screen()
        ID = self.screen.ids.standingorders_screen.dialog_add_standingorder.content_cls.ids.accountfield
        self.screen.ids.standingorders_screen.dialog_add_standingorder.content_cls.acc_dropdown.caller = ID

    def on_kv_post_CategoriesScreen(self):
        self.screen.ids.categories_screen.create_screen()
        
        #ID = self.screen.ids.categories_screen.dialog_add_standingorder.content_cls.ids.accountfield
        #self.screen.ids.standingorders_screen.dialog_add_standingorder.content_cls.acc_dropdown.caller = ID
        
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