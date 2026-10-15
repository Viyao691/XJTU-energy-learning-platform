"""Email verification and opaque, revocable server-side web sessions."""
from __future__ import annotations

import hashlib
import hmac
import ipaddress
import re
import secrets
import smtplib
import ssl
import threading
from typing import Literal
from datetime import datetime, timedelta
from email.message import EmailMessage

from fastapi import HTTPException, Request
from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from app.auth_models import WebEmailCode, WebPasswordFailure, WebSession, WebUser
from app.config import get_settings

SESSION_COOKIE = "__Host-energy-session"
_AUTH_LOCK = threading.Lock()
PASSWORD_ITERATIONS = 600_000
PASSWORD_WINDOW_SECONDS = 900
PASSWORD_EMAIL_ATTEMPTS = 5
PASSWORD_CLIENT_ATTEMPTS = 20
_DUMMY_PASSWORD_HASH = f"pbkdf2_sha256${PASSWORD_ITERATIONS}${'00' * 16}${'00' * 32}"
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}\Z")


def normalize_email(value: str) -> str:
    email = value.strip().lower()
    if len(email) > 254 or len(email.split("@", 1)[0]) > 64 or not _EMAIL_PATTERN.fullmatch(email):
        raise ValueError("请输入有效邮箱地址")
    return email


def _secret(value) -> str:
    return value.get_secret_value() if hasattr(value, "get_secret_value") else str(value)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def hash_password(password: str) -> str:
    # OWASP PBKDF2-HMAC-SHA256 work factor; salt is unique for each registration.
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PASSWORD_ITERATIONS)
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str | None) -> bool:
    _, iterations, salt, expected = (stored or _DUMMY_PASSWORD_HASH).split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(iterations))
    matches = hmac.compare_digest(digest.hex(), expected)
    return stored is not None and matches


def _client_hash(request: Request, settings) -> str:
    client = request.client.host if request.client else "unknown"
    # Enabled only behind the private API and Caddy's overwritten custom header.
    if settings.auth_trust_proxy:
        try:
            client = str(ipaddress.ip_address(request.headers.get("x-energy-client-ip", "")))
        except ValueError:
            pass
    return _hash(client)


def _code_hash(email: str, code: str, settings) -> str:
    key = _secret(settings.auth_code_secret)
    if not key:
        raise HTTPException(503, "邮箱登录尚未配置")
    return hmac.new(key.encode(), f"{email}:{code}".encode(), hashlib.sha256).hexdigest()


def require_web_mode(settings=None) -> None:
    settings = settings or get_settings()
    if not settings.web_mode:
        raise HTTPException(404, "Not Found")


def require_origin(request: Request, settings=None) -> None:
    settings = settings or get_settings()
    if not settings.web_origin or request.headers.get("origin") != settings.web_origin:
        raise HTTPException(403, "请求来源不允许")


def require_csrf(request: Request, session: WebSession | None = None, settings=None) -> None:
    require_origin(request, settings)
    session = session or getattr(request.state, "auth_session", None)
    supplied = request.headers.get("x-csrf-token", "")
    if session is None or not supplied.isascii() or not hmac.compare_digest(supplied, session.csrf_token):
        raise HTTPException(403, "登录校验已失效，请刷新后重试")


def send_email_code(email: str, code: str, settings) -> None:
    if not settings.auth_smtp_host or not settings.auth_smtp_from:
        raise HTTPException(503, "邮箱登录尚未配置")
    message = EmailMessage()
    message["From"] = settings.auth_smtp_from
    message["To"] = email
    message["Subject"] = "储能科研智慧平台账号验证码"
    message.set_content(f"你的账号验证码是：{code}\n有效期 {settings.auth_code_ttl_seconds // 60} 分钟。请勿向他人透露。")
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


def _account_for_intent(db: Session, email: str, intent: Literal["login", "register"] | None) -> WebUser | None:
    user = db.scalar(select(WebUser).where(WebUser.email == email))
    if intent == "login" and user is None:
        raise HTTPException(400, "该邮箱尚未注册，请先注册")
    if intent == "register" and user is not None:
        raise HTTPException(409, "该邮箱已注册，请直接登录")
    return user


def issue_email_code(db: Session, email: str, request: Request, intent: Literal["login", "register"] | None = None) -> int:
    settings = get_settings()
    require_web_mode(settings)
    require_origin(request, settings)
    now = datetime.utcnow()
    client_hash = _client_hash(request, settings)
    code = f"{secrets.randbelow(1_000_000):06d}"
    digest = _code_hash(email, code, settings)
    # Single API worker; reserve the durable send before releasing the lock.
    with _AUTH_LOCK:
        _account_for_intent(db, email, intent)
        latest = db.scalar(select(WebEmailCode).where(WebEmailCode.email == email).order_by(WebEmailCode.id.desc()).limit(1))
        cutoff = now - timedelta(hours=1)
        email_count = db.scalar(select(func.count()).select_from(WebEmailCode).where(WebEmailCode.email == email, WebEmailCode.created_at >= cutoff))
        client_count = db.scalar(select(func.count()).select_from(WebEmailCode).where(WebEmailCode.client_hash == client_hash, WebEmailCode.created_at >= cutoff))
        if (latest and (now - latest.created_at).total_seconds() < settings.auth_code_resend_seconds) or email_count >= settings.auth_code_hourly_limit or client_count >= settings.auth_client_hourly_limit:
            raise HTTPException(429, "发送过于频繁，请稍后重试", headers={"Retry-After": str(settings.auth_code_resend_seconds)})
        db.execute(update(WebEmailCode).where(WebEmailCode.email == email, WebEmailCode.consumed_at.is_(None)).values(consumed_at=now))
        record = WebEmailCode(email=email, client_hash=client_hash, code_hash=digest, created_at=now, expires_at=now + timedelta(seconds=settings.auth_code_ttl_seconds), attempts=0)
        db.add(record)
        db.commit()
        record_id = record.id
    try:
        send_email_code(email, code, settings)
    except Exception:
        db.execute(update(WebEmailCode).where(WebEmailCode.id == record_id).values(consumed_at=datetime.utcnow()))
        db.commit()
        raise HTTPException(503, "验证码发送失败，请稍后重试") from None
    return settings.auth_code_resend_seconds


def _create_session(db: Session, user: WebUser, request: Request, settings, now: datetime) -> tuple[WebUser, WebSession, str]:
    old_token = request.cookies.get(SESSION_COOKIE)
    if old_token:
        db.execute(update(WebSession).where(WebSession.token_hash == _hash(old_token)).values(revoked_at=now))
    token = secrets.token_urlsafe(32)
    session = WebSession(user_id=user.id, token_hash=_hash(token), csrf_token=secrets.token_urlsafe(32), created_at=now, expires_at=now + timedelta(days=settings.auth_session_days))
    db.add(session)
    db.commit()
    db.refresh(user)
    db.refresh(session)
    return user, session, token


def create_password_login(db: Session, email: str, password: str, request: Request) -> tuple[WebUser, WebSession, str]:
    settings = get_settings()
    require_web_mode(settings)
    require_origin(request, settings)
    email_hash, client_hash = _hash(email), _client_hash(request, settings)
    # Match the email-code flow's single API worker and durable failure records.
    with _AUTH_LOCK:
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=PASSWORD_WINDOW_SECONDS)
        db.execute(delete(WebPasswordFailure).where(WebPasswordFailure.created_at <= cutoff))
        email_failures = db.scalar(select(func.count()).select_from(WebPasswordFailure).where(WebPasswordFailure.email_hash == email_hash))
        client_failures = db.scalar(select(func.count()).select_from(WebPasswordFailure).where(WebPasswordFailure.client_hash == client_hash))
        if email_failures >= PASSWORD_EMAIL_ATTEMPTS or client_failures >= PASSWORD_CLIENT_ATTEMPTS:
            db.commit()
            raise HTTPException(429, "登录尝试过于频繁，请稍后重试或使用验证码登录", headers={"Retry-After": str(PASSWORD_WINDOW_SECONDS)})
        user = db.scalar(select(WebUser).where(WebUser.email == email))
        if not _verify_password(password, user.password_hash if user else None):
            db.add(WebPasswordFailure(email_hash=email_hash, client_hash=client_hash, created_at=now))
            db.commit()
            raise HTTPException(401, "邮箱或密码错误，请重试或使用验证码登录")
        return _create_session(db, user, request, settings, now)


def create_login(db: Session, email: str, code: str, request: Request, *, register: bool = False, password: str | None = None) -> tuple[WebUser, WebSession, str]:
    settings = get_settings()
    require_web_mode(settings)
    require_origin(request, settings)
    now = datetime.utcnow()
    expected = _code_hash(email, code, settings)
    with _AUTH_LOCK:
        user = _account_for_intent(db, email, "register" if register else "login")
        record = db.scalar(select(WebEmailCode).where(WebEmailCode.email == email).order_by(WebEmailCode.id.desc()).limit(1))
        if record is None or record.consumed_at is not None or record.expires_at <= now or record.attempts >= settings.auth_code_max_attempts:
            raise HTTPException(400, "验证码错误或已失效")
        record.attempts += 1
        if not hmac.compare_digest(record.code_hash, expected):
            db.commit()
            raise HTTPException(400, "验证码错误或已失效")
        record.consumed_at = now
        if register:
            user = WebUser(email=email, password_hash=hash_password(password), created_at=now, verified_at=now)
            db.add(user)
            db.flush()
        return _create_session(db, user, request, settings, now)


def authenticate_session(db: Session, request: Request) -> tuple[WebUser, WebSession] | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token or len(token) > 128:
        return None
    session = db.scalar(select(WebSession).where(WebSession.token_hash == _hash(token), WebSession.revoked_at.is_(None), WebSession.expires_at > datetime.utcnow()))
    if session is None:
        return None
    user = db.get(WebUser, session.user_id)
    if user is None:
        return None
    return user, session


def authenticate(request: Request, session_factory) -> WebUser | None:
    with session_factory() as db:
        identity = authenticate_session(db, request)
        if identity is None:
            return None
        user, session = identity
        request.state.user = user
        request.state.auth_session = session
        return user
