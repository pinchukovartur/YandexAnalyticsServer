from scripts.services.json_service import *
from scripts.utils.console_utils import *


class AnalyticsController:
    def __init__(self, analyticsDB):
        self.analyticsDB = analyticsDB

    def add_events(self, list_path_for_json_events_files):
        data_download_events = str(self.analyticsDB.get_max_event_datetime())
        print("дата последнего события в БД - " + str(data_download_events))

        for path in list_path_for_json_events_files:
            print("чтение json файла событий ...")
            json_service = JSONService(path)

            events_later_data = json_service.get_dict_data_later_date(data_download_events, "event_datetime")
            print("количесвто новых событий - " + str(len(events_later_data)))

            print("добавляем новые события в базу")
            i = 0
            if len(events_later_data) != 0:
                for event in events_later_data:
                    self.analyticsDB.insert_events(event)
                    printProgressBar(i, len(events_later_data), prefix='Progress add events:', suffix='Complete',
                                     length=50)
                    i = i + 1

            print("работа с событиями " + path + "оконченна \n")

    def add_installations(self, list_path_for_json_installations_files):
        data_download_installations = str(self.analyticsDB.get_max_installation_datetime())
        print("дата последней установки в БД - " + str(data_download_installations))

        for path in list_path_for_json_installations_files:
            print("чтение json файла установок ...")
            json_service = JSONService(path)

            install_later_data = json_service.get_dict_data_later_date(data_download_installations, "install_datetime")
            print("количесвто новых устанок - " + str(len(install_later_data)))

            print("добавляем новые установки в базу")
            i = 0
            if len(install_later_data) != 0:
                for install in install_later_data:
                    self.analyticsDB.insert_installation(install)
                    printProgressBar(i, len(install_later_data), prefix='Progress add installs:', suffix='Complete',
                                     length=50)
                    i = i + 1
            print("работа с установками " + path + " окончена \n")

    def add_errors(self, list_path_for_json_errors_files):
        data_download_errors = str(self.analyticsDB.get_max_errors_datetime())
        print("дата последней ошибки в БД - " + str(data_download_errors))

        for path in list_path_for_json_errors_files:
            print("чтение json файла ошибок ...")
            json_service = JSONService(path)

            errors_later_data = json_service.get_dict_data_later_date(data_download_errors,
                                                                      "error_datetime")
            print("количесвто новых ошибок - " + str(len(errors_later_data)))

            print("добавляем новые ошибки в базу")
            i = 0
            if len(errors_later_data) != 0:
                for error in errors_later_data:
                    self.analyticsDB.insert_error(error)
                    printProgressBar(i, len(errors_later_data), prefix='Progress add installs:', suffix='Complete',
                                     length=50)
                    i = i + 1
            print("работа с ошибками " + path + " окончена \n")

    def add_crashes(self, list_path_for_json_crashes_files):
        data_download_crashes = str(self.analyticsDB.get_max_crashes_datetime())
        print("дата последнего краша в БД - " + str(data_download_crashes))

        for path in list_path_for_json_crashes_files:
            print("чтение json файла крэшей ...")
            json_service = JSONService(path)

            crashes_later_data = json_service.get_dict_data_later_date(data_download_crashes,
                                                                       "crash_datetime")
            print("количесвто новых крэшей - " + str(len(crashes_later_data)))

            print("добавляем новых крэшей в базу")
            i = 0
            if len(crashes_later_data) != 0:
                for crash in crashes_later_data:
                    self.analyticsDB.insert_crashes(crash)
                    printProgressBar(i, len(crashes_later_data), prefix='Progress add installs:', suffix='Complete',
                                     length=50)
                    i = i + 1
            print("работа с крэшами " + path + " окончена \n")
