import uuid
import datetime
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, send_from_directory, Response
from database import query_db, execute_db
from utils.auth import jwt_required, admin_required
from utils.email_service import send_feedback_email
from config import Config

submission_bp = Blueprint('submission_bp', __name__)

STORAGE_ASSIGNMENTS_DIR = os.path.join(Config.STORAGE_DIR, "assignments")
os.makedirs(STORAGE_ASSIGNMENTS_DIR, exist_ok=True)

MAX_PDF_SIZE_BYTES = int(os.getenv("MAX_ASSIGNMENT_PDF_SIZE_MB", "10")) * 1024 * 1024

@submission_bp.route('/api/assignments/<assignment_id>/submit', methods=['POST'])
@submission_bp.route('/api/submissions/upload', methods=['POST'])
@submission_bp.route('/api/submissions', methods=['POST'])
@jwt_required
def submit_task():
    user = request.user
    
    # Handle both multipart/form-data PDF upload and JSON URL submission
    application_id = request.form.get('application_id') or request.form.get('enrollment_id')
    week_number = request.form.get('week_number')
    
    if not application_id and request.is_json:
        data = request.get_json() or {}
        application_id = data.get('application_id') or data.get('enrollment_id')
        week_number = data.get('week_number')

    if not application_id or not week_number:
        return jsonify({'error': 'Application ID and week number are required.'}), 400

    app_record = query_db("SELECT * FROM applications WHERE id = ? AND (user_id = ? OR ? = 'admin')", (application_id, user['sub'], user.get('role')), one=True)
    if not app_record:
        return jsonify({'error': 'Unauthorized or invalid application record.'}), 403

    saved_file_path = None
    original_filename = "assignment_deliverable.pdf"
    file_size = 0

    # 1. File Upload Processing
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename != '':
            original_filename = secure_filename(uploaded_file.filename)
            if not original_filename.lower().endswith('.pdf'):
                return jsonify({'error': 'Only PDF files (.pdf) are allowed for assignment submissions.'}), 400

            # Read content to check MIME type and size
            file_bytes = uploaded_file.read()
            file_size = len(file_bytes)

            if file_size > MAX_PDF_SIZE_BYTES:
                return jsonify({'error': f'File size exceeds maximum limit of {int(MAX_PDF_SIZE_BYTES / (1024*1024))} MB.'}), 400

            if not file_bytes.startswith(b'%PDF'):
                return jsonify({'error': 'Invalid PDF file format.'}), 400

            safe_filename = f"app_{application_id[:8]}_week{week_number}_{uuid.uuid4().hex[:6]}.pdf"
            saved_file_path = os.path.join(STORAGE_ASSIGNMENTS_DIR, safe_filename)
            with open(saved_file_path, 'wb') as f:
                f.write(file_bytes)
            
            file_url = f"/api/submissions/files/{safe_filename}"
    else:
        data = request.get_json() if request.is_json else {}
        file_url = data.get('file_url', '').strip() if data else ""
        if not file_url:
            return jsonify({'error': 'Please upload a valid PDF file for submission.'}), 400

    # Check deadline
    due_status = 'SUBMITTED'
    if app_record.get('start_date'):
        try:
            start_dt = datetime.datetime.strptime(app_record['start_date'], "%B %d, %Y")
            week_due_dt = start_dt + datetime.timedelta(days=7 * int(week_number))
            if datetime.datetime.now() > week_due_dt:
                due_status = 'LATE'
        except Exception:
            pass

    # Check existing submission for this week
    existing = query_db("SELECT * FROM submissions WHERE application_id = ? AND week_number = ?", (application_id, week_number), one=True)
    
    if existing:
        execute_db("""
            UPDATE submissions
            SET file_url = ?, status = ?, feedback = NULL, marks = NULL,
                submitted_at = CURRENT_TIMESTAMP, original_file_name = ?, file_size = ?
            WHERE id = ?
        """, (file_url, due_status, original_filename, file_size, existing['id']))
        sub_id = existing['id']
        msg = f"Week {week_number} assignment re-submitted successfully!"
    else:
        sub_id = str(uuid.uuid4())
        execute_db("""
            INSERT INTO submissions (id, application_id, week_number, file_url, status, original_file_name, file_size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sub_id, application_id, week_number, file_url, due_status, original_filename, file_size))
        msg = f"Week {week_number} assignment submitted successfully!"

    sub_record = query_db("SELECT * FROM submissions WHERE id = ?", (sub_id,), one=True)
    return jsonify({'message': msg, 'submission': sub_record}), 201

@submission_bp.route('/api/submissions/files/<filename>', methods=['GET'])
@jwt_required
def serve_submission_file(filename):
    """Securely serve submitted assignment PDF files."""
    safe_name = secure_filename(filename)
    file_path = os.path.join(STORAGE_ASSIGNMENTS_DIR, safe_name)
    if os.path.exists(file_path):
        return send_from_directory(STORAGE_ASSIGNMENTS_DIR, safe_name)
    return jsonify({'error': 'Submission PDF file not found.'}), 404

@submission_bp.route('/api/admin/submissions/<sub_id>/grade', methods=['POST'])
@submission_bp.route('/api/submissions/<sub_id>/review', methods=['POST'])
@admin_required
def grade_submission(sub_id):
    """Admin endpoint to evaluate, give marks out of 10, add feedback, and update status."""
    data = request.get_json() or {}
    marks = data.get('marks')
    max_marks = data.get('max_marks', 10)
    feedback = data.get('feedback', '').strip()
    status = data.get('status', 'GRADED').lower() # 'graded', 'approved', 'revise', 'rejected'

    if status not in ['graded', 'approved', 'revise', 'rejected']:
        status = 'graded'

    sub_record = query_db("SELECT * FROM submissions WHERE id = ?", (sub_id,), one=True)
    if not sub_record:
        return jsonify({'error': 'Submission record not found.'}), 404

    execute_db("""
        UPDATE submissions
        SET status = ?, marks = ?, max_marks = ?, feedback = ?, reviewed_at = CURRENT_TIMESTAMP, graded_by = 'admin', graded_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, marks, max_marks, feedback, sub_id))

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
            feedback or f"Assignment evaluated. Marks: {marks}/{max_marks}."
        )

        # Check if all weekly assignments are submitted/graded -> Mark completion eligibility (Rule 26)
        graded_count = query_db("""
            SELECT COUNT(*) as cnt FROM submissions
            WHERE application_id = ? AND status IN ('graded', 'approved')
        """, (app_record['id'],), one=True)['cnt']

        if graded_count >= app_record['duration_weeks']:
            # Mark eligible for certificate issuance when official end date arrives (Section 26 Rule)
            execute_db("UPDATE applications SET completion_status = 'eligible' WHERE id = ?", (app_record['id'],))

    updated_sub = query_db("SELECT * FROM submissions WHERE id = ?", (sub_id,), one=True)
    return jsonify({'message': f'Assignment graded successfully.', 'submission': updated_sub}), 200
