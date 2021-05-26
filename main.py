from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd import images_path
from kivymd.icon_definitions import md_icons
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.font_definitions import theme_font_styles
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import backend, dialogs
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import OneLineListItem, ThreeLineListItem
from kivymd.uix.card import MDCard
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from kivymd.uix.tab import MDTabsBase
from datetime import timedelta
from dateutil.relativedelta import relativedelta

Backend = backend.Backend()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)  

    def button_clicked(self, instance):
        for button in App.filter_buttons:
            if button==instance:
                button.md_bg_color = Backend.text_color
                button.text_color  = Backend.bg_color
            else:
                button.md_bg_color = Backend.bg_color
                button.text_color  = Backend.text_color
        App.update_plot()
    

    def before_enter(self):
        self.ids.nav_drawer.set_state(0)
        canvas    = Backend.make_plot(App.filter_buttons)
        yeargraph = self.ids.assetview
        yeargraph.clear_widgets()
        yeargraph.add_widget(canvas)  
        self.ids.floating_button.close_stack()

class AssetView(BoxLayout):
    def __init__(self, **kwargs):
        super(AssetView, self).__init__(**kwargs)

class AccountScreen(Screen):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        self.filter_buttons = [self.ids.oneweek_button, self.ids.twoweeks_button, self.ids.onemonth_button, 
                               self.ids.threemonths_button, self.ids.custom_button]
        self.fill_transfers_list(App.current_account)
        self.ids.accountscreen_toolbar.title = App.current_account + ' transfers'
    
    def button_clicked(self, instance):
        for button in self.filter_buttons:
            if button==instance:
                button.md_bg_color = Backend.text_color
                button.text_color  = Backend.bg_color
            else:
                button.md_bg_color = Backend.bg_color
                button.text_color  = Backend.text_color
        self.fill_transfers_list(App.current_account)

    def generate_month_carditem(self, year, month):
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Backend.bg_color, ripple_behavior=True, ripple_color=Backend.bg_color)
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Backend.bg_color_light, radius=[10,10,10,10])      
        acclabel   = MDLabel(text=Backend.months[month-1]+' '+str(year), font_style='Button')
        acclabel.color = Backend.text_color
        contentbox.add_widget(dialogs.Spacer_Horizontal(0.03))
        contentbox.add_widget(acclabel)
        card.add_widget(contentbox)
        return card

    def generate_transfer_carditem(self, date, purpose, amount):
        
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Backend.bg_color, ripple_behavior=True, ripple_color=Backend.bg_color_light)
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Backend.bg_color, radius=[10,10,10,10])     

        datelabel   = MDLabel(text=date, font_style='Button')
        datelabel.color = Backend.text_color
        datelabel.halign = 'center'
        contentbox.add_widget(datelabel)

        purposelabel   = MDLabel(text=purpose, font_style='Button')
        purposelabel.color = Backend.text_color
        purposelabel.halign = 'center'
        contentbox.add_widget(purposelabel)

        amlabel = MDLabel(text=str(amount), font_style='Button')
        amlabel.color = Backend.error_color if amount<0 else Backend.green_color
        amlabel.halign = 'center'
        contentbox.add_widget(amlabel)

        card.add_widget(contentbox)
        return card

    def fill_transfers_list(self, account):
        self.ids.transfers_list.clear_widgets()
        start_date = App.dialog_date.today
        for i, button in enumerate(self.filter_buttons):
            if button.md_bg_color[0]==1:
                break
        if i<=3:
            timedeltas = [relativedelta(weeks=1), relativedelta(weeks=2), relativedelta(months=1), relativedelta(months=3)]
            timedelta  = timedeltas[i]
            end_date = App.dialog_date.today - timedelta
        if i==4:
            years = list(Backend.accounts[account].keys())[1:]
            years.sort(key=int)
            outer_break = False
            for year in years:
                months = list(Backend.accounts[account][year].keys())[3:]
                months.sort(key=int)
                for month in months:
                    if len(Backend.accounts[account][year][month]['Transfers'])>0:
                        end_date_year = year
                        end_date_month = month
                        outer_break = True
                        break
                if outer_break==True:
                    break
                
            end_date = '{}-{}-{}'.format(end_date_year, end_date_month, '01')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        years, months = Backend.get_year_and_month_indizes(start_date, end_date)

        for i, year in enumerate(years):   
            for month in months[i]:
                card = self.generate_month_carditem(int(year), int(month))
                self.ids.transfers_list.add_widget(card)
                transfers_list = list(Backend.accounts[account][year][month]['Transfers'].keys())
                transfers_list.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date(), reverse=True)
                for date in transfers_list:
                    if datetime.strptime(date, '%Y-%m-%d').date() >= end_date:
                        for transfer in Backend.accounts[account][year][month]['Transfers'][date]:
                            purpose = transfer[1]
                            amount  = transfer[0]
                            card = self.generate_transfer_carditem(date, purpose, amount)
                            self.ids.transfers_list.add_widget(card)
    
class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (400,700)
        self.create_items_for_dropdowns_and_buttons()
        self.slider_labelsize_current = Backend.settings['Labelsize']
        self.slider_titlesize_current = Backend.settings['Titlesize']
        self.slider_linewidth_current = Backend.settings['Linewidth']
        self.slider_markersize_current = Backend.settings['Markersize']

        self.bg_color                     = Backend.bg_color
        self.bg_color_light               = Backend.bg_color_light
        self.text_color                   = Backend.text_color
        self.primary_color                = Backend.primary_color
        self.button_disable_onwhite_color = Backend.button_disable_onwhite_color
        self.error_color                  = Backend.error_color
        self.black_color                  = Backend.black_color
        self.green_color                  = Backend.green_color
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name='Main'))
        sm.add_widget(AccountScreen(name='Account'))
        self.screen = Builder.load_file("main_screen.kv")

        ### Get relevant ids form kv file###
        self.create_dialogs()

        self.add_value_accountfield = self.dialog_add_value.content_cls.ids.accountfield
        self.add_value_amountfield  = self.dialog_add_value.content_cls.ids.amountfield
        self.add_value_purposefield = self.dialog_add_value.content_cls.ids.purposefield
        self.add_value_datefield    = self.dialog_add_value.content_cls.ids.datefield
        self.filter_buttons = [self.screen.ids.main.ids.onemonth_button, self.screen.ids.main.ids.threemonths_button, self.screen.ids.main.ids.sixmonths_button, 
                               self.screen.ids.main.ids.oneyear_button, self.screen.ids.main.ids.threeyears_button]

        date = self.dialog_date.today.strftime('%Y-%m-%d')
        self.add_value_datefield.text = date
        
        self.create_dropdownmenus()
        self.add_account_status_to_mainscreen()
        
    def create_items_for_dropdowns_and_buttons(self):
        self.data_floating_button = {
            'Income/Expenditure': 'bank-outline', 
            'Transfer': 'bank-transfer',
            'Standing Order': 'book-plus',
            'New Account': 'account-plus',
            }

        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in Backend.accounts
        ]

        self.settings_items = [
            {
                "text": sett,
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=sett: self.select_settings_item(x),
            } for sett in Backend.settings
        ]

    def create_dropdownmenus(self):
        self.add_value_acc_dropdown = MDDropdownMenu(
            caller=self.add_value_accountfield,
            items=self.acc_menu_items,
            position="bottom",
            width_mult=4,
        )
    
    def create_dialogs(self):
        self.dialog_add_value = MDDialog(
                type="custom",
                content_cls=dialogs.AddValueDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=Backend.primary_color, on_release=lambda x='Cancel': self.dialog_add_value.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", text_color=Backend.primary_color, on_release=lambda x='Add': self.add_value(x)
                    ),
                ],
            )

        self.dialog_settings = MDDialog(
                title="Settings",
                type="custom",
                content_cls=dialogs.SettingsDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="OK", text_color=Backend.primary_color, on_release=lambda x='Cancel': self.dialog_settings.dismiss()
                    ),
                ],
            )

        self.dialog_date = MDDatePicker(primary_color=Backend.primary_color, selector_color=Backend.primary_color, text_button_color=Backend.primary_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)
               
    def callback_floatingbutton(self, instance):
        if instance.icon == 'bank-outline':
            self.dialog_add_value.open()
        if instance.icon == 'bank-transfer':
            self.reset_data()
        self.screen.main.ids.floating_button.close_stack()
        self.screen.main.ids.main_content.canvas.opacity = 1
        

    def add_value(self, instance):  
        amount        = self.add_value_amountfield.text
        account       = self.add_value_accountfield.text
        purpose       = self.add_value_purposefield.text
        date          = self.add_value_datefield.text
        messagestring = ''
        try:
            amount = float(amount)
        except:
            messagestring += 'Amount field must be number. '
        messagestring += 'Account field is empty. ' if account=='' else ''
        messagestring += 'Purpose field is empty.' if purpose=='' else ''   
        if messagestring!='':
            message = Snackbar(text=messagestring)
            message.bg_color=Backend.black_color
            message.text_color=Backend.text_color
            message.open()
        else:
            #Backend.add_value()
            self.dialog_add_value.dismiss()
            check_button = self.dialog_add_value.content_cls.ids.dialog_income_button.text_color[2]
            message = Snackbar(text="Added {} € to {} for {}".format(amount, account, purpose))
            message.bg_color=Backend.black_color
            message.text_color=Backend.text_color
            message.open()
            self.add_value_amountfield.text  = ''
            self.add_value_accountfield.text = ''
            self.add_value_purposefield.text = ''
            year = date.split('-')[0]
            month = str(int(date.split('-')[1]))
            
            #insert transfer into transfers_list
            if date in Backend.accounts[account][year][month]['Transfers'].keys():
                Backend.accounts[account][year][month]['Transfers'][date].append([amount, purpose])
            else:
                Backend.accounts[account][year][month]['Transfers'][date] = []
                Backend.accounts[account][year][month]['Transfers'][date].append([amount, purpose])

            #update status of account
            if date in Backend.accounts[account]['Status'].keys():
                Backend.accounts[account]['Status'][date] = round(Backend.accounts[account]['Status'][date] + amount,2)
            else:
                last_date = list(Backend.accounts[account]['Status'].keys())
                last_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
                last_date = last_date[-1]
                Backend.accounts[account]['Status'][date] = round(Backend.accounts[account]['Status'][last_date] + amount,2)    
            

            self.AmountLabels[account].text     = str(Backend.accounts[account]['Status'][date])
            if Backend.accounts[account]['Status'][date]<0:
                self.AmountLabels[account].color = self.error_color
            else:
                self.AmountLabels[account].color = self.green_color
            self.update_plot()
            Backend.save_jsons()

    def update_plot(self):
        canvas    = Backend.make_plot(self.filter_buttons)
        yeargraph = self.screen.main.ids.assetview
        yeargraph.clear_widgets()
        yeargraph.add_widget(canvas)

    def update_sizes(self):
        Backend.settings['Labelsize'] = int(self.dialog_settings.content_cls.ids.slider_labelsize.value)
        Backend.settings['Titlesize'] = int(self.dialog_settings.content_cls.ids.slider_titlesize.value)
        Backend.settings['Linewidth'] = int(self.dialog_settings.content_cls.ids.slider_linewidth.value)
        Backend.settings['Markersize'] = int(self.dialog_settings.content_cls.ids.slider_markersize.value)
        self.update_plot()
    
    def reset_data(self):  
        Backend.reset_data()
        self.update_plot()        

    def open_add_value_acc_dropdown(self):
        self.add_value_accountfield.hide_keyboard()
        self.add_value_acc_dropdown.open()
        self.add_value_purposefield.focus = False
        self.add_value_amountfield.focus  = False

    def open_add_value_datepicker(self):
        self.add_value_datefield.hide_keyboard()
        self.dialog_date.open()

    def dialog_date_ok(self, instance, value, date_range):
        date = value.strftime('%Y-%m-%d')
        date = date.split('-')
        self.add_value_datefield.text = '{}.{}.{}'.format(date[2],date[1],date[0])
        self.add_value_datefield.focus  = False
       
    def dialog_date_cancel(self, instance, value):
        self.add_value_datefield.focus  = False
 

    def set_acc_item(self, text_item):
        self.add_value_accountfield.text = text_item
        self.add_value_acc_dropdown.dismiss()
        self.add_value_accountfield.focus = False
        self.add_value_accountfield.text_color_normal = Backend.primary_color

    def generate_main_carditem(self, acc):
        
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Backend.bg_color, ripple_behavior=True, ripple_color=Backend.bg_color, on_release=lambda x=acc:self.go_to_account(acc))
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Backend.bg_color_light, radius=[20,20,20,20])      
        acclabel   = MDLabel(text=acc, font_style='Button')
        acclabel.color = Backend.text_color
        acclabel.halign = 'center'
        contentbox.add_widget(acclabel)
    
        last_date = list(Backend.accounts[acc]['Status'].keys())
        last_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
        last_date = last_date[-1]
        
        amlabel = MDLabel(text=str(Backend.accounts[acc]['Status'][last_date]), font_style='Button')
        amlabel.color = self.error_color if Backend.accounts[acc]['Status'][last_date]<0 else self.green_color
        amlabel.halign = 'center'
        self.AmountLabels[acc] = amlabel
        contentbox.add_widget(amlabel)
        contentbox.add_widget(MDLabel())
        card.add_widget(contentbox)
        
        return card

    def add_account_status_to_mainscreen(self):

        canvas = Backend.make_plot(self.filter_buttons)
        self.screen.ids.main.ids.assetview.add_widget(canvas)

        self.AmountLabels = {}

        #header of table scrollview
        header = self.screen.ids.main.accountsview_header
        header.md_bg_color = Backend.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(dialogs.Spacer_Horizontal(0.05))
        
        labels = ['Account', 'Current Status', 'End Month Status']
        for label in labels:
            header_label = MDLabel(text=label, font_style="Button")
            header_label.color = Backend.text_color
            header_label.halign = 'center'
            header.add_widget(header_label)

        #scrollview items
        for acc in Backend.accounts:
            carditem = self.generate_main_carditem(acc)
            self.screen.ids.main.accountsview.add_widget(carditem)
            self.screen.ids.main.accountsview.add_widget(dialogs.Spacer_Vertical('6dp'))

    def go_to_account(self, acc):
        self.current_account = acc
        self.screen.ids.main.manager.current = 'Account'  
    
    def go_to_mainscreen(self, instance):
        self.screen.ids.main.manager.current = 'Main' 
            
    def build(self):
        return self.screen
        

     

    

App = DemoApp()
App.run()