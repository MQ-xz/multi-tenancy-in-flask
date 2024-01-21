"""Public models"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, String, Integer, ForeignKey

from src.extensions import db


class User(db.Model):
    """User model"""

    __bind_key__ = "public"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    # saving password in plain text is not recommended, this is just for demo
    password = Column(String(50), nullable=False)


class Shop(db.Model):
    """Shop model"""

    __bind_key__ = "public"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)


class UserShop(db.Model):
    """UserShop model"""

    __bind_key__ = "public"

    user_id = Column(ForeignKey(User.id), primary_key=True)
    shop_id = Column(ForeignKey(Shop.id), primary_key=True)
