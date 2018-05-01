import operator

from datetime import datetime

from flask import Blueprint, request, session, g, render_template

from db import db

# The statistics-based routes.
statistics_bp = Blueprint('statistics_bp', __name__)

#-----------------------------
#
# Basic Routes
#
#-----------------------------
@statistics_bp.route('/most_freq', methods=['GET'])
def most_freq_sold():
    start_time = 0
    end_time = datetime.now().timestamp()

    if 'start_time' in request.args:
        start_time = datetime.strptime(request.args.get('start_time'),
                                       '%d/%m/%Y %H:%M:%S %p').timestamp()

    if 'end_time' in request.args:
        end_time = datetime.strptime(request.args.get('end_time'),
                                     '%d/%m/%Y %H:%M:%S %p').timestamp()

    c = db.cursor()
    c.execute("""
    SELECT p.PID as PID, p.PName as PName, SUM(a.Quantity) as Quantity
    FROM product p
    JOIN appears_in a ON p.PID = a.PID
    JOIN cart c ON a.CartID = c.CartID
    WHERE c.TDate > ? AND c.TDate < ? AND c.TStatus = ?
    GROUP BY p.PID, p.PName
    """, (start_time, end_time, 'Purchased',))
    prods = c.fetchall()

    user = None

    if 'cid' in session:
        c.execute('SELECT * from customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    for idx, prod in enumerate(prods):
        prod = dict(zip(prod.keys(), prod))
        prods[idx] = prod

    prods.sort(key=operator.itemgetter('Quantity'), reverse=True)

    print(prods)

    return render_template('statistics/most_freq.html', user=user, prods=prods)
        
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
