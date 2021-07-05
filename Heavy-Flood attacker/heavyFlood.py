import time
import paho.mqtt.client as mqtt
import datetime
import numpy as np
import string
import random 
import json
from time import localtime, strftime, sleep
#parameters

broker =["172.20.10.2","test.mosquitto.org"]
#MQTT FUNCTIONS
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
    time.sleep(1)
    with open("data.csv", 'wb') as fd:
        fd.write(msg.payload)

##Client
client = mqtt.Client("heavyflood")
client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
#######


#Connection
print("connecting to the broker", broker[0])
client.connect(broker[0],keepalive=1)

client.loop_start()
client.subscribe("apartment/room_1/s/state",qos=2)


f = open("t.csv")
sendfile = f.read()
byteArray = bytearray(sendfile,"utf-8")
event = 900000000

times = 1
lambdas = ((event/times)/3600)
while True:
    client.publish("apartment/room_1/s/state", byteArray,qos=2)
    time.sleep(np.random.exponential(1/lambdas))
client.loop_stop()
client.disconnect()