###A ExpansionPanel### 
class SettingsContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super(SettingsContent, self).__init__(**kwargs)
        
    def update_plot(self, touch):
        slider_labelsize = self.ids.slider_labelsize
        labelsize = (int(slider_labelsize.value))
        YearPlot.labelsize = labelsize

class SettingsView(MDBoxLayout):
    def __init__(self, **kwargs):
        super(SettingsView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(
                MDExpansionPanel(
                    icon="none",
                    content=SettingsContent(),
                    panel_cls=MDExpansionPanelOneLine(
                        text="Labelsettings",
                    )
                )
            )
        self.add_widget(Label())

<SettingsContent>
    adaptive_height: True
    orientation: "vertical"
    slider_labelsize: slider_labelsize
    Screen:
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: "Labelsize"

            MDSlider:
                id: slider_labelsize
                on_touch_down: root.update_plot(slider_labelsize)
                on_touch_move: root.update_plot(slider_labelsize)
                on_touch_up: root.update_plot(slider_labelsize)
                min: 8
                max: 24
                value: 12
    Screen:
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: "Titlesize"

            MDSlider:
                min: 0
                max: 100
                value: 80



###Menu Dropdown###
self.menu_items = [
            {
                "text": "Label",
                "viewclass": "OneListItem",
                "on_release": lambda x: self.add_value(),
            } 
        ]     
        self.menu = MDDropdownMenu(
            caller=Button(),
            items=self.menu_items,
            width_mult=4,
        )

MDFloatingActionButton:
                    icon: "settings"
                    md_bg_color: root.txt_color  
                    elevation_normal: 8
                    x: self.width - dp(45)
                    y: dp(500)
                    user_font_size: "12sp"
                    on_release: root.show_dropdown()



