from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import configparser

import random

# 我們的函數
from custom_models import utils, CallDatabase

# LINE 聊天機器人的基本資料
# LINE 聊天機器人的基本資料
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('7HIKsSlQ98H6GVbpIx0KfcuXsx2XX2bXLYTu2vUVkTvYhE0GbU4fkgEs9VIwJfrEve85utAj4QaR3EZp+JPawNfOcy1J7ZYMORKm24vEMy+nbxTNpVlPlms7tJkSWefRZlfPabqhDIKWKzh1YTD9agdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d8ef60b9201703c56b1ca87cce1a26ff')


# 請 LINE 幫我們存入資料
def insert_record(event):
    
    if '暱稱' and '日期' and '今日狀況' in event.message.text:
        
        try:
            record_list = utils.prepare_record(event.message.text) 
            reply = CallDatabase.line_insert_record(record_list)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )

        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='失敗了')
            )

        return True
    else:
        return False

# 請 pixabay 幫我們找圖
def img_search(event):
    
    try:
        try:
            img_source = event.message.text.split(' ')[0].lower()
            target = event.message.text.split(' ')[1]
            random_img_url = utils.get_img_url(img_source=img_source, target=target)
            
        except:
            random_img_url = utils.get_img_url(img_source='pixabay', target=event.message.text)

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=random_img_url,
                preview_image_url=random_img_url
            )
        )
        
        return True
    
    except:
        return False
            
def pretty_echo(event):
    pretty_note = '♫♪♬'
    pretty_text = ''

    for i in event.message.text:

        pretty_text += i
        pretty_text += f" {random.choice(pretty_note)} "

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=pretty_text)
    )
    
    return True

#查詢資料庫資料
def find_record_data(event):
    if '查詢紀錄:' in event.message.text:
        try:
            user = utils.find_userid(event.message.text) 
            message = CallDatabase.database_search(user)
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='找不到，請確認輸入')
            )

        return True
    else:
        return False

def get_visualize(event):
    if '我要看視覺化:' in event.message.text:
        try:
            user = utils.find_userid(event.message.text) 
            #message = CallDatabase.database_search(user)
            message = user + "此功能建立中，請期待"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='找不到，請確認輸入')
            )

        return True
    else:
        return False