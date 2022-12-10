import json

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
import SQL

BTN_SIZE = (.14, .1)


class Employee(MDApp):

    def build(self):
        screen = FloatLayout()

        def menu_callback(text_item):
            Field2.text = text_item
            Field2.error = False
            menu.dismiss()
            validate()

        with open('data.txt','r') as file:
            data = (file.read().replace('\"', '')[:-1].split(sep='!'))

        print(f'{data}')
        pk_list = [el[0] for el in SQL.query('SELECT Employee_ID from employee')]
        dep_list = [el[0] for el in SQL.query('SELECT Department_Name from department')]
        dep_list_id = [el[0] for el in SQL.query('SELECT Department_ID from department')]
        dep_dict = {dep_list[i]: dep_list_id[i] for i in range(len(dep_list_id))}
        menu_items = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback(x),
                'height': dp(64)
            } for data in dep_list
        ]
        print(dep_list)

        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)

        def on_focus(inst, value):
            if value:
                menu.open()

        def validate():

            But2.disabled = Field1.error or Field2.error or Field3.error or \
                            Field4.error or Field5.error or Field6.error or Field7.error
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

        def error_3(instance, value):
            Field3.error = False
            if has_numbers(Field3.text):
                Field3.error = True
                Field3.helper_text = 'Name shouldn\'t contains numbers'
            validate()

        def error_4(instance, value):
            Field4.error = False
            if has_numbers(Field4.text):
                Field4.error = True
                Field4.helper_text = 'Name shouldn\'t contains numbers'
            validate()

        def error_6(instance, value):
            Field6.error = False
            try:
                float(Field6.text)
            except ValueError:
                Field6.error = True
                Field6.helper_text = 'Balance must be a number'
            validate()

        def error_7(instance, value):
            Field7.error = False
            try:
                float(Field7.text)
            except ValueError:
                Field7.error = True
                Field7.helper_text = 'Salary must be a number'
            validate()

        Field1 = MDTextField(
            hint_text="Employee ID (Есть функция автоувеличения)",
            text=data[0],
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=64,
            disabled=True
        )
        Field1.bind(focus=error_1)

        f2= [k for k, v in dep_dict.items() if v == int(data[1])]
        Field2 = MDTextField(
            hint_text="Department ID",
            text=f2[0],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=64,
            required=True
        )
        menu = MDDropdownMenu(
            caller=Field2,
            items=menu_items,
            width_mult=4
        )

        Field2.bind(focus=on_focus)

        Field3 = MDTextField(
            hint_text="First Name",
            text=data[2],
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=20,
            required=True
        )
        Field3.bind(focus=error_3)

        Field4 = MDTextField(
            hint_text="Last Name",
            text=data[3],
            pos_hint={"x": 0.05, "y": 0.6},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=20,
        )
        Field4.bind(focus=error_4)

        Field5 = MDTextField(
            hint_text="Phone Number",
            text=data[4],
            pos_hint={"x": 0.05, "y": 0.5},
            size_hint={0.6, 0.05},
            multiline=False,
        )

        Field6 = MDTextField(
            hint_text="Balance",
            text=data[5],
            pos_hint={"x": 0.05, "y": 0.4},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
        )
        Field6.bind(focus=error_6)

        Field7 = MDTextField(
            hint_text="Salaray",
            text=data[6],
            pos_hint={"x": 0.05, "y": 0.3},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True
        )
        Field7.bind(focus=error_7)

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def new(instance):
            print()
            SQL.query(f'UPDATE employee SET '
                                     f'Department_ID = {dep_dict.get(Field2.text)},'
                                     f'First_Name = \'{Field3.text}\','
                                     f'Last_Name = \'{Field4.text}\','
                                     f'Phone_Number = \'{Field5.text}\','
                                     f'Balance = {Field6.text},'
                                     f'Salary = {Field7.text}'
                                     f'WHERE employee_ID = {Field1.text}')
            
            MDApp.get_running_app().stop()

        def delete(instance):

            SQL.query(f'DELETE from employee WHERE employee_id = {Field1.text}')
            
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
        screen.add_widget(Field5)
        screen.add_widget(Field6)
        screen.add_widget(Field7)
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(But3)
        return screen


if __name__ == "__main__":
    Employee().run()
