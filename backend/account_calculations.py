import matplotlib.pyplot as plt
import json
from datetime import datetime

class Calculations():
    def __init__(self):  
        #basic things
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 

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

    def save_jsons(self):
        with open('settings.json', 'w') as outfile:
            json.dump(self.settings, outfile)
        with open('accounts.json', 'w') as outfile:
            json.dump(self.accounts, outfile)

        