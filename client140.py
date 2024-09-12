# Client 140 App

import paho.mqtt.client as mqtt

BROKER_URL = "127.0.0.1"  # Single endpoint; brokers are bridged
PORT = 1855
TOPIC = "state/topic"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_URL, PORT, 60)
    client.loop_forever()
