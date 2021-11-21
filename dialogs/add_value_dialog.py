from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from backend.demo_setup import DemoData as data
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from dialogs.add_category_dialog import AddCategoryDialogContent
from kivymd.uix.dialog import MDDialog
from datetime import datetime
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.chip import MDChip
from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout

class ContentCustomSheet(StackLayout):
    def __init__(self, **kwargs):
        super(ContentCustomSheet, self).__init__(**kwargs)

class AddValueDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AddValueDialogContent, self).__init__(**kwargs)

    def reset_dialog_after_dismiss(self):
        self.ids.accountfield.text = ''
        self.ids.amountfield.text = ''
        self.ids.purposefield.text = ''
        self.ids.categoryfield.text = ''
        self.ids.datefield.text = data.today_str 
        self.ids.accountfield.focus = False
        self.ids.amountfield.focus = False
        self.ids.purposefield.focus = False
        self.ids.categoryfield.focus = False
        self.ids.dialog_income_button_icon.color = Colors.button_disable_onwhite_color
        self.ids.dialog_income_button_text.color = Colors.button_disable_onwhite_color
        self.ids.dialog_transfer_button_icon.color = Colors.button_disable_onwhite_color
        self.ids.dialog_transfer_button_text.color = Colors.button_disable_onwhite_color
        self.ids.dialog_expenditure_button_text.color = Colors.error_color
        self.ids.dialog_expenditure_button_icon.color = Colors.error_color
        
    def update_acc_items(self):
        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]

        self.acc_dropdown.items = self.acc_menu_items
        cat_items = ['Add new category']
        for cat in data.categories:
            cat_items.append(cat)
        self.cat_menu_items = [
            {
                "text": cat,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=cat: self.set_cat_item(x),
            } for cat in cat_items
        ]

        self.cat_dropdown.items = self.cat_menu_items
      
    def on_kv_post(self, instance):
        self.create_bottomsheet()
        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]

        cat_items = ['Add new category']
        for cat in data.categories:
            cat_items.append(cat)
        self.cat_menu_items = [
            {
                "text": cat,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=cat: self.set_cat_item(x),
            } for cat in cat_items
        ]
        self.acc_dropdown = MDDropdownMenu(
            caller=self.ids.accountfield,
            items=self.acc_menu_items,
            position="bottom",
            width_mult=4,
        )

        self.cat_dropdown = MDDropdownMenu(
            caller=self.ids.categoryfield,
            items=self.cat_menu_items,
            position="auto",
            width_mult=4
        )

        self.dialog_date = MDDatePicker(primary_color=Colors.primary_color, selector_color=Colors.primary_color, 
                                        text_button_color=Colors.primary_color, text_color=Colors.bg_color, specific_text_color=Colors.bg_color,
                                        size_hint_y=None, text_weekday_color=Colors.bg_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)
        self.ids.datefield.text = self.dialog_date.today.strftime('%Y-%m-%d')

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

    def dismiss_dialog_add_category(self, instance):
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.reset_dialog_after_dismiss()            
        
    def dialog_date_ok(self, instance, value, date_range):
        date_str = value.strftime('%Y-%m-%d')
        date_date = datetime.strptime(date_str, '%Y-%m-%d').date() 
        if date_date>data.today_date:
            message = Snackbar(text='Date cannot be higher than today.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
            self.ids.datefield.text = data.today_str
        else:
            self.ids.datefield.text = date_str
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        self.ids.accountfield.focus = False
    
    def dialog_date_cancel(self, instance, value):
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        self.ids.accountfield.focus = False
    

    def open_acc_dropdown(self, accountfield):
        accountfield.hide_keyboard()
        self.acc_dropdown.caller = accountfield
        self.acc_dropdown.open()
        self.ids.purposefield.focus     = False
        self.ids.amountfield.focus      = False

    def create_bottomsheet(self):
        self.content_custom_sheet = ContentCustomSheet()
        self.custom_sheet = MDCustomBottomSheet(screen=self.content_custom_sheet)
        self.custom_sheet.radius = 15
        self.custom_sheet.radius_from = 'top'
        self.custom_sheet.overlay_color = [0,0,0,0]
        self.custom_sheet.animation = True
        self.custom_sheet.size_hint_x = 0.9
        
        first_box = MDBoxLayout(size_hint_y=0.05)
        self.content_custom_sheet.add_widget(first_box)

        first_box = MDBoxLayout(orientation='horizontal', size_hint_y=0.1)
        first_box.add_widget(MDBoxLayout(size_hint_x=0.03))
        label1 = MDLabel(text='Available categories', font_style='Subtitle2', size_hint_x=0.75)
        label1.color = Colors.bg_color
        first_box.add_widget(label1)
        first_box.add_widget(MDBoxLayout(size_hint_x=0.03))
        self.content_custom_sheet.add_widget(first_box)

        first_box = MDBoxLayout(size_hint_y=0.04)
        self.content_custom_sheet.add_widget(first_box)


        first_box = MDBoxLayout(orientation='horizontal', size_hint_y=0.35)
        first_box.add_widget(MDBoxLayout(size_hint_x=0.03))
        scrollview = ScrollView()
        gridlayout = MDGridLayout(size_hint_x=None, rows=1, spacing='2dp')
        
        char = 0
        for cat in (data.categories):
            CHIP = MDChip(text=cat, icon='', color=Colors.bg_color, text_color=Colors.text_color, on_release=lambda x: self.set_cat_item(x))
            gridlayout.add_widget(CHIP)
            char += len(cat)
        gridlayout.width = 10*char + 20*len(data.categories)
       
        scrollview.add_widget(gridlayout)
        first_box.add_widget(scrollview)
        self.content_custom_sheet.add_widget(first_box)

        first_box = MDBoxLayout(orientation='horizontal', size_hint_y=0.3)
        labelbox = MDBoxLayout(size_hint_x=0.03)
        label1 = MDLabel(text='or', font_style='Subtitle2')
        label1.color = Colors.bg_color
        label1.halign = 'center'
        labelbox.add_widget(label1)
        first_box.add_widget(labelbox)
        CHIP = MDChip(text='Add new category', icon='', color=Colors.bg_color, text_color=Colors.text_color, on_release=lambda x: self.set_cat_item(x))
        first_box.add_widget(CHIP)
        first_box.add_widget(MDBoxLayout(size_hint_x=0.03))
        self.content_custom_sheet.add_widget(first_box)

        self.custom_sheet.on_dismiss = lambda x='Hi': self.defocus(x)
        
    def defocus(self, instance):
        self.ids.line_category.color = Colors.button_disable_onwhite_color
        if self.ids.categoryfield.text == '':
            self.ids.caption_category.font_style = 'Subtitle1'
            self.ids.caption_category.pos_hint = {'top': 0.71, 'right': 0.21}

    def open_cat_dropdown(self):
        self.cat_dropdown.caller = self.ids.categoryfield
        self.cat_dropdown.open()
        self.ids.purposefield.focus     = False
        self.ids.amountfield.focus      = False
        #self.ids.line_category.color = Colors.bg_color
        #self.ids.caption_category.font_style = 'Caption'
        #self.ids.caption_category.pos_hint = {'top': 1.02, 'right': 0.21}
        #self.create_bottomsheet()
        #self.custom_sheet.open()
        
    def open_dialog_date(self):
        self.dialog_date.open()

    def set_acc_item(self, text_item):
        self.acc_dropdown.caller.text = text_item
        self.acc_dropdown.dismiss()
        self.acc_dropdown.caller.focus = False
        self.ids.accountfield.focus = False
        if self.ids.categoryfield.text != 'Transfer':
            self.focus_function()

    def set_cat_item(self, cat):
        if cat=='Add new category':
            self.dialog_add_category.open()
        else:
            self.categoryfield.text = cat
        self.cat_dropdown.dismiss()
        #self.custom_sheet.dismiss()
        self.focus_function()

    def execute_add_remove_category(self, instance):
        category = self.dialog_add_category.content_cls.namefield.text
        #add category
        if self.dialog_add_category.content_cls.namefield.hint_text == "Category name":
            data.categories.append(category)
            from backend.settings import ScreenSettings
            active_plots = 0
            for cat in ScreenSettings.settings['CategoriesScreen']['SelectedGraphs']:
                if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][cat]=='down':
                    active_plots += 1
            ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][category]='down' if active_plots < 3 else 'normal'
            ScreenSettings.save(self.app.demo_mode)
            self.dialog_add_category.content_cls.namefield.text = ''
            self.cat_dropdown.caller.text = category
        #remove category
        else:
            for i, cat in enumerate(data.categories):
                if cat==category:
                    data.categories.pop(i)
                    break
        self.dialog_add_category.dismiss()
        self.dialog_add_category.content_cls.reset_dialog_after_dismiss()    
        self.app.global_update()    

    def purposefield_function(self):
        if self.ids.purposefield.hint_text == "Purpose":
            self.focus_function()
        else:
            self.acc_dropdown.caller = self.ids.purposefield
            self.acc_dropdown.open()
            self.ids.amountfield.focus      = False
            self.ids.accountfield.focus     = False


        
    def income_button_clicked(self):
        self.ids.accountfield.hint_text = "Account"
        self.ids.purposefield.hint_text = "Purpose"
        self.ids.purposefield.icon_right = ""
        self.ids.purposefield.keyboard_mode = 'auto'
        self.ids.categoryfield.disabled = False
        self.ids.categoryfield.icon_right = "arrow-down-drop-circle-outline"
        #if switched from expenditure to income button
        if not self.ids.dialog_expenditure_button_icon.color[0]==Colors.error_color[0]:
            self.ids.categoryfield.text = ''
            self.ids.purposefield.text = ""

        if self.ids.dialog_income_button_icon.color[1] == 0:
            self.ids.dialog_income_button_icon.color = Colors.green_color
            self.ids.dialog_income_button_text.color = Colors.green_color
            self.ids.dialog_expenditure_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_text.color = Colors.button_disable_onwhite_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass
    def expenditure_button_clicked(self):
        self.ids.accountfield.hint_text = "Account"
        self.ids.purposefield.hint_text = "Purpose"
        self.ids.purposefield.icon_right = ""
        self.ids.purposefield.keyboard_mode = 'auto'
        self.ids.categoryfield.disabled = False
        self.ids.categoryfield.icon_right = "arrow-down-drop-circle-outline"
        #if switched from expenditure to income button
        if not self.ids.dialog_income_button_icon.color[1]==Colors.green_color[1]:
            self.ids.categoryfield.text = ''
            self.ids.purposefield.text = ""

        if self.ids.dialog_expenditure_button_icon.color[0] == 0:
            self.ids.dialog_income_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_income_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_icon.color = Colors.button_disable_onwhite_color
            self.ids.dialog_transfer_button_text.color = Colors.button_disable_onwhite_color
            self.ids.dialog_expenditure_button_text.color = Colors.error_color
            self.ids.dialog_expenditure_button_icon.color = Colors.error_color
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass      

    def transfer_button_clicked(self):
        if len(data.accounts)<2:
            message = Snackbar(text='Two accounts needed for internal transfer.', snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(self.app.Window.width - (dp(10) * 2)) / self.app.Window.width)
            message.bg_color=Colors.black_color
            message.text_color=Colors.text_color
            message.open()
        else:
            self.ids.amountfield.text = ''
            self.ids.accountfield.hint_text = "Account (from)"
            self.ids.purposefield.text = ""
            self.ids.purposefield.hint_text = "Account (to)"
            self.ids.purposefield.icon_right = "arrow-down-drop-circle-outline"
            self.ids.purposefield.keyboard_mode = 'managed'
            self.ids.categoryfield.text = 'Transfer'
            self.ids.categoryfield.icon_right = ""
            self.ids.categoryfield.disabled = True

            if self.ids.dialog_transfer_button_icon.color[0] == 0:
                self.ids.dialog_transfer_button_icon.color = Colors.primary_color
                self.ids.dialog_transfer_button_text.color = Colors.primary_color
                self.ids.dialog_expenditure_button_text.color = Colors.button_disable_onwhite_color
                self.ids.dialog_expenditure_button_icon.color = Colors.button_disable_onwhite_color
                self.ids.dialog_income_button_icon.color = Colors.button_disable_onwhite_color
                self.ids.dialog_income_button_text.color = Colors.button_disable_onwhite_color
                try:
                    amount = float(self.ids.amountfield.text)
                    if amount>0:
                        self.ids.amountfield.text = str(-amount)
                except:
                    pass     

    def focus_function(self):
        self.ids.accountfield.focus = False
        self.ids.categoryfield.focus = False
        if self.ids.dialog_income_button_icon.color[1] == 0:
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass
        else:
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass

     