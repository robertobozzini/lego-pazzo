
import boto3
import json
# dynamodb=boto3.resource('dynamodb',region_name='eu-west-1')
# table=dynamodb.Table('Alternanza_CLI')

sns = boto3.client('sns')   
sns_topic_arn = 'arn:aws:sns:REGIONE:ACCOUNT_ID:NotifySecondLambdaTopic'

def lambda_handler(event,context):


    for record in event['Records']:
        sns_message = record['Sns']['Message']
        # Se il messaggio è un JSON string, decodificalo
        try:
            payload = json.loads(sns_message)
        except:
            payload = {"message": sns_message}

        # Supponiamo tu abbia salvato il connectionId da qualche parte (es: DynamoDB)
        connection_id = payload.get("connectionId")  # ← dinamico, es: ricevuto in SNS
        if not connection_id:
            print("Nessun connectionId, impossibile inviare")
            continue

        # Inserisci il dominio e stage della tua API Gateway WebSocket
        domain = "xxxxxx.execute-api.eu-west-1.amazonaws.com"
        stage = "prod"

        apigw = boto3.client("apigatewaymanagementapi",
            endpoint_url=f"https://{domain}/{stage}")

        try:
            apigw.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(payload).encode("utf-8")
            )
            print(f"Inviato messaggio a {connection_id}")
        except apigw.exceptions.GoneException:
            print(f"ConnectionId {connection_id} non valido (disconnesso?)")

    return {'statusCode': 200}