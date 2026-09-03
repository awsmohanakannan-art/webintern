import os
import requests
import json
import threading
from config import Config
from database import execute_db

def sync_offer_letter_to_google_sheets(offer_payload, document_id=None):
    """Asynchronously sync Offer Letter record to Google Sheets webhook without blocking user workflow."""
    def _do_sync():
        webhook_url = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL", "")
        if not webhook_url:
            print("[Google Sheets Sync Note]: GOOGLE_SHEETS_WEBHOOK_URL not configured. Skipping remote sync.")
            return

        payload = {
            "type": "OFFER_LETTER",
            "offerId": offer_payload.get("offer_id"),
            "studentId": offer_payload.get("student_id"),
            "studentName": offer_payload.get("student_name"),
            "email": offer_payload.get("email"),
            "mobile": offer_payload.get("mobile", ""),
            "collegeName": offer_payload.get("college", ""),
            "course": offer_payload.get("course_name"),
            "internshipRole": offer_payload.get("role"),
            "company": offer_payload.get("company", "Web Intern Platform"),
            "startDate": offer_payload.get("start_date"),
            "endDate": offer_payload.get("end_date"),
            "duration": offer_payload.get("duration", "4 Weeks"),
            "location": offer_payload.get("location", "Virtual / Remote"),
            "issueDate": offer_payload.get("issue_date"),
            "documentStatus": offer_payload.get("document_status", "ISSUED"),
            "emailStatus": offer_payload.get("email_status", "SENT"),
            "emailMessageId": offer_payload.get("email_message_id", "")
        }

        try:
            res = requests.post(webhook_url, json=payload, timeout=10)
            if res.status_code == 200:
                print(f"[Google Sheets Sync Success]: Offer Letter {offer_payload.get('offer_id')}")
                if document_id:
                    execute_db("UPDATE documents SET sheets_synced = 1, sheets_error = NULL WHERE id = ?", (document_id,))
            else:
                err_msg = f"HTTP {res.status_code}: {res.text}"
                print(f"[Google Sheets Sync Warning]: {err_msg}")
                if document_id:
                    execute_db("UPDATE documents SET sheets_synced = 0, sheets_error = ? WHERE id = ?", (err_msg, document_id))
        except Exception as e:
            print(f"[Google Sheets Sync Failure]: {e}")
            if document_id:
                execute_db("UPDATE documents SET sheets_synced = 0, sheets_error = ? WHERE id = ?", (str(e), document_id))

    threading.Thread(target=_do_sync, daemon=True).start()

def sync_certificate_to_google_sheets(cert_payload, document_id=None):
    """Asynchronously sync Certificate record to Google Sheets webhook without blocking user workflow."""
    def _do_sync():
        webhook_url = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL", "")
        if not webhook_url:
            print("[Google Sheets Sync Note]: GOOGLE_SHEETS_WEBHOOK_URL not configured. Skipping remote sync.")
            return

        payload = {
            "type": "CERTIFICATE",
            "certificateId": cert_payload.get("certificate_id"),
            "studentId": cert_payload.get("student_id"),
            "studentName": cert_payload.get("student_name"),
            "email": cert_payload.get("email"),
            "collegeName": cert_payload.get("college", ""),
            "course": cert_payload.get("course_name"),
            "internshipRole": cert_payload.get("role"),
            "company": cert_payload.get("company", "Web Intern Platform"),
            "startDate": cert_payload.get("start_date"),
            "endDate": cert_payload.get("end_date"),
            "duration": cert_payload.get("duration", "4 Weeks"),
            "guideName": cert_payload.get("guide_name", "Dr. A. K. Sharma"),
            "projectName": cert_payload.get("project_name", "Enterprise Capstone"),
            "certificateDate": cert_payload.get("issue_date"),
            "issueDate": cert_payload.get("issue_date"),
            "documentStatus": cert_payload.get("document_status", "ISSUED"),
            "emailStatus": cert_payload.get("email_status", "SENT"),
            "emailMessageId": cert_payload.get("email_message_id", ""),
            "verificationUrl": cert_payload.get("verification_url", "")
        }

        try:
            res = requests.post(webhook_url, json=payload, timeout=10)
            if res.status_code == 200:
                print(f"[Google Sheets Sync Success]: Certificate {cert_payload.get('certificate_id')}")
                if document_id:
                    execute_db("UPDATE documents SET sheets_synced = 1, sheets_error = NULL WHERE id = ?", (document_id,))
            else:
                err_msg = f"HTTP {res.status_code}: {res.text}"
                print(f"[Google Sheets Sync Warning]: {err_msg}")
                if document_id:
                    execute_db("UPDATE documents SET sheets_synced = 0, sheets_error = ? WHERE id = ?", (err_msg, document_id))
        except Exception as e:
            print(f"[Google Sheets Sync Failure]: {e}")
            if document_id:
                execute_db("UPDATE documents SET sheets_synced = 0, sheets_error = ? WHERE id = ?", (str(e), document_id))

    threading.Thread(target=_do_sync, daemon=True).start()
