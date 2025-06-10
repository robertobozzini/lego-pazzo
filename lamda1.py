import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NomeTabella')

def lambda_handler(event, context):
    # Event SNS contiene Records -> [ { Sns: { Message: ... } } ]
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        
        device=message['device']

        if device=="car":
            id_val_car = message['id']
            car_status = message['status']  # esempio: {"status": "active", "count": 12}

            update_expression = "SET status = :s"
            expr_vals = {":s": car_status}

            table.update_item(
                Key={'id': id_val_car},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expr_vals
            )

            id_gate="gatemotor"
            gate_status=message['status']   

            if gate_status=="in":
                expr_vals={":s": 90}   

                table.update_item(
                    Key={'id':'gate'},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expr_vals
                )
            else:
                expr_vals={":s": 0}   
                table.update_item(
                    Key={'id':'gate'},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expr_vals
                )

            if id_val_car=="red":
                #cambiamo alcuni sensori
            else:
                #cambio altri
    
    


    return {"statusCode": 200}
