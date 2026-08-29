import uuid
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from utils.email_service import send_welcome_newsletter

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/api/site-stats', methods=['GET'])
def get_site_stats():
    stats = query_db("SELECT * FROM site_stats ORDER BY sort_order ASC")
    return jsonify({'stats': stats}), 200

@public_bp.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    testimonials = query_db("SELECT * FROM testimonials WHERE is_published = 1 ORDER BY rating DESC")
    return jsonify({'testimonials': testimonials}), 200

@public_bp.route('/api/products', methods=['GET'])
def get_products():
    products = query_db("SELECT * FROM products WHERE is_active = 1")
    return jsonify({'products': products}), 200

@public_bp.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email or '@' not in email:
        return jsonify({'error': 'Please provide a valid email address.'}), 400

    existing = query_db("SELECT * FROM newsletter_subscribers WHERE email = ?", (email,), one=True)
    if existing:
        return jsonify({'message': 'You are already subscribed to our newsletter!'}), 200

    sub_id = str(uuid.uuid4())
    execute_db("INSERT INTO newsletter_subscribers (id, email) VALUES (?, ?)", (sub_id, email))
    send_welcome_newsletter(email)

    return jsonify({'message': 'Thank you for subscribing to Web Intern updates!'}), 201

@public_bp.route('/api/contact', methods=['POST'])
def contact_form():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message fields are required.'}), 400

    return jsonify({'message': 'Thank you! Your message has been received. Our support team will get back to you shortly.'}), 200
