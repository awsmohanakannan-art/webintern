import os
import io
import json
import uuid
import datetime
from config import Config
from database import init_db, query_db, execute_db
from app import create_app

def test_student_flow_for_mohaneni():
    print("==================================================================")
    print("  STUDENT WORKFLOW VERIFICATION FOR: mohaneni80@gmail.com")
    print("==================================================================")

    app = create_app()
    client = app.test_client()

    student_email = "mohaneni80@gmail.com"
    student_password = "SecurePassword123!"
    student_name = "Mohan Eni"
    student_phone = "9876543210"

    # Step 1: Cleanup any previous record for clean re-test
    print("\n--- STEP 1: CLEANUP & PREPARATION ---")
    prev_user = query_db("SELECT id FROM profiles WHERE email = ?", (student_email,), one=True)
    if prev_user:
        u_id = prev_user['id']
        print(f"Cleaning up previous profile records for {student_email} (ID: {u_id})")
        execute_db("DELETE FROM applications WHERE user_id = ?", (u_id,))
        execute_db("DELETE FROM profiles WHERE id = ?", (u_id,))
        execute_db("DELETE FROM password_resets WHERE email = ?", (student_email,))

    # Step 2: Register Account
    print("\n--- STEP 2: CREATE ACCOUNT (/api/auth/signup & /api/auth/register) ---")
    reg_payload = {
        'full_name': student_name,
        'email': student_email,
        'phone': student_phone,
        'phone_country_code': '+91',
        'password': student_password,
        'confirm_password': student_password,
        'terms_accepted': True,
        'marketing_opt_in': True
    }
    
    res = client.post('/api/auth/signup', json=reg_payload)
    print(f"POST /api/auth/signup -> Status: {res.status_code}, Response: {res.get_json()}")
    assert res.status_code == 200, f"Account creation failed: {res.get_json()}"

    auth_data = res.get_json()
    token = auth_data['token']
    user_id = auth_data['user']['id']
    headers = {'Authorization': f'Bearer {token}'}

    print(f"SUCCESS: Account created for {student_email} (User ID: {user_id})")

    # Step 3: Login User
    print("\n--- STEP 3: LOGIN USER (/api/auth/login) ---")
    login_res = client.post('/api/auth/login', json={
        'email': student_email,
        'password': student_password
    })
    print(f"POST /api/auth/login -> Status: {login_res.status_code}, Response: {login_res.get_json()}")
    assert login_res.status_code == 200, "Login failed!"

    # Step 4: Get User Profile
    print("\n--- STEP 4: FETCH USER PROFILE (/api/auth/me) ---")
    me_res = client.get('/api/auth/me', headers=headers)
    print(f"GET /api/auth/me -> Status: {me_res.status_code}, User: {me_res.get_json()}")
    assert me_res.status_code == 200, "Fetch profile failed!"

    # Step 5: Browse & Select Internship
    print("\n--- STEP 5: BROWSE INTERNSHIPS (/api/internships) ---")
    internships_res = client.get('/api/internships')
    print(f"GET /api/internships -> Status: {internships_res.status_code}")
    assert internships_res.status_code == 200, "Fetch internships failed!"
    
    internships_list = internships_res.get_json().get('internships', [])
    print(f"Found {len(internships_list)} available internships.")
    assert len(internships_list) > 0, "No internships available in database!"

    selected_internship = internships_list[0]
    int_id = selected_internship['id']
    int_slug = selected_internship['slug']
    int_title = selected_internship['title']
    print(f"Selected Internship: {int_title} (ID: {int_id}, Slug: {int_slug})")

    # Step 6: Internship Detail Page
    detail_res = client.get(f"/api/internships/{int_slug}")
    print(f"GET /api/internships/{int_slug} -> Status: {detail_res.status_code}")
    assert detail_res.status_code == 200, "Fetch internship detail failed!"

    # Step 7: Enroll in Internship & Generate Offer Letter
    print("\n--- STEP 7: ENROLL IN INTERNSHIP (/api/enrollments) ---")
    enroll_res = client.post('/api/enrollments', json={'internship_id': int_id}, headers=headers)
    print(f"POST /api/enrollments -> Status: {enroll_res.status_code}, Response: {enroll_res.get_json()}")
    assert enroll_res.status_code in [200, 201], "Enrollment failed!"

    app_record = enroll_res.get_json()['application']
    app_id = app_record['id']
    offer_letter_id = app_record['offer_letter_id']
    print(f"ENROLLED SUCCESSFULLY! App ID: {app_id}, Offer Letter ID: {offer_letter_id}")

    # Step 8: Verify Offer Letter PDF File
    expected_offer_file = os.path.join(Config.GENERATED_OFFERS_DIR, f"offer_{app_id}.pdf")
    print(f"Offer Letter PDF generated on disk: {expected_offer_file} (Exists: {os.path.exists(expected_offer_file)})")
    assert os.path.exists(expected_offer_file), "Offer letter PDF file missing!"

    # Step 9: Submit PDF Deliverable for Week 1
    print("\n--- STEP 9: SUBMIT PDF ASSIGNMENT DELIVERABLE (/api/submissions/upload) ---")
    dummy_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"

    for week in range(1, 5):
        data = {
            'application_id': app_id,
            'week_number': str(week),
            'file': (io.BytesIO(dummy_pdf_bytes), f"assignment_week_{week}_mohaneni.pdf")
        }
        sub_res = client.post('/api/submissions/upload', data=data, content_type='multipart/form-data', headers=headers)
        print(f"Week {week} PDF submission status: {sub_res.status_code}")
        assert sub_res.status_code == 201, f"Week {week} submission failed!"

        sub_id = sub_res.get_json()['submission']['id']

        # Admin grade submission
        admin_login = client.post('/api/auth/admin/login', json={'email': 'admin@webintern.com', 'password': 'admin123'})
        admin_token = admin_login.get_json()['token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}

        grade_res = client.post(f"/api/admin/submissions/{sub_id}/grade", json={
            'status': 'graded',
            'marks': 9.5,
            'max_marks': 10,
            'feedback': f"Great job on Week {week} submission, Mohan!"
        }, headers=admin_headers)
        assert grade_res.status_code == 200, f"Grading Week {week} failed!"
        print(f"Admin graded Week {week} assignment successfully!")

    # Step 10: Verify Certificate Job & Public Certificate Verification
    print("\n--- STEP 10: CERTIFICATE ISSUANCE & VERIFICATION (/api/verify/<id>) ---")
    from utils.certificate_job import process_eligible_certificates
    now_str = datetime.datetime.now().strftime("%B %d, %Y")
    execute_db("UPDATE applications SET end_date = ?, completion_status = 'eligible' WHERE id = ?", (now_str, app_id))

    issued = process_eligible_certificates()
    print(f"Certificates issued by job: {issued}")
    assert issued >= 1, "Certificate issuance job did not issue certificate!"

    cert_rec = query_db("SELECT * FROM certificates WHERE application_id = ?", (app_id,), one=True)
    assert cert_rec is not None, "Certificate record missing in DB!"
    cert_id = cert_rec['id'] if not cert_rec.get('certificate_id') else cert_rec.get('certificate_id')

    verify_res = client.get(f"/api/verify/{cert_id}")
    print(f"Public Verification GET /api/verify/{cert_id} -> Status: {verify_res.status_code}, Json: {verify_res.get_json()}")
    assert verify_res.status_code == 200 and verify_res.get_json()['status'] == 'VERIFIED', "Certificate verification failed!"

    print("\n==================================================================")
    print("  STUDENT WORKFLOW VERIFIED 100% SUCCESSFULLY FOR mohaneni80@gmail.com!")
    print("==================================================================")

if __name__ == '__main__':
    test_student_flow_for_mohaneni()
