import datetime
import os
import time

from requests import *  # install lib

from analytics_сontroller import AnalyticsController
from scripts.dao.analytics_dao import AnalyticsDB


def clear_log():
    log_file = open(os.path.dirname(__file__) + "/log.txt", "w")
    log_file.close()
    log_file = open(os.path.dirname(__file__) + "/err.txt", "w")
    log_file.close()


# open log file
def write_log(log):
    log_file = open(os.path.dirname(__file__) + "/log.txt", "a")
    log_file.write(log + "\n")
    log_file.close()

try:
    # СТАТИЧЕСКИЕ ДАННЫЕ
    TOKEN = "AQAAAAATpP0XAAR70vxUpgjrAkq_h3IGIcgKL-0"
    TIME_SLEEP = 10  # время между запросвми в яндекс для проверки о готовности пакета
    COUNT_PACK = 1000  # количесвто пакетов, на которые разбиваются данные
    SERVER_HOST = "http://192.168.88.225:8080"
    # ДАННЫЕ
    # текущая дата
    today = datetime.datetime.today()
    # папка для хранения файлов
    tmp_folder_path = os.path.dirname(__file__) + "/tmp/"
    # класс для работы с БД (лежит в папках scripts/dao)
    analytics_db = AnalyticsDB("root", "root", "127.0.0.1")
    # максимальные даты в таблицах, берется из БД
    last_download_events = datetime.datetime.strptime(analytics_db.get_max_event_datetime(), '%Y-%m-%d %H:%M:%S')
    last_download_errors = datetime.datetime.strptime(analytics_db.get_max_errors_datetime(), '%Y-%m-%d %H:%M:%S')
    last_download_installations = datetime.datetime.strptime(analytics_db.get_max_installation_datetime(),
                                                             '%Y-%m-%d %H:%M:%S')
    last_download_crashes = datetime.datetime.strptime(analytics_db.get_max_crashes_datetime(), '%Y-%m-%d %H:%M:%S')
    # контролер для парсинга json файлов и отправка их в бд, методы приниают лист с путями до json файлов
    analytics_controller = AnalyticsController(analytics_db)

    # метод спрашивает у сервиса разрешение на обновление
    def get_root():
        try:
            p = get(SERVER_HOST + "/start_download/start")
            if p.text == "you can download":
                write_log("you can download")
            else:
                write_log(p.text)
                time.sleep(5)
                get_root()
        except Exception as e:
            write_log(str(e))
            exit(1)

    # метод добавлет нолик в начало даты, если она меньше 10 т к яндекс не кушает дату с одним значением
    def check_data(value):
        if int(value) < 10:
            return "0" + str(value)
        else:
            return str(value)


    # выполняем запрос пока не получим хороший ответ
    def sen_request(request_str):
        while True:
            try:
                response = get(request_str)
                if response.status_code == 200:
                    write_log(str(response.status_code))
                    return response
                else:
                    write_log(str(response.status_code))
            except Exception as error:
                write_log(str(error))
            time.sleep(TIME_SLEEP)


    def get_list_json_files(file_name, request_str):
        list_files_name = list()
        for i in range(COUNT_PACK):
            write_log("номер части пакета - " + str(i + 1) + " - " + str(file_name))
            response = sen_request(request_str + "&parts_count=" + str(COUNT_PACK)
                                   + "&part_number=" + str(i) + "&oauth_token=" + TOKEN)
            # сохраняем в файл
            f = open(tmp_folder_path + file_name + str(i) + ".json", "wb")
            f.write(response.text.encode(encoding='utf_8_sig', errors='strict'))
            f.close()
            # добавляем путь до json файла в лист
            list_files_name.append(tmp_folder_path + "/" + file_name + str(i) + ".json")

        return list_files_name

    # clear log file
    clear_log()

    # get permission to download
    get_root()

    DATA_START_EVENT = str(last_download_events.date()) + "%20" + check_data(
        last_download_events.hour) + "%3A" + check_data(last_download_events.minute) + "%3A" + check_data(
        last_download_events.second)
    DATA_START_ERROR = str(last_download_errors.date()) + "%20" + check_data(
        last_download_errors.hour) + "%3A" + check_data(last_download_errors.minute) + "%3A" + check_data(
        last_download_errors.second)
    DATA_START_INSTALLATIONS = str(last_download_installations.date()) + "%20" + check_data(
        last_download_installations.hour) + "%3A" + check_data(last_download_installations.minute) + "%3A" + check_data(
        last_download_installations.second)
    DATA_START_CRASHES = str(last_download_crashes.date()) + "%20" + check_data(
        last_download_crashes.hour) + "%3A" + check_data(last_download_crashes.minute) + "%3A" + check_data(
        last_download_crashes.second)
    DATA_END = str(today.date()) + "%20" + check_data(today.hour) + "%3A" + check_data(today.minute) + "%3A" + check_data(
        today.second)

    write_log("дата начала промежутка времени событий - " + str(last_download_events))
    write_log("дата начала промежутка времени ошибок - " + str(last_download_errors))
    write_log("дата начала промежутка времени установок - " + str(last_download_installations))
    write_log("дата начала промежутка времени крэшев - " + str(last_download_crashes))
    write_log("дата конца промежутка времени(общее)- " + str(today))

    # ЗАПРОСЫ В ЯНДЕКС
    request_installations = "https://api.appmetrica.yandex.ru/logs/v1/export/installations.json?application_id=176450" \
                            "" \
                            "&date_since=" + DATA_START_INSTALLATIONS + "&date_until=" + DATA_END + \
                            "" \
                            "&date_dimension=default&use_utf8_bom=true&fields=publisher_name%2Cpublisher_id%2Ctracker_name%2" \
                            "Ctracking_id%2Cclick_timestamp%2Cclick_datetime%2Cclick_ipv6%2Cclick_url_parameters%2Cclick_id%2" \
                            "Cclick_user_agent%2Cinstall_datetime%2Cmatch_type%2Cinstall_timestamp%2Cinstall_receive_datetime%" \
                            "2Cinstall_receive_timestamp%2Cinstall_ipv6%2Cis_reinstallation%2Cios_ifa%2Cios_ifv%2Candroid_id%" \
                            "2Cgoogle_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_locale%2Cdevice_" \
                            "type%2Capp_version_name%2Capp_package_name%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%2Ccountry_" \
                            "iso_code%2Ccity%2Cappmetrica_device_id"
    request_errors = "https://api.appmetrica.yandex.ru/logs/v1/export/errors.json?application_id=176450" \
                     "" \
                     "&date_since=" + DATA_START_ERROR + "&date_until=" + DATA_END + \
                     "" \
                     "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%" \
                     "2Cwindows_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_type%2Cdevice_" \
                     "locale%2Capp_version_name%2Capp_package_name%2Cerror%2Cerror_id%2Cerror_datetime%2Cerror_timestam" \
                     "p%2Cerror_receive_datetime%2Cerror_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%" \
                     "2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"
    request_crashes = "https://api.appmetrica.yandex.ru/logs/v1/export/crashes.json?application_id=176450" \
                  "" \
                  "&date_since=" + DATA_START_CRASHES + "&date_until=" + DATA_END + \
                  "" \
                  "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%2Cwind" \
                  "ows_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_type%2Cdevice_locale%" \
                  "2Capp_version_name%2Capp_package_name%2Ccrash%2Ccrash_id%2Ccrash_group_id%2Ccrash_datetime%2Ccrash_t" \
                  "imestamp%2Ccrash_receive_datetime%2Ccrash_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%" \
                  "2Cmnc%2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"

    request_events = "https://api.appmetrica.yandex.ru/logs/v1/export/events.json?application_id=176450" \
                      "" \
                      "&date_since=" + DATA_START_EVENT + "&date_until=" + DATA_END + \
                      "" \
                      "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%" \
                      "2Cos_name%2Cos_version%2Cdevice_model%2Cdevice_manufacturer%2Cdevice_type%2Cdevice_locale%2" \
                      "Capp_version_name%2Capp_package_name%2Cevent_name%2Cevent_json%2Cevent_datetime%2Cevent_timestamp%" \
                      "2Cevent_receive_datetime%2Cevent_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%" \
                      "2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"

    # отправляем лист контролеру для дальнейшего парсинга файлов и отправки в БД
    analytics_controller.add_installations(get_list_json_files("installations", request_installations))
    analytics_controller.add_errors(get_list_json_files("errors", request_errors))
    analytics_controller.add_crashes(get_list_json_files("crashes", request_crashes))
    analytics_controller.add_events(get_list_json_files("events", request_events))

    write_log("Скрипт начал свою работу в - " + str(today))
    write_log("Скрипт закончил свою работу в - " + str(datetime.datetime.today()))

    # set message about final update
    p = get(SERVER_HOST + "/start_download/ok")
except Exception as error:
    write_log(str(error))
