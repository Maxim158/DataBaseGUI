from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
import SQL

BTN_SIZE = (.14, .1)


class ResStatus(MDApp):

    def build(self):

        screen = FloatLayout()

        pk_list = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Status_ID from research_status')]

        with open('data.txt', 'r') as file:
            data = (file.read().replace('\"', '')[:-1].split(sep='!'))

        print(f'{data}')

        def validate():

            But2.disabled = Field1.error or Field2.error
            print(f'{But2.disabled} BUTTON')

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
            validate()

        def error_2(inst, value):
            Field2.error = False
            if Field2.text == "": Field2.error = True
            validate()

        Field1 = MDTextField(
            hint_text="Status ID",
            text=data[0],
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=18,
            required=True,
            disabled=True
        )
        Field1.bind(focus=error_1)

        Field2 = MDTextField(
            hint_text="Status Name",
            text=data[1],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=20,
            required=True
        )
        Field2.bind(focus=error_2)

        Field3 = MDTextField(
            hint_text="Description",
            text=data[2],
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=50,
        )

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def delete(instance):

            SQL.query(SQL.my_cursor, f'DELETE from research_status WHERE Status_ID = {Field1.text}')
            SQL.mydb.commit()
            MDApp.get_running_app().stop()

        def new(instance):
            SQL.query(SQL.my_cursor, f'UPDATE research_status SET '
                                     f'Status_Name = \'{Field2.text}\','
                                     f'Description = \'{Field3.text if Field3.text != "" else "null"}\''
                                     f' WHERE Status_ID = {Field1.text}')
            SQL.mydb.commit()
            MDApp.get_running_app().stop()

        But2 = MDRaisedButton(
            text='Изменить',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.81, "y": 0.05},
            on_release=new,
        )

        But3 = MDRaisedButton(
            text='Удалить',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.61, "y": 0.05},
            on_release=delete,
        )

        screen.add_widget(Field1)
        screen.add_widget(Field2)
        screen.add_widget(Field3)
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(But3)
        return screen


if __name__ == "__main__":
    ResStatus().run()
