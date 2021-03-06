#import main
import main_test
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

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

def clock():
    mode = 1
    awake = "0900"
    serial = spi(port=0, device=0)
    device = max7219(serial, cascaded=2, block_orientation=0, rotate=0)
    print("Created device")
    #while(True):
    try:
        # main_test.line()
        #while(mode):
            #now = datetime.now()
        #print(request)
        #if (request != ""):
        #    print(request)
            # break;
        #else:
        current = datetime.now().strftime("%M%S")
        with canvas(device) as draw:
            text(draw, (1, 1), current, fill="white", font=proportional(TINY_FONT))
        if(current == awake):
            os.system('mpg321 /home/pi/Music/alert.mp3 &')        
    except KeyboardInterrupt:
        print("turn off")
        device.cleanup()
    #print("off")
    


path=sys.argv[0]
print(path)

# led_status = ""

#要改channel_secret和channel_access_token
channel_secret = '7272a33c0a0c5e35dfe4db9e524c2043'
channel_access_token = 'OadmKL2gibSVMNSu3EPuGwROPzThOP3nw2iZIZhCZe/X2fxCKIqGEfCIPe57YtxxlyKW3Gl3IVjHiSldr6kCUxYW4s0zDoHXvgKHHOyboGag51n6fIqypCPeGF88t4Vkbo6Y7n5rX17DTGTOP+aoeAdB04t89/1O/w1cDnyilFU='
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
#request=""
#clock()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    # print(request)
    print("cb")
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/")
def control_led():
    print("led")
    global led_status
    return led_status

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    global led_status
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    print (event.message.text)

    #in_w = event.message.text
    #in_w = event.message.text
    #print (in_w)
    
    if ('A' == event.message.text):
        led_status = event.message.text # set alert time
        # print('led_status'+event.message.text)
    #elif('關' == in_w):
    #    led_status = '0'
    print ("led狀態:" + led_status)

#if __name__ == "__main__":
def line():
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)
    # main.clock(1, 0000)
