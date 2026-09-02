import uuid
from flask import Blueprint, request, jsonify, make_response
from database import query_db, execute_db
from utils.otp import create_and_store_otp, verify_otp_code
from utils.auth import generate_jwt, check_password, jwt_required
from utils.email_service import send_otp_email
from config import Config
from supabase import create_client

auth_bp = Blueprint('auth_bp', __name__)

def get_supabase_admin():
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_ROLE_KEY)

def get_supabase_anon():
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)

@auth_bp.route('/api/auth/config', methods=['GET'])
def get_auth_config():
    """Return public Supabase configuration for frontend initialization."""
    return jsonify({
        'supabase_url': Config.SUPABASE_URL,
        'supabase_anon_key': Config.SUPABASE_ANON_KEY,
        'google_client_id': Config.GOOGLE_CLIENT_ID
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

@auth_bp.route('/api/auth/register', methods=['POST'])
def register_user():
    """Step 1: Register user with Supabase Auth and create unverified profile."""
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
    if not phone:
        return jsonify({'error': 'Mobile number is required.'}), 400
    if not password:
        return jsonify({'error': 'Password is required.'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400
    if not terms_accepted:
        return jsonify({'error': 'You must agree to the Terms & Conditions and Privacy Policy.'}), 400

    full_mobile = f"{phone_country_code} {phone}".strip()

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

        # 2. Insert into public.profiles in Supabase
        profile_data = {
            'id': user_id,
            'name': full_name,
            'mobile': full_mobile,
            'phone_verified': False,
            'auth_provider': 'email',
            'terms_accepted': True,
            'marketing_opt_in': marketing_opt_in,
            'profile_complete': False
        }
        
        supabase_admin.table('profiles').upsert(profile_data).execute()
        sync_profile_to_local_db(user_id, full_name, email, phone, phone_country_code, marketing_opt_in)

        # 3. Generate mobile OTP for verification
        code = create_and_store_otp(email, purpose='register_mobile')
        send_otp_email(email, code, purpose='registration')

        return jsonify({
            'message': 'Account created! Please enter the 6-digit OTP code sent to verify your account.',
            'user_id': user_id,
            'email': email,
            'dev_otp': code
        }), 200

    except Exception as e:
        err_msg = str(e)
        if 'already registered' in err_msg.lower() or 'already exists' in err_msg.lower() or 'duplicate' in err_msg.lower():
            return jsonify({'error': 'An account with this email address already exists. Please sign in instead.'}), 400
        return jsonify({'error': f'Registration failed: {err_msg}'}), 400

@auth_bp.route('/api/auth/verify-mobile-otp', methods=['POST'])
def verify_mobile_otp():
    """Step 2: Verify OTP code and complete user registration profile."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()
    user_id = data.get('user_id', '').strip()

    if not email or not code:
        return jsonify({'error': 'Email and verification code are required.'}), 400

    valid, msg = verify_otp_code(email, code, purpose='register_mobile')
    if not valid:
        # Fallback check standard 'register' or 'complete_profile' OTPs
        valid, msg = verify_otp_code(email, code, purpose='complete_profile')
        if not valid:
            valid, msg = verify_otp_code(email, code, purpose='register')
            if not valid:
                return jsonify({'error': msg}), 400

    try:
        supabase_admin = get_supabase_admin()
        
        # Mark profile as verified & complete in Supabase
        update_payload = {
            'phone_verified': True,
            'profile_complete': True
        }
        
        if user_id:
            supabase_admin.table('profiles').update(update_payload).eq('id', user_id).execute()
            prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        else:
            prof_res = supabase_admin.table('profiles').select('*').eq('email', email).execute()
            if prof_res.data and len(prof_res.data) > 0:
                user_id = prof_res.data[0]['id']
                supabase_admin.table('profiles').update(update_payload).eq('id', user_id).execute()

        profile = prof_res.data[0] if (prof_res.data and len(prof_res.data) > 0) else None
        user_name = profile.get('name') if profile else email.split('@')[0]

        token = generate_jwt({
            'sub': user_id or str(uuid.uuid4()),
            'email': email,
            'name': user_name,
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Account verified and activated successfully!',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': user_name,
                'mobile': profile.get('mobile') if profile else '',
                'profile_complete': True,
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        return jsonify({'error': f'Failed to verify account: {str(e)}'}), 400

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

        # Retrieve profile from Supabase profiles table
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        
        profile = None
        if prof_res.data and len(prof_res.data) > 0:
            profile = prof_res.data[0]
        else:
            # Create default profile if missing
            default_profile = {
                'id': user_id,
                'name': auth_res.user.user_metadata.get('name', email.split('@')[0]),
                'mobile': '',
                'phone_verified': False,
                'auth_provider': 'email',
                'terms_accepted': True,
                'marketing_opt_in': False,
                'profile_complete': True
            }
            supabase_admin.table('profiles').upsert(default_profile).execute()
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
                'profile_complete': profile.get('profile_complete', True),
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        err_msg = str(e)
        if 'invalid credentials' in err_msg.lower() or 'invalid login' in err_msg.lower():
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
        
        # Fetch profile
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        profile = prof_res.data[0] if (prof_res.data and len(prof_res.data) > 0) else None

        if not profile:
            # Check if existing profile matches by email
            email_prof = supabase_admin.table('profiles').select('*').eq('email', email).execute()
            if email_prof.data and len(email_prof.data) > 0:
                existing = email_prof.data[0]
                provider = 'both' if existing.get('auth_provider') == 'email' else existing.get('auth_provider', 'google')
                supabase_admin.table('profiles').update({'auth_provider': provider}).eq('id', existing['id']).execute()
                profile = existing
                profile['auth_provider'] = provider
            else:
                # Create initial incomplete profile for new Google user
                new_profile = {
                    'id': user_id,
                    'name': name or email.split('@')[0],
                    'mobile': '',
                    'phone_verified': False,
                    'auth_provider': 'google',
                    'terms_accepted': False,
                    'marketing_opt_in': False,
                    'profile_complete': False
                }
                supabase_admin.table('profiles').insert(new_profile).execute()
                profile = new_profile
                sync_profile_to_local_db(user_id, name or email.split('@')[0], email)

        token = generate_jwt({
            'sub': profile['id'],
            'email': email,
            'name': profile.get('name') or name or email.split('@')[0],
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Google user profile retrieved.',
            'token': token,
            'user': {
                'id': profile['id'],
                'email': email,
                'full_name': profile.get('name') or name or email.split('@')[0],
                'mobile': profile.get('mobile', ''),
                'profile_complete': profile.get('profile_complete', False),
                'auth_provider': profile.get('auth_provider', 'google'),
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        return jsonify({'error': f'Failed to sync Google user: {str(e)}'}), 400

@auth_bp.route('/api/auth/complete-google-profile', methods=['POST'])
def complete_google_profile_request():
    """Request OTP for completing Google user profile (Mobile + Terms)."""
    data = request.get_json() or {}
    user_id = data.get('user_id')
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip()
    terms_accepted = data.get('terms_accepted', False)

    if not user_id or not email or not phone:
        return jsonify({'error': 'User ID, email, and mobile number are required.'}), 400
    if not terms_accepted:
        return jsonify({'error': 'You must agree to the Terms & Conditions and Privacy Policy.'}), 400

    code = create_and_store_otp(email, purpose='complete_profile')
    send_otp_email(email, code, purpose='registration')

    return jsonify({
        'message': 'Verification code sent to your email address.',
        'email': email,
        'dev_otp': code
    }), 200

@auth_bp.route('/api/auth/verify-google-profile-otp', methods=['POST'])
def verify_google_profile_otp():
    """Verify OTP and mark Google user profile as complete."""
    data = request.get_json() or {}
    user_id = data.get('user_id')
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()
    phone = data.get('phone', '').strip()
    phone_country_code = data.get('phone_country_code', '+91').strip()
    marketing_opt_in = data.get('marketing_opt_in', False)

    if not email or not code:
        return jsonify({'error': 'Email and verification code are required.'}), 400

    valid, msg = verify_otp_code(email, code, purpose='complete_profile')
    if not valid:
        valid, msg = verify_otp_code(email, code, purpose='register_mobile')
        if not valid:
            return jsonify({'error': msg}), 400

    full_mobile = f"{phone_country_code} {phone}".strip()

    try:
        supabase_admin = get_supabase_admin()

        update_data = {
            'mobile': full_mobile,
            'phone_verified': True,
            'terms_accepted': True,
            'marketing_opt_in': marketing_opt_in,
            'profile_complete': True
        }

        supabase_admin.table('profiles').update(update_data).eq('id', user_id).execute()
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        profile = prof_res.data[0] if (prof_res.data and len(prof_res.data) > 0) else {}

        user_name = profile.get('name') or email.split('@')[0]
        sync_profile_to_local_db(user_id, user_name, email, phone, phone_country_code, marketing_opt_in)

        token = generate_jwt({
            'sub': user_id,
            'email': email,
            'name': user_name,
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Profile completed successfully!',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': user_name,
                'mobile': full_mobile,
                'profile_complete': True,
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        return jsonify({'error': f'Failed to complete profile: {str(e)}'}), 400

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
        # Try fetching from Supabase first
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
                        'profile_complete': p.get('profile_complete', True),
                        'role': 'student'
                    }
                }), 200
        except Exception:
            pass

        # Fallback to local DB
        profile = query_db("SELECT id, full_name, email, phone, phone_country_code, college, avatar_url, created_at FROM profiles WHERE id = ?", (user_payload['sub'],), one=True)
        if profile:
            profile['role'] = 'student'
            return jsonify({'user': profile}), 200

    return jsonify({'error': 'User not found.'}), 404
