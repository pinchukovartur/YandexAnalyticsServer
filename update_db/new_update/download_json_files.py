# standard lib
import time
import os
# download lib
from requests import get
# my lib
from utils.slack_util import send_message_in_slack, SLACK_RED
from const import *
from utils.console_util import print_progressbar

"""
Данный скрипт отвечает за загрузку файлов с яндекса
"""


def __sen_request__(request_str):
    """
    Метод отправляет запрос в ядекс, пока тот не ответит положительно
    :param request_str: запрос в яндекс
    :return: данные аналитики
    """
    while True:
        try:
            response = get(request_str)
            if response.status_code == 200:
                return response
            if response.status_code == 202:
                time.sleep(TIME_SLEEP)
            else:
                print(response.text)
                send_message_in_slack(SLACK_URL, SLACK_CHANEL, "Error download json from yandex",
                                      str(response.text), SLACK_USERNAME, SLACK_ICON, SLACK_RED)
                time.sleep(TIME_SLEEP)
        except Exception as error:
            print(error)
            send_message_in_slack(SLACK_URL, SLACK_CHANEL, "Error download json from yandex",
                                  str(error), SLACK_USERNAME, SLACK_ICON, SLACK_RED)
            time.sleep(TIME_SLEEP)


def get_list_json_files(file_name, request_str):
    """
    Метод получает данные с яндекса и сохраняет в файд
    :param file_name: название для файла
    :param request_str: текст запроса в яндекс
    :return: лист с названием файлов
    """
    list_files_name = list()
    for i in range(COUNT_PACK):
        response = __sen_request__(request_str + "&parts_count=" + str(COUNT_PACK)
                                   + "&part_number=" + str(i) + "&oauth_token=" + TOKEN)
        # save to file
        tmp_folder = os.path.dirname(os.path.realpath(__file__)) + "/tmp/"
        if __check_tmp_folder__(tmp_folder):
            f = open(tmp_folder + file_name + str(i) + ".json", "wb")
            f.write(response.text.encode(encoding='utf_8_sig', errors='strict'))
            f.close()

            # add the path to the json file in the sheet
            list_files_name.append(tmp_folder + "/" + file_name + str(i) + ".json")

            print_progressbar(i+1, COUNT_PACK, prefix='Download ' + file_name + ':',
                              suffix='Downloaded files: ' + str(i+1), length=50)
        else:
            raise NameError("tmp folder not exist! check path - " + str(tmp_folder))

    return list_files_name


def __check_tmp_folder__(tmp_path):
    """
    Метод провеяет, существуели папка для скачиания
    :param tmp_path: путь к папке
    :return: True если есть и False если нет
    """
    if os.path.isdir(tmp_path):
        return True
    else:
        return False
