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
from backend.categoryplot import CategoryPlot

class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs) 
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.months_dict     = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Dez': 12}
    
    def create_screen(self):
        self.filter_buttons = [self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        self.update_plot()

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
        
        canvas    = CategoryPlot.make_plot(self.filter_buttons, data)
        canvas.pos_hint = {'top': 1}
        self.ids.categoryview.clear_widgets()
        self.ids.categoryview.add_widget(canvas)
        label = MDLabel(text='Trend of each category', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 0.99})
        label.color = Colors.text_color
        self.ids.categoryview.add_widget(label)
        
       
    