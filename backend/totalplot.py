import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime
from backend.settings import Sizes
from backend.colors import Colors

class TotalPlot():
    def __init__(self):  
        #basic things
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.fig     = plt.figure(figsize=(1,1), dpi=100)    

    def make_plot(self, filter_buttons, data, set_xticks):
        plt.close(self.fig)
        self.fig     = plt.figure(figsize=(1,1), dpi=100)
        self.ax      = self.fig.add_subplot(111)
        start_year   = str(self.today_date.year)
        start_month  = str(self.today_date.month)
        days = ['31', '30', '29', '28']
        for day in days:
            try:
                start_date   = datetime.strptime('{}-{}-{}'.format(start_year, start_month, day), '%Y-%m-%d').date() 
                break
            except:
                pass
        self.filters = [relativedelta(years=1), relativedelta(years=3), relativedelta(years=5), relativedelta(years=10), relativedelta(years=13)]
        self.filters_help = [365, 1095, 1825, 3650, 4745]
        for i, button in enumerate(filter_buttons):
            if button.md_bg_color[0]==1:
                self.filter_index = i
        
        if self.filter_index==len(filter_buttons)-1:
            end_date = start_date - relativedelta(years=1000)
        else:
            end_date = start_date - self.filters[self.filter_index]
        
        adjust_plot = True
       
        amounts_daily = []
        dates_daily  = []
        possible_dates = list(data.total['Status'].keys())
        possible_dates.sort(reverse=True)
        min_date = possible_dates[-1]
        for date in possible_dates:
            if datetime.strptime(date, '%Y-%m-%d').date()>start_date:
                pass
            else:
                amounts_daily.append(data.total['Status'][date])
                dates_daily.append(datetime.strptime(date, '%Y-%m-%d').date())
            if datetime.strptime(date, '%Y-%m-%d').date()<end_date:
                adjust_plot = False
                break
        
        self.exceed_years = 0
        if adjust_plot:
            end_date = datetime.strptime(min_date, '%Y-%m-%d').date()
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
                    rest_years        = int(int(rest_days / 365) / 6)
                    self.exceed_years = 1 + rest_years
       
     
        amounts_monthly = []
        dates_monthly   = []
        
        possible_dates = list(data.total['Status'].keys())
        possible_dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
        years = [possible_dates[0][0:4]]
        for date in possible_dates:
            if date[0:4]!=years[-1]:
                years.append(date[0:4])

        status_before = 0
        for year in years:
            filter_year        = list(filter(lambda k: str(year) in k, possible_dates))
            for i in range(1,13):
                i_str = '0'+str(i) if i<10 else str(i)
                filter_month   = list(filter(lambda k: i_str in k[5:7], filter_year))
                if len(filter_month)>=1:
                    amounts_monthly.append(data.total['Status'][filter_month[-1]])
                    status_before = amounts_monthly[-1]
                else:
                    amounts_monthly.append(status_before)
                for day in days:
                    try:
                        dates_monthly.append(datetime.strptime('{}-{}-{}'.format(str(year), i_str, day), '%Y-%m-%d').date())
                        break
                    except:
                        pass

        self.profits = []
        self.profits_date = {}
        for i in range(1, len(amounts_monthly)):
            self.profits.append(amounts_monthly[i]-amounts_monthly[i-1])
            month = int((dates_monthly[i]).month)
            year  = int((dates_monthly[i]).year)
            self.profits_date[self.months[month-1]+' '+str(year)] = self.profits[-1]

        for q, date in enumerate(dates_monthly):
            if end_date<date:
                break

        colors = Colors.matplotlib_colors
        #self.ax.plot(dates_daily, amounts_daily, colors[1], linewidth=Sizes.linewidth, markersize=Sizes.markersize, label='Total')        
        xticks, xticklabels = self.get_xticks_and_labels(start_date, end_date)
        self.ax.grid(linestyle=':', linewidth=0.05)
        self.ax.spines['left'].set_color(Colors.text_color_hex)
        self.ax.spines['right'].set_color(Colors.text_color_hex)
        self.ax.spines['top'].set_color(Colors.text_color_hex)
        self.ax.spines['bottom'].set_color(Colors.text_color_hex)
        if set_xticks:
            y_axis_max = int(max(self.profits[q:])+10)
            y_axis_min = int(min(self.profits[q:])-10)
            self.ax.set_xticks(xticks)
            self.ax.set_xticklabels(xticklabels)
            for j, profit in enumerate(self.profits):
                if profit>=0:
                    self.ax.bar(dates_monthly[j], profit, color='forestgreen', width=30)
                else:
                    self.ax.bar(dates_monthly[j], profit, color='firebrick', width=30)
        else:
            y_axis_max = int(max(amounts_monthly[q:])+100)
            y_axis_min = int(min(amounts_monthly[q:])-100)
            self.ax.set_xticks(xticks)
            self.ax.set_xticklabels([])
            self.ax.plot(dates_monthly, amounts_monthly, colors[1], linewidth=Sizes.linewidth, markersize=Sizes.markersize, label='Total')
        self.ax.patch.set_facecolor(Colors.bg_color_light_hex)
        #self.fig.patch.set_facecolor(Colors.bg_color_hex)
        self.fig.patch.set_alpha(0)
        
        self.ax.tick_params(axis='y', colors=Colors.text_color_hex, labelsize=Sizes.labelsize)
        self.ax.tick_params(axis='x', colors=Colors.text_color_hex, labelsize=Sizes.labelsize)
        start_date  = '{}-{}-{}'.format(str(start_date.year), str((start_date+relativedelta(months=1)).month), '01')
        start_date  = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.ax.axis([end_date, start_date,y_axis_min,y_axis_max])
        #self.ax.legend(loc='best', ncol=4, fontsize='medium', facecolor=Colors.bg_color_light_hex, edgecolor=Colors.bg_color_hex, bbox_to_anchor=(0.8, -0.06))
        #print (dir(self.ax.legend))
        canvas = self.fig.canvas  
        
        return canvas        
        
    def get_xticks_and_labels(self, start_date, end_date):
        steps = [relativedelta(months=1), relativedelta(months=3), relativedelta(months=6), relativedelta(years=1), relativedelta(years=1)+relativedelta(years=self.exceed_years)]
        step  = steps[self.filter_index]
        
        start_date  = '{}-{}-{}'.format(str(start_date.year), str((start_date+relativedelta(months=1)).month), '01')
        start_date  = datetime.strptime(start_date, '%Y-%m-%d').date()
        xticklabels = [self.months[int(start_date.strftime('%Y-%m-%d')[5:7])-1]+"\n'"+start_date.strftime('%Y-%m-%d')[2:4]]
        xticks = [start_date]
        next_date = start_date - step
        while next_date>=end_date:
            xticks.append(next_date)
            if self.filter_index<0:
                xticklabels.append(str(int(next_date.strftime('%Y-%m-%d')[8:]))+' '+self.months[int(next_date.strftime('%Y-%m-%d')[5:7])-1])
            else:
                xticklabels.append(self.months[int(next_date.strftime('%Y-%m-%d')[5:7])-1]+"\n'"+next_date.strftime('%Y-%m-%d')[2:4])
            next_date = next_date - step
        return xticks, xticklabels

TotalPlot = TotalPlot()