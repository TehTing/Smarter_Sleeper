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

## MAX7219
#### 一、連接硬體裝置(單個MAX7219)
![.](/.png "MAX7219_pin接法")
#### 二、安裝SPI
檢查是否有東西
```
$ lsmod | grep -i spi
$ ls -l /dev/spi*
如果沒有 -> 進行安裝
$ sudo raspi-config
```
![.](/.png "api安裝")  
![.](/.png "api安裝")  
![.](/.png "api安裝")  
參考自：https://luma-led-matrix.readthedocs.io/en/latest/install.html

#### 三、下載安裝套件
控制MAX7219常見的套件有兩種：max7219和luma.led_matrix。
但我建議使用luma.led_matrix，因為max7219似乎改過文件，目前網路上找到的範例執行後都會出現ModuleNotFoundError，luma.led_matrix在操作上會比較順利，所以以下範例也是用luma.led_matrix套件來撰寫。

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
![.](/.png "接腳")  
![.](/.png "接腳")  
參考自：https://swf.com.tw/?p=738

2. 打開剛剛使用的matrix_demo.py檔案，將第21行程式碼
device = max7219(serial, cascaded=1, block_orientation=block_orientation,
中的cascaded=1改為cascaded=2，cascaded是代表有幾個裝置串接的意思

3. 可以正常顯示的話Max7219的前置作業就全部完成啦！

#### 五、Smarter Sleeper程式撰寫
```python
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

## 連接音響
#### 一、前置工作
1. 將檔案放入這個資料夾/home/pi/Music
2. 更新安裝套件
sudo apt-get update
sudo apt-get install mpg321
3. 執行此套件
```
import os 
os.system('mpg321 /home/pi/Music你的檔名 &')
```
