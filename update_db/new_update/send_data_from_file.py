import os

import json
import mysql.connector
from script_data import *
from download_json_files import get_list_json_files

"""
Скрипт отвечает за добавления в базу
"""


count_entity = 0
count_queries = 0


def create_queries(list_entity, table_name):
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
                query = query + check_value(entity[key]) + ", "
            # удаляем заятую в конце и добавляем скопку для новой сущности
            query = query[0:-2]
            query = query + "), ("
            tmp_list.remove(entity)
            global max_size
            # если превышает максимальный размер запроса, отдеяем его и начинаем создание нового
            if len(query) > max_size:
                break

        list_entity = tmp_list.copy()
        # завершающие штрихи создания запроса
        query = query[0: -3]
        query = query + ";"
        list_queries.append(query)
    return list_queries


def add(name, list_path_for_json_events_files):
    global count_entity
    global count_queries

    for path in list_path_for_json_events_files:

        f = open(path, encoding="utf-8-sig")
        str_json = f.read().replace("\n", "")
        events_later_data = json.loads(str_json, encoding="utf-8")
        list_data = list(events_later_data["data"])

        count_entity = len(list_data) + count_entity
        if len(list_data) != 0:
            queries = create_queries(list_data, name)
            for query in queries:
                insert(query)
                count_queries = count_queries + 1

    print("добавленно " + name + ": " + str(count_entity))
    print("запросов было отправленно: " + str(count_queries))
    count_entity = 0
    count_queries = 0
    print("-------------FINISH-------------")


def check_value(str_val):
    str_val = str(str_val).replace('"', "'")

    if str(str_val) == "0000-00-00 00:00:00":
        return '"0001-01-01 00:00:00"'
    if str(str_val) is "":
        return '""'
    return '"' + str(str_val) + '"'


def insert(query):
    cnx = mysql.connector.connect(user='root', database='analytics', password="root")
    cursor = cnx.cursor()
    try:
        cursor.execute(query)
        # Make sure data is committed to the database
        cnx.commit()
    except Exception as mysql_error:
        print(query)
        print(mysql_error)
        exit(1)
    finally:
        cursor.close()
        cnx.close()


add("installations", get_list_json_files("installations", REQUEST_INSTALLS))
add("crashes", get_list_json_files("crashes", REQUEST_CRASHES))
add("events", get_list_json_files("events", REQUEST_EVENTS))
add("errors", get_list_json_files("errors", REQUEST_ERRORS))
