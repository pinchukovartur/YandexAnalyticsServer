# standard lib
import datetime
import time
import os
# my lib
from utils.slack_util import send_message_in_slack, SLACK_GREEN, SLACK_RED
from utils.console_util import get_console_param
from utils.lock_util import start_work, end_work
from utils.backup_util import run_backup_db
from download_json_files import get_list_json_files
from script_data import request_crashes, request_installs, request_errors, request_events
from insert_in_db import add
from const import *
# install lib
import pycron

"""
Запуск обновления бд
"""

try:
    cron_cmd = get_console_param()["cron"]
    send_message_in_slack(SLACK_URL, SLACK_CHANEL, "Start update every " + str(cron_cmd), str(datetime.datetime.now()),
                          SLACK_USERNAME, SLACK_ICON, SLACK_GREEN)

    while True:
        # start cron script
        if pycron.is_now(cron_cmd):
            # check lock file
            start_work()
            # send start message
            send_message_in_slack(SLACK_URL, SLACK_CHANEL, "Start update DB", str(datetime.datetime.now()), SLACK_USERNAME,
                                  SLACK_ICON, SLACK_GREEN)
            # backup
            run_backup_db(str(os.path.dirname(os.path.realpath(__file__)) + "/backup.sql.gz"), DB_USER, DB_PASSWORD, DB_NAME)
            # download json files
            crash_files = get_list_json_files("crashes", request_crashes())
            install_files = get_list_json_files("installations", request_installs())
            event_files = get_list_json_files("events", request_events())
            error_files = get_list_json_files("errors", request_errors())
            # insert in db
            print("")
            add("crashes", crash_files)
            add("installations", install_files)
            add("events", event_files)
            add("errors", error_files)
            # send end message
            send_message_in_slack(SLACK_URL, SLACK_CHANEL, "End update DB", str(datetime.datetime.now()), SLACK_USERNAME,
                                  SLACK_ICON, SLACK_GREEN)
            # delete lock file
            end_work()
            # wait cron time
            time.sleep(60)

        print("wait cron time - " + str(cron_cmd), " now - " + str(datetime.datetime.now()))
        time.sleep(55)  # wait one minute, so that there is no re-cloning if the repository is very small
except Exception as errorGlobal:
    send_message_in_slack(SLACK_URL, SLACK_CHANEL, "Error update", str(errorGlobal), SLACK_USERNAME,
                          SLACK_ICON, SLACK_RED)