"""Authentication and capability policy for the public lightweight runtime."""
import asyncio
import re
from datetime import datetime

from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.ownership import current_user_id


PUBLIC_GET = frozenset({
    "/health", "/health/live", "/health/ready",
    "/api/v1/campus/events", "/api/v1/campus/public-links",
    "/api/v1/campus/sources", "/api/v1/research/news",
})
ADMIN_PREFIXES = ("/api/v1/settings", "/api/v1/maintenance", "/api/v1/diagnostics")
DISABLED = re.compile(
    r"(?:/document-ai(?:/|$)|/ocr-runs(?:/|$)|/parse-runs(?:/|$)|"
    r"/transcribe-formula$|/cloud-enhance$|/audio$|/contest-sources/\d+/ocr$|"
    r"/visuals/\d+/analyze$|/crops/\d+/(?:analyze|extract-data)$|"
    r"/research/subscriptions(?:/|$))"
)

LONG_OPERATION = re.compile(r"/(?:upload|import|analyze|generate|ask|compare|external-comparison|reading-highlights|index|reindex)(?:/|$)|/analysis/|/research-ideas/review")


def install_web_access(app, settings, auth_factory):
    from app.auth import authenticate, require_csrf
    from app.models import TaskRun
    slots = asyncio.Semaphore(settings.web_model_concurrency)
    pending_users: set[int] = set()

    def task_state(task_id, **values):
        with app.state.session_factory() as db:
            item = db.get(TaskRun, task_id)
            if item is not None:
                for key, value in values.items():
                    setattr(item, key, value)
                db.commit()

    @app.middleware("http")
    async def enforce_web_access(request, call_next):
        path = request.url.path.rstrip("/") or "/"
        public = request.method in {"GET", "HEAD"} and path in PUBLIC_GET
        auth_route = path.startswith("/api/v1/auth/")
        feedback_route = request.method == "POST" and path == "/api/v1/feedback"
        token = current_user_id.set(None)
        task_id = None
        queued_user = None
        try:
            if not public and not auth_route and not feedback_route:
                user = authenticate(request, auth_factory)
                if user is None:
                    return JSONResponse({"detail": "请先登录后使用科研功能"}, status_code=401)
                current_user_id.set(user.id)
                if request.method not in {"GET", "HEAD", "OPTIONS"}:
                    require_csrf(request, settings=settings)
                admin = user.is_admin
                if path == "/metrics" or path.startswith(ADMIN_PREFIXES) or (
                    path.startswith("/api/v1/campus/") and request.method not in {"GET", "HEAD"}
                ):
                    if not admin:
                        return JSONResponse({"detail": "此操作需要管理员权限"}, status_code=403)
                if DISABLED.search(path):
                    return JSONResponse({"detail": "轻量网站首版尚未开放此功能"}, status_code=503)
                if path == "/api/v1/tasks" and request.method == "POST":
                    return JSONResponse({"detail": "请从具体科研操作创建任务"}, status_code=403)
                if request.method == "POST" and LONG_OPERATION.search(path):
                    if user.id in pending_users or len(pending_users) >= settings.web_task_queue_limit:
                        return JSONResponse({"detail": "科研任务正在处理，请稍后重试"}, status_code=429, headers={"Retry-After": "5"})
                    pending_users.add(user.id)
                    queued_user = user.id
                    with app.state.session_factory() as db:
                        task = TaskRun(task_name=f"web:{path}", status="queued", max_attempts=1)
                        db.add(task)
                        db.commit()
                        task_id = task.id
            if task_id is not None:
                async with slots:
                    task_state(task_id, status="running", started_at=datetime.utcnow(), attempt_count=1)
                    response = await call_next(request)
                    task_state(task_id, status="completed" if response.status_code < 400 else "failed", completed_at=datetime.utcnow(), progress=1.0)
                response.headers["X-Task-Id"] = str(task_id)
            else:
                response = await call_next(request)
            if not public:
                response.headers["Cache-Control"] = "private, no-store"
            else:
                response.headers["Cache-Control"] = "public, max-age=60"
            return response
        except HTTPException as exc:
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        finally:
            if queued_user is not None:
                pending_users.discard(queued_user)
            if task_id is not None:
                # A disconnected/crashed request is never replayed automatically.
                with app.state.session_factory() as db:
                    item = db.get(TaskRun, task_id)
                    if item is not None and item.status in {"queued", "running"}:
                        item.status, item.error_code, item.completed_at = "interrupted", "request_interrupted", datetime.utcnow()
                        db.commit()
            current_user_id.reset(token)
