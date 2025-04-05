import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import BackgroundTasks

from dotenv import load_dotenv
from src.services.auth import create_email_token

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def _build_verification_link(email: str) -> str:
    token = create_email_token(email)
    return f"{BACKEND_URL}/users/confirm-email/{token}"


def _build_email_content(email: str) -> MIMEMultipart:
    link = _build_verification_link(email)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your email"
    msg["From"] = EMAIL_USER
    msg["To"] = email

    html = f"""
    <html>
        <body>
            <p>Hi!<br>
               Please confirm your email by clicking on the link below:<br>
               <a href="{link}">Confirm Email</a>
            </p>
        </body>
    </html>
    """
    part = MIMEText(html, "html")
    msg.attach(part)
    return msg


def send_verification_email_sync(email: str):
    msg = _build_email_content(email)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, email, msg.as_string())


def send_verification_email(background_tasks: BackgroundTasks, email: str):
    background_tasks.add_task(send_verification_email_sync, email)
