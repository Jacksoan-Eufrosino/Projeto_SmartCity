
import os, time, json
from prometheus_client import start_http_server, Counter, Histogram
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "smartcity/#")
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

MSG_RECEIVED = Counter("iot_messages_received_total", "Messages received by controller", ["device", "app", "topic"])
LAT_HIST = Histogram("iot_e2e_latency_seconds", "End-to-end latency from device timestamp to controller receive", ["device", "app", "topic"],
                     buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0))

def on_message(client, userdata, msg):
    try:
        now = time.time()
        payload = json.loads(msg.payload.decode("utf-8"))
        device = payload.get("device", "unknown")
        app = payload.get("app", "unknown")
        topic = msg.topic
        ts = float(payload.get("timestamp", now))
        latency = max(0.0, now - ts)
        MSG_RECEIVED.labels(device=device, app=app, topic=topic).inc()
        LAT_HIST.labels(device=device, app=app, topic=topic).observe(latency)
        print(f"[controller] {topic} <- {device}/{app} latency={latency:.3f}s")
    except Exception as e:
        print(f"[controller] parse error: {e}")

def main():
    start_http_server(METRICS_PORT)
    client = mqtt.Client(client_id="controller")
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_forever()

if __name__ == "__main__":
    main()
