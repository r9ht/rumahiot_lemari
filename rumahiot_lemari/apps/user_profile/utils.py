import hashlib,mimetypes,magic

class ResponseGenerator():
    # generate error response in dict format
    def error_response_generator(self,code, message):
        response = {
            "error": {
                "code": code,
                "message": message
            }
        }
        return response

    # generate data response in dict format
    # input parameter data(dict)
    def data_response_generator(self,data):
        response = {
            "data": data
        }
        return response

    # generate error response in dict format
    def success_response_generator(self,code, message):
        response = {
            "success": {
                "code": code,
                "message": message
            }
        }
        return response


class LemariUtils():

    # get object file_type
    # for inmemoryuploadedfile

    def get_file_type(self,inmemoryuploadedfile):
        return mimetypes.MimeTypes().types_map_inv[1][magic.from_buffer(inmemoryuploadedfile.read(), mime=True)][0]

