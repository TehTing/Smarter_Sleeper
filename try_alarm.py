# try alarm
import try_another_play
import os
import time
from time import sleep
from datetime import datetime

def on(alarm):
    current = datetime.now().strftime("%M%S")
    print(current)
    if(current == alarm):
        print(alarm)
        try_another_play()
        print("please wake up")
        

def off():
    global alarm
    awake = "9999"
    print("alarm: off")

def change(set_time):
    global alarm
    alarm = set_time
    print("set time sucess:" + awake)

#if __name__ == "__main__":
#    on()