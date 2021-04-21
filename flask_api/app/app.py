import os
from flask import Flask
from .common import db, api

# api resources
from .resources import Packet_EP, Packet_Table_EP, Packet_Table_Counts_EP


def create_database_uri():
    res = os.listdir("/run/secrets/")
    f = next(f for f in res if "-user" in f)

    with open(os.path.join("/run/secrets/", f), "r") as fin:
        line = fin.read()

    user, _, pas = line.split("=")

    uri = f"mysql+pymysql://{user}:{pas}@{os.getenv('DATABASE_URL')}/{os.getenv('DB_PACKETS')}"
    return uri


def create_app():
    app = Flask(__name__)

    # app configuration setup here
    app.config["SQLALCHEMY_DATABASE_URI"] = create_database_uri()
    debug = os.getenv("DEBUG", False)
    debug = bool(debug) if isinstance(debug, str) else debug
    app.config["DEBUG"] = debug
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app


# flask app configuration
app = create_app()
app.app_context().push()

# database configuration
db.init_app(app)


# api configuration
api.add_resource(Packet_EP, "/", "/packets")
api.add_resource(Packet_Table_EP, "/", "/packets/tables")
api.add_resource(Packet_Table_Counts_EP, "/", "/packets/tables/<protocol_name>")

# init after adding resources
api.init_app(app)