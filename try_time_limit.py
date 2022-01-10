#reference: https://www.itread01.com/content/1548280081.html
import try_alarm
import signal
import time
import RPi.GPIO as GPIO   

def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到訊號 SIGALRM 後的回撥函式，第一個引數是訊號的數字，第二個引數是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 設定訊號和回撥函式
                signal.alarm(num)  # 設定 num 秒的鬧鐘
                print('start alarm signal.')
                while True:
                    
                    try_alarm.on()
                    time.sleep(10)
                
                r = func(*args, **kwargs)
                print('close alarm signal.')
                signal.alarm(0)  # 關閉鬧鐘
                return r
            except RuntimeError as e:
                callback()

        return to_do

    return wrap

def after_timeout():  # 超時後的處理函式
    print("Time out!")

@set_timeout(5, after_timeout)  # 限時 2 秒超時
def connect():  # 要執行的函式

    GPIO.setmode(GPIO.BOARD)   
    GPIO.setup(11, GPIO.IN)
    while True:
        inputValue = GPIO.input(11)
        if inputValue== False:
            print("Button pressed ")
            break
    #time.sleep(10)  # 函式執行時間，寫大於2的值，可測試超時
    print('Finished without timeout.')

if __name__ == '__main__':
    connect()
