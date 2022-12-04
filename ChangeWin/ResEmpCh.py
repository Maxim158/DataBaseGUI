from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
import SQL

BTN_SIZE = (.14, .1)


class ResEmp(MDApp):

    def build(self):
        screen = FloatLayout()

        with open('data.txt', 'r') as file:
            data = (file.read().replace('\"', '')[:-1].split(sep='!'))

        res_in = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Research_Name from research_employee')]
        emp_id_in = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT employee_ID from research_employee')]
        pairs = [[res_in[i], emp_id_in[i]] for i in range(len(res_in))]
        print(pairs)
        emp_id = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT employee_ID from employee')]
        emp = [el[0] + ' ' + el[1] for el in SQL.query(SQL.my_cursor, 'SELECT First_Name,Last_Name from employee')]
        emp_dict = {emp[i]: emp_id[i] for i in range(len(emp_id))}

        Field1 = MDTextField(
            hint_text="Research",
            text=data[0],
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
            disabled=True
        )

        f2 = [k for k, v in emp_dict.items() if v == int(data[1])]
        Field2 = MDTextField(
            hint_text="Employee",
            text=f2[0],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
            disabled=True
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
            print(f'DELETE from research_employee WHERE Research_Name = \'{Field1.text}\' '
                      f'and Employee_ID = {emp_dict.get(Field2.text)}')
            SQL.query(SQL.my_cursor,
                      f'DELETE from research_employee WHERE Research_Name = \'{Field1.text}\' '
                      f'and Employee_ID = {emp_dict.get(Field2.text)}')
            SQL.mydb.commit()
            MDApp.get_running_app().stop()

        But2 = MDRaisedButton(
            text='Изменить',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.81, "y": 0.05},
            disabled=True
        )

        But3 = MDRaisedButton(
            text='Удалить',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.61, "y": 0.05},
            on_release=delete,
        )

        screen.add_widget(Field1)
        screen.add_widget(Field2)
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(But3)
        return screen


if __name__ == "__main__":
    ResEmp().run()
