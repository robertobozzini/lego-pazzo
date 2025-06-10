import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('lego-pazzo')

sns = boto3.client('sns')   
sns_topic_arn = 'arn:aws:sns:REGIONE:ACCOUNT_ID:NotifySecondLambdaTopic'


def lambda2_send():
    response=table.scan()
    items=response['Items']
    
    sns.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps({"records": items})
    )

    return {"statusCode": 200, "message": "Inviato a SNS"}



def lambda_handler(event, context):
    # Event SNS contiene Records -> [ { Sns: { Message: ... } } ]
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        
        device=message['id']

        if device=="red_car" or "blue_car":
            id_val_car = message['id']
            car_status = message['status']  # esempio: {"status": "active", "count": 12}

            verifica=table.get_item(
                Key={'id': id_val_car}
            )
            item = verifica.get('Item')

            if item and item.get('status')==car_status:
                continue

            update_expression = "SET status = :s"
            expr_vals = {":s": car_status}

            table.update_item(
                Key={'id': id_val_car},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expr_vals
            )

            id_gate="gate_motor"
            gate_status=message['status']   

            if gate_status=="in":
                expr_vals={":s": 90}   

                table.update_item(
                    Key={'id':id_gate},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expr_vals
                )
            else:
                expr_vals={":s": 0}   
                table.update_item(
                    Key={'id':id_gate},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expr_vals
                )

            if id_val_car=="red_car":
                #cambiamo alcuni sensori
                continue
            else:
                #cambio altri
                continue
    
    lambda2_send()
    


    return {"statusCode": 200}
