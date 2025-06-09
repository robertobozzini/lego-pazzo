#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# Initialize motors and sensors
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
color_sensor = ColorSensor(Port.S3)

# Set motor speed and direction
def drive(speed, direction):
    if direction == "forward":
        left_motor.run_forever(speed_sp=speed)
        right_motor.run_forever(speed_sp=speed)
    elif direction == "backward":
        left_motor.run_forever(speed_sp=-speed)
        right_motor.run_forever(speed_sp=-speed)
    elif direction == "left":
        left_motor.run_forever(speed_sp=-speed)
        right_motor.run_forever(speed_sp=speed)
    elif direction == "right":
        left_motor.run_forever(speed_sp=speed)
        right_motor.run_forever(speed_sp=-speed)
    else:
        left_motor.stop()
        right_motor.stop()
    
# Example: Drive forward for 5 seconds
drive(50, "forward")
wait(5000) 
drive(0, "stop")

# Example: Turn right
drive(50, "right")
wait(2000)
drive(0, "stop")

# Example: Read color sensor
color_reading = color_sensor.reflected_light_intensity
print(f"Color sensor reading: {color_reading}")

#sensor reading

# Initialize sensors and motors
color_sensor = ColorSensor(Port.S3)
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

while True:
    # Read color sensor
    color_value = color_sensor.reflected_light_intensity
    
    # Example: If color is dark, go forward; otherwise, go backward
    if color_value < 30:
        drive(50, "forward")
        print("Dark color detected. Moving forward.")
    else:
        drive(50, "backward")
        print("Light color detected. Moving backward.")
    
    wait(500)
    
    # Example: Stop motors after 2 seconds
    wait(2000)
    drive(0, "stop")
    
# Define drive function (same as above)
def drive(speed, direction):
    if direction == "forward":
        left_motor.run_forever(speed_sp=speed)
        right_motor.run_forever(speed_sp=speed)
    elif direction == "backward":
        left_motor.run_forever(speed_sp=-speed)
        right_motor.run_forever(speed_sp=-speed)
    elif direction == "left":
        left_motor.run_forever(speed_sp=-speed)
        right_motor.run_forever(speed_sp=speed)
    elif direction == "right":
        left_motor.run_forever(speed_sp=speed)
        right_motor.run_forever(speed_sp=-speed)
    else:
        left_motor.stop()
        right_motor.stop()
