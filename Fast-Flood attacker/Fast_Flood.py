import time
import paho.mqtt.client as mqtt
import datetime
import numpy
import string
import random 
import json
from time import localtime, strftime, sleep
#parameters

Rooms =["Room_1","Room_2","Room_3","Room_4","Room_5","Room_6","Room_7","Room_8","Room_9",
        "Room_10","Room_11","Room_12","Room_13","Room_14",
        "Room_15","Room_16","Room_17","Room_18","Room_19","Room_20","corridor"]
Floors = ["Floor_1","Floor_2","Floor_3","Floor_4","Floor_5"]
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
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    #m_in=json.loads(m_decode) #decode json data
    print("PayLoAd Is: ", m_decode)
##Client
client = mqtt.Client("quickflood")
client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
#######
#Connection
print("connecting to the broker", broker[0])
client.connect(broker[0])
client.loop_start()
client.subscribe("apartment/room_1/fast/state")
#JSON
event = 90000000
times = 1
lambdas = ((event/times)/3600)
max_rand_str_length = 10
def generate_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(random.choice(range(1, max_rand_str_length))))
print(generate_string())
ii = 0
mycodes = []
while ii < 40:
    cc = generate_string()
    mycodes.append(cc)
    ii+=1
while True:
    for item in mycodes:
        client.publish("apartment/room_1/fast/state", item)
        time.sleep(numpy.random.exponential(1/lambdas))

client.loop_stop()
client.disconnect()