#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import json
import sensor
import artificial_light as al
import natural_light as nl
import paho.mqtt.client as mqtt



ip = "localhost"
port = 1883

nl = nl.Natural_light()   
al1 = al.Artificial_light("al1","al1")
artificial_lights = {
                     's1': al1
                     }
    
def broker_connection(ip, port):
    def on_connect (client, userdata, rc):
        print "Room connected with result code " + str(rc) 
        

    def on_subscribe(client, userdata, mid, granted_qos):
        print "Room Client subscripted "       

    def on_publish(client, userdata, mid):
        print "OP -> " + str(mid)  + " <-"
        
    def on_message(client, obj, msg):
        #set artificial light
        if str(msg.topic == '/room1/commands/'):
            #print str(msg.topic) + "----"
            m = json.loads(msg.payload)
            print m
            for k in m.keys():
                artificial_lights[k].update_lux(int(m[k][1]))
#        print "in message " + str(al1.get_lux())

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish
    client.on_message = on_message

    client.connect(ip, port)
    
    return client


def sensor_publish(client, my_sensor):
    topic = "/"+str(my_sensor.sid)+"/"+str(my_sensor.position)+"/value/"
    meas = {}
    meas['id'] = my_sensor.sid
    meas['position'] = my_sensor.position
    val1 = my_sensor.read_lux(1)
    meas['value'] = val1
    msg = json.dumps(meas)
    client.loop_start()
    client.publish(topic, msg)
    time.sleep(1)
    client.loop_stop()
 

if __name__ == "__main__":

    al1 = al.Artificial_light("al1","al1")
    artificial_lights = {
                     's1': al1
                     }
    al1.set_lux()
    
    my_client = broker_connection(ip,port)
    my_client.subscribe("/room1/commands/")
    my_client.loop()
    while (True):
        s1w = sensor.Sensor("s1", "w", 1, nl)
        s1t = sensor.Sensor("s1", "t", 1, al1)
        
        print al1.get_lux()
            
#        val1 = s1w.read_lux(1)
#        val2 = s1t.read_lux(1)
        time.sleep(1)
        sensor_publish(my_client, s1w)
        sensor_publish(my_client, s1t)
   
    print s1t.read_lux(1)
    




