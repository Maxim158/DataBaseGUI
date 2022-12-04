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

        def menu_callback_1(text_item):
            Field1.text = text_item
            Field1.error = False
            menu1.dismiss()
            validate()

        def menu_callback_2(text_item):
            Field2.text = text_item
            Field2.error = False
            menu2.dismiss()
            validate()

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
        menu_items_1 = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback_1(x),
                'height': dp(64)
            } for data in res
        ]
        menu_items_2 = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback_2(x),
                'height': dp(64)
            } for data in emp
        ]

        def on_focus(inst, value):
            if value:
                if inst == Field1:
                    menu1.open()
                if inst == Field2:
                    menu2.open()

        def validate():

            if Field1.text != '' and Field2.text != "":
                But2.disabled =Field1.error or Field2.error or [Field1.text, emp_dict.get(Field2.text)] in pairs

                if But2.disabled:
                    Error.text="Данный сотрудник уже занимается этим исследованием"
                else:
                    Error.text=""
            else:
                But2.disabled = Field1.error or Field2.error


        Field1 = MDTextField(
            hint_text="Research",
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
            error=True
        )
        menu1 = MDDropdownMenu(
            caller=Field1,
            items=menu_items_1,
            width_mult=4
        )
        Field1.bind(focus=on_focus)
        Field2 = MDTextField(
            hint_text="Employee",
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
            theme_text_color="Error",
        )

        def new(instance):
                SQL.query(SQL.my_cursor, f'INSERT INTO research_employee VALUES (\'{Field1.text}\',{emp_dict.get(Field2.text)})')
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
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(Error)
        return screen


if __name__ == "__main__":
    ResEmp().run()
