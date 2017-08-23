import json
# внешняя библиотека MySQLdb (pip install MySQL-python)
from MySQLdb import *
import time
""" Скрипт который выводит количесвто игроков, зашедших в игру после установки игры днем ранее и прошли туториал"""


# ---------------------------------------------------------------------
# Program by Pinchukov Artur
#
# Version     Data      Info
#  1.0     14.08.2017
# ---------------------------------------------------------------------

# создаем подключение
connection = connect(user="root",
                     passwd="root",
                     host="127.0.0.1",
                     db="analytics")

# даты начала и конца
start_date = '2017-08-13 00:00:00'
end_date = '2017-08-14 00:00:00'

"""Тестовый запрос, который выводит установки за один день """
install_query = "SELECT * FROM analytics.installations WHERE installations.install_datetime > '"+start_date+"' AND installations.install_datetime < '"+end_date+"';"

# выполням запрос в БД
connection.query(install_query)
result = connection.store_result()
installations = list(result.fetch_row(result.num_rows()))
print("Количество Installations - " + str(len(installations)))

# даты начала и конца события
start_date_event = '2017-08-14 00:00:00'
end_date_event = '2017-08-15 00:00:00'

event_query = "SELECT * FROM analytics.events where events.event_datetime > '"+start_date_event+"' and events.event_datetime < '"+end_date_event+"' and events.android_id = %s;"

count = 0
# Проверям, есть ли событья у игроков, которые установили игру днем ранее
for installation in installations:
    cursor = connection.cursor()
    # для начала получаем все события у девайся, который установил игру день назад
    # у листа installation под 1 индексом идет android_id
    result = cursor.execute(event_query, (installation[1],))
    # если количесвто событий больше нуля
    if result > 0:
        print("У устройства - " + str(installation[1]) + "  количесвто событий в следующий день - " + str(result))
        # получаем массив всех событий
        events = cursor.fetchall()
        for event in events:
            # получаем json в событии (в листе это идекс 13), парсем его
            dict_event = json.loads(event[13], encoding="utf-8")
            # если в json есть Tutorial07.04 и в нем Completed = 1 то добавляем 1 в счетчик
            if dict_event.get("Tutorial05.01") is not None:
                if dict_event["Tutorial05.01"]["Completed"] == '1':
                    count = count + 1


print("Количество игроков, прошедшие Tutorial07.04 - " + str(count))

time.sleep(360)

