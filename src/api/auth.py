"""just login and register"""

from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token

from src.extensions import db
from src.models.public import User
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


class LoginAPI(MethodView):
    """Login"""

    def post(self):
        """Login"""
        # NOTE: since just a demo, we not handle exception like user not found, etc
        try:
            data = UserSchema().load(request.get_json(), session=db.session)
            user = User.query.filter_by(email=data.email).first()
            if user and user.password == data.password:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            return {"message": "invalid credentials"}, 400
        except ValidationError as err:
            return err.messages, 400


# add url rule
api.add_url_rule("/auth/register", view_func=RegisterAPI.as_view("register"))
api.add_url_rule("/auth/login", view_func=LoginAPI.as_view("login"))
