from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from datetime import datetime
from backend.demo_setup import DemoData as data
from kivymd.uix.picker import MDDatePicker
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

        