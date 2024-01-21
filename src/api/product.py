"""Products APIs"""

from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from src.extensions import db
from src.models.tenant import Product
from src.serializers.tenant import ProductSchema
from src.api import tenant_bp


class ProductsAPI(MethodView):
    """Products API"""

    def get(self):
        """Get products"""
        products = Product.query.all()
        return ProductSchema(many=True).dump(products)

    def post(self):
        """Create a new product"""
        try:
            product = ProductSchema().load(
                request.get_json(), session=db.session
            )
        except ValidationError as err:
            return err.messages, 400
        db.session.add(product)
        db.session.commit()
        return ProductSchema().dump(product), 201


class ProductAPI(MethodView):
    """Product API"""

    def get(self, product_id):
        """Get a product"""
        product = Product.query.get_or_404(product_id)
        return ProductSchema().dump(product)

    def put(self, product_id):
        """Update a product"""
        product = Product.query.get_or_404(product_id)
        product = ProductSchema().load(request.json, instance=product)
        db.session.commit()
        return ProductSchema().dump(product)

    def delete(self, product_id):
        """Delete a product"""
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return "", 204


tenant_bp.add_url_rule(
    "/products", view_func=ProductsAPI.as_view("products_api")
)
tenant_bp.add_url_rule(
    "/products/<int:product_id>", view_func=ProductAPI.as_view("product_api")
)
