import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()


def send_email(email: str, body: str):
    password = os.environ.get("email_password")
    if password == None:
        return
    try:
        msg = EmailMessage()
        msg["from"] = "yoel7501@gmail.com"
        msg["to"] = email
        msg["Subject"] = "your quote from landscaping"
        msg.set_content(body)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login("yoel7501@gmail.com", password)
            server.send_message(msg)
            print("success")
    except smtplib.SMTPAuthenticationError:
        print("wrong username or password")
    except smtplib.SMTPRecipientsRefused:
        print("the address was rejected")
    except smtplib.SMTPException:
        print("parent class")
    except OSError:
        print("dns error or other")
