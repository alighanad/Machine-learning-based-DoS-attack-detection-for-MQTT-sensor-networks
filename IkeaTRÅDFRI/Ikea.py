import time
import paho.mqtt.client as mqtt
import datetime
import numpy
import random as rm
#parameters
hour = datetime.datetime.now()
my_hour = int(hour.hour)
evening_peak_time = 19
night_peak_time = 24
state = ["ON","OFF"]
state_list = [1]

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
    print("your room's light is: ", m_decode)
broker ="172.20.10.2"

##MQTT
client = mqtt.Client("python1")
#client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
#######

print("connecting to the broker", broker)
client.connect(broker)
client.loop_start()
client.subscribe("TRÅDFRI/room/bulb/state/isOn")

while True:
    if evening_peak_time < my_hour < night_peak_time:
        prob = numpy.random.choice(numpy.arange(1, 3), p=[0.5, 0.5])
        if prob == 1:
            state_list.append(state[0])
        else:
            state_list.append(state[1])
        if state_list[-1] == state_list[-2]:
            pass
        else:
            client.publish("TRÅDFRI/room/bulb/state/isOn", state_list[-1])
        #print(state_list)
    else:
         prob = numpy.random.choice(numpy.arange(1, 3), p=[0.2, 0.8])
         if prob == 1:
             state_list.append(state[0])
         else:
             state_list.append(state[1])
         if state_list[-1] == state_list[-2]:
             pass
         else:
             client.publish("TRÅDFRI/room/bulb/state/isOn", state_list[-1])
    time.sleep(0.5)
client.loop_stop()
client.disconnect()
