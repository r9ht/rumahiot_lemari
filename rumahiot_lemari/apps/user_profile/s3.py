import boto3
from rumahiot_lemari.settings import RUMAHIOT_REGION,RUMAHIOT_USERS_PROFILE_TABLE

# S3 client
def dynamodb_client():
    client = boto3.client('s3', region_name=RUMAHIOT_REGION)
    return client

# S3 put object
def put_object(target_bucket,target_file,object_body):
    # please catch the exception in the view so the service wont stop working when something bad happened
    client = dynamodb_client()
    client.put_object(Bucket=target_bucket,Key=target_file,Body=object_body,ACL='public-read')