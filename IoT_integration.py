import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from EV3_setup import *

client_id = "Brick"
endpoint = "a2dvm6ijdlolkr-ats.iot.eu-north-1.amazonaws.com"
root_ca = "AmazonRootCA1.pem"
private_key = "Centralina.private.key"
certificate = "93d66843aaef033a10d941356c43a6f874ff8dfb00ad5a0478cbfd31540c8f03-certificate.pem.crt"
topic = "$aws/things/Centralina/shadow/update/accepted"

client = AWSIoTMQTTClient(client_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, certificate)

client.connect()

def send_update(color):
    if color == Color.RED:
        client.publish(topic, json.dumps({"pk" : "sensori", "sk" : "red_car", "stato" : "in"}), 1)
    elif color == Color.BLUE:
        client.publish(topic, json.dumps({"pk" : "sensori", "sk" : "blue_car", "stato" : "in"}), 1)
    elif color_sensor_old == Color.RED:
        client.publish(topic, json.dumps({"pk" : "sensori", "sk" : "red_car", "stato" : "out"}), 1) 
    elif color_sensor_old == Color.BLUE:
        client.publish(topic, json.dumps({"pk" : "sensori", "sk" : "blue_car", "stato" : "out"}), 1) 
    color_sensor_old = color
    
def modify_stato(pk, sk, stato): # applica le modifiche
    # if pk == "sensori":
    #     if(sk == "gate_motor"):
    #         gate_motor.angle(int(stato))
    #     elif(sk == "red_lights"):
    #         red_lights.dc(100)
    #     elif(sk == "blue_lights"):
    #         blue_lights.dc(100)
    print(pk, sk, stato)

def apply_update(client, userdata, message): # riceve update mandati da IoT
    data = json.loads(message.payload.decode())
    for pk, sk, stato in data.items():
        modify_stato(pk, sk, stato)
        
client.subscribe(topic, 1, apply_update)

while True:
    client.publish(topic, json.dumps({"pk" : "sensori", "sk" : "red_car", "stato" : "in"}), 1)
    client.publish(topic, json.dumps({"pk" : "sensori", "sk" : "red_car", "stato" : "out"}), 1) 


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

# unzip connect_device_package.zip
# chmod +x start.sh
# ./start.sh