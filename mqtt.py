
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import logging

# 讀取設定檔
def load_config():
    with open("conf.json", "r", encoding="utf-8") as f:
        return json.load(f)


def publish_mqtt(config, value, device):
    mqtt_config = config["mqtt"]

    # 從 MQTT topic1 取得 ID
    topic = device["topic"]
    device_id = topic.split("/")[2]
    lat = device["lat"]
    lon = device["lon"]

    # 組合 JSON 資料
    payload = {
        "id": device_id,
        "lat": lat,
        "lon": lon,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": [
            {
                "sensor": "pm10",
                "value": round(float(value), 1),
                "unit": "µg/m3"
            }
        ]
    }
    payload_json = json.dumps(payload, ensure_ascii=False)

    # 建立 MQTT Client
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=mqtt_config["client_id"]
    )

    try:
        client.connect(
            mqtt_config["host"],
            int(mqtt_config["port"]),
            keepalive=60
        )

        client.loop_start()

        # 發布 MQTT
        info = client.publish(
            topic=topic,
            payload=payload_json,
            qos=int(mqtt_config["qos"])
        )

        info.wait_for_publish(timeout=10)

        if info.is_published():
            logging.info("MQTT 發布成功: %s", payload_json)
        else:
            logging.warning("MQTT 發布未完成")

    except Exception as e:
        logging.exception("MQTT 發布失敗")

    finally:
        client.disconnect()
        client.loop_stop()