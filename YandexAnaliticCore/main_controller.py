# install libs
import psutil


# return all active processes
def get_processes():
    return psutil.process_iter()


SCRIPT_NAME = "hello.py"
USER_NAME = "ADMIN"
TYPE_SCRIPT = "SINGLE"  # SINGLE/MULTI
SCRIPT_TEXT = "print('Hello World')"

# словарь с запушенными скриптами типа - <SCRIPT_NAME+USER_NAME>: <PID>
dict_active_script = dict()

# если скрипт для одиночного использования
if TYPE_SCRIPT == "SINGLE":
    if dict_active_script.get(SCRIPT_NAME + USER_NAME) is not None:
        #  проверяем активен ли данный процесс
        for proc in get_processes():
            if proc.pid == dict_active_script.get(SCRIPT_NAME + USER_NAME):
                # процесс еще активен => кидает ошибку
                raise NameError("ERROR!!! одна копия уже запущена")
            else:
                # скрипт окончил работу, следовательно удаляем его из словаря и запускаем новый
                dict_active_script.pop(SCRIPT_NAME + USER_NAME)
                ####  ЗАПУСК СКРИПТА

        pass
    else:
        # СТАРТ СКРИПТ
        pass