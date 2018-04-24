from flask import Blueprint, request, session, g

# The product-based routes.
product_bp = Blueprint('product_bp', __name__)

#-----------------------------
#
# Basic Routes
#
#-----------------------------
@product_bp.route('/', methods=['GET'])
def list_products():
    pass

@product_bp.route('/<int:product_id>', methods=['GET'])
def show_product(product_id):
    pass
