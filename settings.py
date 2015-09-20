__author__ = 'alandinneen'


class Configuration(object):
    MONGO_IP = 'localhost'
    MONGO_PORT = 27017
    MONGO_DB = 'uploads'

class DevConfiguration(Configuration):
    DEBUG = True
    host = "127.0.0.1"
    port = 8001

