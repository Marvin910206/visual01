from __future__ import unicode_literals

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage

import configparser

from apscheduler.schedulers.blocking import BlockingScheduler
import urllib
import datetime

# LINE 聊天機器人的基本資料
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('7HIKsSlQ98H6GVbpIx0KfcuXsx2XX2bXLYTu2vUVkTvYhE0GbU4fkgEs9VIwJfrEve85utAj4QaR3EZp+JPawNfOcy1J7ZYMORKm24vEMy+nbxTNpVlPlms7tJkSWefRZlfPabqhDIKWKzh1YTD9agdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d8ef60b9201703c56b1ca87cce1a26ff')


sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON =========')
    print('This job runs every weekday */20 min.')
    print(f'{datetime.datetime.now().ctime()}')
    print('========== APScheduler CRON =========')

    url = "https://medicalassistant0824.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)
        

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=6, minute=30)
def scheduled_job():
    print('========== APScheduler CRON =========')
    print('This job is run every weekday at 6:30')
    print('========== APScheduler CRON =========')

    line_bot_api.push_message(to, TextSendMessage(text=push_text))

sched.start()