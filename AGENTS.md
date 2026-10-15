# Energy Research Copilot Project Instructions

## Mandatory session bootstrap

For every new Codex chat started in this project:

1. Confirm this is `Energy-Research-Copilot-DeepSeek-Harness-2026-08-21`, then read `START_HERE.md`, `CURRENT_STATUS.md` and `docs/handoff/README.md`. The sibling `phase-0-phase-1-api-mock` is legacy, not the active source.
2. Read `PLAN.md` before planning new Phase work.
3. Read only the files relevant to the current task under `docs/superpowers/specs/` and `docs/superpowers/plans/`.
4. Inspect the current source and runtime before trusting historical status. Test counts in Markdown are evidence from a past run, not proof that the current tree still passes.
5. Follow the user's newest request. Do not automatically continue the roadmap when the user asks for something else.

When handing work to another chat, update `CURRENT_STATUS.md` with the current scope, latest verified results, known blockers, and recommended next action.

## Scope

This repository implements **Energy Research Copilot**, a local-first Chinese research assistant for energy-storage papers. Keep the current architecture simple and maintainable: Next.js frontend, FastAPI backend, SQLite database, local file storage, and Docker Compose. Do not add microservices unless a later approved Phase requires them.

### Project identity before writing

The chat's sidebar project and default working directory are not proof that a request belongs to this repository. Before writing, confirm the requested product and its actual project root. For work belonging to another product, use that product's explicit absolute working directory; do not place its source, release assets, temporary scripts, or status updates here. Keep Git operations scoped to the verified repository, and preserve this project's existing uncommitted changes. Correcting chat organization does not authorize moving or deleting project data.

## Commands

- Start existing images: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\start.ps1`
- Rebuild and start after code changes: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\start.ps1 -Rebuild`
- Backend tests in the supported Python 3.12 environment: `docker compose exec -T backend python -m pytest tests -q`
- Local backend tests (uv-managed Python 3.12 venv): `cd backend; .\venv\Scripts\python.exe -m pytest tests -q`
- Local backend dev server (Mock, uses local Ollama for embeddings): `cd backend; $env:EMBEDDING_BASE_URL='http://127.0.0.1:11434'; .\venv\Scripts\python.exe -m uvicorn app.main:app --port 8000`
- Local backend dev server with OCR models (points at the harness `local_state` copy): `cd backend; $env:EMBEDDING_BASE_URL='http://127.0.0.1:11434'; $env:DOCUMENT_AI_MODEL_PATH='..\local_state\document-ai-models'; $env:PADDLE_PDX_CACHE_HOME='..\local_state\document-ai-models\paddlex'; .\venv\Scripts\python.exe -m uvicorn app.main:app --port 8000`
- Rebuild the local backend venv: `cd backend; uv venv .venv --python 3.12; uv pip install -r requirements.txt --python .venv`
- Frontend tests: `npm.cmd --prefix frontend run test`
- Frontend production build: `npm.cmd --prefix frontend run build`
- Regenerate frontend API types from backend OpenAPI schema: `npm.cmd --prefix frontend run generate:types` (after backend schema changes, also re-run `python -m scripts.export_openapi` in the backend to refresh `backend/openapi.json`)
- Docker Compose security check: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\test_compose_security.ps1`
- Container status: `docker compose ps`
- CI: `.github/workflows/ci.yml` runs backend pytest, frontend tsc/test/build, and OpenAPI/type-drift checks on push/PR to `main`. Both `backend/openapi.json` and `frontend/lib/api.generated.d.ts` are committed artifacts; regenerate and commit them together with schema changes or CI will fail.

The local `backend/.venv` is managed by `uv` and pinned to Python 3.12 (`backend/pyproject.toml` declares `requires-python = ">=3.12,<3.14"`), matching the Docker image. The old Python 3.14 venv was incompatible with the pinned SQLAlchemy 2.0.40 and has been replaced; do not recreate the venv with the system Python 3.14. Docker/Python 3.12 remains the authoritative verification environment.

## Architecture constraints

- Use `ModelProvider`; business services must not import provider SDKs.
- Persist every schema change through `backend/alembic/versions/`.
- Never store, log, or return a raw API key. API responses may only expose configuration state and a masked last four characters.
- API keys are backend-only and must never be sent to the frontend.
- Label analysis claims by evidence status. Mock output is always `AI推断（Mock 演示）`.
- Distinguish full text, abstract-only, and metadata-only evidence in storage and answers.
- Do not claim PDF-level evidence when extraction did not yield it.
- Uploads must be PDF only, path-safe, size-limited, SHA-256 deduplicated, and stored outside static web assets.
- Do not bypass paywalls, institutional authentication, or publisher access controls.
- External model and paper-source calls must use Mock or controlled fakes in automated tests.
- FastAPI routes live in `backend/app/routers/` by domain (`settings.py`, `research.py`, `search.py`, `papers.py`, `knowledge.py`), registered from `app.main.create_app()`; shared DTO/PDF/source helpers stay in `routers/_shared.py`. Do not add routes directly to `main.py`.
- Frontend paper-detail state and handlers live in `frontend/components/papers/usePaperDetail.ts`; its JSX is split into subcomponents in `frontend/components/papers/`. Keep large pages composed from hooks + small components.
- Frontend API response types are generated from the backend OpenAPI schema (`frontend/lib/api.generated.d.ts`). Do not hand-write response types in `frontend/lib/api.ts`; extend generated types with explicit Omit/intersection only when the frontend needs a field the backend does not return.

## Implementation discipline

- Think before coding and state material assumptions.
- Make the smallest change that satisfies the current request.
- Follow red/green tests for behavior changes and bug fixes.
- Preserve unrelated user files and changes.
- Use Alembic for every database schema change.
- Do not claim a feature is complete until its relevant tests, build, and runtime checks have actually run.

## Documentation discipline

After completing work:

- Update `CURRENT_STATUS.md` when current scope, limitations, verification results, or next actions change.
- Update `PLAN.md` when a roadmap item starts, completes, or changes scope.
- Update `TEST_REPORT.md` only with tests and runtime checks that were actually executed.
- Update `README.md` when user-facing setup, commands, configuration, or behavior changes.
- Update `AGENTS.md` only when durable project rules, architecture constraints, or standard commands change.

Never put secrets, API keys, passwords, private account details, or sensitive paper contents into project Markdown files.

## Current handoff

The authoritative short handoff is `CURRENT_STATUS.md`. The detailed roadmap is `PLAN.md`; the latest verification evidence is `TEST_REPORT.md`.


## Frozen homepage boundary (2026-09-24)

The user has frozen the accepted homepage. Production `/dashboard` uses `frontend/components/home-hero/` and `frontend/public/home-hero/`; freeze manifest and checks are in `docs/homepage/` and `scripts/homepage/`. Do not redesign or replace these while refactoring other pages unless the user explicitly reopens the homepage scope. Shared layout/global CSS changes must preserve it.

`archive/hero-development-2026-09-24/` contains historical experiments and Blender masters, outside the runtime/build. Do not reintroduce old visual assertions or run archived exporters against current assets. Cleanup provenance is in `docs/handoff/`; never delete data, secrets, backups or worktrees as visual cleanup.

## Validation budget preference (2026-09-25)

The user explicitly requires quota-conscious completion: do not run full test suites or hash/freeze checks by default. Use one necessary targeted check for material behavior changes. Do not repeatedly rebuild, recapture screenshots, or revalidate cosmetic changes. Expand checks only for a concrete unresolved failure or explicit user request. Preserve the frozen homepage by scope discipline; do not automatically hash it after unrelated page work. Report precisely which revision was checked and any final unverified CSS. This does not reduce research-analysis depth or evidence quality.

## Paper-detail top typography freeze (2026-09-27)

Keep the paper-detail top typography in `frontend/components/papers/reader-refinement.css`: section titles 24px, section labels 13px, PDF description and parsing-tool summary 15px, analysis tabs 16px with at least 44px height, and tab-panel toolbar titles 21px. Do not shrink or change this local block unless the user explicitly asks. This freeze does not prevent new features or unrelated page work.

## Local launch ports (2026-09-25)

Use root `start.ps1` for the maintained desktop/Harness startup. It selects a free frontend host port in 3000–3099 and backend host port in 8000–8099, preserving other applications; follow its printed URL. Docker internal ports remain frontend 3000/backend 8000. Do not assume `npm run dev` port 3001 is free while Docker runs: choose a separate dev port and set `BACKEND_API_URL` to the selected backend host port. Current deployment details and dependency-reuse build limitation are in `docs/handoff/2026-09-25-integration.md`.
