from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
import SQL

BTN_SIZE = (.14, .1)


class Employee(MDApp):

    def build(self):
        def menu_callback(text_item):
            Field1.text = text_item

        screen = FloatLayout()

        res = [el[0] for el in SQL.query('SELECT Research_Name from research')]
        menu_items = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback(x),
                'height': dp(64)
            } for data in res
        ]

        Field1 = MDTextField(
            hint_text="Testing",
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
        )

        def on_focus(inst, value):
            if value:
                menu.open()

        menu = MDDropdownMenu(
            caller=Field1,
            items=menu_items,
            width_mult=4
        )

        Field1.bind(focus=on_focus)

        screen.add_widget(Field1)
        return screen


if __name__ == "__main__":
    Employee().run()
