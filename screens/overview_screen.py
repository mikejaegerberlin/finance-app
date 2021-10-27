from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import Screen
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
from kivy.graphics import *
from datetime import datetime
from dialogs.add_value_dialog import AddValueDialogContent
from dialogs.dialogs_empty_pythonside import Spacer_Horizontal
from backend.colors import Colors
from backend.totalplot import TotalPlot
from backend.piechart import PieChart
from backend.demo_setup import DemoData as data
from dialogs.selection_dialogs import MonthSelectionDialogContent
from kivymd.uix.filemanager import MDFileManager
from kivy.utils import platform
from kivymd.toast import toast
from backend.settings import ScreenSettings
from kivy.uix.label import Label
from dialogs.manage_accounts_dialog import ManageAccountsDialogContent

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.months_text          = ['January', 'February', 'March', 'April', 'Mai', 'June', 'July', 'August', 'September', 'Oktober', 'November', 'December']
        self.months               = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']


    def on_kv_post(self, instance):
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

        self.dialog_select_month = MDDialog(
                type="custom",
                content_cls=MonthSelectionDialogContent(),
                title="Detailed overiew period",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dialog_select_month.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.change_month_overview(x)
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

        
        self.selected_month = data.today_date.month
        self.selected_year = data.today_date.year

        setting_strings = ['Load data', 'Save data', 'Add account']
        self.settings_menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=item: self.execute_settings_instance(x),
            } for item in setting_strings
        ]
        self.dropdown_settings = MDDropdownMenu(
            caller=self.ids.main_toolbar,
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

    def dismiss_dialog_add_value(self, instance):
        self.dialog_add_value.dismiss()
        self.dialog_add_value.content_cls.accountfield.text = ''
        self.dialog_add_value.content_cls.amountfield.text = ''
        self.dialog_add_value.content_cls.purposefield.text = ''
        self.dialog_add_value.content_cls.categoryfield.text = ''
        self.dialog_add_value.content_cls.datefield.text = data.today_str 


    def dismiss_dialog_manage_accounts(self, instance):
        self.dialog_manage_accounts.dismiss()
        self.dialog_manage_accounts.content_cls.accountfield.text = ''
        self.dialog_manage_accounts.content_cls.amountfield.text = ''
        self.dialog_manage_accounts.content_cls.datefield.text = data.today_str 
        


    def open_dialog_select_month(self):
        years = data.get_all_years_of_transfers()
        self.dialog_select_month.content_cls.update_years()
        snackbar = False
        if len(years.keys())>1:
            self.dialog_select_month.open()
        elif len(years.keys())==1:
            months = 0
            for key in years:
                months = len(years[key])
            if months>1:
                self.dialog_select_month.open()
            else:
                snackbar = True
        
        if snackbar or len(years.keys())==0:
            if len(data.accounts)>0:
                messagestring = 'At least data in two months is required.'
            else:
                messagestring = 'No accounts.'
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()

    def open_dialog_add_value(self):
        if len(data.accounts)>0:
            self.dialog_add_value.open()
        else:
            messagestring = 'Cannot add a transfer yet. Add an account first.'
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
              
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
            self.dialog_manage_accounts.open()    
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
            self.app.global_update()
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

    def change_month_overview(self, instance):
        self.dialog_select_month.dismiss()
        month = data.months_rev[self.dialog_select_month.content_cls.month_field.text]
        year = int(self.dialog_select_month.content_cls.year_field.text)
        
        start_date = datetime.strptime('{}-{}-01'.format(year, month), '%Y-%m-%d').date()
        days = ['31', '30', '29', '28']
        for day in days:
            try:
                end_date   = datetime.strptime('{}-{}-{}'.format(year, month, day), '%Y-%m-%d').date() 
                break
            except:
                pass
        self.selected_month = month
        self.selected_year = year
        data.filter_categories_within_dates(start_date, end_date)  
        self.update_plot(filterbutton_clicked=False)
        self.add_things_to_screen()  
        

    def execute_money_transfer(self, instance):
        if self.dialog_add_value.content_cls.ids.purposefield.hint_text == "Purpose":
            self.add_value()
        else:
            self.transfer_value()
        self.app.global_update()

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
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_add_value.dismiss()
            message = Snackbar(text="Transfered {} € from {} to {}".format(amount, account_from, account_to), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.dialog_add_value.content_cls.ids.amountfield.text  = ''
            self.dialog_add_value.content_cls.ids.accountfield.text = ''
            self.dialog_add_value.content_cls.ids.purposefield.text = ''
            self.dialog_add_value.content_cls.ids.datefield.text = data.today_str
            
            #insert transfer into transfers_list and update account status
            if date in data.accounts[account_to]['Transfers'].keys():
                data.accounts[account_to]['Transfers'][date].append([amount, 'From {} to {}'.format(account_from, account_to), 'Transfer'])
            else:
                data.accounts[account_to]['Transfers'][date] = [[amount, 'From {} to {}'.format(account_from, account_to), 'Transfer']]
            if date in data.accounts[account_from]['Transfers'].keys():
                data.accounts[account_from]['Transfers'][date].append([-amount, 'From {} to {}'.format(account_from, account_to), 'Transfer'])
            else:
                data.accounts[account_from]['Transfers'][date] = [[-amount, 'From {} to {}'.format(account_from, account_to), 'Transfer']] 

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
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_add_value.dismiss()
            message = Snackbar(text="Added {} € to {} for {}".format(amount, account, purpose), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
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
                data.accounts[account]['Transfers'][date].append([amount, purpose, category])
            else:
                data.accounts[account]['Transfers'][date] = []
                data.accounts[account]['Transfers'][date].append([amount, purpose, category])
               
    def button_clicked(self, instance):
        for button in self.filter_buttons:
            if button==instance:
                button.md_bg_color = Colors.text_color
                button.text_color  = Colors.bg_color
            else:
                button.md_bg_color = Colors.bg_color
                button.text_color  = Colors.text_color
        self.update_plot(filterbutton_clicked=True)

    def ref_clicked(self, ref):
        if ref=='demo':
            self.app.demo_mode = True
            data.create_new_setup()
            self.app.global_update()
        elif ref=='account':
            self.dialog_manage_accounts.open(force=True)
           
    def exit_demo(self, instance):
        self.app.demo_mode = False
        data.load_internal_setup()
        self.app.global_update()
         
    def update_plot(self, filterbutton_clicked):
        self.filter_buttons = [self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]        
        canvas2, end_date = TotalPlot.make_plot(self.filter_buttons, data, self.selected_month, self.selected_year, filterbutton_clicked)
        date_to_highlight = datetime.strptime('{}-{}-01'.format(self.selected_year, self.selected_month), '%Y-%m-%d').date()
        if filterbutton_clicked and date_to_highlight<end_date:
            self.selected_month = data.current_month
            self.selected_year = data.current_year
            self.add_things_to_screen()
        #canvas2.size_hint_y = 0.99
        canvas2.pos_hint = {'top': 0.99}
        self.ids.assetview.clear_widgets()
        self.ids.assetview.add_widget(canvas2)

        self.ids.piechartview.clear_widgets()
        self.ids.legend_list.clear_widgets()
        try:
            self.remove_widget(self.info_box)
        except:
            pass
        try:
            self.remove_widget(self.demo_info_box)
        except:
            pass

        if self.app.demo_mode:
            text = "[color=#ffcd0a][ref=demo]Exit demo[/ref][/color]"
            self.demo_info_box = MDFloatLayout()
            label = MDLabel(text=text, font_style='Subtitle2')
            label.markup = True
            label.color = Colors.text_color
            label.pos_hint = {'top': 1.35, 'right': 1.03}
            label.on_ref_press = lambda x='Hi': self.exit_demo(x)
            self.demo_info_box.add_widget(label)
            self.add_widget(self.demo_info_box)

        if len(data.accounts)==0:
            text1 = "No accounts!" 
            text2 = "Add a [color=#ffcd0a][ref=account]new account[/ref][/color] or run the [color=#ffcd0a][ref=demo]demo[/ref][/color]."
            self.info_box = MDFloatLayout()
            label = MDLabel(text=text1, font_style='Subtitle2')
            label2 = MDLabel(text=text2, font_style='Caption')
            label2.markup = True
            label.color = Colors.text_color
            label.halign = 'center'
            label.pos_hint = {'top': 0.78}
            label2.color = Colors.text_color
            label2.halign = 'center'
            label2.pos_hint = {'top': 0.74}
            label2.on_ref_press = lambda x: self.ref_clicked(x)
            self.info_box.add_widget(label)
            self.info_box.add_widget(label2)
            self.add_widget(self.info_box)

        elif data.categories_expenditures_total>=0:
            text1 = "No expenditures!" 
            text2 = "Select another month by tapping on the chart above\n or add an expenditure to this month."
            self.info_box = MDFloatLayout()
            label = MDLabel(text=text1, font_style='Subtitle2')
            label2 = MDLabel(text=text2, font_style='Caption')
            label.color = Colors.text_color
            label.halign = 'center'
            label.pos_hint = {'top': 0.78}
            label2.color = Colors.text_color
            label2.halign = 'center'
            label2.pos_hint = {'top': 0.74}
            self.info_box.add_widget(label)
            self.info_box.add_widget(label2)
            self.add_widget(self.info_box)

        else:
            piecanvas = PieChart.make_plot(data.categories_expenditures)
            piecanvas.size_hint_y = 0.95
            piecanvas.size_hint_x = 0.7
            piecanvas.pos_hint = {'top': 1, 'right': 1}
            self.ids.piechartview.size = 100, 100
            self.ids.piechartview.add_widget(piecanvas)
        
            for i, label in enumerate(data.categories_expenditures):
                card = MDCard(size_hint_y=None, height='40dp', md_bg_color=Colors.bg_color, elevation = 0)
                contentbox = MDBoxLayout(orientation='vertical', md_bg_color=Colors.bg_color)

                subbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color)
                rectangle = MDIcon(icon='card', theme_text_color='Custom')
                rectangle.color = Colors.piechart_colors[i]
                rectangle.halign = 'right'
                rectangle.size_hint_x = 0.25
                label1 = MDLabel(text=label, font_style='Caption')
                label1.color = Colors.text_color
                label1.halign = 'left'
                label1.size_hint_x = 0.75
                subbox.add_widget(rectangle)
                subbox.add_widget(label1)
                contentbox.add_widget(subbox)
            
                subbox2 = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color)
                total = round(data.categories_expenditures[label]/data.categories_expenditures_total*100, 1)
                label2 = MDLabel(text='')
                label2.color = Colors.text_color
                label2.halign = 'left'
                label2.size_hint_x = 0.25

                label3 = MDLabel(text=str(round(data.categories_expenditures[label],2))+'€', font_style='Caption')
                label3.color = Colors.text_color
                label3.halign = 'left'
                label3.size_hint_x = 0.35

                label4 = MDLabel(text='=', font_style='Caption')
                label4.color = Colors.text_color
                label4.halign = 'center'
                label4.size_hint_x = 0.05

                label5 = MDLabel(text=str(total)+'%', font_style='Caption')
                label5.color = Colors.text_color
                label5.halign = 'right'
                label5.size_hint_x = 0.35
                subbox2.add_widget(label2)
                subbox2.add_widget(label3)
                subbox2.add_widget(label4)
                subbox2.add_widget(label5)
                contentbox.add_widget(subbox2)

                card.add_widget(contentbox)
                self.ids.legend_list.add_widget(card)
        
            label = MDLabel(text='Trend of monthly profit', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 0.99})
            label.color = Colors.text_color
            self.ids.assetview.add_widget(label)     

    def add_things_to_screen(self):

        header = self.ids.overview_header
        header.clear_widgets()
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(Spacer_Horizontal(0.05))
        
        header_label = MDLabel(text='DETAILED OVERVIEW '+self.months_text[self.selected_month-1]+' '+str(self.selected_year), font_style="Subtitle2")
        header_label.color = Colors.bg_color
        header_label.halign = 'center'
        header.add_widget(header_label)

        profit = round(data.categories_income_total + data.categories_expenditures_total, 2)
        self.ids.status_month_label.text = str(profit)+' €'
        self.ids.status_month_label.color = Colors.green_color if profit>=0 else Colors.error_color

        self.ids.status_expenditures_label.text = str(round(data.categories_expenditures_total, 2))+' €'
        self.ids.status_expenditures_label.color = Colors.green_color if data.categories_expenditures_total>=0 else Colors.error_color

        self.ids.status_income_label.text = str(round(data.categories_income_total, 2))+' €'
        self.ids.status_income_label.color = Colors.green_color if data.categories_income_total>=0 else Colors.error_color

    def execute_accounts_management(self, instance):
        if self.dialog_manage_accounts.content_cls.accountfield.hint_text == "Account name":
            self.add_account()
        else:
            self.remove_account()
            self.dialog_manage_accounts.content_cls.accountfield.text = ''
            self.dialog_manage_accounts.content_cls.amountfield.text = ''
            self.dialog_manage_accounts.content_cls.datefield.text = data.today_str    
            self.app.global_update()
        

    def add_account(self):
        account = self.dialog_manage_accounts.content_cls.accountfield.text.replace(' ','').replace('\t','')
        try:
            amount  = round(float(self.dialog_manage_accounts.content_cls.amountfield.text),2)
            valid_amount = True
        except:
            message = Snackbar(text='Amount must be number.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
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
            data.accounts[account]['Transfers'][date].append([amount, 'Start amount', 'Start amount'])
            ScreenSettings.settings['AccountScreen']['SelectedGraphs'][account] = 'down'
            ScreenSettings.save(self.app.demo_mode)
            data.fill_status_of_account(account)

            self.dialog_manage_accounts.dismiss()
            message = Snackbar(text='Added account {} with {} € start amount.'.format(account, amount), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()

            self.dialog_manage_accounts.content_cls.accountfield.text = ''
            self.dialog_manage_accounts.content_cls.amountfield.text = ''
            self.dialog_manage_accounts.content_cls.datefield.text = data.today_str    
            self.app.global_update()
       
        
    def remove_account(self):
        account = self.dialog_manage_accounts.content_cls.accountfield.text
        del data.accounts[account]
        orders_to_delete = []
        for order in data.standingorders['Orders']:
            if data.standingorders['Orders'][order]['Account'] == account:
                orders_to_delete.append(order)
        for order in orders_to_delete:
            del data.standingorders['Orders'][order]

        self.dialog_manage_accounts.dismiss()
        message = Snackbar(text='Deleted account {}.'.format(account), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
        message.bg_color=Colors.black_color
        message.text_color=Colors.text_color
        message.open()
        

           