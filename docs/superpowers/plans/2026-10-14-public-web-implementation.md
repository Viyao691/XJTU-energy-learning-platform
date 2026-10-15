# 4GB 公网轻量首版实施计划

依据：用户2026-10-14已批准部署设计并授权开始实施。保持当前活跃工作区和桌面行为，保留既有修改；不搬运旧项目或私人数据。

目标：公开储能知识、登录科研及个人数据隔离、轻量运行和独立部署交付；只有容量与真实业务验收满足时才接入线上。

架构：既有Caddy入口、独立Next.js/FastAPI/SQLite。新增邮箱会话认证和ORM所有权约束，采用单API进程及远端模型；无重型模型常驻。

## 任务与验收

- [x] 0. 只读查找现有管理员连接，记录服务器MemTotal/MemAvailable、磁盘、容器资源及实际限额。若管理通道不可用，继续本地实现，留下可执行的只读容量采集脚本；不凭健康接口推断容量。
- [x] 1. 认证：`backend/app/auth_models.py`、`backend/app/auth.py`、`backend/app/routers/auth.py`、Alembic0030及`backend/tests/test_web_auth.py`。契约为POST `/api/v1/auth/email-code`、POST `/api/v1/auth/login`（email/code）、GET `/api/v1/auth/me`、POST `/api/v1/auth/logout`；发送函数在测试替换为受控收件箱。先失败测试再实现验证码过期/错误限流/会话/退出/CSRF。
- [x] 2. 隔离：`backend/app/ownership.py`、models/database/main和Alembic0031；所有私有模型保存user_id，SELECT及批量写操作统一作用域约束，新行自动绑定用户；文档路径按用户分目录，文件hash/DOI/arXiv去重按用户作用域。新增`test_web_isolation.py`覆盖两用户同文件、私有列表/直接ID/下载/检索/任务/写入和管理员边界。默认桌面模式保持不启用认证。
- [x] 3. 前端：`frontend/components/auth/`、`frontend/app/login/`、路由守卫及独立web部署模式；公开白名单dashboard/research/chronicle/help/campus，科研跳转登录；登录/退出显示明确状态。冻结首页不编辑。前端测试覆盖跳转及返回地址限制。
- [x] 4. 轻量：独立`backend/requirements.web.txt`及`Dockerfile.web`，新增远端EmbeddingProvider；重型功能web模式关闭，限制解析页数、存储、任务/模型并发、必要输入大小。维护桌面重型能力。
- [x] 5. 部署：`compose.web.yml`、`.env.web.example`、Caddy子域名附加配置和`deploy/web/`部署/容量/回滚脚本；新增项目、网络与卷。镜像构建在CI或本机，不启动未经容量验证的生产业务。
- [x] 6. 有界任务/性能：只优化当前网络和数据路径；增量图片、页面按需加载、公开/私有缓存边界、SQLite版本检查及WAL短事务、模型预算与队列；不调整研究输出深度。
- [ ] 7. 集成：只运行新增/相关测试、一次必要前端构建、OpenAPI/type生成和受控合成PDF浏览器流程；记录修订、费用和容量边界，不默认全套。
- [ ] 8. 交付：本机/CI Linux轻量镜像、公开知识清单、空库安装/迁移、DNS和证书接入、一次混合负载与恢复演练。缺少管理员/DNS/SMTP/模型配置时明确记录，并完成其余准备工作。

执行：按技能要求委派边界明确的认证、前端和轻量打包任务，主任务整合所有权/运行/部署与审查；不自动提交已有未提交文件。测试命令使用backend/.venv的Python3.12或Docker；前端定向Vitest及最终build。独立阶段先完成可验证的实现，后续验收依据设计第10节。

进度补充：0–6实现及定向检查完成；7契约/构建/Linux及真实HTTPS合成链路完成；8 HTTPS轻量试运行，单次真实模型生成、公开混合检查及备份副本恢复完成。用户已确认真实邮箱收信及登录；正式额度已应用并核实为平台20/100元、每用户10/30元（日/月）。浏览器完整私有科研业务、远端嵌入/AI并发/解析峰值未验收，不能勾选全部完成。
