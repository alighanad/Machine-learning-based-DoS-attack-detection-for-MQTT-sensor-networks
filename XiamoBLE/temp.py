import paho.mqtt.client as mqtt
import time
import random

def on_log(client, userdata, level,buf):
    print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected ok")
    else:
        print("bad connection returned code: ", rc)
def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected result code "+str(rc))
def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("your room's temperature is: ", m_decode)
broker ="172.20.10.2"

client = mqtt.Client("python1")

#client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message

print("connecting to the broker", broker)
client.connect(broker)
client.loop_start()
client.subscribe("evohome/room/temp")
while True:
    temp = random.randrange(17, 25)
    client.publish("evohome/room/temp",temp)
    time.sleep(2)
client.loop_stop()
client.disconnect()
