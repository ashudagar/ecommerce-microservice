import jwt
from datetime import datetime, timedelta

# Secret key for JWT signing (keep it secret and secure)
SECRET_KEY = 'test123'


def generate_jwt_token(user_id):
    # Define payload for JWT token (you can include additional claims)
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }
    # Generate JWT token
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jwt_token


def verify_jwt_token(token):
    try:
        # Decode and verify JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload  # Return decoded payload if token is valid
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None
