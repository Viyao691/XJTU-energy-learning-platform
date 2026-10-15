# 从这里开始 · 2026-09-27

唯一主项目：`Energy-Research-Copilot-DeepSeek-Harness-2026-08-21`。旧 `phase-0-phase-1-api-mock` 仅作历史参考。先以用户新要求为准，不自动继续历史路线图。

1. 读 [当前状态](CURRENT_STATUS.md)：已部署范围、验证边界、已知局限和清理结果。
2. 读 [新对话交接](docs/handoff/README.md) 与 [AGENTS.md](AGENTS.md)，再按任务读 [PLAN.md](PLAN.md) 和相关源码。
3. 需要追溯时读[状态历史](docs/handoff/2026-09-27-status-history.md)、[实际验证报告](TEST_REPORT.md)及各专题交接；历史测试数字不是当前全套通过证明。

最新交付包括共用的 18 供应商目录、校园 AI 整理预算、论文库和科研数据状态分栏、能源视觉与 37 条帮助说明。[2026-09-27 新对话摘要](docs/handoff/2026-09-27-next-session.md)持续记录清理结果。首页 `/dashboard` 已冻结，勿因其他页面工作改动 `frontend/components/home-hero/` 或 `frontend/public/home-hero/`。

根目录 `start.ps1` 维护 Docker 启动，会在前端 3000–3099、后端 8000–8099 选择空闲端口；最近一次部署在 3001/8001，**始终以启动器本次打印的 URL 为准**。修改后只做任务必要的定向验证和构建，不默认重复全套测试、截图或首页哈希。运行设置可变；涉及模型时先只读查询设置状态，绝不输出密钥。

| 路径 | 用途 |
|---|---|
| `frontend/app/`、`frontend/components/workspace/` | 非首页页面与共享视觉壳层 |
| `frontend/components/papers/` | 论文详情、阅读与业务状态 |
| `frontend/components/home-hero/`、`frontend/public/home-hero/` | 冻结首页 |
| `backend/app/routers/`、`backend/app/services/` | FastAPI 业务与后台服务 |
| `frontend/lib/api.ts`、`frontend/lib/api.generated.d.ts`、`backend/openapi.json` | API 调用与生成类型 |
| `frontend/public/workspace/`、`design/non-home/` | 当前非首页素材与设计来源 |
| `docs/handoff/`、`TEST_REPORT.md` | 交接、历史与实际验证证据 |
| `local_state/`、`backups/` | 用户数据、模型和备份；不可当缓存清理 |

2026-09-27 缓存清理已完成，详见[新对话交接](docs/handoff/2026-09-27-next-session.md)与[清理清单](docs/handoff/2026-09-27-cleanup-manifest.json)。
