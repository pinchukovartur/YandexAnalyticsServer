import json
import datetime

""" Class that provides methods for working with json"""


# ---------------------------------------------------------------------
# Program by Pinchukov Artur
#
# Version     Data      Info
#  1.0     11.08.2017
# ---------------------------------------------------------------------


class JSONService:
    """ The method init class"""
    def __init__(self, json_file):
        f = open(json_file, encoding="utf-8-sig")
        str_json = f.read().replace("\n", "")
        self.pars_str = json.loads(str_json, encoding="utf-8")

    """ The method return dict data from json"""
    def get_dict_data(self):
        return self.pars_str["data"]

    """ This method returns events no later than a given number"""
    def get_dict_data_later_date(self, data, tag_in_dict):
        result = list()
        for i in self.pars_str["data"]:
            data_old = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            date_new = datetime.datetime.strptime(i[tag_in_dict], "%Y-%m-%d %H:%M:%S")
            if date_new > data_old:
                result.append(i)
        return result

    """ This method returns max data events"""
    def get_max_data(self, tag_in_dict):
        data_old = datetime.datetime.strptime("0001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        for i in self.pars_str["data"]:
            date_now = datetime.datetime.strptime(i[tag_in_dict], "%Y-%m-%d %H:%M:%S")
            if date_now > data_old:
                data_old = date_now
        return data_old