from main_controller import *
from models import script
import time

controller = ScriptController()

SCRIPT_NAME = "hello"
USER_NAME = "ADMIN"
TYPE_SCRIPT = "SINGLE"  # SINGLE/MULTI
SCRIPT_TEXT = "import time\n" \
              "print('Hello World')\n" \
              "time.sleep(60)\n"

script_test = script.Script(SCRIPT_NAME, TYPE_SCRIPT, USER_NAME, SCRIPT_TEXT)

while True:
    # проверяем мулти или сингл скрипт
    if not controller.check_type_script(script_test.type):
        # проверяем не запущен ли скрипт
        if controller.check_run_script(script_test):
            # если нет то запускаем
            controller.run_script(script_test)
    time.sleep(2)