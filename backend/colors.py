import matplotlib
import random

class Colors(object):
    def __init__(self, **kwargs):
        self.bg_color                     = (0.1, 0.1, 0.1, 1)
        self.bg_color_light               = (100/255, 94/255, 99/255,  0.15)
        self.text_color                   = (255/255, 253/255, 250/255, 1)
        self.primary_color                = (0, 7/255, 143/255, 1)
        self.error_color                  = (1, 0, 0, 0.7)
        self.black_color                  = (0, 0, 0, 1)
        self.green_color                  = (0, 180/255, 0, 1)
        self.button_disable_onwhite_color = (0, 0, 0, 0.3)
        self.white_color                  = (1,1,1,1)

        self.text_color_hex     = str(matplotlib.colors.to_hex([self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3]], keep_alpha=True))
        self.bg_color_hex       = str(matplotlib.colors.to_hex([self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3]], keep_alpha=True))
        self.bg_color_light_hex = str(matplotlib.colors.to_hex([self.bg_color_light[0], self.bg_color_light[1], self.bg_color_light[2], self.bg_color_light[3]], keep_alpha=True))



        self.piechart_colors   = []#(1,0,0,0.7), (252/255, 186/255, 3/255, 1), (255/255, 251/255, 38/255, 1), (0/255, 7/255, 143/255, 1), (4/255, 237/255, 0/255, 1),
                                  #(166/255, 0/255, 237/255, 1), (143/255, 75/255, 7/255, 1)]
                            
        for i in range(50):
            c1 = random.randint(10,255)
            c2 = random.randint(10,255)
            c3 = random.randint(10,255)
            self.piechart_colors.append((c1/255, c2/255, c3/255, 1))

        self.matplotlib_colors = ['r', 'b', 'g', 'r', 'b', 'g', 'r', 'b', 'g']
        self.matplotlib_rgba   = [(1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1), (1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1), (1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1)]

Colors = Colors()