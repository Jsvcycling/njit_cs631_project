#!/usr/bin/env python3

"""This file contains the server code for the CS 631 final project.

Authors:
 - Manuel Aguas <maa995@njit.edu>
 - Jason Grant <jg492@njit.edu>
 - Joshua S. Vega <jsv28@njit.edu>

"""

import os
import sqlite3

from flask import Flask, request, session, g, redirect, flash

from customer import customer_bp
from product  import product_bp
from statistics import statistics_bp

# The Flask app.
app = Flask(__name__)

# App configuration
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'cs631.db')
))

db_connect()

# Register the blueprints.
app.register_blueprint(customer_bp)
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(statistics_bp, url_prefix='/statistics')

def db_connect():
    exists = False
    
    if os.path.join(app.config['DATABASE']):
        exists = True

    g.db = sqlite3.connect(app.config['DATABASE'])
    g.db.row_factory = sqlite3.Row

    if not exists:
        with app.open_resource('create_tables.sql', mode='r') as f:
            g.db.cursor().executescript(f.read())

        g.db.commit()

        with app.open_resource('populate_tables.sql', mode='r') as f:
            g.db.cursor().executescript(f.read())

        g.db.commit()

@app.teardown_appcontext
def close_db():
    if hasattr(g, 'db'):
        g.db.close()
