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
import backend2
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

Backend = backend2.Backend()

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
        canvas    = Backend.make_plot(App.filter_buttons)
        yeargraph = self.ids.assetview
        yeargraph.clear_widgets()
        yeargraph.add_widget(canvas)  
        self.ids.floating_button.close_stack()

class StandingOrdersScreen(Screen):
    def __init__(self, **kwargs):
        super(StandingOrdersScreen, self).__init__(**kwargs) 

    def on_pre_enter(self):
        header = self.ids.header
        header.clear_widgets()
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]

        labels = ['Account', 'From', 'To', 'Date', 'Purpose', 'Amount']
        for label in labels:
            header_label = MDLabel(text=label, font_style="Subtitle2")
            header_label.color = Colors.text_color
            header_label.halign = 'center'
            header.add_widget(header_label)

        #scrollview items
        self.standing_orders_list.clear_widgets()
        for number in Backend.standingorders:
            carditem = self.generate_carditem(Backend.standingorders[number])
            self.standing_orders_list.add_widget(carditem)
            self.standing_orders_list.add_widget(Spacer_Vertical('6dp'))

    def generate_carditem(self, entry):
        card       = MDCard(size_hint_y=None, height='45dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color)
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[20,20,20,20])  
        for i, key in enumerate(entry):
            if not i==len(list(entry.keys()))-1:
                label   = MDLabel(text=str(entry[key]), font_style='Subtitle2')
                label.color = Colors.text_color
                label.halign = 'center'
                contentbox.add_widget(label)

        label   = MDLabel(text=str(entry['Amount'])+' €', font_style='Subtitle2')
        label.color = Colors.error_color if entry['Amount']<0 else Colors.green_color
        label.halign = 'center'
        contentbox.add_widget(label)
        card.add_widget(contentbox)
        return card

class AssetView(BoxLayout):
    def __init__(self, **kwargs):
        super(AssetView, self).__init__(**kwargs)

class AccountScreen(Screen):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs) 
        self.create_dialogs()
 
    def on_pre_enter(self):
        self.ids.accountscreen_toolbar.title = App.current_account + ' transfers'
        self.filter_buttons = [self.ids.twoweeks_button, self.ids.onemonth_button, 
                               self.ids.threemonths_button, self.ids.sixmonths_button, self.ids.custom_button]
        Backend.generate_carditems(10)
        self.fill_transfers_list(App.current_account)
        
        
    def create_dialogs(self):
        self.dialog_change_transferitem = MDDialog(
                title="Change transfer item",
                type="custom",
                content_cls=ChangeTransferitemContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_change_transferitem.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Change': self.change_transfer_item(x)
                    ),
                ],
        )

    def button_clicked(self, instance):
        Backend.generate_carditems(3)
        for button in self.filter_buttons:
            if button==instance:
                button.md_bg_color = Colors.text_color
                button.text_color  = Colors.bg_color
            else:
                button.md_bg_color = Colors.bg_color
                button.text_color  = Colors.text_color
        self.fill_transfers_list(App.current_account)
 
    def open_transfer_dropdown(self, card, box, datelabel, purposelabel, amountlabel):
        self.selected_card = [datelabel, purposelabel, amountlabel, card, box]
        self.items = ['Change', 'Delete']
        self.transfer_menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(50),
                "on_release": lambda x=item: self.transfer_item_selected(x, datelabel, purposelabel, amountlabel, card, box),
            } for item in self.items
        ]

        self.transfer_dropdown = MDDropdownMenu(
            caller=card,
            items=self.transfer_menu_items,
            width_mult=4,
        )
        box.md_bg_color = Colors.bg_color_light
        self.transfer_dropdown.open()

    def change_transfer_item(self, instance):
        new_date    = self.dialog_change_transferitem.content_cls.ids.datefield.text
        new_purpose = self.dialog_change_transferitem.content_cls.ids.purposefield.text
        new_amount  = float(self.dialog_change_transferitem.content_cls.ids.amountfield.text.replace(' €',''))
        old_date    = self.selected_card[0].text
        old_purpose = self.selected_card[1].text
        old_amount  = float(self.selected_card[2].text.replace(' €',''))
        
        if not new_date in Backend.accounts[App.current_account]['Transfers'].keys():
            Backend.accounts[App.current_account]['Transfers'][new_date] = [[new_amount, new_purpose]]
        else:
            Backend.accounts[App.current_account]['Transfers'][new_date].append([new_amount, new_purpose])
        
        if len(Backend.accounts[App.current_account]['Transfers'][old_date])==1:
            del Backend.accounts[App.current_account]['Transfers'][old_date]
        else:
            for i, transfer in enumerate(Backend.accounts[App.current_account]['Transfers'][old_date]):
                if transfer[0]==old_amount and transfer[1]==old_purpose:
                    Backend.accounts[App.current_account]['Transfers'][old_date].pop(i)       
        self.fill_transfers_list(App.current_account)
        Backend.fill_status_of_account(App.current_account)
        App.update_main_accountview(App.current_account)
        self.dialog_change_transferitem.dismiss()

    def transfer_item_selected(self, item, datelabel, purposelabel, amountlabel, card, box):
        date = datelabel.text
        #change 
        if item==self.items[0]:
            box.md_bg_color = Colors.bg_color 
            self.dialog_change_transferitem.content_cls.ids.datefield.text = datelabel.text
            self.dialog_change_transferitem.content_cls.ids.purposefield.text = purposelabel.text
            if 'From' in purposelabel.text and 'to' in purposelabel.text and len(purposelabel.text.split(' '))==4:
                self.dialog_change_transferitem.content_cls.ids.purposefield.disabled = True
            self.dialog_change_transferitem.content_cls.ids.amountfield.text = amountlabel.text.replace(' €','')
            self.dialog_change_transferitem.open()

        #delete
        if item==self.items[1]:
            if len(Backend.accounts[App.current_account]['Transfers'][date])==1:
                check_purposelabel = Backend.accounts[App.current_account]['Transfers'][date][0][1]
                del Backend.accounts[App.current_account]['Transfers'][date]
                
            else:
                for i, transfer in enumerate(Backend.accounts[App.current_account]['Transfers'][date]):
                    if transfer[0]==float(amountlabel.text.replace(' €','')) and transfer[1]==purposelabel.text:
                        Backend.accounts[App.current_account]['Transfers'][date].pop(i)
                        check_purposelabel = transfer[1]
                            
            self.ids.transfers_list.remove_widget(card)
            Backend.fill_status_of_account(App.current_account)
            App.update_main_accountview(App.current_account)

            if 'From' in check_purposelabel and 'to' in check_purposelabel:
                account_from = check_purposelabel.split(' ')[1]
                account_to   = check_purposelabel.split(' ')[3]
                delete_account = account_to if account_from==App.current_account else account_from
                if len(Backend.accounts[delete_account]['Transfers'][date])==1:
                    del Backend.accounts[delete_account]['Transfers'][date]
                
                else:
                    for i, transfer in enumerate(Backend.accounts[delete_account]['Transfers'][date]):
                        if transfer[0]==-float(amountlabel.text.replace(' €','')) and transfer[1]==check_purposelabel:
                            Backend.accounts[delete_account]['Transfers'][date].pop(i)
                Backend.fill_status_of_account(delete_account)
                App.update_main_accountview(delete_account)
                message = Snackbar(text='Deleted transfer also from account {}.'.format(delete_account))
                message.bg_color=Colors.black_color
                message.text_color=Colors.text_color
                message.open()
        self.transfer_dropdown.dismiss()
        
     
    def generate_month_carditem(self, year, month):
        card           = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color)
        contentbox     = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[10,10,10,10])   
        acclabel       = MDLabel(text=Backend.months[month-1]+' '+str(year), font_style='Button')
        acclabel.color = Colors.text_color
        contentbox.add_widget(Spacer_Horizontal(0.03))
        contentbox.add_widget(acclabel)
        card.add_widget(contentbox)
        return card

    def generate_transfer_carditem(self, date, purpose, amount, cardnumber):
        if cardnumber==len(Backend.cards_transferitem):
            Backend.generate_carditems(1)
        card              = Backend.cards_transferitem[cardnumber][0]
        box               = Backend.cards_transferitem[cardnumber][1]
        datelabel         = Backend.cards_transferitem[cardnumber][2]
        purposelabel      = Backend.cards_transferitem[cardnumber][3]
        amountlabel       = Backend.cards_transferitem[cardnumber][4]
        box.md_bg_color   = Colors.bg_color
        datelabel.text    = date
        purposelabel.text = purpose
        amountlabel.text  = str(amount)+' €'
        amountlabel.color = Colors.error_color if amount<0 else Colors.green_color
        card.on_release   = lambda x=box: self.open_transfer_dropdown(card, box, datelabel, purposelabel, amountlabel)
        return card


    def fill_transfers_list(self, account):
        self.ids.transfers_list.clear_widgets()
        start_date = App.dialog_date.today
        for i, button in enumerate(self.filter_buttons):
            if button.md_bg_color[0]==1:
                break
        if i<=3:
            timedeltas = [relativedelta(weeks=2), relativedelta(months=1), relativedelta(months=3), relativedelta(months=6)]
            timedelta  = timedeltas[i]
            end_date   = App.dialog_date.today - timedelta
        if i==4:
            end_date = list(Backend.accounts[account]['Transfers'].keys())
            end_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
            end_date = datetime.strptime(end_date[0], '%Y-%m-%d').date()
        
        transfers_list = list(Backend.accounts[account]['Transfers'].keys())
        transfers_list.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date(), reverse=True)
        transfer_cards = 0
        for i, date in enumerate(transfers_list):
            date_to_date = datetime.strptime(date, '%Y-%m-%d').date()
            if date_to_date >= end_date:
                if i==0:
                    card = self.generate_month_carditem(int(date_to_date.year), int(date_to_date.month))
                    self.ids.transfers_list.add_widget(card)
                elif date_to_date.month!=datetime.strptime(transfers_list[i-1], '%Y-%m-%d').date().month:
                    card = self.generate_month_carditem(int(date_to_date.year), int(date_to_date.month))
                    self.ids.transfers_list.add_widget(card)

                for transfer in Backend.accounts[account]['Transfers'][date]:
                    purpose = transfer[1]
                    amount  = transfer[0]
                    card = self.generate_transfer_carditem(date, purpose, amount, transfer_cards)
                    self.ids.transfers_list.add_widget(card)
                    transfer_cards += 1
    
class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Window.size = (400,700)
        self.create_items_for_dropdowns_and_buttons()
        self.slider_labelsize_current = Backend.settings['Labelsize']
        self.slider_titlesize_current = Backend.settings['Titlesize']
        self.slider_linewidth_current = Backend.settings['Linewidth']
        self.slider_markersize_current = Backend.settings['Markersize']

        self.bg_color                     = Colors.bg_color
        self.bg_color_light               = Colors.bg_color_light
        self.text_color                   = Colors.text_color
        self.primary_color                = Colors.primary_color
        self.button_disable_onwhite_color = Backend.button_disable_onwhite_color
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
        self.add_value_amountfield  = self.dialog_add_value.content_cls.ids.amountfield
        self.add_value_purposefield = self.dialog_add_value.content_cls.ids.purposefield
        self.add_value_datefield    = self.dialog_add_value.content_cls.ids.datefield
        self.filter_buttons = [self.screen.ids.main.ids.onemonth_button, self.screen.ids.main.ids.threemonths_button, self.screen.ids.main.ids.sixmonths_button, 
                               self.screen.ids.main.ids.oneyear_button, self.screen.ids.main.ids.threeyears_button]

        date = self.dialog_date.today.strftime('%Y-%m-%d')
        self.add_value_datefield.text = date
        self.money_transfer_datefield.text = date
        
        self.create_dropdownmenus()
        self.add_account_status_to_mainscreen()
        Backend.generate_carditems(10)
        
        
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
                content_cls=DatePickerContent(Backend),
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
            self.money_transfer_datefield.text = Backend.today_str
            
            #insert transfer into transfers_list and update account status
            if date in Backend.accounts[account_to]['Transfers'].keys():
                Backend.accounts[account_to]['Transfers'][date].append([amount, 'From {} to {}'.format(account_from, account_to)])
            else:
                Backend.accounts[account_to]['Transfers'][date] = [[amount, 'From {} to {}'.format(account_from, account_to)]]
            if date in Backend.accounts[account_from]['Transfers'].keys():
                Backend.accounts[account_from]['Transfers'][date].append([-amount, 'From {} to {}'.format(account_from, account_to)])
            else:
                Backend.accounts[account_from]['Transfers'][date] = [[-amount, 'From {} to {}'.format(account_from, account_to)]] 

            Backend.fill_status_of_account(account_to)
            Backend.fill_status_of_account(account_from)
            self.update_main_accountview(account_to)
            self.update_main_accountview(account_from)

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
            self.add_value_datefield.text = Backend.today_str
            
            #insert transfer into transfers_list and update account status
            if date in Backend.accounts[account]['Transfers'].keys():
                Backend.accounts[account]['Transfers'][date].append([amount, purpose])
            else:
                Backend.accounts[account]['Transfers'][date] = []
                Backend.accounts[account]['Transfers'][date].append([amount, purpose])
            Backend.fill_status_of_account(account)
            self.update_main_accountview(account)

    def update_main_accountview(self, account):
            self.AmountLabels[account].text     = str(Backend.accounts[account]['Status'][Backend.today_str])+' €'
            if Backend.accounts[account]['Status'][Backend.today_str]<0:
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
        acclabel   = MDLabel(text=acc, font_style='Button')
        acclabel.color = Colors.text_color
        acclabel.halign = 'center'
        contentbox.add_widget(acclabel)
    
        last_date = list(Backend.accounts[acc]['Status'].keys())
        last_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
        last_date = last_date[-1]
        
        amlabel = MDLabel(text=str(Backend.accounts[acc]['Status'][last_date])+' €', font_style='Button')
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
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(Spacer_Horizontal(0.05))
        
        labels = ['Account', 'Current Status', 'End Month Status']
        for label in labels:
            header_label = MDLabel(text=label, font_style="Button")
            header_label.color = Colors.text_color
            header_label.halign = 'center'
            header.add_widget(header_label)

        #scrollview items
        for acc in Backend.accounts:
            carditem = self.generate_main_carditem(acc)
            self.screen.ids.main.accountsview.add_widget(carditem)
            self.screen.ids.main.accountsview.add_widget(Spacer_Vertical('6dp'))

    def go_to_account(self, acc):
        self.current_account = acc
        self.screen.ids.main.manager.current = 'Account'  
    
    def go_to_mainscreen(self, instance):
        self.screen.ids.main.manager.current = 'Main' 
            
    def build(self):
        return self.screen
        

     

    

App = DemoApp()
App.run()