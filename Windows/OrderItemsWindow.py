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

        pk_list = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT ID from order_items')]
        order = [str(el[0]) for el in SQL.query(SQL.my_cursor, 'SELECT Order_ID from order_data')]
        product = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Product_Name from product')]
        product_id = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Product_ID from product')]
        product_dict = {product[i]: product_id[i] for i in range(len(product_id))}

        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)

        def validate():

            But2.disabled = Field1.error or Field4.error
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
            else:
                Field1.error = True
            validate()

        def error_4(inst, value):
            Field4.error = False
            if Field4.text != "":
                try:
                    int(Field4.text)
                except ValueError:
                    Field4.error = True
                    Field4.text = 'Количество должно быть числом'
            else:
                Field4.error = True
            validate()

        Field1 = MDTextField(
            hint_text="ID",
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
            helper_text_mode='on_error',
            max_text_length=64,
        )
        Field1.bind(focus=error_1)

        Field2 = Spinner(
            text=order[0],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            values=order
        )

        Field3 = Spinner(
            text=product[0],
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            values=product
        )

        Field4 = MDTextField(
            hint_text="Введите количество",
            pos_hint={"x": 0.05, "y": 0.6},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
            max_text_length=64
        )
        Field4.bind(focus=error_4)

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def new(instance):
            print(f'INSERT INTO order_items VALUES ({Field1.text},'
                                     f'{Field2.text},{product_dict.get(Field3.text)},{Field4.text})')
            SQL.query(SQL.my_cursor, f'INSERT INTO order_items VALUES ({Field1.text},'
                                     f'{Field2.text},{product_dict.get(Field3.text)},{Field4.text})')
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
