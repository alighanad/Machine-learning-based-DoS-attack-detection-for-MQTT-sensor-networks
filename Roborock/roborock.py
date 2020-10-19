import time
import random
import paho.mqtt.client as mqtt

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
    print("your room's TV is: ", m_decode)
broker ="192.168.1.2"

client = mqtt.Client("python1")

#client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message

print("connecting to the broker", broker)
client.connect(broker)
client.loop_start()
client.subscribe("roborock/room/status/isOn")
while True:
    state = random.choice(['ON', 'OFF'])
    client.publish("roborock/room/status/isOn",state)
time.sleep(1000)
client.loop_stop()
client.disconnect()
