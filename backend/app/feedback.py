"""Save website feedback before attempting the existing SMTP notification."""
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import ssl
from threading import Lock

from fastapi import HTTPException
from sqlalchemy import func, select

from app.auth import _client_hash, _secret, authenticate_session, require_origin, require_web_mode
from app.config import get_settings
from app.feedback_models import WebFeedback

_FEEDBACK_LOCK = Lock()


def send_feedback_notification(item, settings) -> bool:
    if not settings.auth_admin_email.strip() or not settings.auth_smtp_host or not settings.auth_smtp_from:
        return False
    message = EmailMessage()
    message["From"] = settings.auth_smtp_from
    message["To"] = settings.auth_admin_email.strip()
    message["Subject"] = "能研智助网站意见反馈"
    message.set_content(f"反馈编号：{item.id}\n\n{item.message}\n\n联系方式：{item.contact or '未提供'}")
    smtp_class = smtplib.SMTP_SSL if settings.auth_smtp_ssl else smtplib.SMTP
    kwargs = {"timeout": 15}
    if settings.auth_smtp_ssl:
        kwargs["context"] = ssl.create_default_context()
    with smtp_class(settings.auth_smtp_host, settings.auth_smtp_port, **kwargs) as smtp:
        if settings.auth_smtp_starttls and not settings.auth_smtp_ssl:
            smtp.starttls(context=ssl.create_default_context())
        if settings.auth_smtp_username:
            smtp.login(settings.auth_smtp_username, _secret(settings.auth_smtp_password))
        smtp.send_message(message)
    return True


def save_feedback(db, request, message: str, contact: str | None) -> bool:
    settings = get_settings()
    require_web_mode(settings)
    require_origin(request, settings)
    client_hash = _client_hash(request, settings)
    identity = authenticate_session(db, request)
    # Reserve the durable record under the same single-worker model as auth.
    with _FEEDBACK_LOCK:
        now = datetime.utcnow()
        count = db.scalar(select(func.count()).select_from(WebFeedback).where(
            WebFeedback.client_hash == client_hash,
            WebFeedback.created_at >= now - timedelta(hours=1),
        ))
        if count >= 5:
            raise HTTPException(429, "提交过于频繁，请一小时后重试", headers={"Retry-After": "3600"})
        item = WebFeedback(message=message, contact=contact, client_hash=client_hash,
                           user_id=identity[0].id if identity else None, created_at=now)
        db.add(item)
        db.commit()
    try:
        sent = send_feedback_notification(item, settings)
    except Exception:
        # Never return SMTP exception text, credentials or user feedback in logs.
        sent = False
    if sent:
        item.notified_at = datetime.utcnow()
        db.commit()
    return sent
