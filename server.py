from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import products_dao
import mysql.connector

app = Flask(__name__)
CORS(app)

import os

cnx = mysql.connector.connect(
    host=os.environ.get('mysql.railway.internal'),
    user=os.environ.get('root'),
    password=os.environ.get('eNxmNedoxXRGRDxAtdkoRJdvGZdbCwbo'),
    database=os.environ.get('railway'),
    port=int(os.environ.get('3306', 3306))
)

@app.route('/get_products', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(cnx)
    response = jsonify(products)
    return response

@app.route('/manage_products')
def manage_products():
    return render_template('manage_product.html')

@app.route('/delete_products', methods=['POST'])
def delete_products():
    products_ids = request.form.get('products_id')
    return_id = products_dao.delete_products(cnx, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insert_product', methods=['POST'])
def insert_product():
    product = {
        'product_name': request.form.get('product_name'),
        'uom_id': request.form.get('uom_id'),
        'price_per_unit': request.form.get('price_per_unit')
    }
    return_id = products_dao.insert_new_products(cnx, product)
    return jsonify({'product_id': return_id})

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/insert_order', methods=['POST'])
def insert_order():
    from datetime import datetime
    import json
    data = request.get_json()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO orders (customer_id, total, datetime) VALUES (%s, %s, %s)",
        (data['customer_name'], data['total'], datetime.now())
    )
    order_id = cursor.lastrowid
    for item in data['order_details']:
        cursor.execute(
            "INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
            (order_id, item['product_id'], item['quantity'], item['total_price'])
        )
    cnx.commit()
    cursor.close()
    return jsonify({'order_id': order_id})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_orders')
def get_orders():
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    return jsonify(orders)

@app.route('/get_order_details/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    details = products_dao.get_order_details(cnx, order_id)
    return jsonify(details)

@app.route('/update_product', methods=['POST'])
def update_product():
    data = request.get_json()
    products_dao.update_product(
        cnx,
        data['product_id'],
        data['name'],
        data['price_per_unit'],
        data['uom_id']
    )
    return jsonify({'message': 'Product updated successfully'})

@app.route('/delete_order', methods=['POST'])
def delete_order():
    data = request.get_json()
    products_dao.delete_order(cnx, data['order_id'])
    return jsonify({'message': 'Order deleted'})

if __name__ == '__main__':
    print("Starting Python Flask Server For Grocery Store")
    app.run(port=5000, debug=True)