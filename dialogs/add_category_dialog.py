from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from backend.demo_setup import DemoData as data
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar

class AddCategoryDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AddCategoryDialogContent, self).__init__(**kwargs)
        
    def update_category_items(self):
        self.category_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_category_item(x),
            } for acc in data.categories
        ]
        self.category_dropdown.items = self.category_menu_items

    def on_kv_post(self, instance):
        self.category_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_category_item(x),
            } for acc in data.categories
        ]
        self.category_dropdown = MDDropdownMenu(
            caller=MDFlatButton(),
            items=self.category_menu_items,
            position="auto",
            width_mult=4,
        )

    def add_category_button_clicked(self):
        self.namefield.focus = False
        self.ids.namefield.hint_text = "Category name"
        self.ids.namefield.text = ""
        self.ids.namefield.icon_right = "blank"
        if self.ids.add_category_button_icon.color[1] == 0:
            self.ids.add_category_button_icon.color = Colors.green_color
            self.ids.add_category_button_text.color = Colors.green_color
            self.ids.remove_category_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.remove_category_button_text.color = Colors.button_disable_onwhite_color
            
    def namefield_focus_function(self):
        if self.ids.namefield.hint_text == 'Which category':
            self.category_dropdown.caller = self.ids.namefield
            self.category_dropdown.open() 
        
    def remove_category_button_clicked(self):
        if len(data.categories)<1:
            message = Snackbar(text='No categories yet.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.ids.namefield.hint_text = "Which category"
            self.ids.namefield.icon_right = "arrow-down-drop-circle-outline"
            self.ids.namefield.keyboard_mode = 'managed'    
            self.namefield.focus = False
        
            if self.ids.remove_category_button_icon.color[0] == 0:
                self.ids.add_category_button_icon.color = Colors.button_disable_onwhite_color
                self.ids.add_category_button_text.color = Colors.button_disable_onwhite_color
                self.ids.remove_category_button_icon.color = Colors.error_color
                self.ids.remove_category_button_text.color = Colors.error_color
            
    def open_category_dropdown(self, namefield):
        namefield.hide_keyboard()
        self.category_dropdown.open()
        namefield.focus      = False

    def set_category_item(self, text_item):
        self.category_dropdown.caller.text = text_item
        self.category_dropdown.dismiss()
        self.category_dropdown.caller.focus = False
        