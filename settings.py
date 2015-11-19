__author__ = 'alandinneen'
from json import dumps

class Configuration(object):
    MONGO_IP = 'localhost'
    MONGO_PORT = 27017
    MONGO_DB = 'uploads'
    CELERY_BROKER_URL = 'amqp://localhost:5672'
    CELERY_APP_NAME = 'dt_regression_api'




class DevConfiguration(Configuration):
    DEBUG = True
    host = "127.0.0.1"
    port = 8001

class ProductionConfiguration(Configuration):
    DEBUG = False
