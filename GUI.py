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
from subprocess import Popen, PIPE, STDOUT

# Program credits
VERSION = '0.2.7'
BTN_SIZE = (.14, .1)


# get_rows(SQL.query(my_cursor, select_all + self.CURRENT_TABLE + ((" " + self.SEEKING) if self.SEEKING!="" else ''))))


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
    LIST_TO_DELETE = []
    PRIMARY_KEY = []
    SEEKING = ""
    EXACTLY = False

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
            column_data=get_columns(SQL.query(my_cursor, describe + MAIN_TABLE)),
            row_data=get_rows(SQL.query(my_cursor, select_all + MAIN_TABLE)),
        )

        table.bind(on_check_press=self.checked)
        table.bind(on_row_press=self.row_checked)

        def Adding(instance):
            print('Pressed')
            # SQL.query(my_cursor, 'INSERT INTO employee VALUES(110,1, "NAME", "", "", 1000,100)')
            p = Popen('Windows\EmployeeWindow.py', shell=True)

        Add = Button(text='Добавить',
                     size_hint=BTN_SIZE,
                     pos_hint={'x': 0.025, 'y': 0.025},
                     on_press=Adding)

        def Deleting(instance):
            print('Deleted')
            clmn = get_columns(query(my_cursor, describe + self.CURRENT_TABLE))
            for el in self.LIST_TO_DELETE:
                sql_query = ''
                for index in range(len(el)):
                    sql_query = sql_query + clmn[index][0] + '=\'' + el[index] + '\' and '
                sql_query = sql_query[:-5]
                print(delete + TablesList.text + ' WHERE ' + sql_query)
                query(my_cursor, delete + self.CURRENT_TABLE + ' WHERE ' + sql_query)
                self.delete_table(screen)
                print(select_all + self.CURRENT_TABLE + (
                    f" WHERE {self.CURRENT_ROW}=\'{self.SEEKING}\'" if self.SEEKING != "" else ''))
                table = MDDataTable(
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    size_hint=(.9, 0.6),
                    use_pagination=True,
                    column_data=get_columns(SQL.query(my_cursor, describe + self.CURRENT_TABLE)),
                    row_data=get_rows(SQL.query(my_cursor, select_all + self.CURRENT_TABLE + (
                        f" WHERE {self.CURRENT_ROW} LIKE \'%{self.SEEKING}%\'" if self.SEEKING != "" else ''))))
                self.LIST_TO_DELETE = []
                table.bind(on_check_press=self.checked)
                table.bind(on_row_press=self.row_checked)
                screen.add_widget(table)

        Delete = Button(text='Удалить Выбранные',
                        size_hint=BTN_SIZE,
                        pos_hint={'x': 0.2, 'y': 0.025},
                        on_press=Deleting)

        def find(instance):
            if SortingList.text != "Выберите ряд":
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
                    column_data=get_columns(SQL.query(my_cursor, describe + self.CURRENT_TABLE)),
                    row_data=get_rows(SQL.query(my_cursor, where if self.EXACTLY else like))
                )
                self.LIST_TO_DELETE = []
                table.bind(on_check_press=self.checked)
                table.bind(on_row_press=self.row_checked)
                screen.add_widget(table)

        Sort = Button(text='Поиск',
                      size_hint=BTN_SIZE,
                      pos_hint={'x': 0.7, 'y': 0.85},
                      on_press=find)

        TablesList = Spinner(text=MAIN_TABLE,
                             values=tuple(el[0] for el in query(my_cursor, "show tables")),
                             size_hint=BTN_SIZE,
                             background_color=[144 / 255, 212 / 255, 107 / 255, 0.7],
                             pos_hint={'x': 0.025, 'y': 0.85})

        SortingList = Spinner(text="Выберите ряд",
                              values=tuple(
                                  el[0] for el in get_columns(query(my_cursor, describe + self.CURRENT_TABLE))),
                              size_hint=BTN_SIZE,
                              background_color=[144 / 255, 212 / 255, 107 / 255, 0.7],
                              pos_hint={'x': 0.85, 'y': 0.85}
                              )
        Input = MDTextField(
            hint_text="Введите параметры сортировки",
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
            text="Точное совпадение",
            size_hint=(.1,.05),
            pos_hint={'x': 0.62, 'y': 0.91}
        )

        def comm(instance):
            mydb.commit()

        comm = Button(text='Подтвердить',
                      size_hint=BTN_SIZE,
                      pos_hint={'x': 0.85, 'y': 0.025},
                      background_color=[0, 0, 1, .5],
                      on_press=comm)

        def revert(instance):
            SQL.mydb.rollback()

        revert = Button(text='Отменить',
                        size_hint=BTN_SIZE,
                        pos_hint={'x': 0.7, 'y': 0.025},
                        background_color=[0, 0, 1, .5],
                        on_press=revert)

        def update(instance):
            self.delete_table(screen)
            newdb = mysql.connector.Connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        db=db_name
    )
            newcur = newdb.cursor()
            table = MDDataTable(
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(.9, 0.6),
                use_pagination=True,
                column_data=get_columns(SQL.query(newcur, describe + self.CURRENT_TABLE)),
                row_data=get_rows(SQL.query(newcur, select_all + self.CURRENT_TABLE))
            )
            get_data = SQL.query(my_cursor, f'SELECT * FROM employee')
            for i in range(len(get_data)):
                print(get_data[i])
            self.LIST_TO_DELETE = []
            table.bind(on_check_press=self.checked)
            table.bind(on_row_press=self.row_checked)
            screen.add_widget(table)

        update = Button(text='Обновить',
                        size_hint=BTN_SIZE,
                        pos_hint={'x': 0.55, 'y': 0.025},
                        background_color=[0, 0, 1, .5],
                        on_press=update)

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
            table = MDDataTable(
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(.9, 0.6),
                use_pagination=True,
                column_data=get_columns(SQL.query(my_cursor, describe + self.CURRENT_TABLE)),
                row_data=get_rows(SQL.query(my_cursor, select_all + self.CURRENT_TABLE))
            )
            self.LIST_TO_DELETE = []
            table.bind(on_check_press=self.checked)
            table.bind(on_row_press=self.row_checked)
            SortingList.values = tuple(el[0] for el in get_columns(query(my_cursor, describe + self.CURRENT_TABLE)))
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
        screen.add_widget(table)
        screen.add_widget(Add)
        # screen.add_widget(Delete)
        screen.add_widget(Sort)
        screen.add_widget(Input)
        screen.add_widget(SortingList)
        screen.add_widget(comm)
        screen.add_widget(version)
        screen.add_widget(revert)
        screen.add_widget(update)
        screen.add_widget(exact)
        screen.add_widget(exact_label)
        return screen

    def checked(self, instance_table, current_row):
        print('Checked')
        print(instance_table, current_row)
        self.LIST_TO_DELETE.append(current_row)
        print(self.LIST_TO_DELETE)
        # Function for row presses

    def row_checked(self, instance_table, instance_row):
        print('Selected Row')
        print(instance_table, instance_row)
        p = Popen('ChangeWin\EmpCh.py', shell=True)
        p.communicate(instance_row)


if __name__ == '__main__':
    MainApp().run()