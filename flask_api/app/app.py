import os
from flask import Flask
from .common import db, api


app = Flask(__name__)

# flask app configuration
