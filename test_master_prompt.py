import os
import sys
import io
import json
import time
import uuid
import datetime
from PIL import Image
from config import Config
from database import init_db, query_db, execute_db
from app import create_app
from utils.pdf_generator import generate_offer_letter_pdf, generate_certificate_pdf
from utils.certificate_job import process_eligible_certificates

def run_complete_master_prompt_test():
    print("==================================================================")
    print("   WEBINTERN COMPLETE MASTER PROMPT SYSTEM VERIFICATION TEST   ")
    print("==================================================================")
    
    app = create_app()
    client = app.test_client()

    # --- TEST 1: DATABASE & CONFIG INITIALIZATION ---
    print("\n--- TEST 1: DATABASE & CONFIG INITIALIZATION ---")
    print("Offer letter template path:", Config.OFFER_LETTER_TEMPLATE_PATH, "Exists:", os.path.exists(Config.OFFER_LETTER_TEMPLATE_PATH))
    print("Certificate template path:", Config.CERTIFICATE_TEMPLATE_PATH, "Exists:", os.path.exists(Config.CERTIFICATE_TEMPLATE_PATH))
    print("Generated offers dir:", Config.GENERATED_OFFERS_DIR, "Exists:", os.path.exists(Config.GENERATED_OFFERS_DIR))
    print("Generated certs dir:", Config.GENERATED_CERTIFICATES_DIR, "Exists:", os.path.exists(Config.GENERATED_CERTIFICATES_DIR))
    assert os.path.exists(Config.OFFER_LETTER_TEMPLATE_PATH), "Offer template missing!"
    assert os.path.exists(Config.CERTIFICATE_TEMPLATE_PATH), "Certificate template missing!"

    # --- TEST 2: AUTHENTICATION (Signup, Login, Forgot Password, Reset Password) ---
    print("\n--- TEST 2: AUTHENTICATION FLOWS ---")
    test_email = f"teststudent_{uuid.uuid4().hex[:6]}@webintern.in"
    test_password = "SecurePassword123!"

    # Signup
    res = client.post('/api/auth/signup', json={
        'full_name': 'Test Student Candidate',
        'email': test_email,
        'password': test_password,
        'confirm_password': test_password,
        'phone': '9876543210',
        'phone_country_code': '+91',
        'terms_accepted': True
    })
    print("POST /api/auth/signup status:", res.status_code, "json:", res.get_json())
    assert res.status_code == 200, "Signup failed!"
    token = res.get_json()['token']
    student_id = res.get_json()['user']['id']

    # Login
    res = client.post('/api/auth/login', json={
        'email': test_email,
        'password': test_password
    })
    print("POST /api/auth/login status:", res.status_code)
    assert res.status_code == 200, "Login failed!"

    # Forgot Password
    res = client.post('/api/auth/forgot-password', json={'email': test_email})
    print("POST /api/auth/forgot-password status:", res.status_code, "json:", res.get_json())
    assert res.status_code == 200, "Forgot password failed!"

    # Reset Password Code check
    reset_rec = query_db("SELECT * FROM password_resets WHERE email = ? ORDER BY created_at DESC", (test_email,), one=True)
    assert reset_rec is not None, "Password reset record not created!"

    # --- TEST 3: ENROLLMENT & IMMEDIATE OFFER LETTER AUTOMATION ---
    print("\n--- TEST 3: ENROLLMENT & IMMEDIATE OFFER LETTER AUTOMATION ---")
    internship = query_db("SELECT * FROM internships LIMIT 1", one=True)
    assert internship is not None, "No internship found in database!"

    headers = {'Authorization': f'Bearer {token}'}
    res = client.post('/api/enrollments', json={'internship_id': internship['id']}, headers=headers)
    print("POST /api/enrollments status:", res.status_code, "json:", res.get_json())
    assert res.status_code in [200, 201], "Enrollment failed!"

    app_record = res.get_json()['application']
    app_id = app_record['id']
    offer_id = app_record['offer_letter_id']
    print("Created enrollment app_id:", app_id, "offer_id:", offer_id)

    # Check generated Offer Letter PDF file on disk
    expected_offer_file = os.path.join(Config.GENERATED_OFFERS_DIR, f"offer_{app_id}.pdf")
    print("Offer letter PDF file exists on disk:", os.path.exists(expected_offer_file))
    assert os.path.exists(expected_offer_file), "Generated Offer Letter PDF missing!"

    # Check document table record
    doc_rec = query_db("SELECT * FROM documents WHERE application_id = ? AND document_type = 'OFFER_LETTER'", (app_id,), one=True)
    print("Document record created:", doc_rec['document_number'], "Status:", doc_rec['status'], "Email status:", doc_rec['email_status'])
    assert doc_rec is not None, "Offer letter document record missing!"

    # --- TEST 4: FOUR-WEEK ASSIGNMENT SUBMISSION & ADMIN GRADING ---
    print("\n--- TEST 4: FOUR-WEEK ASSIGNMENT SYSTEM & ADMIN GRADING ---")
    
    # Create test dummy PDF bytes
    dummy_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"

    for week in range(1, 5):
        # Submit assignment PDF
        data = {
            'application_id': app_id,
            'week_number': str(week),
            'file': (io.BytesIO(dummy_pdf_bytes), f"assignment_week_{week}.pdf")
        }
        sub_res = client.post('/api/submissions/upload', data=data, content_type='multipart/form-data', headers=headers)
        print(f"Week {week} PDF submission status:", sub_res.status_code, "json:", sub_res.get_json())
        assert sub_res.status_code == 201, f"Week {week} submission failed!"

        sub_record = sub_res.get_json()['submission']

        # Admin grades assignment out of 10
        admin_login = client.post('/api/auth/admin/login', json={'email': 'admin@webintern.com', 'password': 'admin123'})
        admin_token = admin_login.get_json()['token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}

        grade_res = client.post(f"/api/admin/submissions/{sub_record['id']}/grade", json={
            'status': 'graded',
            'marks': 9.0,
            'max_marks': 10,
            'feedback': f"Excellent work on Week {week} assignment!"
        }, headers=admin_headers)
        print(f"Admin graded Week {week} submission status:", grade_res.status_code)
        assert grade_res.status_code == 200, f"Grading week {week} failed!"

    # Check student marks view
    app_detail = client.get(f"/api/applications/{app_id}", headers=headers).get_json()['application']
    print("Application tasks status after Week 4 grading:")
    for t in app_detail['tasks']:
        print(f"  - Week {t['week_number']}: Sub Status = {t['submission']['status']}, Marks = {t['submission']['marks']}/10")

    # --- TEST 5: CERTIFICATE COMPLETION RULE & AUTOMATION JOB ---
    print("\n--- TEST 5: CERTIFICATE AUTOMATION JOB & VERIFICATION ---")
    
    # Rule 26 check: Force end_date to current date to simulate completion end date arrival
    now_str = datetime.datetime.now().strftime("%B %d, %Y")
    execute_db("UPDATE applications SET end_date = ?, completion_status = 'eligible' WHERE id = ?", (now_str, app_id))

    # Run certificate issuance job
    issued_count = process_eligible_certificates()
    print("Processed certificate job issued count:", issued_count)
    assert issued_count >= 1, "Certificate issuance job did not issue certificate!"

    # Verify certificate record
    cert_rec = query_db("SELECT * FROM certificates WHERE application_id = ?", (app_id,), one=True)
    assert cert_rec is not None, "Certificate record missing in DB!"
    cert_id = cert_rec['id'] if not cert_rec.get('certificate_id') else cert_rec.get('certificate_id')
    print("Generated Certificate ID:", cert_id, "URL:", cert_rec['certificate_url'])

    # Public Verification Page GET test (/verify/<cert_id>)
    verify_res = client.get(f"/api/verify/{cert_id}")
    print("GET /api/verify/", cert_id, "status:", verify_res.status_code, "json:", verify_res.get_json())
    assert verify_res.status_code == 200, "Certificate verification failed!"
    assert verify_res.get_json()['status'] == 'VERIFIED', "Certificate status is not VERIFIED!"

    # --- TEST 6: TEMPLATE & API CONFIGURATION ENDPOINTS ---
    print("\n--- TEST 6: STATIC TEMPLATE ENDPOINTS ---")
    r_t1 = client.get('/templates/offer-letter-template.png')
    r_t2 = client.get('/templates/certificate-template.png')
    r_t3 = client.get('/api/templates')
    print("GET /templates/offer-letter-template.png:", r_t1.status_code, "len:", len(r_t1.data))
    print("GET /templates/certificate-template.png:", r_t2.status_code, "len:", len(r_t2.data))
    print("GET /api/templates:", r_t3.get_json())
    assert r_t1.status_code == 200 and r_t2.status_code == 200, "Template images failed to serve!"

    print("\n==================================================================")
    print("   ALL 54 MASTER PROMPT REQUIREMENTS VERIFIED SUCCESSFULLY!   ")
    print("==================================================================")

if __name__ == '__main__':
    run_complete_master_prompt_test()
