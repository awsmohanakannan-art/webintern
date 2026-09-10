import uuid
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from utils.email_service import send_welcome_newsletter, send_contact_form_notification

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/api/site-stats', methods=['GET'])
@public_bp.route('/site-stats', methods=['GET'])
def get_site_stats():
    stats = query_db("SELECT * FROM site_stats ORDER BY sort_order ASC")
    return jsonify({'stats': stats}), 200

@public_bp.route('/api/testimonials', methods=['GET'])
@public_bp.route('/testimonials', methods=['GET'])
def get_testimonials():
    testimonials = query_db("SELECT * FROM testimonials WHERE is_published = 1 ORDER BY rating DESC")
    return jsonify({'testimonials': testimonials}), 200

@public_bp.route('/api/products', methods=['GET'])
@public_bp.route('/products', methods=['GET'])
def get_products():
    products = query_db("SELECT * FROM products WHERE is_active = 1")
    return jsonify({'products': products}), 200

@public_bp.route('/api/newsletter', methods=['POST'])
@public_bp.route('/newsletter', methods=['POST'])
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
@public_bp.route('/contact', methods=['POST'])
def contact_form():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip() or data.get('mobile', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not name:
        return jsonify({'error': 'Your Name is required.'}), 400
    if not email or '@' not in email:
        return jsonify({'error': 'A valid Email Address is required.'}), 400
    if not message:
        return jsonify({'error': 'Message / Requirement details are required.'}), 400

    # Save inquiry to database
    msg_id = str(uuid.uuid4())
    execute_db("""
        INSERT INTO contact_messages (id, name, email, phone, subject, message, status)
        VALUES (?, ?, ?, ?, ?, ?, 'UNREAD')
    """, (msg_id, name, email, phone, subject, message))

    # Send email notification to webinternsupport@gmail.com
    send_contact_form_notification(
        sender_name=name,
        sender_email=email,
        sender_phone=phone,
        subject_line=subject,
        message_text=message
    )

    return jsonify({
        'message': 'Thank you! Your requirements and message have been sent directly to webinternsupport@gmail.com. Our support team will get back to you shortly.'
    }), 200
