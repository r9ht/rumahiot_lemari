from django.shortcuts import render,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rumahiot_lemari.apps.user_profile.utils import error_response_generator,data_response_generator
from rumahiot_lemari.apps.sidik_modules.authorization import get_user_uuid,get_access_token
from rumahiot_lemari.apps.user_profile.dynamodb import get_user_profile

# Create your views here.
@csrf_exempt
def user_profile(request):
    if request.method != "GET":
        response_data = error_response_generator(400, "Bad request method")
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
    else:
        try:
            token = get_access_token(request)
        except KeyError:
            response_data = error_response_generator(400, "Please define the authorization header")
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            if token['token'] is None:
                response_data = error_response_generator(400, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
            else:
                user = get_user_uuid(token['token'])
                if user['user_uuid'] == None:
                    response_data = error_response_generator(400, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                else:
                    try:
                        user_profile = get_user_profile(user['user_uuid'])
                    except:
                        # for unknown internal server error
                        response_data = error_response_generator(500, "Internal server error")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
                    else:
                        response_data = data_response_generator(user_profile)
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)








