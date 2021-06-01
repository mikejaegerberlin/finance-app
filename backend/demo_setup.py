import random
from datetime import datetime
from backend.account_calculations import Calculations
import json

class DemoData(Calculations):
    def __init__(self): 
        self.current_account = ''
        self.today_str       = datetime.today().strftime('%Y-%m-%d')
        self.today_date      = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.current_month   = int(self.today_date.month)
        self.current_year    = int(self.today_date.year)
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.accounts        = {}
        self.standingorders  = {}

        #self.create_new_setup() 
        #self.save_accounts()
        #self.save_standingorders()
        self.load_setup()

    def load_setup(self):
        with open('accounts.json', 'r') as infile:
            self.accounts = json.load(infile)

        with open('standingorders.json', 'r') as infile:
            self.standingorders = json.load(infile)
    
    def create_new_setup(self):
        #structure:
        #accounts[account]['Transfers'][date]
        #accounts[account]['Status'][date]

        #accounts[account]['Income'][year]
        #accounts[account]['Expenditure'][year]
        #accounts[account]['Profit'][year]

        #accounts[account]['Income'][year][month]
        #accounts[account]['Expenditure'][year][month]
        #accounts[account]['Profit'][year][month]
        
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

        
        keys = ['Account', 'From', 'To', 'Day', 'Purpose', 'Amount', 'MonthListed']
        for i in range(10):
            self.standingorders[i] = {}
            self.standingorders[i][keys[0]] = accounts_list[random.randint(0,2)]
            self.standingorders[i][keys[1]] = self.months[random.randint(0,11)] + '\n' + '2021'
            self.standingorders[i][keys[2]] = self.months[random.randint(0,11)] + '\n' + str(random.randint(2022,2025))
            day       = random.randint(1,28)
            amount    = round(float(random.randint(-2000,100)) + round(random.random(),2),2)
            purpose   = Purposes[random.randint(0,13)] 
            self.standingorders[i][keys[3]] = str(day)+'.'
            self.standingorders[i][keys[4]] = purpose
            self.standingorders[i][keys[5]] = amount
            self.standingorders[i][keys[6]] = False

        for acc in self.accounts:
            self.check_standingorders_in_transfer(acc)
            self.fill_status_of_account(acc)

    def save_accounts(self):
        with open('accounts.json', 'w') as outfile:
            json.dump(self.accounts, outfile)

    def save_standingorders(self):
        with open('standingorders.json', 'w') as outfile:
            json.dump(self.standingorders, outfile)

DemoData = DemoData()
