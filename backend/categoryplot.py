import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime
from backend.settings import Sizes
from backend.colors import Colors
from copy import deepcopy
from backend.settings import ScreenSettings

class CategoryPlot():
    def __init__(self):  
        #basic things
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.fig     = plt.figure(figsize=(1,1), dpi=100)   

    def get_list_for_category(self, data, key):
        transfer_list = []
        date_list = []
        for acc in data.accounts:
            for date in data.accounts[acc]['Transfers']:
                for entry in data.accounts[acc]['Transfers'][date]:
                    if entry[2]==key:
                        appendix = entry
                        appendix.append(date)
                        date_list.append(date)
                        transfer_list.append(appendix)
        
        return transfer_list, date_list


        #self.accounts[acc]['Transfers'][date] = [[amount, purpose, category]] 

    def make_plot(self, filter_buttons, data):
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
        try:
            min_date = possible_dates[-1]
        except:
            min_date = data.today_str
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
       
        
        category_x_axis = {}
        category_y_axis = {}
      
        for key in data.categories:
            
            transfer_list, date_list = self.get_list_for_category(data, key)
            amounts_monthly = []
            dates_monthly   = []
            
            sorted_date_list = deepcopy(date_list)
            sorted_date_list.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
            
            try:
                years = [sorted_date_list[0][0:4]]
                for date in sorted_date_list:
                    if date[0:4]!=years[-1]:
                        years.append(date[0:4])
            except:
                years = []
            for year in years:
                for i in range(1,13):
                    if (int(year)<self.today_date.year) or (int(year)==self.today_date.year and i<=self.today_date.month):
                        i_str = '0'+str(i) if i<10 else str(i)
                        amounts_cumulative = 0
                        for transfer in transfer_list:
                            if transfer[3][0:4]==year and transfer[3][5:7]==i_str:
                                amounts_cumulative += float(transfer[0])
                        amounts_monthly.append(amounts_cumulative)
                        needed_year = (datetime.strptime('{}-{}-{}'.format(str(year), i_str, '01'), '%Y-%m-%d').date() - relativedelta(months=1)).year
                        needed_month = (datetime.strptime('{}-{}-{}'.format(str(year), i_str, '01'), '%Y-%m-%d').date() - relativedelta(months=1)).month
                        needed_month = '0'+str(needed_month) if needed_month<10 else str(needed_month)
                        for day in days:
                            try:
                                dates_monthly.append(datetime.strptime('{}-{}-{}'.format(str(needed_year), needed_month, day), '%Y-%m-%d').date())
                                break
                            except:
                                pass
            category_x_axis[key] = dates_monthly
            category_y_axis[key] = amounts_monthly
            

        for q, date in enumerate(dates_monthly):
            if end_date<date:
                break

        colors = Colors.piechart_colors_hex
        xticks, xticklabels = self.get_xticks_and_labels(start_date, end_date)
        self.ax.grid(axis='y', linestyle=':', linewidth=0.05)
        self.ax.grid(axis='x', linestyle=':', linewidth=0.05, alpha=0.3)
        self.ax.spines['left'].set_color(Colors.text_color_hex)
        self.ax.spines['right'].set_color(Colors.text_color_hex)
        self.ax.spines['top'].set_color(Colors.text_color_hex)
        self.ax.spines['bottom'].set_color(Colors.text_color_hex)
     
        xticks = xticks
        xticklabels = xticklabels
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticklabels)
        max_amounts = []
        min_amounts = []
        for key in category_y_axis:
            try:
                if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][key] == 'down':
                    max_amounts.append(max(category_y_axis[key][q:]))
                    min_amounts.append(min(category_y_axis[key][q:]))
            except:
                pass
        try:
            y_axis_max = int(max(max_amounts)+100)
            y_axis_min = int(min(min_amounts)-100)
        except:
            y_axis_max = 10
            y_axis_min = -10
        offset = [[],[],[],[],[]]
        for k in range(len(category_x_axis[key])):
            for i in range(5):
                offset[i].append(0)
        graph_no = 0
        for h, key in enumerate(category_x_axis):
            if ScreenSettings.settings['CategoriesScreen']['SelectedGraphs'][key] == 'down':
                #self.ax.plot(category_x_axis[key], category_y_axis[key], colors[h], linestyle='-', linewidth=Sizes.linewidth, marker='o', markersize=Sizes.markersize)
                for k, value in enumerate(category_y_axis[key]):
                    if graph_no==0:
                        self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=offset[graph_no][k])
                        offset[graph_no+1][k] += value

                    elif graph_no==1:
                        if (offset[graph_no][k]<0 and value<0) or (offset[graph_no][k]>0 and value>0):
                            self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=offset[graph_no][k])
                            offset[graph_no+1][k] += offset[graph_no][k] + value
                        if (offset[graph_no][k]<0 and value>0) or (offset[graph_no][k]>0 and value<0):
                            self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=0)
                            offset[graph_no+1][k] += value

                    elif graph_no==2:
                        if value>0:
                            max_offset = max([offset[1][k], offset[2][k]])
                            if max_offset<0:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=0)
                                offset[graph_no+1][k] += value
                            else:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=max_offset)
                                offset[graph_no+1][k] += max_offset + value
                        if value<0:
                            min_offset = min([offset[1][k], offset[2][k]])
                            if min_offset>0:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=0)
                                offset[graph_no+1][k] += value
                            else:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=min_offset)
                                offset[graph_no+1][k] += min_offset + value

                    elif graph_no==3:
                        if value>0:
                            max_offset = max([offset[1][k], offset[2][k], offset[3][k]])
                            if max_offset<0:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=0)
                                offset[graph_no+1][k] += value
                            else:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=max_offset)
                                offset[graph_no+1][k] += max_offset + value
                        if value<0:
                            min_offset = min([offset[1][k], offset[2][k], offset[3][k]])
                            if min_offset>0:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=0)
                                offset[graph_no+1][k] += value
                            else:
                                self.ax.bar(category_x_axis[key][k], value, width=30, color=colors[h], bottom=min_offset)
                                offset[graph_no+1][k] += min_offset + value
                         
                graph_no += 1

        #get y_min y_max
        for q, date in enumerate(category_x_axis[key]):
            if date>=end_date:
                break
        offsets_min, offsets_max = [], []
        for i in range(5):
            offsets_min.append(min(offset[i][q:]))
            offsets_max.append(max(offset[i][q:]))
        y_axis_min = min(offsets_min)-100
        y_axis_max = max(offsets_max)+100

        self.for_legend = category_y_axis
        self.ax.patch.set_facecolor(Colors.bg_color_light_hex)
        #self.fig.patch.set_facecolor(Colors.bg_color_hex)
        self.fig.patch.set_alpha(0)
        
        self.ax.tick_params(axis='y', colors=Colors.text_color_hex, labelsize=Sizes.labelsize)
        self.ax.tick_params(axis='x', colors=Colors.text_color_hex, labelsize=Sizes.labelsize)
        start_date  = '{}-{}-{}'.format(str(start_date.year), str((start_date+relativedelta(months=1)).month), '01')
        start_date  = datetime.strptime(start_date, '%Y-%m-%d').date()
        try:
            self.ax.axis([end_date, dates_monthly[-1],y_axis_min,y_axis_max])
        except:
            pass
        
        canvas = self.fig.canvas  
        
        return canvas        
        
    def get_xticks_and_labels(self, start_date, end_date):
        steps = [relativedelta(months=1), relativedelta(months=3), relativedelta(months=6), relativedelta(years=1), relativedelta(years=1)+relativedelta(years=self.exceed_years)]
        step  = steps[self.filter_index]
        
        #start_date  = '{}-{}-{}'.format(str(start_date.year), str((start_date+relativedelta(months=1)).month), '01')
        start_date  = '{}-{}-{}'.format(str(start_date.year), str((start_date).month), '01')
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

CategoryPlot = CategoryPlot()