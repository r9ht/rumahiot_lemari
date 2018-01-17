import boto3
from uuid import uuid4
from boto3.dynamodb.conditions import Key
from rumahiot_lemari.settings import RUMAHIOT_REGION,RUMAHIOT_USERS_PROFILE_TABLE
import json

# DynamoDB client
def dynamodb_client():
    client = boto3.resource('dynamodb', region_name=RUMAHIOT_REGION)
    return client

# get user profile data
# input parameter : user_uuid(string)
# return : response(dict)
def get_user_profile(user_uuid):
    client = dynamodb_client()
    table = client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
    response = table.get_item(Key={
        'user_uuid' : user_uuid
    })
    return response['Item']


# update user profile data
# input parameter : user_uuid(string) , full_name(string), phone_number(string)
# return : status(boolean)
def update_user_profile(user_uuid,full_name,phone_number):
    # keep the error from breaking service by catching the client error in the view
    status = False
    client = dynamodb_client()
    table = client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
    response = table.put_item(
        Item = {
            'user_uuid': user_uuid,
            'full_name': full_name,
            'phone_number' : phone_number,
            'profile_image' : get_user_profile(user_uuid)['profile_image']
        }
    )
    status = True
    return status
