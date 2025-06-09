from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S3)
color_sensor_old = color_sensor.color()

def send_update(color):
    if color == Color.RED:
        print(color)
        # Chiama IoT e fa
    elif color == Color.BLUE:
        print(color)
        # Chiama IoT e fa
        
def main():
    while True:
        if color_sensor.color() != color_sensor_old: # quando cambia colore chiama AWS
            color_sensor_old = color_sensor.color()
            send_update(color_sensor.color())