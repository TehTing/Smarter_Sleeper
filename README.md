# Smarter_Sleeper
1.  下載max7219套件
$ git clone https://github.com/rm-hull/max7219.git 
$ cd max7219 
$ sudo python setup.py install

2.  執行測試程式碼
import max7219.led as led
import max7219.canvas as canvas
import max7219.transitions as transitions
import time
import datetime
from random import randrange

led.init()

while True:
    t = time.time()
    ctime = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    led.show_message(ctime, transition = transitions.left_scroll)

出現Error:
ModuleNotFoundError: No module named 'max7219.led'; 'max7219' is not a package
