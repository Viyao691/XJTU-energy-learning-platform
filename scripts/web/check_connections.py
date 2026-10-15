"""Verify TLS/authentication without sending mail or generating paid tokens."""
import json
import smtplib
import ssl

import httpx
from app.config import get_settings
from app.secrets import get_model_api_key

settings = get_settings()
result = {}
try:
    kwargs = {"timeout": 20}
    if settings.auth_smtp_ssl:
        kwargs["context"] = ssl.create_default_context()
    smtp_class = smtplib.SMTP_SSL if settings.auth_smtp_ssl else smtplib.SMTP
    with smtp_class(settings.auth_smtp_host, settings.auth_smtp_port, **kwargs) as smtp:
        if settings.auth_smtp_starttls and not settings.auth_smtp_ssl:
            smtp.starttls(context=ssl.create_default_context())
        smtp.login(settings.auth_smtp_username, settings.auth_smtp_password.get_secret_value())
    result["smtp_tls_auth"] = True
except (OSError, smtplib.SMTPException):
    result["smtp_tls_auth"] = False
try:
    response = httpx.get(settings.model_base_url.rstrip("/") + "/models", headers={"Authorization": "Bearer " + get_model_api_key(settings.model_provider, settings.model_base_url)}, timeout=20)
    result["model_auth"] = response.is_success
    result["model_available"] = response.is_success and settings.model_name in [row.get("id") for row in response.json().get("data", [])]
except (httpx.HTTPError, ValueError, TypeError):
    result["model_auth"] = False
result["mail_sent"] = False
result["paid_generation"] = False
print(json.dumps(result))
