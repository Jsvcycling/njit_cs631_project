from flask import Blueprint, request, session, g, render_template

from db import db

# The product-based routes.
product_bp = Blueprint('product_bp', __name__)

#-----------------------------
#
# Basic Routes
#
#-----------------------------
@product_bp.route('/', methods=['GET'])
def list_products():
    q = request.args.get('query', '', type=str)
    prods = None
    user = None
    
    c = db.cursor()

    if len(q) > 0:
        # Bad idea. Doesn't protect against SQL injection.
        c.execute("""
        SELECT * FROM product
        LEFT JOIN offer_product USING (PID)
        WHERE product.PName LIKE \'%{}%\'
        """.format(q))
        prods = c.fetchall()
    else:
        c.execute("""
        SELECT * FROM product
        LEFT JOIN offer_product USING (PID)
        """)
        prods = c.fetchall()

    if 'cid' in session:
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    c.close()
    return render_template('product/list_products.html', prods=prods, user=user, q=q)

@product_bp.route('/<int:product_id>', methods=['GET'])
def show_product(product_id):
    c = db.cursor()
    c.execute("""
    SELECT * FROM product
    LEFT JOIN offer_product ON product.PID = offer_product.PID
    LEFT JOIN computer ON product.PID = computer.PID
    LEFT JOIN laptop ON product.PID = laptop.PID
    LEFT JOIN printer ON product.PID = printer.PID
    WHERE product.PID=?
    """, (product_id,))
    prod = c.fetchone()
    
    user = None

    if 'cid' in session:
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    c.close()
    return render_template('product/show_product.html', prod=prod, user=user)
