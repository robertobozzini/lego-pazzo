from EV3_setup import *
from IoT_integration import *

def main():
    global color_sensor_old
    while True:
        if color_sensor.color() != color_sensor_old: # quando cambia colore chiama AWS
            send_update(color_sensor.color())
            
# tutto ok tranne lambda 2/3