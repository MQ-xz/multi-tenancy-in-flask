"""tenant based model"""

from sqlalchemy import Column, String, Integer, ForeignKey

from src.extensions import db
from .public import User


class Product(db.Model):
    """Product model"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)


class Order(db.Model):
    """Order model"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), nullable=False)
    product_id = Column(ForeignKey(Product.id), nullable=False)
