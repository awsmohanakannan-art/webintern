import uuid
import datetime
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from utils.auth import jwt_required, admin_required
from utils.email_service import send_feedback_email

submission_bp = Blueprint('submission_bp', __name__)

@submission_bp.route('/api/submissions', methods=['POST'])
@jwt_required
def submit_task():
    user = request.user
    data = request.get_json() or {}
    application_id = data.get('application_id')
    week_number = data.get('week_number')
    file_url = data.get('file_url', '').strip()

    if not application_id or not week_number or not file_url:
        return jsonify({'error': 'Application ID, week number, and task submission file URL are required.'}), 400

    app_record = query_db("SELECT * FROM applications WHERE id = ? AND user_id = ?", (application_id, user['sub']), one=True)
    if not app_record:
        return jsonify({'error': 'Unauthorized or invalid application.'}), 403

    # Check existing submission for this week
    existing = query_db("SELECT * FROM submissions WHERE application_id = ? AND week_number = ?", (application_id, week_number), one=True)
    
    if existing:
        execute_db("""
            UPDATE submissions
            SET file_url = ?, status = 'pending', feedback = NULL, submitted_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (file_url, existing['id']))
        sub_id = existing['id']
        msg = f"Week {week_number} task deliverable re-submitted successfully!"
    else:
        sub_id = str(uuid.uuid4())
        execute_db("""
            INSERT INTO submissions (id, application_id, week_number, file_url, status)
            VALUES (?, ?, ?, ?, 'pending')
        """, (sub_id, application_id, week_number, file_url))
        msg = f"Week {week_number} task deliverable submitted successfully!"

    sub_record = query_db("SELECT * FROM submissions WHERE id = ?", (sub_id,), one=True)
    return jsonify({'message': msg, 'submission': sub_record}), 201

@submission_bp.route('/api/submissions/<sub_id>/review', methods=['POST'])
@admin_required
def review_submission(sub_id):
    data = request.get_json() or {}
    status = data.get('status') # 'approved' or 'revise'
    feedback = data.get('feedback', '').strip()

    if status not in ['approved', 'revise']:
        return jsonify({'error': 'Status must be either approved or revise.'}), 400

    sub_record = query_db("SELECT * FROM submissions WHERE id = ?", (sub_id,), one=True)
    if not sub_record:
        return jsonify({'error': 'Submission record not found.'}), 404

    execute_db("""
        UPDATE submissions
        SET status = ?, feedback = ?, reviewed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, feedback, sub_id))

    # Fetch candidate details
    app_record = query_db("""
        SELECT a.*, i.duration_weeks, p.full_name, p.email
        FROM applications a
        JOIN profiles p ON a.user_id = p.id
        JOIN internships i ON a.internship_id = i.id
        WHERE a.id = ?
    """, (sub_record['application_id'],), one=True)

    if app_record:
        # Notify student via email
        send_feedback_email(
            app_record['email'],
            app_record['full_name'],
            sub_record['week_number'],
            status,
            feedback or ("Great work! Task approved." if status == 'approved' else "Please review requirements and re-submit.")
        )

        # Check if final week approved -> Auto issue certificate
        if status == 'approved':
            approved_count = query_db("""
                SELECT COUNT(*) as cnt FROM submissions
                WHERE application_id = ? AND status = 'approved'
            """, (app_record['id'],), one=True)['cnt']

            if approved_count >= app_record['duration_weeks']:
                # Check if certificate exists
                cert = query_db("SELECT * FROM certificates WHERE application_id = ?", (app_record['id'],), one=True)
                if not cert:
                    cert_id = str(uuid.uuid4())
                    execute_db("""
                        INSERT INTO certificates (id, application_id, is_verified_paid)
                        VALUES (?, ?, 0)
                    """, (cert_id, app_record['id']))
                
                # Mark application completed
                execute_db("UPDATE applications SET status = 'completed' WHERE id = ?", (app_record['id'],))

    updated_sub = query_db("SELECT * FROM submissions WHERE id = ?", (sub_id,), one=True)
    return jsonify({'message': f'Submission marked as {status}.', 'submission': updated_sub}), 200
