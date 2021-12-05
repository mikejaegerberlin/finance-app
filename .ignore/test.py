import base64
import json


file = open(r'C:\Users\jmike\OneDrive\Desktop\MyApps\finance-app\.ignore\data.vifi', "rb")
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
    
accounts = my_data['accounts']
standingorders = my_data['standingorders']
categories = my_data['categories']
for order in standingorders['Orders']:
    if standingorders['Orders'][order]['MonthListed'] == 'Trü':
        standingorders['Orders'][order]['MonthListed'] = True
    else:
        standingorders['Orders'][order]['MonthListed'] = False

my_data = {}
my_data['accounts']       = accounts
my_data['standingorders'] = standingorders
my_data['categories']     = categories
print (my_data)
with open(r'C:\Users\jmike\OneDrive\Desktop\MyApps\finance-app\.ignore\my_data.vifi', 'w') as outfile:
    json.dump(my_data, outfile)