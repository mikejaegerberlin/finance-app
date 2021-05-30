import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime

class AccountPlot():
    def __init__(self):  
        #basic things
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.fig     = plt.figure(figsize=(1,1), dpi=100)    

    def make_plot(self, filter_buttons):
        plt.close(self.fig)
        self.fig     = plt.figure(figsize=(1,1), dpi=100)
        self.ax      = self.fig.add_subplot(111)
        start_date   = self.today_date
        self.filters = [relativedelta(months=1), relativedelta(months=3), relativedelta(months=6),
                        relativedelta(years=1), relativedelta(years=3)]
        for i, button in enumerate(filter_buttons):
            if button.md_bg_color[0]==1:
                self.filter_index = i
                filter = self.filters[i]
        end_date     = start_date - filter
        amounts = {}
        dates   = {}
        for acc in self.accounts:
            amounts[acc] = []
            dates[acc]   = []
            possible_dates = list(self.accounts[acc]['Status'].keys())
            possible_dates.sort(reverse=True)
            for date in possible_dates:
                if datetime.strptime(date, '%Y-%m-%d').date()>start_date:
                    pass
                else:
                    amounts[acc].append(self.accounts[acc]['Status'][date])
                    dates[acc].append(datetime.strptime(date, '%Y-%m-%d').date())
                if datetime.strptime(date, '%Y-%m-%d').date()<end_date:
                    break
        colors = ['r', 'b', 'g']
        for i, acc in enumerate(self.accounts):
            self.ax.plot(dates[acc], amounts[acc], colors[i], linewidth=self.settings['Linewidth'], markersize=self.settings['Markersize'])
            xticks, xticklabels = self.get_xticks_and_labels(start_date, end_date, filter)
            self.ax.set_xticks(xticks)
            self.ax.set_xticklabels(xticklabels)
        self.ax.patch.set_facecolor(self.bg_color_light_hex)
        self.fig.patch.set_facecolor(self.bg_color_hex)
        self.ax.grid(linestyle=':', linewidth=0.05)
        self.ax.spines['left'].set_color(self.text_color_hex)
        self.ax.spines['right'].set_color(self.text_color_hex)
        self.ax.spines['top'].set_color(self.text_color_hex)
        self.ax.spines['bottom'].set_color(self.text_color_hex)
        self.ax.tick_params(axis='y', colors=self.text_color_hex, labelsize=self.settings['Labelsize'])
        self.ax.tick_params(axis='x', colors=self.text_color_hex, labelsize=self.settings['Labelsize'])
        self.ax.axis([end_date, start_date,-1000,1000])
        canvas = self.fig.canvas  
        self.save_jsons()
        return canvas        
        
    def get_xticks_and_labels(self, start_date, end_date, filter):
        steps = [relativedelta(days=7), relativedelta(days=14), relativedelta(days=28), relativedelta(months=3), relativedelta(months=6)]
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

    