import json

from kivy.config import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '600')
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivy.uix.spinner import Spinner
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.datatables import MDDataTable
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
import SQL
from SQL import *
from config import *
from subprocess import Popen

# Program credits
VERSION = '0.5.0'
BTN_SIZE = (.14, .1)


def get_columns(data):
    columns = []
    print(data)
    for row in data:
        columns.append([row[0], dp(40)])
    return columns


def get_rows(data):
    rows = []
    for row in data:
        rows.append(row)
    return rows


class MainApp(MDApp):
    CURRENT_TABLE = MAIN_TABLE
    CURRENT_ROW = ""
    PRIMARY_KEY = []
    SEEKING = ""
    EXACTLY = False
    WinDict = {
        'counter': "CounterWindow.py",
        'department': "DepartmentWindow.py",
        'employee': "EmployeeWindow.py",
        'order_data': "OrderDataWindow.py",
        'order_items': "OrderItemsWindow.py",
        'order_status': "OrderStatusWindow.py",
        'product_categories': "ProductCatWindow.py",
        'product': "ProductWindow.py",
        'research': "ResearchWindow.py",
        'research_employee': "ResEmpWin.py",
        'research_status': "ResStatusWin.py",
        'warehouse': "WarehouseWindow.py",
    }
    WinCh = {
        'counter': "CtrCh.py",
        'department': "DepCh.py",
        'employee': "EmpCh.py",
        'order_data': "DataCh.py",
        'order_items': "ItemsCh.py",
        'order_status': "OrSCh.py",
        'product_categories': "PrCatCh.py",
        'product': "PrCh.py",
        'research': "ResCh.py",
        'research_employee': "ResEmpCh.py",
        'research_status': "ResStCh.py",
        'warehouse': "WarCh.py",
    }

    def delete_table(self, screen):
        for child in screen.children:
            if type(child) == type(MDDataTable()):
                screen.remove_widget(child)

    def build(self):
        # Define Screen
        screen = FloatLayout()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_pallete = "BlueGray"

        # Define Table
        table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(.9, 0.6),
            use_pagination=True,
            column_data=get_columns(SQL.query(describe + MAIN_TABLE)),
            row_data=get_rows(SQL.query(select_all + MAIN_TABLE)),
        )

        table.bind(on_check_press=self.checked)
        table.bind(on_row_press=self.row_checked)

        def Adding(instance):
            print('Pressed')
            Win = self.WinDict[TablesList.text]
            p = Popen(f'Windows\{Win}', shell=True)

        Add = Button(text='????????????????',
                     size_hint=BTN_SIZE,
                     pos_hint={'x': 0.025, 'y': 0.025},
                     on_press=Adding)

        def find(instance):
            if SortingList.text != "???????????????? ????????" and self.CURRENT_TABLE != "Procedure":
                self.SEEKING = Input.text
                print('Find')
                self.delete_table(screen)
                like = f'{select_all} {self.CURRENT_TABLE} WHERE {self.CURRENT_ROW} LIKE \'%{self.SEEKING}%\''
                where = f'{select_all} {self.CURRENT_TABLE} WHERE {self.CURRENT_ROW} = \'{self.SEEKING}\''
                print(like)
                print(where)
                table = MDDataTable(
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    size_hint=(.9, 0.6),
                    use_pagination=True,
                    column_data=get_columns(SQL.query(describe + self.CURRENT_TABLE)),
                    row_data=get_rows(SQL.query(where if self.EXACTLY else like))
                )
                table.bind(on_check_press=self.checked)
                table.bind(on_row_press=self.row_checked)
                screen.add_widget(table)

        Sort = Button(text='??????????',
                      size_hint=BTN_SIZE,
                      pos_hint={'x': 0.7, 'y': 0.85},
                      on_press=find)

        TablesList = Spinner(text=MAIN_TABLE,
                             values=tuple(el[0] for el in query("show tables")),
                             size_hint=BTN_SIZE,
                             background_color=[144 / 255, 212 / 255, 107 / 255, 0.7],
                             pos_hint={'x': 0.025, 'y': 0.85})

        SortingList = Spinner(text="???????????????? ????????",
                              values=tuple(
                                  el[0] for el in get_columns(query(describe + self.CURRENT_TABLE))),
                              size_hint=BTN_SIZE,
                              background_color=[144 / 255, 212 / 255, 107 / 255, 0.7],
                              pos_hint={'x': 0.85, 'y': 0.85}
                              )
        Input = MDTextField(
            hint_text="?????????????? ?????????????????? ????????????????????",
            multiline=False,
            size_hint=(.25, .05),
            pos_hint={'x': 0.2, 'y': 0.83}
        )

        def on_check(checkbox, value):
            if value:
                self.EXACTLY = True
            else:
                self.EXACTLY = False

        exact = CheckBox(
            pos_hint={'x': 0.6, 'y': 0.86},
            size_hint=(.1, .05),
            color=[0, 0, 0, 1],
        )
        exact.bind(active=on_check)
        exact_label = MDLabel(
            text="???????????? ????????????????????",
            size_hint=(.08, .05),
            pos_hint={'x': 0.62, 'y': 0.91}
        )

        def update(instance):
            self.delete_table(screen)
            table = MDDataTable(
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(.9, 0.6),
                use_pagination=True,
                column_data=get_columns(SQL.query(describe + self.CURRENT_TABLE)),
                row_data=get_rows(SQL.query(select_all + self.CURRENT_TABLE))
            )
            get_data = SQL.query(f'SELECT * FROM employee')
            for i in range(len(get_data)):
                print(get_data[i])
            table.bind(on_check_press=self.checked)
            table.bind(on_row_press=self.row_checked)
            screen.add_widget(table)

        update = Button(text='????????????????',
                        size_hint=BTN_SIZE,
                        pos_hint={'x': 0.85, 'y': 0.025},
                        background_color=[0, 0, 1, .5],
                        on_press=update)

        def procedure(inst):
            qr = SQL.query("call GetSalaryDetail")
            self.CURRENT_TABLE = "Procedure"
            self.delete_table(screen)
            SortingList.text = "???????????????? ????????"
            table = MDDataTable(
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(.9, 0.6),
                use_pagination=True,
                column_data=[
                    ("Name", dp(64)),
                    ("LEVEL", dp(64)),
                ],
                row_data=get_rows(qr)
            )
            table.bind(on_check_press=self.checked)
            table.bind(on_row_press=self.row_checked)
            SortingList.values = tuple(["Name", "LEVEL"])
            screen.add_widget(table)

        proc = Button(text='??????????????????',
                        size_hint=BTN_SIZE,
                        pos_hint={'x': 0.25, 'y': 0.025},
                        on_press=procedure)

        def on_focus(instance, value):
            if value:
                print('User Focused')
            else:
                print('User Unfocused')

        Input.bind(focus=on_focus)

        def change_table(spinner, text):
            self.CURRENT_TABLE = TablesList.text
            print('Change Table', spinner, 'has text', text)
            self.delete_table(screen)
            SortingList.text = "???????????????? ????????"
            table = MDDataTable(
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(.9, 0.6),
                use_pagination=True,
                column_data=get_columns(SQL.query(describe + self.CURRENT_TABLE)),
                row_data=get_rows(SQL.query(select_all + self.CURRENT_TABLE))
            )
            table.bind(on_check_press=self.checked)
            table.bind(on_row_press=self.row_checked)
            SortingList.values = tuple(el[0] for el in get_columns(query(describe + self.CURRENT_TABLE)))
            screen.add_widget(table)

        def sorting_row(spinner, text):
            self.CURRENT_ROW = SortingList.text
            print('Sorting table', spinner, 'has text', text)

        TablesList.bind(text=change_table)
        SortingList.bind(text=sorting_row)

        version = MDLabel(text=f"version {VERSION}",
                          theme_text_color="Hint",
                          pos_hint={'x': 0.92, 'y': -0.49})

        screen.add_widget(TablesList)
        screen.add_widget(proc)
        screen.add_widget(table)
        screen.add_widget(Add)
        screen.add_widget(Sort)
        screen.add_widget(Input)
        screen.add_widget(SortingList)
        screen.add_widget(version)
        screen.add_widget(update)
        screen.add_widget(exact)
        screen.add_widget(exact_label)
        return screen

    def checked(self, instance_table, current_row):
        print('Checked')
        print(instance_table, current_row)
        # Function for row presses

    def row_checked(self, table, row):
        print('Selected Row')
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        data = str()
        for i in range(start_index, end_index + 1):
            data = data + (row.table.recycle_data[i]["text"]) + '!'
        with open('data.txt', 'w') as file:
            file.write(json.dumps(data))
        Win = self.WinCh[self.CURRENT_TABLE]
        p = Popen(f'ChangeWin\{Win}', shell=True)


if __name__ == '__main__':
    MainApp().run()
