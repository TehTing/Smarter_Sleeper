# 操控時間顯示面板的程式

import time
import os
import pygame
from time import sleep
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

serial = spi(port=0, device=0)
device = max7219(serial, cascaded=2, block_orientation=0, rotate=0)
print("Created device")

def clock(mode, awake):
    try:
        current = datetime.now().strftime("%H%M")
        # 測試時可以用下面這行，以秒計算比較好看出變化
        # current = datetime.now().strftime("%M%S")
        with canvas(device) as draw:
            text(draw, (1, 1), current, fill="white", font=proportional(TINY_FONT))
        if(current == awake):
            os.system('mpg321 /home/pi/Music/alert.mp3 &')
        sleep(1)
    except KeyboardInterrupt:
        print("turn off")
        device.cleanup()


def clock_set():
    clock(mode, awake)

def change(set_time):
    awake = set_time

if __name__ == "__main__":
    mode = 1
    awake = "0900"
    while(True):
        clock(mode, awake)
