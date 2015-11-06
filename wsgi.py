__author__ = 'alandinneen'
from dt_regression_api import create_app
import settings


config = settings.ProductionConfiguration()
application = create_app(config)