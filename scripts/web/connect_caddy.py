"""Append the reviewed site block, validate, then reload the existing edge."""
import fcntl
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

root = Path("/srv/energy-research-web")
config = Path("/srv/exam-king-beta/deploy/Caddyfile")
container = "exam-king-beta-caddy-1"

def run(*args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {args[0]} {args[1]}")

with (root / "caddy-update.lock").open("w") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    original = config.read_bytes()
    if b"energy.viyao.cn {" in original:
        print(json.dumps({"caddy": "site_already_present"}))
    else:
        backup = root / ("Caddyfile.before-energy-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
        backup.write_bytes(original)
        backup.chmod(0o600)
        candidate = root / "Caddyfile.energy-candidate"
        candidate.write_bytes(original.rstrip() + b"\n\n" + (root / "energy.Caddyfile").read_bytes())
        candidate.chmod(0o600)
        run("docker", "cp", str(candidate), f"{container}:/tmp/Caddyfile.energy-candidate")
        run("docker", "exec", container, "caddy", "validate", "--config", "/tmp/Caddyfile.energy-candidate", "--adapter", "caddyfile")
        if config.read_bytes() != original:
            raise SystemExit("Existing Caddy configuration changed during preparation; no update performed")
        # This is a single-file bind mount: preserve its inode so reload sees it.
        with config.open("wb") as destination:
            destination.write(candidate.read_bytes())
            destination.flush()
            os.fsync(destination.fileno())
        try:
            run("docker", "exec", container, "caddy", "reload", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile")
        except RuntimeError:
            config.write_bytes(original)
            run("docker", "exec", container, "caddy", "reload", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile")
            raise SystemExit("Reload failed; original Caddy configuration restored")
        print(json.dumps({"caddy": "validated_and_reloaded", "backup": backup.name}))
