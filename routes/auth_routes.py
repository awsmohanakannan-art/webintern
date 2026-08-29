import uuid
from flask import Blueprint, request, jsonify, make_response
from database import query_db, execute_db
from utils.otp import create_and_store_otp, verify_otp_code
from utils.auth import generate_jwt, check_password, jwt_required
from utils.email_service import send_otp_email

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/auth/register/request-otp', methods=['POST'])
def register_request_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    terms_accepted = data.get('terms_accepted', False)

    if not email or not full_name:
        return jsonify({'error': 'Full name and email address are required.'}), 400

    if not terms_accepted:
        return jsonify({'error': 'You must agree to the Terms & Conditions and Privacy Policy.'}), 400

    code = create_and_store_otp(email, purpose='register')
    send_otp_email(email, code, purpose='registration')

    return jsonify({
        'message': 'Verification code sent to your email address.',
        'email': email,
        'dev_otp': code # Output for frictionless local testing
    }), 200

@auth_bp.route('/api/auth/register/verify-otp', methods=['POST'])
def register_verify_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()
    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    phone_country_code = data.get('phone_country_code', '+91')
    marketing_opt_in = data.get('marketing_opt_in', False)

    if not email or not code:
        return jsonify({'error': 'Email and verification code are required.'}), 400

    valid, msg = verify_otp_code(email, code, purpose='register')
    if not valid:
        return jsonify({'error': msg}), 400

    # Check if user profile already exists
    existing = query_db("SELECT * FROM profiles WHERE email = ?", (email,), one=True)
    if existing:
        user_id = existing['id']
    else:
        user_id = str(uuid.uuid4())
        execute_db(
            "INSERT INTO profiles (id, full_name, email, phone, phone_country_code, marketing_opt_in) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, full_name or email.split('@')[0], email, phone, phone_country_code, 1 if marketing_opt_in else 0)
        )

    token = generate_jwt({
        'sub': user_id,
        'email': email,
        'name': full_name or email.split('@')[0],
        'role': 'student'
    })

    resp = make_response(jsonify({
        'message': 'Registration successful.',
        'token': token,
        'user': {
            'id': user_id,
            'email': email,
            'full_name': full_name,
            'role': 'student'
        }
    }))
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
    return resp, 200

@auth_bp.route('/api/auth/login/request-otp', methods=['POST'])
def login_request_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email address is required.'}), 400

    code = create_and_store_otp(email, purpose='login')
    send_otp_email(email, code, purpose='login')

    return jsonify({
        'message': 'Verification code sent to your email address.',
        'email': email,
        'dev_otp': code
    }), 200

@auth_bp.route('/api/auth/login/verify-otp', methods=['POST'])
def login_verify_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()

    if not email or not code:
        return jsonify({'error': 'Email and verification code are required.'}), 400

    valid, msg = verify_otp_code(email, code, purpose='login')
    if not valid:
        return jsonify({'error': msg}), 400

    profile = query_db("SELECT * FROM profiles WHERE email = ?", (email,), one=True)
    if not profile:
        user_id = str(uuid.uuid4())
        full_name = email.split('@')[0].capitalize()
        execute_db(
            "INSERT INTO profiles (id, full_name, email) VALUES (?, ?, ?)",
            (user_id, full_name, email)
        )
        profile = {'id': user_id, 'full_name': full_name, 'email': email}

    token = generate_jwt({
        'sub': profile['id'],
        'email': profile['email'],
        'name': profile['full_name'],
        'role': 'student'
    })

    resp = make_response(jsonify({
        'message': 'Login successful.',
        'token': token,
        'user': {
            'id': profile['id'],
            'email': profile['email'],
            'full_name': profile['full_name'],
            'role': 'student'
        }
    }))
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
    return resp, 200

@auth_bp.route('/api/auth/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    admin = query_db("SELECT * FROM admins WHERE email = ?", (email,), one=True)
    if not admin or not check_password(password, admin['password_hash']):
        return jsonify({'error': 'Invalid administrator credentials.'}), 401

    token = generate_jwt({
        'sub': admin['id'],
        'email': admin['email'],
        'name': admin['full_name'],
        'role': 'admin'
    })

    resp = make_response(jsonify({
        'message': 'Admin authentication successful.',
        'token': token,
        'user': {
            'id': admin['id'],
            'email': admin['email'],
            'full_name': admin['full_name'],
            'role': 'admin'
        }
    }))
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
    return resp, 200

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required
def get_current_user():
    user_payload = request.user
    if user_payload.get('role') == 'admin':
        admin = query_db("SELECT id, email, full_name, created_at FROM admins WHERE id = ?", (user_payload['sub'],), one=True)
        if admin:
            admin['role'] = 'admin'
            return jsonify({'user': admin}), 200
    else:
        profile = query_db("SELECT id, full_name, email, phone, phone_country_code, college, avatar_url, created_at FROM profiles WHERE id = ?", (user_payload['sub'],), one=True)
        if profile:
            profile['role'] = 'student'
            return jsonify({'user': profile}), 200

    return jsonify({'error': 'User not found.'}), 404
