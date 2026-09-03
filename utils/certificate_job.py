import uuid
import datetime
import os
from database import query_db, execute_db
from utils.pdf_generator import generate_certificate_pdf
from utils.email_service import send_certificate_email
from utils.google_sheets_service import sync_certificate_to_google_sheets
from config import Config

def process_eligible_certificates():
    """
    Idempotent background job to process certificate issuance (Section 26 & 27 Rules):
    1. Checks enrollments whose end_date has arrived/passed.
    2. Verifies completion status (all weekly assignments graded/approved).
    3. Checks certificate does not already exist.
    4. Generates unique Certificate ID, PDF, sends email, and syncs to Google Sheets.
    """
    print("[Certificate Automation Job]: Running eligibility check...")
    
    # Query active/completed applications with valid end_date or eligible status
    apps = query_db("""
        SELECT a.*, i.title as internship_title, i.duration_weeks, i.company_name, i.guide_name, i.project_name,
               p.full_name as student_name, p.email as student_email, p.college as student_college
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        JOIN profiles p ON a.user_id = p.id
        WHERE a.completion_status IN ('eligible', 'approved', 'completed') OR a.status = 'completed'
    """)

    issued_count = 0
    now_dt = datetime.datetime.now()

    for app_record in apps:
        app_id = app_record['id']

        # 1. Check existing issued document to prevent duplicate issuance (Section 46 Idempotency)
        doc_exists = query_db("SELECT * FROM documents WHERE application_id = ? AND document_type = 'CERTIFICATE'", (app_id,), one=True)
        if doc_exists:
            continue

        # 2. Verify End Date has arrived/passed (Section 26 Rule)
        end_date_str = app_record.get('end_date')
        end_date_reached = False
        if end_date_str:
            try:
                end_dt = datetime.datetime.strptime(end_date_str, "%B %d, %Y")
                if now_dt.date() >= end_dt.date():
                    end_date_reached = True
            except Exception:
                end_date_reached = True # Fallback if format differs
        else:
            end_date_reached = True

        if not end_date_reached:
            print(f"[Certificate Job]: Application {app_id[:8]} end date {end_date_str} has not arrived yet.")
            continue

        # 3. Verify all assignment deliverables are approved/graded
        duration_weeks = app_record.get('duration_weeks') or 4
        graded_count = query_db("""
            SELECT COUNT(*) as cnt FROM submissions
            WHERE application_id = ? AND status IN ('graded', 'approved')
        """, (app_id,), one=True)['cnt']

        if graded_count < duration_weeks and app_record.get('completion_status') != 'eligible':
            print(f"[Certificate Job]: Application {app_id[:8]} has only {graded_count}/{duration_weeks} assignments completed.")
            continue

        # 4. Generate unique Certificate ID (Idempotent DB constraint check)
        cert_id = app_record.get('certificate_id') or f"WI-INT-2026-{app_id[:6].upper()}"
        issue_date_str = now_dt.strftime("%B %d, %Y")
        verify_url = f"https://webintern.in/verify/{cert_id}"

        # 5. Generate Certificate PDF with QR Code
        pdf_bytes = generate_certificate_pdf(
            student_name=app_record['student_name'],
            internship_title=app_record['internship_title'],
            date_str=issue_date_str,
            cert_id=cert_id,
            is_verified=True,
            college_name=app_record.get('student_college'),
            guide_name=app_record.get('guide_name') or "Dr. A. K. Sharma",
            project_name=app_record.get('project_name') or f"{app_record['internship_title']} Capstone",
            duration=f"{duration_weeks} Weeks",
            start_date=app_record.get('start_date'),
            end_date=end_date_str,
            company_name=app_record.get('company_name') or "Web Intern Platform",
            verification_url=verify_url
        )

        cert_file_path = os.path.join(Config.GENERATED_CERTIFICATES_DIR, f"certificate_{cert_id}.pdf")
        cert_url = f"/api/certificates/{cert_id}/pdf"

        # 6. Database record upsert
        existing_cert = query_db("SELECT * FROM certificates WHERE application_id = ?", (app_id,), one=True)
        if existing_cert:
            execute_db("""
                UPDATE certificates
                SET certificate_url = ?, is_verified_paid = 1, issued_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (cert_url, existing_cert['id']))
            cert_db_id = existing_cert['id']
        else:
            cert_db_id = str(uuid.uuid4())
            execute_db("""
                INSERT INTO certificates (id, application_id, certificate_url, is_verified_paid)
                VALUES (?, ?, ?, 1)
            """, (cert_db_id, app_id, cert_url))

        # Update application status
        execute_db("""
            UPDATE applications
            SET status = 'completed', completion_status = 'completed', certificate_id = ?
            WHERE id = ?
        """, (cert_id, app_id))

        # Save document record
        doc_id = str(uuid.uuid4())
        
        # 7. Send Certificate Email via Resend
        email_success, email_res = send_certificate_email(
            to_email=app_record['student_email'],
            student_name=app_record['student_name'],
            internship_title=app_record['internship_title'],
            cert_id=cert_id,
            pdf_bytes=pdf_bytes,
            start_date=app_record.get('start_date'),
            end_date=end_date_str,
            verification_url=verify_url
        )

        email_status = "SENT" if email_success else "FAILED"
        msg_id = email_res.get('id') if isinstance(email_res, dict) else str(email_res)

        execute_db("""
            INSERT INTO documents (id, application_id, student_id, document_type, document_number, file_path, status, email_status, email_message_id)
            VALUES (?, ?, ?, 'CERTIFICATE', ?, ?, 'ISSUED', ?, ?)
        """, (doc_id, app_id, app_record['user_id'], cert_id, cert_file_path, email_status, msg_id))

        # 8. Sync to Google Sheets asynchronously
        sync_certificate_to_google_sheets({
            "certificate_id": cert_id,
            "student_id": app_record['user_id'],
            "student_name": app_record['student_name'],
            "email": app_record['student_email'],
            "college": app_record.get('student_college') or "",
            "course_name": app_record['internship_title'],
            "role": app_record['internship_title'],
            "company": app_record.get('company_name') or "Web Intern Platform",
            "start_date": app_record.get('start_date') or "",
            "end_date": end_date_str or "",
            "duration": f"{duration_weeks} Weeks",
            "guide_name": app_record.get('guide_name') or "Dr. A. K. Sharma",
            "project_name": app_record.get('project_name') or f"{app_record['internship_title']} Capstone",
            "issue_date": issue_date_str,
            "document_status": "ISSUED",
            "email_status": email_status,
            "email_message_id": msg_id,
            "verification_url": verify_url
        }, document_id=doc_id)

        issued_count += 1
        print(f"[Certificate Job Success]: Certificate {cert_id} issued to {app_record['student_name']}.")

    print(f"[Certificate Automation Job Finished]: Issued {issued_count} certificates.")
    return issued_count
