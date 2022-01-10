#reference: https://www.itread01.com/content/1548280081.html

import signal
import time

def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到訊號 SIGALRM 後的回撥函式，第一個引數是訊號的數字，第二個引數是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 設定訊號和回撥函式
                signal.alarm(num)  # 設定 num 秒的鬧鐘
                print('start alarm signal.')
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

@set_timeout(2, after_timeout)  # 限時 2 秒超時
def connect():  # 要執行的函式
    time.sleep(10)  # 函式執行時間，寫大於2的值，可測試超時
    print('Finished without timeout.')

if __name__ == '__main__':
    connect()