"""Views"""
from flask import jsonify

from . import api_bp


def index():
    """Index"""
    return jsonify({"message": "Hello, World!"})


api_bp.add_url_rule("/", view_func=index)
