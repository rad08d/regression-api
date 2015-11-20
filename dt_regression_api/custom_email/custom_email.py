__author__ = 'alandinneen'
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email(object):
    """
    This class is used to generate the base email structure for all api responses.
    """

    ### Email specific dodads ####
    _RECIEVERS = 'dtregression@eshots.com'
    _SENDER = 'dtregression@eshots.com'
    _MSGSUBJECT = 'DT Testing API -- Response'
    _BASE_EMAIL_HTML = """
        <html>
            <head><h1>DT Regression API Response Message</h1></head>
                <br>
            <body>
                <p>
                    {0}
                </p>
            </body>
        </html>
    """
    ### SMTP specific configs ####
    _MAIL_SERVER = 'smtp.gmail.com'
    _MAIL_PORT = 587
    _MAIL_USER = 'regressioneshots@gmail.com'
    _MAIL_USER_PASS = '!Welcome1'

    def _build_base_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = self._MSGSUBJECT
        msg['From'] = self._SENDER
        msg['To'] = self._RECIEVERS
        self._msgTxt = ''
        return msg

    def send_email(self):
        self.msg.attach(MIMEText(self._BASE_EMAIL_HTML.format(self._msgTxt), 'html'))
        s = SMTP(self._MAIL_SERVER, self._MAIL_PORT)
        s.ehlo()
        s.starttls()
        s.login(self._MAIL_USER, self._MAIL_USER_PASS)
        s.sendmail(self._MAIL_USER, self._RECIEVERS, self.msg.as_string())
        s.quit()


class SuccessEmail(Email):
    """
    This class is used to inherit from a base email class and build a new success email.
    It should be used to configure any future successful email specific logic.
    """

    def __init__(self, msgTxt=None):
        self.msg = super(SuccessEmail, self)._build_base_email()
        self._msgTxt = msgTxt


class FailureEmail(Email):
    """
    This class is used to build an email notification that some sort of failure occurred.
    It should be used to configure any future failure email specific logic
    """

    def __init__(self, msgTxt=None):
        self.msg = super(FailureEmail, self)._build_base_email()
        self._msgTxt = msgTxt
