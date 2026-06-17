

import mysql.connector
from sql_connection import get_sql_connection
cnx = get_sql_connection()


def get_all_products(cnx):
    cursor = cnx.cursor()
    query = (
        "SELECT products.product_id, products.name, uom.uom_name, products.price_per_unit "
        "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id"
    )
    cursor.execute(query)

    response = []

    for (product_id, name, uom_name, price_per_unit) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'unit_name': uom_name,
            'price_per_unit': float(price_per_unit)
        })
    cursor.close()
    return response



def insert_new_products(cnx, products):
    cursor = cnx.cursor()
    query = ("insert into products"
             "(name, uom_id, price_per_unit)" 
              "values (%s, %s, %s)")
    data = (products['product_name'], products['uom_id'], products['price_per_unit'])
    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid

def delete_products(cnx, products_id):
    cursor = cnx.cursor()
    query = ("delete from products where product_id = %s")
    cursor.execute(query, (products_id,))
    cnx.commit()
    cursor.close()

def get_order_details(cnx, order_id):
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.name, od.quantity, od.total_price
        FROM order_details od
        JOIN products p ON od.product_id = p.product_id
        WHERE od.order_id = %s
    """, (order_id,))
    return cursor.fetchall()

def update_product(cnx, product_id, name, price, unit_id):
    cursor = cnx.cursor()
    cursor.execute(
        "UPDATE products SET name=%s, price_per_unit=%s, uom_id=%s WHERE product_id=%s",
        (name, price, unit_id, product_id)
    )
    cnx.commit()

def delete_order(cnx, order_id):
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM order_details WHERE order_id=%s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
    cnx.commit()

if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='grocery_store')

    cnx.close()