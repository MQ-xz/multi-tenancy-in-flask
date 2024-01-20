"""App"""
# use factory patter

from flask import Flask

from src.api.views import api
from src.extensions import db, migrate


def create_app():
    """Create app"""
    _app = Flask(__name__)

    # load config from settings.py
    _app.config.from_object("src.settings")

    # register blueprints
    _app.register_blueprint(api)

    # register extensions
    extensions(_app)

    return _app


def extensions(_app):
    """Register extensions"""
    db.init_app(_app)
    migrate.init_app(_app, db)


app = create_app()
