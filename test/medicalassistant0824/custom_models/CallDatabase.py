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