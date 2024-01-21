"""just login and register"""

from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token

from src.extensions import db
from src.models.public import User, UserShop
from src.serializers.public import UserSchema
from . import public_bp


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
        request_data = request.get_json()
        try:
            data = UserSchema().load(
                request_data, session=db.session, unknown="exclude"
            )
            user = User.query.filter_by(email=data.email).first()
            if user and user.password != data.password:
                return {"message": "invalid credentials"}, 400
            if workspace := request_data.get("shop"):
                # Shop specific login
                user_shop = UserShop.query.filter_by(
                    user_id=user.id, shop_id=workspace
                ).first_or_404("shop not found")
                access_token = create_access_token(
                    identity=user.id,
                    # shop specific claims for shop specific login and access
                    additional_claims={"tenant": user_shop.shop_id},
                )
                refresh_token = create_refresh_token(
                    identity=user.id,
                    additional_claims={"tenant": user_shop.shop_id},
                )
            else:
                # Global login
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        except ValidationError as err:
            return err.messages, 400


# add url rule
public_bp.add_url_rule(
    "/auth/register", view_func=RegisterAPI.as_view("register")
)
public_bp.add_url_rule("/auth/login", view_func=LoginAPI.as_view("login"))
