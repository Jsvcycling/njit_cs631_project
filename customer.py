from datetime import datetime

from flask import Blueprint, request, session, render_template, redirect, url_for, \
    flash

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
        c.execute("""
        SELECT * FROM customer c
        LEFT JOIN shipping_address s ON c.CID = s.CID AND c.Address = s.SAName
        WHERE c.CID=?
        """, (session['cid'],))
        user = c.fetchone()
        c.close()

    if user:
        return render_template('customer/profile.html', user=user)
        
    return render_template('customer/index.html')

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'cid' in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('customer/login.html')
    else:
        c = db.cursor()
        c.execute('SELECT CID FROM customer where Email=?', (
            request.form['email'],
        ))
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
        c.execute("""
        INSERT INTO customer (FName, LName, Email)
        VALUES (?, ?, ?)
        """, (
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
        ))
        db.commit()

        c.execute('SELECT CID FROM customer WHERE Email=?', (
            request.form['email'],
        ))
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
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    return redirect('/')

@customer_bp.route('/profile/update', methods=['GET', 'POST'])
def update_profile():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')
    
    if request.method == 'GET':
        c = db.cursor()
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()
        c.close()

        if not user:
            flash('An internal error occured.')
            return redirect('/')
        
        return render_template('customer/update.html', user=user)
    else:
        c = db.cursor()
        c.execute("""
        UPDATE customer SET FName=?, LName=?, Email=?, Phone=?
        WHERE CID=?
        """, (
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
            request.form['phone'],
            session['cid'],
        ))
        db.commit()
        c.close()

        flash('Profile successfully updated.')
        return redirect('/profile')

@customer_bp.route('/profile/delete', methods=['GET'])
def delete_profile():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')
    
    c = db.cursor()
    c.execute('DELETE FROM customer WHERE CID=?', (session['cid'],))
    db.commit()
    c.close()

    session.pop('cid', None)
    
    flash('User account has been successfully deleted.')
    return redirect('/')

#-----------------------------
#
# Shipping Address Management
#
#-----------------------------
@customer_bp.route('/profile/addresses', methods=['GET'])
def list_addresses():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('SELECT * FROM shipping_address WHERE CID=?', (session['cid'],))
    addrs = c.fetchall()
    c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
    user = c.fetchone()
    c.close()

    return render_template('customer/list_addresses.html', addrs=addrs, user=user)

@customer_bp.route('/profile/addresses/new', methods=['GET', 'POST'])
def create_address():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    if request.method == 'GET':
        c = db.cursor()
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()
        c.close()

        return render_template('customer/new_address.html', user=user)
    else:
        c = db.cursor()

        c.execute("""
        INSERT INTO shipping_address VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session['cid'],
            request.form['name'],
            request.form['recipient_name'],
            request.form['street'],
            request.form['house_num'],
            request.form['city'],
            request.form['zip_code'],
            request.form['state'],
            request.form['country'],
        ))

        db.commit()
        c.close()

        flash('Successfully added shipping address.')
        return redirect('/profile/addresses')

@customer_bp.route('/profile/addresses/<name>/update', methods=['GET', 'POST'])
def update_address(name):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    if request.method == 'GET':
        c = db.cursor()
        c.execute('SELECT * FROM shipping_address WHERE CID=? AND SAName=?', (
            session['cid'],
            name,
        ))
        addr = c.fetchone()
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()
        c.close()

        return render_template('customer/update_address.html', addr=addr, user=user)
    else:
        c = db.cursor()

        c.execute("""
        UPDATE shipping_address SET RecipientName=?, Street=?, SNumber=?,
        City=?, Zip=?, State=?, Country=?
        WHERE CID=? AND SAName=?
        """, (
            request.form['recipient_name'],
            request.form['street'],
            request.form['house_num'],
            request.form['city'],
            request.form['zip_code'],
            request.form['state'],
            request.form['country'],
            session['cid'],
            name,
        ))

        db.commit()
        c.close()

        flash('Successfully updatd shipping address.')
        return redirect('/profile/addresses')

@customer_bp.route('/profile/addresses/<name>/delete', methods=['GET'])
def delete_address(name):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('DELETE FROM shipping_address WHERE CID=? AND SAName=?', (
        session['cid'],
        name,
    ))
    db.commit()
    c.close()

    flash('Successfully deleted shipping address.')
    return redirect('profile/addresses')

#-----------------------------
#
# Credit Card Management
#
#-----------------------------
@customer_bp.route('/profile/cards', methods=['GET'])
def list_cards():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute("""
    SELECT * FROM credit_card JOIN stored_card USING (CCNumber)
    WHERE CID=?
    """, (session['cid'],))
    cards = c.fetchall()
    c.execute('SELECT * FROM customer where CID=?', (session['cid'],))
    user = c.fetchone()
    c.close()

    return render_template('customer/list_cards.html', cards=cards, user=user)

@customer_bp.route('/profile/cards/new', methods=['GET', 'POST'])
def create_card():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    if request.method == 'GET':
        c = db.cursor()
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()
        c.close()

        return render_template('customer/new_card.html', user=user)
    else:
        c = db.cursor()

        c.execute('INSERT INTO credit_card VALUES (?, ?, ?, ?, ?, ?)', (
            request.form['cc_number'],
            request.form['cc_code'],
            request.form['cc_owner'],
            request.form['cc_type'],
            request.form['cc_zip'],
            request.form['cc_date'],
            ))
        c.execute('INSERT INTO stored_card VALUES (?, ?)', (
            request.form['cc_number'],
            session['cid'],
        ))
        
        db.commit()
        c.close()

        flash('Successfully added credit card.')
        return redirect('/profile/cards')

@customer_bp.route('/profile/cards/<cc_number>/update', methods=['GET', 'POST'])
def update_card(cc_number):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    if request.method == 'GET':
        c = db.cursor()
        c.execute("""
        SELECT * FROM credit_card JOIN stored_card USING (CCNumber)
        WHERE CCNumber=? AND CID=?
        """, (
            cc_number,
            session['cid'],
        ))
        card = c.fetchone()
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()
        c.close()

        return render_template('customer/update_card.html', card=card, user=user)
    else:
        c = db.cursor()

        c.execute("""
        UPDATE credit_card SET SecNumber=?, OwnerName=?, CCType=?, CCZip=?, CCDate=?
        WHERE CCNumber=?
        """, (
            request.form['cc_code'],
            request.form['cc_owner'],
            request.form['cc_type'],
            request.form['cc_zip'],
            request.form['cc_date'],
            cc_number,
        ))

        db.commit()
        c.close()

        flash('Successfully updatd credit card.')
        return redirect('/profile/cards')

@customer_bp.route('/profile/cards/<cc_number>/delete', methods=['GET'])
def delete_card(cc_number):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('DELETE FROM stored_card WHERE CID=? AND CCNumber=?', (
        session['cid'],
        cc_number,
    ))
    db.commit()
    c.close()

    flash('Successfully deleted credit card.')
    return redirect('profile/cards')

#-----------------------------
#
# Cart Management
#
#-----------------------------
@customer_bp.route('/basket', methods=['GET'])
def show_basket():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute("""
    SELECT * FROM product
    JOIN appears_in ON product.PID = appears_in.PID
    JOIN cart ON cart.CartID = appears_in.CartID
    WHERE cart.CID=? AND cart.TStatus=?
    """, (
        session['cid'],
        'Open',
    ))
    products = c.fetchall()
    c.execute('SELECT * FROM shipping_address WHERE CID=?', (session['cid'],))
    addrs = c.fetchall()
    c.execute("""
    SELECT * FROM credit_card JOIN stored_card USING (CCNumber)
    WHERE CID=?
    """, (session['cid'],))
    cards = c.fetchall()
    c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
    user = c.fetchone()
    c.close()

    # Compute the total price for each item.
    for idx, prod in enumerate(products):
        prod = dict(zip(prod.keys(), prod))
        prod['Cost'] = round(prod['Quantity'] * prod['PriceSold'], 2)
        products[idx] = prod

    # Compute the total price of the purchase.
    total = 0.0
    for prod in products:
        total += prod['Cost']

    total = round(total, 2)

    return render_template('customer/cart.html', prods=products, addrs=addrs,
                           cards=cards, total=total, user=user)

@customer_bp.route('/basket/purchase', methods=['POST'])
def purchase_basket():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    print(request.form['addr_name'])

    if request.form['addr_name'] == '' or request.form['cc_number'] == '':
        flash('Please select a shipping address and credit card')
        return redirect('/basket')

    c = db.cursor()
    c.execute('SELECT CartID FROM cart WHERE CID=? AND TStatus=?', (
        session['cid'],
        'Open',
    ))
    cart = c.fetchone()
    c.execute("""
    UPDATE cart SET SAName=?, CCNumber=?, TStatus=?, TDate=?
    WHERE CID=? AND TStatus=?
    """, (
        request.form['addr_name'],
        request.form['cc_number'],
        'Purchased',
        datetime.now().timestamp(),
        session['cid'],
        'Open',
    ))
    db.commit()
    c.close()

    flash('Successfully purchased products.')
    return redirect('/')

@customer_bp.route('/basket/clear', methods=['GET'])
def clear_basket():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('SELECT CartID FROM cart WHERE CID=? AND TStatus=?', (
        session['cid'],
        'Open',
    ))
    cart = c.fetchone()

    if cart:
        c.execute('DELETE FROM appears_in WHERE CartID=?', (cart['CartID'],))
        db.commit()

    c.close()

    flash('Cleared cart.')
    return redirect('/basket')

@customer_bp.route('/basket/<int:product_id>/add', methods=['GET'])
def add_to_basket(product_id):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('SELECT CartID FROM cart WHERE CID=? AND TStatus=?', (
        session['cid'],
        'Open',
    ))
    cart = c.fetchone()
    c.execute('SELECT * FROM product WHERE PID=?', (product_id,))
    prod = c.fetchone()

    if not prod:
        flash('Product not found.')
        return redirect('/basket')

    if not cart:
        # Create a cart and get the cart id.
        c.execute('INSERT INTO cart (CID) VALUES (?)', (session['cid'],))
        db.commit()
        c.execute('SELECT CartID FROM cart WHERE CID=? AND TStatus=?', (
            session['cid'],
            'Open',
        ))
        cart = c.fetchone()

    cart_id = cart['CartID']

    # Check to see if the item is already in the cart.
    c.execute('SELECT * FROM appears_in WHERE CartID=? AND PID=?', (
        cart_id,
        product_id,
    ))
    prod_cart = c.fetchone()

    if prod_cart:
        # Item already in cart, increment quantity.
        c.execute('UPDATE appears_in SET Quantity=? WHERE CartID=? AND PID=?', (
            prod_cart['Quantity'] + 1,
            cart_id,
            product_id,
        ))
        db.commit()
        c.close()

        flash('Item already in basket. Incremented quantity.')
        return redirect('/basket')

    c.execute('SELECT * FROM offer_product WHERE PID=?', (product_id,))
    offer = c.fetchone()
    c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
    user = c.fetchone()

    price_sold = prod['PPrice']

    if user['Status'] == 'Gold' or user['Status'] == 'Platinum':
        price_sold = offer['OfferPrice']

    c.execute('INSERT INTO appears_in VALUES (?, ?, ?, ?)', (
        cart_id,
        product_id,
        1,
        price_sold,
    ))
    db.commit()
    c.close()

    flash('Item successfully added to cart.')
    return redirect('/basket')

@customer_bp.route('/basket/<int:product_id>/update', methods=['POST'])
def update_basket_item(product_id):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('SELECT CartID FROM cart WHERE CID=? AND TStatus=?', (
        session['cid'],
        'Open',
    ))
    cart = c.fetchone()
    c.execute('SELECT * FROM appears_in WHERE CartID=? AND PID=?', (
        cart['CartID'],
        product_id,
    ))
    prod_cart = c.fetchone()

    if prod_cart:
        c.execute('UPDATE appears_in SET Quantity=? WHERE CartID=? AND PID=?', (
            request.form['quantity'],
            cart['CartID'],
            product_id,
        ))
        db.commit()
        
    c.close()

    flash('Cart succesfully updated.')
    return redirect('/basket')

@customer_bp.route('/basket/<int:product_id>/delete', methods=['GET'])
def delete_basket_item(product_id):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute('SELECT CartID FROM cart WHERE CID=? AND TStatus=?', (
        session['cid'],
        'Open',
    ))
    cart = c.fetchone()
    c.execute('DELETE FROM appears_in WHERE CartID=? AND PID=?', (
        cart['CartID'],
        product_id,
    ))
    db.commit()
    c.close()

    flash('Successfully removed item from cart.')
    return redirect('/basket')

#-----------------------------
#
# Order Management
#
#-----------------------------
@customer_bp.route('/orders', methods=['GET'])
def list_orders():
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')

    c = db.cursor()
    c.execute("""
    SELECT * FROM cart WHERE CID=? AND TStatus=? ORDER BY TDate DESC
    """, (session['cid'], 'Purchased',))
    orders = c.fetchall()
    c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
    user = c.fetchone()

    for idx, order in enumerate(orders):
        order = dict(zip(order.keys(), order))
        
        c.execute('SELECT * FROM appears_in WHERE CartID=?', (
            order['CartID'],
        ))
        prods = c.fetchall()

        order_total = 0

        for prod in prods:
            order_total += prod['Quantity'] * prod['PriceSold']

        order['TotalPrice'] = round(order_total, 2)
        order['TDate'] = datetime.fromtimestamp(order['TDate']).strftime(
            '%A %B %d, %Y %I:%M:%S %p'
        )
        orders[idx] = order

    print(orders)

    return render_template('customer/list_orders.html', orders=orders,
                           user=user)

@customer_bp.route('/orders/<int:order_id>', methods=['GET'])
def show_order(order_id):
    if 'cid' not in session:
        flash('You must be authenticated to view that page.')
        return redirect('/login')
    
    c = db.cursor()
    c.execute("""
    SELECT * FROM product
    JOIN appears_in ON product.PID = appears_in.PID
    JOIN cart ON cart.CartID = appears_in.CartID
    WHERE cart.CartID=?
    """, (order_id,))
    products = c.fetchall()
    c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
    user = c.fetchone()
    c.close()

    # Compute the total price for each item.
    for idx, prod in enumerate(products):
        prod = dict(zip(prod.keys(), prod))
        prod['Cost'] = round(prod['Quantity'] * prod['PriceSold'], 2)
        products[idx] = prod

    # Compute the total price of the purchase.
    total = 0.0
    for prod in products:
        total += prod['Cost']

    total = round(total, 2)

    return render_template('customer/show_order.html', prods=products,
                           total=total, user=user)
