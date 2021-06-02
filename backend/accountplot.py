import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime
from backend.settings import Sizes
from backend.colors import Colors

class AccountPlot():
    def __init__(self):  
        #basic things
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.fig     = plt.figure(figsize=(1,1), dpi=100)    

    def make_plot(self, filter_buttons, data):
        plt.close(self.fig)
        self.fig     = plt.figure(figsize=(1,1), dpi=100)
        self.ax      = self.fig.add_subplot(111)
        start_date   = self.today_date
        self.filters = [relativedelta(months=1), relativedelta(months=3), relativedelta(months=6),
                        relativedelta(years=1), relativedelta(years=3), relativedelta(years=5), relativedelta(years=10), relativedelta(years=13)]
        self.filters_help = [30, 90, 180, 365, 1095, 1825, 3650, 4745]
        for i, button in enumerate(filter_buttons):
            if button.md_bg_color[0]==1:
                self.filter_index = i
        
        if self.filter_index==len(filter_buttons)-1:
            end_date = start_date - relativedelta(years=1000)
        else:
            end_date = start_date - self.filters[self.filter_index]
        amounts = {}
        dates   = {}
        adjust_plot = True
        min_dates = []
        for acc in data.accounts:
            amounts[acc] = []
            dates[acc]   = []
            possible_dates = list(data.accounts[acc]['Status'].keys())
            possible_dates.sort(reverse=True)
            min_dates.append(possible_dates[-1])
            for date in possible_dates:
                if datetime.strptime(date, '%Y-%m-%d').date()>start_date:
                    pass
                else:
                    amounts[acc].append(data.accounts[acc]['Status'][date])
                    dates[acc].append(datetime.strptime(date, '%Y-%m-%d').date())
                if datetime.strptime(date, '%Y-%m-%d').date()<end_date:
                    adjust_plot = False
                    break
        
        self.exceed_years = 0
        if adjust_plot:
            end_date = datetime.strptime(min(min_dates), '%Y-%m-%d').date()
            delta    = start_date - end_date
            if delta.days<=30:
                self.filter_index = 0
            else:
                exceeded = True
                for i in range(len(self.filters)-1):
                    if delta.days>self.filters_help[i] and delta.days<=self.filters_help[i+1]:
                        distance1 = delta.days - self.filters_help[i]
                        distance2 = self.filters_help[i+1] - delta.days 
                        if distance1>distance2:
                            self.filter_index = i+1
                        else:
                            self.filter_index = i
                        exceeded = False
                        if self.filter_index==len(self.filters)-1:
                            self.exceed_years = 1
                        break
                        
                if exceeded:
                    rest_days         = delta.days - self.filters_help[-1]
                    rest_years        = int(int(rest_days / 365) / 3)
                    self.exceed_years = 1 + rest_years
       
        colors = ['r', 'b', 'g']
        maxes  = []
        mines  = []
        for i, acc in enumerate(data.accounts):
            self.ax.plot(dates[acc], amounts[acc], colors[i], linewidth=Sizes.linewidth, markersize=Sizes.markersize)
            maxes.append(max(amounts[acc]))
            mines.append(min(amounts[acc]))
        xticks, xticklabels = self.get_xticks_and_labels(start_date, end_date)
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticklabels)
        y_axis_max = int(max(maxes)+100)
        y_axis_min = int(min(mines)-100)
        self.ax.patch.set_facecolor(Colors.bg_color_light_hex)
        self.fig.patch.set_facecolor(Colors.bg_color_hex)
        self.ax.grid(linestyle=':', linewidth=0.05)
        self.ax.spines['left'].set_color(Colors.text_color_hex)
        self.ax.spines['right'].set_color(Colors.text_color_hex)
        self.ax.spines['top'].set_color(Colors.text_color_hex)
        self.ax.spines['bottom'].set_color(Colors.text_color_hex)
        self.ax.tick_params(axis='y', colors=Colors.text_color_hex, labelsize=Sizes.labelsize)
        self.ax.tick_params(axis='x', colors=Colors.text_color_hex, labelsize=Sizes.labelsize)
        self.ax.axis([end_date, start_date,y_axis_min,y_axis_max])
        canvas = self.fig.canvas  
        return canvas        
        
    def get_xticks_and_labels(self, start_date, end_date):
        steps = [relativedelta(days=7), relativedelta(days=14), relativedelta(days=28), relativedelta(months=3), relativedelta(months=6), 
                 relativedelta(years=1), relativedelta(years=2), relativedelta(years=2)+relativedelta(years=self.exceed_years)]
        step  = steps[self.filter_index]
        
        if self.filter_index<3:
            xticklabels = [str(int(start_date.strftime('%Y-%m-%d')[8:]))+' '+self.months[int(start_date.strftime('%Y-%m-%d')[5:7])-1]]
        else:
            start_date  = '{}-{}-{}'.format(str(start_date.year), str(start_date.month), '01')
            start_date  = datetime.strptime(start_date, '%Y-%m-%d').date()
            xticklabels = [self.months[int(start_date.strftime('%Y-%m-%d')[5:7])-1]+' '+start_date.strftime('%Y-%m-%d')[0:4]]
        xticks = [start_date]
        next_date = start_date - step
        while next_date>=end_date:
            xticks.append(next_date)
            if self.filter_index<3:
                xticklabels.append(str(int(next_date.strftime('%Y-%m-%d')[8:]))+' '+self.months[int(next_date.strftime('%Y-%m-%d')[5:7])-1])
            else:
                xticklabels.append(self.months[int(next_date.strftime('%Y-%m-%d')[5:7])-1]+' '+next_date.strftime('%Y-%m-%d')[0:4])
            next_date = next_date - step
        return xticks, xticklabels

AccountPlot = AccountPlot()