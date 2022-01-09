# 用luma套件測試設備max7219是否正常運作
# 參考自 luma 套件提供的 matrix_demo.py

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import time

serial = spi(port=0, device=0)
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)
print("Created device")
msg = "12345678"
print(msg)
show_message(device, msg, fill="white", font=proportional(CP437_FONT))
time.sleep(1)

msg = "Slow"
print(msg)
# show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
# "scroll_delay" can slow down the speed
time.sleep(1)

# change light intensity
msg = "A"
print(msg)
for _ in range(2):
    for intensity in range(16):
        device.contrast(intensity * 16)
        with canvas(device) as draw:
            text(draw, (0, 0), msg, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)

device.contrast(0x80)
time.sleep(1)
device.cleanup()
