import subprocess
import os
import signal
import time
#p = subprocess.Popen('gnome-terminal -x sh -c "python3.5 /home/pinchukov/Documents/web-post/test.py>text.txt; exec bash"', shell=True)
p = subprocess.Popen('python3.5 /home/pinchukov/Documents/web-post/test.py>text.txt', shell=True)

print(p.pid)
p_child = p.pid
time.sleep(5)
os.kill(p_child, signal.SIGKILL)
time.sleep(100)

import atexit
atexit.register(p_child)