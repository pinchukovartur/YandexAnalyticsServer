# install libs
import datetime
from subprocess import Popen

import psutil


class ScriptController:
    # метод иницализации
    def __init__(self):
        self.dict_run_script = dict()

    # метод возвращает true если скрипт имеет тип MULTI, если SINGLE то False, иначе генерирурет ошибку
    def check_type_script(self, script_type):
        if script_type == "SINGLE":
            return False
        elif script_type == "MULTI":
            return True
        else:
            raise NameError("ERROR!!! неизвестный тип скрипта")

    # метод проверяет запущен ли скрипт в данный момент
    def check_run_script(self, script):

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
    def run_script(self, script):
        # создаем файлик со скриптом
        file_name = script.name + script.username + str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        file = open(file_name + ".py", "w")
        file.write(script.text)
        file.close()
        # запускаем скрипт
        process = Popen('python ' + file_name + ".py" + ">" + file_name + ".txt", shell=True)
        print("Старт процесс - " + str(process.pid))
        self.dict_run_script[script.username + script.name] = str(process.pid)
