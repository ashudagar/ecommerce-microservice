from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from common.db import init_db, db
from common.utils import *
from common.models import Order
from common.jwt_tokens import verify_jwt_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_jwt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ashudagar/projects/ecommerce-microservice/ms_arch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
init_db(app)


@app.route('/orders', methods=['GET'])
def get_orders():
    token = request.headers.get('Authorization')
    if token:
        token = token.split()[1]  # Extract token from Authorization header
        payload = verify_jwt_token(token)
        if payload:
            user_id = User.query.filter_by(username=payload.get('user_id')).first()
            orders = Order.query.filter_by(user_id=user_id.id).all()
            result = [{'id': order.id, 'user_id': order.user_id, 'product_id': order.product_id, 'quantity': order.quantity} for
                      order in orders]
        else:
            return jsonify({'message': 'Invalid or expired token'}), 401
    else:
        return jsonify({'message': 'Missing token'}), 401
    return jsonify(result)


@app.route('/orders', methods=['POST'])
def create_order():
    token = request.headers.get('Authorization')
    if token:
        token = token.split()[1]  # Extract token from Authorization header
        payload = verify_jwt_token(token)
        if payload:
            user_id = User.query.filter_by(username=payload.get('user_id')).first()
            print(user_id)

            new_order = Order(user_id=user_id.id, product_id=request.json.get('product_id'), quantity=request.json.get('quantity'))
            db.session.add(new_order)
            db.session.commit()

            return jsonify({'message': 'Order created successfully'}), 201
        else:
            return jsonify({'message': 'Invalid or expired token'}), 401
    else:
        return jsonify({'message': 'Missing token'}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5001)
