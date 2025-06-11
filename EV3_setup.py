from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S1)
color_sensor_old = color_sensor.color()
gate_motor = Motor(Port.A)
gate_motor.reset_angle(0)
red_lights = Motor(Port.B)
blue_lights = Motor(Port.C)