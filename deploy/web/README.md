# 4GB共机网站部署

当前工作区源码为来源。所有镜像在本机/CI构建，服务器不编译。保持考试大王原项目、数据和配额；储能使用独立目录、SQLite和卷。

## 准备与迁移

1. 运行`scripts/web/server_capacity.py`取得实际资源。2026-10-14只读快照物理内存3655MiB、available2330MiB、磁盘13.17GiB；不是负载峰值验收。
2. 构建并导出两个镜像、复制`compose.web.yml`及`.env.web.example`到`/srv/energy-research-web`。域名为energy.viyao.cn；边缘网络已核实为exam-king-beta_edge。
3. 用户已选择沿用既有SMTP邮箱作为管理员。`scripts/web/bootstrap_server.py`在服务器私密生成新环境文件，保留已有.env.web，不输出凭据；禁止将真实.env放进源码、日志或镜像。
4. 启动之前显式迁移，不让Web进程自行升级数据库：

```sh
cd /srv/energy-research-web
docker compose -f compose.web.yml --env-file .env.web config --quiet
docker compose -f compose.web.yml --env-file .env.web run --rm --no-deps backend python -m alembic upgrade head
docker compose -f compose.web.yml --env-file .env.web up -d --no-build
```

首次是空库，不导入本机私人论文/笔记。已有库先用一致备份并保留受管文件；0031的owner0属于原桌面用户，不公开。0031不自动降级合并不同用户，需恢复兼容的改前备份。

## 域名与入口

DNSPod新增energy A指向115.159.51.147。追加`energy.Caddyfile`站点块到既有Caddyfile，保留原全局和viyao.cn块；先保存配置副本、validate，再reload。

现有Caddy可以经原edge网络访问新energy-web别名，无需增加80/443监听或重建考试大王。API没有发布主机端口。AUTH_TRUST_PROXY只在此入口覆盖X-Energy-Client-IP、Next转发、API无直接公网入口的部署中启用。

公开知识名单由frontend/components/auth/routes.ts定义；API公开名单由backend/app/web_access.py定义。私有数据不公共缓存。邮箱会话是host-only、Secure Cookie；正式登录需HTTPS。

2026-10-15账号入口区分注册与登录：新用户通过`/api/v1/auth/register`创建验证账号，`/login`仅登录已有账号；验证码`intent`为login/register时会先检查账号状态。游客登录为公开浏览弹窗，不创建账号或科研会话。已有用户与会话无需迁移。

## 资源与费用边界

新Web/API上限256/512MiB、CPU0.25/1核。实际服务器不是4096MiB，需要混合负载后判断持续容量；不按配置上限宣称支持某个用户人数。

首版原生PDF最多100页、30MiB、提取文本2M字符，解析并发1；每人受管PDF/CSV/导出等总量200MiB；表格5MiB/10000行/200列。重型OCR/视觉/语音/全库重建及个人自动订阅关闭。轻量镜像不含Pandoc，Markdown/文本可导出，依赖Pandoc的Office导出尚未开放。

LLM与嵌入的单次预留额默认0，真实付费调用关闭。配置供应商密钥、模型及经过核实的费用预留后再开放。账本是保守额度占用，实际费用字段保持未知，不能当供应商账单；失败占用不释放，不自动重试。已有桌面输出预算保持，不能压低科研深度来模拟性能提升。

用户批准复用本机正式DeepSeek V4 Pro配置，scripts/web/reuse_local_model.py只读解密本机数据卷，以受校验SSH stdin传入新站.env.web，不输出或保存临时明文。该脚本保持预留0，开放须另设单次预留。2026-10-14[官方价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)高峰输入未命中9元/百万tokens、输出27元/百万tokens；Web文本请求最多128000 UTF-8字节、64000输出tokens，超限拒绝而不截断，思考模式保持。按公开ByteLevel分词器推算内容最大约2.88元，可设3元保守占用；这不是托管分词器/实际收费的合同保证，价格变化需重核。用户确认的正式试运行额度为平台每日20元/月100元、每用户每日10元/月30元；每次保守占用3元，故每用户最多3份单独报告/UTC日。三类报告应从各自入口逐次生成，旧聚合入口已停用。

本机嵌入为Ollama/BGE-M3，不能直接迁到4GB共机。远端嵌入接口已实现但尚无供应商配置，跨论文向量检索保持不可用。模型全站默认配置在服务器环境文件管理；现有系统设置中的UserSetting仍属当前管理员用户，不能作为全站模型设置发布界面。

## 验收和恢复

验收HTTPS/证书、真实验证码收信、两个用户私有数据、PDF上传/阅读/笔记、选定模型证据问答，以及一次共机负载和测试数据备份恢复。健康接口只证明服务/存储可用。

保留上一对Web/API镜像和schema/备份点。纯Web可独立回退；迁移后不能只换旧API。Caddy异常恢复其改前配置并验证考试大王。新项目不得使用down -v或清理旧项目卷。

未完成容量、真实模型费用和业务验收时，只报告已确认的功能与限制。部署状态以CURRENT_STATUS.md最新记录为准。
