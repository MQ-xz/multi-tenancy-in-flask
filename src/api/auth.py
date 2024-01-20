"""just login and register"""

from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from src.extensions import db
from src.serializers.public import UserSchema
from . import api


class RegisterAPI(MethodView):
    """Register"""

    def post(self):
        """Register"""
        try:
            data = UserSchema().load(request.get_json(), session=db.session)
            db.session.add(data)
            db.session.commit()
            return {"message": "success"}, 201
        except ValidationError as err:
            return err.messages, 400


# add url rule
api.add_url_rule("/auth/register", view_func=RegisterAPI.as_view("register"))
