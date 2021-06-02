from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivymd.uix.card import MDCard
from kivy.graphics import *
from datetime import datetime
from dateutil.relativedelta import relativedelta 
from dialogs.dialogs_empty_pythonside import ChangeTransferitemContent
from dialogs.dialogs_empty_pythonside import Spacer_Horizontal
from backend.colors import Colors
from backend.demo_setup import DemoData as data
from backend.carditems import CardItemsBackend

class AccountScreen(Screen):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs) 
        self.create_dialogs()
 
    def on_pre_enter(self):
        self.ids.accountscreen_toolbar.title = data.current_account + ' transfers'
        self.filter_buttons = [self.ids.twoweeks_button, self.ids.onemonth_button, 
                               self.ids.threemonths_button, self.ids.sixmonths_button, self.ids.custom_button]
        CardItemsBackend.generate_carditems(10)
        self.fill_transfers_list(data.current_account)

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
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Change': self.check_and_execute_change_transfer_item(x)
                    ),
                ],
        )

    def button_clicked(self, instance):
        CardItemsBackend.generate_carditems(3)
        for button in self.filter_buttons:
            if button==instance:
                button.md_bg_color = Colors.text_color
                button.text_color  = Colors.bg_color
            else:
                button.md_bg_color = Colors.bg_color
                button.text_color  = Colors.text_color
        self.fill_transfers_list(data.current_account)
 
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

    def check_and_execute_change_transfer_item(self, instance):
        new_date    = self.dialog_change_transferitem.content_cls.ids.datefield.text
        new_purpose = self.dialog_change_transferitem.content_cls.ids.purposefield.text
        old_date    = self.selected_card[0].text
        old_purpose = self.selected_card[1].text
        old_amount  = float(self.selected_card[2].text.replace(' €',''))
        try:
            new_amount  = float(self.dialog_change_transferitem.content_cls.ids.amountfield.text.replace(' €',''))
            print (new_amount, old_amount)
            self.change_transfer_item(new_date, old_date, new_purpose, old_purpose, new_amount, old_amount, data.current_account)
            if 'From' in old_purpose and 'to' in old_purpose:
                account_from = old_purpose.split(' ')[1]
                account_to   = old_purpose.split(' ')[3]
                other_account = account_to if account_from==data.current_account else account_from
                self.change_transfer_item(new_date, old_date, new_purpose, old_purpose, -new_amount, -old_amount, other_account)
            data.save_accounts()
            self.message_after_change_transfer_item(new_date, old_date, new_purpose, old_purpose, new_amount, old_amount)
        except:
            message = Snackbar(text='Amount must be number.')
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()

    def change_transfer_item(self, new_date, old_date, new_purpose, old_purpose, new_amount, old_amount, account):
        print (account)
        print (new_amount)
        print (old_amount)
        if not new_date in data.accounts[account]['Transfers'].keys():
            data.accounts[account]['Transfers'][new_date] = [[new_amount, new_purpose]]
        else:
            data.accounts[account]['Transfers'][new_date].append([new_amount, new_purpose])
        
        if len(data.accounts[account]['Transfers'][old_date])==1:
            del data.accounts[account]['Transfers'][old_date]
        else:
            for i, transfer in enumerate(data.accounts[account]['Transfers'][old_date]):
                if transfer[0]==old_amount and transfer[1]==old_purpose:
                    data.accounts[account]['Transfers'][old_date].pop(i)       
        self.fill_transfers_list(account)
        data.fill_status_of_account(account)

    def message_after_change_transfer_item(self, new_date, old_date, new_purpose, old_purpose, new_amount, old_amount):
        if 'From' in old_purpose and 'to' in old_purpose:
            account_from = old_purpose.split(' ')[1]
            account_to   = old_purpose.split(' ')[3]
            other_account = account_to if account_from==data.current_account else account_from
            message = 'Changed transfer also in account {}.'.format(other_account)
        else:
            message = ''
            if new_date!=old_date:
                message += 'Changed date from {} to {}. '.format(old_date, new_date)
            if new_purpose!=old_purpose:
                message += 'Changed purpose from {} to {}. '.format(old_purpose, new_purpose)
            if new_amount!=old_amount:
                message += 'Changed amount from {} to {}. '.format(old_amount, new_amount)    
        message = Snackbar(text=message)
        message.bg_color=Colors.black_color
        message.text_color=Colors.text_color
        message.open()
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
            if len(data.accounts[data.current_account]['Transfers'][date])==1:
                check_purposelabel = data.accounts[data.current_account]['Transfers'][date][0][1]
                del data.accounts[data.current_account]['Transfers'][date]
                
            else:
                for i, transfer in enumerate(data.accounts[data.current_account]['Transfers'][date]):
                    if transfer[0]==float(amountlabel.text.replace(' €','')) and transfer[1]==purposelabel.text:
                        data.accounts[data.current_account]['Transfers'][date].pop(i)
                        check_purposelabel = transfer[1]
                            
            self.ids.transfers_list.remove_widget(card)
            data.fill_status_of_account(data.current_account)

            if 'From' in check_purposelabel and 'to' in check_purposelabel:
                account_from = check_purposelabel.split(' ')[1]
                account_to   = check_purposelabel.split(' ')[3]
                delete_account = account_to if account_from==data.current_account else account_from
                if len(data.accounts[delete_account]['Transfers'][date])==1:
                    del data.accounts[delete_account]['Transfers'][date]
                
                else:
                    for i, transfer in enumerate(data.accounts[delete_account]['Transfers'][date]):
                        if transfer[0]==-float(amountlabel.text.replace(' €','')) and transfer[1]==check_purposelabel:
                            data.accounts[delete_account]['Transfers'][date].pop(i)
                data.fill_status_of_account(delete_account)
                message_text = 'Deleted transfer also from account {}.'.format(delete_account)   
            else:
                message_text = 'Deleted {} for {} on {}'.format(amountlabel.text, purposelabel.text, datelabel.text)
            message = Snackbar(text=message_text)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            data.save_accounts()
        self.transfer_dropdown.dismiss()
        
     
    def generate_month_carditem(self, year, month):
        card           = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color)
        contentbox     = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[10,10,10,10])   
        acclabel       = MDLabel(text=data.months[month-1]+' '+str(year), font_style='Button')
        acclabel.color = Colors.text_color
        contentbox.add_widget(Spacer_Horizontal(0.03))
        contentbox.add_widget(acclabel)
        card.add_widget(contentbox)
        return card

    def generate_transfer_carditem(self, date, purpose, amount, cardnumber):
        if cardnumber==len(CardItemsBackend.cards_transferitem):
            CardItemsBackend.generate_carditems(1)
        card              = CardItemsBackend.cards_transferitem[cardnumber][0]
        box               = CardItemsBackend.cards_transferitem[cardnumber][1]
        datelabel         = CardItemsBackend.cards_transferitem[cardnumber][2]
        purposelabel      = CardItemsBackend.cards_transferitem[cardnumber][3]
        amountlabel       = CardItemsBackend.cards_transferitem[cardnumber][4]
        box.md_bg_color   = Colors.bg_color
        datelabel.text    = date
        purposelabel.text = purpose
        amountlabel.text  = str(amount)+' €'
        amountlabel.color = Colors.error_color if amount<0 else Colors.green_color
        card.on_release   = lambda x=box: self.open_transfer_dropdown(card, box, datelabel, purposelabel, amountlabel)
        return card


    def fill_transfers_list(self, account):
        self.ids.transfers_list.clear_widgets()
        start_date = data.today_date
        for i, button in enumerate(self.filter_buttons):
            if button.md_bg_color[0]==1:
                break
        if i<=3:
            timedeltas = [relativedelta(weeks=2), relativedelta(months=1), relativedelta(months=3), relativedelta(months=6)]
            timedelta  = timedeltas[i]
            end_date   = data.today_date - timedelta
        if i==4:
            end_date = list(data.accounts[account]['Transfers'].keys())
            end_date.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
            end_date = datetime.strptime(end_date[0], '%Y-%m-%d').date()
        
        transfers_list = list(data.accounts[account]['Transfers'].keys())
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

                for transfer in data.accounts[account]['Transfers'][date]:
                    purpose = transfer[1]
                    amount  = transfer[0]
                    card = self.generate_transfer_carditem(date, purpose, amount, transfer_cards)
                    self.ids.transfers_list.add_widget(card)
                    transfer_cards += 1