# 新对话交接 · 2026-09-27

2026-10-03论文库关键词、研究体裁与缺失名词解释整理已部署；33篇各8关键词，10份缺失名词已补齐并保存，旧23份保留。标题化学式显示与未来上传本地规则同步修正。[最新交接](2026-10-03-library-metadata.md)。

主项目根目录为 `Energy-Research-Copilot-DeepSeek-Harness-2026-08-21`，即本文上两级目录。`phase-0-phase-1-api-mock` 是历史项目。先读根目录 [START_HERE.md](../../START_HERE.md)、[AGENTS.md](../../AGENTS.md)、[CURRENT_STATUS.md](../../CURRENT_STATUS.md)，再按用户新任务读取目标源码和 [PLAN.md](../../PLAN.md)；不要自动继续旧路线图。

[新对话摘要与清理结果](2026-09-27-next-session.md)给出最近范围。[压缩前状态历史](2026-09-27-status-history.md)保留逐轮构建、定向测试和正式截图链接；[TEST_REPORT.md](../../TEST_REPORT.md)只记录已执行检查。历史记录可能相互覆盖，以最新只读运行状态和源码为准。

最新论文快速理解 Mermaid 图示部署与服务计数检查见[交接记录](2026-09-27-mermaid-deployment.md)；真实模型生成和图形渲染验收由本轮主任务继续记录。

2026-10-03全库33篇批量报告补齐及图表详细版已完成，523条图表记录保存且无空项，本轮用户模型API调用0。最新范围、格式与续接说明见[全库图表交接](2026-10-03-library-visual-analysis.md)。

## 启动与运行边界

- 根目录 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./start.ps1` 启动现有镜像；确需重建时才用 `start.ps1 -Rebuild`。脚本在前端 3000–3099、后端 8000–8099 避让其他应用。最近部署地址为前端 3001、后端 8001，实际以本次输出为准；Docker 内部仍为前端 3000、后端 8000。
- 独立前端开发服务器应另选空闲端口并用 `BACKEND_API_URL` 指向当前后端主机端口，勿默认占用 Docker 正在用的 3001。开发服务器改变不会自动更新正式容器。
- 任何真实模型调用前先只读 GET `/api/v1/settings` 核对当前供应商/模型；最近一次只读观察为 Mock，早前曾是 DeepSeek，不能从历史记录推断此刻状态。无需、不得在聊天或文档输出密钥。
- 用户偏好节省验证额度：业务改动做一组必要定向检查；只有具体失败或用户要求时才扩大。不要默认全量测试、反复构建、截图或首页哈希。

## 功能入口

| 功能 | 源码入口 |
|---|---|
| 搜索、论文库、上传、单篇阅读 | `frontend/app/search`、`library`、`upload`、`papers/[id]`，论文详情状态在 `components/papers/usePaperDetail.ts` |
| 论文问答、比较、订阅与日报 | `frontend/app/knowledge`、`compare`、`subscriptions`、`research-daily` |
| 学习包、校园公开资讯 | `frontend/app/learning`、`learning/[id]`、`campus` |
| 科研数据、想法、竞赛 | `frontend/app/research-data`、`ideas`、`contests`、`contests/[id]` |
| 设置、首次引导、诊断、备份、帮助 | `frontend/app/settings`、`onboarding`、`diagnostics`、`maintenance`、`help` |
| 后端业务 | `backend/app/routers/`、`backend/app/services/`；`main.py` 负责组装 |

前端 API 包装在 `frontend/lib/api.ts`，响应类型从 `backend/openapi.json` 生成到 `frontend/lib/api.generated.d.ts`。数据库变更必须经 Alembic。`/dashboard` 首页及 `frontend/components/home-hero/`、`frontend/public/home-hero/` 已冻结。

## 当前限制与资料保护

- 18 供应商目录供设置和引导共用；校园 AI 日限 20/100/0 与输出 Token 上限独立于仅供参考的金额预算。[预算实现](2026-09-27-campus-ai-budget.md)、[帮助事实核对](2026-09-27-help-content-refresh.md)。
- 重走首次引导的第 2 步会覆盖全局模型及部分预算，且可能重置文档视觉；三种模式只记录偏好。见[重复引导说明](2026-09-27-onboarding-repeat-help.md)。
- 保留全文、摘要、元数据、规则与 AI 推断的证据边界；模型/视觉输出不可当作论文原文。公共网站的 401/403、robots 与 429 限制不能绕过。公众号公开外链不等于正文订阅，群消息和小程序尚未接入。
- `local_state`、`backups`、`backend/data`、`.env`、密钥、模型、用户 PDF、`.git` 与工作树不是可随意删除的缓存。2026-09-27 清理结果见[新对话摘要](2026-09-27-next-session.md)和[清理清单](2026-09-27-cleanup-manifest.json)。

## 新对话开场

> 在当前 Energy-Research-Copilot-DeepSeek-Harness-2026-08-21 开发我接下来指定的新功能。先读 START_HERE.md、AGENTS.md、CURRENT_STATUS.md 和 docs/handoff/README.md，再核对目标源码与当前运行状态。首页冻结，数据与密钥保留；只做必要定向验证，不自动推进旧路线图。
