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
from json import dumps

logger = getLogger(__name__)

@api_blueprint.route('/api/upload', methods=['POST'])
def upload():
    """
    This method is used to insert any data posted to the api as a string along
    with the remote ip address.
    """
    data = str(request.get_data(as_text=True))
    requestip = request.remote_addr
    ts = time()
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    datadict = {"ip": str(requestip),
                "data": data,
                "upload_time": timestamp}
    uploadid = insert_upload(datadict=datadict)
    if uploadid:
        celtask.send_successful_upload_notification.apply_async(args=[data])
        return Response(response=build_response_js(status=200, requestip=requestip, uploadid=uploadid), status=200, mimetype='application/json')
    else:
        return Response(response=build_response_js(status=500, requestip=requestip), status=500, mimetype='application/json')


@api_blueprint.route('/api/upload/xml', methods=['POST'])
def upload_xml():
    """
    This url is meant to expose xml validation. It inserts into the database if it is valid or invalid.
    """
    requestip = request.remote_addr
    data = str(request.get_data(as_text=True))
    ts = time()
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    datadict = {"ip": str(requestip),
                "data": data,
                "upload_time": timestamp,
                "validXML": None}
    validation = validate_xml(data)
    if validation == True:
        datadict['validXML'] = "Validated"
        uploadid = insert_upload(datadict=datadict)
        celtask.send_vaidated_xml_notification.apply_async(args=[data])
        return Response(response=build_response_js(status=200, requestip=requestip, uploadid=uploadid), status=200, mimetype='application/json')
    else:
        datadict["validXML"] = validation
        uploadid = insert_upload(datadict=datadict)
        celtask.send_invalid_xml_notification.apply_async(args=[validation])
        return Response(response=build_response_js(status=200, requestip=requestip, uploadid=uploadid), status=200, mimetype='application/json')


def insert_upload(datadict):
    """
    This method is a helper
    """
    logger.info("Begging upload...")
    settings = Configuration()
    client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
    try:
        db = client[settings.MONGO_DB]
        #Specify mongo collection
        upload = db.posts
        uploadid = upload.insert_one(datadict).inserted_id
        return uploadid
    except errors.NetworkTimeout as e:
        logger.info("Insert failed. There has been a network error. ", e)
        return None
    except errors.OperationFailure as e:
        logger.info("Insert failed. There has been an operation failure. ", e)
        return None
    finally:
        client.close()
        logger.info("Upload completed! Upload ID: " + str(uploadid))


def build_response_js(status, requestip, uploadid=None):
    """
    This method builds the json to return to the client that posted.
    """
    MESSAGES = {'Success': "Your request was succesfully processed.",
                'Failure': "Your request failed to processed."}
    responsejs = {'ip': requestip,
                  'uploadid': uploadid}
    if status == 200:
        responsejs["Success"] = MESSAGES['Success']
    else:
        responsejs["Failure"] = MESSAGES['Failure']
    responsejs = dumps(responsejs)
    return responsejs


def validate_xml(xml):
    """
    This method is meant to validate an xml string and return a state of true or an parsing error message.
    """
    try:
        xml = ET.fromstring(xml)
        if xml is not None:
            return True
    except ET.ParseError as e:
        return "XML Parse Error: " + str(e)