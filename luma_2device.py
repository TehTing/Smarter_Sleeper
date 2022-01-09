# 此程式用於測試兩個max7219的串聯是否成功

import time
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

serial = spi(port=0, device=0)
device = max7219(serial, cascaded=2, block_orientation=0, rotate=0)
print("Created device")

def time(mode):
    while(mode):
        now = datetime.now()
        current=datetime.now().strftime('%H')+datetime.now().strftime('%M')
        with canvas(device) as draw:
            text(draw, (1, 1), current, fill="white", font=proportional(TINY_FONT))
        #time.sleep(0.5)

def main():
    mode = 1
    time(mode)
        

if __name__ == "__main__":
    main()
