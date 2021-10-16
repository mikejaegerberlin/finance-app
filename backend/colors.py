import matplotlib
import random

class Colors(object):
    def __init__(self, **kwargs):
        self.bg_color                     = (0.18, 0.18, 0.18, 1)
        #self.bg_color                     = (0,0,0, 1)
        self.bg_color_light               = (100/255, 94/255, 99/255,  0.15)
        self.text_color                   = (255/255, 253/255, 250/255, 1)
        #self.primary_color                = (0, 7/255, 143/255, 1)
        self.primary_color                = (255/255, 205/255, 10/255, 1)
        
        self.error_color                  = (1, 0, 0, 0.7)
        self.black_color                  = (0, 0, 0, 1)
        self.green_color                  = (0, 180/255, 0, 1)
        self.button_disable_onwhite_color = (0, 0, 0, 0.3)
        self.white_color                  = (1,1,1,1)

        self.text_color_hex     = str(matplotlib.colors.to_hex([self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3]], keep_alpha=True))
        self.bg_color_hex       = str(matplotlib.colors.to_hex([self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3]], keep_alpha=True))
        self.bg_color_light_hex = str(matplotlib.colors.to_hex([self.bg_color_light[0], self.bg_color_light[1], self.bg_color_light[2], self.bg_color_light[3]], keep_alpha=True))

        self.piechart_colors   = [(255/255, 205/255, 10/255, 1), (255/255, 120/255, 10/255, 1), (255/255, 0/255, 10/255, 1), (255/255, 0/255, 150/255, 1),
                                  (255/255, 0/255, 255/255, 1), (200/255, 0/255, 255/255, 1), (150/255, 0/255, 255/255, 1), (100/255, 0/255, 255/255, 1),
                                  (50/255, 0/255, 255/255, 1), (0/255, 0/255, 255/255, 1), (0/255, 100/255, 255/255, 1), (0/255, 150/255, 255/255, 1),
                                  (0/255, 200/255, 255/255, 1), (0/255, 255/255, 255/255, 1), (0/255, 255/255, 200/255, 1), (0/255, 255/255, 150/255, 1),
                                  (0/255, 255/255, 100/255, 1), (0/255, 255/255, 50/255, 1), (0/255, 255/255, 0/255, 1), (100/255, 255/255, 0/255, 1),
                                  (150/255, 255/255, 0/255, 1), (200/255, 255/255, 0/255, 1), (255/255, 255/255, 0/255, 1)]
        self.piechart_colors_hex = []
        for color in self.piechart_colors:
            self.piechart_colors_hex.append(str(matplotlib.colors.to_hex(color, keep_alpha=True)))
        #for i in range(50):
        #    c1 = random.randint(50,255)
        #    c2 = random.randint(50,255)
        #    c3 = random.randint(50,255)
        #    self.piechart_colors.append((c1/255, c2/255, c3/255, 1))
        #    self.piechart_colors_hex.append(str(matplotlib.colors.to_hex([c1/255, c2/255, c3/255, 1], keep_alpha=True)))

        self.matplotlib_colors = ['r', 'b', 'g', 'r', 'b', 'g', 'r', 'b', 'g']
        self.matplotlib_rgba   = [(1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1), (1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1), (1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1)]

Colors = Colors()