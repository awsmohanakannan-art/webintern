import uuid
from flask import Blueprint, request, jsonify, make_response
from database import query_db, execute_db
from utils.auth import generate_jwt, check_password, jwt_required
from config import Config
from supabase import create_client

auth_bp = Blueprint('auth_bp', __name__)

DEFAULT_SUPABASE_URL = "https://fzmdeigwxiesegvtuafk.supabase.co"
DEFAULT_SUPABASE_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ6bWRlaWd3eGllc2VndnR1YWZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg0MjA2NDAsImV4cCI6MjEwMzk5NjY0MH0.aqk90jQu4yBCgc0wi9zA0cMHf5XZ31OPVc3hcED0_J8"
DEFAULT_SUPABASE_SERVICE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ6bWRlaWd3eGllc2VndnR1YWZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4ODQyMDY0MCwiZXhwIjoyMTAzOTk2NjQwfQ.osKcbobbZPLz7RpO0zVgyHbIPJC2l6QDF6MBQ-W0uTA"

def get_supabase_admin():
    url = (Config.SUPABASE_URL or DEFAULT_SUPABASE_URL).strip()
    key = (Config.SUPABASE_SERVICE_ROLE_KEY or DEFAULT_SUPABASE_SERVICE).strip()
    return create_client(url, key)

def get_supabase_anon():
    url = (Config.SUPABASE_URL or DEFAULT_SUPABASE_URL).strip()
    key = (Config.SUPABASE_ANON_KEY or DEFAULT_SUPABASE_ANON).strip()
    return create_client(url, key)

@auth_bp.route('/api/auth/config', methods=['GET'])
def get_auth_config():
    """Return public Supabase configuration for frontend initialization."""
    return jsonify({
        'supabase_url': Config.SUPABASE_URL or DEFAULT_SUPABASE_URL,
        'supabase_anon_key': Config.SUPABASE_ANON_KEY or DEFAULT_SUPABASE_ANON,
        'google_client_id': Config.GOOGLE_CLIENT_ID or "1013835320701-p74mrb7a14tjng226elmppqgko9mldvi.apps.googleusercontent.com"
    }), 200

def sync_profile_to_local_db(user_id, full_name, email, phone="", phone_country_code="+91", marketing_opt_in=False):
    """Sync profile record to SQLite database for compatibility with existing routes."""
    try:
        existing = query_db("SELECT id FROM profiles WHERE id = ? OR email = ?", (user_id, email), one=True)
        if existing:
            execute_db(
                "UPDATE profiles SET full_name = ?, email = ?, phone = ?, phone_country_code = ?, marketing_opt_in = ? WHERE id = ?",
                (full_name, email, phone, phone_country_code, 1 if marketing_opt_in else 0, existing['id'])
            )
        else:
            execute_db(
                "INSERT INTO profiles (id, full_name, email, phone, phone_country_code, marketing_opt_in) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, full_name, email, phone, phone_country_code, 1 if marketing_opt_in else 0)
            )
    except Exception as e:
        print(f"[SQLite Sync Warning]: {e}")

def safe_upsert_profile(supabase_admin, profile_dict):
    """Helper to safely upsert profiles even if certain columns differ in Postgres schema."""
    try:
        supabase_admin.table('profiles').upsert(profile_dict).execute()
    except Exception as e:
        err_str = str(e)
        if 'email' in err_str and 'column' in err_str:
            fallback_dict = {k: v for k, v in profile_dict.items() if k != 'email'}
            supabase_admin.table('profiles').upsert(fallback_dict).execute()
        else:
            print(f"[Profiles Upsert Warning]: {e}")

@auth_bp.route('/api/auth/register', methods=['POST'])
def register_user():
    """Register user with Supabase Auth and directly create activated profile."""
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip()
    phone_country_code = data.get('phone_country_code', '+91').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    terms_accepted = data.get('terms_accepted', False)
    marketing_opt_in = data.get('marketing_opt_in', False)

    # Validations
    if not full_name:
        return jsonify({'error': 'Full name is required.'}), 400
    if not email:
        return jsonify({'error': 'Email address is required.'}), 400
    if not password:
        return jsonify({'error': 'Password is required.'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400
    if confirm_password and password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400
    if not terms_accepted:
        return jsonify({'error': 'You must agree to the Terms & Conditions and Privacy Policy.'}), 400

    full_mobile = f"{phone_country_code} {phone}".strip() if phone else ""

    try:
        supabase_admin = get_supabase_admin()
        
        # 1. Create user in Supabase Auth
        res = supabase_admin.auth.admin.create_user({
            'email': email,
            'password': password,
            'email_confirm': True,
            'user_metadata': {'name': full_name}
        })

        if not res.user:
            return jsonify({'error': 'Failed to create account in Supabase Auth.'}), 400

        user_id = str(res.user.id)

        # 2. Insert into public.profiles in Supabase as completed/active
        profile_data = {
            'id': user_id,
            'name': full_name,
            'email': email,
            'mobile': full_mobile,
            'phone_verified': True,
            'auth_provider': 'email',
            'terms_accepted': True,
            'marketing_opt_in': marketing_opt_in,
            'profile_complete': True
        }
        
        safe_upsert_profile(supabase_admin, profile_data)
        sync_profile_to_local_db(user_id, full_name, email, phone, phone_country_code, marketing_opt_in)

        token = generate_jwt({
            'sub': user_id,
            'email': email,
            'name': full_name,
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Account created successfully!',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'mobile': full_mobile,
                'profile_complete': True,
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        err_msg = str(e)
        if any(term in err_msg.lower() for term in ['already registered', 'already exists', 'duplicate', 'user with this email', 'has already been registered']):
            return jsonify({'error': 'An account with this email address already exists. Please sign in instead.'}), 400
        return jsonify({'error': f'Registration failed: {err_msg}'}), 400

@auth_bp.route('/api/auth/login', methods=['POST'])
def login_user():
    """Login user with Email and Password using Supabase Auth."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email address and password are required.'}), 400

    try:
        supabase_anon = get_supabase_anon()
        supabase_admin = get_supabase_admin()

        # Sign in via Supabase Auth
        auth_res = supabase_anon.auth.sign_in_with_password({
            'email': email,
            'password': password
        })

        if not auth_res.user:
            return jsonify({'error': 'Invalid email or password.'}), 401

        user_id = str(auth_res.user.id)

        # Retrieve profile from Supabase profiles table by ID
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        
        profile = None
        if prof_res.data and len(prof_res.data) > 0:
            profile = prof_res.data[0]
        else:
            default_profile = {
                'id': user_id,
                'name': auth_res.user.user_metadata.get('name', email.split('@')[0]),
                'email': email,
                'mobile': '',
                'phone_verified': True,
                'auth_provider': 'email',
                'terms_accepted': True,
                'marketing_opt_in': False,
                'profile_complete': True
            }
            safe_upsert_profile(supabase_admin, default_profile)
            profile = default_profile
            sync_profile_to_local_db(user_id, profile['name'], email)

        token = generate_jwt({
            'sub': user_id,
            'email': email,
            'name': profile.get('name') or email.split('@')[0],
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Login successful.',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': profile.get('name') or email.split('@')[0],
                'mobile': profile.get('mobile', ''),
                'profile_complete': True,
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        err_msg = str(e)
        if 'invalid credentials' in err_msg.lower() or 'invalid login' in err_msg.lower() or 'invalid email' in err_msg.lower():
            return jsonify({'error': 'Invalid email or password.'}), 401
        return jsonify({'error': f'Authentication failed: {err_msg}'}), 400

@auth_bp.route('/api/auth/google-sync', methods=['POST'])
def sync_google_user():
    """Sync profile and handle provider linking for users logging in via Google OAuth."""
    data = request.get_json() or {}
    user_id = data.get('id')
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()

    if not user_id or not email:
        return jsonify({'error': 'User ID and email are required for Google auth sync.'}), 400

    try:
        supabase_admin = get_supabase_admin()
        
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        profile = prof_res.data[0] if (prof_res.data and len(prof_res.data) > 0) else None

        if not profile:
            new_profile = {
                'id': user_id,
                'name': name or email.split('@')[0],
                'email': email,
                'mobile': '',
                'phone_verified': True,
                'auth_provider': 'google',
                'terms_accepted': True,
                'marketing_opt_in': False,
                'profile_complete': True
            }
            safe_upsert_profile(supabase_admin, new_profile)
            profile = new_profile
            sync_profile_to_local_db(user_id, name or email.split('@')[0], email)
        else:
            if profile.get('auth_provider') == 'email':
                supabase_admin.table('profiles').update({'auth_provider': 'both'}).eq('id', user_id).execute()
                profile['auth_provider'] = 'both'

        token = generate_jwt({
            'sub': profile['id'],
            'email': email,
            'name': profile.get('name') or name or email.split('@')[0],
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Google authentication successful.',
            'token': token,
            'user': {
                'id': profile['id'],
                'email': email,
                'full_name': profile.get('name') or name or email.split('@')[0],
                'mobile': profile.get('mobile', ''),
                'profile_complete': True,
                'auth_provider': profile.get('auth_provider', 'google'),
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        return jsonify({'error': f'Failed to sync Google user: {str(e)}'}), 400

@auth_bp.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Trigger Supabase password reset email flow."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email address is required.'}), 400

    try:
        supabase_anon = get_supabase_anon()
        supabase_anon.auth.reset_password_for_email(email)

        return jsonify({
            'message': 'If an account exists with this email address, a password reset link has been sent.'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send password reset email: {str(e)}'}), 400

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
        try:
            supabase_admin = get_supabase_admin()
            prof_res = supabase_admin.table('profiles').select('*').eq('id', user_payload['sub']).execute()
            if prof_res.data and len(prof_res.data) > 0:
                p = prof_res.data[0]
                return jsonify({
                    'user': {
                        'id': p['id'],
                        'full_name': p.get('name') or user_payload.get('name'),
                        'email': user_payload.get('email'),
                        'mobile': p.get('mobile'),
                        'profile_complete': True,
                        'role': 'student'
                    }
                }), 200
        except Exception:
            pass

        profile = query_db("SELECT id, full_name, email, phone, phone_country_code, college, avatar_url, created_at FROM profiles WHERE id = ?", (user_payload['sub'],), one=True)
        if profile:
            profile['role'] = 'student'
            return jsonify({'user': profile}), 200

    return jsonify({'error': 'User not found.'}), 404
