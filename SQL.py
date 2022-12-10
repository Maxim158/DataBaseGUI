import mysql.connector

from config import host, user, password, db_name


def query(data):
    mydb = mysql.connector.Connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        db=db_name
    )

    my_cursor = mydb.cursor()

    my_cursor.execute(data)
    result = my_cursor.fetchall()
    if data.split()[0] in ('INSERT', 'DELETE'):
        mydb.commit()
    my_cursor.close()
    mydb.close()
    return result


if __name__ == '__main__':
    res = (query("show tables"))
    print(res)
    newRes = tuple(el[0] for el in res)
