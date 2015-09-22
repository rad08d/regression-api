__author__ = 'alandinneen'
from json import dumps

class Configuration(object):
    MONGO_IP = 'localhost'
    MONGO_PORT = 27017
    MONGO_DB = 'uploads'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_APP_NAME = 'dt_regression_api'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_DEFAULT_SENDER = 'datatransfer@eshots.com'
    MAIL_USER = 'regressioneshots@gmail.com'
    MAIL_USER_PASS = '!Welcome1'

    MESSAGES = {'Success': "Your request was succesfully processed.",
                'Failure': "Your request failed to processed."}




    # Application specific cofiguration methods.
    def build_response_js(self, status, requestip):
        responsejs = {'ip': requestip}
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

