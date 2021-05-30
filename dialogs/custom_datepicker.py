from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from datetime import datetime
from dateutil.relativedelta import relativedelta
from kivymd.uix.button import MDFillRoundFlatButton

class DatePickerContent(MDBoxLayout):
    def __init__(self, Backend, **kwargs):
        super(DatePickerContent, self).__init__(**kwargs)
        self.spacing     = "12dp"
        self.height      = "250dp"
        self.months      = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.weekdays    = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        self.today_str   = datetime.today().strftime('%Y-%m-%d')
        self.today_date  = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.size_hint_y = None
        self.orientation = 'vertical'

        #make month box
        month_box   = MDBoxLayout(orientation='horizontal')
        month_label = MDLabel(text='{} {}'.format(self.months[int(self.today_date.month)-1], self.today_date.year))
        month_label.color = Backend.black_color
        month_box.add_widget(month_label)
        self.add_widget(month_box)

        #make weekday box
        weekday_box = MDBoxLayout(orientation='horizontal')        
        for day in self.weekdays:
            label = MDLabel(text=day)
            label.color=Backend.button_disable_onwhite_color
            label.halign = 'center'
            weekday_box.add_widget(label)
        self.add_widget(weekday_box)

        #make date boxes
        start_date = datetime.strptime('{}-{}-{}'.format(self.today_date.year, self.today_date.month, '01'), '%Y-%m-%d').date() 
        end_date   = datetime.strptime('{}-{}-{}'.format(self.today_date.year, self.today_date.month, '01'), '%Y-%m-%d').date() + relativedelta(months=1)
        empty_labels_start = start_date.weekday()
        empty_labels_end   = 6 - end_date.weekday() 
        days_delta = int((end_date - start_date).days)

        #first date box
        date_box = MDBoxLayout(orientation='horizontal')
        for i in range(empty_labels_start):
            date_box.add_widget(MDLabel(text=''))
        for i in range(empty_labels_start,7):
            label = MDFillRoundFlatButton(text=str((start_date+relativedelta(days=i-empty_labels_start)).day))
            label.halign = 'center' 
            date_box.add_widget(label)
        self.add_widget(date_box)
        
        #date boxes in between
        start_day   = '0' + str(int(label.text)+1)
        start_date  = datetime.strptime('{}-{}-{}'.format(self.today_date.year, self.today_date.month, start_day), '%Y-%m-%d').date()
        weeks_delta = int(int((end_date - start_date).days) / 7)
        day         = int(start_day)

        for week in range(0,weeks_delta):
            date_box = MDBoxLayout(orientation='horizontal')
            for i in range(0,7):
                label = MDFillRoundFlatButton(text=str(day))
                label.halign = 'center' 
                date_box.add_widget(label)
                day += 1
            self.add_widget(date_box)

        #last date box
        date_box = MDBoxLayout(orientation='horizontal')
        for i in range(day-1, days_delta):
            label = MDFillRoundFlatButton(text=str(i+1))
            label.halign = 'center' 
            date_box.add_widget(label)
        for i in range(empty_labels_end+1):
            date_box.add_widget(MDLabel(text=''))
        self.add_widget(date_box)
        
        