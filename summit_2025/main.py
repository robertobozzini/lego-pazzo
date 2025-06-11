#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import os
import traceback
import time
import ujson
from umqtt import MQTTClient



# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

aws_endpoint = b'10.77.77.122'

#If you followed the blog, these names are already set.
thing_name = "Centralina"
client_id = "test"
# private_key = "private.key.der"
# private_cert = "certificate.der"


topic_pub = "$aws/things/" + thing_name + "/shadow/update"
topic_sub = "$aws/things/" + thing_name + "/shadow/update/accepted"

# Create your objects here.
ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S1)
motor = Motor(Port.A)
color = color_sensor.color()
old_color = color


def mqtt_connect(client=client_id, endpoint=aws_endpoint):
    mqtt = MQTTClient(client_id=client, server=endpoint, port=1883, keepalive=1200)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message, motor.angle())
    if message.get("state", {}).get("reported", {}).get("device", {}).get("client") != "aws":
        pass
    if message.get("state", {}).get("reported", {}).get("sensors", {}).get("motor") == "ON" and motor.angle() != -90:
        motor.run_angle(100, -90)
    elif message.get("state", {}).get("reported", {}).get("sensors", {}).get("motor") == "OFF" and motor.angle() == -90:
        motor.run_angle(100, 90)
    print("Done")


#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
try:
    mqtt = mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)
    mqtt.subscribe(topic_sub)
except Exception as e:
    import sys
    sys.print_exception(e)
    print("Unable to connect to MQTT.")


while True:
#Check for messages.
    try:
        mqtt.check_msg()
    except Exception as e:
        print(e)
        print("Unable to check for messages.")
    if color_sensor.color() != old_color:
        print("Color changed from", old_color, "to", color_sensor.color())
        old_color = color_sensor.color()
        mesg = ujson.dumps({
            "state":{
                "reported": {
                    "device": {
                        "client": client_id,
                        "uptime": time.ticks_ms(),
                    },
                    "sensors": {
                        "light":  str(color_sensor.color()),
                    },
                }
            }
        })

        #Using the message above, the device shadow is updated.
        try:
            mqtt_publish(client=mqtt, message=mesg)
        except Exception as e:
            print(e)
            print("Unable to publish message.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 60 seconds")
    time.sleep(0.5)