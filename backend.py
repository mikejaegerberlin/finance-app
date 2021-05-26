import matplotlib.pyplot as plt
import matplotlib
import json
import random
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Backend():
    def __init__(self):  
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        accounts = {}
        accounts_list = ['DKB', 'ING', 'Cash']
        years         = [2018, 2019, 2020, 2021]
        for acc in accounts_list:
            accounts[acc] = {}
            accounts[acc]['Status']  = {}
            sum_total_income = 0
            sum_total_expenditure = 0
            for year in years:
                accounts[acc][year] = {}
                accounts[acc][year]['Income']      = 0
                accounts[acc][year]['Expenditure'] = 0
                accounts[acc][year]['Profit']      = 0 
                sum_year_income      = 0
                sum_year_expenditure = 0
                for i in range(1,13):
                    accounts[acc][year][i] = {}
                    accounts[acc][year][i]['Income']      = round(float(random.randint(0,1000)) + round(random.random(),2),2)
                    accounts[acc][year][i]['Expenditure'] = round(float(random.randint(-1000,0)) + round(random.random(),2),2)
                    accounts[acc][year][i]['Profit']      = accounts[acc][year][i]['Income'] + accounts[acc][year][i]['Expenditure']
                    accounts[acc][year][i]['Transfers']   = {}
                    sum_year_income      += accounts[acc][year][i]['Income']
                    sum_year_expenditure += accounts[acc][year][i]['Expenditure']

                accounts[acc][year]['Income']      = sum_year_income
                accounts[acc][year]['Expenditure'] = sum_year_expenditure
                accounts[acc][year]['Profit']      = sum_year_income + sum_year_expenditure
                sum_total_income      += sum_year_income
                sum_total_expenditure += sum_year_expenditure

        Purposes = ['Eat & Drink', 'Culture', 'Miete', 'Anschaffung', 'Musik', 'Schuhe', 'Möbel', 'Restaurant', 'Eis', 'Cocktail', 'Flug', 'Ticket', 'Gitarre', 'Bier']
        for acc in accounts_list:
            for q in range(400):
                year   = random.randint(2018,2021)
                month  = random.randint(1,12)
                day    = random.randint(1,28)
                amount = round(float(random.randint(-100,100)) + round(random.random(),2),2)
                purpose= Purposes[random.randint(0,13)]

                month_str = '0'+str(month) if month<10 else str(month)
                day_str = '0'+str(day) if day<10 else str(day)
                date = '{}-{}-{}'.format(year, month_str, day_str)

                if not datetime.strptime(date, '%Y-%m-%d').date()>self.today_date:
                    if date in accounts[acc][year][month]['Transfers'].keys():
                        accounts[acc][year][month]['Transfers'][date].append([amount, purpose])
                    else:
                        accounts[acc][year][month]['Transfers'][date] = []
                        accounts[acc][year][month]['Transfers'][date].append([amount, purpose]) 

            accounts[acc]['Status']['2018-01-01'] = 0
            for year in years:
                for i in range(1,13):
                    dates = list(accounts[acc][year][i]['Transfers'].keys())
                    dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
                    for date in dates:
                        for transfer in accounts[acc][year][i]['Transfers'][date]:
                            last_date = list(accounts[acc]['Status'])[-1]
                            if last_date!=date:
                                accounts[acc]['Status'][date] = round(accounts[acc]['Status'][last_date] + transfer[0],2)
                            else:
                                accounts[acc]['Status'][date] = round(accounts[acc]['Status'][date] + transfer[0],2)
              
            if not self.today_str in accounts[acc]['Status'].keys():
                accounts[acc]['Status'][self.today_str] = accounts[acc]['Status'][date]

        with open('accounts.json', 'w') as qt:
            json.dump(accounts, qt)
         
        '''settings = {}
        settings['Labelsize'] = 20
        settings['Titlesize'] = 20
        settings['Linewidth'] = 5
        settings['Markersize'] = 2

        with open('settings.json', 'w') as qt:
            json.dump(settings, qt)'''
        
        self.months  = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.clicks  = 0
        self.get_colors()

        with open('accounts.json', 'r') as qt:
            self.accounts = json.load(qt)

        with open('data.json', 'r') as fp:
            self.data = json.load(fp)

        with open('settings.json', 'r') as lp:
            self.settings = json.load(lp)
        self.fig     = plt.figure(figsize=(1,1), dpi=100)      

    def get_colors(self):
        self.bg_color                     = (0.1, 0.1, 0.1, 1)
        self.bg_color_light               = (90/255, 94/255, 99/255,  0.15)
        self.text_color                   = (255/255, 253/255, 250/255, 1)
        self.primary_color                = (0, 7/255, 143/255, 0.8)
        self.error_color                  = (1, 0, 0, 0.7)
        self.black_color                  = (0, 0, 0, 1)
        self.green_color                  = (0, 180/255, 0, 1)
        self.button_disable_onwhite_color = (0, 0, 0, 0.3)

        self.text_color_hex     = str(matplotlib.colors.to_hex([self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3]], keep_alpha=True))
        self.bg_color_hex       = str(matplotlib.colors.to_hex([self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3]], keep_alpha=True))
        self.bg_color_light_hex = str(matplotlib.colors.to_hex([self.bg_color_light[0], self.bg_color_light[1], self.bg_color_light[2], self.bg_color_light[3]], keep_alpha=True))

    def add_value(self):
        self.data['x'].append(self.months[self.clicks])
        self.data['y'].append(random.randint(-100,100))
        self.clicks += 1
        if self.clicks==12:
            self.clicks = 0
        self.save_jsons()

    def reset_data(self):
        self.data['x'] = []
        self.data['y'] = []
        self.save_jsons()

    def get_xticks_and_labels(self, start_date, end_date, filter):
        
        steps = [relativedelta(days=7), relativedelta(days=14), relativedelta(days=28), relativedelta(months=3),
                 relativedelta(months=6)]
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

    def get_year_and_month_indizes(self, start_date, end_date):

        start_date_year = start_date.strftime('%Y-%m-%d').split('-')[0]
        start_date_month = start_date.strftime('%Y-%m-%d').split('-')[1]
        end_date_year = end_date.strftime('%Y-%m-%d').split('-')[0]
        end_date_month = end_date.strftime('%Y-%m-%d').split('-')[1]

        years  = [end_date_year]
        months = [str(int(end_date_month))]
        if end_date_year!=start_date_year:
            for i in range(int(start_date_year)-int(end_date_year)):
                years.append(str(int(years[-1])+1))
            iterative_date = end_date
            while iterative_date<=(start_date - relativedelta(months=1)): 
                iterative_date = iterative_date + relativedelta(months=1)
                iterative_date = start_date if iterative_date>start_date else iterative_date
                months.insert(0, str(int(iterative_date.strftime('%Y-%m-%d').split('-')[1])))
        else:
            for i in range(int(start_date_month)-int(end_date_month)):
                months.append(str(int(months[-1])+1))
            months.sort(key=int, reverse=True)
        
        years.sort(key=int, reverse=True)

        real_months = []
        if len(years)>1:
            j = 0
            for year in years:
                real_months.append([])
                for i in range(j, len(months)):
                    real_months[-1].append(months[i])
                    if months[i]=='1':
                        j = i+1
                        break
        else:
            real_months.append(months)
        months = real_months

        return years, months
        
    def save_jsons(self):

        with open('settings.json', 'w') as outfile:
            json.dump(self.settings, outfile)

        with open('accounts.json', 'w') as outfile:
            json.dump(self.accounts, outfile)

        with open('data.json', 'w') as outfile:
            json.dump(self.data, outfile)

