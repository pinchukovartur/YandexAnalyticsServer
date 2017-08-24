import datetime

from requests import post  # install lib
import time

while True:
    values = {"ask_ref": "http://androidphones.ru/kak-smenit-imei-na-android-device-id.html",
              "helpful_answer": "Нет..."}
    p = post("http://androidphones.ru/helpful/helpful_counter.php", data=values)
