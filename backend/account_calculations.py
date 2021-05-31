from datetime import datetime
from dateutil.relativedelta import relativedelta

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

    def make_dates(from, to, day):
        day = '0' + str(day) if int(day)<10 else str(day)
        from = from.split('\n')[0]
        if to=='-':
            end_month = '0'+str(self.today_date.month) if int(self.today_date.month)<10 else str(self.today_date.month)
        else:
            to = to.split('\n')[0]
        for i, month in enumerate(self.months):
            if month in from:
                start_month = str(i+1) if i+1>9 else '0'+str(i+1) 
            if month in to:
                end_month   = str(i+1) if i+1>9 else '0'+str(i+1)

        start_date = datetime.strptime('{}-{}-{}'.format(from[1], start_month, day), '%Y-%m-%d').date() 
        end_date   = datetime.strptime('{}-{}-{}'.format(to[1], end_month, day), day), '%Y-%m-%d').date()
        date_range = [start_date]
        it_date    = start_date + relativedelta(months=1)
        while it_date<=end_date:
            date_range.append(it_date)
        return date_range

    def add_standingorder_to_transfers(self, date_range, acc):
        for date in date_range:
            date = date.strftime('%Y-%m-%d')
            if not date in self.accounts[acc]['Transfers'].keys():
                self.accounts[acc]['Transfers'][date] = [[order['Amount'], order['Purpose']]
            else:
                check = False
                for transfer in self.accounts[acc]['Transfers'][date]:
                    if transfer[0]==order['Amount'] and transfer[1]==order['Purpose']:
                        check = True
                if check==False:
                    self.accounts[acc]['Transfers'][date].append([order['Amount'], order['Purpose'])

    def check_standingorders_in_transfer(self, acc):
        orders = []
        for i in range(len(self.standingorders)):
            order = self.standingorders[i]
            if acc in order['Account']:
                #parse standing order entry in date
                date_range = self.make_dates(order['From'], order['To'], order['Day'])

                #populate standingorder into transfers of account
                self.add_standingorder_to_transfer(date_range, acc)


                






        
                


    def calculate_end_month_status(self, acc):
        pass

    def calculate_month_summary(self, acc, month):
        pass

    

        