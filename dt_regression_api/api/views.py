__author__ = 'alandinneen'
from logging import getLogger
from time import time
from datetime import datetime
import xml.etree.ElementTree as ET
from . import api_blueprint
from settings import Configuration
from pymongo import MongoClient, errors
from flask import Response, request
import dt_regression_api.tasks as celtask


@api_blueprint.route('/api/upload', methods=['POST'])
def upload():
    """
    This method is used to insert any data posted to the api as a string along
    with the remote ip address.
    """
    logger = getLogger(__name__)
    data = str(request.get_data(as_text=True))
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
        #Specify mongo collection
        upload = db.posts
        upload_id = upload.insert_one(datadict).inserted_id
        responsejs = settings.build_response_js("Success", requestip=requestip, uploadid=str(upload_id))
        resp = Response(responsejs, status=200, mimetype='application/json')
    except errors.NetworkTimeout as e:
        logger.info("Insert failed. There has been a network error. ", e)
        responsejs = settings.build_response_js("Failure", requestip=requestip)
        resp = Response(responsejs, status=500, mimetype='application/json')
        return resp
    except errors.OperationFailure as e:
        logger.info("Insert failed. There has been an operation failure. ", e)
        responsejs = settings.build_response_js("Failure", requestip)
        resp = Response(responsejs, status=500, mimetype='application/json')
        return resp
    finally:
        client.close()
    logger.info("Upload completed! Upload ID: " + str(upload_id))
    celtask.send_successful_upload_notification.apply_async(args=[data])
    return resp


@api_blueprint.route('/api/upload/xml', methods=['POST'])
def upload_xml():
    """
    This url is meant to expose xml validation
    """
    data = str(request.get_data(as_text=True))
    try:
        xml = ET.fromstring(data)
        if xml is not None:
            celtask.send_vaidated_xml_notification.apply_async(args=[data])
    except ET.ParseError as e:
        celtask.send_invalid_xml_notification.apply_async(args=[e])
