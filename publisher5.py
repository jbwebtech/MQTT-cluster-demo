# Publisher 5 App

import time
import random
import paho.mqtt.client as mqtt

PRIMARY_BROKER_URL = "127.0.0.1"    # Publisher 5 connects to Broker 5
PRIMARY_BROKER_PORT = 1855          # Broker 5 port
BACKUP_BROKER_URL = "127.0.0.1"     # Backup Broker connection if Broker 6 is available
BACKUP_BROKER_PORT = 1856           # Broker 6 port

TOPIC = "state/topic"
SYNC_TOPIC = "sync/state"           # Topic to synchronize state between publishers
HEARTBEAT_TOPIC = "heartbeat/check" # Heartbeat topic to check the availability of the other publisher
HEARTBEAT_MESSAGE = "publisher5"    # Heartbeat message from Publisher 5

state = 0  # Shared state to maintain consistency

def on_connect(client, userdata, flags, rc):
    print(f"Connected to broker {PRIMARY_BROKER_URL}:{PRIMARY_BROKER_PORT} with result code {rc}")
    # Subscribe to synchronization topics
    client.subscribe(SYNC_TOPIC)
    client.subscribe(HEARTBEAT_TOPIC)

def on_message(client, userdata, msg):
    global state
    if msg.topic == SYNC_TOPIC:
        state = int(msg.payload.decode())  # Update state from sync messages
        print(f"Received synchronized state: {state}")
    elif msg.topic == HEARTBEAT_TOPIC:
        print(f"Heartbeat received: {msg.payload.decode()}")  # Monitor heartbeats

def publish_state(client):
    global state
    client.loop_start()
    try:
        while True:
            state = random.randint(1, 100)  # Simulate some state
            print(f"Publishing state: {state} to {PRIMARY_BROKER_URL}:{PRIMARY_BROKER_PORT}")
            client.publish(TOPIC, state)
            client.publish(SYNC_TOPIC, state)  # Synchronize state
            client.publish(HEARTBEAT_TOPIC, HEARTBEAT_MESSAGE)  # Send heartbeat
            time.sleep(15)  # Publish every n seconds
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Attempt to connect to the primary broker
    try:
        client.connect(PRIMARY_BROKER_URL, PRIMARY_BROKER_PORT)
    except Exception as e:
        print(f"Failed to connect to {PRIMARY_BROKER_URL}:{PRIMARY_BROKER_PORT}, trying backup broker {BACKUP_BROKER_URL}:{BACKUP_BROKER_PORT}")
        client.connect(BACKUP_BROKER_URL, BACKUP_BROKER_PORT)

    publish_state(client)
