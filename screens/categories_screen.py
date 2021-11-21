from typing import Text
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
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from dialogs.selection_dialogs import MonthSelectionDialogContent
from datetime import datetime

class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs) 
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.months_dict     = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Dez': 12}
    
    def create_screen(self):
        self.filter_buttons = [self.ids.oneyear_button, self.ids.threeyears_button, self.ids.fiveyears_button,
                               self.ids.tenyears_button, self.ids.all_button]
        self.selected_month = data.today_date.month
        self.selected_year = data.today_date.year                       
        self.update_plot(filterbutton_clicked=False)
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
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_add_category(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.execute_add_remove_category(x)
                    ),
                ],
            )

        self.dialog_select_month = MDDialog(
                type="custom",
                content_cls=MonthSelectionDialogContent(),
                title="Detailed overiew period",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Cancel': self.dismiss_dialog_select_month(x)
                    ),
                    MDFlatButton(
                        text="OK", theme_text_color='Custom', text_color=Colors.bg_color, on_release=lambda x='Add': self.change_month_overview(x)
                    ),
                ],
            )
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def dismiss_dialog_select_month(self, instance):
        self.dialog_select_month.content_cls.reset_dialog_after_dismiss()
        self.dialog_select_month.dismiss()
        
    def dismiss_dialog_add_category(self, instance):
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.reset_dialog_after_dismiss()    

    def hook_keyboard(self, window, key, *largs):
       if key == 27:
           self.app.go_to_main()
           return True 

    def open_dialog_select_month(self):
        years = data.get_all_years_of_transfers()
        self.dialog_select_month.content_cls.update_years()
        snackbar = False
        if len(years.keys())>1:
            self.dialog_select_month.open()
        elif len(years.keys())==1:
            months = 0
            for key in years:
                months = len(years[key])
            if months>1:
                self.dialog_select_month.open()
            else:
                snackbar = True
        
        if snackbar or len(years.keys())==0:
            if len(data.accounts)>0:
                messagestring = 'At least data in two months is required.'
            else:
                messagestring = 'No accounts.'
            message = Snackbar(text=messagestring, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()

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
        self.update_plot(filterbutton_clicked=False)
       

    def execute_add_remove_category(self, instance):
        category = self.dialog_add_category.content_cls.namefield.text
        #add category
        if self.dialog_add_category.content_cls.namefield.hint_text == "Category name":
            data.categories.append(category)
            active_plots = 0
            for cat in ScreenSettings.settings['CategoriesScreen']['SelectedGraphs']:
                if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='down':
                    active_plots += 1
            ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][category]='down' if active_plots < 3 else 'normal'
            ScreenSettings.save(self.app.demo_mode)
        #remove category
        else:
            for i, cat in enumerate(data.categories):
                if cat==category:
                    data.categories.pop(i)
                    break
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.reset_dialog_after_dismiss()    
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
        self.update_plot(filterbutton_clicked=False)
        ScreenSettings.save(self.app.demo_mode)

    def button_clicked(self, instance):
        for button in self.filter_buttons:
            if button==instance:
                button.md_bg_color = Colors.text_color
                button.text_color  = Colors.bg_color
            else:
                button.md_bg_color = Colors.bg_color
                button.text_color  = Colors.text_color
        self.update_plot(filterbutton_clicked=True)

    def add_label_card(self, text):
        card       = MDCard(size_hint_y=None, height='20dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        label2 = MDLabel(text=text, font_style='Caption')
        label2.color = Colors.text_color
        label2.halign = 'center'
        card.add_widget(label2)
        self.ids.category_list.add_widget(card)   
        self.ids.category_list.add_widget(Spacer_Vertical('3dp')) 

    def update_plot(self, filterbutton_clicked):
        self.ids.categoryview.clear_widgets()
        canvas    = CategoryPlot.make_plot(self.filter_buttons, data, self.selected_year, self.selected_month, filterbutton_clicked)
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
            sum = data.get_sum_of_category(cat, self.selected_month, self.selected_year)
            sorted_categories[cat] = sum
            cat_colors[cat] = Colors.piechart_colors[i]
            if sum<=0:
                total_expenditure += sum
        sorted_categories = dict(sorted(sorted_categories.items(), key=lambda item: item[1]))

        self.IconBoxes = {}
        
        cardcount = 0
        for cat in sorted_categories:         
            if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='down':
                if cardcount==0:
                    self.add_label_card(text='Selected categories in {} {}'.format(self.months[self.selected_month-1], self.selected_year))                
                carditem = self.generate_main_carditem(cat, sorted_categories[cat], total_expenditure, cat_colors[cat])
                self.ids.category_list.add_widget(carditem)
                self.ids.category_list.add_widget(Spacer_Vertical('6dp'))
                cardcount += 1
            
        cardcount = 0
        label = False
        for cat in sorted_categories:
            if sorted_categories[cat]!=0 and ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='normal':
                if cardcount==0:
                    self.add_label_card(text='Other categories in {} {}'.format(self.months[self.selected_month-1], self.selected_year))    
                    label = True
                carditem = self.generate_main_carditem(cat, sorted_categories[cat], total_expenditure, cat_colors[cat])
                self.ids.category_list.add_widget(carditem)
                self.ids.category_list.add_widget(Spacer_Vertical('6dp'))
                cardcount += 1

        cardcount = 0
        for cat in sorted_categories:
            if sorted_categories[cat]==0 and ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='normal':
                if cardcount==0 and label==False:
                    self.add_label_card(text='Other categories in {} {}'.format(self.months[self.selected_month-1], self.selected_year))   
                carditem = self.generate_main_carditem(cat, sorted_categories[cat], total_expenditure, cat_colors[cat])
                self.ids.category_list.add_widget(carditem)
                self.ids.category_list.add_widget(Spacer_Vertical('6dp'))    
                cardcount += 1    
        self.add_label_card(text='Tap on category to see trend.') 
        card       = MDCard(size_hint_y=None, height='22dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, elevation=0)
        self.ids.category_list.add_widget(card)

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

    def select_category(self, cat):
        active_plots = 0
        for cat2 in data.categories:
            if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat2] == 'down':
                active_plots += 1
        if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='normal':
            if active_plots < 3: 
                ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat] = 'down'
                self.update_plot(filterbutton_clicked=False)
            else:
                message = Snackbar(text='Max. 3 categories can be selected.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
                message.bg_color=Colors.black_color
                message.text_color=Colors.text_color
                message.open()
        else:
            if active_plots > 1: 
                ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat] = 'normal'
                self.update_plot(filterbutton_clicked=False)
            else:
                message = Snackbar(text='At least 1 category must be selected.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
                message.bg_color=Colors.black_color
                message.text_color=Colors.text_color
                message.open()

    def generate_main_carditem(self, cat, sum, total, color):
        card       = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color, on_release=lambda x=cat:self.select_category(cat))
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
        
       
    