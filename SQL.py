import mysql.connector

from config import host, user, password, db_name

mydb = mysql.connector.Connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    db=db_name
)

my_cursor = mydb.cursor()


def update_bd():
    mydb = mysql.connector.Connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        db=db_name
    )


def query(cursor, data):
    cursor.execute(data)
    result = cursor.fetchall()
    return result


if __name__ == '__main__':
    res = (query(my_cursor, "show tables"))
    print(res)
    newRes = tuple(el[0] for el in res)
