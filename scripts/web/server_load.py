"""One 10-minute public-page/health mix; no mail, keys or paid models."""
import concurrent.futures
import json
import subprocess
import time
import urllib.request
from collections import Counter
from pathlib import Path

root = Path("/srv/energy-research-web")
targets = [
    "https://energy.viyao.cn/dashboard", "https://energy.viyao.cn/help",
    "https://energy.viyao.cn/backend-api/health/ready", "https://viyao.cn/api/health",
]
started = time.monotonic()
latencies = []
statuses = Counter()
minimum_available = 100000
maximum_rss = {}
container_names = ["energy-research-web-frontend-1", "energy-research-web-backend-1", "exam-king-beta-web-1", "exam-king-beta-api-1"]
pids = {name: int(subprocess.check_output(["docker", "inspect", name, "--format", "{{.State.Pid}}"], text=True)) for name in container_names}

def request(url):
    before = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            response.read()
            return response.status, time.monotonic() - before
    except Exception:
        return "error", time.monotonic() - before

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    while time.monotonic() - started < 600:
        for status, latency in pool.map(request, targets):
            statuses[str(status)] += 1
            latencies.append(latency)
        available = next(int(line.split()[1]) // 1024 for line in Path("/proc/meminfo").read_text().splitlines() if line.startswith("MemAvailable:"))
        minimum_available = min(minimum_available, available)
        for name, pid in pids.items():
            status_path = Path(f"/proc/{pid}/status")
            if status_path.exists():
                rss = next((int(line.split()[1]) // 1024 for line in status_path.read_text().splitlines() if line.startswith("VmRSS:")), 0)
                maximum_rss[name] = max(maximum_rss.get(name, 0), rss)
        progress = {"elapsed_seconds": round(time.monotonic() - started), "requests": len(latencies), "statuses": dict(statuses), "minimum_available_mib": minimum_available, "maximum_process_rss_mib": maximum_rss}
        (root / "load-progress.json").write_text(json.dumps(progress))
        time.sleep(2)
latencies.sort()
progress.update(p95_seconds=round(latencies[min(len(latencies)-1, int(len(latencies)*.95))], 3), scope="public_pages_and_health_only", real_model_concurrency_verified=False)
(root / "load-result.json").write_text(json.dumps(progress, indent=2))
print(json.dumps(progress))
