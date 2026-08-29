import resend
from config import Config

if Config.RESEND_API_KEY and not Config.RESEND_API_KEY.startswith("re_demo"):
    resend.api_key = Config.RESEND_API_KEY

def send_otp_email(to_email, otp_code, purpose='login'):
    subject = f"Web Intern - Your Verification Code is {otp_code}"
    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; background-color: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #0B3D91; margin: 0; font-size: 24px;">web<span style="color: #2E7DFF;">intern</span></h2>
            <p style="color: #4B5563; font-size: 14px; margin-top: 4px;">Virtual Internship Platform</p>
        </div>
        <hr style="border: none; border-top: 1px solid #DCE6F5; margin: 20px 0;" />
        <h3 style="color: #082B66; font-size: 18px; margin-bottom: 12px;">Your One-Time Code</h3>
        <p style="color: #4B5563; line-height: 1.5;">Use the following 6-digit code to complete your {purpose}:</p>
        <div style="text-align: center; margin: 24px 0;">
            <span style="font-size: 32px; font-weight: 700; letter-spacing: 6px; color: #0B3D91; background: #EAF1FB; padding: 12px 28px; border-radius: 8px; display: inline-block;">
                {otp_code}
            </span>
        </div>
        <p style="color: #4B5563; font-size: 13px;">This verification code is valid for 10 minutes. Do not share this code with anyone.</p>
        <hr style="border: none; border-top: 1px solid #DCE6F5; margin: 20px 0;" />
        <p style="color: #9CA3AF; font-size: 12px; text-align: center;">© 2026 Web Intern. Secure Automated Verification System.</p>
    </div>
    """
    
    return _dispatch_email(to_email, subject, html_content)

def send_offer_letter_email(to_email, student_name, internship_title, pdf_bytes=None):
    subject = f"Official Offer Letter - {internship_title} at Web Intern"
    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; background-color: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #0B3D91; margin: 0; font-size: 26px;">web<span style="color: #2E7DFF;">intern</span></h2>
        </div>
        <h3 style="color: #082B66; font-size: 20px;">Congratulations, {student_name}! 🎉</h3>
        <p style="color: #4B5563; line-height: 1.6;">We are thrilled to accept your application for the <strong>{internship_title}</strong> at Web Intern.</p>
        <p style="color: #4B5563; line-height: 1.6;">Your 4-week virtual internship program is now active on your student dashboard. Access your weekly tasks, submit deliverables, and track your progress live.</p>
        <div style="text-align: center; margin: 24px 0;">
            <a href="http://localhost:5000/#/dashboard" style="background-color: #0B3D91; color: #FFFFFF; text-decoration: none; padding: 12px 28px; border-radius: 24px; font-weight: 600; display: inline-block;">Go to Student Dashboard →</a>
        </div>
        <p style="color: #4B5563; font-size: 13px;">Your official Internship Offer Letter is generated and available in your portal.</p>
    </div>
    """
    return _dispatch_email(to_email, subject, html_content)

def send_feedback_email(to_email, student_name, week_number, status, feedback_text):
    status_color = "#10B981" if status == "approved" else "#F59E0B"
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

def _dispatch_email(to_email, subject, html_content):
    if Config.RESEND_API_KEY and not Config.RESEND_API_KEY.startswith("re_demo"):
        try:
            params = {
                "from": "Web Intern <notifications@webintern.com>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }
            email_res = resend.Emails.send(params)
            return True, email_res
        except Exception as e:
            print(f"[Resend Email Error]: {e}")
            return False, str(e)
    else:
        print(f"\n================ [MOCK EMAIL DISPATCH] ================")
        print(f"TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print(f"=======================================================\n")
        return True, "Mock email logged to console"
