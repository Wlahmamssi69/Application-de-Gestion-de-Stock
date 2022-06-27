import sqlite3


def create_db():
    con = sqlite3.connect(r'system.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, email text, gender text, contact text, dob text, doj text, password text, type text, address text, salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT, name text, contact text, desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(id INTEGER PRIMARY KEY AUTOINCREMENT, name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY AUTOINCREMENT, category text, supplier text, name text, price text, qty text, status text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS sales(invoice INTEGER PRIMARY KEY AUTOINCREMENT, cl_name text, cl_contact text , date text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS line_sale(invoice INTEGER, product_id INTEGER , price text, qty Text, PRIMARY KEY (invoice, product_id), FOREIGN KEY (invoice) REFERENCES sales(invoice), FOREIGN KEY (product_id) REFERENCES product(id))")
    con.commit()



create_db()
