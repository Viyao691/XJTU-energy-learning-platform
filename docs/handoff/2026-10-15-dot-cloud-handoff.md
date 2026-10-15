# 能研智助网站 · dot 云端编辑交接

网站：https://energy.viyao.cn

源码仓库：https://github.com/Viyao691/XJTU-energy-learning-platform

本次交接分支：`codex/energy-web-handoff-20261015`。从此分支继续编辑，不从旧 main 开始。网站部署和 GitHub 分支独立，提交源码不会自动发布到服务器。

视频、手机审查记录与可编辑素材位于私有资料页：https://chatgpt.com/space/page_5c4fbfe044d48191b07919ac010fe77e 。使用用户自己的账号访问；没有授权访问时以仓库内 `docs/mobile/2026-10-15-mobile-audit.md` 为准。

## 当前版本

最新为2026-10-15紧凑账号版：API/Web均 `web-20261015-compact`，BUILD_ID `SeH-5j_0F2ZiqrBHeV3rc`，Alembic0033。注册email/code/password，默认登录email/password，忘记密码切email/code；密码8–128字符，旧账号可继续验证码登录。导航232px、账户完整换行、首页无搜索且弹层160px/14px，品牌使用用户选定A-final小尺寸版。后端46/前端39定向检查和生产构建通过，服务器备份迁移后健康，真实HTTPS版本匹配。手机审查见 `docs/mobile/2026-10-15-compact-account-audit.md`。私有页原126秒巡览为此前mobile4版本，新的截图与审查资料单独标记。

以下mobile4信息是上一个部署版本，新的开发应以上段、CURRENT_STATUS和当前源码为准。

2026-10-15 已部署登录、注册、游客入口与手机布局修正。Web 镜像 `energy-research-web:web-20261015-mobile4`，BUILD_ID `Y9lh0Lu-TpxDM0gFSJ-jC`。API 镜像 `energy-research-api:web-20261015-account`。服务器保持 4GB，公开知识可以浏览，科研功能需要登录；重型 OCR 等功能暂未开放。

本次源码快照覆盖当前前后端、迁移、测试、网页构建配置和必要静态图片，不包含模型、数据库、用户论文、环境密钥或服务器会话。它基于仓库 main `3c97a48e17519f009a7eaa145d742e2558e81f78` 叠加本机当前源码；历史资料保留在原仓库。

## 编辑入口和约束

先读 `AGENTS.md`、`START_HERE.md`、`CURRENT_STATUS.md`、`docs/handoff/README.md`，再读取新任务相关文件。当前用户要求已经完成的范围是登录/注册/游客界面、手机端适配和巡览视频，后续只执行用户新指令。

前端为 Next.js，源码在 `frontend/`；后端为 FastAPI、SQLite 和本地文件存储，源码在 `backend/`。账号入口在 `frontend/components/auth/`，页面及共享样式在 `frontend/app/` 和 `frontend/components/`。手机审查清单在 `docs/mobile/2026-10-15-mobile-audit.md`。

保留已接受的桌面首页（`frontend/components/home-hero/`、`frontend/public/home-hero/`）以及论文顶部字号冻结。不要把手机修改扩展为桌面首页重做。不能覆盖服务器真实环境变量、密钥和付费模型预算；`.env.web.example` 只有示例。云端开发默认 Mock，不发真实验证码、不调用付费模型、不上传私人论文。

## 云端运行与交付

Node.js 24，Python 3.12。前端 `npm ci` 后可运行 `ENERGY_WEB_MODE=true BACKEND_API_URL=http://127.0.0.1:8000 npm run dev -- --port 3002`（在 `frontend` 目录）。Linux 后端可在独立 Python 3.12 虚拟环境安装 `backend/requirements.web.txt` 与开发需要的 `requirements-dev.txt`；数据库和存储目录使用临时工作目录，迁移使用 Alembic。按照现有配置使用 Mock，不从生产导出数据。

网站构建入口为 `frontend/Dockerfile.web`、`backend/Dockerfile.web` 和 `compose.web.yml`。前端 Docker 以仓库根目录为上下文，后端以 `backend` 为上下文；网页静态资源优化脚本在 `scripts/web/`。本机 Windows 的 `start.ps1` 用于原本桌面环境，不是 Linux 云端启动命令。

最近手机改动验证为 33 项定向测试通过、生产构建通过；360/390px 共 24 个布局实际观察，线上 390px 论文库另行确认。视频为 36 个界面截图组成的 126 秒无声巡览，并非连续屏幕录制，也未做真实 Android/iOS 浏览器测试。本次云端同步不重复运行全量测试。

推荐交给 dot 的提示：

> 在 `Viyao691/XJTU-energy-learning-platform` 的 `codex/energy-web-handoff-20261015` 分支继续编辑能研智助网站。先读项目交接与当前源码；保持桌面首页和论文顶部字体冻结，仅实施我本次指定的修改，做必要定向检查。提交到独立分支供审查，不自动部署。视频素材和审查记录见交接私有资料页。
