import base64
import requests
from config import Config

def _get_resend_key():
    return (Config.RESEND_API_KEY or "").strip()

def _dispatch_email(to_email, subject, html_content, attachments=None):
    api_key = _get_resend_key()
    from_email = getattr(Config, 'RESEND_FROM_EMAIL', 'notifications@webintern.in') or 'notifications@webintern.in'
    
    if api_key and not api_key.startswith("re_demo") and api_key not in ["", "your_resend_api_key"]:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": f"Web Intern <{from_email}>",
            "to": [to_email] if isinstance(to_email, str) else to_email,
            "subject": subject,
            "html": html_content
        }
        
        if attachments:
            payload["attachments"] = attachments
            
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=5)
            if res.status_code in [200, 201]:
                data = res.json()
                print(f"[Resend Email Success]: Sent to {to_email}, ID: {data.get('id')}")
                return True, data
            else:
                err_body = res.text
                print(f"[Resend Email Error HTTP {res.status_code}]: {err_body}")
                return False, f"Resend API error ({res.status_code}): {err_body}"
        except Exception as e:
            print(f"[Resend Email Exception]: {e}. Falling back to mock dispatch.")
            return True, {"id": "resend_offline_msg_id_123", "status": "queued_offline"}
    else:
        print(f"\n================ [MOCK EMAIL DISPATCH] ================")
        print(f"TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print(f"=======================================================\n")
        return True, {"id": "mock_msg_id_12345", "status": "mock_sent"}

def send_forgot_password_email(to_email, reset_link=None, reset_code=None):
    subject = "Web Intern - Password Reset Request"
    if not reset_link:
        reset_link = "https://webintern.in/#/reset-password"
    
    code_html = f"""
        <div style="text-align: center; margin: 24px 0;">
            <span style="font-size: 28px; font-weight: 700; letter-spacing: 4px; color: #0B3D91; background: #EAF1FB; padding: 12px 24px; border-radius: 8px; display: inline-block;">
                {reset_code}
            </span>
        </div>
    """ if reset_code else ""

    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; background-color: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #0B3D91; margin: 0; font-size: 24px;">web<span style="color: #2E7DFF;">intern</span></h2>
            <p style="color: #4B5563; font-size: 14px; margin-top: 4px;">Virtual Internship Platform</p>
        </div>
        <hr style="border: none; border-top: 1px solid #DCE6F5; margin: 20px 0;" />
        <h3 style="color: #082B66; font-size: 18px; margin-bottom: 12px;">Password Reset Request</h3>
        <p style="color: #4B5563; line-height: 1.5;">We received a request to reset your password for your Web Intern account.</p>
        {code_html}
        <div style="text-align: center; margin: 24px 0;">
            <a href="{reset_link}" style="background-color: #0B3D91; color: #FFFFFF; text-decoration: none; padding: 12px 28px; border-radius: 24px; font-weight: 600; display: inline-block;">Reset Password →</a>
        </div>
        <p style="color: #4B5563; font-size: 13px;">If you did not request a password reset, you can safely ignore this email.</p>
        <hr style="border: none; border-top: 1px solid #DCE6F5; margin: 20px 0;" />
        <p style="color: #9CA3AF; font-size: 12px; text-align: center;">© 2026 Web Intern. Secure Automated Verification System.</p>
    </div>
    """
    return _dispatch_email(to_email, subject, html_content)

def send_offer_letter_email(to_email, student_name, internship_title, pdf_bytes=None, start_date=None, end_date=None, duration="4 Weeks", offer_id=None):
    subject = "Your WebIntern Internship Offer Letter"
    eff_start = start_date or "Immediate"
    eff_end = end_date or "4 Weeks from Start Date"
    eff_offer_id = offer_id or "WI-OFFER-2026"

    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; background-color: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #0B3D91; margin: 0; font-size: 26px;">web<span style="color: #2E7DFF;">intern</span></h2>
        </div>
        <p style="color: #4B5563;">Dear <strong>{student_name}</strong>,</p>
        <p style="color: #4B5563; font-weight: 600;">Congratulations!</p>
        <p style="color: #4B5563; line-height: 1.6;">Your internship enrollment with WebIntern has been confirmed.</p>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin: 16px 0; color: #334155;">
            <p style="margin: 4px 0;"><strong>Internship:</strong> {internship_title}</p>
            <p style="margin: 4px 0;"><strong>Start Date:</strong> {eff_start}</p>
            <p style="margin: 4px 0;"><strong>End Date:</strong> {eff_end}</p>
            <p style="margin: 4px 0;"><strong>Duration:</strong> {duration}</p>
            <p style="margin: 4px 0;"><strong>Offer ID:</strong> {eff_offer_id}</p>
        </div>
        <p style="color: #4B5563;">Your Offer Letter is attached to this email. You can also view it from your WebIntern dashboard.</p>
        <div style="text-align: center; margin: 24px 0;">
            <a href="https://webintern.in/#/dashboard" style="background-color: #0B3D91; color: #FFFFFF; text-decoration: none; padding: 12px 28px; border-radius: 24px; font-weight: 600; display: inline-block;">Go to Dashboard →</a>
        </div>
        <p style="color: #64748B; font-size: 13px;">Regards,<br/>WebIntern Team</p>
    </div>
    """
    
    attachments = None
    if pdf_bytes:
        encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        attachments = [{
            "filename": f"Offer_Letter_{eff_offer_id}.pdf",
            "content": encoded_pdf
        }]

    return _dispatch_email(to_email, subject, html_content, attachments=attachments)

def send_certificate_email(to_email, student_name, internship_title, cert_id, pdf_bytes=None, start_date=None, end_date=None, verification_url=None):
    subject = "Your WebIntern Internship Completion Certificate"
    eff_start = start_date or "N/A"
    eff_end = end_date or "N/A"
    eff_verify_url = verification_url or f"https://webintern.in/verify/{cert_id}"

    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; background-color: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #0B3D91; margin: 0; font-size: 26px;">web<span style="color: #2E7DFF;">intern</span></h2>
        </div>
        <p style="color: #4B5563;">Dear <strong>{student_name}</strong>,</p>
        <p style="color: #4B5563; font-weight: 600;">Congratulations on successfully completing your internship with WebIntern.</p>
        <p style="color: #4B5563; line-height: 1.6;">Your Internship Completion Certificate has been issued.</p>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin: 16px 0; color: #334155;">
            <p style="margin: 4px 0;"><strong>Certificate ID:</strong> {cert_id}</p>
            <p style="margin: 4px 0;"><strong>Internship:</strong> {internship_title}</p>
            <p style="margin: 4px 0;"><strong>Start Date:</strong> {eff_start}</p>
            <p style="margin: 4px 0;"><strong>End Date:</strong> {eff_end}</p>
        </div>
        <p style="color: #4B5563;">Your certificate is attached to this email. You can also access it from your WebIntern dashboard.</p>
        <p style="color: #4B5563;"><strong>Certificate Verification:</strong> <a href="{eff_verify_url}" style="color: #2E7DFF;">{eff_verify_url}</a></p>
        <div style="text-align: center; margin: 24px 0;">
            <a href="{eff_verify_url}" style="background-color: #0B3D91; color: #FFFFFF; text-decoration: none; padding: 12px 28px; border-radius: 24px; font-weight: 600; display: inline-block;">Verify Certificate →</a>
        </div>
        <p style="color: #64748B; font-size: 13px;">Regards,<br/>WebIntern Team</p>
    </div>
    """

    attachments = None
    if pdf_bytes:
        encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        attachments = [{
            "filename": f"WebIntern_Certificate_{cert_id}.pdf",
            "content": encoded_pdf
        }]

    return _dispatch_email(to_email, subject, html_content, attachments=attachments)

def send_feedback_email(to_email, student_name, week_number, status, feedback_text):
    status_color = "#10B981" if status in ["approved", "graded"] else "#F59E0B"
    subject = f"Task Week {week_number} Evaluation Update - Web Intern"
    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 550px; margin: 0 auto; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; background-color: #FFFFFF;">
        <h3 style="color: #082B66;">Task Evaluation Result</h3>
        <p style="color: #4B5563;">Hello <strong>{student_name}</strong>,</p>
        <p style="color: #4B5563;">Your submission for <strong>Week {week_number}</strong> has been reviewed:</p>
        <div style="padding: 16px; border-radius: 8px; background: #F8F9FA; border-left: 4px solid {status_color}; margin: 16px 0;">
            <p style="margin: 0; font-weight: 600; color: {status_color}; text-transform: uppercase; font-size: 13px;">Status: {status}</p>
            <p style="margin: 8px 0 0 0; color: #4B5563;">{feedback_text}</p>
        </div>
        <p style="color: #4B5563;">Log in to your student workspace to view complete details or proceed to the next module.</p>
    </div>
    """
    return _dispatch_email(to_email, subject, html_content)

def send_welcome_newsletter(to_email):
    subject = "Welcome to Web Intern Newsletter!"
    html_content = """
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 24px;">
        <h2 style="color: #0B3D91;">web<span style="color: #2E7DFF;">intern</span></h2>
        <h3>Thank you for subscribing!</h3>
        <p style="color: #4B5563;">You will now receive weekly career tips, newly launched virtual internships, and industry insights straight to your inbox.</p>
    </div>
    """
    return _dispatch_email(to_email, subject, html_content)
