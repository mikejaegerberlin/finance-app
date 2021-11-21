import random
from datetime import datetime
from backend.account_calculations import Calculations
import json
from kivy.utils import platform
import base64



class DemoData(Calculations):
    def __init__(self): 
        #structure:
        #accounts[account]['Transfers'][date]
        #accounts[account]['Status'][date]

        #accounts[account]['Income'][year]
        #accounts[account]['Expenditure'][year]
        #accounts[account]['Profit'][year]

        #accounts[account]['Income'][year][month]
        #accounts[account]['Expenditure'][year][month]
        #accounts[account]['Profit'][year][month]
        self.keys_list       = ['Transfers', 'Status', 'Income', 'Expenditure', 'Profit']
        self.current_account = ''
        self.today_str       = datetime.today().strftime('%Y-%m-%d')
        self.today_date      = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        month                = '0'+str(self.today_date.month) if self.today_date.month<10 else str(self.today_date.month)
        year                 = str(self.today_date.year)
        self.first_of_month_date = datetime.strptime('{}-{}-01'.format(year, month), '%Y-%m-%d').date() 
        self.current_month   = int(self.today_date.month)
        self.current_year    = int(self.today_date.year)
        self.months          = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.months_rev      = {'January': 1, 'February': 2, 'March': 3, 'April':4, 'Mai': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'December': 12,
                                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr':4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Dez': 12}
        self.months_text     = ['January', 'February', 'March', 'April', 'Mai', 'June', 'July', 'August', 'September', 'Oktober', 'November', 'December']
        self.total           = {}
        try:
            #self.jiubui()
            self.load_internal_setup()      
        except:
            self.accounts        = {}
            self.standingorders  = {}
            self.standingorders['Orders'] = {}
            self.standingorders['Reset date'] = self.today_str
            self.categories = []
            self.save_accounts(demo_mode=False)
            self.save_standingorders(demo_mode=False)
        
    def load_setup(self, path):

        file = open(path, "rb")
        bytes = file.read()
        msg_bytes = base64.b64decode(bytes)
        ascii_msg = msg_bytes.decode('ascii')
        replace_numbers = [12,11,10,1,2,3,4,5,6,7,8,9]
        ascii_msg = ascii_msg.replace("'", "\"").replace('oe','ö').replace('ue','ü').replace('ae','ä')

        for number in replace_numbers:
            ascii_msg = ascii_msg.replace(str(number)+':','"'+str(number)+'":')
        try:
            my_data = json.loads(ascii_msg)
        except Exception as err:
            error_string = str(err)
            spot = int(error_string.split('(')[-1].replace('char ','').replace(')',''))
            ascii_msg = ascii_msg[0:spot]
            my_data = json.loads(ascii_msg)
            
        self.accounts = my_data['accounts']
        self.standingorders = my_data['standingorders']
        self.categories = my_data['categories']
        for order in self.standingorders['Orders']:
            if self.standingorders['Orders'][order]['MonthListed'] == 'Trü':
                self.standingorders['Orders'][order]['MonthListed'] = True
            else:
                self.standingorders['Orders'][order]['MonthListed'] = False

    def save_setup(self):

        my_data = {}
        my_data['accounts']       = self.accounts
        my_data['standingorders'] = self.standingorders
        my_data['categories']     = self.categories
        if platform == 'android':
            for order in my_data['standingorders']['Orders']:
                my_data['standingorders']['Orders'][order]['MonthListed'] = str(my_data['standingorders']['Orders'][order]['MonthListed'])
            message = str(my_data)
            message = message.replace('ö','oe').replace('ü','ue').replace('ä','ae')
            ascii_message = message.encode('ascii')
            binary_data = base64.b64encode(ascii_message)
            
            #binary_data = binascii.a2b_base64(data_string)
            self.save_file_android(binary_data)
        else:
            with open('\my_datttaaa.vifi', 'w') as outfile:
                json.dump(my_data, outfile)

    def save_file_android(self, binary_data):
        from kivy.logger import Logger
        from kivy.clock import Clock
        from jnius import autoclass
        from jnius import cast
        from android import activity
        from android.permissions import Permission, request_permissions, check_permission
        
        Activity = autoclass('android.app.Activity')
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')
        FileOutputStream = autoclass('java.io.FileOutputStream')
        Env = autoclass('android.os.Environment')

        MediaStore_Images_Media_DATA = "_data"

        # Custom request codes
        RESULT_SAVE_DOC = 1

        def android_dialog_save_doc(save_callback):
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            
            def on_activity_save(request_code, result_code, intent):
                if request_code != RESULT_SAVE_DOC:
                    Logger.warning('android_dialog_save_doc: ignoring activity result that was not RESULT_SAVE_DOC')
                    return
                
                if result_code == Activity.RESULT_CANCELED:
                    Clock.schedule_once(lambda dt: save_callback(None), 0)
                    return
                
                if result_code != Activity.RESULT_OK:
                    # This may just go into the void...
                    raise NotImplementedError('Unknown result_code "{}"'.format(result_code))
                
                selectedUri = intent.getData()                  # Uri
                filePathColumn = [MediaStore_Images_Media_DATA] # String
                
                # Cursor
                cursor = currentActivity.getContentResolver().query(selectedUri, filePathColumn, None, None, None)
                cursor.moveToFirst()
                
                # If you need to get the document path, but I used selectedUri.getPath()
                # columnIndex = cursor.getColumnIndex(filePathColumn[0])  # int
                # docPath = cursor.getString(columnIndex)                 # String
                cursor.close()
                Logger.info('android_ui: android_dialog_save_doc() selected %s', selectedUri.getPath())
                
                Clock.schedule_once(lambda dt: save_callback(selectedUri), 0)
            
            activity.bind(on_activity_result = on_activity_save)
            
            # Here's another Intent in contrast to get the file
            intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            intent.setType('*/*')
            
            currentActivity.startActivityForResult(intent, RESULT_SAVE_DOC)
                    
        def android_do_saving(uri):
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                         
            pfd = currentActivity.getContentResolver().openFileDescriptor(uri, "w")
            fos = FileOutputStream(pfd.getFileDescriptor())
            fos_ch = fos.getChannel()
            fos.write(binary_data)
            #fos_ch.truncate(len(binary_data))
            fos.close()
            openedUri = uri
                    
        android_dialog_save_doc(android_do_saving)
    

    def create_new_setup(self):
        self.categories      = ['Freizeit', 'Musik', 'Möbel', 'Miete', 'Essen&Trinken', 'Reisen', 'Versicherung', 'Gehalt', 'Bekleidung']
        accounts_list = ['DKB', 'ING']
        Purposes      = ['Wohnung', 'Proberaum', 'Schuhe', 'Schrank', 'Vedis', 'Eis', 'Cocktails', 'B-DD', 
                        'Looperboard', 'Gitarre', 'Bier']
        
        years         = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        #years         = [2019, 2020, 2021]
        #initialize dictionaries
        self.accounts = {}
        for acc in accounts_list:
            self.accounts[acc] = {}
            for key in self.keys_list:
                self.accounts[acc][key] = {}
        
        #fill transfers
        for acc in accounts_list:
            for q in range(500):
                year      = random.randint(years[0],years[-1])
                month     = random.randint(1,12)
                day       = random.randint(1,28)
                amount    = round(float(random.randint(-100,100)) + round(random.random(),2),2)
                purpose   = Purposes[random.randint(0,10)]
                category  = self.categories[random.randint(0,8)]

                month_str = '0'+str(month) if month<10 else str(month)
                day_str   = '0'+str(day) if day<10 else str(day)
                date      = '{}-{}-{}'.format(year, month_str, day_str)

                if not datetime.strptime(date, '%Y-%m-%d').date()>self.today_date:
                    if date in self.accounts[acc]['Transfers'].keys():
                        self.accounts[acc]['Transfers'][date].append([amount, purpose, category])
                    else:
                        self.accounts[acc]['Transfers'][date] = [[amount, purpose, category]]
        
            dates = list(self.accounts[acc]['Transfers'].keys())
            
            #fill income, expenditure, profit
            for year in years:
                year = str(year)
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

        
        keys = ['Account', 'From', 'M/A', 'Day', 'Purpose', 'Amount', 'Category', 'MonthListed']
        mo_an = ['M', 'A']
        self.standingorders['Orders'] = {}
        for i in range(4):
            i = str(i)
            self.standingorders['Orders'][str(i)] = {}
            self.standingorders['Orders'][str(i)][keys[0]] = accounts_list[random.randint(0,1)]
            self.standingorders['Orders'][str(i)][keys[1]] = self.months[random.randint(0,7)] + '\n' + '2021'
            self.standingorders['Orders'][str(i)][keys[2]] = mo_an[random.randint(0,1)]
            day       = random.randint(1,5)
            amount    = round(float(random.randint(-200,200)) + round(random.random(),2),2)
            purpose   = Purposes[random.randint(0,10)] 
            category  = self.categories[random.randint(0,8)]
            self.standingorders['Orders'][str(i)][keys[3]] = str(day)+'.'
            self.standingorders['Orders'][str(i)][keys[4]] = purpose
            self.standingorders['Orders'][str(i)][keys[5]] = amount
            self.standingorders['Orders'][str(i)][keys[6]] = category
            self.standingorders['Orders'][str(i)][keys[7]] = False
        self.standingorders['Reset date']   = self.today_str
        
        for acc in self.accounts:
            self.add_standingorders_in_transfers_demosetup(acc)
            self.fill_status_of_account(acc)
        
    def save_accounts(self, demo_mode):
        my_data = {}
        my_data['accounts']       = self.accounts
        my_data['standingorders'] = self.standingorders
        my_data['categories']     = self.categories
  
        if not demo_mode:
            with open('my_data.vifi', 'w') as outfile:
                json.dump(my_data, outfile)

    def load_internal_setup(self):
        with open('my_data.vifi', 'r') as infile:
            my_data = json.load(infile)
        
        self.accounts = my_data['accounts']
        self.standingorders = my_data['standingorders']
        self.categories = my_data['categories']
                            
    def save_standingorders(self, demo_mode):
        self.save_accounts(demo_mode)
        

DemoData = DemoData()
