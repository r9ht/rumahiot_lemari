from django.shortcuts import render
from django.shortcuts import render, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from rumahiot_lemari.apps.user_profile.utils import ResponseGenerator, RequestUtils, LemariUtils
from rumahiot_lemari.apps.sidik_modules.authorization import LemariSidikModuleNoEmail
from rumahiot_lemari.apps.dashboard.mongodb import LemariMongoDB
from rumahiot_lemari.settings import VALID_STATISTIC_TYPE
import datetime
from rumahiot_lemari.apps.dashboard.resources import UserAdddashBoardChartResource

# Create your views here.

def get_device_exported_xlsx(request):
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
                    exported_xlsxs = db.get_user_exported_xlsx(user_uuid=user['user_uuid'])
                    data = {
                        'user_uuid': user['user_uuid'],
                        'device_exported_xlsx': [],
                        'device_exported_xlsx_count': exported_xlsxs.count(True)
                    }
                    for exported_xlsx in exported_xlsxs:
                        device = db.get_device_by_device_uuid(device_uuid=exported_xlsx['device_uuid'], user_uuid=user['user_uuid'])
                        # Remove the id
                        exported_xlsx.pop('_id')
                        exported_xlsx['device_name'] = device['device_name']
                        data['device_exported_xlsx'].append(exported_xlsx)

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