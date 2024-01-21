"""Views"""
from flask import jsonify

from . import public_bp


def index():
    """Index"""
    return jsonify({"message": "Hello, World!"})


public_bp.add_url_rule("/", view_func=index)
