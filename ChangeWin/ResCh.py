from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivymd.uix.pickers import MDDatePicker
import SQL

BTN_SIZE = (.14, .1)


class Research(MDApp):

    def build(self):

        def menu_callback(text_item):
            Field5.text = text_item
            Field5.error = False
            menu.dismiss()
            validate()

        screen = FloatLayout()

        with open('data.txt', 'r') as file:
            data = (file.read().replace('\"', '')[:-1].split(sep='!'))

        print(f'{data}')

        pk_list = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Research_Name from research')]

        status = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Status_Name from order_status')]
        status_id = [el[0] for el in SQL.query(SQL.my_cursor, 'SELECT Status_ID from order_status')]
        status_dict = {status[i]: status_id[i] for i in range(len(status_id))}

        menu_items = [
            {
                "text": data,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=data: menu_callback(x),
                'height': dp(64)
            } for data in status
        ]

        def save(inst, value, date_range):
            Field2.text = str(value)
            Field2.error = False
            validate()

        def show_date():
            date_dialog = MDDatePicker(year=2020, month=1, day=1)
            date_dialog.bind(on_save=save)
            date_dialog.open()

        def on_focus(inst, value):
            if value:
                if inst == Field5:
                    menu.open()
                if inst == Field2:
                    show_date()

        def validate():

            But2.disabled = Field1.error or Field3.error or Field4.error or Field2.error or Field5.error
            print(f'{But2.disabled} BUTTON')

        def error_1(instance, value):
            Field1.error = False
            if Field1.text != "":
                if Field1.text in pk_list:
                    Field1.helper_text = 'That Research already exists'
                    Field1.error = True
            else:
                Field1.error = True
            validate()

        def error_3(instance, value):
            Field3.error = False
            if Field3.text == "": Field3.error = True
            validate()

        def error_4(instance, value):
            Field4.error = False
            if Field4.text != "":
                try:
                    float(Field4.text)
                except:
                    Field4.helper_text = 'Budget should be decimal'
                    Field4.error = True
            else:
                Field4.error = True
            validate()

        Field1 = MDTextField(
            hint_text="Research Name",
            text=data[0],
            pos_hint={"x": 0.05, "y": 0.9},
            size_hint={0.6, 0.05},
            multiline=False,
            required=True,
            helper_text_mode='on_error',
            max_text_length=200,
            disabled=True
        )
        Field1.bind(focus=error_1)

        Field2 = MDTextField(
            hint_text='Select Date',
            text=data[1],
            pos_hint={"x": 0.05, "y": 0.8},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
        )
        Field2.bind(focus=on_focus)

        Field3 = MDTextField(
            hint_text="Synopsis",
            text=data[2],
            pos_hint={"x": 0.05, "y": 0.7},
            size_hint={0.6, 0.05},
            required=True,
            max_text_length=200
        )
        Field3.bind(focus=error_3)

        Field4 = MDTextField(
            hint_text='Budget',
            text=data[3],
            pos_hint={"x": 0.05, "y": 0.6},
            size_hint={0.6, 0.05},
            required=True,
            max_text_length=19
        )
        Field4.bind(focus=error_4)

        f5 = [k for k, v in status_dict.items() if v == data[4]]
        Field5 = MDTextField(
            hint_text="Status",
            text=f5[0],
            pos_hint={"x": 0.05, "y": 0.5},
            size_hint={0.6, 0.05},
            required=True,
            multiline=False,
        )
        menu = MDDropdownMenu(
            caller=Field5,
            items=menu_items,
            width_mult=4
        )
        Field5.bind(focus=on_focus)

        def close_app(self):
            MDApp.get_running_app().stop()

        But1 = MDRaisedButton(
            text='Закрыть окно',
            size_hint=BTN_SIZE,
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=close_app
        )

        def delete(instance):

            SQL.query(SQL.my_cursor, f'DELETE from research WHERE Research_Name = \'{Field1.text}\'')
            SQL.mydb.commit()
            MDApp.get_running_app().stop()

        def new(instance):
            print(f'UPDATE research SET '
                                     f'Date = \'{Field2.text}\','
                                     f'Synopsis = \'{Field3.text}\','
                                     f'Budget = {Field4.text},'
                                     f'Status_ID = {status_dict.get(Field5.text)}'
                                     f' WHERE Research_Name = {Field1.text}')
            SQL.query(SQL.my_cursor, f'UPDATE research SET '
                                     f'Date = \'{Field2.text}\','
                                     f'Synopsis = \'{Field3.text}\','
                                     f'Budget = {Field4.text},'
                                     f'Status_ID = {status_dict.get(Field5.text)}'
                                     f' WHERE Research_Name = \'{Field1.text}\'')
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
        screen.add_widget(Field4)
        screen.add_widget(Field5)
        screen.add_widget(But1)
        screen.add_widget(But2)
        screen.add_widget(But3)
        return screen


if __name__ == "__main__":
    Research().run()
