from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#======這裡是呼叫的檔案內容=====
from message import *
from Function import *
import Globals
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========


scope = ["",'',"",""]
creds = ServiceAccountCredentials.from_json_keyfile_name("YOURJSONFILE", scope)
client = gspread.authorize(creds)
sheet = client.open("練團室時間表").sheet1  # Open the spreadhseet 


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('')
# Channel Secret
handler = WebhookHandler('')

# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(Globals.state)
    if 'exit()' in msg:
        Globals.state.clear()
        message = exitbut()
        line_bot_api.reply_message(event.reply_token, message)
    elif '建立預約' in msg:
        Globals.state.append('create')
        message = alone_or_group()
        line_bot_api.reply_message(event.reply_token, message)
    elif '取消預約' in msg:
        Globals.state.append('cancel')
        message = what_your_name()
        line_bot_api.reply_message(event.reply_token, message)
    elif not Globals.state:
        message = starting()
        line_bot_api.reply_message(event.reply_token, message)
    elif '我想要個練' in msg:
        Globals.state.append("alone")
        date_compensate(time.localtime(time.time()+8*3600))
        message = which_day(Globals.state[-1])
        line_bot_api.reply_message(event.reply_token, message)
    elif '我想要團練' in msg:
        Globals.state.append("group")
        date_compensate(time.localtime(time.time()+8*3600))
        message = which_day(Globals.state[-1])
        line_bot_api.reply_message(event.reply_token, message)
    elif '/' in msg:
        Globals.state.append(msg)
        if Globals.state[0] == "create": message = how_long()
        else: message = cancelling()
        line_bot_api.reply_message(event.reply_token, message)
    elif '小時' in msg:
        Globals.state.append(int(msg[0]))
        message = pick_a_time()
        line_bot_api.reply_message(event.reply_token, message)
    elif '_' in msg:
        Globals.state.append(msg)
        if Globals.state[0] == "create": message = booking()
        else: message = which_day()
        line_bot_api.reply_message(event.reply_token, message)
    elif '.' in msg:
        start = int(msg[0:-1])
        if start < 8 or start > 21:
            message = TextSendMessage(text="二活開放時間為8.~22.請輸入24小時制的時間")
        else:
            Globals.state.append(start)
            message = what_your_name()
        line_bot_api.reply_message(event.reply_token, message)
    
    elif '到' in msg:
        Globals.state.append(msg)
        message = erase()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text='不好意思您輸入的字詞無效請再輸入一次')
        line_bot_api.reply_message(event.reply_token, message)
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
