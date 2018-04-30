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
        c.execute('SELECT * FROM product WHERE PName LIKE \'%{}%\''.format(q))
        prods = c.fetchall()
    else:
        c.execute('SELECT * FROM product')
        prods = c.fetchall()

    if 'cid' in session:
        c.execute('SELECT * FROM customer WHERE CID=?', (session['cid'],))
        user = c.fetchone()

    # TODO: If the user exists and they are Gold or Platinum status, show the
    #       discounted price (e.g. cross out original price).

    c.close()
    return render_template('product/list_products.html', prods=prods, user=user, q=q)

@product_bp.route('/<int:product_id>', methods=['GET'])
def show_product(product_id):
    if request.method == 'GET':
        return render_template('product/product_search.html')
    else:
        c = db.cursor()
        c.execute("""
            SELECT * FROM product
            WHERE PID=? """, (
            product_id)
            , )
        item = c.fetchone()

        # check if item is a laptop
        c = db.cursor()
        c.execute("""
            SELECT * FROM laptop
            WHERE PID=? """, (
            product_id)
            , )
        itemlp = c.fetchone()

        # check if item is a printer
        c = db.cursor()
        c.execute("""
                  SELECT * FROM printer
                  WHERE PID=? """, (
            product_id)
                  , )
        itempr = c.fetchone()

        # check if item is a computer
        c = db.cursor()
        c.execute("""
                  SELECT * FROM computer
                  WHERE PID=? """, (
            product_id)
                  , )

        itemcmp = c.fetchone()
        c.close()
        # depending on type of product, return different template
        if itemlp:
            return render_template('product/product_results.html', prodccl=itemlp, prodc=item)
        elif itemcmp:
            render_template('product/product_results.html', prodcc=itemcmp, prodc=item)
        elif itempr:
            render_template('product/product_results.html', prodcp=itempr, prodc=item)
        else:
            return render_template('product/product_results.html', prodc=item)
