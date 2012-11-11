import smtplib
from email.mime.text import MIMEText

class emails():
    """Handling of sending emails"""

    def __init__(self):
        self.ouremail = "noreply@rpitutortime.com"
        self.smtp = smtplib.SMTP('localhost')

    def __del__(self):
        self.smtp.quit()
        
    def send_email(self, user, msg, subject):
        """Send the email address in the user object an email
           The content of this email is msg.
           Subject must not be null. This way we pass more spam filters"""

        payload = MIMEText(msg)
        payload['From'] = self.ouremail
        payload['To'] = user.email
        payload['Subject'] = subject 
        self.smtp.sendmail(self.ouremail, [user.email], payload.as_string())