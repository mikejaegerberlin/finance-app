import json
from backend.demo_setup import DemoData as data

class ScreenSettings():
    def __init__(self):
        self.make_structure()
        #self.load_settings()

    def make_structure(self):
        self.settings = {}
        self.settings['AccountScreen'] = {}
        self.settings['AccountScreen']['SelectedGraphs'] = {}
        self.settings['AccountScreen']['SelectedGraphs']['DKB'] = 'down'
        self.settings['AccountScreen']['SelectedGraphs']['ING'] = 'down'
        self.settings['AccountScreen']['SelectedGraphs']['Cash'] = 'down'

        self.settings['CategoriesScreen'] = {}
        self.settings['CategoriesScreen']['SelectedGraphs'] = {}
        for q, cat in enumerate(data.categories):
            self.settings['CategoriesScreen']['SelectedGraphs'][cat] = 'down' if q<4 else 'normal'

    def load_settings(self):

        with open('settings.json', 'r') as lp:
            self.settings = json.load(lp)

    def save(self):
        with open('settings.json', 'w') as qt:
            json.dump(self.settings, qt)

class Sizes():
    def __init__(self):  

        settings = {}
        settings['Labelsize'] = 12
        settings['Titlesize'] = 20
        settings['Linewidth'] = 5
        settings['Markersize'] = 3

        #with open('settings.json', 'w') as qt:
        #    json.dump(settings, qt)

        #with open('settings.json', 'r') as lp:
        #    self.file = json.load(lp)

        self.labelsize  = settings['Labelsize']
        self.titlesize  = settings['Titlesize']
        self.linewidth  = settings['Linewidth']
        self.markersize = settings['Markersize']

    def save(self):
        self.file['Labelsize']  = self.labelsize
        self.file['Titlesize']  = self.titlesize
        self.file['Linewidth']  = self.linewidth
        self.file['Markersize'] = self.markersize
        with open('settings.json', 'w') as outfile:
            json.dump(self.file, outfile)

Sizes = Sizes()
ScreenSettings = ScreenSettings()
 
        