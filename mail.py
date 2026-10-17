import logging
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()

log = logging.getLogger(__name__)

MAIL_HOST = os.environ.get("MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "465"))  # env values are strings
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


def mail_is_configured() -> bool:
    """True only if both the sender address and password are set and non-empty."""
    return all([MAIL_USER, MAIL_PASSWORD])


def build_estimate_body(low, high) -> str:
    """Plain-text email body. low/high are None when the yard needs a site visit."""
    if low is None or high is None:
        return (
            "Thanks for your interest!\n\n"
            "Based on what you told us, we'd like to take a quick look at your "
            "yard before giving a price. Reply to this email and we'll schedule "
            "a free visit.\n"
        )
    return (
        "Thanks for your interest!\n\n"
        f"Your estimated price range is ${low:,} to ${high:,}.\n\n"
        "This is an estimate, not a final quote. The final price is confirmed "
        "once we review your request.\n"
    )


def send_email(to_address: str, body: str, subject: str = "Your landscaping estimate") -> bool:
    """Send a plain-text email. Returns True only if the server accepted it."""
    if not mail_is_configured():
        log.error("Email not sent: MAIL_USER / MAIL_PASSWORD are not set")
        return False

    try:
        msg = EmailMessage()
        msg["From"] = MAIL_USER
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.set_content(body)
    except ValueError:
        # EmailMessage rejects header values containing newlines
        log.exception("Email not sent: invalid header value")
        return False

    try:
        with smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT, timeout=10) as server:
            server.login(MAIL_USER, MAIL_PASSWORD)
            server.send_message(msg)
        return True
    except smtplib.SMTPAuthenticationError:
        log.exception("Email not sent: login rejected (check MAIL_USER / app password)")
    except smtplib.SMTPRecipientsRefused:
        log.exception("Email not sent: recipient address was rejected")
    except (smtplib.SMTPException, OSError):
        log.exception("Email not sent: SMTP or network error")
    return False
