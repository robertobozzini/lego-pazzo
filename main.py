from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

client_id = "MyTestClient"
endpoint = "your-iot-endpoint.amazonaws.com"
root_ca = "AmazonRootCA1.pem"
private_key = "private.key"
certificate = "certificate.pem.crt"
topic = "test/topic"

client = AWSIoTMQTTClient(client_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, certificate)

client.connect()

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S3)
color_sensor_old = color_sensor.color()

def send_update(color):
    if color == Color.RED:
        client.publish(topic, "RED IN", 1)
    elif color == Color.BLUE:
        client.publish("my/topic", "BLUE IN", 1)
        

def apply_update(client, userdata, message): # applica update mandati da IoT
    print(message.payload.deocde())
    
client.subscribe(topic, 1, apply_update)       


def main():
    while True:
        if color_sensor.color() != color_sensor_old: # quando cambia colore chiama AWS
            color_sensor_old = color_sensor.color()
            send_update(color_sensor.color())