import boto3
from rumahiot_lemari.settings import RUMAHIOT_REGION,RUMAHIOT_USERS_PROFILE_TABLE
from datetime import datetime

class LemariDynamoDB():

    def __init__(self):
        self.client = boto3.resource('dynamodb', region_name=RUMAHIOT_REGION)

    # get user profile data
    # input parameter : user_uuid(string)
    # return : response(dict)
    def get_user_profile(self,user_uuid):
        table = self.client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
        response = table.get_item(Key={
            'user_uuid': user_uuid
        })
        return response['Item']

    # update user profile data
    # input parameter : user_uuid(string) , full_name(string), phone_number(string)
    def update_user_profile(self,user_uuid, full_name, phone_number):
        # keep the error from breaking service by catching the client error in the view
        table = self.client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
        response = table.update_item(
            Key = {
              'user_uuid' : user_uuid
            },
            UpdateExpression="set full_name=:f, phone_number=:p, time_updated=:t",
            ExpressionAttributeValues={
                ':f': full_name,
                ':p': phone_number,
                ':t': str(datetime.now().timestamp())
            },
            ReturnValues="UPDATED_NEW"
        )

    # update user profile picture
    # input parameter : user_uuid(string) , profile_image(string)
    def update_user_profile_picture(self,user_uuid, profile_picture):
        # keep the error from breaking service by catching the client error in the view
        table = self.client.Table(RUMAHIOT_USERS_PROFILE_TABLE)
        response = table.update_item(
            Key={
                'user_uuid': user_uuid
            },
            UpdateExpression="set profile_picture=:p, time_updated=:t",
            ExpressionAttributeValues={
                ':p' : profile_picture,
                ':t': str(datetime.now().timestamp())
            },
            ReturnValues="UPDATED_NEW"
        )
