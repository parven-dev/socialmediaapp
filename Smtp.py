import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


class MailServer:
    def __init__(self, otp, sender):
        self.otp = otp
        self.sender = sender
        load_dotenv()

    def smtp_server(self):
        email_user = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")

        if email_user is None or password is None:
            print("Email user or Password not set in Env")

        subject = "OTP For Verification"
        body = f"""
        Thank you for using Socialmediaapp
        Please find below your OTP
        OTP: {self.otp}
        """

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = self.sender
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), 587)
        server.starttls()
        server.login(email_user, password)

        text = msg.as_string()

        server.sendmail(email_user, self.sender, text)

        server.quit()
        return "mail sent"
