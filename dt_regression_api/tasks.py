__author__ = 'alandinneen'
from custom_email import custom_email as em
from celery import Celery
from settings import Configuration


#Create and load celery to handle async processes
settings = Configuration()
celery = Celery('tasks', broker=settings.CELERY_BROKER_URL)


@celery.task
def send_successful_upload_notification(data):
    msg = """
    <h4>Your upload was succesfully uploaded!</h4>
    <h4>Here is what was uploaded:</h4>
        <br>
    <h4>{0}</h4>
    """.format(data)
    assemble_send_email(msg=msg)

@celery.task
def send_vaidated_xml_notification(data):
    msg = """
    <h4>Your uploaded XML syntax has been validated. Nice job!</h4>
    <h4>Below is your validated XML: </h4>
        <br>
    <h4>{0}</h4>
    """.format(data)
    assemble_send_email(msg=msg)

@celery.task
def send_invalid_xml_notification(message, data):
    msg = """
    <h4>Your uploaded XML syntax is INVALID.....come on, rookie.....</h4>
    <h4>Below is what Python has to say about your XML: </h4>
        <br>
    <h4>{0}</h4>
    <h4>Your malformed XML is as follows: </h4>
    <h4>{1}</h4>
    """.format(message, data)
    assemble_send_email(msg=msg, success=False)

def assemble_send_email(msg,success=True):
    if success:
        email = em.SuccessEmail(msgTxt=msg)
    else:
        email = em.FailureEmail(msgTxt=msg)
    email.send_email()