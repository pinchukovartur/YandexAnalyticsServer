# -*- coding: utf-8 -*- 
# внешняя библиотека MySQLdb (pip install MySQL-python)
from MySQLdb import *

""" Скрипт который выводит количество установок с 'даты-1'  по 'дату-2'"""


# ---------------------------------------------------------------------
# Program by Pinchukov Artur
#
# Version     Data      Info
#  1.0     14.08.2017
# ---------------------------------------------------------------------

# Метод выполняющий select в MySQL БД
# user - имя пользователя в БД
# password - пароль пользователя БД
# host - адрес БД
# db - имя БД
# query - sql запрос
def select(user, password, host, db, query):
    connection = connect(user=user,
                         passwd=password,
                         host=host,
                         db=db)
    connection.query(query)
    result = connection.store_result()
    list_row = list(result.fetch_row(result.num_rows()))
    return list_row

# даты начала и конца
start_date = '2017-08-13 00:00:00'
end_date = '2017-08-15 00:00:00'


"""Тестовый запрос, который выводит все установки в заданное время """
query = "SELECT * FROM analytics.installations where installations.install_datetime > '"+start_date+"' and installations.install_datetime < '"+end_date+"';"

# Выполняем запрос
result = select("root", "root", "127.0.0.1", "analytics", query)

print("Количество записей - " + str(len(result)))
print("Результат:")
for row in result:
    print(row)