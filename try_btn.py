# try_btn.py

import RPi.GPIO as GPIO   
import time   

GPIO.setmode(GPIO.BOARD)   
GPIO.setup(11, GPIO.IN)
cont = 10
while True:
    inputValue = GPIO.input(11)
    if inputValue== False:
        print("Button pressed ")
        while inputValue ==  False:
            time.sleep(0.5)
            inputValue = GPIO.input(11)
        
