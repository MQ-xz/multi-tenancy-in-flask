"""tenant based models"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models.tenant import Product, Order


class ProductSchema(SQLAlchemyAutoSchema):
    """Product schema"""

    class Meta:
        """Meta class"""

        model = Product
        load_instance = True


class OrderSchema(SQLAlchemyAutoSchema):
    """Order schema"""

    class Meta:
        """Meta class"""

        model = Order
        load_instance = True
        include_fk = True
