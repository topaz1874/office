from flask import Blueprint

bp = Blueprint('mqtt', __name__)

from app.blueprints.mqtt import routes 