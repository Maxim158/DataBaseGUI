from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
import SQL

BTN_SIZE = (.14, .1)


class Department(MDApp):

    def build(self):
        screen = FloatLayout()

        pk_list = [el[0] for el in SQL.query('SELECT Department_ID from department')]

        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)

        def validate():

            But2.disabled = Field1.error or Field2.error

            print(f'{But2.disabled} BUTTON')
            print(f'{Field1.error} BUTTON {Field2.error}')

        def error_1(instance, value):
            Field1.error = False
            if Field1.text != "":
                try:
                    int(Field1.text)
                    if int(Field1.text) in pk_list:
                        Field1.helper_text = 'That ID already exists'
                        Field1.error = True
                except ValueError:
                    Field1.error = True
                    Field1.helper_text = 'ID must be INT'
            else: Field1.error = True
            validate()

        def error_2(instance, value):
            Field2.error = False
            if Field2.text == "":
                Field2.error = True
            validate()

        Field1 = MDTextField(
            hint_text="Department ID",
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
            helper_text_mode='on_error',
            max_text_length=64,
        )
        Field1.bind(focus=error_1)

        Field2 = MDTextField(
            hint_text="Department Name",
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=50,
            required=True
        )
        Field2.bind(focus=error_2)

        Field3 = MDTextField(
            hint_text="Description",
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=256,
        )

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='?????????????? ????????',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def new(instance):
            print(f'INSERT INTO department VALUES ({Field1.text}, {Field2.text},'
                                     f' {Field3.text if Field3.text != "" else "null"})')
            SQL.query(f'INSERT INTO department VALUES ({Field1.text}, \'{Field2.text}\','
                                     f' {Field3.text if Field3.text != "" else "null"})')
            MDApp.get_running_app().stop()

        But2 = MDRaisedButton(
            text='????????????????',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.81, "y": 0.05},
            on_release=new,
            disabled=True
        )

        screen.add_widget(Field1)
        screen.add_widget(Field2)
        screen.add_widget(Field3)
        screen.add_widget(But1)
        screen.add_widget(But2)
        return screen


if __name__ == "__main__":
    Department().run()
