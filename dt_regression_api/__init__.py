__author__ = 'alandinneen'
from flask import Flask
from . import customlogg
from .auth import auth_blueprint
from .api import api_blueprint

def create_app(config):
    app = Flask(__name__)
    add_blueprints(app)
    return app


def add_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint)