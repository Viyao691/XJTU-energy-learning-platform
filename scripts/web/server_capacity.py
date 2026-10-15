"""Read-only server capacity snapshot. Never prints container environments."""
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(*args):
    return subprocess.check_output(args, text=True).strip()


memory = {}
for line in Path("/proc/meminfo").read_text().splitlines():
    key, _, value = line.partition(":")
    if key in {"MemTotal", "MemAvailable", "SwapTotal"}:
        memory[key + "MiB"] = int(value.split()[0]) // 1024
disk = shutil.disk_usage("/srv")
containers = []
for name in run("docker", "ps", "--format", "{{.Names}}").splitlines():
    item = json.loads(run("docker", "inspect", name))[0]
    containers.append({
        "name": name, "memory_limit_mib": item["HostConfig"]["Memory"] // 1024**2,
        "cpu_limit": item["HostConfig"]["NanoCpus"] / 10**9,
        "networks": list(item["NetworkSettings"]["Networks"]),
        "status": item["State"]["Status"],
    })
print(json.dumps({
    "time_utc": datetime.now(timezone.utc).isoformat(), "memory": memory,
    "disk_free_gib": round(disk.free / 1024**3, 2), "containers": containers,
    "usage": run("docker", "stats", "--no-stream", "--format", "{{.Name}} {{.MemUsage}} {{.CPUPerc}}"),
}, ensure_ascii=False, indent=2))
