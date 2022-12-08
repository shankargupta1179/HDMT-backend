import json
import boto3

client = boto3.client('dynamodb')

def hello(event, context):
    data = client.get_item(TableName='HDMT-Table',
    Key = {
         'pk': {
             'S': '2022'
         },
         'sk': {
             'S': '2022#1#22'
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
    # print(data['item'])
    
    return response
    
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('HDMT-Table')
    
    # # define the item data
    # item = {
    #     'pk': '2022',
    #     'sk': '2022#1#22#gupta',
    #     'student_name': 'ravi',
    #     'student_roll': 123456,
    #     'panelist_name':'sourabh'
    # }
    
    # # put the item in the table
    # table.put_item(Item=item)
    
    # return 'Success'


# def lambda_handler(event, context):
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('HDMT-Table')
    
    # # define the primary key of the item to retrieve
    # key = {
    #     'pk': '2022',
    #     'sk': '2022#1#22'
    # }
    
    # # get the item from the table
    # response = table.get_item(Key=key)
    # print(response)
    # item = response['Item']
    
    # return {
    #     'statusCode': 200,
    #     'headers': {'Content-Type': 'application/json'},
    #     'body': json.dumps(item)
    # }
