import uuid
import datetime
from flask import Blueprint, request, jsonify, Response
from database import query_db, execute_db
from utils.auth import jwt_required
from utils.email_service import send_offer_letter_email
from utils.pdf_generator import generate_offer_letter_pdf

application_bp = Blueprint('application_bp', __name__)

@application_bp.route('/api/applications', methods=['POST'])
@jwt_required
def create_application():
    user = request.user
    data = request.get_json() or {}
    internship_id = data.get('internship_id')

    if not internship_id:
        return jsonify({'error': 'Internship ID is required.'}), 400

    internship = query_db("SELECT * FROM internships WHERE id = ?", (internship_id,), one=True)
    if not internship:
        return jsonify({'error': 'Selected internship program not found.'}), 404

    # Check existing active application
    existing = query_db("SELECT * FROM applications WHERE user_id = ? AND internship_id = ?", (user['sub'], internship_id), one=True)
    if existing:
        return jsonify({
            'message': 'You have already applied to this internship.',
            'application': existing
        }), 200

    app_id = str(uuid.uuid4())
    execute_db("""
        INSERT INTO applications (id, user_id, internship_id, status, offer_letter_sent)
        VALUES (?, ?, ?, 'active', 1)
    """, (app_id, user['sub'], internship_id))

    # Fetch user profile to send offer letter
    profile = query_db("SELECT * FROM profiles WHERE id = ?", (user['sub'],), one=True)
    student_name = profile['full_name'] if profile else user.get('name', 'Student')
    to_email = profile['email'] if profile else user.get('email')

    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    pdf_bytes = generate_offer_letter_pdf(student_name, internship['title'], date_str)

    # Trigger transactional offer letter email
    send_offer_letter_email(to_email, student_name, internship['title'], pdf_bytes)

    new_app = query_db("SELECT * FROM applications WHERE id = ?", (app_id,), one=True)
    return jsonify({
        'message': 'Application submitted successfully! Your official offer letter has been sent to your email.',
        'application': new_app
    }), 201

@application_bp.route('/api/applications/me', methods=['GET'])
@jwt_required
def get_my_applications():
    user = request.user
    apps = query_db("""
        SELECT a.*, i.title as internship_title, i.slug as internship_slug, i.duration_weeks, i.cover_image_url,
               s.name as sector_name, c.id as certificate_id, c.is_verified_paid
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        JOIN sectors s ON i.sector_id = s.id
        LEFT JOIN certificates c ON a.id = c.application_id
        WHERE a.user_id = ?
        ORDER BY a.applied_at DESC
    """, (user['sub'],))

    for app_item in apps:
        # Calculate weekly progress
        approved_subs = query_db("""
            SELECT COUNT(*) as cnt FROM submissions
            WHERE application_id = ? AND status = 'approved'
        """, (app_item['id'],), one=True)
        
        completed_weeks = approved_subs['cnt'] if approved_subs else 0
        app_item['completed_weeks'] = completed_weeks
        app_item['progress_percent'] = int((completed_weeks / app_item['duration_weeks']) * 100)
        
        # Latest submission
        latest_sub = query_db("""
            SELECT * FROM submissions
            WHERE application_id = ?
            ORDER BY week_number DESC LIMIT 1
        """, (app_item['id'],), one=True)
        app_item['latest_submission'] = latest_sub

    return jsonify({'applications': apps}), 200

@application_bp.route('/api/applications/<app_id>', methods=['GET'])
@jwt_required
def get_application_detail(app_id):
    user = request.user
    app_record = query_db("""
        SELECT a.*, i.title as internship_title, i.slug as internship_slug, i.duration_weeks, i.full_description,
               s.name as sector_name, c.id as certificate_id, c.is_verified_paid
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        JOIN sectors s ON i.sector_id = s.id
        LEFT JOIN certificates c ON a.id = c.application_id
        WHERE a.id = ? AND (a.user_id = ? OR ? = 'admin')
    """, (app_id, user['sub'], user.get('role')), one=True)

    if not app_record:
        return jsonify({'error': 'Application record not found.'}), 404

    tasks = query_db("SELECT * FROM internship_tasks WHERE internship_id = ? ORDER BY week_number ASC", (app_record['internship_id'],))
    submissions = query_db("SELECT * FROM submissions WHERE application_id = ? ORDER BY week_number ASC", (app_id,))

    sub_map = {s['week_number']: s for s in submissions}

    for task in tasks:
        task['submission'] = sub_map.get(task['week_number'])

    app_record['tasks'] = tasks
    return jsonify({'application': app_record}), 200

@application_bp.route('/api/applications/<app_id>/offer-letter.pdf', methods=['GET'])
@jwt_required
def download_offer_letter(app_id):
    user = request.user
    app_record = query_db("""
        SELECT a.*, i.title as internship_title
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        WHERE a.id = ? AND (a.user_id = ? OR ? = 'admin')
    """, (app_id, user['sub'], user.get('role')), one=True)

    if not app_record:
        return jsonify({'error': 'Application not found.'}), 404

    profile = query_db("SELECT * FROM profiles WHERE id = ?", (app_record['user_id'],), one=True)
    student_name = profile['full_name'] if profile else "Intern Candidate"
    date_str = datetime.datetime.strptime(app_record['applied_at'], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y") if ' ' in str(app_record['applied_at']) else datetime.datetime.now().strftime("%B %d, %Y")

    pdf_bytes = generate_offer_letter_pdf(student_name, app_record['internship_title'], date_str)
    
    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'inline; filename="Offer_Letter_{app_id[:8]}.pdf"'}
    )
