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
from rumahiot_lemari.apps.sidik_modules.decorator import post_method_required, get_method_required, authentication_required, authentication_required_with_email

# Create your views here.

@get_method_required
@authentication_required
def get_device_exported_xlsx(request, user):

    # Gudang class
    rg = ResponseGenerator()
    db = LemariMongoDB()

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