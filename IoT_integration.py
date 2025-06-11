import json
from time import sleep
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

def create_json(car, action):
    if car == "red_car" == action == "in" == True:
        return json.dumps({"sensors" : {"PK" : "sensori", "SK" : "red_car", "stato" : "in"}, "client": "test"})
    elif car =="blue_car" == action == "in" == True:
        return json.dumps({"sensors" : {"PK" : "sensori", "SK" : "blue_car", "stato" : "in"}, "client": "test"})
    elif car == "red_car" == action == "out" == True:
        return json.dumps({"sensors" : {"PK" : "sensori", "SK" : "red_car", "stato" : "out"}, "client": "test"})
    else:
        return json.dumps({"sensors" : {"PK" : "sensori", "SK" : "blue_car", "stato" : "out"}, "client": "test"})

def send_update(color):
    if color == Color.RED:
        client.publish(topic, create_json("red_car", "in"), 1)
    elif color == Color.BLUE:
        client.publish(topic, create_json("blue_car", "in"), 1)
    elif color_sensor_old == Color.RED:
        client.publish(topic, create_json("red_car", "out"), 1) 
    elif color_sensor_old == Color.BLUE:
        client.publish(topic, create_json("blue_car", "out"), 1) 
    color_sensor_old = color
    
def modify_stato(PK, SK, stato): # applica le modifiche
    # if PK == "sensori":
    #     if(SK == "gate_motor"):
    #         gate_motor.angle(int(stato))
    #     elif(SK == "red_lights"):
    #         red_lights.dc(100)
    #     elif(SK == "blue_lights"):
    #         blue_lights.dc(100)
    print(PK, SK, stato)
    
def apply_update(client, userdata, message): # riceve update mandati da IoT
    data = json.loads(message.payload.decode())
    print("Recv : ", data)
    # modify_stato(it.get("PK"), it.get("SK"), it.get("stato"))
    # for it in data:
        
client.subscribe(topic, 1, apply_update)

while True:
    continue
    # sleep(1)
    
# {'state': {'reported': {'sensors': {'light': 'Color.BLACK'}, 'device': {'client': 'test', 'uptime': 1153125}}},
# 'metadata': {'reported': {'sensors': {'light': {'timestamp': 1749633960}},'device': {'client': {'timestamp': 1749633960}, 'uptime': {'timestamp': 1749633960}}}},
# 'version': 220, 'timestamp': 1749633960}

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