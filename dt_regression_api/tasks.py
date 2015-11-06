__author__ = 'alandinneen'
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery
from settings import Configuration


#Create and load celery to handle async processes
settings = Configuration()
celery = Celery('tasks', broker=settings.CELERY_BROKER_URL)

@celery.task
def send_upload_notification(data):
    settings = Configuration()
    RECIEVERS = settings.MAIL_RECIPIENT
    MESSAGETEXT = settings.MESSAGES['Success'] + "\nYour uploaded data: \n " + data
    msg = MIMEMultipart()
    msg['Subject'] = "Test email from Testing API"
    msg['From'] = settings.MAIL_DEFAULT_SENDER
    msg['To'] = RECIEVERS
    msg.attach(MIMEText(MESSAGETEXT, 'plain'))
    s = SMTP(settings.MAIL_SERVER, 587)
    s.ehlo()
    s.starttls()
    s.login(settings.MAIL_USER, settings.MAIL_USER_PASS)
    s.sendmail(settings.MAIL_USER, settings.MAIL_RECIPIENT, msg.as_string())
    s.quit()