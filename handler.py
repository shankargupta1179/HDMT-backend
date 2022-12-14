import json
import boto3

client = boto3.client('dynamodb')

def get_data(event, context):
    data = client.get_item(TableName='HDMT-Table',
    Key = {
         'pk': {
             'S': '2022'
         },
         'sk': {
             'S': '2022#CU'
         }
     })
    response={
         'statusCode':200,
         'body': json.dumps(data),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response
    # # get the item from the table
    # response = table.get_item(Key=key)
    # item = response['Item']


def post_data(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    # key = {
    #     'pk': '2022',
    #     'sk': '2022#CU',
    #     'entity_name': 'Chandigarh University',
    #     'date': "12/12/2022",
    #     'admin_name':'sourabh',
    #     'placement_coordinator': 'Amanpreet Singh Dhillon',
    #     'contact_entity': 8798987876,
    #     'email_entity': 'ams@gmail.com'
    # }
    
    key = json.loads(event.get('body'))
    response =table.put_item(Item=key)
    
    return {
        'statusCode': 200,
        'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response)
    }

def update_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    response = table.update_item(
        Key={
            'pk': '2022',
        },
        UpdateExpression = 'SET admin_name = :val1, contact_entity= :val2',
        ExpressionAttributeValues={
            ':val1': "awanti",
            ':val2': 7456981237
         }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_panelist_data(event,context):
    data = client.get_item(TableName='HDMT-Table',
    Key = {
         'pk': {
             'S': '2022'
         },
         'sk': {
             'S': '2022#CU'
         }
     })
    response={
         'statusCode':200,
         'body': json.dumps(data),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response

def post_panelist_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    key = json.loads(event.get('body'))
    response =table.put_item(Item=key)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }

def get_panel_data(event,context):
    data = client.get_item(TableName='HDMT-Table',
    Key = {
         'pk': {
             'S': '2022'
         },
         'sk': {
             'S': '2022#CU'
         }
     })
    response={
         'statusCode':200,
         'body': json.dumps(data),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response

def post_panel_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    key = json.loads(event.get('body'))
    response =table.put_item(Item=key)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }

def get_entity_data(event,context):
    data = client.get_item(TableName='HDMT-Table',
    Key = {
         'pk': {
             'S': '2022'
         },
         'sk': {
             'S': '2022#CU'
         }
     })
    response={
         'statusCode':200,
         'body': json.dumps(data),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response

def post_entity_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    key = json.loads(event.get('body'))
    response =table.put_item(Item=key)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }