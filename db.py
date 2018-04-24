import os
import sqlite3

db = None
db_path = 'cs631.db'
exists = False

if os.path.exists(db_path):
    exists = True
    
db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row

if not exists:
    with open('create_tables.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

    with open('populate_tables.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()


