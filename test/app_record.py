from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

from custom_models import utils, PhoebeTalks

app = Flask(__name__)

# LINE 聊天機器人的基本資料
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('7HIKsSlQ98H6GVbpIx0KfcuXsx2XX2bXLYTu2vUVkTvYhE0GbU4fkgEs9VIwJfrEve85utAj4QaR3EZp+JPawNfOcy1J7ZYMORKm24vEMy+nbxTNpVlPlms7tJkSWefRZlfPabqhDIKWKzh1YTD9agdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d8ef60b9201703c56b1ca87cce1a26ff')



# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 紀錄資料
@handler.add(MessageEvent, message=TextMessage)
def reply_text_message(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        reply = False
        #加入紀錄
        if not reply:
            reply = PhoebeTalks.insert_record(event)
        #查看文字紀錄
        if not reply:
            reply = PhoebeTalks.find_record_data(event)
        #查看視覺化紀錄
        if not reply:
            reply = PhoebeTalks.get_visualize(event)

        if not reply:
            reply = PhoebeTalks.img_search(event)
                    
        if not reply:
            reply = PhoebeTalks.img_search(event)

        if not reply:
            reply = PhoebeTalks.index_flex(event)

        if not reply:
            reply = PhoebeTalks.pretty_echo(event)
        

if __name__ == "__main__":
    app.run()