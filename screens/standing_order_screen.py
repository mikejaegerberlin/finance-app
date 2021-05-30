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
        for number in data.standingorders:
            carditem = self.generate_carditem(data.standingorders[number])
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

