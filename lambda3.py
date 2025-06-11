import json
import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

client_id = "Brick"
endpoint = "a2dvm6ijdlolkr-ats.iot.eu-north-1.amazonaws.com"
root_ca = "AmazonRootCA1.pem"
private_key = "Centralina.private.key"
certificate = "93d66843aaef033a10d941356c43a6f874ff8dfb00ad5a0478cbfd31540c8f03-certificate.pem.crt"
topic= "$aws/things/Centralina/shadow/update/documents"

client = AWSIoTMQTTClient(client_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, certificate)

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('lego-pazzo2')


def lambda_handler(event, context):
    print("WebSocket message received:")
    print(event)
    try:
        newdata=json.loads(event['requestContext']['body'])
    except json.JSONDecodeError:
        return {'statusCode': 201}
    # pk=newdata['PK']
    table.put_item(
        Item=newdata
    )
    
    client.connect()
    client.publish(topic, json.dumps(newdata), 1)
                   
    return {'statusCode': 200}
    # Dati connessione WebSocket
    # connection_id = event['requestContext']['connectionId']
    # domain = event['requestContext']['domainName']
    # stage = event['requestContext']['stage']
    # message = event.get('body', '{}')

    # Invia una risposta al client
    # apigw = boto3.client('apigatewaymanagementapi',
    #     endpoint_url=f"https://{domain}/{stage}")

    # apigw.post_to_connection(
    #     ConnectionId=connection_id,
    #     Data="✅ Messaggio ricevuto. Lo inoltro a SNS.".encode('utf-8')
    # )

    # # Decodifica il messaggio ricevuto (prova a leggere JSON)
    # try:
    #     data = json.loads(message)
    # except json.JSONDecodeError:
    #     data = {"raw": message}

    # # Invia a IoT
    # client.publish(topic_S, json.dumps(data), 1)

