import mysql.connector
from datetime import datetime, timedelta
import logging



# 建立 MySQL 連線
def connect_mysql(config):
    try:
        conn = mysql.connector.connect(
            host=config["mySql"]["host"],
            port=int(config["mySql"]["port"]),
            database=config["mySql"]["database"],
            user=config["mySql"]["user"],
            password=config["mySql"]["password"],
            connection_timeout=10,
            use_pure=True
        )
        return conn

    except mysql.connector.Error as e:
        logging.warning(f"MySQL 連線失敗: {e}")
        return None


# 查詢 MySQL 資料
def read_mysql(conn, config, device):
    query_time = (datetime.now() - timedelta(hours=1)).replace(
        minute=0, second=0, microsecond=0
    )

    cursor = conn.cursor()

    try:
        table = config["mySql"]["table"]
        cursor.execute(
            f"SELECT MValue FROM `{table}` WHERE MStation={device['MStation']} AND Mitem=1 AND MDate=%s",
            (query_time,)
        )

        row = cursor.fetchone()
        result = row[0] if row else None

        return result

    finally:
        cursor.close()


# 關閉 MySQL 連線
def close_mysql(conn):
    if conn:
        conn.close()
        print("MySQL 連線已關閉")
