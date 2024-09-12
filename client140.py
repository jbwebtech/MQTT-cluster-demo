# Client 140 App

import paho.mqtt.client as mqtt

BROKER_URL = "127.0.0.1"            # Primary brkoer host; brokers are bridged
BROKER_PORT = 1855                  # Primary broker port; brokers are bridged
BACKUP_BROKER_URL = "127.0.0.1"     # Broker 6 is the backup connection if Broker 6 is available
BACKUP_BROKER_PORT = 1856           # Broker 6 port
TOPIC = "state/topic"

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
    print(f"Connected to MQTT Broker at {BROKER_URL}:{BROKER_PORT} with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    """
    MQTT callback for when a PUBLISH message is received from the server.

    Prints a message with the received payload and topic

    :param client: MQTT client instance
    :param userdata: User data set in Client() or userdata_set()
    :param msg: Message object with topic and payload
    """
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
