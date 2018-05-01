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

    start_time_str = request.args.get('start_time', '', type=str)
    end_time_str   = request.args.get('end_time', '', type=str)

    if len(start_time_str) > 0:
        start_time = datetime.strptime(start_time_str,
                                       '%d/%m/%Y %H:%M:%S %p').timestamp()

    if len(end_time_str) > 0:
        end_time = datetime.strptime(end_time_str,
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

    c.close()

    prods.sort(key=operator.itemgetter('Quantity'), reverse=True)

    print(prods)

    return render_template('statistics/most_freq.html', user=user, prods=prods,
                           start_time=start_time_str, end_time=end_time_str)
        
@statistics_bp.route('/most_unique', methods=['GET'])
def most_unique_sold():
    start_time = 0
    end_time = datetime.now().timestamp()

    start_time_str = request.args.get('start_time', '', type=str)
    end_time_str   = request.args.get('end_time', '', type=str)

    if len(start_time_str) > 0:
        start_time = datetime.strptime(start_time_str,
                                       '%d/%m/%Y %H:%M:%S %p').timestamp()

    if len(end_time_str) > 0:
        end_time = datetime.strptime(end_time_str,
                                     '%d/%m/%Y %H:%M:%S %p').timestamp()

    c = db.cursor()
    c.execute("""
    SELECT p.PID as PID, p.PName as PName, COUNT(DISTINCT c.CID) as NumCust
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

    c.close()

    for idx, prod in enumerate(prods):
        prod = dict(zip(prod.keys(), prod))
        prods[idx] = prod

    prods.sort(key=operator.itemgetter('NumCust'), reverse=True)

    print(prods)

    return render_template('statistics/most_unique.html', user=user,
                           prods=prods, start_time=start_time_str,
                           end_time=end_time_str)

@statistics_bp.route('/best_customers', methods=['GET'])
def best_customers():
    start_time = 0
    end_time = datetime.now().timestamp()

    start_time_str = request.args.get('start_time', '', type=str)
    end_time_str   = request.args.get('end_time', '', type=str)

    if len(start_time_str) > 0:
        start_time = datetime.strptime(start_time_str,
                                       '%d/%m/%Y %H:%M:%S %p').timestamp()

    if len(end_time_str) > 0:
        end_time = datetime.strptime(end_time_str,
                                     '%d/%m/%Y %H:%M:%S %p').timestamp()

    c = db.cursor()
    c.execute("""
    SELECT c.CID AS CID, c.FName AS FName, c.LName AS LName,
    SUM(a.TotalPrice) AS TotalPrice
    FROM customer c
    JOIN cart b ON c.CID = b.CID
    JOIN (SELECT CartID, SUM(Quantity * PriceSold) AS TotalPrice
    FROM appears_in GROUP BY CartID) a ON b.CartID = a.CartID
    WHERE b.TDate > ? AND b.TDate < ? AND b.TStatus = ?
    GROUP BY c.CID, c.FName, c.LName LIMIT 10
    """, (start_time, end_time, 'Purchased',))
    custs = c.fetchall()

    user = None

    if 'cid' in session:
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    c.close()

    for idx, cust in enumerate(custs):
        cust = dict(zip(cust.keys(), cust))
        custs[idx] = cust

    custs.sort(key=operator.itemgetter('TotalPrice'), reverse=True)

    print(custs)

    return render_template('statistics/best_customers.html', user=user,
                           custs=custs, start_time=start_time_str,
                           end_time=end_time_str)

@statistics_bp.route('/best_zipcodes', methods=['GET'])
def best_zipcodes():
    start_time = 0
    end_time = datetime.now().timestamp()

    start_time_str = request.args.get('start_time', '', type=str)
    end_time_str   = request.args.get('end_time', '', type=str)

    if len(start_time_str) > 0:
        start_time = datetime.strptime(start_time_str,
                                       '%d/%m/%Y %H:%M:%S %p').timestamp()

    if len(end_time_str) > 0:
        end_time = datetime.strptime(end_time_str,
                                     '%d/%m/%Y %H:%M:%S %p').timestamp()

    c = db.cursor()
    c.execute("""
    SELECT s.Zip AS Zip, COUNT(c.CartID) AS NumShip FROM shipping_address s
    JOIN cart c ON c.CID = s.CID AND c.SAName = s.SAName
    WHERE c.TDate > ? AND c.TDate < ? AND c.TStatus = ?
    GROUP BY s.Zip LIMIT 5
    """, (start_time, end_time, 'Purchased',))
    zips = c.fetchall()

    user = None

    if 'cid' in session:
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    c.close()

    zips.sort(key=operator.itemgetter('NumShip'), reverse=True)

    print(zips)

    return render_template('statistics/best_zipcodes.html', user=user, zips=zips,
                           start_time=start_time_str, end_time=end_time_str)

@statistics_bp.route('/avg_price', methods=['GET'])
def avg_price():
    start_time = 0
    end_time = datetime.now().timestamp()

    start_time_str = request.args.get('start_time', '', type=str)
    end_time_str   = request.args.get('end_time', '', type=str)

    if len(start_time_str) > 0:
        start_time = datetime.strptime(start_time_str,
                                       '%d/%m/%Y %H:%M:%S %p').timestamp()

    if len(end_time_str) > 0:
        end_time = datetime.strptime(end_time_str,
                                     '%d/%m/%Y %H:%M:%S %p').timestamp()

    c = db.cursor()
    c.execute("""
    SELECT p.PID AS PID, p.PName AS PName,
    SUM(a.OrderCost) / SUM(a.Quantity) AS AvgPrice,
    a.OrderCost AS OrderCost, a.Quantity AS Quantityb
    FROM product p
    JOIN (SELECT CartID, PID, Quantity * PriceSold AS OrderCost, Quantity
    FROM appears_in) a ON a.PID = p.PID
    JOIN cart c ON a.CartID = c.CartID
    WHERE c.TDate > ? AND c.TDate < ? AND c.TStatus = ?
    GROUP BY p.PID, p.PName
    """, (start_time, end_time, 'Purchased',))
    prods = c.fetchall()

    user = None

    if 'cid' in session:
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    c.close()

    for idx, prod in enumerate(prods):
        prod = dict(zip(prod.keys(), prod))
        prod['AvgPrice'] = round(prod['AvgPrice'], 2)
        prods[idx] = prod

    prods.sort(key=operator.itemgetter('AvgPrice'), reverse=True)
        
    print(prods)

    return render_template('statistics/avg_price.html', user=user, prods=prods,
                           start_time=start_time_str, end_time=end_time_str)
