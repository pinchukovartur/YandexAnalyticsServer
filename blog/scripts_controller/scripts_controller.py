import os
import xml.etree.cElementTree as ET
from subprocess import Popen
from datetime import datetime

# install libs
import psutil


# метод проверяет запущен ли скрипт в данный момент


def __check_run_script(self, script):
    print("Есть ли в словаре pid - " + str(self.dict_run_script.get(script.username + script.name)))

    # проверяем, есть ли скрипт в словаре с запущеными скриптами
    if self.dict_run_script.get(script.username + script.name) is not None:
        #  проверяем активен ли данный процесс
        for process in psutil.process_iter():
            # проверяем совпадает ли pid процесса с pid в словаре
            if str(process.pid) == self.dict_run_script.get(script.username + script.name):
                # процесс еще активен
                return False
        # скрипт окончил работу
        self.dict_run_script.pop(script.username + script.name)
        print(str(script.username + script.name) + " окончил свою работу")
        return True
    else:
        return True


# метод запускающий скрипт
def run_script(script_name, script_type, auth_script, script_path, start_date_script):
    # проверяем тип скрипта
    if script_type == "SINGLE":
        return False
    elif script_type == "MULTI":
        # если мулти
        # запускаем скрипт
        log_path = os.path.dirname(__file__) + "/logs/" + auth_script + "/"
        log_name = script_name + ".txt"
        __check_folder(log_path)
        p = Popen("python " + script_path + ">" + log_path + log_name, shell=True)
        print("python " + script_path + ">" + log_path + log_name)
        # записываем в конфиг данные скрипта
        config_path = os.path.dirname(__file__) + "/xml_data/"
        config_name = auth_script + ".xml"

        _add_script_in_xml(config_path+config_name, script_name, script_type, start_date_script, auth_script, str(p.pid))
    else:
        raise NameError("ERROR!!! неизвестный тип скрипта")


# метод записывает информацию о скрипте в xml файл
def _add_script_in_xml(config_path, script_name, script_type, start_date_script, author_script, PID):
    __check_file_exist(config_path)
    # заполняем
    script = ET.Element("script")
    ET.SubElement(script, "name").text = script_name
    ET.SubElement(script, "type").text = script_type
    ET.SubElement(script, "start_data").text = start_date_script
    ET.SubElement(script, "author").text = author_script
    ET.SubElement(script, "PID").text = PID
    # записываем
    tree = ET.parse(config_path)
    root = tree.getroot()
    root.append(script)
    tree.write(config_path)


# метод создает пустой xml файл если его нет
def __check_file_exist(config_path):
    # если xml файла не существует, то создаем его
    if not os.path.isfile(config_path):
        scripts = ET.Element("scripts")
        tree = ET.ElementTree(scripts)
        tree.write(config_path)


# метод проверяет существует ли папка, если нет то создает ее
def __check_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)