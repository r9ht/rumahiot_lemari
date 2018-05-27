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

@csrf_exempt
def add_device_dashboard_chart(request) :
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
                    try:
                        # Verify the data format
                        j = json.loads(request.body.decode('utf-8'))
                        d = UserAdddashBoardChartResource(**j)
                    except TypeError:
                        response_data = rg.error_response_generator(400, "One of the request inputs is not valid")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                    except ValueError:
                        response_data = rg.error_response_generator(400, "Malformed JSON")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                    else:
                        device = db.get_device_by_device_uuid(device_uuid=d.device_uuid, user_uuid=user['user_uuid'])
                        if (device) :
                            if (type(d.statistic_type) is str) and d.statistic_type in VALID_STATISTIC_TYPE:
                                if (d.statistic_type == '2'):
                                    # Make sure it is less than equal 168 hour and more than equal 1 hour
                                    if (type(d.n_last_hour) is int and (d.n_last_hour >= 1 and d.n_last_hour <= 168)):
                                        data = {
                                            'user_dashboard_chart_uuid': uuid4().hex,
                                            'device_uuid': d.device_uuid,
                                            'user_uuid': user['user_uuid'],
                                            'statistic_type': d.statistic_type ,
                                            'n_last_hour': d.n_last_hour
                                        }
                                        # put the data into db
                                        db.put_user_device_dashboard_chart(data=data)
                                        response_data = rg.success_response_generator(200, "Device dashboard chart successfully added")
                                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                                    else:
                                        response_data = rg.error_response_generator(400, 'Hour must be larger than 1 and less than 168')
                                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                                else:
                                    data = {
                                        'user_dashboard_chart_uuid': uuid4().hex,
                                        'device_uuid': d.device_uuid,
                                        'user_uuid': user['user_uuid'],
                                        'statistic_type': d.statistic_type,
                                    }
                                    # put the data into db
                                    db.put_user_device_dashboard_chart(data=data)
                                    response_data = rg.success_response_generator(200, "Device dashboard chart successfully added")
                                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

                            else:
                                response_data = rg.error_response_generator(400, 'Invalid statistic type')
                                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                        else:
                            response_data = rg.error_response_generator(400, 'Invalid device uuid')
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

                else:
                    response_data = rg.error_response_generator(401, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)

            else:
                response_data = rg.error_response_generator(401, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

def get_device_dashboard_chart(request):
    # Gudang class
    rg = ResponseGenerator()
    requtils = RequestUtils()
    auth = LemariSidikModuleNoEmail()
    db = LemariMongoDB()
    lutils = LemariUtils()

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
                    device_dashboard_charts = db.get_dashboard_chart_by_user_uuid(user_uuid=user['user_uuid'])
                    data = {
                        'device_dashboard_charts': [],
                        'device_dashboard_chart_count': device_dashboard_charts.count(True)
                    }
                    for device_dashboard_chart in device_dashboard_charts :
                        # Remove unnecessary key
                        device_dashboard_chart.pop('_id')
                        device_dashboard_chart.pop('user_uuid')
                        data['device_dashboard_charts'].append(device_dashboard_chart)

                    response_data = rg.data_response_generator(data)
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


                else:
                    response_data = rg.error_response_generator(401, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=401)

            else:
                response_data = rg.error_response_generator(401, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

def remove_device_dashboard_chart(request, user_dashboard_chart_uuid):
    # Gudang class
    rg = ResponseGenerator()
    requtils = RequestUtils()
    auth = LemariSidikModuleNoEmail()
    db = LemariMongoDB()
    lutils = LemariUtils()

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
                    dashboard_chart = db.get_dashboard_chart_by_uuid(user_dashboard_chart_uuid=user_dashboard_chart_uuid, user_uuid=user['user_uuid'])
                    if (dashboard_chart):
                        db.remove_chart_by_chart_uuid(user_dashboard_chart_uuid=user_dashboard_chart_uuid)
                        response_data = rg.success_response_generator(200, "Device dashboard chart successfully removed")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

                    else:
                        response_data = rg.error_response_generator(400, 'Invalid user dashboard chart')
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