# Import all the necessity libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init the app
app = Flask(__name__)

# Getting Base directory to store the DB
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init the DB and Masrshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=True)
    qty = db.Column(db.Integer, nullable=True)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a POST request for adding products
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Create a GET request to fetch all the products
@app.route('/product', methods=['GET'])
def fetch_all_product():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Create a GET request to fetch specific product using id
@app.route('/product/<id>', methods=['GET'])
def get_single_product(id):
    single_product = Product.query.get(id)
    return product_schema.jsonify(single_product)

# Create a PUT request to update the product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product_to_update = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product_to_update.name = name
    product_to_update.description = description
    product_to_update.price = price
    product_to_update.qty = qty

    db.session.commit()

    return product_schema.jsonify(product_to_update)

# Create a DELETE request for deleting the product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    del_product = Product.query.get(id)
    db.session.delete(del_product)
    db.session.commit()

    return product_schema.jsonify(del_product)

# Run the Server
if __name__ == '__main__':
    app.run(debug=True)
