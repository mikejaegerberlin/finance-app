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
        self.dialog_graph_selection = MDDialog(
                type="custom",
                content_cls=GraphSelectionDialogContent(),
                title="Displayed trends",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_graph_selection(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_graph_selection(x)
                    ),
                ],
            )
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def open_dialog_graph_selection(self):
        self.reset_values = {}
        for acc in ScreenSettings.settings['AccountScreen']['SelectedGraphs']:
            self.reset_values[acc] = ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc]
        self.dialog_graph_selection.open()

    def dismiss_dialog_graph_selection(self, instance):
        self.dialog_graph_selection.dismiss()
        self.dialog_graph_selection.content_cls.reset_dialog_after_dismiss()
       
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
        card       = MDCard(size_hint_y=None, height='20dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        label2 = MDLabel(text='Tap on account to see transfers.', font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'center'
        card.add_widget(label2)
        self.ids.accountsview.add_widget(card)
        card       = MDCard(size_hint_y=None, height='60dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        self.ids.accountsview.add_widget(card)
      
