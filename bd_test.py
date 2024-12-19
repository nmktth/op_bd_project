import sqlite3
sqlite3.connect('db.sqlite3').cursor().execute("""
    UPDATE products_product SET cur_percent = 12 WHERE price = 799
""").connection.commit()
