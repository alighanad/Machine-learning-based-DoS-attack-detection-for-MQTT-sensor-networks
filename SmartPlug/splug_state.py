import time
import paho.mqtt.client as mqtt
import datetime
import numpy
import random 
import json
from time import localtime, strftime, sleep

#parameters
hour = datetime.datetime.now()
my_hour = int(hour.hour)
states = ["ON","OFF"]
state = states[0]

Rooms =["Room_1","Room_2","Room_3","Room_4","Room_5","Room_6","Room_7","Room_8","Room_9",
        "Room_10","Room_11","Room_12","Room_13","Room_14",
        "Room_15","Room_16","Room_17","Room_18","Room_19","Room_20","corridor"]

Floors = ["Floor_1","Floor_2","Floor_3","Floor_4","Floor_5"]

Splug = ["splug_1","splug_2","splug_3","splug_4","splug_5"]

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
    topic = msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    #m_in=json.loads(m_decode) #decode json data
    print("Plug status is: ", m_decode)
##MQTT
client = mqtt.Client("smartplug-sensor")
#client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
#######

print("connecting to the broker", broker[0])
client.connect(broker[0])
client.loop_start()
client.subscribe("apartment/room_1/splug_1/state/on")
event = 200
times = 1
lambdas = ((event/times)/3600)
#JSON
while True:
    myMsg = {"Room":Rooms[0],
        "Floors": Floors[0],
        "Splug": Splug[0], 
        "Payload":state
        }

    data_out = json.dumps(myMsg)
    power = numpy.random.normal(loc=300, scale=100)
    time.sleep(1/lambdas)
    if power > 200:
        myMsg["Payload"] = states[1]
        data_out = json.dumps(myMsg)

        client.publish("apartment/room_1/splug_1/state", data_out)
        time.sleep(1/lambdas)
        myMsg["Payload"] = states[0]
        data_out = json.dumps(myMsg)

        client.publish("apartment/room_1/splug_1/state", data_out)
 

    
client.loop_stop()
client.disconnect()