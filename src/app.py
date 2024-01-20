"""App"""
# use factory patter

from flask import Flask

from src.api.views import api


def create_app():
    """Create app"""
    _app = Flask(__name__)

    # register blueprints
    _app.register_blueprint(api)

    return _app


app = create_app()
