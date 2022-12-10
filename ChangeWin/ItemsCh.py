from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivymd.uix.pickers import MDDatePicker
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
import SQL

BTN_SIZE = (.14, .1)


class Order(MDApp):

    def build(self):

        def menu_callback_2(text_item):
            Field2.text = text_item
            Field2.error = False
            menu2.dismiss()
            validate()

        def menu_callback_3(text_item):
            Field3.text = text_item
            Field3.error = False
            menu3.dismiss()
            validate()

        screen = FloatLayout()

        with open('data.txt', 'r') as file:
            data = (file.read().replace('\"', '')[:-1].split(sep='!'))

        print(f'{data}')

        pk_list = [el[0] for el in SQL.query('SELECT ID from order_items')]
        order = [str(el[0]) for el in SQL.query('SELECT Order_ID from order_data')]
        product = [el[0] for el in SQL.query('SELECT Product_Name from product')]
        product_id = [el[0] for el in SQL.query('SELECT Product_ID from product')]
        product_dict = {product[i]: product_id[i] for i in range(len(product_id))}
        menu_items_2 = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback_2(x),
                'height': dp(64)
            } for data in order
        ]
        menu_items_3 = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback_3(x),
                'height': dp(64)
            } for data in product
        ]

        def on_focus(inst, value):
            if value:
                if inst == Field2:
                    menu2.open()
                if inst == Field3:
                    menu3.open()

        def validate():

            But2.disabled = Field1.error or Field2.error or Field3.error or Field4.error
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
            text=data[3],
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
            helper_text_mode='on_error',
            max_text_length=64,
            disabled=True
        )
        Field1.bind(focus=error_1)

        Field2 = MDTextField(
            hint_text="Order ID",
            text=data[0],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
        )

        menu2 = MDDropdownMenu(
            caller=Field2,
            items=menu_items_2,
            width_mult=4
        )
        Field2.bind(focus=on_focus)

        f3 = [k for k, v in product_dict.items() if v == int(data[1])]
        Field3 = MDTextField(
            hint_text="Product",
            text=f3[0],
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
        )

        menu3 = MDDropdownMenu(
            caller=Field3,
            items=menu_items_3,
            width_mult=4
        )
        Field3.bind(focus=on_focus)

        Field4 = MDTextField(
            hint_text="Введите количество",
            text=data[2],
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

        def delete(instance):

            SQL.query(f'DELETE from order_items WHERE ID = {Field1.text}')
            
            MDApp.get_running_app().stop()

        def new(instance):
            SQL.query(f'UPDATE order_items SET '
                                     f'ORDER_ID = {Field2.text},'
                                     f'PRODUCT_ID = {product_dict.get(Field3.text)},'
                                     f'Quantity = {Field4.text} '
                                     f'WHERE ID = {Field1.text}')
            
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
        screen.add_widget(Field4)
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(But3)
        return screen


if __name__ == "__main__":
    Order().run()
