"""Web-only login endpoints; use the global, unscoped DB dependency."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator
from sqlalchemy.orm import Session

from app import auth


class EmailCodeRequest(BaseModel):
    email: str
    intent: Literal["login", "register"] | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return auth.normalize_email(value)


class LoginRequest(EmailCodeRequest):
    model_config = ConfigDict(extra="forbid")
    code: str | None = Field(default=None, pattern=r"^\d{6}$")
    password: SecretStr | None = Field(default=None, min_length=8, max_length=128, repr=False)

    @model_validator(mode="after")
    def validate_credentials(self):
        supplied = self.model_fields_set & {"code", "password"}
        if len(supplied) != 1 or (self.code is None and self.password is None):
            raise ValueError("请选择密码或验证码登录")
        return self


class RegisterRequest(EmailCodeRequest):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(pattern=r"^\d{6}$")
    password: SecretStr = Field(min_length=8, max_length=128, repr=False)


class AuthUserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool


class AuthResponse(BaseModel):
    user: AuthUserResponse
    csrf_token: str


class EmailCodeResponse(BaseModel):
    message: str
    retry_after_seconds: int


class LogoutResponse(BaseModel):
    message: str


def _identity_response(user, session) -> AuthResponse:
    return AuthResponse(user=AuthUserResponse(id=user.id, email=user.email, is_admin=user.is_admin), csrf_token=session.csrf_token)


def _require_identity(db, request):
    auth.require_web_mode()
    identity = auth.authenticate_session(db, request)
    if identity is None:
        raise HTTPException(401, "请先登录")
    return identity


def register_auth_routes(app, get_db) -> None:
    @app.post("/api/v1/auth/email-code", response_model=EmailCodeResponse, status_code=202)
    def email_code(payload: EmailCodeRequest, request: Request, response: Response, db: Session = Depends(get_db)):
        retry_after = auth.issue_email_code(db, payload.email, request, payload.intent)
        response.headers["Cache-Control"] = "private, no-store"
        return EmailCodeResponse(message="验证码已发送，请检查邮箱", retry_after_seconds=retry_after)

    @app.post("/api/v1/auth/login", response_model=AuthResponse)
    def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
        if payload.password is not None:
            user, session, token = auth.create_password_login(db, payload.email, payload.password.get_secret_value(), request)
        else:
            user, session, token = auth.create_login(db, payload.email, payload.code, request)
        response.set_cookie(auth.SESSION_COOKIE, token, max_age=auth.get_settings().auth_session_days * 86400, secure=True, httponly=True, samesite="lax", path="/")
        response.headers["Cache-Control"] = "private, no-store"
        return _identity_response(user, session)

    @app.post("/api/v1/auth/register", response_model=AuthResponse)
    def register(payload: RegisterRequest, request: Request, response: Response, db: Session = Depends(get_db)):
        user, session, token = auth.create_login(db, payload.email, payload.code, request, register=True, password=payload.password.get_secret_value())
        response.set_cookie(auth.SESSION_COOKIE, token, max_age=auth.get_settings().auth_session_days * 86400, secure=True, httponly=True, samesite="lax", path="/")
        response.headers["Cache-Control"] = "private, no-store"
        return _identity_response(user, session)

    @app.get("/api/v1/auth/me", response_model=AuthResponse)
    def me(request: Request, response: Response, db: Session = Depends(get_db)):
        user, session = _require_identity(db, request)
        response.headers["Cache-Control"] = "private, no-store"
        return _identity_response(user, session)

    @app.post("/api/v1/auth/logout", response_model=LogoutResponse)
    def logout(request: Request, response: Response, db: Session = Depends(get_db)):
        _, session = _require_identity(db, request)
        auth.require_csrf(request, session)
        session.revoked_at = datetime.utcnow()
        db.commit()
        response.delete_cookie(auth.SESSION_COOKIE, path="/", secure=True, httponly=True, samesite="lax")
        response.headers["Cache-Control"] = "private, no-store"
        return LogoutResponse(message="已退出登录")
