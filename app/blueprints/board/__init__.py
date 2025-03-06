from flask import Blueprint

bp = Blueprint('board', __name__)

from app.blueprints.board import routes 