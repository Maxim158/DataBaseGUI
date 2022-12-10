from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
import SQL

BTN_SIZE = (.14, .1)


class Product(MDApp):

    def build(self):

        def menu_callback_2(text_item):
            Field2.text = text_item
            Field2.error = False
            menu2.dismiss()
            validate()

        def menu_callback_7(text_item):
            Field7.text = text_item
            Field7.error = False
            menu7.dismiss()
            validate()

        screen = FloatLayout()

        pk_list = [el[0] for el in SQL.query('SELECT Product_ID from product')]
        cat = [el[0] for el in SQL.query('SELECT Category_Name from product_categories')]
        cat_id = [el[0] for el in SQL.query('SELECT Category_ID from product_categories')]
        war = [el[0] for el in SQL.query('SELECT Warehouse_Name from warehouse')]
        war_id = [el[0] for el in SQL.query('SELECT Warehouse_ID from warehouse')]

        cat_dict = {cat[i]: cat_id[i] for i in range(len(cat_id))}
        war_dict = {war[i]: war_id[i] for i in range(len(war_id))}

        menu_items_2 = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback_2(x),
                'height': dp(64)
            } for data in cat
        ]
        menu_items_7 = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback_7(x),
                'height': dp(64)
            } for data in war
        ]

        def on_focus(inst, value):
            if value:
                if inst == Field2:
                    menu2.open()
                if inst == Field7:
                    menu7.open()

        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)

        def validate():

            But2.disabled = Field1.error or Field2.error or Field3.error or Field5.error or Field6.error or Field7.error
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

        def error_3(instance, value):
            Field3.error = False
            if has_numbers(Field3.text):
                Field3.error = True
                Field3.helper_text = 'Name shouldn\'t contains numbers'
            if Field3.text == "": Field3.error = True
            validate()

        def error_5(instance, value):
            Field5.error = False
            if Field5.text != "":
                try:
                    float(Field5.text)
                except ValueError:
                    Field5.error = True
                    Field5.helper_text = 'Price must be float'
            else:
                Field5.error = True
            validate()

        def error_6(instance, value):
            Field6.error = False
            if Field6.text == '': Field6.error = True
            try:
                int(Field6.text)
            except ValueError:
                Field6.error = True
                Field6.helper_text = 'Quantity must be INT'
            validate()

        Field1 = MDTextField(
            hint_text="Product ID",
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=64,
            required=True
        )
        Field1.bind(focus=error_1)

        Field2 = MDTextField(
            hint_text="Categories",
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
            error=True
        )
        menu2 = MDDropdownMenu(
            caller=Field2,
            items=menu_items_2,
            width_mult=4
        )
        Field2.bind(focus=on_focus)

        Field3 = MDTextField(
            hint_text="Product Name",
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=50,
            required=True
        )
        Field3.bind(focus=error_3)

        Field4 = MDTextField(
            hint_text="Description",
            pos_hint={"x": 0.05, "y": 0.6},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=50,
        )

        Field5 = MDTextField(
            hint_text="List Price",
            pos_hint={"x": 0.05, "y": 0.5},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True
        )
        Field5.bind(focus=error_5)
        Field6 = MDTextField(
            hint_text="Quantity",
            pos_hint={"x": 0.05, "y": 0.4},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
        )
        Field6.bind(focus=error_6)

        Field7 = MDTextField(
            hint_text="Warehouse",
            pos_hint={"x": 0.05, "y": 0.3},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
            error=True
        )
        menu7 = MDDropdownMenu(
            caller=Field7,
            items=menu_items_7,
            width_mult=4
        )
        Field7.bind(focus=on_focus)

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def new(instance):
            print(f'INSERT INTO product VALUES ({Field1.text},'
                  f'{cat_dict.get(Field2.text)},\'{Field3.text}\',\'{Field4.text if Field4.text != "" else "null"}\','
                  f'{Field5.text},{Field6.text},'
                  f'{war_dict.get(Field7.text)})')
            SQL.query(f'INSERT INTO product VALUES ({Field1.text},'
                      f'{cat_dict.get(Field2.text)},\'{Field3.text}\',\'{Field4.text if Field4.text != "" else "null"}\','
                      f'{Field5.text},{Field6.text},'
                      f'{war_dict.get(Field7.text)})')
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
        screen.add_widget(Field5)
        screen.add_widget(Field6)
        screen.add_widget(Field7)
        screen.add_widget(But1)
        screen.add_widget(But2)
        return screen


if __name__ == "__main__":
    Product().run()
