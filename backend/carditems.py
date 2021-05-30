from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from backend.colors import Colors

class CardItemsBackend():
    def __init__(self):  
        self.cards_transferitem = []

    def generate_carditems(self, number):
        if number>1 and len(self.cards_transferitem)>60:
            pass
        else:
            for i in range(number):
                sublist = []
                card = MDCard(size_hint_y=None, height='36dp', md_bg_color=Colors.bg_color, ripple_behavior=True, ripple_color=Colors.bg_color_light)
                contentbox          = MDBoxLayout(orientation='horizontal', md_bg_color=Colors.bg_color, radius=[10,10,10,10]) 
                datelabel           = MDLabel(text='', font_style='Subtitle2')
                datelabel.color     = Colors.text_color
                datelabel.halign    = 'center'
                contentbox.add_widget(datelabel)   
                purposelabel        = MDLabel(text='', font_style='Subtitle2')
                purposelabel.color  = Colors.text_color
                purposelabel.halign = 'center'
                contentbox.add_widget(purposelabel)
                amountlabel         = MDLabel(text='', font_style='Subtitle2')
                amountlabel.color   = Colors.text_color
                amountlabel.halign  = 'center'
                contentbox.add_widget(amountlabel) 
                card.add_widget(contentbox)
                sublist = [card, contentbox, datelabel, purposelabel, amountlabel]
                self.cards_transferitem.append(sublist)

CardItemsBackend = CardItemsBackend()