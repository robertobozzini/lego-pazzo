import json
import boto3

sns = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:REGIONE:ACCOUNT_ID:NOME_TOPIC'

def lambda_handler(event, context):
    print("WebSocket message received:")
    print(event)

    # Dati connessione WebSocket
    connection_id = event['requestContext']['connectionId']
    domain = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    message = event.get('body', '{}')

    # Invia una risposta al client
    apigw = boto3.client('apigatewaymanagementapi',
        endpoint_url=f"https://{domain}/{stage}")

    apigw.post_to_connection(
        ConnectionId=connection_id,
        Data="✅ Messaggio ricevuto. Lo inoltro a SNS.".encode('utf-8')
    )

    # Decodifica il messaggio ricevuto (prova a leggere JSON)
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        data = {"raw": message}

    # Invia a SNS
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=json.dumps(data)
    )

    return {'statusCode': 200}
