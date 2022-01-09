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