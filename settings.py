__author__ = 'alandinneen'


class Configuration(object):
    EFNCONN = 'mysql+mysqldb://eshots_readonly:fr0sti3s@192.168.27.183:3306/efn'


class DevConfiguration(Configuration):
    DEBUG = True
    host = "127.0.0.1"
    port = 8001

