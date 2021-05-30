import json

class Sizes():
    def __init__(self):  

        with open('settings.json', 'r') as lp:
            self.file = json.load(lp)
        self.labelsize  = self.file['Labelsize']
        self.titlesize  = self.file['Titlesize']
        self.linewidth  = self.file['Linewidth']
        self.markersize = self.file['Markersize']
        '''settings = {}
        settings['Labelsize'] = 20
        settings['Titlesize'] = 20
        settings['Linewidth'] = 5
        settings['Markersize'] = 2

        with open('settings.json', 'w') as qt:
            json.dump(settings, qt)'''   

    def save(self):
        self.file['Labelsize']  = self.labelsize
        self.file['Titlesize']  = self.titlesize
        self.file['Linewidth']  = self.linewidth
        self.file['Markersize'] = self.markersize
        with open('settings.json', 'w') as outfile:
            json.dump(self.file, outfile)

Sizes = Sizes()
 
        