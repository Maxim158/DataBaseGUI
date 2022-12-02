from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
import SQL

BTN_SIZE = (.14, .1)


class Employee(MDApp):

    def build(self):
        screen = FloatLayout()

        pk_list = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Employee_ID from employee')]
        dep_list = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Department_ID from department')]
        print(dep_list)

        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)

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

        def error_2(instance, value):
            Field2.error = False
            try:
                int(Field2.text)
                if int(Field2.text) not in dep_list:
                    Field2.helper_text = 'That Department ID doesnt exist'
                    Field2.error = True
            except ValueError:
                Field2.error = True
                Field2.helper_text = 'Department ID must be INT'
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
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=64,
        )
        Field1.bind(focus=error_1)

        Field2 = MDTextField(
            hint_text="Department ID",
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            multiline=False,
            helper_text_mode='on_error',
            max_text_length=64,
            required=True
        )
        Field2.bind(focus=error_2)

        Field3 = MDTextField(
            hint_text="First Name",
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=20,
            required=True
        )
        Field3.bind(focus=error_3)

        Field4 = MDTextField(
            hint_text="Last Name",
            pos_hint={"x": 0.05, "y": 0.6},
            size_hint={0.6, 0.05},
            multiline=False,
            max_text_length=20,
        )
        Field4.bind(focus=error_4)

        Field5 = MDTextField(
            hint_text="Phone Number",
            pos_hint={"x": 0.05, "y": 0.5},
            size_hint={0.6, 0.05},
            multiline=False,
        )

        Field6 = MDTextField(
            hint_text="Balance",
            pos_hint={"x": 0.05, "y": 0.4},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
        )
        Field6.bind(focus=error_6)

        Field7 = MDTextField(
            hint_text="Salaray",
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
            pass
            # SQL.query(SQL.my_cursor, f'INSERT INTO employee VALUES ({Field1.text if Field1.text != "" else "null"},'
            #                          f'{Field2.text},\'{Field3.text}\',\'{Field4.text}\','
            #                          f'\'{Field5.text}\',{Field6.text},'
            #                          f'{Field7.text})')
            # SQL.mydb.commit()
            # MDApp.get_running_app().stop()

        But2 = MDRaisedButton(
            text='Изменить',
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
    Employee().run()
