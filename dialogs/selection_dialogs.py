from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from datetime import datetime
from backend.demo_setup import DemoData as data
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty
from backend.settings import ScreenSettings

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''

class GraphSelectionDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(GraphSelectionDialogContent, self).__init__(**kwargs)  

    def on_kv_post(self, instance):
        self.update_list()

    def update_list(self):
        self.ids.confirm_list.clear_widgets()       
        for i, acc in enumerate(data.accounts):
            listitem = ListItemWithCheckbox(text=acc, icon='vector-line')
            listitem.ids.iconleft.theme_text_color = 'Custom'
            listitem.ids.iconleft.text_color = Colors.piechart_colors[i]
            listitem.ids.checkboxright.state = ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc]
            listitem.ids.checkboxright.on_release = lambda x=acc: self.checkbox_selected(x)
            self.ids.confirm_list.add_widget(listitem)

    def checkbox_selected(self, acc):
        if ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc]=='down':
            ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc] = 'normal'
        else:
            ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc] = 'down'

    def reset_dialog_after_dismiss(self):
        reset_values = self.app.screen.ids.accounts_screen.reset_values
        for acc in reset_values:
            ScreenSettings.settings['AccountScreen']['SelectedGraphs'][acc] = reset_values[acc]
        self.update_list()

       
class GraphSelectionDialogCategoriesContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(GraphSelectionDialogCategoriesContent, self).__init__(**kwargs)  

    def on_kv_post(self, instance):
        self.update_list()

    def update_list(self):
        self.ids.confirm_list.clear_widgets()       
        for i, cat in enumerate(data.categories):
            listitem = ListItemWithCheckbox(text=cat, icon='card')
            listitem.ids.iconleft.theme_text_color = 'Custom'
            listitem.ids.iconleft.text_color = Colors.piechart_colors[i]
            listitem.ids.checkboxright.state = ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]
            listitem.ids.checkboxright.on_release = lambda x=listitem: self.checkbox_selected(x)
            self.ids.confirm_list.add_widget(listitem)

    def checkbox_selected(self, listitem):
        cat = listitem.text
        if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='normal':
            count = 0
            for check in ScreenSettings.settings['CategoriesScreen']['SelectedGraphs']:
                if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][check]=='down':
                    count += 1
            if count<3:
                ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat] = 'down'
            else:
                listitem.ids.checkboxright.state = 'normal'
        else:
            ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat] = 'normal'

class MonthSelectionDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(MonthSelectionDialogContent, self).__init__(**kwargs)

    def reset_dialog_after_dismiss(self):
        self.ids.month_field.focus = False
        self.ids.year_field.focus = False

    def open_month_dropdown(self):
        self.ids.year_field.focus = False
        self.month_dropdown.open()

    def open_year_dropdown(self):
        self.ids.month_field.focus = False
        self.year_dropdown.open()

    def update_years(self):
        year = str(data.today_date.year)   
        self.years = data.get_all_years_of_transfers() 
        if len(self.years.keys())==0:
            self.years[str(year)] = ['']
        self.month_menu_items = [
            {
                "text": month,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=month: self.set_month_item(x),
            } for month in self.years[str(year)]
        ]
        self.year_menu_items = [
            {
                "text": year,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=year: self.set_year_item(x),
            } for year in list(self.years.keys())
        ]
        self.year_dropdown.items = self.year_menu_items
        self.month_dropdown.items = self.month_menu_items
        self.ids.month_field.text = self.years[str(year)][0]

    def on_kv_post(self, instance):
        self.years = data.get_all_years_of_transfers() 
        month = data.months_text[data.today_date.month-1]
        year = str(data.today_date.year)   
        self.ids.month_field.text = month
        self.ids.year_field.text = year
        if len(self.years.keys())==0:
            self.years[str(year)] = ['']

        self.month_menu_items = [
            {
                "text": month,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=month: self.set_month_item(x),
            } for month in self.years[str(year)]
        ]
        self.month_dropdown = MDDropdownMenu(
            caller=self.ids.month_field,
            items=self.month_menu_items,
            position="auto",
            width_mult=4,
        )

        self.year_menu_items = [
            {
                "text": year,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=year: self.set_year_item(x),
            } for year in list(self.years.keys())
        ]
        self.year_dropdown = MDDropdownMenu(
            caller=self.ids.year_field,
            items=self.year_menu_items,
            position="auto",
            width_mult=4,
        )
  
    def set_year_item(self, year):
        self.ids.year_field.text = year
        self.ids.year_field.focus = False
        self.ids.month_field.focus = False
        self.month_menu_items = [
            {
                "text": month,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=month: self.set_month_item(x),
            } for month in self.years[str(year)]
        ]
        self.month_dropdown.items = self.month_menu_items
        self.ids.month_field.text = self.years[str(year)][0]
        self.year_dropdown.dismiss() 

    def set_month_item(self, month):
        self.ids.month_field.text = month
        self.ids.year_field.focus = False
        self.ids.month_field.focus = False
        self.month_dropdown.dismiss()
       
        