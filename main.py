from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait


ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S3)

def send_update(color):
    if color == Color.RED:
        # chiama IoT e fa 
    elif color == Color.BLUE:
        # chiama IoT e fa