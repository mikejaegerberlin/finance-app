import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
 
 
class MainWid(BoxLayout):
    def __init__(self):
        super(MainWid, self).__init__()
        for i in range(30):
            self.ids.container_y.add_widget(Button(text=f"Botony: {i}"))
        for i in range(30):
            self.ids.container_x.add_widget(Button(text=f"Botonx: {i}"))
 
 
class MainApp(App):
    title = "Scroll view"
 
    def build(self):
        return MainWid()
 
 
if __name__ == "__main__":
    MainApp().run()