from flask import Blueprint, request, session, g

# The customer-based routes.
customer_bp = Blueprint('customer_bp', __name__)

#-----------------------------
#
# Basic Routes
#
#-----------------------------
@customer_bp.route('/', methods=['GET'])
def index():
    pass

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass

@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    pass

#-----------------------------
#
# Profile Management
#
#-----------------------------
@customer_bp.route('/profile', methods=['GET'])
def show_profile():
    pass

@customer_bp.route('/profile/update', methods=['POST'])
def update_profile():
    pass

@customer_bp.route('/profile/delete', methods=['POST'])
def delete_profile():
    pass

#-----------------------------
#
# Shipping Address Management
#
#-----------------------------
@customer_bp.route('/profile/addresses', methods=['GET'])
def list_addresses():
    pass

@customer_bp.route('/profile/addresses/new', methods=['POST'])
def create_address():
    pass

@customer_bp.route('/profile/addresses/update', methods=['POST'])
def update_address():
    pass

@customer_bp.route('/profile/addresses/delete', methods=['POST'])
def delete_address():
    pass

#-----------------------------
#
# Credit Card Management
#
#-----------------------------
@customer_bp.route('/profile/cards', methods=['GET'])
def list_cards():
    pass

@customer_bp.route('/profile/cards/new', methods=['POST'])
def create_card():
    pass

@customer_bp.route('/profile/cards/update', methods=['POST'])
def update_card():
    pass

@customer_bp.route('/profile/cards/delete', methods=['POST'])
def delete_card():
    pass

#-----------------------------
#
# Cart Management
#
#-----------------------------
@customer_bp.route('/basket', methods=['GET'])
def show_basket():
    pass

@customer_bp.route('/basket/add', methods=['GET'])
def add_to_basket():
    pass

@customer_bp.route('/basket/edit', methods=['POST'])
def update_basket():
    pass

#-----------------------------
#
# Order Management
#
#-----------------------------
@customer_bp.route('/orders', methods=['GET'])
def list_orders():
    pass

@customer_bp.route('/orders/<order_id:int>', methods=['GET'])
def show_order(order_id):
    pass
