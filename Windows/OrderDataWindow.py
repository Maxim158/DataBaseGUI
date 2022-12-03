from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivymd.uix.pickers import MDDatePicker
import SQL

BTN_SIZE = (.14, .1)


class Order(MDApp):

    def build(self):
        screen = FloatLayout()

        pk_list = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Order_ID from order_data')]
        res_name = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Research_Name from research')]
        status = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Status_Name from order_status')]
        status_id = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Status_ID from order_status')]
        status_dict = {status[i]: status_id[i] for i in range(len(status_id))}

        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)

        def validate():

            But2.disabled = Field1.error
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

        Field1 = MDTextField(
            hint_text="Order ID",
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
            helper_text_mode='on_error',
            max_text_length=64,
        )
        Field1.bind(focus=error_1)

        Field2 = Spinner(
            text=res_name[0],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            values=res_name
        )

        def save(inst, value,date_range):
            Field3.text=str(value)

        def show_date(inst):
            date_dialog = MDDatePicker(year=2020, month=1, day=1)
            date_dialog.bind(on_save=save)
            date_dialog.open()

        Field3 = Button(
            text="Select Date",
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05}
        )
        Field3.bind(on_release=show_date)

        Field4 = Spinner(
            text=status[0],
            pos_hint={"x": 0.05, "y": 0.6},
            size_hint={0.6, 0.05},
            values=status
        )

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def new(instance):
            print(f'INSERT INTO order_data VALUES ({Field1.text},'
                                     f'\'{Field2.text}\',{Field3.text},\'{status_dict.get(Field4.text)}\')')
            SQL.query(SQL.my_cursor, f'INSERT INTO order_data VALUES ({Field1.text},'
                                     f'\'{Field2.text}\',\'{Field3.text}\',\'{status_dict.get(Field4.text)}\')')
            SQL.mydb.commit()
            MDApp.get_running_app().stop()

        But2 = MDRaisedButton(
            text='Добавить',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.81, "y": 0.05},
            on_release=new,
            disabled=True
        )

        screen.add_widget(Field1)
        screen.add_widget(Field2)
        screen.add_widget(Field3)
        screen.add_widget(Field4)
        screen.add_widget(But1)
        screen.add_widget(But2)
        return screen


if __name__ == "__main__":
    Order().run()
