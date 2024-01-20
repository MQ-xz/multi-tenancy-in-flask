"""Views"""
from flask import jsonify

from . import api


def index():
    """Index"""
    return jsonify({"message": "Hello, World!"})


api.add_url_rule("/", view_func=index)
