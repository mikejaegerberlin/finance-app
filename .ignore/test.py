from kivymd.app import MDApp
from kivy.lang import Builder


class Test(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('test.kv')

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return self.screen
        


Test().run()