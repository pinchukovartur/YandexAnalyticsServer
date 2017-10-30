import time
from script_data import *
from requests import *

"""
Данный скрипт отвечает за загрузку файлов с яндекса
"""


def __sen_request__(request_str):
    while True:
        try:
            response = get(request_str)

            print(response.status_code)
            if response.status_code == 200:
                return response
            else:
                time.sleep(TIME_SLEEP)
        except Exception as error:
            time.sleep(TIME_SLEEP)


def get_list_json_files(file_name, request_str):
    list_files_name = list()
    for i in range(COUNT_PACK):
        response = __sen_request__(request_str + "&parts_count=" + str(COUNT_PACK)
                                   + "&part_number=" + str(i) + "&oauth_token=" + TOKEN)
        # save to file
        f = open(TMP_FOLDER_FOR_JSON_FILES + file_name + str(i) + ".json", "wb")
        f.write(response.text.encode(encoding='utf_8_sig', errors='strict'))
        f.close()
        # add the path to the json file in the sheet
        list_files_name.append(TMP_FOLDER_FOR_JSON_FILES + "/" + file_name + str(i) + ".json")

    return list_files_name

