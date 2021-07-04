from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
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
from dialogs.dialogs_empty_pythonside import Spacer_Vertical
from backend.colors import Colors
from backend.demo_setup import DemoData as data
from datetime import datetime
from dialogs.add_standingorder_dialog import AddStandingOrderDialogContent
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs) 
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.months_dict     = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Dez': 12}
        self.create_dialogs()
        
       
    #create dialogs for the screen
    def create_dialogs(self):

        content = AddStandingOrderDialogContent()
        self.dialog_add_standingorder = MDDialog(
                title="Add standing order",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x='Cancel': self.dialog_add_standingorder.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.primary_color, on_release=lambda x: self.add_standing_order(x, content)
                    ),
                ],
        )

    def add_standing_order(self, instance, content):
        order = content.add_standing_order()
        self.dialog_add_standingorder.dismiss()
        data.add_order_in_transfers(order)
        data.fill_status_of_account(order['Account'])      
        data.fill_total_status()     
        data.save_accounts()
        self.update_standingorder_list()
        
    def create_screen(self):
        self.md_bg_color = Colors.bg_color
        header = self.ids.standingorder_header
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]

        self.padding_x = [0.2, 0.11, 0.11, 0.08, 0.25, 0.25]
        labels = ['Account', 'From', 'To', 'Day', 'Purpose', 'Amount']
        for i, label in enumerate(labels):
            header_label = MDLabel(text=label, font_style="Subtitle2")
            header_label.color = Colors.text_color
            header_label.halign = 'center'
            header_label.size_hint_x = self.padding_x[i]
            header.add_widget(header_label)

        self.update_standingorder_list()

    def update_standingorder_list(self):
        #scrollview items
        self.standing_orders_list.clear_widgets()
        sorted_orders = self.sort_standingorders()
        data.standingorders['Orders'] = sorted_orders
        data.save_standingorders()
        for number in sorted_orders:
            carditem = self.generate_carditem(sorted_orders[number], number)
            self.standing_orders_list.add_widget(carditem)
            self.standing_orders_list.add_widget(Spacer_Vertical('6dp'))

    def open_standingorder_dialog(self, instance):
        self.dialog_add_standingorder.open()

    def sort_standingorders(self):
        sorted_orders = {}
        k             = 0
        for acc in data.accounts:
            dates  = []
            orders = []
            #getting all dates of standingorders
            for i in data.standingorders['Orders']:
                entry = data.standingorders['Orders'][i]
                if acc in entry['Account']:
                    month = str(self.months_dict[entry['From'].split('\n')[0]])
                    month = month if int(month)>9 else '0' + month
                    year  = entry['From'].split('\n')[1]
                    day   = entry['Day'].replace('.','')
                    day   = day if int(day)>9 else '0' + day
                    dates.append('{}-{}-{}'.format(year, month, day)) 
                    orders.append(entry)
               
            dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
                     
            #sorting
            for order in orders:
                sorted_orders[str(k)] = {}
                sorted_orders[str(k)]['Account'] = order['Account']
                sorted_orders[str(k)]['From']    = order['From']
                sorted_orders[str(k)]['To']      = order['To']
                sorted_orders[str(k)]['Day']     = order['Day']
                sorted_orders[str(k)]['Purpose'] = order['Purpose']
                sorted_orders[str(k)]['Amount']  = order['Amount']
                sorted_orders[str(k)]['MonthListed']  = order['MonthListed']
                k += 1
        return sorted_orders

    def generate_carditem(self, entry, number):
        card       = MDCard(size_hint_y=None, height='45dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color)
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[20,20,20,20])  
        for i, key in enumerate(entry):
            if i<len(list(entry.keys()))-2:
                label   = MDLabel(text=str(entry[key]), font_style='Subtitle2')
                label.color = Colors.text_color
                label.halign = 'center'
                label.size_hint_x = self.padding_x[i]
                contentbox.add_widget(label)

        label   = MDLabel(text=str(entry['Amount'])+' €', font_style='Subtitle2')
        label.color = Colors.error_color if entry['Amount']<0 else Colors.green_color
        label.halign = 'center'
        label.size_hint_x = self.padding_x[-1]
        contentbox.add_widget(label)
        card.add_widget(contentbox)
        card.on_release   = lambda x=contentbox: self.open_standingorder_dropdown(card, contentbox, number)
        return card

    def open_standingorder_dropdown(self, card, contentbox, number):
        items = ['Delete']
        standingorder_menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=item: self.delete_item(x, card, number),
            } for item in items
        ]

        self.standingorder_dropdown = MDDropdownMenu(
                    caller=card,
                    items=standingorder_menu_items,
                    width_mult=4,
                )
        contentbox.md_bg_color = Colors.bg_color
        self.standingorder_dropdown.open()
        
    def delete_item(self, instance, card, number):
        self.standing_orders_list.remove_widget(card)    
        del data.standingorders['Orders'][str(number)]
        self.standingorder_dropdown.dismiss()
        self.update_standingorder_list()
 

        

