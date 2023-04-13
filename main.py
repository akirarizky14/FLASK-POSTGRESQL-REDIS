from flask import Flask,request, url_for, redirect,render_template,jsonify
from psycopg2 import pool
import time
import redis
app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.select(1)


class PgPool:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(
            1, 100,
            database="shop",
            user="postgres",
            password="admin",
            host="localhost",)
    def get_connection(self):
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        return self.connection_pool.putconn(connection)

    def close_all_connections(self):
        return self.connection_pool.closeall()
pg_pool = PgPool()

@app.route('/')
def categories():
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_date, total_amount FROM orders")
    data = cur.fetchall()
    cur.close()
    conn.close()
    labels = [row[0].strftime('%Y-%m-%d') for row in data]
    values = [row[1] for row in data]

    return render_template('index.html', data =data,labels=labels, values=values)


# REDIS
def read():
    start_time = time.time()
    redis_client.set('key', 'value')
    value = redis_client.get('key')
    end_time = time.time()  # Akhir waktu eksekusi query
    timee = [end_time - start_time]
    print(timee)
    return timee
def create():
    start_time = time.time()
    redis_client.set('key', 'value')
    end_time = time.time()  # Akhir waktu eksekusi query
    timee = [end_time - start_time]
    print(timee)
    return timee
def delete_redis():
    start_time = time.time()
    redis_client.delete('key')
    end_time = time.time()  # Akhir waktu eksekusi query
    timee = [end_time - start_time]
    print(timee)
    return timee

def edit():
    start_time = time.time()
    redis_client.set('key', 'new_value')
    end_time = time.time()  # Akhir waktu eksekusi query
    timee = [end_time - start_time]
    print(timee)
    return timee

@app.route('/read', methods=['GET'])
def show():
    a = read()
    b = create()
    c = delete_redis()
    d = edit()
    z = [a,b,c,d]
    print(z)
    return z

# Bar chart

def execute_query_get():
    start_time = time.time()
    query = "SELECT * FROM product"
    conn = pg_pool.get_connection()
      # Memulai waktu eksekusi query
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    end_time = time.time()
    # Akhir waktu eksekusi query
    timee = [end_time - start_time]
    return (timee)  # Menampilkan waktu eksekusi query

def execute_query_Insert():
    start_time = time.time()
    query_post = "INSERT INTO product (code, name, category, price ,discount) VALUES ('0001', 'Iphone', 'Mobile', 1000,100)"
    conn = pg_pool.get_connection()
      # Memulai waktu eksekusi query
    cur = conn.cursor()
    cur.execute(query_post)
    conn.commit()
    end_time = time.time()
    timeea = [end_time - start_time]# Akhir waktu eksekusi query
    return (timeea)  # Menampilkan waktu eksekusi query

def execute_query_Delete():
    start_time = time.time()
    query_delete = "DELETE FROM product WHERE code = '0001'"
    conn = pg_pool.get_connection()
      # Memulai waktu eksekusi query
    cur = conn.cursor()
    cur.execute(query_delete)
    conn.commit()
    end_time = time.time()
    timee = [end_time - start_time]# Akhir waktu eksekusi query
    return (timee)  # Menampilkan waktu eksekusi query


def execute_query_put():
    start_time = time.time()
    query_put = "UPDATE product SET code = '0029' , name = 'Changed' WHERE code = '0029'"
    conn = pg_pool.get_connection()
      # Memulai waktu eksekusi query
    cur = conn.cursor()
    cur.execute(query_put)
    conn.commit()
    end_time = time.time()  # Akhir waktu eksekusi query
    timee = [end_time - start_time]
    return (timee)  # Menampilkan waktu eksekusi query

@app.route('/BarChart')
def execute_query_getall():
    conn = pg_pool.get_connection()
    a = execute_query_Insert()
    b = execute_query_Delete()
    c = execute_query_put()
    d = execute_query_get()
    apa = [a,b,c,d]
    print('Ini a ',a)
    print('Ini b', b)
    print('Ini c', c)
    print('Ini d', d)
    redis = show()
    # print(apa)
    conn.close()
    return render_template('chart.html',data = apa, data_redis = redis)  # Menampilkan waktu eksekusi query

# PRODUCTS
@app.get("/products")
def get():
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        data = cur.fetchall()
        cur.close()
        conn.close()
        pg_pool.return_connection(conn)
        return data

@app.route("/products",methods=['POST'])
def post():
        data = request.get_json()
        code = data['code']
        name = data['name']
        category = data['category']
        price = int(data['price'])
        discount = int(data['discount'])
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO product (code, name, category, price ,discount)'
                    'VALUES (%s, %s, %s, %s,%s)',
                    (code, name, category, price ,discount))
        # cur.execute("SELECT * FROM product")
        conn.commit()
        cur.close()
        conn.close()
        pg_pool.return_connection(conn)
        return jsonify(message="Product created successfully"), 201
@app.route("/products/<int:pid>",methods=['DELETE'])
def delete(pid):
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM product WHERE pid = %s", (pid,))
        conn.commit()
        cur.close()
        pg_pool.return_connection(conn)
        return jsonify(message="products deleted successfully")
@app.route("/products/<int:pid>",methods=['PUT'])
def put(pid):
        data = request.get_json()
        code = data['code']
        name = data['name']
        category = data['category']
        price = int(data['price'])
        discount = int(data['discount'])
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE product SET code = %s , name = %s, category = %s, price = %s ,discount = %s WHERE pid = %s',
                    (code, name, category, price, discount, pid))
        conn.commit()
        cur.close()
        pg_pool.return_connection(conn)
        return jsonify(message="product updated successfully")
# USERS
@app.get("/users")
def get_users():
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    data_users = cur.fetchall()
    cur.close()
    conn.close()
    pg_pool.return_connection(conn)
    return data_users
@app.route("/users",methods=['POST'])
def post_users():
        data_users = request.get_json()
        username = data_users['username']
        password = data_users['password']
        email = data_users['email']
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password, email)'
                    'VALUES (%s, %s, %s)',
                    (username, password, email))
        conn.commit()
        cur.close()
        conn.close()
        pg_pool.return_connection(conn)
        return jsonify(message="Users created successfully"), 201
@app.route("/users/<int:id>",methods=['DELETE'])
def delete_users(id):
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    pg_pool.return_connection(conn)
    return jsonify(message="Users deleted successfully")
@app.route("/users/<int:id>",methods=['PUT'])
def put_users(id):
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = %s , password = %s, email = %s WHERE id = %s',
                (username, password, email, id))
    conn.commit()
    cur.close()
    pg_pool.return_connection(conn)
    return jsonify(message="users updated successfully")

# ORDERS
@app.get("/orders")
def get_orders():
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    data_users = cur.fetchall()
    cur.close()
    conn.close()
    pg_pool.return_connection(conn)
    return data_users
@app.route("/orders",methods=['POST'])
def orders_users():
        data_orders = request.get_json()
        customer_id = int(data_orders['customer_id'])
        order_date = data_orders['order_date']
        total_amount = int(data_orders['total_amount'])
        status = data_orders['status']
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO orders (customer_id, order_date, total_amount, status)'
                    'VALUES (%s, %s, %s, %s)',
                    (customer_id, order_date, total_amount, status))
        conn.commit()
        cur.close()
        conn.close()
        pg_pool.return_connection(conn)
        return jsonify(message="Orders created successfully"), 201
@app.route("/orders/<int:id>",methods=['DELETE'])
def orders_delete(id):
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    pg_pool.return_connection(conn)
    return jsonify(message="orders deleted successfully")
@app.route("/orders/<int:id>",methods=['PUT'])
def put_orders(id):
    data_orders = request.get_json()
    customer_id = int(data_orders['customer_id'])
    order_date = data_orders['order_date']
    total_amount = int(data_orders['total_amount'])
    status = data_orders['status']
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE orders SET customer_id = %s , order_date = %s, total_amount = %s , status = %s  WHERE id = %s',
                (customer_id, order_date, total_amount, status,id))
    conn.commit()
    cur.close()
    pg_pool.return_connection(conn)
    return jsonify(message="orders updated successfully")
# Basket
@app.get("/baskets")
def get_baskets():
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket")
    data_users = cur.fetchall()
    cur.close()
    conn.close()
    return data_users
@app.route("/baskets",methods=['POST'])
def basket_users():
        data_orders = request.get_json()
        item_name = data_orders['item_name']
        quantity = data_orders['quantity']
        conn = pg_pool.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO basket (item_name, quantity)'
                    'VALUES (%s, %s)',
                    (item_name, quantity))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message="Basket created successfully"), 201
@app.route("/baskets/<int:id>",methods=['DELETE'])
def basket_delete(id):
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM basket WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    return jsonify(message="basket deleted successfully")
@app.route("/baskets/<int:id>",methods=['PUT'])
def put_baskets(id):
    data_orders = request.get_json()
    item_name = data_orders['item_name']
    quantity = data_orders['quantity']
    conn = pg_pool.get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE basket SET item_name = %s , quantity = %s',
                (item_name, quantity))
    conn.commit()
    cur.close()
    return jsonify(message="baskets updated successfully")

def close_db_connection(exception):
    pg_pool.close_all_connections()

if __name__ == '__main__':
    app.run(debug=True)