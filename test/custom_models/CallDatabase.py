import psycopg2
import os

def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '(user_id, time_record, body_record)'
    postgres_insert_query = f"""INSERT INTO self_body {table_columns} VALUES (%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"恭喜您！ {cursor.rowcount} 筆資料成功紀錄！"
    print(message)

    cursor.close()
    conn.close()
    
    return message


def database_search(user):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    
    postgres_select_query = f"""SELECT * FROM self_body WHERE user_id='{user}' ORDER BY record_no DESC;"""
    
    cursor.execute(postgres_select_query)
    raw = cursor.fetchmany(7)
    message = []
    
    for i in raw:
        message.append(str(i[2]))
        message.append(str(i[3]))
       
    message = str(message)
    
    cursor.close()
    conn.close()
    
    return message

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import pyimgur

def visual_picture(user):
    ### 體溫表 ###
    temp = [ 37.0, 36.4, 36.8, 37.3, 37.8, 38.5,
            37.2, 39.4, 36.3, 36.9, 36.7, 35.5,
            35.7, 36.8, 36.4, 37.1, 36.8, 37.3,
            37.8, 38.4, 38.4, 36.7, 35.4, 36.3, 
            36.9, 36.7, 35.5, 35.7, 36.8, 36.4,]

    dates = [ '2021-11-01', '2021-11-02', '2021-11-03', '2021-11-04',
            '2021-11-05', '2021-11-06', '2021-11-07', '2021-11-08',
            '2021-11-09', '2021-11-10', '2021-11-11', '2021-11-12',
            '2021-11-13', '2021-11-14', '2021-11-15', '2021-11-16',
            '2021-11-17', '2021-11-18', '2021-11-19', '2021-11-20',
            '2021-11-21', '2021-11-22', '2021-11-23','2021-11-24', 
            '2021-11-25', '2021-11-26', '2021-11-27', '2021-11-28', 
            '2021-11-29', '2021-11-30']

    # 設定日期
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

    # Choose some nice levels
    deg = []
    for i in range(30):
        if temp[i] > 36.5:
            degree = temp[i] - 36.5
        else:
            degree = temp[i] - 36.5
        deg.append(degree)

    levels = np.tile(deg,int(np.ceil(len(dates)/30)))[:len(dates)]

    # 創建圖表
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    ax.set(title="November Temperature ( compare with 36.5 )")

    ax.vlines(dates,0 , levels, color="tab:red")  # 垂直線
    ax.plot(dates, np.zeros_like(dates), "-o",
            color="C0", markerfacecolor="w")  # 中間線

    # 設定軸
    for d, l, r in zip(dates, levels, temp):
        ax.annotate(r, xy=(d, l),
                    xytext=(-2, np.sign(l)*3), textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="bottom" if l > 0 else "top")

    # x軸設定
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # 移除多餘之線條
    ax.yaxis.set_visible(False)
    ax.spines["left"].set_visible(False) 
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.margins(y=0.1)
    path = plt.savefig("temp.png")
    im = pyimgur.Imgur(user)
    uploaded_image = im.upload_image(path)
    return uploaded_image.link


