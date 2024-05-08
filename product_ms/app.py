from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from common.db import init_db, db
from common.utils import *
from common.models import Product
from common.jwt_tokens import verify_jwt_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_jwt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ashudagar/projects/ecommerce-microservice/ms_arch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)


@app.route('/products', methods=['GET'])
def get_products():
    token = request.headers.get('Authorization')
    if token:
        token = token.split()[1]  # Extract token from Authorization header
        payload = verify_jwt_token(token)
        if payload:
            products = Product.query.all()
            result = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
            return jsonify(result)
        else:
            return jsonify({'message': 'Invalid or expired token'}), 401
    else:
        return jsonify({'message': 'Missing token'}), 401


@app.route('/products', methods=['POST'])
def create_product():
    token = request.headers.get('Authorization')
    if token:
        token = token.split()[1]  # Extract token from Authorization header
        payload = verify_jwt_token(token)
        if payload:
            new_product = Product(name=request.json.get('name'), price=request.json.get('price'))
            db.session.add(new_product)
            db.session.commit()

            return jsonify({'message': 'Product created successfully'}), 201
        else:
            return jsonify({'message': 'Invalid or expired token'}), 401
    else:
        return jsonify({'message': 'Missing token'}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5002)
