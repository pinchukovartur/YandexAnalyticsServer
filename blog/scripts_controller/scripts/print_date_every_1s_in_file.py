import datetime
import time
import os


while True:
    f = open(os.path.dirname(__file__)+"/log.txt", "a")
    f.write(str(datetime.datetime.now()))
    f.close()
    time.sleep(1)
