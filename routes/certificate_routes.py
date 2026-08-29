import datetime
from flask import Blueprint, jsonify, Response
from database import query_db
from utils.pdf_generator import generate_certificate_pdf

certificate_bp = Blueprint('certificate_bp', __name__)

@certificate_bp.route('/api/certificates/<cert_id>', methods=['GET'])
def get_certificate(cert_id):
    cert = query_db("""
        SELECT c.*, a.user_id, a.applied_at, p.full_name as student_name,
               i.title as internship_title, s.name as sector_name
        FROM certificates c
        JOIN applications a ON c.application_id = a.id
        JOIN profiles p ON a.user_id = p.id
        JOIN internships i ON a.internship_id = i.id
        JOIN sectors s ON i.sector_id = s.id
        WHERE c.id = ? OR c.application_id = ?
    """, (cert_id, cert_id), one=True)

    if not cert:
        return jsonify({'error': 'Certificate record not found.'}), 404

    return jsonify({'certificate': cert}), 200

@certificate_bp.route('/api/certificates/<cert_id>/pdf', methods=['GET'])
def download_certificate_pdf(cert_id):
    cert = query_db("""
        SELECT c.*, a.user_id, p.full_name as student_name, i.title as internship_title
        FROM certificates c
        JOIN applications a ON c.application_id = a.id
        JOIN profiles p ON a.user_id = p.id
        JOIN internships i ON a.internship_id = i.id
        WHERE c.id = ? OR c.application_id = ?
    """, (cert_id, cert_id), one=True)

    if not cert:
        return jsonify({'error': 'Certificate record not found.'}), 404

    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    pdf_bytes = generate_certificate_pdf(
        cert['student_name'],
        cert['internship_title'],
        date_str,
        cert['id'][:12].upper(),
        is_verified=bool(cert['is_verified_paid'])
    )

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'inline; filename="WebIntern_Certificate_{cert["id"][:8]}.pdf"'}
    )
