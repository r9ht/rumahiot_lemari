import boto3
from rumahiot_lemari.settings import RUMAHIOT_REGION,RUMAHIOT_USERS_PROFILE_TABLE
from datetime import datetime

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
            'profile_image' : get_user_profile(user_uuid)['profile_image'],
            'time_updated' : str(datetime.now().timestamp())
        }
    )
    status = True
    return status


# update user profile picture
# input parameter : user_uuid(string) , profile_image(string)
# return : status(boolean)
def update_user_profile_picture(user_uuid,profile_picture):
    # keep the error from breaking service by catching the client error in the view
    status = False
    client = dynamodb_client()
    table = client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
    user_profile =  get_user_profile(user_uuid)
    response = table.put_item(
        Item={
            'user_uuid': user_uuid,
            'full_name': user_profile['full_name'],
            'phone_number': user_profile['phone_number'],
            'profile_image': profile_picture,
            'time_updated' : str(datetime.now().timestamp())
        }
    )
    status = True
    return status


