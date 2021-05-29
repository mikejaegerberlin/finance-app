import matplotlib.pyplot as plt
import matplotlib
import json
import random
from dateutil.relativedelta import relativedelta
from datetime import datetime
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class Backend():
    def __init__(self):  
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.get_colors()
        self.create_demo_setup()
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.cards_transferitem = []
        self.cards_monthitem    = []
        
                 
        '''settings = {}
        settings['Labelsize'] = 20
        settings['Titlesize'] = 20
        settings['Linewidth'] = 5
        settings['Markersize'] = 2

        with open('settings.json', 'w') as qt:
            json.dump(settings, qt)'''    

        with open('accounts.json', 'r') as qt:
            self.accounts = json.load(qt)

        with open('settings.json', 'r') as lp:
            self.settings = json.load(lp)

        self.fig     = plt.figure(figsize=(1,1), dpi=100)    
              
    def get_colors(self):
        self.bg_color                     = (0.1, 0.1, 0.1, 1)
        self.bg_color_light               = (100/255, 94/255, 99/255,  0.15)
        self.text_color                   = (255/255, 253/255, 250/255, 1)
        self.primary_color                = (0, 7/255, 143/255, 0.8)
        self.error_color                  = (1, 0, 0, 0.7)
        self.black_color                  = (0, 0, 0, 1)
        self.green_color                  = (0, 180/255, 0, 1)
        self.button_disable_onwhite_color = (0, 0, 0, 0.3)

        self.text_color_hex     = str(matplotlib.colors.to_hex([self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3]], keep_alpha=True))
        self.bg_color_hex       = str(matplotlib.colors.to_hex([self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3]], keep_alpha=True))
        self.bg_color_light_hex = str(matplotlib.colors.to_hex([self.bg_color_light[0], self.bg_color_light[1], self.bg_color_light[2], self.bg_color_light[3]], keep_alpha=True))
        
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

    def generate_carditems(self, number):
        
        if number>1 and len(self.cards_transferitem)>60:
            pass
        else:
            for i in range(number):
                sublist = []
                card = MDCard(size_hint_y=None, height='36dp', md_bg_color=self.bg_color, ripple_behavior=True, ripple_color=self.bg_color_light)
                contentbox          = MDBoxLayout(orientation='horizontal', md_bg_color=self.bg_color, radius=[10,10,10,10]) 
                datelabel           = MDLabel(text='', font_style='Subtitle2')
                datelabel.color     = self.text_color
                datelabel.halign    = 'center'
                contentbox.add_widget(datelabel)   
                purposelabel        = MDLabel(text='', font_style='Subtitle2')
                purposelabel.color  = self.text_color
                purposelabel.halign = 'center'
                contentbox.add_widget(purposelabel)
                amountlabel         = MDLabel(text='', font_style='Subtitle2')
                amountlabel.color   = self.text_color
                amountlabel.halign  = 'center'
                contentbox.add_widget(amountlabel) 
                card.add_widget(contentbox)
                sublist = [card, contentbox, datelabel, purposelabel, amountlabel]
                self.cards_transferitem.append(sublist)
            
        #for i in range(48):
        #    self.cards_monthitem.append(MDCard(size_hint_y=None, height='36dp', md_bg_color=self.bg_color, 
        #                                       ripple_behavior=True, ripple_color=self.bg_color))
        
    def save_jsons(self):
        
        with open('settings.json', 'w') as outfile:
            json.dump(self.settings, outfile)

        with open('accounts.json', 'w') as outfile:
            json.dump(self.accounts, outfile)

    def create_demo_setup(self):
        #structure:
        #accounts[account]['Transfers'][date]
        #accounts[account]['Status'][date]

        #accounts[account]['Income'][year]
        #accounts[account]['Expenditure'][year]
        #accounts[account]['Profit'][year]

        #accounts[account]['Income'][year][month]
        #accounts[account]['Expenditure'][year][month]
        #accounts[account]['Profit'][year][month]

        self.accounts = {}
        accounts_list = ['DKB', 'ING', 'Cash']
        keys_list     = ['Transfers', 'Status', 'Income', 'Expenditure', 'Profit']
        Purposes      = ['Eat & Drink', 'Culture', 'Miete', 'Anschaffung', 'Musik', 
                         'Schuhe', 'Möbel', 'Restaurant', 'Eis', 'Cocktail', 'Flug', 
                        'Ticket', 'Gitarre', 'Bier']
        years         = [2019, 2020, 2021]

        #initialize dictionaries
        for acc in accounts_list:
            self.accounts[acc] = {}
            for key in keys_list:
                self.accounts[acc][key] = {}
        
        #fill transfers
        for acc in accounts_list:
            for q in range(200):
                year      = random.randint(years[0],years[-1])
                month     = random.randint(1,12)
                day       = random.randint(1,28)
                amount    = round(float(random.randint(-100,100)) + round(random.random(),2),2)
                purpose   = Purposes[random.randint(0,13)]

                month_str = '0'+str(month) if month<10 else str(month)
                day_str   = '0'+str(day) if day<10 else str(day)
                date      = '{}-{}-{}'.format(year, month_str, day_str)

                if not datetime.strptime(date, '%Y-%m-%d').date()>self.today_date:
                    if date in self.accounts[acc]['Transfers'].keys():
                        self.accounts[acc]['Transfers'][date].append([amount, purpose])
                    else:
                        self.accounts[acc]['Transfers'][date] = [[amount, purpose]]
        
            dates = list(self.accounts[acc]['Transfers'].keys())
            
            #fill income, expenditure, profit
            for year in years:
                self.accounts[acc]['Income'][year]      = {}
                self.accounts[acc]['Expenditure'][year] = {}
                self.accounts[acc]['Profit'][year]      = {}

                filter_year        = list(filter(lambda k: str(year) in k, dates))
                year_income        = 0
                year_expenditure   = 0
                for i in range(1,13):
                    month_income      = 0
                    month_expenditure = 0
                    i_str = '0'+str(i) if i<10 else str(i)
                    filter_month   = list(filter(lambda k: i_str in k[5:7], filter_year))
                    for date in filter_month:
                        for transfer in self.accounts[acc]['Transfers'][date]:
                            if transfer[0]>=0:
                                month_income      += transfer[0]
                            else:
                                month_expenditure += transfer[0]
        
                    self.accounts[acc]['Income'][year][i]      = month_income
                    self.accounts[acc]['Expenditure'][year][i] = month_expenditure
                    self.accounts[acc]['Profit'][year][i]      = month_income + month_expenditure
                    year_income      += month_income
                    year_expenditure += month_expenditure
                
                self.accounts[acc]['Income'][year]['Total']      = year_income
                self.accounts[acc]['Expenditure'][year]['Total'] = year_expenditure
                self.accounts[acc]['Profit'][year]['Total']      = year_income + year_expenditure

            #fill status
            self.fill_status_of_account(acc)

        with open('accounts.json', 'w') as qt:
            json.dump(self.accounts, qt)

    def fill_status_of_account(self, acc):
        
        self.accounts[acc]['Status'] = {}
        dates = list(self.accounts[acc]['Transfers'].keys())
        dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
        
        for i, date in enumerate(dates):
            for transfer in self.accounts[acc]['Transfers'][date]:
                if len(self.accounts[acc]['Status'].keys())==0:
                    self.accounts[acc]['Status'][date] = round(transfer[0], 2)
                elif not date in self.accounts[acc]['Status'].keys():
                    previous_date = dates[i-1]
                    self.accounts[acc]['Status'][date] = round(self.accounts[acc]['Status'][previous_date] + transfer[0], 2)
                else:
                    self.accounts[acc]['Status'][date] = round(self.accounts[acc]['Status'][date] + transfer[0], 2)
                    
        if not self.today_str in self.accounts[acc]['Status'].keys():
            self.accounts[acc]['Status'][self.today_str] = round(self.accounts[acc]['Status'][dates[-1]], 2)

      
 
        