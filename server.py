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

with app.app_context():
    # App configuration
    app.config.from_object(__name__)

    app.secret_key = 'hello-world'

    # Register the blueprints.
    app.register_blueprint(customer_bp)
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(statistics_bp, url_prefix='/statistics')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
