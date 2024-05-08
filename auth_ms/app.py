from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from common.db import init_db, db
from common.utils import *
from common.jwt_tokens import generate_jwt_token, verify_jwt_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_jwt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ashudagar/projects/ecommerce-microservice/ms_arch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
init_db(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    username = data['username']
    password = data['password']
    role = data.get('role', 'user')  # Default role is 'user'
    hashed_password = generate_password_hash(password)

    user = User(username=username, password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    # Validate user credentials and generate JWT token
    user_id = authenticate(request.json['username'], request.json['password'])
    if user_id:
        jwt_token = generate_jwt_token(user_id.username)
        return jsonify({'token': jwt_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/users', methods=['GET'])
def get_users():
    token = request.headers.get('Authorization')
    if token:
        token = token.split()[1]  # Extract token from Authorization header
        payload = verify_jwt_token(token)
        if payload:
            users = User.query.all()
            result = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
            return jsonify(result)
        else:
            return jsonify({'message': 'Invalid or expired token'}), 401
    else:
        return jsonify({'message': 'Missing token'}), 401


if __name__ == '__main__':
    app.run(debug=True)
