import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime
from backend.settings import Sizes
from backend.colors import Colors

class PieChart():
    def __init__(self):  
        #basic things
        self.months     = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        self.today_str  = datetime.today().strftime('%Y-%m-%d')
        self.today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
        self.fig     = plt.figure(figsize=(1,1), dpi=100)    

    def make_plot(self, categories):
        plt.close(self.fig)
        self.fig     = plt.figure(figsize=(1,1), dpi=100)
        self.ax      = self.fig.add_subplot(111)
        labels       = []
        values       = []
        colors       = []
        for i, label in enumerate(categories):
            labels.append(label)
            values.append(-categories[label])
            colors.append(Colors.piechart_colors[i])
      
        self.fig.patch.set_facecolor(Colors.bg_color_hex)
        piechart = self.ax.pie(values, labels = labels, autopct='%1.1f%%', startangle=15, shadow = True, colors=colors)
        self.ax.axis('equal')
        canvas = self.fig.canvas 

        return canvas 

PieChart = PieChart()