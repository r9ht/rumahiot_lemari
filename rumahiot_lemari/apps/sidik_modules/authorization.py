# This section provide Sidik authentication methods for RumahIoT services
import requests
from rumahiot_lemari.settings import SIDIK_TOKEN_VALIDATION_ENDPOINT

class LemariAuthorization():
    # validate jwt token using Sidik service and return user uuid if the token is valid
    # input parameter : token (string)
    # return :  data['user_uuid'] = user_uuid, when the token is valid (string)
    #           data['error'] = None, when the token is valid (string)
    #           data['user_uuid'] = None, when the token is invalid or expired
    #           data['error'] = Error, message when the token is invalid (string)
    # data = {
    #     'user_uuid' : user_uuid(string),
    #     'error' : error(string)
    # }

    def get_user_uuid(self,token):
        data = {}
        # define the auth payload
        payload = {
            'token': token
        }
        response = requests.post(SIDIK_TOKEN_VALIDATION_ENDPOINT, data=payload)
        # check if the request success
        if response.status_code == 200:
            # return the user uuid
            data['user_uuid'] = response.json()['data']['payload']['user_uuid']
            data['error'] = None
            return data
        else:
            # return the error
            data['user_uuid'] = None
            data['error'] = response.json()['error']['message']
            return data

    # get access token from authorization header
    # input parameter : request(request)
    # return :  data['token'] = token, when the header format is correct (string)
    #           data['error'] = None, when the header format is correct
    #           data['token'] = None, when the header format is incorrect
    #           data['error'] = Error, when the header format is incorrect(string)
    # data = {
    #     'token' : token(string),
    #     'error' : error(string)
    # }
    def get_access_token(self,request):
        data = {}
        auth_header = request.META['HTTP_AUTHORIZATION'].split()
        # verify the authorization header length (including authorization type, currently using bearer)
        if len(auth_header) != 2:
            data['token'] = None
            data['error'] = 'Invalid authorization header length'
            return data
        else:
            # check for the type
            if auth_header[0].lower() != 'bearer':
                data['token'] = None
                data['error'] = 'Invalid authorization token method'
                return data
            else:
                data['token'] = auth_header[1]
                data['error'] = None
                return data

