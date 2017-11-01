import os
import datetime
import mysql.connector

"""
Данный скрипт отвечает за получение данных с базы
"""


def __get_max_datetime__(table, column):
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

        for date_time in cursor:
            date = date_time[0]

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


def __check_data__(value):
    """
    Метод добавляет нолик в цифрам, так как яндекс принимает только двоичные значения в дате
    :param value: значения даты
    :return: двоичное значение
    """
    if int(value) < 10:
        return "0" + str(value)
    else:
        return str(value)


def __get_end_date__():
    today = datetime.datetime.today()
    date_end = str(today.date()) + "%20" + __check_data__(today.hour) + "%3A" + __check_data__(
        today.minute) + "%3A" + __check_data__(today.second)
    return date_end


# CREATE REQUEST

def request_events():
    last_download_events = datetime.datetime.strptime(__get_max_datetime__("events", "event_datetime"),
                                                      '%Y-%m-%d %H:%M:%S')
    data_start_event = str(last_download_events.date()) + "%20" + __check_data__(
        last_download_events.hour) + "%3A" + __check_data__(last_download_events.minute) + "%3A" + __check_data__(
        last_download_events.second)

    request_events_str = "https://api.appmetrica.yandex.ru/logs/v1/export/events.json?application_id=176450" \
                         "" \
                         "&date_since=" + data_start_event + "&date_until=" + __get_end_date__() + \
                         "" \
                         "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%" \
                         "2Cos_name%2Cos_version%2Cdevice_model%2Cdevice_manufacturer%2Cdevice_type%2Cdevice_locale%2" \
                         "Capp_version_name%2Capp_package_name%2Cevent_name%2Cevent_json%2Cevent_datetime%2Cevent_timestamp%" \
                         "2Cevent_receive_datetime%2Cevent_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%" \
                         "2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"
    return request_events_str


def request_errors():
    last_download_errors = datetime.datetime.strptime(__get_max_datetime__("errors", "error_datetime"),
                                                      '%Y-%m-%d %H:%M:%S')
    date_start_error = str(last_download_errors.date()) + "%20" + __check_data__(
        last_download_errors.hour) + "%3A" + __check_data__(last_download_errors.minute) + "%3A" + __check_data__(
        last_download_errors.second)
    request_errors_str = "https://api.appmetrica.yandex.ru/logs/v1/export/errors.json?application_id=176450" \
                         "" \
                         "&date_since=" + date_start_error + "&date_until=" + __get_end_date__() + \
                         "" \
                         "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%" \
                         "2Cwindows_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_type%2Cdevice_" \
                         "locale%2Capp_version_name%2Capp_package_name%2Cerror%2Cerror_id%2Cerror_datetime%2Cerror_timestam" \
                         "p%2Cerror_receive_datetime%2Cerror_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%" \
                         "2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"
    return request_errors_str


def request_crashes():
    last_download_crashes = datetime.datetime.strptime(__get_max_datetime__("crashes", "crash_datetime"),
                                                       '%Y-%m-%d %H:%M:%S')
    date_start_crashes = str(last_download_crashes.date()) + "%20" + __check_data__(
        last_download_crashes.hour) + "%3A" + __check_data__(last_download_crashes.minute) + "%3A" + __check_data__(
        last_download_crashes.second)
    request_crashes_str = "https://api.appmetrica.yandex.ru/logs/v1/export/crashes.json?application_id=176450" \
                          "" \
                          "&date_since=" + date_start_crashes + "&date_until=" + __get_end_date__() + \
                          "" \
                          "&date_dimension=default&use_utf8_bom=true&fields=ios_ifa%2Cios_ifv%2Candroid_id%2Cgoogle_aid%2Cwind" \
                          "ows_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_type%2Cdevice_locale%" \
                          "2Capp_version_name%2Capp_package_name%2Ccrash%2Ccrash_id%2Ccrash_group_id%2Ccrash_datetime%2Ccrash_t" \
                          "imestamp%2Ccrash_receive_datetime%2Ccrash_receive_timestamp%2Cconnection_type%2Coperator_name%2Cmcc%" \
                          "2Cmnc%2Ccountry_iso_code%2Ccity%2Cappmetrica_device_id"
    return request_crashes_str


def request_installs():
    last_download_installations = datetime.datetime.strptime(__get_max_datetime__("installations", "install_datetime"),
                                                             '%Y-%m-%d %H:%M:%S')

    date_start_installs = str(last_download_installations.date()) + "%20" + __check_data__(
        last_download_installations.hour) + "%3A" + __check_data__(
        last_download_installations.minute) + "%3A" + __check_data__(
        last_download_installations.second)
    request_installs_str = "https://api.appmetrica.yandex.ru/logs/v1/export/installations.json?application_id=176450" \
                           "" \
                           "&date_since=" + date_start_installs + "&date_until=" + __get_end_date__() + \
                           "" \
                           "&date_dimension=default&use_utf8_bom=true&fields=publisher_name%2Cpublisher_id%2Ctracker_name%2" \
                           "Ctracking_id%2Cclick_timestamp%2Cclick_datetime%2Cclick_ipv6%2Cclick_url_parameters%2Cclick_id%2" \
                           "Cclick_user_agent%2Cinstall_datetime%2Cmatch_type%2Cinstall_timestamp%2Cinstall_receive_datetime%" \
                           "2Cinstall_receive_timestamp%2Cinstall_ipv6%2Cis_reinstallation%2Cios_ifa%2Cios_ifv%2Candroid_id%" \
                           "2Cgoogle_aid%2Cos_name%2Cos_version%2Cdevice_manufacturer%2Cdevice_model%2Cdevice_locale%2Cdevice_" \
                           "type%2Capp_version_name%2Capp_package_name%2Cconnection_type%2Coperator_name%2Cmcc%2Cmnc%2Ccountry_" \
                           "iso_code%2Ccity%2Cappmetrica_device_id"
    return request_installs_str
