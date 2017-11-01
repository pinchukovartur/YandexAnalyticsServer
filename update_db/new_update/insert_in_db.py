# standard lib
import json
# download lib
import mysql.connector
# my lib
from utils.slack_util import send_message_in_slack, SLACK_GREEN, SLACK_RED
from const import *
from utils.console_util import print_progressbar

"""
Скрипт отвечает за добавления в базу
"""

count_entity = 0
count_queries = 0


def __create_queries__(list_entity, table_name):
    """
    Метод создает лист с запросами в БД
    :param list_entity: лист всех данных
    :param table_name: название таблицы в БД
    :return: лист запросов
    """
    # создаваемый лист запросов
    list_queries = list()
    # пока не переберем все входные данные
    while len(list_entity) != 0:
        # начало запроса
        query = "INSERT INTO analytics." + table_name + " ("
        # добавление в запрос название столбцов
        for key in list_entity[0].keys():
            query = query + key + ", "
        # убираем запятую в конце и добавляем атрибут values
        query = query[0:-2]
        query = query + ") VALUES ("
        # перебераем все сущности в листе
        tmp_list = list_entity.copy()
        for entity in list_entity:
            # перебераем все значения сущности
            for key in entity.keys():
                query = query + __check_value__(entity[key]) + ", "
            # удаляем заятую в конце и добавляем скопку для новой сущности
            query = query[0:-2]
            query = query + "), ("
            tmp_list.remove(entity)
            # если превышает максимальный размер запроса, отдеяем его и начинаем создание нового
            if len(query) > MAX_SIZE_QUERY:
                break

        list_entity = tmp_list.copy()
        # завершающие штрихи создания запроса
        query = query[0: -3]
        query = query + ";"
        list_queries.append(query)
    return list_queries


def __check_value__(str_val):
    """
    Метод проверяет дату на валидность
    :param str_val: дата
    :return: валидная дата
    """
    str_val = str(str_val).replace('"', "'")

    if str(str_val) == "0000-00-00 00:00:00":
        return '"0001-01-01 00:00:00"'
    if str(str_val) is "":
        return '""'
    return '"' + str(str_val) + '"'


def add(table_name, list_path_for_json_events_files):
    global count_entity
    global count_queries
    i = 0
    for path in list_path_for_json_events_files:

        f = open(path, encoding="utf-8-sig")
        str_json = f.read().replace("\n", "")
        events_later_data = json.loads(str_json, encoding="utf-8")
        list_data = list(events_later_data["data"])

        count_entity = len(list_data) + count_entity
        if len(list_data) != 0:
            queries = __create_queries__(list_data, table_name)
            for query in queries:
                __insert__(query)
                count_queries = count_queries + 1

        print_progressbar(i, len(list_path_for_json_events_files), prefix='Insert ' + table_name + ':',
                          suffix='Inserts: '+str(count_entity) + " query: " + str(count_queries), length=50)
        i += 1

    send_message_in_slack(SLACK_URL, SLACK_CHANEL, "Insert in DB finished", "добавленно " + table_name +
                          ": " + str(count_entity) + "\nзапросов было отправленно: " + str(count_queries),
                          SLACK_USERNAME, SLACK_ICON, SLACK_GREEN)

    print("добавленно " + table_name + ": " + str(count_entity))
    print("запросов было отправленно: " + str(count_queries))
    count_entity = 0
    count_queries = 0
    print("-------------FINISH-------------")


def __insert__(query):
    """
    Метод подключается к БД и делает insert
    :param query: insert query
    :return: null
    """
    cnx = mysql.connector.connect(user='root', database='analytics', password="root")
    cursor = cnx.cursor()
    try:
        cursor.execute(query)
        # Make sure data is committed to the database
        cnx.commit()
    except Exception as mysql_error:
        print(query)
        print(mysql_error)
        send_message_in_slack(SLACK_URL, SLACK_CHANEL, "MySQL Error!! Need restore DB!", str(mysql_error),
                              SLACK_USERNAME, SLACK_ICON, SLACK_RED)
        exit(1) ###################### NEED CREATE RESTORE DB
    finally:
        cursor.close()
        cnx.close()
