from django.shortcuts import render,HttpResponse
import json
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from rumahiot_lemari.apps.user_profile.utils import error_response_generator,data_response_generator,success_response_generator,get_file_type
from rumahiot_lemari.apps.sidik_modules.authorization import get_user_uuid,get_access_token
from rumahiot_lemari.apps.user_profile.dynamodb import get_user_profile,update_user_profile,update_user_profile_picture
from rumahiot_lemari.apps.user_profile.forms import UpdateProfileForm,UpdateProfilePictureForm
from rumahiot_lemari.apps.user_profile.s3 import put_object
from rumahiot_lemari.settings import RUMAHIOT_UPLOAD_BUCKET,RUMAHIOT_REGION

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



# todo : merge this thing with the profile update ?
@csrf_exempt
def user_profile_picture_update(request):
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
                    form = UpdateProfilePictureForm(request.POST,request.FILES)
                    if form.is_valid():
                        profile_image_file = form.cleaned_data['profile_image']
                        file_extension = get_file_type(profile_image_file)
                        target_location = 'image/profile/{}/{}{}'.format(user['user_uuid'],uuid4().hex,file_extension)
                        try :
                            response = put_object(RUMAHIOT_UPLOAD_BUCKET,target_location,profile_image_file.file.getvalue())
                        except:
                            # catch unknown error
                            response_data = error_response_generator(500, "Internal server error")
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
                        else:
                            file_location = 'https://s3-{}.amazonaws.com/{}/{}'.format(RUMAHIOT_REGION,RUMAHIOT_UPLOAD_BUCKET,target_location)
                            try:
                                db_response = update_user_profile_picture(user['user_uuid'],file_location)
                            except:
                                # catch unknown error
                                response_data = error_response_generator(500, "Internal server error")
                                return HttpResponse(json.dumps(response_data), content_type="application/json",
                                                    status=500)
                            else:
                                response_data = success_response_generator(200, "User profile picture successfully updated")
                                return HttpResponse(json.dumps(response_data), content_type="application/json",
                                                    status=200)

                        # print(type(form.cleaned_data['profile_image'].file.getvalue()))

                        # try :
                        #     update_status = update_user_profile_picture(user['user_uuid'], form.cleaned_data['full_name'],
                        #                                         form.cleaned_data['phone_number'])
                        # except :
                        #     response_data = error_response_generator(500, "Internal server error")
                        #     return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
                        # else:
                        #     # always true
                        #     if update_status:
                        #         response_data = success_response_generator(200, "User profile picture successfully updated")
                        #         return HttpResponse(json.dumps(response_data), content_type="application/json",
                        #                             status=200)
                        #     else:
                        #         # to catch unknown error
                        #         response_data = error_response_generator(500, "Internal server error")
                        #         return HttpResponse(json.dumps(response_data), content_type="application/json",
                        #                             status=500)
                    else:
                        response_data = error_response_generator(400,"Invalid or missing parameter submitted")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)









