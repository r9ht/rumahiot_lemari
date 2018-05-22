from django.shortcuts import render, HttpResponse
import json
from uuid import uuid4
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rumahiot_lemari.apps.dashboard.mongodb import LemariMongoDB
from rumahiot_lemari.apps.user_profile.utils import LemariUtils, RequestUtils, ResponseGenerator
from rumahiot_lemari.apps.sidik_modules.authorization import LemariSidikModuleNoEmail
from rumahiot_lemari.apps.network_connection.forms import AddUserWifiConnectionForm, UpdateUserWifiConnectionForm

# Create your views here.

def retrieve_user_wifi_connection_list(request):
    # Gudang class
    rg = ResponseGenerator()
    requtils = RequestUtils()
    auth = LemariSidikModuleNoEmail()
    db = LemariMongoDB()

    if request.method == 'GET':
        # Check the token
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(401, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                # Check token validity
                if user['user_uuid'] != None:

                    # Get all conenction detail
                    wifi_connections = db.get_user_wifi_connection(user_uuid=user['user_uuid'])
                    data = {
                        'user_uuid' : user['user_uuid'],
                        'wifi_connections' : [],
                        'wifi_connection_count': wifi_connections.count(True)
                    }

                    # Append to data
                    for wifi_connection in wifi_connections:
                        # Security enabled
                        security_enabled = '0'
                        if wifi_connection['security_enabled']:
                            security_enabled = '1'

                        wifi_connection_data = {
                            'user_wifi_connection_uuid': wifi_connection['user_wifi_connection_uuid'],
                            'connection_name': wifi_connection['connection_name'],
                            'ssid': wifi_connection['ssid'],
                            'security_enabled': security_enabled,
                            'password': wifi_connection['password'],
                            'time_updated': wifi_connection['time_updated']

                        }
                        data['wifi_connections'].append(wifi_connection_data)

                    # Generate response object
                    response_data = rg.data_response_generator(data)
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)

                else:
                    response_data = rg.error_response_generator(401, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
            else:
                response_data = rg.error_response_generator(401, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)
    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

@csrf_exempt
def add_user_wifi_connection(request):
    # Gudang class
    rg = ResponseGenerator()
    requtils = RequestUtils()
    auth = LemariSidikModuleNoEmail()
    db = LemariMongoDB()

    if request.method == 'POST':
        # Check the token
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(401, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                # Check token validity
                if user['user_uuid'] != None:

                    form = AddUserWifiConnectionForm(request.POST)
                    if form.is_valid():

                        # Check for security_enabled
                        raw_security_enabled = form.cleaned_data['security_enabled']
                        if raw_security_enabled == '1':
                            if 'password' in form.cleaned_data :
                                password = form.cleaned_data['password']
                                security_enabled = True
                            else:
                                response_data = rg.error_response_generator(400, 'Please spesify SSID password')
                                return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

                        elif raw_security_enabled == '0':
                            security_enabled = False
                            password = '-'
                        else:
                            response_data = rg.error_response_generator(400, 'invalid or missing parameter submitted')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

                        # Construct user wifi connection structure
                        user_wifi_connection = {
                            'user_wifi_connection_uuid': uuid4().hex,
                            'user_uuid': user['user_uuid'],
                            'connection_name': form.cleaned_data['connection_name'],
                            'ssid': form.cleaned_data['ssid'],
                            'security_enabled': security_enabled,
                            'password': password,
                            'time_updated': datetime.now().timestamp()
                        }

                        # Put in db
                        db.put_user_wifi_connection(user_wifi_connection=user_wifi_connection)

                        # Generate response object
                        response_data = rg.success_response_generator(200,'Wifi connection successfully added')
                        return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)
                    else:
                        response_data = rg.error_response_generator(400, 'invalid or missing parameter submitted')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                else:
                    response_data = rg.error_response_generator(401, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
            else:
                response_data = rg.error_response_generator(401, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)
    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

@csrf_exempt
def update_user_wifi_connection(request):
    # Gudang class
    rg = ResponseGenerator()
    requtils = RequestUtils()
    auth = LemariSidikModuleNoEmail()
    db = LemariMongoDB()

    if request.method == 'POST':
        # Check the token
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(401, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                # Check token validity
                if user['user_uuid'] != None:

                    form = UpdateUserWifiConnectionForm(request.POST)
                    if form.is_valid():
                        # Check user_wifi_connection_uuid
                        user_wifi_connection = db.get_user_wifi_connection_by_uuid(user_uuid=user['user_uuid'], user_wifi_connection_uuid=form.cleaned_data['user_wifi_connection_uuid'])
                        if user_wifi_connection != None:
                            # Check for security_enabled
                            raw_security_enabled = form.cleaned_data['security_enabled']
                            if raw_security_enabled == '1':
                                if 'password' in form.cleaned_data:
                                    password = form.cleaned_data['password']
                                    security_enabled = True
                                else:
                                    response_data = rg.error_response_generator(400, 'Please spesify SSID password')
                                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

                            elif raw_security_enabled == '0':
                                security_enabled = False
                                password = '-'
                            else:
                                response_data = rg.error_response_generator(400, 'invalid or missing parameter submitted')
                                return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                            # Put in db
                            db.update_user_wifi_connection(object_id=user_wifi_connection['_id'], new_connection_name=form.cleaned_data['connection_name'],
                                                           new_ssid=form.cleaned_data['ssid'], new_security_enabled=security_enabled, new_password=password)
                            # Generate response object
                            response_data = rg.success_response_generator(200, 'Wifi connection successfully updated')
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                        else:
                            response_data = rg.error_response_generator(400, 'invalid user wifi connection uuid')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                    else:
                        response_data = rg.error_response_generator(400, 'invalid or missing parameter submitted')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                else:
                    response_data = rg.error_response_generator(401, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
            else:
                response_data = rg.error_response_generator(401, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)
    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

@csrf_exempt
def remove_user_wifi_connection(request, user_wifi_connection_uuid):
    # Gudang class
    rg = ResponseGenerator()
    requtils = RequestUtils()
    auth = LemariSidikModuleNoEmail()
    db = LemariMongoDB()

    if request.method == 'GET':
        # Check the token
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(401, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                # Check token validity
                if user['user_uuid'] != None:
                    # Check user_wifi_connection_uuid
                    user_wifi_connection = db.get_user_wifi_connection_by_uuid(user_uuid=user['user_uuid'], user_wifi_connection_uuid=user_wifi_connection_uuid)
                    if user_wifi_connection != None:
                        # Check if the connection is being used
                        user_devices = db.get_user_devices_by_user_wifi_connection_uuid(user_uuid=user['user_uuid'], user_wifi_connection_uuid=user_wifi_connection_uuid)
                        if user_devices.count(True) == 0:
                            db.remove_user_wifi_connection_by_uuid(user_wifi_connection_uuid=user_wifi_connection_uuid)
                            # Generate response object
                            response_data = rg.success_response_generator(200, 'Wifi connection successfully removed')
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                        else:
                            # Generate response object
                            response_data = rg.error_response_generator(400, 'Wifi connection is being used by one or more device')
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                    else:
                        response_data = rg.error_response_generator(400, 'invalid user wifi connection uuid')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                else:
                    response_data = rg.error_response_generator(401, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)
            else:
                response_data = rg.error_response_generator(401, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)
    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)