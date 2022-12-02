from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


kv = Builder.load_string("""
Screen:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Changing row Window'
        Button:
            text: 'Exit'
            on_release: app.stop()
""")


class AddWindow(App):

    def build(self):
        return kv


if __name__ == "__main__":
    AddWindow().run()
