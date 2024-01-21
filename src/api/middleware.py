"""Middleware for the API

for handling tenant requests
"""

from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

from src.models.public import UserShop
from src.utils.database import Database
from . import tenant_bp


@tenant_bp.before_request
def before_request():
    """Before request

    switch tenant schema
    """
    verify_jwt_in_request()

    tenant = get_jwt().get("tenant")
    if not tenant:
        return {"message": "You are not logged into any tenant"}, 403

    user = get_jwt_identity()
    if not UserShop.query.filter_by(user_id=user, shop_id=tenant).first():
        return {"message": "You are not a member of this tenant"}, 403

    Database(tenant).switch_schema()
