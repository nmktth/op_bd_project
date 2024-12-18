import sqlite3
sqlite3.connect('db.sqlite3').cursor().execute("""
    CREATE TABLE products_product (
        url TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL DEFAULT 0.00 NOT NULL,
        start_price REAL DEFAULT 0.00 NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    )
""").connection.commit()