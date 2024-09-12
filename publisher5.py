# Publisher 5 App

import time
import random
import paho.mqtt.client as mqtt

BROKER_URLS = [("localhost", 1855), ("localhost", 1856)]  # Broker 5 and Broker 6
TOPIC = "state/topic"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def publish_state(client, broker_url):
    client.connect(*broker_url)
    client.loop_start()
    
    try:
        while True:
            state = random.randint(1, 100)  # Simulate some state
            print(f"Publishing state: {state} to {broker_url}")
            client.publish(TOPIC, state)
            time.sleep(30)  # Publish every n seconds
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    for broker_url in BROKER_URLS:
        client = mqtt.Client()
        client.on_connect = on_connect
        publish_state(client, broker_url)
