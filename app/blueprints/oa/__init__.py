from flask import Blueprint

bp = Blueprint('oa', __name__)

from app.blueprints.oa import routes 