# Reference: https://sites.google.com/site/raspberrypidiy/basic/gpioinput

# import necessary library 匯入RPi.GPIO與time時間函式庫
import RPi.GPIO as GPIO   
import time   

# to use Raspberry Pi board pin numbers 使用板上定義的腳位號碼
GPIO.setmode(GPIO.BOARD)   

# set up pin 11 as an output  將P1接頭的11腳位設定為輸入 
GPIO.setup(11, GPIO.IN)

# enter while loop unitl exit 隨著時間迴圈會重複執行，直到強制離開
while True:

# set up input value as GPIO.11 將P1接頭的11腳位的值設定為inputValue
    inputValue = GPIO.input(11)

# when user press the btn 如果是真 (玩家按下按鈕)
    if inputValue== False:

# show string on screen   顯示被按下
        print("Button pressed ")
        while inputValue ==  False:
            time.sleep(0.5)
            inputValue = GPIO.input(11)