import datetime
import os
import time
import subprocess

from analytics_сontroller import AnalyticsController
from scripts.dao.analytics_dao import AnalyticsDB
from requests import *  # install lib

# STATIC DATA
TOKEN = "AQAAAAATpP0XAAR70vxUpgjrAkq_h3IGIcgKL-0"
# time between requests in yandex to check if the package is ready
TIME_SLEEP = 10
# number of packets to which data is divided
COUNT_PACK = 1000
SERVER_HOST = "http://192.168.0.111:8080"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "analytics"
DB_HOST = "127.0.0.1"
dir_project = os.path.dirname(os.path.realpath(__file__))
LOG_FILE = dir_project + "/log.txt"
ERR_FILE = dir_project + "/err.txt"
LOCK_FILE = dir_project + "/lock.txt"
TMP_FOLDER_FOR_JSON_FILES = dir_project + "/tmp/"
BACKUP_FILE_NAME = dir_project + "/backup.sql.gz"


# clear log file
def clear_file(file_path):
    f = open(file_path, "w")
    f.write("")
    f.close()


# open log file
def write_file(message, file_path):
    file = open(file_path, "a")
    file.write(str(message) + "\n")
    file.close()


# check already update
def check_lock_file(lock_file):
    if os.path.isfile(lock_file):
        print("ERROR!!! already update")
        exit(1)
    else:
        f = open(lock_file, "w")
        f.write("start update - " + str(datetime.datetime.now()))
        f.close()


# delete lock file
def delete_lock_file(lock_file):
    if os.path.isfile(lock_file):
        os.remove(lock_file)


# the method run backup mysql bd
def run_backup_db(backup_file):
    if os.path.isfile(backup_file):
        os.remove(backup_file)

    p = subprocess.run("mysqldump -u "+DB_USER+" -p"+DB_PASSWORD+" "+DB_NAME+" | gzip > " + backup_file, shell=True)
    print(p.returncode)
    if p.returncode != 0:
        print("Error! run backup DB")
        raise NameError("Error! run backup DB")

try:
    # check already update
    check_lock_file(LOCK_FILE)

    # DATA
    # the current date
    today = datetime.datetime.today()
    # class to work with the database (lies in the scripts / dao folders)
    analytics_db = AnalyticsDB(DB_USER, DB_PASSWORD, DB_HOST)
    # the maximum date in the tables is taken from the database
    last_download_events = datetime.datetime.strptime(analytics_db.get_max_event_datetime(), '%Y-%m-%d %H:%M:%S')
    last_download_errors = datetime.datetime.strptime(analytics_db.get_max_errors_datetime(), '%Y-%m-%d %H:%M:%S')
    last_download_installations = datetime.datetime.strptime(analytics_db.get_max_installation_datetime(),
                                                             '%Y-%m-%d %H:%M:%S')
    last_download_crashes = datetime.datetime.strptime(analytics_db.get_max_crashes_datetime(), '%Y-%m-%d %H:%M:%S')
    # controller for parsing json files and sending them to the database, methods accept a sheet with paths to jsonfiles
    analytics_controller = AnalyticsController(analytics_db)

    # the method asks the service for permission to update
    def get_root():
        try:
            p = get(SERVER_HOST + "/start_download/start")
            if p.text == "you can download":
                write_file("i did get root from server", LOG_FILE)
            else:
                write_file(p.text, LOG_FILE)
                time.sleep(5)
                get_root()
        except Exception as e:
            write_file(str(e), LOG_FILE)
            exit(1)

    # the method adds zeroes to the beginning of the date, if it is less than 10 tons to Yandex does not eat the date
    # with one value
    def check_data(value):
        if int(value) < 10:
            return "0" + str(value)
        else:
            return str(value)

    # we execute the request until we get a good answer
    def sen_request(request_str):
        while True:
            try:
                response = get(request_str)
                if response.status_code == 200:
                    return response
            except Exception as error:
                write_file(str(error), ERR_FILE)
            time.sleep(TIME_SLEEP)

    # get list json files with data from yandex analytic
    def get_list_json_files(file_name, request_str):
        list_files_name = list()
        for i in range(COUNT_PACK):
            text = "pack number:" + str(i + 1) + " | name:" + str(file_name) + " | date:" + str(datetime.datetime.now())
            write_file(text, LOG_FILE)
            response = sen_request(request_str + "&parts_count=" + str(COUNT_PACK)
                                   + "&part_number=" + str(i) + "&oauth_token=" + TOKEN)
            # save to file
            f = open(TMP_FOLDER_FOR_JSON_FILES + file_name + str(i) + ".json", "wb")
            f.write(response.text.encode(encoding='utf_8_sig', errors='strict'))
            f.close()
            # add the path to the json file in the sheet
            list_files_name.append(TMP_FOLDER_FOR_JSON_FILES + "/" + file_name + str(i) + ".json")

        return list_files_name

    # clear log file
    clear_file(ERR_FILE)
    clear_file(LOG_FILE)

    # get permission to download
    get_root()

    # save old db
    run_backup_db(BACKUP_FILE_NAME)

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

    write_file("start date period of time events - " + str(last_download_events), LOG_FILE)
    write_file("start date period of time errors - " + str(last_download_errors), LOG_FILE)
    write_file("start date period of time installs - " + str(last_download_installations), LOG_FILE)
    write_file("start date period of time crashes - " + str(last_download_crashes), LOG_FILE)
    write_file("end-of-time date (total) - " + str(today), LOG_FILE)

    # REQUEST IN YANDEX
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

    # send the sheet to the controller for further parsing the files and sending them to the database
    analytics_controller.add_installations(get_list_json_files("installations", request_installations))
    analytics_controller.add_errors(get_list_json_files("errors", request_errors))
    analytics_controller.add_crashes(get_list_json_files("crashes", request_crashes))
    analytics_controller.add_events(get_list_json_files("events", request_events))

    write_file("The script began its work in - " + str(today), LOG_FILE)
    write_file("The script finished its work in - " + str(datetime.datetime.today()), LOG_FILE)

    # set message about final update
    p = get(SERVER_HOST + "/start_download/ok")

    delete_lock_file(LOCK_FILE)
except Exception as error:
    write_file(str(error), ERR_FILE)
