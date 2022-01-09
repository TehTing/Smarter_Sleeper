import main_try
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
led_status = ""

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


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
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

    if (event.message.text != led_status):
        led_status = event.message.text # set alert time
        main_try.change(led_status)
    print ("led狀態:" + led_status)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)

