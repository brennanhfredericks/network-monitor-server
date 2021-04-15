import os
from flask import Flask
from .common import db, api

# api resources
from .resources import Packet_EP


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # app configuration setup here
    app.config.from_envvar("YOURAPPLICATION_SETTINGS")
    return app


# flask app configuration
app = create_app()

# database configuration
db.init_app(app)


# api configuration
api.add_resource(Packet_EP, "/packets")

# init after adding resources
api.init_app(app)