# Client 140 App

import paho.mqtt.client as mqtt

BROKER_URL = "127.0.0.1"            # Primary brkoer host; brokers are bridged
BROKER_PORT = 1855                  # Primary broker port; brokers are bridged
BACKUP_BROKER_URL = "127.0.0.1"     # Broker 6 is the backup connection if Broker 5 is unavailable
BACKUP_BROKER_PORT = 1856           # bROKER 6 port
TOPIC = "state/topic"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker at {BROKER_URL}:{BROKER_PORT} with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Attempt to connect to Broker 1
    try:
        client.connect(BROKER_URL, BROKER_PORT, 60)
    except Exception as e:
        print(f"Failed to connect to {BROKER_URL}:{BROKER_PORT}, trying backup broker {BACKUP_BROKER_URL}:{BACKUP_BROKER_PORT}")
        client.connect(BACKUP_BROKER_URL, BACKUP_BROKER_PORT, 60)

    client.loop_forever()
