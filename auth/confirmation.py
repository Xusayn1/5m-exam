import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from core.db_settings import execute_query


def send_email(recipient_email: str, subject: str, body: str) -> bool:
    email_user: str = "sanjarbekwork@gmail.com"
    email_pass: str = "ukjc bzah lgvv qvxh"

    msg: MIMEMultipart = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server: Optional[smtplib.SMTP] = None
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")
        return False
    finally:
        if server:
            server.quit()


def generate_code(user_email: str) -> Optional[str]:
    delete_query: str = "DELETE FROM codes WHERE email = %s"
    execute_query(query=delete_query, params=(user_email,))

    code: str = str(random.randint(100000, 999999))

    insert_query: str = "INSERT INTO codes (email, code) VALUES (%s, %s)"
    params: tuple = (user_email, code)

    if execute_query(query=insert_query, params=params):
        print(f"Kod {user_email} manziliga yuborildi.")
        print(f"DEBUG: Tasdiqlash kodi -> {code}")
        return code

    print("Kodni saqlashda xatolik yuz berdi.")
    return None