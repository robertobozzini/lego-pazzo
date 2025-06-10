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
        client.publish(topic, json.dumps({"id" : "red_car", "status" : "in"}), 1)
    elif color == Color.BLUE:
        client.publish(topic, json.dumps({"id" : "blue_car", "status" : "in"}), 1)
    elif color_sensor_old == Color.RED:
        client.publish(topic, json.dumps({"id" : "red_car", "status" : "out"}), 1) 
    elif color_sensor_old == Color.BLUE:
        client.publish(topic, json.dumps({"id" : "blue_car", "status" : "out"}), 1) 
    color_sensor_old = color
    
def modify_status(id, status): # applica le modifiche
    if id == "gate_motor":
        gate_motor.angle(status)
    return

def apply_update(client, userdata, message): # riceve update mandati da IoT
    data = json.loads(message.payload.decode())
    for id, status in data.items():
        modify_status(id, status)
        
client.subscribe(topic, 1, apply_update)




#     Turn on your device and make sure it's connected to the internet.
#     Choose how you want to load files onto your device.
#         If your device supports a browser, open the AWS IoT console on your device and run this wizard. You can download the files directly to your device from the browser.
#         If your device doesn't support a browser, choose the best way to transfer files from the computer with the browser to your device. Some options to transfer files include using the file transfer protocol (FTP) and using a USB memory stick.
#     Make sure that you can access a command-line interface on your device.
#         If you're running this wizard on your IoT device, open a terminal window on your device to access a command-line interface.
#         If you're not running this wizard on your IoT device, open an SSH terminal window on this device and connect it to your IoT device.
#     From the terminal window, enter this command:

#     ping a2dvm6ijdlolkr-ats.iot.eu-north-1.amazonaws.com

# After you complete these steps and get a successful ping response, you're ready to continue and connect your device to AWS IoT.