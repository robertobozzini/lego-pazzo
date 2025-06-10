from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S1)
color_sensor_old = color_sensor.color()
gate_motor = Motor(Port.A)
gate_motor.reset_angle(0)