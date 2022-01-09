# Smarter Sleeper
## 專案介紹
打開手機鬧鐘的App，裡面是一整排滑不完的鬧鐘清單嗎？即便設了很多鬧鐘，關掉鬧鐘繼續睡的壞習慣還是讓你不斷遲到嗎？嘗試使用防貪睡的App，在完成關掉鬧鐘的任務後坐在床上，溫暖的床又讓你沉淪了嗎？  
  
  Smart Sleeper提供三段強度的喚醒方式，讓你戒掉貪睡的壞習慣：
  
#### 使用元件
* Raspberry Pi 3
* Raspberry Pi NOIR/CS
* MAX7219 矩陣顯示模組 * 2
* 藍芽音響與音源線
* 杜邦線數條
* 1.5V電池 * 4
* 4節電池座

## MAX7219前置
#### 一、連接硬體裝置(單個MAX7219)
![.](/images/max7219_pin_1.png "MAX7219_pin接法")
#### 二、安裝SPI
檢查是否有東西
```
$ lsmod | grep -i spi
$ ls -l /dev/spi*
如果沒有 -> 進行安裝
$ sudo raspi-config
```
![.](/images/max7219_api_1.jpg "api安裝")  
![.](/images/max7219_api_2.jpg "api安裝")  
![.](/images/max7219_api_3.jpg "api安裝")  
參考自：https://luma-led-matrix.readthedocs.io/en/latest/install.html

#### 三、下載安裝套件
控制MAX7219常見的套件有兩種：`max7219`和`luma.led_matrix`。
但我建議使用`luma.led_matrix`，因為`max7219`似乎改過文件，目前網路上找到的範例執行後都會出現`ModuleNotFoundError`，`luma.led_matrix`在操作上會比較順利，所以以下範例也是用`luma.led_matrix`套件來撰寫。

```
# 更新套件
$ sudo usermod -a -G spi,gpio pi
$ sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg-dev
$ sudo -i pip install --upgrade pip setuptools
$ sudo apt-get purge python-pip

# 下載luma.led_matrix套件
$ sudo -H pip install --upgrade luma.led_matrix
$ git clone https://github.com/rm-hull/luma.led_matrix.git

# 更改目前位置
$ cd luma.led_matrix

# 執行測試檔案
$ python3 examples/matrix_demo.py -h
```
參考自：https://www.twblogs.net/a/5b8d06102b71771883396f6d

>若測試檔案無法打開，可直接使用下面程式碼測試：
>>```
晚點放

參考影片(裡面有對這段程式碼的簡單介紹)：https://www.youtube.com/watch?v=sB79wyqsbAo&ab_channel=%E5%90%B3%E7%B4%B9%E8%A3%B3


#### 四、串接兩個Max7219
個別測試好Max7219可以正常使用後，接著就可以來串接兩個Max7219。

1. 連接設備  
![.](/images/max7219_pin_2.png "接腳")  
![.](/images/max7219_pin_3.png "接腳")  
參考自：https://swf.com.tw/?p=738

2. 打開剛剛使用的matrix_demo.py檔案，將第21行程式碼
`device = max7219(serial, cascaded=1, block_orientation=block_orientation,`
中的`cascaded=1`改為`cascaded=2`，cascaded是代表有幾個裝置串接的意思

3. 可以正常顯示的話Max7219的前置作業就全部完成啦！

## 連接音響
#### 一、前置工作
1. 將檔案放入這個資料夾 /home/pi/Music
2. 更新安裝套件
```
sudo apt-get update
sudo apt-get install mpg321
```
3. 執行此套件
```
import os 
os.system('mpg321 /home/pi/Music/你的檔名 &')
# 例如：os.system('mpg321 /home/pi/Music/mymusic.mp3 &')
```
## Smarter Sleeper程式撰寫
**還沒完成**
```python
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

def time(mode):
    while(mode):
        now = datetime.now()
	current=datetime.now().strftime('%M')+datetime.now().strftime('%S')	# 測試的時候可以用這行
# (H=Hour, M=Minute S=Second)
        current=datetime.now().strftime('%H')+datetime.now().strftime('%M')


        with canvas(device) as draw:
            text(draw, (1, 1), current, fill="white", font=proportional(TINY_FONT))
def main():
    mode = 1
    time(mode)   

if __name__ == "__main__":
    main()
```

## Line bot前置
1. 創建LineBot帳號，請見此[參考頁面](https://blog.cavedu.com/2021/12/06/rasbperry-pi-line-messaging-api/)建立 LINE messaging API的部分進行操作  
2. 安裝套件
```
# ngrok伺服器
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip --no-check-certificate 
unzip ngrok-stable-linux-arm.zip
./ngrok --version
# linebot套件
pip install line-bot-sdk
```
3. 設定webhook參數
```
# 先開啟第一個terminal
$ ./ngrok http 8000
```
將htpps開頭的網址複製起來(下圖框起來的那欄)  
![.](/images/webhook_1.jpg "ngrok執行畫面")  
**注意：不要關閉此terminal，執行linebot時我們需要ngrok保持在開啟的狀態**  
來到line developers網頁，找到Messaging API頁的webhook，將剛才複製的網址貼上，並在結尾加上`/callback`。
接著按下Update並確保Use webhook是開啟的狀態  
![.](/images/webhook_2.jpg "ngrok執行畫面" )   
**注意：每次重開ngrok都要執行一次修改參數的動作，因此盡量不要一直開開關關，不然一直改參數你會很累。**  
3. 設定linebot_test.py參數
linebot_test.py中將`channel_secret=''`和`'channel_access_token''`的內容補上  
> channel_secret的資料在line developers的Basic settings頁  
channel_access_token的資料在line developers的Messaging API頁
以上內容參考自：https://blog.cavedu.com/2021/12/06/rasbperry-pi-line-messaging-api/
