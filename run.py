__author__ = 'alandinneen'
from dt_regression_api import create_app
import settings as app_settings
from sys import argv
from inspect import getmembers, isclass

# Get class names in global user defined app settings
settingsclsnames = getmembers(app_settings, isclass)

configlist = []


for name in settingsclsnames:
    configlist.append(name[0])

# Check user input to see which mode user supplied at command line
obj = None
for arg in argv:
    if arg in configlist:
        class_ = getattr(app_settings, arg)
        obj = class_()
    else:
        obj = app_settings.DevConfiguration

app = create_app(obj)

#create and run app with user defined parameters or the default dev configuration
app.run(host=obj.host, port=int(obj.port))