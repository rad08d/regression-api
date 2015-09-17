__author__ = 'alandinneen'
from flask import Flask
from logging import getLogger
from . import auth_blueprint

def check_auth(username, password):
    """
    This method is used to check the username, password against the database to authenticate a sure
    """
