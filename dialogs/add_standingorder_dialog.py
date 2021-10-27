from kivymd.uix.boxlayout import MDBoxLayout
from backend.colors import Colors
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from datetime import datetime
from backend.demo_setup import DemoData as data
from kivymd.uix.picker import MDDatePicker

class AddStandingOrderDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AddStandingOrderDialogContent, self).__init__(**kwargs)
        months      = ['January', 'February', 'March', 'April', 'Mai', 'June', 'July', 'August', 'September', 'Oktober', 'November', 'December']
        todays_year = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date().year
        years       = [str(int(todays_year)+1)]  
        days        = []      
        for i in range(10):
            years.append(str(int(years[-1])-1))
        for i in range(31):
            days.append(str(i+1))

        self.month_items = [
            {
                "text": month,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=month: self.set_item(x),
            } for month in months
        ]
        self.year_items = [
            {
                "text": year,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=year: self.set_item(x),
            } for year in years
        ]
        self.day_items = [
            {
                "text": day,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=day: self.set_item(x),
            } for day in days
        ]
        mo_an_items = ['Monthly (M)', 'Annualy (A)']
        self.monthly_annual_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=item: self.set_item(x),
            } for item in mo_an_items
        ]
        
        self.dropdown = MDDropdownMenu(
            caller=MDFlatButton(),
            items=self.month_items,
            width_mult=4,
        )

    def on_kv_post(self, instance):
        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]
        self.cat_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_cat_item(x),
            } for acc in data.categories
        ]
        
        self.acc_dropdown = MDDropdownMenu(
            caller=MDFlatButton(),
            items=self.acc_menu_items,
            position="bottom",
            width_mult=4,
        )
        self.cat_dropdown = MDDropdownMenu(
            caller=MDFlatButton(),
            items=self.cat_menu_items,
            position="auto",
            width_mult=4,
        )

        self.dialog_date = MDDatePicker(primary_color=Colors.primary_color, selector_color=Colors.primary_color, 
                                        text_button_color=Colors.primary_color, text_color=Colors.bg_color, specific_text_color=Colors.bg_color,
                                        size_hint_y=None, text_weekday_color=Colors.bg_color)
        self.dialog_date.bind(on_save=self.dialog_date_ok, on_cancel=self.dialog_date_cancel)

    def update_category_account_items(self):
        self.category_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_cat_item(x),
            } for acc in data.categories
        ]
        self.cat_dropdown.items = self.category_menu_items

        self.acc_menu_items = [
            {
                "text": acc,
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=acc: self.set_acc_item(x),
            } for acc in data.accounts
        ]

        self.acc_dropdown.items = self.acc_menu_items

    def add_standing_order(self):
        no_orders = list(data.standingorders['Orders'].keys())
        if len(no_orders)>1:
            no_orders.sort(key=int)
            new_number = str(int(no_orders[-1]) + 1)
        else:
            new_number = '1' 
        data.standingorders['Orders'][new_number] = {}
        data.standingorders['Orders'][new_number]['Account']     = self.ids.accountfield.text
        data.standingorders['Orders'][new_number]['From']        = self.ids.fromfield_month.text[0:3]+'\n'+self.ids.fromfield_year.text
        data.standingorders['Orders'][new_number]['M/A']         = 'M'
        data.standingorders['Orders'][new_number]['Day']         = self.ids.dayfield.text+'.'
        data.standingorders['Orders'][new_number]['Purpose']     = self.ids.purposefield.text
        data.standingorders['Orders'][new_number]['Amount']      = float(self.ids.amountfield.text)
        data.standingorders['Orders'][new_number]['Category']    = self.ids.categoryfield.text
        data.standingorders['Orders'][new_number]['MonthListed'] = False
        self.ids.accountfield.text    = ''
        self.ids.fromfield_month.text = ''
        self.ids.fromfield_year.text  = ''
        self.ids.categoryfield.text   = ''
        self.ids.dayfield.text        = ''
        self.ids.purposefield.text    = ''
        self.ids.amountfield.text     = ''
        order = data.standingorders['Orders'][new_number]
        return order

        
       
    def open_dropdown(self, textfield):
        if 'From (year)' in textfield.hint_text:
            self.dropdown.items = self.year_items
        elif 'From (month)' in textfield.hint_text:
            self.dropdown.items = self.month_items
        elif 'Day' in textfield.hint_text:
            self.dropdown.items = self.day_items
        else:
            self.dropdown.items = self.monthly_annual_items
        self.dropdown.caller = textfield
        self.dropdown.open()  

    def set_item(self, item):
        self.dropdown.caller.text = item
        self.focus_function()
        self.dropdown.dismiss()

        
    def income_button_clicked(self):
        self.ids.accountfield.hint_text = "Account"
        self.ids.purposefield.hint_text = "Purpose"
        self.ids.purposefield.icon_right = ""
        self.ids.purposefield.keyboard_mode = 'auto'
        self.ids.categoryfield.disabled = False
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
        self.ids.amountfield.text = ''
        self.ids.accountfield.hint_text = "Account (from)"
        self.ids.purposefield.text = ""
        self.ids.purposefield.hint_text = "Account (to)"
        self.ids.purposefield.icon_right = "arrow-down-drop-circle-outline"
        self.ids.purposefield.keyboard_mode = 'managed'
        self.ids.categoryfield.text = 'Transfer'
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
        self.ids.accountfield.focus    = False
        self.ids.categoryfield.focus   = False
        self.ids.fromfield_month.focus = False
        self.ids.fromfield_year.focus  = False
        self.ids.categoryfield.focus   = False
        self.ids.executionfield.focus  = False
        if self.ids.dialog_income_button_icon.color[1] == 0:
            try:
                amount = float(self.ids.amountfield.text)
                if amount>0:
                    self.ids.amountfield.text = str(-amount) if self.ids.purposefield.hint_text == "Purpose" else str(amount)
            except:
                pass
        else:
            try:
                amount = float(self.ids.amountfield.text)
                if amount<0:
                    self.ids.amountfield.text = str(-amount)
            except:
                pass

    def purposefield_function(self):
        if self.ids.purposefield.hint_text == "Purpose":
            self.focus_function()
        else:
            self.acc_dropdown.caller = self.ids.purposefield
            self.acc_dropdown.open()
            self.ids.amountfield.focus      = False
            self.ids.accountfield.focus     = False

    def dialog_date_ok(self, instance, value, date_range):
        date = value.strftime('%Y-%m-%d')
        self.ids.datefield.text = date
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        self.ids.accountfield.focus = False
    
    def dialog_date_cancel(self, instance, value):
        self.ids.purposefield.focus = False
        self.ids.amountfield.focus = False
        self.ids.accountfield.focus = False

    def open_acc_dropdown(self, field):
        self.acc_dropdown.caller = field
        field.hide_keyboard()
        self.acc_dropdown.open()
        self.ids.purposefield.focus     = False
        self.ids.amountfield.focus      = False

    def open_cat_dropdown(self, categoryfield):
        self.cat_dropdown.caller        = self.ids.categoryfield
        categoryfield.hide_keyboard()
        self.cat_dropdown.open()
        self.ids.purposefield.focus     = False
        self.ids.amountfield.focus      = False

    def set_acc_item(self, text_item):
        self.acc_dropdown.caller.text = text_item
        self.acc_dropdown.dismiss()
        self.acc_dropdown.caller.focus = False
        self.focus_function()

    def set_cat_item(self, text_item):
        self.cat_dropdown.caller.text = text_item
        self.cat_dropdown.dismiss()
        self.cat_dropdown.caller.focus = False
        self.focus_function()