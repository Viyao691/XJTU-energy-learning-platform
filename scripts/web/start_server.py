"""Load the verified release and start only the isolated, capped web project."""
import json
import subprocess
from pathlib import Path

root = Path("/srv/energy-research-web")
available = next(int(line.split()[1]) // 1024 for line in Path("/proc/meminfo").read_text().splitlines() if line.startswith("MemAvailable:"))
if available < 1300:
    raise SystemExit("Available memory below the first-start threshold; no services started")
files = {"energy-web-20261014.tar.gz": 369003896, "energy-api-final-20261014.tar": 86841344}
for name, size in files.items():
    if (root / name).stat().st_size != size:
        raise SystemExit("Release transfer is incomplete")

def run(*args):
    result = subprocess.run(args, cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(f"Deployment step failed: {args[0]} {args[1]}; inspect privately on server")
    return result.stdout.strip()

for name in files:
    run("docker", "load", "-i", str(root / name))
for image, expected in (
    ("energy-research-api:web-20261014", "sha256:633562715457bacdabab06641d74e464f74355a0bfb78874b3315a045deb17b2"),
    ("energy-research-web:web-20261014", "sha256:3e85ea1e0d6fd7a4ec8c13ed2b742e19b0a3a081203015af93b63759e82721e7"),
):
    if run("docker", "image", "inspect", image, "--format", "{{.Id}}") != expected:
        raise SystemExit("Loaded image does not match the verified release")
compose = ("docker", "compose", "-f", "compose.web.yml", "--env-file", ".env.web")
run(*compose, "config", "--quiet")
run(*compose, "run", "--rm", "--no-deps", "backend", "python", "-m", "alembic", "upgrade", "head")
run(*compose, "up", "-d", "--no-build", "--wait", "--wait-timeout", "120")
print(json.dumps({"services": "healthy", "migration": "head", "initial_available_mib": available, "public_route_connected": False}))
