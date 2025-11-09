import sqlite3


def create_database():
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 1 NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                category TEXT NOT NULL,
                item TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        con.commit()

    print("Database and tables: customers and products created successfully (or already exist)")


def customers_insert_one(name: str, phone: str, email: str = "none@none.none"):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        if name is None:
            print("name must NOT be None!")
            return
        if phone is None:
            print("phone must NOT be None!")
            return

        cur.execute("INSERT INTO customers (name, phone, email) VALUES(?, ?, ?)", (name, phone, email))
        con.commit()


def customers_insert_many(customer_list: list[tuple[str, str, str]]):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        for i, (name, phone, email) in enumerate(customer_list):
            if name is None:
                print(f"{i}: name must NOT be None!")
                return
            if phone is None:
                print(f"{i}: phone must NOT be None!")
                return

        cur.executemany("INSERT INTO customers (name, phone, email) VALUES(?, ?, ?)", customer_list)
        con.commit()


def customers_get_one(customer_id: int):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        return cur.fetchone()


def customers_get_many(where_clause: str = None, params: tuple = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        if where_clause:
            query = f"SELECT * FROM customers WHERE {where_clause}"
            cur.execute(query, params if params else ())
        else:
            cur.execute("SELECT * FROM customers")
        return cur.fetchall()


def customers_update_one(customer_id: int, name: str = None, phone: str = None, email: str = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if phone is not None:
            updates.append("phone = ?")
            params.append(phone)
        if email is not None:
            updates.append("email = ?")
            params.append(email)

        if not updates:
            print("No fields to update!")
            return

        params.append(customer_id)
        query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = ?"
        cur.execute(query, params)
        con.commit()


def customers_update_many(where_clause: str, params: tuple, name: str = None, phone: str = None, email: str = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        updates = []
        update_params = []

        if name is not None:
            updates.append("name = ?")
            update_params.append(name)
        if phone is not None:
            updates.append("phone = ?")
            update_params.append(phone)
        if email is not None:
            updates.append("email = ?")
            update_params.append(email)

        if not updates:
            print("No fields to update!")
            return

        query = f"UPDATE customers SET {', '.join(updates)} WHERE {where_clause}"
        cur.execute(query, update_params + list(params))
        con.commit()


def customers_delete_one(customer_id: int):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        con.commit()


def customers_delete_many(where_clause: str, params: tuple):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        query = f"DELETE FROM customers WHERE {where_clause}"
        cur.execute(query, params)
        con.commit()


def products_insert_one(name: str, price: float, stock_quantity: int = 1, latitude: float = None, longitude: float = None, category: str = None, item: str = None, description: str = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        if name is None:
            print("name must NOT be None!")
            return
        if price is None:
            print("price must NOT be None!")
            return
        if latitude is None:
            print("latitude must NOT be None!")
            return
        if longitude is None:
            print("longitude must NOT be None!")
            return
        if category is None:
            print("category must NOT be None!")
            return
        if item is None:
            print("item must NOT be None!")
            return

        cur.execute("INSERT INTO products (name, price, stock_quantity, latitude, longitude, category, item, description) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (name, price, stock_quantity, latitude, longitude, category, item, description))
        con.commit()


def products_insert_many(product_list: list[tuple[str, float, int, float, float, str, str, str]]):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        for i, (name, price, stock_quantity, latitude, longitude, category, item, description) in enumerate(product_list):
            if name is None:
                print(f"{i}: name must NOT be None!")
                return
            if price is None:
                print(f"{i}: price must NOT be None!")
                return
            if latitude is None:
                print(f"{i}: latitude must NOT be None!")
                return
            if longitude is None:
                print(f"{i}: longitude must NOT be None!")
                return
            if category is None:
                print(f"{i}: category must NOT be None!")
                return
            if item is None:
                print(f"{i}: item must NOT be None!")
                return

        cur.executemany("INSERT INTO products (name, price, stock_quantity, latitude, longitude, category, item, description) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", product_list)
        con.commit()


def products_get_one(product_id: int):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        return cur.fetchone()


def products_get_many(where_clause: str = None, params: tuple = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        if where_clause:
            query = f"SELECT * FROM products WHERE {where_clause}"
            cur.execute(query, params if params else ())
        else:
            cur.execute("SELECT * FROM products")
        return cur.fetchall()


def products_update_one(product_id: int, name: str = None, price: float = None, stock_quantity: int = None, latitude: float = None, longitude: float = None, category: str = None, item: str = None, description: str = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if price is not None:
            updates.append("price = ?")
            params.append(price)
        if stock_quantity is not None:
            updates.append("stock_quantity = ?")
            params.append(stock_quantity)
        if latitude is not None:
            updates.append("latitude = ?")
            params.append(latitude)
        if longitude is not None:
            updates.append("longitude = ?")
            params.append(longitude)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if item is not None:
            updates.append("item = ?")
            params.append(item)
        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if not updates:
            print("No fields to update!")
            return

        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE product_id = ?"
        cur.execute(query, params)
        con.commit()


def products_update_many(where_clause: str, params: tuple, name: str = None, price: float = None, stock_quantity: int = None, latitude: float = None, longitude: float = None, category: str = None, item: str = None, description: str = None):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()

        updates = []
        update_params = []

        if name is not None:
            updates.append("name = ?")
            update_params.append(name)
        if price is not None:
            updates.append("price = ?")
            update_params.append(price)
        if stock_quantity is not None:
            updates.append("stock_quantity = ?")
            update_params.append(stock_quantity)
        if latitude is not None:
            updates.append("latitude = ?")
            update_params.append(latitude)
        if longitude is not None:
            updates.append("longitude = ?")
            update_params.append(longitude)
        if category is not None:
            updates.append("category = ?")
            update_params.append(category)
        if item is not None:
            updates.append("item = ?")
            update_params.append(item)
        if description is not None:
            updates.append("description = ?")
            update_params.append(description)

        if not updates:
            print("No fields to update!")
            return

        query = f"UPDATE products SET {', '.join(updates)} WHERE {where_clause}"
        cur.execute(query, update_params + list(params))
        con.commit()


def products_delete_one(product_id: int):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        con.commit()


def products_delete_many(where_clause: str, params: tuple):
    with sqlite3.connect("store.db") as con:
        cur = con.cursor()
        query = f"DELETE FROM products WHERE {where_clause}"
        cur.execute(query, params)
        con.commit()