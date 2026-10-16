import json
from mysql_db import connect_mysql, read_mysql, close_mysql
from mqtt import publish_mqtt
import logging

# 設定 Log
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
    filemode="a"
)

# 讀取設定檔
def load_config():
    with open("conf.json", "r", encoding="utf-8") as f:
        return json.load(f)


# 主程式
def main():
    config = load_config()
    conn = connect_mysql(config)

    if conn:
        try:
            for device in config["device"]:
                result = read_mysql(conn, config, device)

                # 發布 MQTT
                if result is not None:
                    publish_mqtt(config, result, device)
                else:
                    logging.warning("查無資料")

        finally:
            close_mysql(conn)

        

if __name__ == "__main__":
    main()