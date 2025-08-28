
import os, time, json, random, string, sys
from prometheus_client import start_http_server, Counter
import paho.mqtt.client as mqtt

DEVICE_NAME = os.getenv("DEVICE_NAME", "SensorX")
APP = os.getenv("APP", "generic")
TOPIC = os.getenv("TOPIC", "smartcity/test")
BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = float(os.getenv("INTERVAL_SECONDS", "5"))
PAYLOAD_BYTES = int(os.getenv("PAYLOAD_BYTES", "256"))
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

# Prometheus metrics
MSG_SENT = Counter("iot_messages_sent_total", "Messages published by device", ["device", "app", "topic"])

# Start metrics server
start_http_server(METRICS_PORT)

client = mqtt.Client(client_id=f"{DEVICE_NAME}")
client.connect(BROKER, PORT, 60)

msg_id = 0

def make_payload(target_bytes: int):
    # base payload
    data = {
        "device": DEVICE_NAME,
        "app": APP,
        "msg_id": None,  # to be filled
        "timestamp": time.time(),
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
    }
    s = json.dumps(data, separators=(',', ':'))
    pad_len = max(0, target_bytes - len(s))
    if pad_len > 0:
        data["pad"] = "".join(random.choice(string.ascii_letters) for _ in range(pad_len))
    return data

while True:
    msg_id += 1
    payload = make_payload(PAYLOAD_BYTES)
    payload["msg_id"] = msg_id
    payload["timestamp"] = time.time()
    client.publish(TOPIC, json.dumps(payload))
    MSG_SENT.labels(device=DEVICE_NAME, app=APP, topic=TOPIC).inc()
    print(f"[{DEVICE_NAME}] Published to {TOPIC}: id={msg_id}, size≈{PAYLOAD_BYTES}B")
    time.sleep(INTERVAL)
