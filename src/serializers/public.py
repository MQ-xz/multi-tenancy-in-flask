"""Public model serializers"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


from src.models.public import User, Shop, UserShop


class UserSchema(SQLAlchemyAutoSchema):
    """User schema"""

    class Meta:
        """Meta class"""

        model = User
        load_instance = True


class ShopSchema(SQLAlchemyAutoSchema):
    """Shop schema"""

    class Meta:
        """Meta class"""

        model = Shop
        load_instance = True


class UserShopSchema(SQLAlchemyAutoSchema):
    """UserShop schema"""

    class Meta:
        """Meta class"""

        model = UserShop
        load_instance = True
