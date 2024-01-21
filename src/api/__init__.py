"""APIs"""

from flask import Blueprint

public_bp = Blueprint("public", __name__, url_prefix="/api/v1/")
tenant_bp = Blueprint("tenant", __name__, url_prefix="/api/v1/")

# pylint: disable=wrong-import-position
from . import (
    views,
    auth,
    shop,
    product,
)
