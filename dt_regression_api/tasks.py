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
    <h1>Your upload was succesfully uploaded!</h1>
        <br>
    <h3>Here is what was uploaded:</h3>
        <br>
    <h5>{0}</h5>
    """.format(data)
    email = em.SuccessEmail(msgTxt=msg)
    email.send_email()
