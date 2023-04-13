from flask import Flask, jsonify, request
import redis
import time
app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Switch to database 1
redis_client.select(1)

# Perform Redis commands on database 1


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
def delete():
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
    c = delete()
    d = edit()
    z = [a,b,c,d]
    print(z)
    return z

if __name__ == '__main__':
    app.run()