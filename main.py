from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
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
from screens.account_screen import AccountScreen

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)  

    def button_clicked(self, instance):
        for button in App.filter_buttons:
            if button==instance:
                button.md_bg_color = Colors.text_color
                button.text_color  = Colors.bg_color
            else:
                button.md_bg_color = Colors.bg_color
                button.text_color  = Colors.text_color
        App.update_plot()
    
    def before_enter(self):
        self.ids.nav_drawer.set_state(0)
        for acc in data.accounts:
            App.update_main_accountview(acc)
        canvas    = AccountPlot.make_plot(App.filter_buttons, data)
        yeargraph = self.ids.assetview
        yeargraph.clear_widgets()
        yeargraph.add_widget(canvas)  
        self.ids.floating_button.close_stack()

class AssetView(BoxLayout):
    def __init__(self, **kwargs):
        super(AssetView, self).__init__(**kwargs)

class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (400,700)
        self.create_items_for_dropdowns_and_buttons()
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
        sm.add_widget(AccountScreen(name='Account'))
        sm.add_widget(StandingOrdersScreen(name='Standing order'))
        self.screen = Builder.load_file("main_screen.kv")

        ### Get relevant ids form kv file###
        self.create_dialogs()

        self.add_value_accountfield = self.dialog_add_value.content_cls.ids.accountfield
        self.add_value_amountfield  = self.dialog_add_value.content_cls.ids.amountfield
        self.add_value_purposefield = self.dialog_add_value.content_cls.ids.purposefield
        self.add_value_datefield    = self.dialog_add_value.content_cls.ids.datefield

        self.money_transfer_accountfield_from = self.dialog_money_transfer.content_cls.ids.accountfield_from
        self.money_transfer_accountfield_to   = self.dialog_money_transfer.content_cls.ids.accountfield_to
        self.money_transfer_amountfield    = self.dialog_money_transfer.content_cls.ids.amountfield
        self.money_transfer_datefield      = self.dialog_money_transfer.content_cls.ids.datefield
        self.add_value_amountfield         = self.dialog_add_value.content_cls.ids.amountfield
        self.add_value_purposefield = self.dialog_add_value.content_cls.ids.purposefield
        self.add_value_datefield    = self.dialog_add_value.content_cls.ids.datefield
        self.filter_buttons = [self.screen.ids.main.ids.onemonth_button, self.screen.ids.main.ids.threemonths_button, self.screen.ids.main.ids.sixmonths_button, 
                               self.screen.ids.main.ids.oneyear_button, self.screen.ids.main.ids.threeyears_button]

        date = self.dialog_date.today.strftime('%Y-%m-%d')
        self.add_value_datefield.text = date
        self.money_transfer_datefield.text = date

        #exectute this block if demodata is load from json        
        '''if data.today_date.day==1:
            data.reset_standingorders_monthlisted()
        for acc in data.accounts:
            data.check_standingorders(acc)
            data.fill_status_of_account(acc)
        data.save_standingorders()'''

        self.create_dropdownmenus()
        self.add_account_status_to_mainscreen()
        CardItemsBackend.generate_carditems(10)
        
        
        
    def create_items_for_dropdowns_and_buttons(self):
        self.data_floating_button = {
            'Income/Expenditure': 'bank-outline', 
            'Transfer': 'bank-transfer',
            'Standing Orders': 'file-document-multiple-outline',
            'Accounts': 'account-multiple',
            }

        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]

        self.settings_items = [
            {
                "text": sett,
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=sett: self.select_settings_item(x),
            } for sett in Sizes.file
        ]
        
    def create_dropdownmenus(self):
        self.acc_dropdown = MDDropdownMenu(
            caller=self.add_value_accountfield,
            items=self.acc_menu_items,
            position="bottom",
            width_mult=4,
        )
    
    def create_dialogs(self):
        self.dialog_add_value = MDDialog(
                type="custom",
                content_cls=AddValueDialogContent(Colors),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_add_value.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Add': self.add_value(x)
                    ),
                ],
            )

        self.dialog_settings = MDDialog(
                title="Settings",
                type="custom",
                content_cls=SettingsDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_settings.dismiss()
                    ),
                ],
            )

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

        self.dialog_date = MDDatePicker(primary_color=Colors.primary_color, selector_color=Colors.primary_color, 
                                        text_button_color=Colors.primary_color, text_color=Colors.bg_color, specific_text_color=Colors.bg_color,
                                        size_hint_y=None, text_weekday_color=Colors.bg_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)

        self.dialog_date_custom = MDDialog(
                title="Pick a date",
                type="custom",
                content_cls=DatePickerContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel':self.dialog_date_custom_cancel(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Add': self.dialog_date_custom_ok(x)
                    ),
                ],
            )
               
    def callback_floatingbutton(self, instance):
        if instance.icon == 'bank-outline':
            self.dialog_add_value.open()
        if instance.icon == 'bank-transfer':
            self.dialog_money_transfer.open()
        if instance.icon == 'file-document-multiple-outline':
            self.screen.ids.main.manager.current = 'Standing order'
        if instance.icon == 'account-multiple':
            self.dialog_date_custom.open()
        self.screen.main.ids.floating_button.close_stack()
        self.screen.main.ids.main_content.canvas.opacity = 1
        
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

    def add_value(self, instance):  
        self.dialog_add_value.content_cls.focus_function()
        amount        = self.add_value_amountfield.text
        account       = self.add_value_accountfield.text
        purpose       = self.add_value_purposefield.text
        date          = self.add_value_datefield.text
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
            self.add_value_amountfield.text  = ''
            self.add_value_accountfield.text = ''
            self.add_value_purposefield.text = ''
            self.add_value_datefield.text = data.today_str
            
            #insert transfer into transfers_list and update account status
            if date in data.accounts[account]['Transfers'].keys():
                data.accounts[account]['Transfers'][date].append([amount, purpose])
            else:
                data.accounts[account]['Transfers'][date] = []
                data.accounts[account]['Transfers'][date].append([amount, purpose])
            data.fill_status_of_account(account)
            self.update_main_accountview(account)
            data.save_accounts()
            

    def update_main_accountview(self, account):
            self.AmountLabels[account].text     = str(data.accounts[account]['Status'][data.today_str])+' €'
            if data.accounts[account]['Status'][data.today_str]<0:
                self.AmountLabels[account].color = Colors.error_color
            else:
                self.AmountLabels[account].color = Colors.green_color
            self.update_plot()
            

    def update_plot(self):
        canvas    = AccountPlot.make_plot(self.filter_buttons, data)
        yeargraph = self.screen.main.ids.assetview
        yeargraph.clear_widgets()
        yeargraph.add_widget(canvas)

    def update_sizes(self):
        Sizes.labelsize = int(self.dialog_settings.content_cls.ids.slider_labelsize.value)
        Sizes.titlesize = int(self.dialog_settings.content_cls.ids.slider_titlesize.value)
        Sizes.linewidth = int(self.dialog_settings.content_cls.ids.slider_linewidth.value)
        Sizes.markersize = int(self.dialog_settings.content_cls.ids.slider_markersize.value)
        Sizes.save()
        self.update_plot()

    def open_acc_dropdown(self, accountfield):
        accountfield.hide_keyboard()
        self.acc_dropdown.caller = accountfield
        self.acc_dropdown.open()
        
        self.add_value_purposefield.focus     = False
        self.add_value_amountfield.focus      = False
        self.money_transfer_datefield.focus   = False
        self.money_transfer_amountfield.focus = False
        if accountfield==self.money_transfer_accountfield_from:
            self.money_transfer_accountfield_to.focus = False
        else:
            self.money_transfer_accountfield_from.focus = False

    def open_datepicker(self, datefield):
        self.selected_datefield = datefield
        self.dialog_date.open()
        
    def dialog_date_ok(self, instance, value, date_range):
        date = value.strftime('%Y-%m-%d')
        self.selected_datefield.text = date
        self.money_transfer_accountfield_to.focus = False
        self.money_transfer_accountfield_from.focus = False
        self.add_value_accountfield.focus = False
    
    def dialog_date_cancel(self, instance, value):
        self.money_transfer_accountfield_to.focus = False
        self.money_transfer_accountfield_from.focus = False
        self.add_value_accountfield.focus = False

    def dialog_date_custom_cancel(self, x):
        self.money_transfer_accountfield_to.focus = False
        self.money_transfer_accountfield_from.focus = False
        self.add_value_accountfield.focus = False
        self.dialog_date_custom.dismiss()

    def dialog_date_custom_ok(self, x):
        self.money_transfer_accountfield_to.focus = False
        self.money_transfer_accountfield_from.focus = False
        self.add_value_accountfield.focus = False
        self.selected_datefield.text = '2019-01-01'
        self.dialog_date_custom.dismiss()
 

    def set_acc_item(self, text_item):
        self.acc_dropdown.caller.text = text_item
        self.acc_dropdown.dismiss()
        self.acc_dropdown.caller.focus = False
        self.dialog_add_value.content_cls.focus_function()

    def generate_main_carditem(self, acc):
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, on_release=lambda x=acc:self.go_to_account(acc))
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[20,20,20,20])      
        acclabel   = MDLabel(text=acc, font_style='Subtitle2')
        acclabel.color = Colors.text_color
        acclabel.halign = 'center'
        contentbox.add_widget(acclabel)
    
        last_date = list(data.accounts[acc]['Status'].keys())
        last_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
        last_date = last_date[-1]
        
        amlabel = MDLabel(text=str(data.accounts[acc]['Status'][last_date])+' €', font_style='Subtitle2')
        amlabel.color = self.error_color if data.accounts[acc]['Status'][last_date]<0 else self.green_color
        amlabel.halign = 'center'
        self.AmountLabels[acc] = amlabel
        contentbox.add_widget(amlabel)
        contentbox.add_widget(MDLabel())
        card.add_widget(contentbox)
        
        return card

    def add_account_status_to_mainscreen(self):

        canvas = AccountPlot.make_plot(self.filter_buttons, data)
        self.screen.ids.main.ids.assetview.add_widget(canvas)

        self.AmountLabels = {}

        #header of table scrollview
        header = self.screen.ids.main.accountsview_header
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(Spacer_Horizontal(0.05))
        
        labels = ['Account', 'Current Status', 'End Month Status']
        for label in labels:
            header_label = MDLabel(text=label, font_style="Subtitle2")
            header_label.color = Colors.text_color
            header_label.halign = 'center'
            header.add_widget(header_label)

        #scrollview items
        for acc in data.accounts:
            carditem = self.generate_main_carditem(acc)
            self.screen.ids.main.accountsview.add_widget(carditem)
            self.screen.ids.main.accountsview.add_widget(Spacer_Vertical('6dp'))

    def go_to_account(self, acc):
        self.current_account = acc
        data.current_account = acc
        self.screen.ids.main.manager.current = 'Account'  
    
    def go_to_mainscreen(self, instance):
        self.screen.ids.main.manager.current = 'Main' 
            
    def build(self):
        return self.screen
        

     

    

App = DemoApp()
App.run()