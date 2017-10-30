import os
import datetime
import mysql.connector

"""
Данный скрипт отвечает за получение данных с базы и настроки остальныых скриптов
"""

# STATIC DATA
TOKEN = "AQAAAAATpP0XAAR70vxUpgjrAkq_h3IGIcgKL-0"
# time between requests in yandex to check if the package is ready
TIME_SLEEP = 10
# number of packets to which data is divided
COUNT_PACK = 1000
SERVER_HOST = "http://localhost:8080"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "analytics"
DB_HOST = "localhost"
__dir_project__ = os.path.dirname(os.path.realpath(__file__))
TMP_FOLDER_FOR_JSON_FILES = __dir_project__ + "/tmp/"

max_size = 35000  # максимальный размер запроса (в символах)


def get_max_datetime(table, column):
    """
    Метод возвращает максимальную дату в таблице
    :param table: название талицы
    :param column: название колонки с датой
    :return: максимальная дата
    """
    query = "SELECT max(" + table + "." + column + ") FROM analytics." + table + ";"

    cnx = mysql.connector.connect(user='root', database='analytics', password="root")
    cursor = cnx.cursor()
    date = ""
    try:
        cursor.execute(query)

        for datetime in cursor:
            date = datetime[0]

    except Exception as mysql_error:
        print(query)
        print(mysql_error)
        exit(1)
    finally:
        cursor.close()
        cnx.close()

    if date is not None:
        return str(date)
    else:
        return "2012-01-01 00:00:00"


# MAX DATE IN DB
today = datetime.datetime.today()
last_download_events = datetime.datetime.strptime(get_max_datetime("events", "event_datetime"), '%Y-%m-%d %H:%M:%S')
last_download_errors = datetime.datetime.strptime(get_max_datetime("errors", "error_datetime"), '%Y-%m-%d %H:%M:%S')
last_download_installations = datetime.datetime.strptime(get_max_datetime("installations", "install_datetime"),
                                                         '%Y-%m-%d %H:%M:%S')
last_download_crashes = datetime.datetime.strptime(get_max_datetime("crashes", "crash_datetime"), '%Y-%m-%d %H:%M:%S')


def check_data(value):
    """
    Метод добавляет нолик в цифрам, так как яндекс принимает только двоичные значения в дате
    :param value: значения даты
    :return: двоичное значение
    """
    if int(value) < 10:
        return "0" + str(value)
    else:
        return str(value)


# DATE IN REQUEST
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

# REQUESTS
REQUEST_INSTALLS = "https://api.appmetrica.yandex.ru/logs/v1/export/installations.json?application_id=176450" \
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
REQUEST_ERRORS = "https://api.appmetrica.yandex.ru/logs/v1/export/errors.json?application_id=176450" \
                 "" \
                 "&date_since=" + DATA_START_ERROR + "&date_until=" + DATA_END + \
                 "" \
                 "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%" \
                 "2Cwindows_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_type%2Cdevice_" \
                 "locale%2Capp_version_name%2Capp_package_name%2Cerror%2Cerror_id%2Cerror_datetime%2Cerror_timestam" \
                 "p%2Cerror_receive_datetime%2Cerror_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%" \
                 "2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"
REQUEST_CRASHES = "https://api.appmetrica.yandex.ru/logs/v1/export/crashes.json?application_id=176450" \
                  "" \
                  "&date_since=" + DATA_START_CRASHES + "&date_until=" + DATA_END + \
                  "" \
                  "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%2Cwind" \
                  "ows_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_type%2Cdevice_locale%" \
                  "2Capp_version_name%2Capp_package_name%2Ccrash%2Ccrash_id%2Ccrash_group_id%2Ccrash_datetime%2Ccrash_t" \
                  "imestamp%2Ccrash_receive_datetime%2Ccrash_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%" \
                  "2Cmnc%2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"

REQUEST_EVENTS = "https://api.appmetrica.yandex.ru/logs/v1/export/events.json?application_id=176450" \
                 "" \
                 "&date_since=" + DATA_START_EVENT + "&date_until=" + DATA_END + \
                 "" \
                 "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%" \
                 "2Cos_name%2Cos_version%2Cdevice_model%2Cdevice_manufacturer%2Cdevice_type%2Cdevice_locale%2" \
                 "Capp_version_name%2Capp_package_name%2Cevent_name%2Cevent_json%2Cevent_datetime%2Cevent_timestamp%" \
                 "2Cevent_receive_datetime%2Cevent_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%" \
                 "2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"
