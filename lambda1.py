import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('lego-pazzo2')

def get_all_connection_ids():
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
        ExpressionAttributeValues={
            ":pk": "connessioni",  
            ":prefix": "conn#"
        }
    )
    return [item['SK'].replace("conn#", "") for item in response['Items']]

def send_to_all_connections(data, endpoint_url):
    client = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url=endpoint_url
    )

    connection_ids = get_all_connection_ids()

    for connection_id in connection_ids:
        try:
            client.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(data).encode('utf-8')
            )
        except client.exceptions.GoneException:
            print(f"Connessione {connection_id} non più attiva — rimuovo.")
            table.delete_item(Key={'SK': f'conn#{connection_id}'})

def lambda_handler(event, context):
    print("Evento ricevuto:", event)
    
    message = event.get('payload') or event.get('message') or event
    if isinstance(message, str):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            print("Errore nel parsing del JSON")

    print("Messaggio dopo parsing:", message)
    device = message.get('SK')
    print("Dispositivo:", device)

    if device in ("red_car", "blue_car"):
        id_val_car = device
        car_status = message['stato']

        verifica = table.get_item(Key={'SK': id_val_car, 'PK': 'sensori'})
        item = verifica.get('Item')

        if not item or item.get('stato') != car_status:
            table.update_item(
                Key={'SK': id_val_car, 'PK': 'sensori'},
                UpdateExpression="SET stato = :s",
                ExpressionAttributeValues={":s": car_status}
            )

            updated_item = {"SK": id_val_car, "stato": car_status}

            gate_value = "90" if car_status == "in" else "0"
            table.update_item(
                Key={'SK': "gate_motor", 'PK': 'sensori'},
                UpdateExpression="SET stato = :s",
                ExpressionAttributeValues={":s": gate_value}
            )

            updated_item_gate = {"SK": "gate_motor", "stato": gate_value}

            endpoint = "wss://5l3ibg8vdb.execute-api.eu-north-1.amazonaws.com"  # <-- Metti il tuo endpoint WebSocket

            send_to_all_connections([updated_item, updated_item_gate], endpoint)

    return {
        "statusCode": 200,
        "body": "Dati inviati via WebSocket"
    }