__author__ = 'alandinneen'
from json import dumps

class Configuration(object):
    MONGO_IP = 'localhost'
    MONGO_PORT = 27017
    MONGO_DB = 'uploads'
    CELERY_BROKER_URL = 'amqp://localhost:5672'
    CELERY_APP_NAME = 'dt_regression_api'

    MESSAGES = {'Success': "Your request was succesfully processed.",
                'Failure': "Your request failed to processed."}




    # Application specific cofiguration methods.
    def build_response_js(self, status, requestip, uploadid=None):
        responsejs = {'ip': requestip,
                      'uploadid': uploadid}
        if status == 'Success':
            responsejs["Success"] = self.MESSAGES['Success']
        else:
            responsejs["Failure"] = self.MESSAGES['Failure']
        responsejs = dumps(responsejs)
        return responsejs




class DevConfiguration(Configuration):
    DEBUG = True
    host = "127.0.0.1"
    port = 8001

class ProductionConfiguration(Configuration):
    DEBUG = False
