from datetime import datetime
from dateutil.relativedelta import relativedelta

class Calculations():
    def __init__(self):  
        pass
        
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

    def make_dates(self, from_str, to, day):
        day = day.replace('.','')
        day = '0' + str(day) if int(day)<10 else str(day)
        year_begin = from_str.split('\n')[1]
        year_end   = to.split('\n')[1]
        from_str = from_str.split('\n')[0]
        if to=='-':
            end_month = '0'+str(self.today_date.month) if int(self.today_date.month)<10 else str(self.today_date.month)
        else:
            to = to.split('\n')[0]
        for i, month in enumerate(self.months):
            if month in from_str:
                start_month = str(i+1) if i+1>9 else '0'+str(i+1) 
            if month in to:
                end_month   = str(i+1) if i+1>9 else '0'+str(i+1)

        start_date = datetime.strptime('{}-{}-{}'.format(year_begin, start_month, day), '%Y-%m-%d').date() 
        end_date   = datetime.strptime('{}-{}-{}'.format(year_end, end_month, day), '%Y-%m-%d').date()
        date_range = [start_date]
        it_date    = start_date + relativedelta(months=1)
        while it_date<=end_date:
            date_range.append(it_date)
            it_date = it_date + relativedelta(months=1)
        return date_range

    def check_if_current_month_listed(self, date, order):
        if date.month==self.today_date.month and date.year==self.today_date.year:
            order['MonthListed'] = True

    def add_standingorder_to_transfers(self, date_range, order):
        acc = order['Account']
        for date in date_range:
            if date<=self.today_date:
                date_str = date.strftime('%Y-%m-%d')
                if not date_str in self.accounts[acc]['Transfers'].keys():
                    self.accounts[acc]['Transfers'][date_str] = [[order['Amount'], order['Purpose']]]
                    self.check_if_current_month_listed(date, order)
                else:
                    check = False
                    for transfer in self.accounts[acc]['Transfers'][date_str]:
                        if transfer[0]==order['Amount'] and transfer[1]==order['Purpose']:
                            check = True
                    if check==False:
                        self.accounts[acc]['Transfers'][date_str].append([order['Amount'], order['Purpose']])
                        self.check_if_current_month_listed(date, order)

    def check_standingorders_in_transfer(self, acc):
        orders = []
        for i in range(len(self.standingorders)):
            order = self.standingorders[i]
            if acc in order['Account']:
                #parse standing order entry in date
                date_range = self.make_dates(order['From'], order['To'], order['Day'])

                #populate standingorder into transfers of account
                self.add_standingorder_to_transfers(date_range, order)
        


                






        
                


    def calculate_end_month_status(self, acc):
        pass

    def calculate_month_summary(self, acc, month):
        pass

    

        