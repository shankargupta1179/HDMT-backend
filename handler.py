import json
import boto3

client = boto3.resource('dynamodb')

def get_data(event, context):
    # records = {}
    # records["pk"] = {"S":"panelist"}
    # data = client.get_item(TableName='HDMT-Table',
    # Key = {
    #      'pk': {
    #          'S': '2022'
    #      },
    #      'sk': {
    #          'S': '2022#CU'
    #      }
    #  })
    
    table = client.Table('HDMT-Table')
    records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'panelist'})['Items']
    # items = response['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
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
    key['pk'] = 'panelist'
    key['sk'] = 'panelist' + '#' + key['panelist_first_name']
    response =table.put_item(Item=key)
    
    return {
        'statusCode': 200,
        'headers': {
        "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
       "Access-Control-Allow-Origin": '*',
       "Access-Control-Allow-Credentials": 'true',
       "Access-Control-Allow-Methods": 'GET,POST,PUT'
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
    # data = client.get_item(TableName='HDMT-Table',
    # Key = {
    #      'pk': {
    #          'S': '2022'
    #      },
    #      'sk': {
    #          'S': '2022#CU'
    #      }
    #  })
    
    table = client.Table('HDMT-Table')
    records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'entity'})['Items']
    # items = response['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response

def post_entity_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    # key = json.loads(event.get('body'))
    # response =table.put_item(Item=key)
    
    key = json.loads(event.get('body')) 
    key['pk'] = 'entity'
    key['sk'] = key['entity_name']
    response =table.put_item(Item=key)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Credentials": 'true',
            "Access-Control-Allow-Methods": 'GET,POST,PUT,OPTIONS'
        },
        'body': json.dumps(response)
    }
    