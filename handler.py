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

def get_all_panelists(event,context):
    user_pool_id =  "us-east-1_2mpkLzGvv"
    client_id = "1l3fojck1fom7rcvvjb0c8ksf7"
    cognito = boto3.client('cognito-idp')
    list = []
    users= []
    next_page = None
    kwargs = {

            'UserPoolId': user_pool_id

        }
    users_remain = True
    while(users_remain):
        if next_page:
            kwargs['PaginationToken'] = next_page
        response = cognito.list_users(**kwargs)
        users.extend(response['Users'])
        next_page = response.get('PaginationToken', None)
        users_remain = next_page is not None

       
    for i in users:
        item = {}
        for j in i["Attributes"]:
            item.update({j['Name'] :j['Value']} )  
        list.append(item)    

    response={
            "statusCode":200, 
            "body": json.dumps(list, indent=4, sort_keys=True, default=str),
            'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
            }
        }
    return response  


def get_panelist_data(event,context):
    # data = client.get_item(TableName='HDMT-Table',
    # Key = {
    #      'pk': {
    #          'S': '2022'
    #      },
    #      'sk': {
    #          'S': '2022#CU'
    #      }
    #  })
    # response={
    #      'statusCode':200,
    #      'body': json.dumps(data),
    #      'headers': {
    #          'Content-Type': 'application/json',
    #          'Access-Control-Allow-Origin': '*'
    #      },
    #  }
    
    # return response
    table = client.Table('HDMT-Table')
    records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'panelist'})['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response

def post_panelist_data(event,context):
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('HDMT-Table')
    key = json.loads(event["body"]) 
    # key['pk'] = 'panelist'
    # key['sk'] = key['panelist_email'] 
    # response =table.put_item(Item=key)
    client = boto3.client('cognito-idp')
    response = client.admin_create_user(
        UserPoolId='us-east-1_2mpkLzGvv',
        Username=key['email'],
        UserAttributes=key['attr'],
        TemporaryPassword= 'Defaultpass@123',
        ForceAliasCreation=False,
        
        DesiredDeliveryMediums=[
            'EMAIL',
        ],
        ClientMetadata={
            'string': 'string'
        }
    )
    attrArr = response['User']['Attributes']
    sub = attrArr[0]

    username = str(sub['Value'])
    response = client.admin_update_user_attributes(
    UserPoolId='us-east-1_2mpkLzGvv',
    Username=username,
    UserAttributes=[
        {
            'Name': 'email_verified',
            'Value': 'true'
        },
    ],
    ClientMetadata={
        'string': 'string'
    }
   )
    return {"statusCode" : 200, "body" : json.dumps(response, indent=4, sort_keys=True, default=str)}
    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    #         "Access-Control-Allow-Origin": '*',
    #         "Access-Control-Allow-Credentials": 'true',
    #         "Access-Control-Allow-Methods": 'GET,POST,PUT,OPTIONS'
    #     },
    #     'body': json.dumps(response2)
    # }

    
    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    #         "Access-Control-Allow-Origin": '*',
    #         "Access-Control-Allow-Credentials": 'true',
    #         "Access-Control-Allow-Methods": 'GET,POST,PUT,OPTIONS'
    #     },
    #     'body': json.dumps(response2)
    # }

def update_panelist(event,response):
  client = boto3.client('cognito-idp')
  key=json.loads(event["body"])
  response = client.admin_update_user_attributes(
    UserPoolId='us-east-1_2mpkLzGvv',
    Username= key['email'] ,
    UserAttributes= key['attr'],
    ClientMetadata={
        'string': 'string'
    }
)
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

def get_panel_data(event,context):
    table = client.Table('HDMT-Table')
    records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'panel'})['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
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
    key['pk'] = 'panel'
    key['sk'] = key['panel_title']
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

def get_entity_data(event,context):
    table = client.Table('HDMT-Table')
    if(event.get('queryStringParameters')==None):
        records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'entity'})['Items']
    else:
        records = table.query(KeyConditionExpression="pk=:pk and sk=:sk",ExpressionAttributeValues={':pk':'entity',':sk':event.get('queryStringParameters').get('entity_name')})['Items']
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

def update_entity_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    key = json.loads(event.get('body')) 
    response = table.update_item(
        Key={
            'pk':'entity',
            'sk':key['entity_name']
        },
        UpdateExpression = 'SET contactDetails= :contact',
        ExpressionAttributeValues={
            ':contact': key['contactDetails']
        }
    )
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

def get_hiring_data(event,context):
    table = client.Table('HDMT-Table')
    # items = response['Items']
    # print(event.get('queryStringParameters'));
    if(event.get('queryStringParameters')==None):
        records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'drive'})['Items']
    else:
        # print(event.get('queryStringParameters').get('title'))
        records = table.query(KeyConditionExpression="pk=:pk and sk=:sk",ExpressionAttributeValues={':pk':'drive',':sk':event.get('queryStringParameters').get('title')})['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    
    return response

def post_hiring_data(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    
    key = json.loads(event.get('body')) 
    key['pk'] = 'drive'
    key['sk'] = key['title']
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

def get_candidates(event,context):
    table = client.Table('HDMT-Table')
    if(event.get('queryStringParameters')==None):
        records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'candidate'})['Items']
    else:   
        records = table.query(KeyConditionExpression="pk=:pk and begins_with(sk,:sk)",ExpressionAttributeValues={':pk':'candidate',':sk':event.get('queryStringParameters').get('entity')})['Items']
    response={
            'statusCode':200,
            'body': json.dumps(records),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

    return response

def post_candidate(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    
    records = json.loads(event.get('body')) 
    with table.batch_writer() as batch:
        for record in records:
            record['pk'] = 'candidate'
            record['sk'] = record['entity']+'#'+record['candidate_email']
            response =table.put_item(Item=record)

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

def get_specific_drive_panelist(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    # records = table.query(KeyConditionExpression="pk=:pk and sk=:sk",ExpressionAttributeValues={':pk':'drive-panelist'})['Items']
    if(event.get('queryStringParameters')==None):
        records = table.query(KeyConditionExpression="pk=:pk and sk=:sk",ExpressionAttributeValues={':pk':'drive-panelist'})['Items']
    else:   
        records = table.query(KeyConditionExpression="pk=:pk and begins_with(sk,:sk)",ExpressionAttributeValues={':pk':'drive-panelist',':sk':event.get('queryStringParameters').get('title')})['Items']
    response={
            'statusCode':200,
            'body': json.dumps(records),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
    return response


def post_specific_drive_panelist(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    key = json.loads(event.get('body')) 
    key['pk'] = 'drive-panelist'
    key['sk'] = key['title'] 
    response = table.put_item(Item=key)
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

def get_panel_data(event,context):
    table = client.Table('HDMT-Table')
    # records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'panel'})['Items']
    if(event.get('queryStringParameters')==None):
        records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'panel'})['Items']
    else:
        records = table.query(KeyConditionExpression="pk=:pk and begins_with(sk,:sk)",ExpressionAttributeValues={':pk':'panel',':sk':event.get('queryStringParameters').get('title')})['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
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
    key['pk'] = 'panel'
    key['sk'] = key['title']+"#"+ key['panel_title']
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

def post_panel_candidate(event,context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HDMT-Table')
    key = json.loads(event.get('body'))
    key['pk'] = "candidate_panel"
    key['sk'] = key['candidate_email']+"#"+key['panel_title']
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

def get_panel_candidate(event,context):
    table = client.Table('HDMT-Table')
    # records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'panel'})['Items']
    if(event.get('queryStringParameters')==None):
        records = table.query(KeyConditionExpression="pk=:pk",ExpressionAttributeValues={':pk':'candidate_panel'})['Items']
    else:
        records = table.query(KeyConditionExpression="pk=:pk and begins_with(sk,:sk)",ExpressionAttributeValues={':pk':'candidate_panel',':sk':event.get('queryStringParameters').get('candidate_email')})['Items']
    response={
         'statusCode':200,
         'body': json.dumps(records),
         'headers': {
             'Content-Type': 'application/json',
             'Access-Control-Allow-Origin': '*'
         },
     }
    return response

