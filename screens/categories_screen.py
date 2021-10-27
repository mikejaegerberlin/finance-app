from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.dialog import MDDialog
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivymd.uix.card import MDCard
from kivy.graphics import *
from dialogs.dialogs_empty_pythonside import Spacer_Vertical
from backend.colors import Colors
from backend.demo_setup import DemoData as data
from kivymd.uix.button import MDFlatButton
from backend.categoryplot import CategoryPlot
from dialogs.selection_dialogs import GraphSelectionDialogCategoriesContent
from dialogs.add_category_dialog import AddCategoryDialogContent
from backend.settings import ScreenSettings
from dialogs.dialogs_empty_pythonside import Spacer_Horizontal
from kivy.base import EventLoop

class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs) 
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.months_dict     = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Dez': 12}
    
    def create_screen(self):
        self.filter_buttons = [self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        self.update_plot()
        self.create_mainlist()
        self.dialog_graph_selection = MDDialog(
                type="custom",
                content_cls=GraphSelectionDialogCategoriesContent(),
                title='Displayed trends and detailed overview period',
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dialog_graph_selection.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_graph_selection(x)
                    ),
                ],
            )

        self.dialog_add_category = MDDialog(
                type="custom",
                content_cls=AddCategoryDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dialog_add_category.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_add_remove_category(x)
                    ),
                ],
            )
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
       if key == 27:
           self.app.go_to_main()
           return True 

    def execute_add_remove_category(self, instance):
        category = self.dialog_add_category.content_cls.namefield.text
        #add category
        if self.dialog_add_category.content_cls.namefield.hint_text == "Category name":
            data.categories.append(category)
            ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][category]='normal'
            ScreenSettings.save(self.app.demo_mode)
        #remove category
        else:
            for i, cat in enumerate(data.categories):
                if cat==category:
                    data.categories.pop(i)
                    break
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.namefield.text = ''
        self.app.global_update()

    def remove_category_from_transfers(self, category):
        for acc in data.accounts:
            for date in data.accounts[acc]['Transfers']:
                to_delete = []
                for i, transfer in enumerate(data.accounts[acc]['Transfers'][date]):
                    if transfer[2]==category:
                        to_delete.append(i)  
                for q, spot in enumerate(to_delete):
                    del data.accounts[acc]['Transfers'][date][spot-q]

    def execute_graph_selection(self, instance):
        self.dialog_graph_selection.dismiss()
        self.update_plot()
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
        self.ids.categoryview.clear_widgets()
        canvas    = CategoryPlot.make_plot(self.filter_buttons, data)
        canvas.pos_hint = {'top': 0.99}
        self.ids.categoryview.clear_widgets()
        self.ids.categoryview.add_widget(canvas)
        label = MDLabel(text='Trend of each category', font_style='Caption', md_bg_color=Colors.bg_color, size_hint_y=0.1, halign='center', pos_hint={'top': 0.99})
        label.color = Colors.text_color
        self.ids.categoryview.add_widget(label)

        #scrollview items
        self.ids.category_list.clear_widgets()
        sorted_categories = {}
        total_expenditure = 0
        cat_colors = {}
        for i, cat in enumerate(data.categories):
            sum = data.get_sum_of_category(cat, data.first_of_month_date, data.today_date)
            sorted_categories[cat] = sum
            cat_colors[cat] = Colors.piechart_colors[i]
            if sum<=0:
                total_expenditure += sum
        sorted_categories = dict(sorted(sorted_categories.items(), key=lambda item: item[1]))

        self.IconBoxes = {}
        for cat in sorted_categories:
            #if sorted_categories[cat]!=0:
            if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='down':
                carditem = self.generate_main_carditem(cat, sorted_categories[cat], total_expenditure, cat_colors[cat])
                self.ids.category_list.add_widget(carditem)
                self.ids.category_list.add_widget(Spacer_Vertical('6dp'))
        for cat in sorted_categories:
            if sorted_categories[cat]!=0 and ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='normal':
                carditem = self.generate_main_carditem(cat, sorted_categories[cat], total_expenditure, cat_colors[cat])
                self.ids.category_list.add_widget(carditem)
                self.ids.category_list.add_widget(Spacer_Vertical('6dp'))
        
        #card       = MDCard(size_hint_y=None, height='5dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        #self.ids.category_list.add_widget(card)

    def create_mainlist(self):
        #header of table scrollview
        header = self.ids.category_header
        header.md_bg_color = Colors.primary_color
        header.radius = [20,20,20,20]
        header.add_widget(Spacer_Horizontal(0.05))
        
        labels = ['CATEGORY', 'SUM', 'PERCENT']
        sizes = [0.37, 0.33, 0.3]
        for q, label in enumerate(labels):
            header_label = MDLabel(text=label, font_style="Subtitle2")
            header_label.color = Colors.bg_color
            header_label.halign = 'center'
            header_label.size_hint_x = sizes[q]
            header.add_widget(header_label)

        

    def generate_main_carditem(self, cat, sum, total, color):
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color)
        contentbox = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color_light, radius=[20,20,20,20])   
        contentbox.size_hint_x = 1

        subbox = MDBoxLayout(orientation='horizontal')
        subbox.size_hint_x = 0.4
        icon = MDIcon(icon='card', theme_text_color='Custom')
        icon.color=color
        icon.halign = 'right'
        label2 = MDLabel(text=cat, font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'center'
        if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='normal':
            icon.icon = 'blank'
        self.IconBoxes[cat] = icon
        icon.size_hint_x = 0.125
        label2.size_hint_x = 0.275
        subbox.add_widget(icon)
        subbox.add_widget(label2)   
        contentbox.add_widget(subbox)

        amlabel = MDLabel(text=str(round(sum,2))+' €', font_style='Subtitle2')
        amlabel.color = Colors.error_color if sum<0 else Colors.green_color
        amlabel.halign = 'center'
        amlabel.size_hint_x = 0.3
        contentbox.add_widget(amlabel)

        if sum<0:
            perclabel = MDLabel(text=str(round(sum/total*100,2))+' %', font_style='Subtitle2')
        else:
            perclabel = MDLabel(text='-', font_style='Subtitle2')
        perclabel.color = Colors.text_color
        perclabel.halign = 'center'
        perclabel.size_hint_x = 0.3
        contentbox.add_widget(perclabel)

        card.add_widget(contentbox)
        
        return card
        
       
    