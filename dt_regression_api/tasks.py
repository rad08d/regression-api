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
    <h3>Your upload was succesfully uploaded!</h3>
        <br>
    <h3>Here is what was uploaded:</h3>
        <br>
    <h4>{0}</h4>
    """.format(data)
    email = em.SuccessEmail(msgTxt=msg)
    email.send_email()
