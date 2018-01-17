from django.shortcuts import render,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rumahiot_lemari.apps.user_profile.utils import error_response_generator,data_response_generator,success_response_generator
from rumahiot_lemari.apps.sidik_modules.authorization import get_user_uuid,get_access_token
from rumahiot_lemari.apps.user_profile.dynamodb import get_user_profile,update_user_profile
from rumahiot_lemari.apps.user_profile.forms import UpdateProfileForm

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


@csrf_exempt
def user_profile_update(request):
    if request.method != "POST":
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
                    form = UpdateProfileForm(request.POST)
                    if form.is_valid():
                        # check if defined form field is submitted (check only for the field with required = False)
                        # use '-' as business logic for None in DynamoDB
                        if form.cleaned_data['phone_number'] == '':
                            form.cleaned_data['phone_number'] = '-'
                        # catch the exception if DynamoDB client got error
                        try :
                            update_status = update_user_profile(user['user_uuid'], form.cleaned_data['full_name'],
                                                                form.cleaned_data['phone_number'])
                        except :
                            response_data = error_response_generator(500, "Internal server error")
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
                        else:
                            # always true
                            if update_status:
                                response_data = success_response_generator(200, "User profile successfully updated")
                                return HttpResponse(json.dumps(response_data), content_type="application/json",
                                                    status=200)
                            else:
                                # to catch unknown error
                                response_data = error_response_generator(500, "Internal server error")
                                return HttpResponse(json.dumps(response_data), content_type="application/json",
                                                    status=500)


                    else:
                        response_data = error_response_generator(400,"Invalid or missing parameter submitted")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)







