"""Shop API endpoints"""

from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.serializers.public import ShopSchema, UserShopSchema
from src.extensions import db
from . import public_bp


class ShopsAPI(MethodView):
    """Shops API"""

    decorators = [jwt_required()]

    def post(self):
        """Create new shop"""
        try:
            shop = ShopSchema().load(request.get_json(), session=db.session)
            db.session.add(shop)
            db.session.flush()
            user_shop = UserShopSchema().load(
                {"user_id": get_jwt_identity(), "shop_id": shop.id},
                session=db.session,
            )
            db.session.add(user_shop)
            db.session.commit()
            return {"message": "success"}, 201
        except ValidationError as err:
            return err.messages, 400


public_bp.add_url_rule("/shops", view_func=ShopsAPI.as_view("shops"))
