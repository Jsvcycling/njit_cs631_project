from flask import Blueprint, request, session, render_template, redirect, url_for, flash

from db import db

# The customer-based routes.
customer_bp = Blueprint('customer_bp', __name__)

#-----------------------------
#
# Basic Routes
#
#-----------------------------
@customer_bp.route('/', methods=['GET'])
def index():
    user = None
    if 'cid' in session:
        c = db.cursor()
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()
        c.close()
        
    return render_template('customer/index.html', user=user)

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'cid' in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('customer/login.html')
    else:
        c = db.cursor()
        c.execute('SELECT CID FROM customer where Email=?', (request.form['email'],))
        user = c.fetchone()
        c.close()

        if user:
            session['cid'] = user['CID']
            return redirect('/')
        else:
            flash('User not found.')
            return render_template('customer/login.html')

@customer_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('cid', None)
    return redirect('/')

@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'cid' in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('customer/register.html')
    else:
        c = db.cursor()
        
        c.execute('INSERT INTO customer (FName, LName, Email) VALUES (?, ?, ?)', (
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
        ))
        
        db.commit()

        c.execute('SELECT CID FROM customer WHERE Email=?', (request.form['email'],))
        user = c.fetchone()
        c.close()

        if user:
            session['cid'] = user['CID']
            return redirect('/')
        else:
            flash('An error occurred. Please try again.')
            return render_template('customer/register.html')

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

@customer_bp.route('/orders/<int:order_id>', methods=['GET'])
def show_order(order_id):
    pass
