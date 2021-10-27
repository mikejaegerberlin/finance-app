from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivymd.uix.card import MDCard
from kivy.graphics import *
from datetime import datetime
from dialogs.add_value_dialog import AddValueDialogContent
from dialogs.manage_accounts_dialog import ManageAccountsDialogContent
from dialogs.dialogs_empty_pythonside import Spacer_Horizontal, Spacer_Vertical
from backend.colors import Colors
from backend.accountplot import AccountPlot
from backend.demo_setup import DemoData as data
from dialogs.add_value_dialog import AddValueDialogContent
from dialogs.selection_dialogs import GraphSelectionDialogContent
from kivy.uix.screenmanager import SlideTransition
from backend.settings import ScreenSettings
from kivy.base import EventLoop
from kivy.metrics import dp

class AccountsScreen(Screen):
    def __init__(self, **kwargs):
        super(AccountsScreen, self).__init__(**kwargs)

    def initialize_dialogs(self):
        self.dialog_add_value = MDDialog(
                type="custom",
                content_cls=AddValueDialogContent(),
                title="Add transfer",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_add_value(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_money_transfer(x)
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

        self.dialog_graph_selection = MDDialog(
                type="custom",
                content_cls=GraphSelectionDialogContent(),
                title="Displayed trends",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dialog_graph_selection.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_graph_selection(x)
                    ),
                ],
            )
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

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
        

    def hook_keyboard(self, window, key, *largs):
       if key == 27:
           self.app.go_to_main()
           return True 

    def execute_graph_selection(self, instance):
        self.dialog_graph_selection.dismiss()
        self.update_plot()
        for acc in data.accounts:
            self.update_main_accountview(acc)
        ScreenSettings.save(self.app.demo_mode)

    #def on_pre_enter(self):
    #    self.app.update_accounts_screen()
       
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
            self.dialog_manage_accounts.content_cls.accountfield.text = ''
            self.dialog_manage_accounts.content_cls.amountfield.text = ''
            self.dialog_manage_accounts.content_cls.datefield.text = data.today_str
            data.accounts[account] = {}
            for key in data.keys_list:
                data.accounts[account][key] = {}
            data.accounts[account]['Transfers'][date] = []
            data.accounts[account]['Transfers'][date].append([amount, 'Start amount', 'Start amount'])
            ScreenSettings.settings['AccountScreen']['SelectedGraphs'][account] = 'down'
            ScreenSettings.save(self.app.demo_mode)
            self.dialog_graph_selection.content_cls.update_list()
            data.fill_status_of_account(account)
            self.ids.accountsview.clear_widgets()
            self.AmountLabels = {}
            self.IconBoxes = {}
            for i, acc in enumerate(data.accounts):
                carditem = self.generate_main_carditem(acc, i)
                self.ids.accountsview.add_widget(carditem)
                self.ids.accountsview.add_widget(Spacer_Vertical('6dp'))
            card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
            label2 = MDLabel(text='Tap on account to see transfers.', font_style='Caption')
            label2.color = Colors.text_color
            label2.halign = 'center'
            card.add_widget(label2)
            self.ids.accountsview.add_widget(card)
            card       = MDCard(size_hint_y=None, height='60dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
            self.ids.accountsview.add_widget(card)

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
        self.ids.accountsview.clear_widgets()
        self.AmountLabels = {}
        self.IconBoxes = {}
        for i, acc in enumerate(data.accounts):
            carditem = self.generate_main_carditem(acc, i)
            self.ids.accountsview.add_widget(carditem)
            self.ids.accountsview.add_widget(Spacer_Vertical('6dp'))
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        label2 = MDLabel(text='Tap on account to see transfers.', font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'center'
        card.add_widget(label2)
        self.ids.accountsview.add_widget(card)
        card       = MDCard(size_hint_y=None, height='60dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        self.ids.accountsview.add_widget(card)

        self.dialog_manage_accounts.dismiss()
        message = Snackbar(text='Deleted account {}.'.format(account), snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
        message.bg_color=Colors.black_color
        message.text_color=Colors.text_color
        message.open()
        data.filter_categories_within_dates(data.first_of_month_date, data.today_date)  
        self.dialog_manage_accounts.content_cls.accountfield.text = ''
        self.dialog_manage_accounts.content_cls.amountfield.text = ''
        self.dialog_manage_accounts.content_cls.datefield.text = data.today_str    


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
        self.update_plot()

    
    def update_plot(self):
        ScreenSettings.update()
        self.filter_buttons = [self.ids.onemonth_button, self.ids.threemonths_button, self.ids.sixmonths_button, 
                               self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        canvas    = AccountPlot.make_plot(self.filter_buttons, data)
        canvas.pos_hint = {'top': 0.99}
        self.ids.assetview.clear_widgets()
        self.ids.assetview.add_widget(canvas)
        label = MDLabel(text='Trend of each account', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 0.99})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)

    def update_main_accountview(self, account):
        self.AmountLabels[account].text     = str(data.accounts[account]['Status'][data.today_str])+' €'
        if data.accounts[account]['Status'][data.today_str]<0:
            self.AmountLabels[account].color = Colors.error_color
        else:
            self.AmountLabels[account].color = Colors.green_color

        for acc in data.accounts:
            if ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc]=='down': 
                self.IconBoxes[acc].icon = 'vector-line'
            else:
                self.IconBoxes[acc].icon = 'blank'
           

    def go_to_account(self, acc):
        data.current_account = acc
        self.app.screen.ids.main.manager.transition = SlideTransition()
        self.app.screen.ids.main.manager.current = 'Transfers'

    def generate_main_carditem(self, acc, i):
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, on_release=lambda x=acc:self.go_to_account(acc))
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[20,20,20,20])   

        subbox = MDBoxLayout(orientation='horizontal')
        icon = MDIcon(icon='vector-line', theme_text_color='Custom')
        icon.color=Colors.piechart_colors[i]
        icon.halign = 'right'
        label2 = MDLabel(text=acc, font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'left'
        if ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc]=='normal':
            icon.icon = 'blank'
        self.IconBoxes[acc] = icon
        subbox.add_widget(icon)
        subbox.add_widget(label2)   
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
        '''self.ids.assetview.clear_widgets()
        canvas = AccountPlot.make_plot(self.filter_buttons, data)
        canvas.pos_hint = {'top': 1}
        self.ids.assetview.add_widget(canvas)
        label = MDLabel(text='Trend of each account', font_style='Subtitle1', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 1})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)'''
        self.AmountLabels = {}
        self.IconBoxes = {}

        #header of table scrollview
        self.ids.accountsview_header.clear_widgets()
        header = self.ids.accountsview_header
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(Spacer_Horizontal(0.05))
        
        labels = ['ACCOUNT', 'STATUS', 'END MONTH']
        for label in labels:
            header_label = MDLabel(text=label, font_style="Subtitle2")
            header_label.color = Colors.bg_color
            header_label.halign = 'center'
            header.add_widget(header_label)

        #scrollview items
        self.ids.accountsview.clear_widgets()
        for i, acc in enumerate(data.accounts):
            carditem = self.generate_main_carditem(acc, i)
            self.ids.accountsview.add_widget(carditem)
            self.ids.accountsview.add_widget(Spacer_Vertical('6dp'))
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        label2 = MDLabel(text='Tap on account to see transfers.', font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'center'
        card.add_widget(label2)
        self.ids.accountsview.add_widget(card)
        card       = MDCard(size_hint_y=None, height='60dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        self.ids.accountsview.add_widget(card)
      
