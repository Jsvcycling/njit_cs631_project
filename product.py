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
    # return list of all products. if user wants more info on product, search specific product id in next method
    if request.method == 'GET':
        return render_template('product/product_search.html')
    else:
        c = db.cursor()
        c.execute("""
            SELECT * FROM product
            """, )
        items = c.fetchall()
        c.close()

        return render_template('product/product_results.html', prodc=items)




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
