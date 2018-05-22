from pymongo import MongoClient

from rumahiot_lemari.settings import \
    RUMAHIOT_GUDANG_DATABASE, \
    RUMAHIOT_GUDANG_MONGO_HOST, \
    RUMAHIOT_GUDANG_MONGO_PASSWORD, \
    RUMAHIOT_GUDANG_MONGO_PORT, \
    RUMAHIOT_GUDANG_MONGO_USERNAME, \
    RUMAHIOT_LEMARI_USER_WIFI_CONNECTIONS_COLLECTION, \
    RUMAHIOT_GUDANG_USERS_DEVICE_COLLECTION

from bson.json_util import dumps
import json, datetime


class LemariMongoDB:

    # initiate the client
    def __init__(self):
        self.client = MongoClient(RUMAHIOT_GUDANG_MONGO_HOST,
                                  username=RUMAHIOT_GUDANG_MONGO_USERNAME,
                                  password=RUMAHIOT_GUDANG_MONGO_PASSWORD,
                                  )

    # Put data into specified database and collection
    # input parameter : database(string), collection(string), data(dictionary)
    # return : result(dict)
    def put_data(self, database, collection, data):
        db = self.client[database]
        col = db[collection]
        result = col.insert_one(data)
        return result

    # Get user wifi connection data
    # Input parameter : user_uuid(string)
    def get_user_wifi_connection(self, user_uuid):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_LEMARI_USER_WIFI_CONNECTIONS_COLLECTION]
        result = col.find({
            'user_uuid' : user_uuid
        })
        return result

    # Add new user wifi connection
    # Input parameter : (user_wifi_connection, dict)
    def put_user_wifi_connection(self, user_wifi_connection):
        result = self.put_data(database=RUMAHIOT_GUDANG_DATABASE, collection=RUMAHIOT_LEMARI_USER_WIFI_CONNECTIONS_COLLECTION, data=user_wifi_connection)
        return result

    # Get user_wifi_connection using user_wifi_connection_uuid and user_uuid
    # Input parameter : user_wifi_connection_uuid (string), user_uuid(string)
    def get_user_wifi_connection_by_uuid(self, user_wifi_connection_uuid, user_uuid):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_LEMARI_USER_WIFI_CONNECTIONS_COLLECTION]
        result = col.find_one({
            'user_uuid': user_uuid,
            'user_wifi_connection_uuid': user_wifi_connection_uuid
        })
        return result

    # Update user wifi connection data
    def update_user_wifi_connection(self, object_id, new_connection_name, new_ssid, new_security_enabled, new_password):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_LEMARI_USER_WIFI_CONNECTIONS_COLLECTION]
        col.update_one({'_id': object_id}, {'$set': {'connection_name': new_connection_name,
                                                     'ssid': new_ssid,
                                                     'security_enabled': new_security_enabled,
                                                     'password':new_password,
                                                     'time_updated': datetime.datetime.now().timestamp()}})

    # Get user device using user_wifi_connection_uuid
    def get_user_devices_by_user_wifi_connection_uuid(self, user_uuid, user_wifi_connection_uuid):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_GUDANG_USERS_DEVICE_COLLECTION]
        result = col.find({
            'user_uuid' : user_uuid,
            'user_wifi_connection_uuid': user_wifi_connection_uuid
        })

        return result

    # Remove specified user_wifi_connection
    # Input parameter : user_wifi_uuid (string)
    def remove_user_wifi_connection_by_uuid(self, user_wifi_connection_uuid):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_LEMARI_USER_WIFI_CONNECTIONS_COLLECTION]
        col.remove({
            'user_wifi_connection_uuid': user_wifi_connection_uuid
        })