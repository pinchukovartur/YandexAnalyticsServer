import datetime
import os
import xml.etree.cElementTree as ET
from subprocess import Popen

# install libs
import psutil

CONFIG_PATH = os.path.dirname(__file__) + "/xml_data/"

# метод запускающий скрипт
def run_script(script_name, script_type, auth_script, script_path, start_date_script):
    # записываем в конфиг данные скрипта
    config_name = auth_script + ".xml"
    __check_file_exist(CONFIG_PATH + config_name)

    # проверяем тип скрипта
    if script_type == "SINGLE":
        # если скрипт активый кидаем ерор
        if get_script_status(auth_script, script_name, CONFIG_PATH + config_name):
            raise NameError("ERROR!!! одна копия скрипта уже запущена")
        else:
            __run_script(script_name, auth_script, script_path, CONFIG_PATH, config_name, script_type,
                         start_date_script)
    elif script_type == "MULTI":
        # если мулти
        # запускаем скрипт
        __run_script(script_name, auth_script, script_path, CONFIG_PATH, config_name, script_type, start_date_script)
    else:
        raise NameError("ERROR!!! неизвестный тип скрипта")


# метод записывает информацию о скрипте в xml файл
def _add_script_in_xml(config_path, script_name, script_type, start_date_script, author_script, PID):
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


def get_script_status(username, script_name, config_path):
    # обновляем файл конфигов, 3 раза дабы точно убедиться)))
    __delete_old_script_in_xml(config_path)
    __delete_old_script_in_xml(config_path)
    __delete_old_script_in_xml(config_path)

    # проходим по всем скриптам в конфиге
    tree = ET.parse(config_path)
    # проходим по всем активным pid-ам
    i = 0
    for scripts in tree.iter():
        if scripts.tag == "scripts":
            for script in scripts:
                for subelem in script:
                    if subelem.tag == "name" and subelem.text == script_name:
                        i = i + 1
                    if subelem.tag == "author" and subelem.text == username:
                        i = i + 1
                    if i > 1:
                        return True

                i = 0
    return False


# the method delete old scripts in xml config
def __delete_old_script_in_xml(config_path):
    # state script in at the time
    state_script = False

    # read xml file
    tree = ET.parse(config_path)
    # bypass scripts
    for scripts in tree.iter():
        if scripts.tag == "scripts":
            # bypass script
            for script in scripts:
                # bypass sub element
                for subelem in script:
                    if subelem.tag == "PID":
                        # bypass on active pids
                        for process in psutil.process_iter():
                            if str(subelem.text) == str(process.pid) and str(process.name()) == "cmd.exe":
                                state_script = True
                # if script was not find delete him
                if not state_script:
                    scripts.remove(script)
                state_script = False
    tree.write(config_path)


def __run_script(script_name, auth_script, script_path, config_path, config_name, script_type, start_date_script):
    # create path where save logs files
    log_path = os.path.dirname(__file__) + "/logs/" + auth_script + "/"
    # logs name
    log_name = script_name + ".txt"
    # check folder if exist create it
    __check_folder(log_path)
    # start process
    p = Popen("python " + script_path + ">" + log_path + str(
        datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d_%H_%M_%S_")) + log_name, shell=True)
    # add info in xml file with meta data
    _add_script_in_xml(config_path + config_name, script_name, script_type, start_date_script, auth_script, str(p.pid))


def stop_scripts(username, script_name):
    # обновляем файл конфигов, 3 раза дабы точно убедиться)))
    __delete_old_script_in_xml(CONFIG_PATH + username + ".xml")
    __delete_old_script_in_xml(CONFIG_PATH + username + ".xml")
    __delete_old_script_in_xml(CONFIG_PATH + username + ".xml")

    # проходим по всем скриптам в конфиге
    tree = ET.parse(CONFIG_PATH + username + ".xml")
    # проходим по всем активным pid-ам
    i = 0
    pid = -1
    for scripts in tree.iter():
        if scripts.tag == "scripts":
            for script in scripts:
                for subelem in script:
                    if subelem.tag == "name" and subelem.text == script_name:
                        i = i + 1
                    if subelem.tag == "author" and subelem.text == username:
                        i = i + 1
                    if subelem.tag == "PID":
                        pid = int(subelem.text)
                        i = i + 1
                    if i > 2 and pid > -1:
                        # УБИВАЕМ ПРОЦЕСС И ЕГО ДЕТЕЙ!!! УХАХААХАХАХАХ насильственно !)
                        Popen('taskkill /f /PID ' + str(pid) + " /T", shell=True)
                    print(subelem.text)
                i = 0

    # обновляем файл конфигов, 3 раза дабы точно убедиться)))
    __delete_old_script_in_xml(CONFIG_PATH + username + ".xml")
    __delete_old_script_in_xml(CONFIG_PATH + username + ".xml")
    __delete_old_script_in_xml(CONFIG_PATH + username + ".xml")
