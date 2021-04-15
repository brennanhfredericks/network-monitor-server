import os
from flask import Flask
from .common import db, api


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # app configuration setup here

    return app


app = create_app()
# flask app configuration
