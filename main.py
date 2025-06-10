from EV3_setup import *
from IoT_integration import *
import json

def main():
    client.subscribe(topic, 1, apply_update)
    global color_sensor_old
    while True:
        if color_sensor.color() != color_sensor_old: # quando cambia colore chiama AWS
            color_sensor_old = color_sensor.color()
            send_update(color_sensor.color())