import matplotlib

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

        self.text_color_hex     = str(matplotlib.colors.to_hex([self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3]], keep_alpha=True))
        self.bg_color_hex       = str(matplotlib.colors.to_hex([self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3]], keep_alpha=True))
        self.bg_color_light_hex = str(matplotlib.colors.to_hex([self.bg_color_light[0], self.bg_color_light[1], self.bg_color_light[2], self.bg_color_light[3]], keep_alpha=True))

        self.matplotlib_colors = ['r', 'b', 'g', 'r', 'b', 'g', 'r', 'b', 'g']
        self.matplotlib_rgba   = [(1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1), (1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1), (1, 0, 0, 0.7), (0, 0, 1, 0.7), (0, 180/255, 0, 1)]

Colors = Colors()