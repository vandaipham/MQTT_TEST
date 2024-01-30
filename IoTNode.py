import paho.mqtt.client as mqtt
from datetime import datetime as dt
import random
import time

broker = 'localhost'
port = 1883

# setup topics to publish
temperature = "yourID/feeds/temperature"
humidity = "yourID/feeds/humidity"
light = "yourID/feeds/light"

# setup topics to subribe
lamp1 = "yourID/feeds/lamp1"
lamp2 = "yourID/feeds/lamp2"
lamp3 = "yourID/feeds/lamp3"

# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}' # can be changed to yourID
username = 'yourID'               # fill in yourID
password = 'yourPassword'      # fill in your password


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code "+str(reason_code))
    client.subscribe(lamp1)
    client.subscribe(lamp2)
    client.subscribe(lamp3)
    
def on_message(client, userdata, message, properties=None):
    print(
        f"{dt.now()} Received message {message.payload} on topic '{message.topic}' with QoS {message.qos}"
    )

def on_subscribe(client, userdata, mid, qos, properties=None):
    print(f"{dt.now()} Subscribed with QoS {qos}")

def on_publish(client, userdata, mid,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Published message id: "+str(mid))

def publish(client):
    while True:
        time.sleep(5)
        t = random.randint(0, 100)
        #msg = f"messages: {msg_count}"
        result = client.publish(temperature, t)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{t}` to topic `{temperature}`")
        else:
            print(f"Failed to send message to topic {temperature}")

        h = random.randint(0, 100)
        #msg = f"messages: {msg_count}"
        result = client.publish(humidity, h)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{h}` to topic `{humidity}`")
        else:
            print(f"Failed to send message to topic {humidity}")

        l = random.randint(0, 1000)
        #msg = f"messages: {msg_count}"
        result = client.publish(light, l)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{l}` to topic `{light}`")
        else:
            print(f"Failed to send message to topic {light}")

client = mqtt.Client(client_id="clientid", protocol=mqtt.MQTTv311, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set(username, password)
client.connect(broker, port, keepalive=60)
client.loop_start()

publish(client)

if KeyboardInterrupt:
    client.unsubscribe(lamp1)
    client.unsubscribe(lamp2)
    client.unsubscribe(lamp3)
    client.disconnect()