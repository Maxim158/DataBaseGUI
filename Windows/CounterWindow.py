from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import FloatLayout

BTN_SIZE = (.14, .1)


class Counter(MDApp):

    def build(self):
        screen = FloatLayout()

        Field1 = MDLabel(
            text="Данная таблица не может быть изменена",
            halign="center"
        )

        screen.add_widget(Field1)
        return screen


if __name__ == "__main__":
    Counter().run()
