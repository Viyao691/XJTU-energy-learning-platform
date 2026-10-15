"""Transfer only the approved local model config over verified SSH stdin."""
import json
import subprocess
from pathlib import Path

SOURCE = '''
import json, sqlite3
from pathlib import Path
from cryptography.fernet import Fernet
db = sqlite3.connect("file:/source/energy_copilot.db?mode=ro", uri=True)
db.row_factory = sqlite3.Row
row = db.execute("select model_provider,model_name,model_base_url,timeout_seconds from user_settings where id=1").fetchone()
assert row is not None and row["model_provider"] == "deepseek" and row["model_base_url"] == "https://api.deepseek.com"
store = json.loads(Path("/source/runtime-secrets.json").read_text())
assert store.get("model_provider") == row["model_provider"]
assert store.get("model_base_url") in (None, row["model_base_url"])
key = Fernet(Path("/source/runtime-secret.key").read_bytes()).decrypt(store["model_api_key_ciphertext"].encode()).decode()
assert key and "\\n" not in key and "\\r" not in key
print(json.dumps({"MODEL_PROVIDER":row["model_provider"],"MODEL_NAME":row["model_name"],"MODEL_BASE_URL":row["model_base_url"],"MODEL_TIMEOUT_SECONDS":str(row["timeout_seconds"]),"MODEL_API_KEY":key}))
'''

DESTINATION = '''
import json,sys
from pathlib import Path
payload=json.load(sys.stdin)
assert set(payload)=={"MODEL_PROVIDER","MODEL_NAME","MODEL_BASE_URL","MODEL_TIMEOUT_SECONDS","MODEL_API_KEY"}
path=Path("/srv/energy-research-web/.env.web")
values={}
for line in path.read_text().splitlines():
    if line.lstrip().startswith("#") or "=" not in line: continue
    key,value=line.split("=",1)
    value=value.strip()
    if value.startswith('"'): value=json.loads(value)
    elif value.startswith("'") and value.endswith("'"): value=value[1:-1].replace("\\'", "'")
    values[key.strip()]=value
values.update(payload)
values["WEB_MODEL_CALL_RESERVE_CNY"]="0"
def quote(value): return "'"+str(value).replace("'", "\\'")+"'"
path.write_text("\\n".join(key+"="+quote(value) for key,value in values.items())+"\\n")
path.chmod(0o600)
print(json.dumps({"model_configured":True,"provider":payload["MODEL_PROVIDER"],"model":payload["MODEL_NAME"],"paid_calls_enabled":False}))
'''

access = Path(r"C:\Users\28742\Documents\Codex\考试大王\exam-pilot-web\.verification\deployment-access")
source = subprocess.run([
    "docker", "run", "--rm", "--user", "0", "--mount",
    "type=volume,source=energy_copilot_data,target=/source,readonly", "--entrypoint", "python",
    "energy-research-api:web-20261014", "-c", SOURCE,
], capture_output=True, text=True)
if source.returncode:
    raise SystemExit("Local model configuration could not be read; no transfer performed")
payload = json.loads(source.stdout)
remote_command = "python3 -c '" + DESTINATION.replace("'", "'\"'\"'") + "'"
result = subprocess.run([
    "ssh", "-i", str(access / "ep-public-20261009"), "-o", f"UserKnownHostsFile={access / 'known_hosts'}",
    "-o", "StrictHostKeyChecking=yes", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
    "root@115.159.51.147", remote_command,
], input=json.dumps(payload), capture_output=True, text=True)
if result.returncode:
    raise SystemExit("Server configuration transfer failed; check server configuration privately")
print(result.stdout.strip())
