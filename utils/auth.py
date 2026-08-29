import jwt
import datetime
import bcrypt
from functools import wraps
from flask import request, jsonify
from config import Config

def generate_jwt(payload_data, expires_in_hours=24):
    payload = payload_data.copy()
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_in_hours)
    payload['iat'] = datetime.datetime.utcnow()
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            token = request.cookies.get('access_token')

        if not token:
            return jsonify({'error': 'Authentication token missing', 'code': 'UNAUTHORIZED'}), 401

        payload = decode_jwt(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token', 'code': 'INVALID_TOKEN'}), 401

        request.user = payload
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            token = request.cookies.get('access_token')

        if not token:
            return jsonify({'error': 'Admin token missing', 'code': 'UNAUTHORIZED'}), 401

        payload = decode_jwt(token)
        if not payload or payload.get('role') != 'admin':
            return jsonify({'error': 'Admin access required', 'code': 'FORBIDDEN'}), 403

        request.user = payload
        return f(*args, **kwargs)
    return decorated
