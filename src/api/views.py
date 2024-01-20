"""Views"""
from flask import jsonify, Blueprint

api = Blueprint("api", __name__, url_prefix="/api/v1")


def index():
    """Index"""
    return jsonify({"message": "Hello, World!"})


api.add_url_rule("/", view_func=index)
