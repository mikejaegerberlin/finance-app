from logging import root
from kivymd import app
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
from backend.totalplot import TotalPlot
from backend.piechart import PieChart
from backend.demo_setup import DemoData as data
from backend.settings import Sizes
from backend.carditems import CardItemsBackend
from screens.standing_order_screen import StandingOrdersScreen
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from screens.transfers_screen import TransfersScreen

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']

    def on_kv_post(self, instance):
        self.dialog_add_value = MDDialog(
                type="custom",
                content_cls=AddValueDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_add_value.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Add': self.execute_money_transfer(x)
                    ),
                ],
            )

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
            message = Snackbar(text=messagestring)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.dialog_add_value.dismiss()
            message = Snackbar(text="Transfered {} € from {} to {}".format(amount, account_from, account_to))
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

            data.fill_status_of_account(account_to)
            data.fill_status_of_account(account_from)
            data.save_accounts()

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
            data.fill_status_of_account(account)
            data.fill_total_status()
            data.filter_categories_within_dates(data.first_of_month_date, data.today_date)    
            self.update_plot()
            self.add_things_to_screen()
            data.save_accounts()
            
        
        
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
        self.filter_buttons = [self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        #canvas    = TotalPlot.make_plot(self.filter_buttons, data, set_xticks=False)
        #canvas.size_hint_y = 0.75
        #canvas.pos_hint = {'top': 0.98}
        
        canvas2 = TotalPlot.make_plot(self.filter_buttons, data, set_xticks=True)
        canvas2.size_hint_y = 0.98
        canvas2.pos_hint = {'top': 0.98}

        
        self.ids.assetview.clear_widgets()
        #self.ids.assetview.add_widget(canvas)
        self.ids.assetview.add_widget(canvas2)

        piecanvas = PieChart.make_plot(data.categories_amounts)
        piecanvas.size_hint_y = 1
        piecanvas.size_hint_x = 0.75
        piecanvas.pos_hint = {'top': 1, 'right': 1}
        self.ids.piechartview.add_widget(piecanvas)

        legendbox = MDBoxLayout(orientation='vertical', size_hint_x = 0.4, size_hint_y = 0.98)
        for i, label in enumerate(data.categories_amounts):
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
            legendbox.add_widget(subbox)

            subbox2 = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color)
            total = round(data.categories_amounts[label]/data.categories_total*100, 1)
            label2 = MDLabel(text='')
            label2.color = Colors.text_color
            label2.halign = 'right'
            label2.size_hint_x = 0.25
            label3 = MDLabel(text=str(round(data.categories_amounts[label],2))+'€ = '+str(total)+'%', font_style='Caption')
            label3.color = Colors.text_color
            label3.halign = 'left'
            label3.size_hint_x = 0.75
            subbox2.add_widget(label2)
            subbox2.add_widget(label3)
            legendbox.add_widget(subbox2)

        self.ids.piechartview.add_widget(legendbox)
        legendbox.pos_hint = {'top': 1, 'left': 0.4}


       
        #self.ids.piechartview.clear_widgets()
        #self.ids.piechartview.add_widget(canvas3)

        #label = MDLabel(text='Total status (monthly)', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 1})
        #label.color = Colors.text_color
        #self.ids.assetview.add_widget(label)

        #label2 = MDLabel(text='Monthly profit', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.08, halign='center', pos_hint={'top': 0.3})
        #label2.color = Colors.text_color
        #self.ids.assetview.add_widget(label2)
       
        label = MDLabel(text='Monthly profit', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 0.99})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)

        

    def add_things_to_screen(self):
       
        self.ids.month_label.text = 'Profit '+self.months[int(data.today_date.month)-1]+' '+str(data.today_date.year)
        profit = round(TotalPlot.profits_date[self.months[int(data.today_date.month)-1]+' '+str(data.today_date.year)], 2)

        self.ids.status_month_label.text = str(profit)+' €'
        self.ids.status_month_label.color = Colors.green_color if profit>=0 else Colors.error_color
   