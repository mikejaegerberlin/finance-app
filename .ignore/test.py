from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreen:

    MDFillRoundFlatButton:
        text: 'HI'
        size_hint_x: 0.5
        pos_hint: {"center_x": .5, "center_y": .5}

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.03
        MDBoxLayout:
            size_hint: 0.1, 1
        
        MDLabel:
            size_hint_x: 0.35
            text: 'Expenditures:'
            font_style: 'Subtitle2'
            theme_text_color: 'Custom'
            halign: 'left'

        MDLabel:
            id: status_expenditures_label
            font_style: 'Subtitle2'
            halign: 'center'
            size_hint: 0.45, 1
            
        MDBoxLayout:
            size_hint: 0.1, 1

'''


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)


Example().run()
