from datetime import datetime
from dateutil.relativedelta import relativedelta

class Calculations():
    def __init__(self):  
        pass
        

    def fill_income_expenditure_profit(self, acc):
        dates = list(self.accounts[acc]['Transfers'].keys())
        dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date())
        years = [str(datetime.strptime(dates[0], '%Y-%m-%d').date().year)]
        
        for date_str in dates:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if int(date.year)!=years[-1]:
                years.append(str(date.year))

        for year in years:    
            filter_year        = list(filter(lambda k: str(year) in k, dates))
            year_income        = 0
            year_expenditure   = 0
            if not str(year) in self.accounts[acc]['Income'].keys():
                self.accounts[acc]['Income'][str(year)] = {}
                self.accounts[acc]['Expenditure'][str(year)] = {}
                self.accounts[acc]['Profit'][str(year)] = {}

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

            if len(self.accounts[acc]['Transfers'][date])==0 and len(self.accounts[acc]['Status'].keys())!=0:
                self.accounts[acc]['Status'][date] = self.accounts[acc]['Status'][dates[i-1]]

                
        if not self.today_str in self.accounts[acc]['Status'].keys():
            self.accounts[acc]['Status'][self.today_str] = round(self.accounts[acc]['Status'][dates[-1]], 2)

        self.fill_income_expenditure_profit(acc)
        
       
    def fill_total_status(self):
        self.total['Status'] = {}
        date_min = []
        for acc in self.accounts:
            dates = list(self.accounts[acc]['Transfers'].keys())
            dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
            date_min.append(datetime.strptime(dates[0], '%Y-%m-%d').date())
        try:
            date = min(date_min)

            while date<=self.today_date:
                date_str = date.strftime('%Y-%m-%d')
                for i, acc in enumerate(self.accounts):
                    if date_str in self.accounts[acc]['Transfers'].keys():
                        for transfer in self.accounts[acc]['Transfers'][date_str]:
                            if len(self.total['Status'].keys())==0:
                                self.total['Status'][date_str] = round(transfer[0], 2)
                            elif not date_str in self.total['Status'].keys():
                                self.total['Status'][date_str] = round(self.total['Status'][previous_date_str] + transfer[0], 2)
                            else:
                                self.total['Status'][date_str] = round(self.total['Status'][date_str] + transfer[0], 2)
                        previous_date_str = date_str
                date = date + relativedelta(days=1)
        except:
            pass
      
        if not self.today_str in self.total['Status'].keys():
            try:
                self.total['Status'][self.today_str] = round(self.total['Status'][dates[-1]], 2)
            except:
                pass

    def make_dates(self, from_str, to, day):
        day = day.replace('.','')
        day = '0' + str(day) if int(day)<10 else str(day)
        year_begin = from_str.split('\n')[1]
        year_end   = to.split('\n')[1]
        from_str = from_str.split('\n')[0]
        if '-' in to:
            end_month = '0'+str(self.today_date.month) if int(self.today_date.month)<10 else str(self.today_date.month)
            year_end  = str(self.today_date.year)
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

    def check_todays_status(self, acc):
        dates = list(self.accounts[acc]['Status'].keys())
        dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
        last_date = datetime.strptime(dates[-1], '%Y-%m-%d').date() 
        if last_date<self.today_date:
            self.accounts[acc]['Status'][self.today_str] = self.accounts[acc]['Status'][dates[-1]]
        
    def reset_standingorders_monthlisted(self):
        for i in range(len(self.standingorders['Orders'])):
           self.standingorders['Orders'][str(i)]['MonthListed'] = False

    def check_standingorders(self, acc):
        for i in range(len(self.standingorders['Orders'])):  
            order = self.standingorders['Orders'][str(i)]
            #filter order in terms of account
            if acc in order['Account']:
                date_range = self.make_dates(order['From'], order['To'], order['Day'])

                #check if today is within range of standing order
                if self.today_date>=date_range[0] and self.today_date<=date_range[-1]:

                    #check if todays day is already standing orders day and if it was already listed
                    if self.today_date.day>=date_range[0].day and order['MonthListed']==False:
                        month    = '0'+str(self.today_date.month) if self.today_date.month<10 else str(self.today_date.month)
                        day      = '0'+str(date_range[0].day) if date_range[0].day<10 else str(date_range[0].day)
                        date_str = '{}-{}-{}'.format(self.today_date.year, month, day)

                        #add standingorder to transfers
                        if not date_str in self.accounts[acc]['Transfers'].keys():
                            self.accounts[acc]['Transfers'][date_str] = [[order['Amount'], order['Purpose'], order['Category']]]
                        else:
                            self.accounts[acc]['Transfers'][date_str].append([order['Amount'], order['Purpose'], order['Category']])
                        order['MonthListed'] = True

    def add_order_in_transfers(self, order):
        date_range = self.make_dates(order['From'], order['To'], order['Day'])
        acc = order['Account']
        for date in date_range:

            #only if date is lower than today
            if date<=self.today_date:
                date_str = date.strftime('%Y-%m-%d')

                #add standingorder to transfers
                if not date_str in self.accounts[acc]['Transfers'].keys():
                    self.accounts[acc]['Transfers'][date_str] = [[order['Amount'], order['Purpose']]]
                else:
                    self.accounts[acc]['Transfers'][date_str].append([order['Amount'], order['Purpose']])
                if date.month==self.today_date.month and date.year==self.today_date.year:
                    order['MonthListed'] = True

    def filter_categories_within_dates(self, start_date, end_date):
        self.categories_amounts = {}
        self.categories_expenditures = {}
        for acc in self.accounts:
            dates = list(self.accounts[acc]['Transfers'].keys())
            dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
            for date in dates:
                if datetime.strptime(date, '%Y-%m-%d').date()>=start_date and datetime.strptime(date, '%Y-%m-%d').date()<=end_date:
                    for transfer in self.accounts[acc]['Transfers'][date]:
                        category = transfer[2]
                        amount   = transfer[0]
                        if not category in self.categories_amounts.keys():
                            self.categories_amounts[category] = amount
                        else:
                            self.categories_amounts[category] += amount

                        if not category in self.categories_expenditures.keys() and amount<0:
                            self.categories_expenditures[category] = amount
                        elif amount<0:
                            self.categories_expenditures[category] += amount
        

        self.categories_total = 0
        for cat in self.categories_amounts:
            self.categories_total += self.categories_amounts[cat]

        self.categories_amounts = dict(sorted(self.categories_amounts.items(), key=lambda item: item[1]))
        self.categories_expenditures = dict(sorted(self.categories_expenditures.items(), key=lambda item: item[1]))
        
        #delete amounts >= 0
        to_delete = []
        for cat in self.categories_amounts:
            if self.categories_amounts[cat]>=0:
                to_delete.append(cat)
        for key in to_delete:
            del self.categories_amounts[key]

        #needed for percentage
        self.categories_total = 0
        for cat in self.categories_amounts:
            self.categories_total += self.categories_amounts[cat]

        self.categories_expenditures_total = 0
        for cat in self.categories_expenditures:
            self.categories_expenditures_total += self.categories_expenditures[cat]

    def get_sum_of_category(self, cat, start_date, end_date):
        amount = 0
        for acc in self.accounts:
            dates = list(self.accounts[acc]['Transfers'].keys())
            dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
            for date in dates:
                if datetime.strptime(date, '%Y-%m-%d').date()>=start_date and datetime.strptime(date, '%Y-%m-%d').date()<=end_date:
                    for transfer in self.accounts[acc]['Transfers'][date]:
                        category = transfer[2]
                        if category==cat:
                            amount += transfer[0]
                         
        return amount
                        
    def get_all_months_of_transfers(self):
        dates = list(self.total['Status'].keys())
        dates.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d').date()) 
        date_min = datetime.strptime(dates[0], '%Y-%m-%d').date()
        date_max = datetime.strptime(dates[-1], '%Y-%m-%d').date()
 
        date = date_max - relativedelta(months=1)
        months = [self.months_text[date_max.month-1]+' '+str(date_max.year)]
        while date.year>=date_min.year and date.month>=date_min.month:
            months.append(self.months_text[date.month-1]+' '+str(date.year))
            date = date - relativedelta(months=1)
        return months
        


    ####################################################################################################################################################
    ############################################################ FUNCTIONS ONLY FOR DEMOSETUP ##########################################################
    ####################################################################################################################################################

    def add_order_to_transfers_demosetup(self, date_range, order, acc):
        for date in date_range:

            #only if date is lower than today
            if date<=self.today_date:
                date_str = date.strftime('%Y-%m-%d')

                #add standingorder to transfers
                if not date_str in self.accounts[acc]['Transfers'].keys():
                    self.accounts[acc]['Transfers'][date_str] = [[order['Amount'], order['Purpose'], order['Category']]]
                else:
                    self.accounts[acc]['Transfers'][date_str].append([order['Amount'], order['Purpose'], order['Category']])
                if date.month==self.today_date.month and date.year==self.today_date.year:
                    order['MonthListed'] = True

    def add_standingorders_in_transfers_demosetup(self, acc):
        for i in range(len(self.standingorders['Orders'])):
            order = self.standingorders['Orders'][str(i)]
            if acc in order['Account']:
                #parse standing order entry in date
                date_range = self.make_dates(order['From'], order['To'], order['Day'])

                #populate standingorder into transfers of account
                self.add_order_to_transfers_demosetup(date_range, order, acc)
          
        


                






        
                


    

    

        