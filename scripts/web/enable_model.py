"""Apply the reviewed first-release allocation and restart only the new API."""
import json
import subprocess
from pathlib import Path

root = Path("/srv/energy-research-web")
image = subprocess.check_output(["docker", "image", "inspect", "energy-research-api:web-20261014", "--format", "{{.Id}}"], text=True).strip()
assert image == "sha256:633562715457bacdabab06641d74e464f74355a0bfb78874b3315a045deb17b2"
path = root / ".env.web"
value = path.read_text()
assert "MODEL_PROVIDER='deepseek'" in value and "MODEL_NAME='deepseek-v4-pro'" in value
if "WEB_MODEL_CALL_RESERVE_CNY='0'" in value:
    path.write_text(value.replace("WEB_MODEL_CALL_RESERVE_CNY='0'", "WEB_MODEL_CALL_RESERVE_CNY='3'"))
    path.chmod(0o600)
elif "WEB_MODEL_CALL_RESERVE_CNY='3'" not in value:
    raise SystemExit("Unexpected model allocation; no change performed")
budgets = {
    "DAILY_BUDGET_CNY": "20", "MONTHLY_BUDGET_CNY": "100",
    "WEB_USER_DAILY_BUDGET_CNY": "10", "WEB_USER_MONTHLY_BUDGET_CNY": "30",
}
lines = path.read_text().splitlines()
found = {line.split("=", 1)[0] for line in lines if "=" in line} & budgets.keys()
assert found == budgets.keys(), "Budget configuration is incomplete"
path.write_text("\n".join(f"{key}='{budgets[key]}'" if (key := line.split("=", 1)[0]) in budgets else line for line in lines) + "\n")
path.chmod(0o600)
result = subprocess.run(["docker", "compose", "-f", "compose.web.yml", "--env-file", ".env.web", "up", "-d", "--no-build", "--no-deps", "--wait", "--wait-timeout", "90", "backend"], cwd=root, capture_output=True, text=True)
if result.returncode:
    raise SystemExit("New API restart failed; inspect privately on server")
print(json.dumps({"model": "deepseek-v4-pro", "call_allocation_cny": 3, "platform_daily_cny": 20, "platform_monthly_cny": 100, "user_daily_cny": 10, "user_monthly_cny": 30, "api": "healthy"}))
