"""Create only the new site's private configuration on the same server."""
import json
import secrets
from email.utils import parseaddr
from pathlib import Path


def read_env(path):
    values = {}
    for line in path.read_text().splitlines():
        if line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if value[:1] == value[-1:] and value[:1] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


target = Path("/srv/energy-research-web")
if target.resolve() != target:
    raise SystemExit("Deployment directory is not the expected absolute path")
target.mkdir(mode=0o700, exist_ok=True)
destination = target / ".env.web"
if destination.exists():
    print(json.dumps({"environment": "preserved"}))
else:
    values = read_env(target / ".env.web.example")
    existing = read_env(Path("/srv/exam-king-beta/.env.public"))
    fields = ("HOST", "PORT", "USERNAME", "PASSWORD", "FROM", "USE_SSL")
    for field in fields:
        name = "AUTH_SMTP_SSL" if field == "USE_SSL" else f"AUTH_SMTP_{field}"
        if existing.get(f"EP_WEB_SMTP_{field}"):
            values[name] = existing[f"EP_WEB_SMTP_{field}"]
    address = parseaddr(values.get("AUTH_SMTP_FROM", ""))[1] or values.get("AUTH_SMTP_USERNAME", "")
    if not address or not values.get("AUTH_SMTP_PASSWORD"):
        raise SystemExit("Existing verified SMTP configuration is unavailable")
    values["AUTH_ADMIN_EMAIL"] = address.lower()
    values["AUTH_SMTP_FROM"] = f"能研智助 <{address}>"
    values["AUTH_CODE_SECRET"] = secrets.token_urlsafe(48)
    values["AUTH_SMTP_STARTTLS"] = "false" if values["AUTH_SMTP_SSL"].lower() == "true" else "true"
    # Never write these private values into logs, source, artifacts or stdout.
    destination.write_text("\n".join(f"{key}={json.dumps(value, ensure_ascii=False)}" for key, value in values.items()) + "\n")
    destination.chmod(0o600)
    print(json.dumps({"environment": "created", "admin_configured": True, "smtp_configured": True, "paid_models_enabled": False}))
