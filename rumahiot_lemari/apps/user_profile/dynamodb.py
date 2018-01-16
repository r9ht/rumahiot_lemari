import boto3
from uuid import uuid4
from boto3.dynamodb.conditions import Key
from rumahiot_lemari.settings import RUMAHIOT_REGION,RUMAHIOT_USERS_PROFILE_TABLE
import json

# DynamoDB client
def dynamodb_client():
    client = boto3.resource('dynamodb', region_name=RUMAHIOT_REGION)
    return client


def get_user_profile(user_uuid):
    client = dynamodb_client()
    table = client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
    response = table.get_item(Key={
        'user_uuid' : user_uuid
    })
    return response['Item']

