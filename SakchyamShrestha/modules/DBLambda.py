import os
import json
import boto3
import uuid

def lambda_handler(event, context):
    print("Received event:", event)
    if "Records" not in event:
        return {'status': 'error', 'reason': 'No Records key in event'}

    table_name = os.environ.get('TABLE_NAME', 'WebHealthTableV2')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    for record in event['Records']:
        try:
            message = record['Sns']['Message']
            # If the message is a JSON string, parse it
            try:
                message_dict = json.loads(message)
            except Exception:
                message_dict = {"notification": message}
            item = {
                'id': str(uuid.uuid4()),
                **message_dict
            }
            table.put_item(Item=item)
            print(f"Successfully wrote to DynamoDB: {item}")
        except Exception as e:
            print(f"Error processing record: {e}")
            return {'status': 'error', 'reason': str(e)}

    return {'status': 'success'}