import uuid
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from utils.auth import jwt_required
from utils.razorpay_service import create_razorpay_order, verify_razorpay_signature
from config import Config

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/api/payments/create-order', methods=['POST'])
@jwt_required
def create_order():
    user = request.user
    data = request.get_json() or {}
    certificate_id = data.get('certificate_id')

    if not certificate_id:
        return jsonify({'error': 'Certificate ID is required.'}), 400

    cert = query_db("SELECT * FROM certificates WHERE id = ?", (certificate_id,), one=True)
    if not cert:
        return jsonify({'error': 'Certificate record not found.'}), 404

    # Fetch product info
    product = query_db("SELECT * FROM products WHERE is_active = 1 LIMIT 1", one=True)
    amount_inr = product['price_inr'] if product else 499

    receipt_id = f"rcpt_{uuid.uuid4().hex[:10]}"
    success, razorpay_order = create_razorpay_order(
        amount_inr,
        receipt_id,
        notes={'certificate_id': certificate_id, 'user_id': user['sub']}
    )

    if not success:
        return jsonify({'error': 'Failed to create payment order with gateway.'}), 500

    order_id = razorpay_order['id']

    # Store payment record in database
    payment_id = str(uuid.uuid4())
    execute_db("""
        INSERT INTO payments (id, user_id, certificate_id, product_id, razorpay_order_id, amount_inr, status)
        VALUES (?, ?, ?, ?, ?, ?, 'created')
    """, (payment_id, user['sub'], certificate_id, product['id'] if product else None, order_id, amount_inr))

    return jsonify({
        'message': 'Razorpay order generated successfully.',
        'order_id': order_id,
        'key_id': Config.RAZORPAY_KEY_ID,
        'amount': razorpay_order['amount'],
        'currency': razorpay_order['currency'],
        'payment_record_id': payment_id
    }), 200

@payment_bp.route('/api/payments/verify', methods=['POST'])
@jwt_required
def verify_payment():
    user = request.user
    data = request.get_json() or {}
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')
    certificate_id = data.get('certificate_id')

    if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
        return jsonify({'error': 'Missing payment signature verification parameters.'}), 400

    is_valid = verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
    if not is_valid:
        return jsonify({'error': 'Payment signature verification failed.'}), 400

    # Update payment record
    execute_db("""
        UPDATE payments
        SET razorpay_payment_id = ?, razorpay_signature = ?, status = 'paid'
        WHERE razorpay_order_id = ?
    """, (razorpay_payment_id, razorpay_signature, razorpay_order_id))

    # Mark certificate as verified paid
    if certificate_id:
        execute_db("UPDATE certificates SET is_verified_paid = 1 WHERE id = ?", (certificate_id,))
    else:
        pmt = query_db("SELECT certificate_id FROM payments WHERE razorpay_order_id = ?", (razorpay_order_id,), one=True)
        if pmt and pmt['certificate_id']:
            execute_db("UPDATE certificates SET is_verified_paid = 1 WHERE id = ?", (pmt['certificate_id'],))

    return jsonify({
        'message': 'Payment verified successfully! Your certificate has been upgraded to Verified status.',
        'status': 'paid'
    }), 200

@payment_bp.route('/api/payments/webhook', methods=['POST'])
def payment_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get('X-Razorpay-Signature')

    # Log webhook event cleanly
    data = request.get_json() or {}
    event = data.get('event')
    print(f"[Razorpay Webhook Event]: {event}")

    if event == 'payment.captured':
        payment_entity = data.get('payload', {}).get('payment', {}).get('entity', {})
        order_id = payment_entity.get('order_id')
        if order_id:
            execute_db("UPDATE payments SET status = 'paid' WHERE razorpay_order_id = ?", (order_id,))
            pmt = query_db("SELECT certificate_id FROM payments WHERE razorpay_order_id = ?", (order_id,), one=True)
            if pmt and pmt['certificate_id']:
                execute_db("UPDATE certificates SET is_verified_paid = 1 WHERE id = ?", (pmt['certificate_id'],))

    return jsonify({'status': 'ok'}), 200
