from datetime import datetime, timedelta
from typing import Any, Union

from passlib.context import CryptContext
import logging
from app.config import settings
import json
import emails
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger

logger = get_logger(__name__)

def send_email(
    subject: str = "",
    content: str = "",
 ) -> None:
    if not settings.SMTP_HOST or \
        not settings.SMTP_PORT or \
        not settings.SMTP_USER or \
        not settings.SMTP_PASSWORD:
        return False
    message = emails.Message(
        subject=subject,                              
        html=content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )   
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=settings.EMAIL_TO, smtp=smtp_options)
    logger.info(f"send email result: {response}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def flat_object(data):
    flat_obj = {}
    for k, v in data.items():
        if k == '_links':
            k = 'links'
        if isinstance(v, list):
            flat_obj[k] = json.dumps(v)
        elif isinstance(v, dict):
            _flat_obj = flat_object(v)
            for kk, vv in _flat_obj.items():
                flat_obj[f'{k}_{kk}'] = vv
        else:
            if k == 'self':
                k = 'self_'
            if v is not None:
                flat_obj[k] = v
    return flat_obj