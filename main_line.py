import try_alarm
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

path=sys.argv[0]
print(path)

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
text = "Enter the action you want to do:\nturn on & set alarm time\nformate(2359)\nturn off"
# line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text))
#line_bot_api.push_message('to', TextSendMessage(text=text))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
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
'''
@app.route("/")
def control_led():
    print("led")
    global led_status
    return led_status
'''

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    
    if event.message.text == 'turn off':
        #try:
        try_alarm.off()
        text = "The alarm sucessfully turned off."
        '''
        except Error:
            text = "Eoor: fail to turn off"
        finally:
        '''
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text))
    else:
        global set_alarm
        text="set alarm"+ event.message.text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text))
        try_alarm.change(event.message.text)

    print (event.message.text)
    '''
    if event.message.text == 'set time':
        text = "please enter the time you want to set\nformate(2359)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text))
    '''
    # led_status = event.message.text # set alert time
        # main_clock.change(led_status)
    # print ("led狀態:" + led_status)

if __name__ == "__main__":
    global set_alarm
    set_alarm="0000"
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)

