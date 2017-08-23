import os
import xml.etree.cElementTree as ET
from subprocess import Popen
import datetime

# install libs
import psutil


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
        p = Popen("python " + script_path + ">" + log_path + str(datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d_%H_%M_%S_")) + log_name, shell=True)
        print("python " + script_path + ">" + log_path + log_name)
        # записываем в конфиг данные скрипта
        config_path = os.path.dirname(__file__) + "/xml_data/"
        config_name = auth_script + ".xml"

        print(p.pid)
        print(os.getpid())
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


def check_run_scripts(username):
    pass


# метод удаляет из конфига все устаревшие скрипты
def __delete_old_script_in_xml(config_path):
    # состояние скрипт по умолчанию не активное
    state_script = False

    # проходим по всем скриптам в конфиге
    tree = ET.parse(config_path)
    # проходим по всем активным pid-ам

    for scripts in tree.iter():
        if scripts.tag == "scripts":
            for script in scripts:
                for subelem in script:
                    if subelem.tag == "PID":
                        for process in psutil.process_iter():
                            # проверям совпадает ли пид в конфиги с активными
                            if str(subelem.text) == str(process.pid):
                                # если такой пид есть, то делаем состояние активным
                                state_script = True
                            # если пид так и не был найдет, удаляем скрипт
                if not state_script:
                        scripts.remove(script)
    # записываем в файл
    tree.write(config_path)

__delete_old_script_in_xml("D:\Projects\Django\web-post\\blog\scripts_controller\\xml_data\\admin.xml")
