# Publisher 6 App

import time
import random
import paho.mqtt.client as mqtt

BROKER_URL = "127.0.0.1"        # Publisher 6 connects to Broker 6
BROKER_PORT = 1856
BACKUP_BROKER_URL = "127.0.0.1" # Broker 5 is the backup connection if Broker 6 is unavailable
BACKUP_BROKER_PORT = 1855
TOPIC = "state/topic"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to broker {BROKER_URL} with result code {rc}")

def publish_state(client):
    client.loop_start()
    try:
        while True:
            state = random.randint(1, 100)  # Simulate some state
            print(f"Publishing state: {state} to {BROKER_URL}:{BROKER_PORT}")
            client.publish(TOPIC, state)
            time.sleep(10)  # Publish every n seconds
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    
    try:
        client.connect(BROKER_URL, BROKER_PORT)
    except Exception as e:
        print(f"Failed to connect to {BROKER_URL}, trying backup broker {BACKUP_BROKER_URL}:{BACKUP_BROKER_PORT}")
        client.connect(BACKUP_BROKER_URL, BACKUP_BROKER_PORT)

    publish_state(client)
