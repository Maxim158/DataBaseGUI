from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
import SQL

BTN_SIZE = (.14, .1)


class Employee(MDApp):


    def build(self):


        screen = FloatLayout()


        res = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Research_Name from research')]
        res_in = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Research_Name from research_employee')]
        emp_id_in = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT employee_ID from research_employee')]
        pairs = [[res_in[i],emp_id_in[i]] for i in range(len(res_in))]
        print(pairs)
        emp_id = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT employee_ID from employee')]
        emp = [el[0]+' '+el[1] for el in SQL.query(SQL.my_cursor, 'SELECT First_Name,Last_Name from employee')]
        emp_dict = {emp[i]:emp_id[i] for i in range(len(emp_id))}
        print(emp_dict)


        def swap(inst):
            Error.text = ""

        Field1 = Spinner(
            text=res[0],
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            values=res
        )
        Field1.bind(on_release=swap)
        Field2 = Spinner(
            text=emp[0],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            values=emp
        )
        Field2.bind(on_release=swap)

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        Error = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error"
        )

        def new(instance):
            if [Field1.text, emp_dict.get(Field2.text)] in pairs:
                Error.text = "Данный сотрудник уже занимается этим исследованием"
            else:
                pass
                SQL.query(SQL.my_cursor, f'INSERT INTO research_employee VALUES (\'{Field1.text}\',{emp_dict.get(Field2.text)})')
                SQL.mydb.commit()
                MDApp.get_running_app().stop()

        But2 = MDRaisedButton(
            text='Добавить',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.81, "y": 0.05},
            on_release=new,
        )

        screen.add_widget(Field1)
        screen.add_widget(Field2)
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(Error)
        return screen


if __name__ == "__main__":
    Employee().run()
