
import boto3
import json
ddb=boto3.resource('dynamodb',region_name='eu-north-1')
# table=dynamodb.Table('Alternanza_CLI')
table = ddb.Table('lego-pazzo')
def lambda_handler(event, context):

    connection_id = event['requestContext']['connectionId']
    # ddb = boto3.resource('dynamodb')
    if(instruction==0):
        table.put_item(Item={'PK':'connection','SK':connection_id,'stato':1})
    else:
        table.delete_item(Key={'PK':"connection",'SK':connection_id})
    return {'statusCode': 200}