import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from EV3_setup import *

client_id = "MyTest Client"
endpoint = "your-iot-endpoint.amazonaws.com"
root_ca = "AmazonRootCA1.pem"
private_key = "private.key"
certificate = "certificate.pem.crt"
topic = "test/topic"

client = AWSIoTMQTTClient(client_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, certificate)

client.connect()


def send_update(color):
    if color == Color.RED:
        client.publish(topic, json.dumps({"id" : "red", "status" : "in"}), 1)
    elif color == Color.BLUE:
        client.publish(topic, json.dumps({"id" : "blue", "status" : "in"}) 1)
        
def modify_status(device, status): # applica le modifiche
    if device == "gate_motor":
        gate_motor.angle(status)

def apply_update(client, userdata, message): # riceve update mandati da IoT
    data = json.loads(message.payload.decode())
    for device, status in data.items():
        modify_status(device, status)