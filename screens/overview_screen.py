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
from dialogs.selection_dialogs import MonthSelectionDialogContent

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.months_text          = ['January', 'February', 'March', 'April', 'Mai', 'June', 'July', 'August', 'September', 'Oktober', 'November', 'December']
        self.months               = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']


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

        self.dialog_select_month = MDDialog(
                type="custom",
                content_cls=MonthSelectionDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_select_month.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Add': self.change_month_overview(x)
                    ),
                ],
            )

        self.selected_month = data.today_date.month
        self.selected_year = data.today_date.year

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
        self.update_plot()
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
        
        canvas2 = TotalPlot.make_plot(self.filter_buttons, data, self.selected_month, self.selected_year, set_xticks=True)
        canvas2.size_hint_y = 0.98
        canvas2.pos_hint = {'top': 0.98}

        
        self.ids.assetview.clear_widgets()
        #self.ids.assetview.add_widget(canvas)
        self.ids.assetview.add_widget(canvas2)

        self.ids.piechartview.clear_widgets()
        piecanvas = PieChart.make_plot(data.categories_expenditures)
        piecanvas.size_hint_y = 0.95
        piecanvas.size_hint_x = 0.7
        piecanvas.pos_hint = {'top': 1, 'right': 1}
        self.ids.piechartview.size = 100, 100
        self.ids.piechartview.add_widget(piecanvas)
       
        self.ids.legend_list.clear_widgets()
        for i, label in enumerate(data.categories_expenditures):
            card = MDCard(size_hint_y=None, height='40dp', md_bg_color=Colors.bg_color)
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

       
        #self.ids.piechartview.clear_widgets()
        #self.ids.piechartview.add_widget(canvas3)

        #label = MDLabel(text='Total status (monthly)', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 1})
        #label.color = Colors.text_color
        #self.ids.assetview.add_widget(label)

        #label2 = MDLabel(text='Monthly profit', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.08, halign='center', pos_hint={'top': 0.3})
        #label2.color = Colors.text_color
        #self.ids.assetview.add_widget(label2)
       
        label = MDLabel(text='Trend of monthly profit', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 0.99})
        label.color = Colors.text_color
        self.ids.assetview.add_widget(label)

        

    def add_things_to_screen(self):
       
        self.ids.month_button.text = self.months_text[self.selected_month-1]+' '+str(self.selected_year)
        try:
            profit = round(TotalPlot.profits_date[self.months[self.selected_month-1]+' '+str(self.selected_year)], 2)
        except:
            profit = 0

        self.ids.status_month_label.text = str(profit)+' €'
        self.ids.status_month_label.color = Colors.green_color if profit>=0 else Colors.error_color

        self.ids.status_expenditures_label.text = str(round(data.categories_expenditures_total, 2))+' €'
        self.ids.status_expenditures_label.color = Colors.green_color if data.categories_expenditures_total>=0 else Colors.error_color
   