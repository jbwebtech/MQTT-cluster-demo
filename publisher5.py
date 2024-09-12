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
    """
    MQTT callback for when the client receives a CONNACK response from the server.

    The value of rc determines success or not:
        0: Connection successful
        1: Connection refused - incorrect protocol version
        2: Connection refused - invalid client identifier
        3: Connection refused - server unavailable
        4: Connection refused - bad username or password
        5: Connection refused - not authorised
        6-255: Currently unused.

    :param client: MQTT client instance
    :param userdata: User data set in Client() or userdata_set()
    :param flags: Response flags sent by the broker
    :param rc: Result code from the broker
    """
    print(f"Connected to broker {PRIMARY_BROKER_URL}:{PRIMARY_BROKER_PORT} with result code {rc}")
    # Subscribe to synchronization topics
    client.subscribe(SYNC_TOPIC)
    client.subscribe(HEARTBEAT_TOPIC)

def on_message(client, userdata, msg):
    """
    MQTT callback for when a PUBLISH message is received from the server.

    Updates the shared state and prints a message when a sync message is received
    from the other publisher. Also prints a message when a heartbeat is received
    from the other publisher.

    :param client: MQTT client instance
    :param userdata: User data set in Client() or userdata_set()
    :param msg: Message object with topic and payload
    """
    global state
    if msg.topic == SYNC_TOPIC:
        state = int(msg.payload.decode())  # Update state from sync messages
        print(f"Received synchronized state: {state}")
    elif msg.topic == HEARTBEAT_TOPIC:
        print(f"Heartbeat received: {msg.payload.decode()}")  # Monitor heartbeats

def publish_state(client):
    """
    Publishes a random state to the broker every n seconds and synchronizes it across publishers.
    
    :param client: MQTT client instance
    """
    
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
