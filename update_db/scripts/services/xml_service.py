import xml.etree.ElementTree as ET

""" Class that provides methods for working with json"""


# ---------------------------------------------------------------------
# Program by Pinchukov Artur
#
# Version     Data      Info
#  1.0     14.08.2017
# ---------------------------------------------------------------------


class XMLService:
    """ The method init class"""
    def __init__(self, xml_file):
        # pars file config
        self.xml_file = xml_file
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        # get param
        self.data_dict = dict()
        for data in root:
            self.data_dict[data.tag] = data.text

    """ The method return data last download"""
    def get_dict_data(self):
        return self.data_dict

    """ The method set value in config file"""
    def set_data(self, tag_in_config_file, value):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        for data in root:
            if data.tag == tag_in_config_file:
                data.text = str(value)
        tree.write(self.xml_file)