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
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
import threading
from multiprocessing import Process
from dialogs.add_category_dialog import AddCategoryDialogContent
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from dialogs.manage_accounts_dialog import ManageAccountsDialogContent
from dialogs.add_value_dialog import AddValueDialogContent
from dialogs.add_standingorder_dialog import AddStandingOrderDialogContent
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
import copy

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
        #ScreenSettings.update()
        ScreenSettings.load_settings()
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
        self.create_dialogs()
       
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
            data.clean_transfers(acc)
        data.fill_total_status() 
        data.save_accounts(self.demo_mode)
        ScreenSettings.save(self.demo_mode)

    def update_main_screen(self):
        self.update_backend()
        start_date, end_date = self.get_start_and_end_date(self.screen.ids.main.selected_year, self.screen.ids.main.selected_month)
        data.filter_categories_within_dates(start_date, end_date)  
        self.screen.ids.main.update_plot(filterbutton_clicked=False)
        self.screen.ids.main.add_things_to_screen()

    def update_accounts_screen(self):
        self.update_backend()
        self.screen.ids.accounts_screen.update_plot()
        self.screen.ids.accounts_screen.dialog_graph_selection.content_cls.update_list()
        self.screen.ids.accounts_screen.add_account_status_to_mainscreen()
        
    def update_categories_screen(self):
        self.update_backend()
        self.screen.ids.categories_screen.update_plot(filterbutton_clicked=False)
        self.screen.ids.categories_screen.dialog_graph_selection.content_cls.update_list()

    def update_standingorder_screen(self):
        self.update_backend()
        self.screen.ids.standingorders_screen.update_standingorder_list()

    def global_update(self):
        self.update_backend()
        self.update_main_screen()
        self.update_accounts_screen()
        self.update_categories_screen()
        self.update_standingorder_screen()
        self.dialog_add_category.content_cls.update_category_items()
        self.dialog_add_value.content_cls.update_acc_items()
        self.dialog_manage_accounts.content_cls.update_acc_items()
        self.dialog_add_standingorder.content_cls.update_category_account_items()

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
        
    def on_kv_post_CategoriesScreen(self):
        self.screen.ids.categories_screen.create_screen()
            
    def go_to_accounts(self):
        if len(data.accounts)>0:
            self.screen.ids.main.manager.transition = FadeTransition()
            self.screen.ids.main.manager.current = 'Accounts'
        else:
            message = Snackbar(text='No accounts!', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()    

    def go_to_standingorders(self):
        if len(data.accounts)>0:
            self.screen.ids.main.manager.transition = FadeTransition()
            self.screen.ids.main.manager.current = 'Standing order'
        else:
            message = Snackbar(text='No accounts!', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()     

    def go_to_main(self):
        self.screen.ids.main.manager.transition = FadeTransition()
        self.screen.ids.main.manager.current = 'Main' 

    def go_to_categories(self):
        if len(data.accounts)>0 and len(data.categories)>0:
            self.screen.ids.main.manager.transition = FadeTransition()
            self.screen.ids.main.manager.current = 'Categories' 
        elif len(data.categories)<1:
            message = Snackbar(text='No categories yet!', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()  
        else:    
            message = Snackbar(text='No accounts yet!', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()       

    def update_sizes(self):
        Sizes.labelsize = int(self.dialog_settings.content_cls.ids.slider_labelsize.value)
        Sizes.titlesize = int(self.dialog_settings.content_cls.ids.slider_titlesize.value)
        Sizes.linewidth = int(self.dialog_settings.content_cls.ids.slider_linewidth.value)
        Sizes.markersize = int(self.dialog_settings.content_cls.ids.slider_markersize.value)
        Sizes.save()
        self.update_plot()
            
    def build(self):
        return self.screen

    ########## DIALOGS ###########
    def create_dialogs(self):     
        self.dialog_add_category = MDDialog(
                    type="custom",
                    content_cls=AddCategoryDialogContent(),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_add_category(x)
                        ),
                        MDFlatButton(
                            text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_add_remove_category(x)
                        ),
                    ],
                )    

        self.dialog_manage_accounts = MDDialog(
                type="custom",
                content_cls=ManageAccountsDialogContent(),
                title="Add/Delete account",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_manage_accounts(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_accounts_management(x)
                    ),
                ],
            )

        self.dialog_add_value = MDDialog(
                type="custom",
                content_cls=AddValueDialogContent(),
                title='Add transfer',
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_add_value(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_money_transfer(x)
                    ),
                ],
            )

        content = AddStandingOrderDialogContent()
        self.dialog_add_standingorder = MDDialog(
                title="Add standing order",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_add_standingorder(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x: self.add_standing_order(x, content)
                    ),
                ],
        )

        ### FOR LOAD AND SAVE DATA ###
        setting_strings = ['Load data', 'Save data', 'Add account', 'Add order', 'Add category', 'Run demo']
        self.settings_menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=item: self.execute_settings_instance(x),
            } for item in setting_strings
        ]
        self.dropdown_settings = MDDropdownMenu(
            caller=self.screen.ids.main.ids.main_toolbar,
            items=self.settings_menu_items,
            position="auto",
            width_mult=4,
        )
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        self.file_manager.md_bg_color = Colors.bg_color
        self.file_manager.specific_text_color = Colors.text_color
        self.file_manager.opposite_colors = Colors.primary_color

    ### SETTINGS ###3
    def execute_settings_instance(self, instance):
        self.settings_instance = instance
        if instance=='Load data':
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                def callback(permission, results):
                    if all([res for res in results]):
                        self.file_manager_open()
                        self.manager_open = True
                    else:
                        print ('Did not get all permissions')
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], callback)
    
        if instance=='Save data':
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                def callback(permission, results):
                    if all([res for res in results]):
                        data.save_setup()
                        self.manager_open = True
                    else:
                        print ('Did not get all permissions')
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], callback)

        if instance=='Add account':
            self.open_dialog_manage_accounts()  

        if instance=='Add category':
            self.open_dialog_add_category()      
        
        if instance=='Add order':
            self.open_dialog_add_standingorder()

        if instance=='Run demo':
            self.demo_mode = True
            self.load_demo()
        self.dropdown_settings.dismiss()

    def file_manager_open(self):
        if platform == 'android':
            from android.storage import primary_external_storage_path
            primary_ext_storage = primary_external_storage_path()
            self.file_manager.show(primary_ext_storage)  # for mobile phone
        else:
            self.file_manager.show('/')  # for computer

    def select_path(self, path): 
        self.exit_manager()
        toast(path)
        #self.app.get_running_app().change_profile_source(path)
        print(path)
        if self.settings_instance=='Load data':
            data.load_setup(path)
            ScreenSettings.update()
            self.global_update()
        if self.settings_instance=='Save data':
            data.save_setup()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def load_demo(self):
        data.create_new_setup()
        ScreenSettings.update()
        self.global_update()
    
    ### DIALOG ADD STANDING ORDER ###
    def open_dialog_add_standingorder(self):
        self.dialog_add_standingorder.open()

    def dismiss_dialog_add_standingorder(self, instance):
        self.dialog_add_standingorder.dismiss()
        self.dialog_add_standingorder.content_cls.reset_dialog_after_dismiss()

    def add_standing_order(self, instance, content):
        order = content.add_standing_order()
        self.dialog_add_standingorder.dismiss()
        data.add_order_in_transfers(order)
        data.fill_status_of_account(order['Account'])      
        data.fill_total_status()     
        data.save_accounts(self.demo_mode)
        self.global_update()
        self.go_to_standingorders()

    ### DIALOG ADD VALUE ###
    def open_dialog_add_value(self):
        if len(data.accounts)>0:
            self.dialog_add_value.open()
        else:
            messagestring = 'Cannot add a transfer yet. Add an account first.'
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()

    def dismiss_dialog_add_value(self, instance):
        self.dialog_add_value.dismiss()
        self.dialog_add_value.content_cls.reset_dialog_after_dismiss()

    def execute_money_transfer(self, instance):
        if self.dialog_add_value.content_cls.ids.purposefield.hint_text == "Purpose":
            self.add_value()
        else:
            self.transfer_value()

    def transfer_value(self):
        amount        = self.dialog_add_value.content_cls.ids.amountfield.text
        account_from  = self.dialog_add_value.content_cls.ids.accountfield.text
        account_to    = self.dialog_add_value.content_cls.ids.purposefield.text
        date          = self.dialog_add_value.content_cls.ids.datefield.text
        messagestring = ''
        try:
            amount = round(float(amount),2)
        except:
            messagestring += 'Amount field must be number. '
        messagestring += 'Account field from is empty. ' if account_from=='' else ''
        messagestring += 'Account field to is empty.' if account_to=='' else ''   
        messagestring += 'Account field from and to are same. ' if account_from==account_to else ''
        if messagestring!='':
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_add_value.dismiss()
            message = Snackbar(text="Transfered {} € from {} to {}".format(amount, account_from, account_to), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.dialog_add_value.content_cls.ids.amountfield.text  = ''
            self.dialog_add_value.content_cls.ids.accountfield.text = ''
            self.dialog_add_value.content_cls.ids.purposefield.text = ''
            self.dialog_add_value.content_cls.ids.datefield.text = data.today_str
            
            #insert transfer into transfers_list and update account status
            if date in data.accounts[account_to]['Transfers'].keys():
                data.accounts[account_to]['Transfers'][date].append([amount, 'From {} to {}'.format(account_from, account_to), 'Transfer', datetime.now().strftime('%H-%M-%S')])
            else:
                data.accounts[account_to]['Transfers'][date] = [[amount, 'From {} to {}'.format(account_from, account_to), 'Transfer', datetime.now().strftime('%H-%M-%S')]]
            if date in data.accounts[account_from]['Transfers'].keys():
                data.accounts[account_from]['Transfers'][date].append([-amount, 'From {} to {}'.format(account_from, account_to), 'Transfer', datetime.now().strftime('%H-%M-%S')])
            else:
                data.accounts[account_from]['Transfers'][date] = [[-amount, 'From {} to {}'.format(account_from, account_to), 'Transfer', datetime.now().strftime('%H-%M-%S')]] 
            self.dialog_add_value.content_cls.reset_dialog_after_dismiss()    
            self.global_update()

    def add_value(self):  
        self.dialog_add_value.content_cls.focus_function()
        amount        = self.dialog_add_value.content_cls.ids.amountfield.text
        account       = self.dialog_add_value.content_cls.ids.accountfield.text
        purpose       = self.dialog_add_value.content_cls.ids.purposefield.text
        category      = self.dialog_add_value.content_cls.ids.categoryfield.text
        date          = self.dialog_add_value.content_cls.ids.datefield.text
        messagestring = ''
        try:
            amount = round(float(amount),2)
        except:
            messagestring += 'Amount field must be number. '
        messagestring += 'Account field is empty. ' if account=='' else ''
        messagestring += 'Purpose field is empty.' if purpose=='' else ''
        messagestring += 'Category field is empty.' if category=='' else ''    
        if messagestring!='':
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_add_value.dismiss()
            message = Snackbar(text="Added {} € to {} for {}".format(amount, account, purpose), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.dialog_add_value.content_cls.ids.amountfield.text  = ''
            self.dialog_add_value.content_cls.ids.accountfield.text = ''
            self.dialog_add_value.content_cls.ids.purposefield.text = ''
            self.dialog_add_value.content_cls.ids.categoryfield.text = ''
            self.dialog_add_value.content_cls.ids.datefield.text = data.today_str
            
            #insert transfer into transfers_list and update account status
            if date in data.accounts[account]['Transfers'].keys():
                data.accounts[account]['Transfers'][date].append([amount, purpose, category, datetime.now().strftime('%H-%M-%S')])
            else:
                data.accounts[account]['Transfers'][date] = []
                data.accounts[account]['Transfers'][date].append([amount, purpose, category, datetime.now().strftime('%H-%M-%S')])
            self.dialog_add_value.content_cls.reset_dialog_after_dismiss() 
            self.global_update()   
    
    ### DIALOG ACCOUNTS ###
    def open_dialog_manage_accounts(self):
        self.dialog_manage_accounts.open()

    def dismiss_dialog_manage_accounts(self, instance):
        self.dialog_manage_accounts.dismiss()
        self.dialog_manage_accounts.content_cls.reset_dialog_after_dismiss()

    def execute_accounts_management(self, instance):
        if self.dialog_manage_accounts.content_cls.accountfield.hint_text == "Account name":
            self.add_account()
        else:
            self.remove_account()
            self.dialog_manage_accounts.content_cls.accountfield.text = ''
            self.dialog_manage_accounts.content_cls.amountfield.text = ''
            self.dialog_manage_accounts.content_cls.datefield.text = data.today_str    
            self.global_update()
        self.dialog_manage_accounts.content_cls.reset_dialog_after_dismiss() 
        self.go_to_accounts()

    def add_account(self):
        account = self.dialog_manage_accounts.content_cls.accountfield.text.replace(' ','').replace('\t','')
        try:
            amount  = round(float(self.dialog_manage_accounts.content_cls.amountfield.text),2)
            valid_amount = True
        except:
            message = Snackbar(text='Amount must be number.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            valid_amount = False
        if valid_amount:
            date    = self.dialog_manage_accounts.content_cls.datefield.text
            data.accounts[account] = {}
            for key in data.keys_list:
                data.accounts[account][key] = {}
            data.accounts[account]['Transfers'][date] = []
            data.accounts[account]['Transfers'][date].append([amount, 'Start amount', 'Start amount', datetime.now().strftime('%H-%M-%S')])
            ScreenSettings.settings['AccountScreen']['SelectedGraphs'][account] = 'down'
            ScreenSettings.save(self.demo_mode)
            data.fill_status_of_account(account)

            self.dialog_manage_accounts.dismiss()
            message = Snackbar(text='Added account {} with {} € start amount.'.format(account, amount), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()

            self.dialog_manage_accounts.content_cls.accountfield.text = ''
            self.dialog_manage_accounts.content_cls.amountfield.text = ''
            self.dialog_manage_accounts.content_cls.datefield.text = data.today_str    
            self.global_update()
       
        
    def remove_account(self):
        account = self.dialog_manage_accounts.content_cls.accountfield.text
        
        orders_to_delete = []
        for order in data.standingorders['Orders']:
            if data.standingorders['Orders'][order]['Account'] == account:
                orders_to_delete.append(order)
        for order in orders_to_delete:
            del data.standingorders['Orders'][order]

        cats_to_delete = []
        for date in data.accounts[account]['Transfers']:
            for transfer in data.accounts[account]['Transfers'][date]:
                cat = transfer[2]
                if not cat in cats_to_delete:
                    cats_to_delete.append(cat)
        del data.accounts[account]

        real_cats_to_delete = copy.deepcopy(cats_to_delete)
        for acc in data.accounts:
            for date in data.accounts[acc]['Transfers']:
                for transfer in data.accounts[acc]['Transfers'][date]:
                    cat = transfer[2]
                    if cat in cats_to_delete:
                        try:
                            real_cats_to_delete.remove(cat)
                        except:
                            pass

        for cat in real_cats_to_delete:
            try:
                data.categories.remove(cat)
            except:
                pass

        self.dialog_manage_accounts.dismiss()
        message = Snackbar(text='Deleted account {}.'.format(account), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
        message.bg_color=Colors.black_color
        message.text_color=Colors.text_color
        message.open()    


    ### DIALOG CATEGORY ###
    def open_dialog_add_category(self):
        if len(data.accounts)>0:
            self.dialog_add_category.open()
        else:
            message = Snackbar(text='No accounts!', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.Window.width - (dp(10) * 2)) / self.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()     

    def dismiss_dialog_add_category(self, instance):
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.reset_dialog_after_dismiss()   

    def execute_add_remove_category(self, instance):
        category = self.dialog_add_category.content_cls.namefield.text
        #add category
        if self.dialog_add_category.content_cls.namefield.hint_text == "Category name":
            data.categories.append(category)
            active_plots = 0
            for cat in ScreenSettings.settings['CategoriesScreen']['SelectedGraphs']:
                if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='down':
                    active_plots += 1
            ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][category]='down' if active_plots < 3 else 'normal'
            ScreenSettings.save(self.demo_mode)
        #remove category
        else:
            for i, cat in enumerate(data.categories):
                if cat==category:
                    data.categories.pop(i)
                    break
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.reset_dialog_after_dismiss()    
        self.global_update()   
        self.go_to_categories()              
        

     

    

App = DemoApp()
App.run()