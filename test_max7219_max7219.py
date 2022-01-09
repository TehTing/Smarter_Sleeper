'''
用 max7219 套件測試裝置 max7219 是否能夠使用
原本此程式測試後可以正常運作
但可能因為文件更新的關係，這幾天再測試時是失敗的
建議改用 luma 套件控制 max7219
測試程式碼請換用 test_max7219_luma.py
'''

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
