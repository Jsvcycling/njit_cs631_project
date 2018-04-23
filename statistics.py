from flask import Blueprint, request, session, g

# The statistics-based routes.
statistics_bp = Blueprint('statistics_bp', __name__)

#-----------------------------
#
# Basic Routes
#
#-----------------------------
@statistics_bp.route('/', methods=['GET'])
def index():
    pass

@statistics_bp.route('/most_freq')
def most_freq_sold():
    pass

@statistics_bp.route('/most_unique')
def most_unique_sold():
    pass

@statistics_bp.route('/best_customers')
def best_customers():
    pass

@statistics_bp.route('/best_zipcodes')
def best_zipcodes():
    pass

@statistics_bp.route('/avg_price')
def avg_price():
    pass
