__author__ = 'alandinneen'
from . import api_blueprint
from settings import Configuration
from pymongo import MongoClient, errors
from logging import getLogger
from flask import Response, request
from json import dumps
from time import time
from datetime import datetime

@api_blueprint.route('/api/upload', methods=['POST'])
def upload():
    """
    This method is used to insert any data posted to the api as a string along
    with the remote ip address.
    """
    logger = getLogger(__name__)
    data = str(request.get_data())
    requestip = request.remote_addr
    ts = time()
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    datadict = {"ip": str(requestip),
                "data": data,
                "upload_time": timestamp}
    logger.info("Begging upload...")
    settings = Configuration()
    client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
    try:
        db = client[settings.MONGO_DB]
        upload = db.uploads
        upload_id = upload.insert_one(datadict).inserted_id
        responsejs = build_response_js("Success", requestip)
        resp = Response(responsejs, status=200, mimetype='application/json')
    except errors.NetworkTimeout as e:
        logger.info("Insert failed. There has been a network error. ", e)
        responsejs = build_response_js("Failure", requestip)
        resp = Response(responsejs, status=500, mimetype='application/json')
        return resp
    except errors.OperationFailure as e:
        logger.info("Insert failed. There has been an operation failure. ", e)
        responsejs = build_response_js("Failure", requestip)
        resp = Response(responsejs, status=500, mimetype='application/json')
        return resp
    logger.info("Upload completed! Upload ID: " + str(upload_id))

    return resp

def build_response_js(status, requestip):
    """
    This method is used to build the response json to the requesting server.
    """
    responsejs = {'ip': requestip}
    if status == 'Success':
        responsejs["Success"] = "Your request was succesfully processed."
    else:
        responsejs["Failure"] = "Your request failed to processed."
    responsejs = dumps(responsejs)
    return responsejs