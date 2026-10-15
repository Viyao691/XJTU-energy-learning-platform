# 最新验证报告 · 2026-10-15

## 首页电脑端菜单对齐

- 仅CSS改动；Docker生产构建及类型检查通过，原有autoprefixer警告保留。不新增镜像实现的CSS单测，不重跑业务套件。
- 浏览器1920×1080：系统菜单与入口均245.900009px宽、x1469.287475px，菜单文字22px；选中入口::after内容none。实际截图已观察并保存desktop-menu.jpg。
- 浏览器360×800：菜单宽160px、字号14px、伪元素none、页面宽360；手机紧凑尺寸保留。已恢复视口并关闭本轮临时预览标签。
- 本地Docker最初未运行，后台启动已有Docker Desktop后构建完成。发布包6,662,572字节，仅前端；Web BUILD_ID 8yDvKZd36uWibrAIGi575、服务器image ID faa92d8b2180683376bbdd9e499415632821ed1159a54dc9b528de91fb8dc62e；服务健康、真实HTTPS /dashboard 200且版本匹配。

## Web紧凑布局、密码登录与正式Logo

- GitHub交接分支推送成功，ls-remote匹配 `15ecb811b018a33a01395d0a8d77133c35f07241`。私有Page五个本轮新附件（源码1,727,655字节、静态素材6,948,042字节、审查3,061字节及两张手机截图）均file_access_confirmed=true；读回确认提交/BUILD_ID与五份引用存在。

- Python3.12密码、验证码、Web集成、迁移组45passed；密码校验不回显输入1passed。0033在隔离SQLite升级/降级保留账号会话。Linux生产依赖镜像临时库实际HTTP注册200、错密码401、密码登录200、读取会话200，未发邮件或调用模型。初版检查脚本会话工厂名写错，改为项目make_session_factory后通过，不是生产缺陷。
- 前端web-auth24、WorkspaceShell7、homepage-photographic5、branched-nav3共39passed。新Logo公开资源测试先失败，修复brand白名单后通过；branched-nav旧清单18更新为现有20项，仅补已存在的编年史与城市应用。没有跑全量套件。
- 最终Docker Web生产构建含类型检查通过，BUILD_ID SeH-5j_0F2ZiqrBHeV3rc；既有autoprefixer警告保留。仅针对实际手机观察发现的Logo资源拦截、关闭按钮被遮挡、菜单字号过大修订后重建；无后续未构建CSS。
- 360×800登录卡495.6px、注册卡536.2px，document宽360/高800；390×844卡片底681.4/701.7，无水平溢出。长邮箱在151.6px内换行，账户卡122.4px高、底743px。最终首页菜单160×261.8px、文字14px/点击44px；Logo浅深两图均实际加载。验证码/密码切换、游客框、抽屉关闭、隔离合成账号登录进入论文库均浏览器实查。
- 发布包7,903,654字节含API源码、Alembic0033、Web编译产物和Logo。服务器4份认证/迁移文件摘要、Web BUILD_ID匹配；先一致备份，再迁移0033，原web_users2/web_sessions3/papers0保留，API/Web健康。新镜像均web-20261015-compact；真实HTTPS登录/健康/Logo为200，登录HTML含密码表单和忘记密码。
- 正式浏览器旧标签刷新及新只读标签打开超时；未把本地截图冒充线上账户流程。未做实际Android/iOS/软键盘测试；不调用付费模型，不发生产验证码。

## dot 云端交接

- 补齐deploy/web与交接资料入口后的最终源码ZIP1,713,771字节，必要文件和ZIP完整性通过。最终GitHub HEAD `cc79ca55acac9f7209021faf3c7ce69065026d87`，ls-remote只读匹配；资料页源码附件已换成最终包。

- GitHub新分支推送成功，提交 `6bc31ba3b4bc1cf75478988a479d1b2d15e6e0b3`；基于main `3c97a48e17519f009a7eaa145d742e2558e81f78` 叠加240个当前源码/素材文件，没有改动main。
- 代码快照1,708,587字节，必要构建文件（Next配置、锁文件、轻量后端依赖、Alembic配置、Web Dockerfile、Compose、静态资源优化脚本）存在，ZIP testzip通过。静态图片叠加包6,917,300字节。
- 可编辑手机巡览素材1,053,209字节、36张截图，跨系统生成脚本compile语法检查通过；本次未重复渲染原视频。
- 视频、审查Markdown、线上截图、代码ZIP、素材叠加ZIP与视频可编辑ZIP上传结果均file_access_confirmed=true。私有Page已插入六个真实文件引用和GitHub分支/编辑说明。
- 未重新构建/部署网站，未验证dot实际云端运行环境、真机浏览器或真实付费科研流程。

## Web手机适配

- title-motion2、workspace-shell7、markdown-mermaid13、learning-analytics5共27passed；reader-refinement6passed（新增Web手机逐页图像、原件入口与翻页）。学习活动图测试曾以900>280失败，修改后5项通过。没有运行全套或首页哈希。
- 最终Docker Web构建成功、含类型检查（Next15.5.27）；BUILD_ID Y9lh0Lu-TpxDM0gFSJ-jC。原有autoprefixer警告保留。每次必要重建均对应逐界面发现的具体剩余问题，最后一次只有储能史手机照片contain/关闭动画。
- CUA实际检查24种页面布局，390×844本地Dev初查与360×800生产构建复核；学习全部页签、引导1–7、注册/登录/游客、订阅/证据抽屉、地图切换、笔记、原文翻页、数据表格、报告流程图与缩放均有截图。具体记录见docs/mobile/2026-10-15-mobile-audit.md。
- 实读最终手机活动SVG viewBox宽249.6；流程图100%适配容器，125%宽284.5/容器256/scrollWidth313，可放大滚动；PDF原文图像按完整比例显示；数据详情修复后整页scrollWidth345<=360、表格宽279.2。最后照片object-fit=contain、图片框319.2×260、整页345<=360。
- 业务数据来自独立无卷测试容器，全部为合成布局记录。自测提交实际返回判定；模型引导仅Mock测试。早期Failed to fetch为本地Dev进程停止，恢复后请求完成；fixture question_type字段曾无效，修正为multiple_choice。未作为生产后端缺陷处理。Ollama索引在测试环境不可用，未验证真实科研问答或真实模型生成。
- 发布包6,659,544字节，仅更新服务器frontend，最终服务器Web image ID97e8bcfff220072d94562540c08992868ebd0f546399e1f72dc49151fb4d4d98；Compose健康；真实TLS HTTPS /login 200且BUILD_ID匹配。线上390px论文库实际截图已查看，当前账号论文数0。
- 视频1080×1920/24fps/126秒/36视图/4,682,585字节；FFmpeg完整解码3024帧、退出0。36张源图逐张已观察；为无声截图巡览，不冒充连续录屏、真机实测或科研结果。
- 线上最终390px实读document.scrollWidth375、标题25px；隔离预览容器和Dev服务已停止，临时标签关闭、视口恢复。最终照片CSS已复核，无后续未部署样式。

## 2026-10-15 登录页视觉修订

- web-auth21passed（3.33s）；最后主题恢复修复后workspace-shell7passed（6.53s），含原首页壳、主题和导航行为。未跑全套或首页哈希。
- 最终Docker Web构建成功，含类型检查；BUILD_ID X2k2_WsiPUFlOk6E7C3bv。本轮针对浏览器发现的旧header样式覆盖、手机断句/深色input覆盖、刷新主题缺失进行了必要修复和重建；既有autoprefixer警告仍在。
- 独立访客预览使用生产镜像，桌面双栏截图已查看；390×844手机单栏card宽343.2px、document scrollWidth375px，无水平溢出，注册切换及原生游客dialog显示正常。最终同一CSS已读标题按句换行；最终构建刷新后theme=dark，邮箱input背景rgb(23,42,46)，恢复主题正确。没有发信或真实注册/模型调用。
- 发布包5,675,222字节，服务器只更新frontend并保留旧版本环境；Compose frontend healthy，服务器Web image ID 7fc40bea184cb41d57c0a4855790405c1af16b932cf974d2fa28169a36a0ec94。真实HTTPS /login 200，HTML中的BUILD_ID和web-auth-layout/欢迎回来核对通过。临时容器和预览标签清理、视口恢复。

## 2026-10-15 账号入口与游客交互

- 后端test_web_auth/test_web_integration共27passed（122项既有警告）；新增注册/未知账号登录/重复注册/验证码intent先检查账号的测试先红后绿。前端web-auth21passed，覆盖模式、注册提交、游客入口与身份卡。未跑全套。
- backend/openapi.json与frontend/lib/api.generated.d.ts同步（159路径/213schema）。新后端Linux image_smoke通过，fake SMTP/合成PDF，两用户隔离、非root与SQLite3.54；无真实发信或模型调用。
- 最终Web Docker生产构建通过，含类型检查；既有autoprefixer警告未改。审查及浏览器发现全局!important按钮样式覆盖，局部auth.css修复后必要重建；最终BUILD_ID ZSBLPGtFH01m3RXI_IxoX。
- 线上账号卡横向完整显示，宽199.2px，用户已有管理员会话保留。独立localhost游客预览使用同一生产镜像，验证注册页/切换、原生dialog、ESC关闭并恢复游客按钮焦点、进入/dashboard。最终深色模式实读选中背景rgb(36,70,95)，未选中透明；弹窗返回按钮透明、进入按钮rgb(25,62,91)。Tab观察未作为焦点循环成功证据。
- 最终运行包6,672,278字节，服务器复用旧依赖镜像打包，仅更新新站。代码摘要和BUILD_ID匹配；Compose两服务healthy，HTTPS ready返回database/storage/queue均ok。临时预览容器删除，浏览器视口恢复。未发送真实注册邮件，不重复AI调用/负载测试。

## 2026-10-14 登录确认与正式额度应用

- 用户明确确认网站登录成功；服务器只读核实非测试验证用户1名，不输出邮箱或会话。真实收信/登录结果来自用户本人确认。
- 修改前运行任务/模型调用均为0；仅调整新站私密环境并重建后端容器，未改源码镜像/数据库/会话或考试大王。
- 运行配置实读：平台日20/月100元、每用户日10/月30元、单次占用3元；本UTC日平台余额17元。HTTPS ready返回status=ready、database/storage/queue均ok。
- 同步.env.web.example、额度脚本及部署/状态/计划。没有再次调用付费模型、重建镜像或重复负载/套件。

## 2026-10-14 公网轻量实施验证

- 最终API镜像manifest633562715457bacdabab06641d74e464f74355a0bfb78874b3315a045deb17b2，包含DeepSeek费用请求边界，Linux运行smoke再次通过。正式Web manifest3e85ea1e0d6fd7a4ec8c13ed2b742e19b0a3a081203015af93b63759e82721e7；两端镜像身份相同。启动检查最初误用config ID，诊断修正；前端健康检查最初因HOSTNAME绑定容器名失败，Compose改0.0.0.0后健康。
- 服务器空库显式迁移并启动两容器；Caddy备份/validate/reload成功。新站HTTPS证书正常校验：help/ready200、私有论文401；原站health200。本机旧NXDOMAIN缓存导致普通解析仍失败，验证使用已核实A记录curl --resolve，未关闭证书验证；浏览器正式登录页能正常打开。
- SMTP TLS认证、DeepSeek/models权限和型号可用均通过，没有发送测试验证码。真实HTTPS临时会话/PDF/笔记/任务与文件跨用户404、admin403/OCR503检查通过；SQLite backup副本integrity_check及笔记/PDF恢复通过。初次脚本对Caddy/API合并Cache-Control头精确匹配失败，改为no-store且无public语义后完成；无产品缓存变更。测试账号/私有数据清理，未触碰其他用户。
- 单次真实DeepSeek快速理解返回957字符、AI归纳（待原文证据核验）；按3元保守占用入账，actual_cost仍未知。使用无实验结果的合成文档及临时会话，通过真实HTTPS请求；不证明真实论文的科研分析质量。仅保留无会话测试身份及费用账本，私有测试数据清理；不自动重试。
- 一次约10分钟公开dashboard/help及两站健康接口混合1116请求：1115次200、1次error，P95 0.196秒，最低可用内存1988MiB。期间含API配置重建，未记录逐URL错误来源；后台重建后PID变化导致其进程RSS非连续采样。不是零失败、真实模型双并发/解析峰值或浏览器首屏验收。服务器/srv/energy-research-web/load-result.json保留原结果。

- 后端定向组：test_web_auth/ownership/migration/pdf_limits/integration/model/embedding/provider_expansion，共77passed、107warnings。旧库迁移发现SQLite批量重建会级联删除子记录，修复后旧Paper/Note/Source均保留owner0；空库迁移通过。
- 后续限额组：新增web_limits7项及已有有效PDF下载1项通过；web PDF与HTTP集成3项通过。原生解析共用单槽，2M字符、租户PDF/CSV/导出总量和下载发表前容量覆盖。新增DeepSeek请求边界3项受控fakeHTTP测试通过，无真实模型调用。
- 代理IP补充4项、认证17项；前端auth17项、dashboard7项、图片优化合成1项通过。正式frontend Docker构建（含Next15.5.27、最终备案页脚）成功，config ID175a704c071a47d0d85216e711a0c9eac54d3ce1e1bc4c5be48d3227db234423。
- OpenAPI和前端类型已一起生成，158paths/213schemas。部署素材253个源/输出文件，240670242→224370524bytes，13个优化文件；这是包体/磁盘节省，不是LCP或网络性能测量。
- 后端Linux镜像运行scripts/web/image_smoke.py通过：SQLite3.54.0、UID10001、无Torch/Paddle/Docling/Whisper；临时空库Alembic、假邮件登录、合成PDF上传/任务ID/笔记、两用户隔离、admin/OCR边界。该检查发生在最后DeepSeek请求边界加入前，最后镜像构建在继续。
- DNSPod界面保存成功，外部1.1.1.1解析energy.viyao.cn为115.159.51.147。服务器新目录、私密SMTP/管理员/model配置创建成功；付费调用仍关闭。网站HTTPS、真实收信/模型输出、混合负载、恢复演练尚未验收。
- 当前源树包含用户原有未提交变更，未自动提交、重置或搬运。未运行全量套件/首页冻结哈希；实际检查只支持上述范围。

## 2026-10-14 公网部署方案只读核查

- 核对活跃Harness当前源码及考试大王本地部署配置；已有账号/所有权隔离缺口、Ollama默认依赖、重型运行库和3552MiB已有容器限额合计均据当前文件记录。
- 本项目`docker compose ps --format json`成功，输出为空；没有启动、停止或重建服务。
- 实际GET `https://viyao.cn/api/health`返回HTTP200，正文为`{"status":"ok","database":"ok"}`。本机查询`energy.viyao.cn`返回DNS名称不存在；未修改DNS。
- 静态目录一次体积统计约228.4MiB，不等同于首屏传输量。设计候选预算合计4096MiB；实际主机资源、负载峰值、SMTP、远端嵌入及优化后性能均未验收。
- 仅新增部署草案并更新状态/计划/本报告；未改应用源码、调用模型、登录生产主机、调整在线配额或执行测试套件/应用构建。

## 2026-10-14 参赛文件定向检查

- 简介最新批注修订：删除“包括关键字、作品概要……300字以内”填写说明段，保留正文和表格；最终PDF单页，文字检查及渲染查看完成，桌面Word/PDF同步替换。

- 最新个人承诺书：按用户指令仅删除开头“／本团队____________（团队名称）”，桌面修正版DOCX/PDF已替换；PDF单页、该文字不存在、填写线与原签名保留，最终渲染已查看。

- 后续原格式修正版：承诺书保留原“本人／本团队”结构、未使用团队空线、签名栏及原签名，填写内容使用下划线；简介恢复原表格说明并在同一单元格内填写250字正文。两份PDF均1页，Word导出及最终逐页渲染查看完成。非正文包部件继续逐字节保留，支撑ZIP未修改。

- 官方简介和承诺书：各1页PDF；简介250字；用户提供的原签名媒体、关系、样式、页脚等非`word/document.xml`部件保持原样。正文仅填写相关字段，保留原承诺条款。Word导出并用Poppler渲染，连同12页支撑PDF共14页已逐页查看。
- 支撑ZIP：24个文件，5,257,288字节，小于100MB；`ZipFile.testzip()`通过，包含4份PDF及设计/公开数据复现/许可资料，无视频或DOCX。
- 临时副本实际执行`rerun.py`成功：11个模拟工况效率均值95.32545454545453%，样本标准差2.311793086054044个百分点；输入原件未改动。记录见`tmp/competition-20261014/verification.json`。
- 本轮访问历史后端8001端口连接被拒绝；未确认当前业务可用性。公开仓库页面可访问；未调用模型、重建、启动应用或运行全量测试。资料中的学习和科研案例分别标明2026-10-08及2026-10-04历史日期。

## 2026-10-14 参赛PDF V6与Visio图源

- Microsoft Visio 16.0 InvisibleApp创建六页图源，VSDX及六张SVG导出成功；ZIP/XML核对六页原生形状67/48/35/37/31/22，Foreign=0，图源46088 bytes。原生PDF导出内部错误，使用SVG矢量转换路线。
- 临时svglib字体映射初次回退，显式登记宋体与Times文件后修复。转换发现曲线默认黑填充及marker/tspan不兼容，已显式填充、箭头及混合脚本位置规范化，原SVG和图源保留。
- `verify_report.py --visio`最终12页540×960 pt、7613可检索字符、4082208 bytes、文本边界问题为空。全部联系表与第3/5/7/10页全图已查看；字体span检查显示Helvetica/Times-Roman可见文本为空。记录在 `tmp/pdfs/visio-report/validation.json`。
- 未运行应用测试/重建/冻结哈希，未调用业务模型或变更用户数据库。临时SVG转换库安装于 `tmp/visio-svg-runtime/`，产品依赖未变。

## 2026-10-13 交晓智原生智能体与研读工作流

- 初始JSON工作流：三个节点“运行成功”，20349ms、2572 Tokens。仅使用明确标注的功能测试摘要，结果保留证据范围和缺失实验信息。
- 输出改为Markdown后的必要复测：三个节点“运行成功”，25563ms、2646 Tokens；收到Markdown结构化研读报告。最终发布工作流版本1.0.0。
- 智能体联通：一条摘要测试消息，实际执行记录显示“工作流 能研智助_储能论文证据研读 调用”，工作流23.94s；整次回答73.924s、12450 Tokens。最终回答明确“仅摘要（功能测试用非真实论文摘要）”，列出未提供的温度、填料比例、图表与数值。
- 智能体v1.0.0提交后，平台明确显示“智能体配置已发布成功”，渠道页显示“运行中”。随后学校渠道提交弹窗显示“已提交发布”，需要到审批中心查看进度；[截图](docs/handoff/2026-10-13-jiaoxiaozhi/approval-submitted.jpg)。尚未验证审核通过或学校智能体中心已上线。
- 已通过文件选择器上传并保存已有正式Logo至工作流和智能体。Web访问权限设置被自动审批拒绝，未启用Web/API/MCP等集成开关，未生成密钥。
- 未运行原项目pytest、前端测试或构建，未改原产品代码或运行服务；未验证真实PDF上传、长论文分析、联网检索、导出或原私人数据库接入。


## 2026-10-11 GitHub 介绍与展示视频

- 在线播放入口提交 `3c97a48e17519f009a7eaa145d742e2558e81f78` 推送成功；GitHub API实读相同main，README blob `4819bc70c01cc82d3cf522a5fc70a898479546e6` 与本地一致。main及播放页两个发布目录clean，本地测试服务器已停止。

- 完整视频在线播放：GitHub Pages原先不存在，独立 `codex/video-demo` 分支 `c2c9730` 发布成功，API网站及构建状态均built；播放页直接引用同一份Release原视频。
- 本地真实浏览器：duration315.285333秒、readyState4；点击播放成功，currentTime实读9.712984秒。公网HTML200且与已测HTML逐字一致；视频1024字节Range请求206，`bytes 0-1023/221642366`。
- 公网浏览器导航及重绑定各一次超时；未做公网整片播放、跳转或移动端实际检查。README/文档空白检查通过。

- 后续“解决的问题”重写：章节隔离检查通过，正文有五个独立小标题，README 其余内容完全一致；Markdown 空白检查通过。提交 `351a58a` 经本机系统代理推送成功，未增加素材或运行应用测试/构建。

- GitHub API 确认公开仓库、当前账号管理/推送权限及初始 main `c0751e1fe7d0e48256b09ab34fbeb503bfce0d46`，与独立发布目录一致。仓库改名、简介与主题标签更新返回成功。
- README 本地文件链接检查通过；十九张静态截图与一份八秒 GIF 存在，指定删除段落与旧仓库名均已从 README 移除。提交前 Git 空白检查通过。
- 用户指定原视频 FFprobe：H.264/AAC、1920×1080、30fps、315.285333 秒、221,642,366 字节；未转码上传。GitHub Release 发布成功，上传状态和原文件字节数一致。
- `7b95b393f37d6d2bb691d49492bb893517f23db7` 推送成功；GitHub API 实读 main 同一提交、README blob `ec9168eb97b83ba2d1a6da75be6a03b58c2b8818`、二十处展示图片引用、指定段落和旧仓库名均不存在，视频 Release 公开且完整大小吻合。视频正式下载链接使用 `platform-demo-2026-10-11` 标签；独立发布目录最终 clean。
- 本轮为介绍与素材调整，未运行应用测试、构建、真实模型请求或重打包便携 ZIP。

## 2026-10-10 Remotion首页末段衔接（7.5秒修订）

- 首页只在末段进入，早段hero为reading；225帧完整Player导出成功，实际标题背景/裁剪问题修复后仅补f186—223共38帧，再编码最终MP4。最终源码npm run check exit0。
- 一次最终转场FFprobe记录：1920×1080，30fps，225帧，7.500000秒，H.264/yuv420p/tv/BT.709，无音轨，3,043,349字节。记录在新工程renders/media-info.json。
- 实际查看170/210/224末段采样、修正210帧及最终联系表；连续预览查看接缝221—228相邻帧，首页位置、尺寸、角度连续。未整段实时播放/音频试听。
- 预览初次298帧：静态PNG网格输入默认25fps；固定30fps后312帧：原录屏可变时间戳尾帧被截掉。将原88帧按N/30重置时间戳、固定CFR后，最终预览313帧/30fps/10.433333秒，4,319,136字节，含音频，记录在renders/preview-media-info.json。用户原文件未改动。
- 源码与素材：output/video/remotion-home-handoff-2026-10-10/。预览去上下播放器/录制HUD，主内容未拉伸。未运行产品测试/构建、冻结校验或操作ChatCut。

## 2026-10-10 Remotion黑色网格转场（独立视频素材）

- 最终动画由同一src/Transition.tsx的useCurrentFrame计算；完整184帧Player截图与FFmpeg编码成功，npm run render exit0。
- 实际查看Remotion Player第65/183帧PNG（1920×1080）及最终MP4抽出的12帧联系表。确认真实界面、中文标题、三卡构图与固定网格；未整段实时播放。
- 一次最终FFprobe结果已保存renders/media-info.json：video-only H.264，1920×1080，30/1fps，184帧，6.133333秒，yuv420p，color_range=tv，BT.709，1,940,849字节。PNG RGB仅执行一次limited-range转换。
- 本机标准CLI的Edge CDP启动失败；独立截图成功后改用Remotion Player+PowerShell隐藏启动Edge，无CDP按帧截图。Chrome Headless Shell下载未完成，未用作最终渲染器。没有修改系统浏览器策略或关闭用户浏览器。
- 工程：output/video/remotion-black-grid-transition-2026-10-10/；无产品测试、产品构建、冻结校验或ChatCut工程改动。旧浅色初稿保留。新增Player导出入口后，最终源码npm run check（tsc --noEmit）exit0。

## 2026-10-10 Remotion独立转场（视频素材）

- 独立工程npm run check通过（TypeScript）；实际Remotion整段渲染两次exit0，第二次针对首版实际画面中前景遮挡、行业长截图中段取景两处问题修正。
- 查看首版12帧联系表、品牌帧和末帧；查看修正版联系表与末帧确认两处修正。未整段实时播放，不以采样帧代替全片播放验收。
- 最终FFprobe：H.264、1920×1080、30/1 fps、210帧、7.000000秒、yuv420p、color_range=tv、BT.709、2,905,592字节，仅video流；已从JPEG渲染的full-range规范化为limited-range。
- 本轮未运行应用测试/构建，未修改应用或正式ChatCut时间线。视频与工程位于 `output/video/remotion-painpoint-transition-2026-10-10/`；当前正式视频仍为8784帧。

## 参赛作品介绍PDF（文档验证）

- V5示例图式与字体修订：原生重构架构/RAG/任务分支/学习环路/OPC反馈图，内置image_gen插画作局部配图。字体检查发现旧映射仍让三线表表头使用微软雅黑，改为独立宋体字体族后，最终资源为SimSun和Times New Roman系列（默认Helvetica未用作标签）。`verify_report.py --refined`：12页540×960 pt、7629可检索字符、6549302 bytes、文本边界问题为空。全部联系表及第4/5/7页全图已目视检查，修复第5页英文对象名拆字换行后近看通过。记录在 `tmp/pdfs/refined-report/validation.json`。构建初期第7页超过正文区14.4pt，缩紧学习图后通过；未运行应用测试或业务模型。

- V4图式与公式修订：当前源码确认嵌入L2归一化后以内积计算余弦得分；公式改为向量定义、二范数分式与编号。内置image_gen编辑架构/RAG两图，统一原生流程配色。`verify_report.py --publication`：12页540×960 pt、7153可检索字符、6429003 bytes，文本边界问题为空；全部联系表及第4页全图已目视检查。记录在 `tmp/pdfs/publication-report/validation.json`。只修改报告与记录，未运行应用测试或业务模型。

- V3论文汇报版：12页540×960 pt，7139可检索字符，6646132 bytes；宋体首行缩进、三线表、连续章节及图注。内置图像模型生成2张学术示意图，RAG连接经一次定向编辑纠正为embedding→SQLite→cosine ranking。全部页面渲染、查看联系表，近看第2-4页三线表/架构/RAG/公式，文本边界无越界。`verify_report.py --academic`结果在 `tmp/pdfs/academic-report/validation.json`。未运行应用测试或重新调用业务模型。

- V2评审修订：按七项必需内容重写，新增业务架构、输入处理与技术架构、AI任务编排表、学习对象关联、实践双路径；用户原始视频通过OpenCV只读提取学习包画面。最终14页540×960 pt，9018可检索字符，4105466 bytes。所有页已渲染并检查联系表，近看第5页架构；最后架构文字修订后检查无越界。只读API再次核对知识库、学习概览、订阅与15项科学配方；没有调用模型或修改用户记录。V1检查记录如下。

- ReportLab生成14页正式报告；PyMuPDF打开、提取、渲染全部页面。页面全部540×960 pt（9:16），正文可检索8894字符，包含作品名称、关键词、概要、痛点、创新、场景与成效，中文字体嵌入。
- 目视检查两张全页联系表，近看咨询/学习循环及架构。修正复习回到卡片箭头与图中多行文字；最终所有文本块页面边界检查无越界。最终PDF约4.30MB。
- 2026-10-08只读8001健康/数据库ok；资料索引35篇中33篇有索引/2678分块；学习包个案2来源/14卡片/15题/2开放薄弱项，存在其他失败与待生成；订阅3条、均启用、有成功记录。未测试教育效果或商业指标。
- 验证脚本：`docs/competition/2026-10-08/work-introduction/portrait-report/verify_report.py`；记录与页面在 `tmp/pdfs/portrait-report/`。本轮没有产品行为变更，未跑应用全套、构建、哈希冻结或调用用户模型。

## 科研想法与实验设计删除

- 后端删除回归：RED两项405，GREEN `backend/.venv/Scripts/python.exe -m pytest tests/test_research_assistance_phase6b.py -q -k 'delete_idea or delete_experiment_design' --disable-warnings`，2 passed/7 deselected。覆盖同事务关联删除、单个设计删除、其他记录保留、来源数据集保留并解除关联、缺失404。
- 前端 `npm.cmd --prefix frontend run test -- tests/research-tools-flow.test.tsx -t "delet"`，3 passed；覆盖数量确认、取消/失败保留状态、成功列表与编辑清理。
- 导出OpenAPI及生成前端类型exit0；一次frontend生产构建exit0，复用现有后端依赖仅COPY源码构建exit0。3001/8001部署并等待healthy成功。
- 隔离Edge实际页面：创建临时想法与3个同名设计；取消不删；单删后保留想法和2个设计；删除想法确认显示2个、全部关联设计404，编辑区清空，pageerror=[]。仅临时记录已清理，不操作既有个人记录。
- 验证脚本/日志在 `outputs/idea-delete-2026-10-07/`，不上传GitHub；未调用模型、跑全套或重打包Windows ZIP。

## 论文流程图兼容与DeepSeek输出预算

- 后续按用户明确指令“用codex帮助生成，别用deepseek额度”：Sol依据现存正文与本地提取证据补齐4篇中6份末尾图，图前正文逐字符保留，未新增数值或页码，图注/证据状态记录Codex归纳。隔离Edge以只读API响应替换预览6份报告共8图，全部ready且pageerror=[]；然后事务写回本地，仅更新指定6个报告字段及证据状态，逐字段GET API确认内容一致。没有DeepSeek/API模型调用；预算调整尚无真实64k请求验收。
- 写回第一次试图更新不存在的updated_at字段，事务回滚；移除后写入成功。prompt_version追加Codex后缀使当前版本筛选返回空报告，发现后恢复原兼容版本号，以图注/证据状态记录补图来源，最终API校验通过。原记录备份与修复稿、预览日志在 `outputs/paper-render-2026-10-07/`，不上传GitHub。没有重新构建或重复UI检查；写回内容与预览相同。
- 只读复现论文36三栏目：快速2图/1 ready、通俗2图/1 ready、审稿人1图/0 ready。失败完整图含未引号 `NLFMO||HC`；另外两图的API原文结束于半截节点，不是前端删去内容。只读资料查询还找到4篇中的6份明显残缺图尾，未变更记录。
- 前端新增特殊字符标签回归：red 1 failed/12 skipped；green `markdown-mermaid.test.tsx` 13 passed，3.31s。
- 后端最终命令（backend cwd）：`.\.venv\Scripts\python.exe -m pytest tests/test_paper_analysis.py tests/test_provider_expansion.py tests/test_paper_experience_api.py -q -k 'report_rejects_obviously_incomplete_mermaid or report_accepts_completed_mermaid or deepseek_paper_reports_keep_thinking or deepseek_length_response or deepseek_rejects_incomplete_diagram or failed_report_keeps_previous_content_and_records_failed_task' --disable-warnings`，12 passed/57 deselected，16 warnings，2.19s。覆盖实际未围栏图尾、围栏/CRLF、完整图与后续正文、DeepSeek三报告64000、length分支、失败保留原报告。
- 一次frontend生产构建exit0；基于现有依赖镜像仅COPY后端改动的构建exit0，保留旧镜像标签。3001前端及8001后端更新exit0。首次在后端重建期间提前读取health出现ResponseEnded/代理500；等待compose healthy后复查health=ok、代理论文数35。
- 最终Edge读取指定论文三个栏目：快速2/2 ready，通俗1/2 ready，审稿人0/1 ready，pageerror=[]。后两者仍是已保存内容缺失，未声称全部图修复。脚本与日志在 `outputs/paper-render-2026-10-07/`，不上传公开仓库。
- 未真实模型调用、未替换个人报告、未全套/截图/哈希检查；预算与失败分支用受控假响应验证，尚未验证真实64k请求。用户引用的原句未找到于源码及现存分析字段，原失败请求不可追溯。

## 自测选项与科学文本排版

- 修前隔离Edge复现：1920视口，radio布局宽1220–1325px、高13px，第二题数学节点0。
- 定向回归：`npm.cmd --prefix frontend run test -- tests/learning.test.tsx -t "renders quiz notation while submitting"`；RED 1 failed/22 skipped（题干缺少msub），GREEN 1 passed/22 skipped，测试428ms、命令3.75s。验证题干/选项/解析/参考要点渲染及点击标签后仍提交B，不改答案文本。
- 首次Docker前端构建在新增解析渲染的可空字段类型检查失败；加存在条件并清除radio继承padding后，必要重构建exit0，生产类型检查通过。期间本地tsc过滤学习页/测试路径无匹配错误，不声称全项目tsc无错误。
- 仅frontend3001部署exit0；最终隔离Edge1920深色、390浅色均通过：radio22×22px、同列对齐、文字间距12px、行高44px、选项在视口内、整行点击选中，第二题msub1/msup4，共5个KaTeX节点，KaTeX错误0、pageerror=[]。脚本/构建日志/结果在 `outputs/quiz-format-2026-10-07/`，不进入公开仓库。
- GREEN发生在可空解析条件小修前；最终版本由生产构建及上述页面检查覆盖。未提交真实答案、写入用户数据、调用模型、运行全套或重打包Windows ZIP。

## PDF 外层翻页修复

- RED：`npm.cmd --prefix frontend run test -- tests/reader-refinement.test.tsx`，31.28s，2 failed/3 passed；失败断言确认翻页与缩略图点击后 iframe 没有替换。
- GREEN：`npm.cmd --prefix frontend run test -- tests/reader-refinement.test.tsx tests/paper-experience.test.tsx`，13.70s；reader-refinement 5/5 passed，paper-experience 35/40 passed、5 failed。输出截断，只定位 HelpPage 工作流说明及 `Single paper` 标题断言；其余失败名称未恢复，未扩修复或声称整文件通过。
- 详情定向：`npm.cmd --prefix frontend run test -- tests/paper-experience.test.tsx -t "shows the local PDF, visual navigation and selected page preview" --reporter=dot`，2.78s，1 passed/39 skipped。
- 一次 Docker frontend build exit0，类型检查和生产构建通过；仅 frontend3001 `up -d --no-deps frontend` exit0。后端未重启，数据未写入。
- 隔离 Edge：固定初始第1页，修前下一页显示2但 iframe 保留、PDF loads=1；修后下一页2、缩略图4、上一页3均替换 iframe，PDF loads=4，最终src含 `#page=3`、browserErrors=[]。脚本在 `outputs/pdf-navigation-2026-10-07/check.cjs`。初期检查未固定起始页，图表自动选页使预期不符，改用 `?page=1` 后完成有效前后验证。
- 未人工确认内置 PDF 工具栏显示、未做其与外层页码双向同步、未跑全套或重打包便携 ZIP。

## Windows x64 便携运行时冷启动验收

- Windows 便携包构建一次成功；已安装完整 Windows 后端依赖。运行环境包含 Python 3.12、Node 24、Pandoc 和 OCR 运行库，启用本机 runtime proxy，初始 Mock 模式及空 `data`。
- 在路径含中文与空格的临时目录、且系统 PATH 无 Python/Node 的环境冷启动：health、首页、dashboard、runtime proxy 均 HTTP 200；空库初始化 Alembic 0029、campus seed 67。合成 PDF 上传 HTTP 201，页图与图卡 HTTP 200；DOCX/PPTX 创建 HTTP 201，下载文件为 PK 容器格式。
- 3100 已被占用，启动器成功避让并选择 3101；退出后 8100 与 3101 关闭。临时数据已删除，stage data 目录为空；既有 3001/8001 未改动。
- 最终 ZIP `Energy-Research-Copilot-Windows-x64.zip` 为 926,812,896 字节（约 884 MiB），`data` 为空，许可与素材清单在包内。GitHub API 确认 tag `v0.1.0-windows-portable` 的 Release 为已发布、资产 `uploaded` 且大小为 926,812,896 字节；下载地址为 https://github.com/Viyao691/energy-storage-research-learning-platform/releases/download/v0.1.0-windows-portable/Energy-Research-Copilot-Windows-x64.zip。
- 未做 Office 渲染验收、真实模型服务或 OCR 模型权重验收；未跑全套测试。

## 2026-10-04 科研想法排版

- Sol局部CSS与Astra规格/质量审查通过。两次Docker frontend生产构建与仅frontend3001部署exit0；第二次为复选框被通配input规则误伤、Markdown15px覆盖修正；后端未更新。保留无关既有构建警告，未运行单元/全套或hash。
- 最终1920×1080：entry/design/panel1552.8px，入口列710.21/784.98px；label/input/button/review Markdown均16px，checkbox18×18。390×844：entry/design单列335.2px，document scrollWidth375 <=390，无横溢；viewport恢复。初次尝试向disabled生成按钮发送键盘滚动失败，改为enabled保存按钮，仅滚动未提交。
- 只保留一张最终浅色桌面截图，[尺寸与截图](docs/handoff/2026-10-04-ideas-layout.md)。无真实模型、数据写入、全套或双主题截图矩阵；深色未单独渲染验收。

## 2026-10-04 科研功能补齐与真实验收

- 后端Python 3.12：`.venv/Scripts/python.exe -m pytest tests/test_research_tools_revision.py tests/test_research_assistance_phase6b.py tests/test_scientific_analysis_phase6.py -q --disable-warnings` 为15 passed/2 skipped、10.74s，154 warnings；本地Pandoc格式用例跳过。后续修订仅revision文件7 passed、4.49s，75 warnings。此前首次新测试从根目录运行存在导入失败，不计作行为red；前期缺陷实测及旧确认用例失败作为依据。
- 模型预算新用例red因缺少thinking开关失败，修后两定向用例2 passed、2.17s，24 warnings。PPT分页新定向用例先red无slide-level，green1 passed、2.16s；最后数组/文本摘要数值完整性修正后该项1 passed、2.04s，18 warnings。均使用受控模型/格式命令，不冒充真实AI或Pandoc结果。
- 前端新流程初始3 failed，green相关三文件9 passed、4.07s；现场旧统计诊断与复核计数修正定向red1 failed，green1 passed/5 skipped、2.21s。最终Docker前端两次生产构建均exit0、含类型检查；第二次专为现场缺陷。全局本地tsc有无关编年史测试TS2769，未称通过。
- 后端四次依赖复用构建exit0：初版、真实模型长度修正、PPT分页、审查指出摘要截断值修正；各对应部署成功Healthy。前端3001/后端8001端口、现有数据和配置保留。最终OpenAPI154 paths/207 schemas、TS207 schemas一起生成，后续无schema变化。
- 真实浏览器：双工作表各11行，质量缺失5/区间1，完整详情全部11行；旧确认未复核分析409，复核后analysis3/4完成。逐列诊断及旧版“未记录”显示正常，用户已核对2/待复核0。Table6均值95.32545454545453、样本SD2.311793086054044。
- 真实DeepSeek/deepseek-flash：候选首轮length失败未保存，局部预算/非思考修复后1次重试成功idea2；design1九字段保存且刷新恢复，1次真实审查成功553字符。仅选公开数据1、2，论文0。原候选极差比较错误及无映射跨表建议已如实保留，用户界面八字段人工纠正保存，不称模型科学正确。
- UI三格式：Markdown4、DOCX5、PPTX6创建下载；PPT6单页缺陷修复后PPT7最终下载200、7页，含效率均值及DOI，各页文本9–432字符。MD/DOCX下载200并包含真实数字，DOCX主XML有效。最终产物脚本exit0；仅下载CSV首行效率+11后 rerun.py重算均值从95.32545454545453到96.32545454545453，差1.0，线上数据未动。
- 完整[报告、数据与产物](docs/validation/2026-10-04-research-tools-completion/README.md)。保留两张最终视口截图；未全套、首页hash、Office逐页渲染、移动端或截图矩阵。无提交或历史测试数据删除。

## 2026-10-04 科研数据与科研想法真实数据评估

- 现有Docker 3001/8001，DeepSeek/deepseek-flash，使用Frontiers DOI 10.3389/fmech.2021.690793的Table 2/6公开数据各11行；保留缺失、温度区间与模拟来源属性。实测数据/响应见[完整报告](docs/validation/2026-10-04-research-tools/README.md)和[运行证据](docs/validation/2026-10-04-research-tools/runtime-evidence.json)。未改应用、模型设置或部署。
- 浏览器：CSV预览11×4、可见7数据行；错误单位JSON阻止提交；正确单位保存全部11行，5个缺失仍null、区间仍文本。XLSX双表预览成功，无选择器；通过API确认第二表。收藏/已读、1项收藏筛选成功，刷新两个数据集保留。手工想法保存及刷新保留，检查表创建显示9缺项但无编辑器，刷新后界面不显示旧检查表。Markdown框架界面生成成功。
- 真实模型两操作均502（访问日志确认）：候选选题生成、设计审查；没有成功候选或审查文本。一次64-token同提示诊断上游400 invalid_request_error，要求JSON模式提示中包含json；当前提示缺失，模型连接测试返回成功。未反复调用或修改配置。
- API：重复CSV409、TXT400；Table 2统计潜热均值199.463636 kJ/kg、样本标准差28.998768，含缺失/区间两列静默跳过。Table 6效率均值95.325455%、样本标准差2.311793个百分点，count=11，独立Python核对三项一致。数据缺失仍confirmed/confidence1.0的现象如实记录，不计为数据质量通过。
- Markdown下载404；DOCX/PPTX各201创建、200下载，ZIP结构/主XML有效，PPTX1页，未Office渲染。分析ZIP200含6文件、CSV表头+11行；源码/包中rerun.py只回显已存结果，没有重新执行算法。
- Sol在backend cwd执行 `.venv/Scripts/python.exe -m pytest tests/test_research_assistance_phase6b.py::test_csv_preview_confirmation_and_independent_dataset tests/test_research_assistance_phase6b.py::test_xlsx_read_only_preview_and_formula_rejection tests/test_research_assistance_phase6b.py::test_user_and_selected_evidence_ideas_and_experiment_checks tests/test_research_assistance_phase6b.py::test_markdown_export_uses_only_selected_evidence -q`：4 passed、6.47s、exit0，51条既有DeprecationWarnings，使用隔离Mock/SQLite。未将Mock结果表述为真实模型可用。
- 仅保存两张浏览器视口截图；fullPage截图不可用，未做截图矩阵、移动端、全套或构建。测试记录保留并标注，无删除原有数据。本轮完成测试评估，功能缺陷仍待实施。

## 2026-10-04 订阅主题内容隔离与储热检索

- Sol在backend cwd执行 `.venv/Scripts/python.exe -m pytest tests/test_research_news.py::test_thermal_storage_news_anchor_matches_specific_topic_not_generic_energy_or_ai tests/test_phase4_research.py::test_thermal_storage_subscription_sends_english_paper_query_but_keeps_saved_chinese -q`：red 2 failed、2.52s；green 2 passed、1.73s、exit0，3条既有SQLAlchemy utcnow提示。验证5个热储能中英文锚、排除泛能源/AI以及英文论文请求、数据库中文query保留。
- Sol在frontend cwd执行 `npm.cmd run test -- tests/subscription-detail-reading.test.tsx`：red 3 failed、1.73s；green 3 passed、1.72s、exit0。验证不调用通用日报、论文优先/主题新闻计数、全文摘要保留、中文失败重试及主题新闻空态。
- 主控核对运行research.py与本地修改前一致，最终仅一处英文查询映射变化；后端复用before-topic-subscription-20261004镜像COPY research.py/research_news.py，构建exit0。一次frontend生产构建exit0，含类型检查；既有无关CSS/缓存警告保留。3001/8001部署exit0，两容器Healthy。
- 实际执行两个订阅一次：液流id3/run12 success，发现50、新增18条文献、总58；储热id4/run13 partial，发现50、新增20、总60，arxiv暂不可用，其他论文源及5新闻源成功；两者主题新闻0。[接口证据](docs/handoff/2026-10-04-topic-subscriptions-runtime.json)。新增收录不代表新发表，其中来源可能包含补充材料元数据。
- 浏览器3001：两主题名称/query正确、相关论文50条在前、本主题资讯0在后、无能源与AI通用组；液流资讯页签卡片0并有明确空提示，error logs=[]。每页仍加载最新推荐最多50条，未扩展分页。浏览详情沿用既有自动中文整理，本次未等待或单独验证其模型输出；手动订阅检查不调用模型。
- 未全套、截图、移动端或模型质量验证；保留历史推荐与用户周期，手工立即检查按原逻辑更新下次运行时间。

## 2026-10-04 科研日报能源新闻来源

- Sol在backend cwd运行 `.venv/Scripts/python.exe -m pytest tests/test_research_news.py -q`：red 2 failed/4 passed；green 6 passed、0.32s、exit0，4条既有datetime.utcnow弃用提示。覆盖新增来源、域名/主题过滤、缓存、失败回退及去重。
- Sol在frontend cwd运行 `npm.cmd run test -- tests/research-daily-news.test.tsx`：red 1 failed、2.78s；green 1 passed、1.68s、exit0。覆盖能源在前、AI单列、真实来源数量、日期与链接。
- 一次frontend生产构建exit0（含类型检查），保留既有无关CSS警告。后端使用 `docs/handoff/2026-10-04-energy-news-refresh.Dockerfile` 复用现有镜像，仅COPY新闻服务，构建exit0；部署3001/8001成功且两容器Healthy。
- 初版实际RSS返回48条，发现CLEW全站feed混有webinar/grants/experts。Sol新增 `test_clean_energy_wire_accepts_news_articles_only`，仅该项red 1 failed、0.39s；green 1 passed、0.28s、exit0。修复后仅追加后端镜像构建和后端更新，两项exit0/Healthy，没有重复构建前端。
- 最终API实际41条：EIA10、MIT能源10、MIT AI10、CLEW1、ScienceDaily10，warnings=[]，CLEW均为/news/；[接口记录](docs/handoff/2026-10-04-energy-news-runtime.json)。浏览器3001实际能源31条/AI10条、5个来源、非新闻CLEW链接0、error logs=[]。
- 未全套、截图或移动端复测；无模型调用、数据写入或schema修改。外部RSS内容和可用性会随发布方变化。

## 2026-10-04 学习卡片分段与来源折叠

- Sol 在 frontend cwd 执行 `npm.cmd run test -- tests/learning.test.tsx -t "formats plain card sentences|keeps authored Markdown"`：red 2 failed /20 skipped，2.07s，exit1；green 2 passed /20 skipped，2.30s，exit0。覆盖纯数字编号、纯文本分段/加粗、原生来源默认闭合/展开/收起，以及已有 Markdown/列表/公式保留。
- 一次 `docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend` 成功exit0；仅frontend更新3001成功exit0，后端8001未动；保留无关既有Autoprefixer/缓存警告。
- 浏览器3001学习包1：第一张卡片编号“1”、正文5个p和1个strong、4条完整来源；默认来源 isVisible=false且无来源文本进入可见DOM snapshot，展开后isVisible=true并有E1，收起后false；浏览器error logs=[]。初始用getBoundingClientRect检测隐藏内容得到非零尺寸，改用原生details状态及Playwright可见性确认；未修改产品。
- 未调用模型或修改学习数据，未重跑20旧项、全套、截图矩阵或移动端复测。

## 2026-10-04 学习各项加载动画

- Sol 在 frontend cwd 执行 `npm.cmd run test -- tests/learning.test.tsx`：red 4 failed / 16 passed，34.26s，exit1（开始11:01:25）；实施后 green 20 passed，5.97s，exit0。新增用例覆盖生成等待/重复请求/失败重试、创建防重、复习读取与保存、版本读取与比较失败恢复；既有 jsdom canvas 提示保留。
- 主控执行一次 `docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend`，Next 生产编译、类型检查和镜像构建成功，exit0；其他页面原有 Autoprefixer/缓存警告保留。
- 设置 FRONTEND_HOST_PORT=3001 / BACKEND_HOST_PORT=8001 后，仅执行 `docker compose -f docker-compose.yml -f docker-compose.harness.yml up -d --no-deps frontend`，exit0。未重建/重启后端。
- Codex 浏览器实际3001：刷新学习包捕获“正在读取学习包…”及0.0s；复习列表、版本列表/原生导出链接、六栏目导航和自测生成入口正常，浏览器 error logs=[]。没有触发真实模型或保存学习数据。长请求/写入状态经受控 Promise 测试验证，未跑全套、截图矩阵、移动端复测。

## 2026-10-03 首页分类与轻粒子

- `npm.cmd --prefix frontend run test -- tests/homepage-photographic.test.tsx tests/dashboard-research.test.tsx`：旧实现2文件5项按预期失败，修改后同两文件8项通过，粒子GL在jsdom mock。
- 主项目前端生产构建及仅前端3001部署成功；初次脚本因PowerShell错误策略把Docker进度stderr当异常，恢复执行后缓存构建成功。实际深色Dock全局样式冲突修复后追加CSS生产构建/部署成功，无全量、哈希或重复测试。
- 1280×720：document client/scroll尺寸均1280×720，标语与卡片交叠0，粒子Canvas1、浏览器错误0；论文菜单含原五路由，菜单向上展开。390×844：页面无横纵溢出，六卡均在视口内，科研菜单范围x18.8–371.6、y435–679.2。
- 最终深色五分类按钮底色均rgba(0,0,0,0)，滚轮下滑两页后document/body scrollTop0。临时尺寸已恢复，最终浅色主题。实际截图与两份构建日志在docs/homepage-proposal/2026-10-03-categories/；后端/数据未动。


## 2026-10-03 储能编年史热储能三路线

- 实施前新文件3项真实red：exit1，18:38:01，1.75s，独立研究/统计隔离/论文阅读未实现。实施后 `npm.cmd --prefix frontend run test -- tests/chronicle-thermal.test.tsx --maxWorkers=1 --minWorkers=1`：7/8通过，18:59:11，2.00s；一项遇到重复h2/h3同名，修内容重复小标题后同文件加 `-t 'thermal papers open'`：1通过/7跳过，exit0，18:59:56，1.76s。8项最终全部已验证通过，没有把跳过算新执行，也未重跑旧套件。覆盖三路独立结构、热市场隔离、论文/年份阅读返回、MWh_th/e和MW_th/e、材料保留率/干材料分母/归一化功率、7档案及对应图源。
- 一次 `docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend` exit0，Next15.5.22编译、类型检查及静态生成成功，保留既有其他页面CSS Autoprefixer/cache警告；FRONTEND_HOST_PORT=3001/BACKEND_HOST_PORT=8001后 `up -d --no-deps --no-build --wait --wait-timeout 120 frontend` exit0，frontend healthy，仅前端部署。
- 一次现有Playwright+Edge真实3001验证exit0：HTTP200；三路工程照片naturalWidth1400/1783/1400，三机制概念图1916/1672/1916、政策原页1158，全部加载。首年详解返回保留；三路政策市场SVG均0；2026潜热96.85%保留率、MGA0.5MW_e/0.5MW_th、Tempo20MWh_th设计目标显示；共享浅深主题颜色不同、暂停article opacity1；390px scrollWidth390、pageerror0。未截图、主机build、全套或哈希。
- [运行证据](docs/handoff/2026-10-03-chronicle-thermal-runtime.json)、[交接](docs/handoff/2026-10-03-chronicle-thermal.md)。媒体输入JSON尾字面换行导致一次parse失败，无写入；Luna修正后合并成功。

## 2026-10-03 储能编年史机械六路线

- Red：实施前同新测试文件3项失败，exit1，17:37:42，1.66s，缺独立研究/统计/阅读行为。Green：`npm.cmd --prefix frontend run test -- tests/chronicle-mechanical.test.tsx --maxWorkers=1 --minWorkers=1`，9/9通过，exit0，18:16:05，2.14s。覆盖独立数据与六章、抽蓄统计隔离、论文阅读/返回、热容量/燃料/模型/设计边界、素材与15档案映射、真实年份阅读及返回。未重跑旧套件。
- `docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend`一次exit0，Next15.5.22编译、类型检查及27页静态生成成功；保留原有其他页面Autoprefixer/cache警告。设置FRONTEND_HOST_PORT=3001、BACKEND_HOST_PORT=8001后`up -d --no-deps --no-build --wait --wait-timeout 120 frontend` exit0，frontend健康，仅前端重建。
- 现有Playwright+Edge一次真实3001核对exit0：HTTP200；六路线图片naturalWidth分别3000/1536/1536/1024/940/741，进入详情再返回保留各自首个年份；抽蓄65.94GW显示且展厅SVG数量0；真实浅/深按钮切换html主题及对应文字/遮罩颜色；暂停时article opacity1；390px scrollWidth390；pageerror0。没有截图、主机重复build、全套测试或哈希。
- [交接与边界](docs/handoff/2026-10-03-chronicle-mechanical.md)。

## 2026-10-03 首页单屏铺满

- `npm.cmd --prefix frontend run test -- tests/homepage-photographic.test.tsx tests/dashboard-research.test.tsx`：2文件8项通过。
- Docker前端生产构建、仅前端3001部署成功；实际390px发现搜索框受共享header影响，修复后再构建部署一次，两次成功，未重复测试或运行全套。
- 1280×720页面/Hero/画框均填满视口，下半区节点0、页脚隐藏；滚轮下滑两页后scrollTop0。1920×960铺满且八入口在屏内。390×844无页面溢出，八入口与Dock在屏内，搜索框修复后横向18–372.4px、高42px。
- [交接](docs/handoff/2026-10-03-homepage-fullscreen.md)、[浅色实拍](docs/homepage-proposal/2026-10-03-fullscreen/live-light.jpg)、构建日志位于同目录；后端/数据库未修改。


## 2026-10-03 储能编年史：统一六栏与企业简介（已部署）

- 只运行相关文件。main首次`npm.cmd --prefix frontend run test -- tests/storage-chronicle.test.tsx tests/chronicle-revision.test.tsx --maxWorkers=1 --minWorkers=1`，16/18通过；新revision9/9通过，旧文件两处断言仍按三栏目结构（返回年份按钮和policy只有一个img）失败。修断言后旧9第一次8/9，素材循环尾部仍点击旧企业页签；改回政策市场后同旧文件9/9 exit0，总计2.95s。没有为通过断言更改实际组件行为，新9不重复。
- 主写入前候选revision9/9 exit0，15.02s，证明三路线六栏目ID映射；默认worker一次无进展终止，单worker通过。自动审批此前担心整组件替换与映射undefined，在有定向差异/检查证据后允许主路径写入，没有绕过拒绝。
- 本轮`docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend`一次exit0，含生产编译与类型检查，保留既有其他CSS Autoprefixer/cache警告；`up --no-deps --no-build --detach --wait --wait-timeout 120 frontend`仅替换前端，3001健康，8001后端未重启。未主机重复build、全量测试或哈希。
- 实际3001 HTTP200；六栏在展示/详解完全相同，材料/企业/返回选中保留；小字均至少14px、正文18px；QS/PowerCo企业背景与材料背景匹配，双主题fixed背景稳定，标题下导读和正文来源行不再显示，参考资料默认折叠且有原始链接，表格保留；BYD营收与2026-08-31市值快照显示；390px scrollWidth390，无pageerror。
- 一组真实1920×1080截图：[浅色详解](docs/screenshots/chronicle-revision/company-reading-light.png)、[深色详解](docs/screenshots/chronicle-revision/company-reading-dark.png)，[运行数据](docs/screenshots/chronicle-revision/runtime.json)。没有重复美容截图。

## 2026-10-03 首页静态最终版与交互框底色

- `npm.cmd --prefix frontend run test -- tests/homepage-photographic.test.tsx tests/dashboard-research.test.tsx`：2文件9 passed，静态单摄影图/双主题/业务统计/无场景层/单入口悬停与焦点/下半区通过。
- 静态撤销和用户随后追加的纯CSS修正各一次实际主目录Docker前端生产构建与仅前端部署成功；类型检查通过，3001/8001保持。纯CSS修正后不重复Vitest。
- 3001实际双主题原摄影图可见，Canvas及动效层/热点0，图片animation/transform均none。上传卡片hover与键盘焦点背景rgba(255,252,247,.8)，独立卡片激活；场景静止。深色Dock hover背景rgba(0,0,0,0)。真实33论文/2订阅/6未读正常，浅色已恢复。
- 未全量/哈希/新图像生成/用户模型API调用，窄屏未重复检查。[最终截图与记录](docs/handoff/2026-10-03-homepage-static-final.md)。


- **2026-10-03 城市模式按钮与页首**：两次Docker前端构建部署；初次实际检查仍被共享ID样式覆盖，最终模式按钮data-specular=off后确认三模式选中深蓝白字、未选中较浅，浅深主题均显示区别。指定页首说明句已不存在。未新增或运行测试。

## 2026-10-03 城市应用阅读与机制图解优化

- 定向 `npm.cmd --prefix frontend run test -- tests/storage-city-applications.test.tsx`：7 passed，覆盖场景差异、展开强调与机制图及原有交互。
- 仅主项目Docker前端两次生产构建和 `up -d --no-deps frontend` 部署成功，第二次为UPS小图标与文字间距修正；路由保持3001，后端未动。
- 实际3001检查：正文15px、图解标签14px、场景按钮16px；序号字体CityDigits/Times New Roman，箭头35px、光球9px、0.7s。展开内容分段加粗并显示机制配图；390窗口无横溢、图解标签仍14px、正文15px。保留暂停与场景切换。未全量测试或哈希检查；小图标位置修正未重跑测试。
- [实际页面](docs/handoff/storage-city-readable-3001.jpg)。

## 2026-10-03 储能编年史（正式3001，三条路线）

- 主项目定向：`npm.cmd --prefix frontend run test -- tests/storage-chronicle.test.tsx`，最终9/9通过（test 910ms /总计3.41s）。早期动态导入造成2个测试超时；改静态导入后本组通过。后续仅修改素材绑定和CSS，最终绑定/主题由正式浏览器覆盖。
- Docker：`docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend` 生产构建exit0，Next 15.5.22编译/类型检查通过；素材绑定修正后的增量为缓存命中。初次正式浏览器发现SpecularInteractions全局ID规则覆盖浅色按钮，随后局部修正CSS并增量构建、前端替换。构建保留已有StorageCityApplications Autoprefixer/cache警告，无相关源文件修改。没有主机重复build或全量测试。
- 部署使用FRONTEND_HOST_PORT=3001、BACKEND_HOST_PORT=8001和`up --no-deps --no-build --detach --wait --wait-timeout 120 frontend`；仅重建前端容器，健康，后端未重启。
- 实际HTTP200；共享主题根属性和localStorage一致、场景选中颜色有区别、暂停后CTA/正文可见，展厅宽度1656px（浅）、1656px（深），均超过主区域94%。固态Toyota、AI材料标签、2026税务截图、QS/BMW企业图正确；锂离子/钠离子独立年份、阅读返回保留年份；钠电2024为实际50MW/100MWh；工信部政策绑定正确。31可用图片均解码，390px无横向溢出，pageerror为0。
- 一组1920×1080真实视口截图：[浅色](docs/screenshots/chronicle-main/solid-light.png)、[深色](docs/screenshots/chronicle-main/solid-dark.png)、[材料](docs/screenshots/chronicle-main/material-dark.png)、[政策](docs/screenshots/chronicle-main/policy-dark.png)。[运行数据](docs/screenshots/chronicle-main/runtime.json)。只在实际失败后续跑检查，未哈希、全量测试或反复美容审查。

## 2026-10-03 首页2.5D摄影动效

- 首页两文件定向Vitest：10 passed，覆盖入口/统计/主题、物体与卡片悬停及焦点、视差限制/离开复位/reduced跳过动画帧、下半区。
- 实际主目录Docker前端新源码编译、类型检查、27页生成成功，随后仅重建frontend，保持3001/8001。首次构建调用命中旧目录缓存，确认目录后完成实际编译，未把缓存输出当作新源码证据。
- 3001浏览器：Canvas0，双主题摄影图加载，风机动画running且变换持续变化；纸张热点抬起，储能流光opacity .95/2.3s；问答键盘焦点触发orb/光环7s；视差出现且离开归零。390×844外部视口文档375px宽无横溢，八入口两列，视差none，最近论文/科研提醒仍在页面。视口及浅色已恢复。reduced停止动画CSS已检查，未做系统偏好浏览器演示。
- 未全量/哈希；未调用用户文本模型API，素材使用imagegen。[日志、截图与验证边界](docs/handoff/2026-10-03-homepage-2d-motion.md)。


## 2026-10-03 论文库元数据与缺失名词补齐

- Sol定向前端检查：chemical-title、library-paper-state、markdown-mermaid，共25 passed；涵盖Ni(OH)₂、CO₂、结构相普通数字及既有Mermaid显示。
- Sol定向后端与私有导入脚本检查：元数据、PDF出版信息及保存脚本，共40 passed；受控数据，无外部模型或真实网络调用。保存脚本帮助命令正常。
- 导入先预览后应用，一次事务更新33篇关键词和体裁、新增10份名词解释，失败0。数据库只读确认33篇各8关键词、33份清单均存在；本次10份各20项，23份旧清单保留。
- 后端复用原镜像依赖、刷新paper_metadata源码一次；前端生产构建一次成功，编译和类型检查通过。一次部署前后端，保留3001/8001。
- 实际3001论文库已加载20/33篇，Ni(OH)₂和CO₂正确显示；飞轮控制显示方法研究、虚拟电厂调度显示仿真研究，卡片均显示针对性关键词。GET /backend-api/api/v1/papers/24/glossary返回已保存20项、provider为codex；8001 /health返回status及database均ok。
- 未运行全套测试、哈希或重复构建；首页、三类报告、图表内容和数据库结构未改。本轮用户配置模型API调用0。[范围与交接](docs/handoff/2026-10-03-library-metadata.md)。

## 2026-10-03 储能城市应用（3001主项目）

- Sol：`npm.cmd --prefix frontend run test -- tests/storage-city-applications.test.tsx`，最终6 passed；覆盖场景切换、七条线路、暂停、应急局部备用路径、场景图解与展开说明。
- 主项目：`docker compose -p energy-research-copilot-deepseek-harness-2026-08-21 -f docker-compose.yml -f docker-compose.harness.yml build frontend` 成功，编译及类型检查通过并生成新路由。随后 `up -d --no-deps frontend` 成功，保持3001前端/8001后端，后端未重启。
- 实际3001浏览器：1920×1080下地图宽1157.5px，医院热点完整在图内；7条连接和7条动画存在。1024×768下页面无横向溢出且全部热点在图内。暂停时地图与右侧箭头动画均paused；应急模式城市流动路径0、局部备用路径1；原理展开内容可见。视口已恢复。
- [实际页面截图](docs/handoff/storage-city-live-3001.jpg)。未全量测试、哈希校验、重复构建或外部模型调用。

## 2026-10-03 全库图表详细版与格式

- 正式SQLite一次最终保存审计：33篇三类报告无缺失；523条图表记录全部非空，其中476条原图／表格／续表和47条正文引用指引，全部对应detailed-v2；历史快照208条均已整理。真实项五节、分点、加粗、无代码围栏的格式缺项0。审计及逐批保存记录在私有local_state/batch-paper-processing/2026-10-02，公共文档不收录论文内容。格式核对不替代科学内容的逐图阅读。
- 11篇缺失的33份报告直接由Codex生成并写入正式数据库；33篇报告字段均非空。实际后端及前端代理已读取代表性报告。原有22篇报告未覆盖。
- 页面实际检查：paper36图表正文18px／33.3px行高，五个小节、12项列表、10处加粗、代码块0。VisualPanel只包裹图表解读及裁切解读，reader-refinement.css仅作用于该局部；不改顶部冻结字号。前端此次Docker构建退出0但全部命中缓存，不据此宣称新编译；实际页面样式已生效，未重复截图。
- 后端仅一组定向pytest：test_api.py中visual_analysis_prompt_requires_reviewer_evidence_chain_and_professional_checks、decoupling_figure_one_prompt_and_mock_are_explicitly_subfigure_scoped，2 passed、43 deselected，受控Mock，无网络模型调用。
- 最终后端复用已有依赖，仅复制providers.py刷新源码镜像，构建退出0并仅重建backend，保留3001/8001与数据挂载。容器实际导入新提示词，五节／分点／Unicode要求断言通过；8001健康ok，3001代理读取paper20最终46条，空解读0，续表p72存在。未重启前端、未运行全套或首页哈希。本轮外部模型API调用0。

## 2026-10-03 真实3D与模型动效恢复

- `npm.cmd --prefix frontend run test -- tests/homepage-photographic.test.tsx tests/dashboard-research.test.tsx`：2文件9 passed；覆盖Scene接线、八入口/对应模型hover及focus、主题、真实统计与下半区。沿用测试文件名，内容已改为真实3D组件接线。
- 一次Docker前端生产构建退出0（含类型检查），仅frontend部署3001；[最终构建日志](docs/homepage-proposal/2026-10-03-live/frontend-build.log)。后端未修改或重启。
- 实际浏览器Canvas1、完整摄影场景图片0、data-ready=true。鼠标点击/移入地球、纸张、设备分别激活orb/paper/storage；纸张截图可见翻页；Tab聚焦论文库问答卡片联动orb。浅深主题均显示真实模型。390×844窄屏实际clientWidth=scrollWidth=375，Canvas与世界层均1155.55×650且在画框内居中裁切，8入口两列约164px，下半区最近5篇仍存在。
- [浅色](docs/homepage-proposal/2026-10-03-live/live-light.jpg)、[深色](docs/homepage-proposal/2026-10-03-live/live-dark.jpg)、[设备联动](docs/homepage-proposal/2026-10-03-live/live-dark-interaction.jpg)为自然视口实际截图，未拉伸或补边。未全套、哈希、重复构建或模型API调用；未新增任意拖转/自由相机。

## 2026-10-03 摄影场景首页（已部署）

- `npm.cmd --prefix frontend run test -- tests/homepage-photographic.test.tsx tests/dashboard-research.test.tsx`：2个文件、8 passed。初跑两条旧断言因重复的“论文库总数”标签失败，修改查询后通过；后续仅布局兼容导出、CSS及图标路径修正，未重复测试。
- Docker前端生产构建包含类型检查：4次尝试，旧AnchorMap类型不兼容失败、一次复制路径未带入修复导致同样失败，恢复兼容后成功，实际视觉修正后最终成功。最终日志见[frontend-build.log](docs/homepage-proposal/2026-10-02/frontend-build.log)。仅更新frontend至3001，backend未重启。
- 实际浏览器：浅深主题及刷新保持；八入口href正确，点击论文库进入/library，Ctrl+K进入/search；最近5篇与科研提醒仍可滚动查看。运行33篇、2订阅、6未读，无Canvas。390×844窄屏clientWidth与scrollWidth均375，8入口两列，标题15px。窄屏检查在最终顶部颜色/主题图标/文件夹修正前完成，未重复检查。
- [浅色截图](docs/homepage-proposal/2026-10-02/implemented-light.jpg)和[深色截图](docs/homepage-proposal/2026-10-02/implemented-dark.jpg)为约1265px自然视口的完整截图，未拉伸、补边或编辑。未跑全套、后端、哈希检查或业务模型调用；本轮不是全业务端到端验收。

## 2026-10-02 证据映射与科研表单（已部署）

- 后端 `tests/test_claim_evidence.py` 12 passed，覆盖新版报告提取、缺失/过期/不同模型索引只处理本篇、现有索引复用、空报告提示、索引成功后检索失败回滚保留旧映射/索引，以及active解析页码和docling坐标来源。前端 `tests/claims-panel.test.tsx` 1 passed，验证面板内进度、错误和成功重试反馈；均为受控模型/嵌入提供者。
- 科研表单 `tests/scientific-form.test.tsx` 24 passed，既有 `tests/phase6-document-intelligence-ui.test.ts` 7 passed，最终组合31项通过。覆盖15种实际算法数据形状、空值/单位/参数校验、倍率行号转换、建立→确认→运行、修改后禁算、连续小数输入、XRD/CV可选参数、光谱区间及组间不等长数据。中间帮助旧静态校准文案断言失败，改为准确说明仅曲线校验所需条件后通过。最终帮助只将JSON编辑改为只读查看文案，未再次运行这组检查。
- [后端构建](docs/handoff/2026-10-02-paper-tools-backend-build.log)与[前端构建](docs/handoff/2026-10-02-paper-tools-frontend-build.log)各一次退出0，前端含类型检查；部署保持3001/8001，代理健康ok。无API或数据库schema变化，无全量测试或首页哈希。
- 实际浏览器paper16点击建立映射，自动准备本篇索引后显示8条结论与全文证据，点击“查看第4页证据”后PDF iframe为`#page=4`；读取页码控件时定位器role误选超时，改用实际iframe状态确认，不重复生成。前端更新后刷新仍有8条。科研页显示中文容量保持率、空的两行容量输入、单位、无需额外参数、保存/核对/确认/运行；没有向用户论文保存演示数值，计算80%流程由受控交互测试验证。实际仅本地Ollama调用，无付费文本模型、无报告重生成。帮助与README已同步，未截图复验。

## 2026-10-02 PDF标题与期刊识别（已部署）

- Python3.12定向组：`tests/test_pdf_bibliography.py`、`tests/test_paper_metadata.py`、`tests/test_paper_metadata_backfill.py`与既有API上传/重复/无效三个检查，38 passed。覆盖完整属性标题、多行排版、刊头/默认属性排除、期刊格式、精确DOI及来源失败、上传后跨请求读取、预览不写入及自定义标题保留。后续中文短标题/Nature前缀校正单项1 passed。最终将重复文件早检恢复到PDF读取/联网前，同时保留锁内并发检查，此小调整后未重复运行测试。未跑全量测试。
- 正式33篇先用只读SQLite和本地PDF形成[预览](docs/handoff/2026-10-02-pdf-bibliography-local-preview.json)，20标题、9期刊候选正确。复用依赖单次[后端构建](docs/handoff/2026-10-02-pdf-bibliography-backend-build.log)退出0，仅部署backend至8001；无需API类型或数据库结构变更、前端未重建。
- 部署后运行 `python -m app.backfill_paper_metadata --bibliography-only`，33篇扫描、26条更新、0失败，20标题与9期刊写回且标题索引同步；[实际应用记录](docs/handoff/2026-10-02-pdf-bibliography-applied.json)。运行接口确认#36完整标题、#18标题Redox flow batteries: a review与期刊J Appl Electrochem、总数仍33、缺失期刊只剩#3（无可识别期刊与DOI）；3001后端代理健康ok。没有真实公网查询、模型调用或测试数据写入用户论文库；README已同步。

## 2026-10-01 名词解释持久保存与缓存（已部署）

- 后端Python3.12 `.venv`运行 `pytest tests/test_paper_experience_api.py -k glossary -q`：3 passed、22 deselected。受控模型计数验证首次生成后GET一致、普通生成不再调用、显式重新生成调用、失败保留旧结果；旧清单恢复不创建provider、不覆盖已有保存结果。
- 前端 `vitest run tests/paper-experience.test.tsx tests/api-glossary.test.ts -t glossary`：5 passed、36 skipped。包含打开论文读取已有清单、不自动生成及显式重新生成；未执行全量测试。
- OpenAPI及前端生成类型已同步。前后端各一次Docker构建退出0，前端含类型检查；保持3001/8001部署。运行数据库 `alembic current` 为0029 head；代理健康ok，新GET `/papers/16/glossary` 返回200/null（该篇未有保存清单）。成功生成持久化由受控API测试验证，没有向用户论文写入测试数据，没有真实付费模型调用。
- 当前可访问页面没有残存术语清单，未恢复此前丢失输出。概念问答仍为页面会话，帮助与README区分两者。[前端构建](docs/handoff/2026-10-01-glossary-persistence-frontend-build.log)、[后端构建](docs/handoff/2026-10-01-glossary-persistence-backend-build.log)。

## 2026-09-30 名词解释15–20项专业短语与缩写（已部署）

- backend目录 `.\.venv\Scripts\python.exe -m pytest tests/test_paper_glossary.py tests/test_paper_experience_api.py -k glossary -q`：5 passed、22 deselected，覆盖普通词/括号译名过滤、专业短语与缩写同时保留、已知缩写补齐和Mock API新数量。首次从根目录执行导入失败，改为backend工作目录后通过。
- 发现过滤后数量可能不足15时补上最终数量检查，并仅再次运行 `tests/test_paper_glossary.py`：5 passed，含20项原始结果过滤后不足15的拒绝用例。最后将必选缩写上限恢复12，避免与至少8专业短语、总数最多20的提示矛盾；对应上限断言新增后未再运行pytest。无全量测试或真实模型调用。
- 前端单次Docker生产构建退出0（含类型检查），后端单次复用依赖源码刷新；统一部署保持3001/8001，代理健康ok。[前端构建](docs/handoff/2026-09-30-specialist-glossary-frontend-build.log)、[后端构建](docs/handoff/2026-09-30-specialist-glossary-backend-build.log)。部署模块受控Mock返回18项，其中12项专业短语；RESEARCH/STUDY/METHODS候选仅保留XRD。实际浏览器名词解释显示“点击生成15–20个专业术语，包含专业短语与缩写”，指定说明后缀不存在；未点击真实生成、未截图复验。帮助及README已同步，无数据库/API结构变化。

## 2026-09-30 流程图化学角标与名词缩写覆盖（已部署）

- 前端 `markdown-mermaid.test.tsx` 最终 12 项通过；新增明确化学式、Unicode 下标/离子电荷上标、显式分数与小数脚本，结构标签与节点 ID 保留。初次 11 项通过后发现显式分数脚本缺少斜线，小范围补齐并最终检查一次。
- 后端 `tests/test_paper_glossary.py` 3 项通过，覆盖报告及全文末端缩写入选、模型遗漏保底/别名去重/最多12项、结构相语境和元素/格式噪声过滤。仅受控结构化结果；没有真实模型请求。报告提示词规则已同步，但未重新生成真实论文报告。
- 前端单次 Docker 生产构建退出 0（含类型检查），后端单次复用依赖源码刷新；统一部署保持 3001/8001，代理健康 ok。[前端构建](docs/handoff/2026-09-30-chemical-glossary-frontend-build.log)、[后端构建](docs/handoff/2026-09-30-chemical-glossary-backend-build.log)。部署模块以公开示例文本得到 XRD、HAADF-STEM、mRIXS、P2、P3；浏览器已有 paper 16 的两图 ready，无新增生成。未全量测试、截图复验或更改 API/数据库结构。

## 2026-09-30 删除论文解析证据状态行（已部署）

仅删除 AnalysisTabs 与 VisualPanel 的证据状态展示块；论文组件目录搜索“证据状态：”无匹配。纯文案删除没有新增或运行测试。前端单次生产构建退出 0（含类型检查），仅部署 frontend 到原 3001；浏览器刷新 paper 16，报告正文存在且状态整行不存在。未重生成、调用模型或截图复验。[构建日志](docs/handoff/2026-09-30-paper-status-build.log)。

## 2026-09-30 论文正文内联标注隐藏（已部署）

在 frontend 目录执行 `npm.cmd exec -- vitest run tests/markdown-mermaid.test.tsx`，9/9 通过。新增覆盖明确类别、无页码标签、半全角方/圆括号与页码范围、`[Na+]`、`[1]`、普通链接及默认 Markdown 显示保留；既有 Mermaid 与普通代码块测试同文件通过。仅论文生成正文启用过滤，用户笔记与其他页面默认不启用。

前端单次 Docker 生产构建退出 0，包含类型检查，仅部署 frontend 保持 3001，backend 未重启。[构建日志](docs/handoff/2026-09-30-paper-labels-build.log)。实际浏览器打开已有 paper 16 报告，正文同类内联类别括号标注为 0；没有重生成或真实模型调用。未运行全量测试、哈希或截图复验。

## 2026-09-30 订阅详情排版、官方资讯与中文重点（已部署）

- 后端 `.venv/Scripts/python.exe -m pytest tests/test_research_reading.py -q`：4 项通过，覆盖五条批量、并发与跨实例缓存、来源变更、失败保缓存、缺摘要、接口限制及官方 URL 范围。受控模型，不访问真实模型。
- 前端 `subscription-detail-reading.test.tsx`：2 项通过，覆盖旧主题无新闻时独立展示官方快讯、最新五条中文标题/三重点、完整摘要与交互头卡、论文页签补齐整理及失败重试。最终仅调整资讯分区优先及日期排序，没有重复运行这组测试；最终生产构建与运行已检查。
- 前端单次 Docker 生产构建退出 0（含类型检查），后端单次复用依赖刷新源码镜像；部署保持 3001/8001，代理健康 `ok`。新增接口的 OpenAPI 与前端生成类型已同步，无数据库迁移。[前端构建](docs/handoff/2026-09-30-reading-frontend-build.log)、[后端构建](docs/handoff/2026-09-30-reading-backend-build.log)。
- 实际浏览器 `/subscriptions/2` 显示 50 条已加载论文、20 条 MIT News 官方能源/AI 快讯。已配置 `zhipu / glm-4.7` 完成一次五条批量中文整理，每条恰好三重点；原始标题摘要可展开，通用快讯单独标识。刷新后五条直接复用，持久缓存条数和时间戳未变，没有新增生成。1440px 视口正文 1110px 无横向溢出、主题头为 block 分层卡片，临时视口已恢复。[实际页面截图](docs/handoff/2026-09-30-subscription-reading.jpg)。未逐页/逐主题复验、未运行全量测试。

## 2026-09-30 订阅内容独立详情页（已部署）

`npm.cmd --prefix frontend run test -- tests/research-pages.test.tsx tests/research-results.test.tsx` 4 项通过，覆盖订阅/日报链接的主题与运行参数、立即检查只反馈、详情读取单条订阅与完整长标题摘要、原文/已读。没有重复运行全套或单独 TypeScript；单次 Docker 前端生产构建退出 0，包含编译及类型检查，部署保持 3001/8001，backend 未重启。[构建日志](docs/handoff/2026-09-30-subscription-detail-build.log)。

实际浏览器点击钠离子主题“查看订阅内容”跳转 `/subscriptions/2`，页面主题正确，完整摘要 1219 字符；摘要 computed `display:block`、`overflow:visible`，无截行。1440px 桌面视口正文与结果卡片均 1100px，无横向溢出；默认窄视口卡片 272px，也无横向溢出。点击“返回研究订阅”正常返回列表，临时视口已恢复；没有触发真实模型或手动检索，未截图逐页复验。

## 2026-09-30 界面精简、科研资讯与导航背景（已部署）

- Mermaid 单文件 8 项通过，含旧图去页码与正文引用保留。界面删文案/字号完成后 TypeScript 退出 0。
- 后端首次目标筛选 `tests/test_research_news.py tests/test_phase4_research.py -k "official_feed or daily_news or stores_new_recommendation or scheduler_start_runs_an_overdue or research_api_crud"` 5 项通过；`test_phase4_research.py -k news_failure_preserves` 1 项通过。运行发现 AI RSS 分类包含普通校园新闻后，最终 `test_research_news.py` 4 项通过，覆盖分类反例、主题锚点、缓存及来源失败反馈。使用受控 HTTP 响应，不调用付费模型。
- 前端 `research-results.test.tsx visual-data.test.tsx -t "opens notification|research run chart"` 7 项通过、2 跳过；`research-pages.test.tsx` 2 项通过，覆盖无需订阅的资讯、提醒展开原文和立即检查反馈。最终 TypeScript 退出 0。初次未筛选 `visual-data` 有既存 TopicArtwork 的旧 SVG 断言失败（当前实现为图片），没有修改无关断言，不宣称全文件或全套通过。
- 前端单次 Docker 生产构建退出 0；后端复用现有依赖增量构建，部署后保持前端 3001、后端 8001。首轮真实资讯读取发现分类过宽，修正后仅再次刷新 backend，未重建前端。[前端构建日志](docs/handoff/2026-09-30-ui-news-frontend-build.log)、[后端初次构建](docs/handoff/2026-09-30-ui-news-backend-build.log)、[主题过滤部署](docs/handoff/2026-09-30-news-topic-backend-build.log)。
- 实际前端代理健康 `ok`；最终 `/backend-api/api/v1/research/news` 返回 20 条、两个 MIT 官方来源、无警告，MIT Reads/Poitras 校园条目不再出现。浏览器确认已有订阅记录展开后含论文 DOI 原文链接、订阅主题内容可展开、问答正文 16px/辅助 15px、诊断正文 16px、日报与订阅辅助/图表 14px。paper 16 两图 ready、无渲染错误、无图内页码。导航壁纸实际资源与浅深左右切换已检查，恢复浅色；没有逐页截图复验或全量业务回归。
- 未改变用户订阅周期或触发真实模型调用；本轮没有手动执行用户主题的真实联网运行，订阅联网组合与失败保稿由目标测试覆盖，既存调度状态为 running。无数据库迁移，新增 API 的 OpenAPI 与前端生成类型已同步。

## 2026-09-30 GLM 裸 Mermaid 流程图修复（已部署）

针对 paper 16 实际返回的 `mermaid` 与 `flowchart TD` 分行格式补充回归样例：修复前未渲染，修复后 `npm.cmd --prefix frontend run test -- tests/markdown-mermaid.test.tsx` 的 7 项均通过。frontend 生产构建成功，部署到原 3001 端口后前端代理及数据库健康返回 `ok`。未调用模型；修复在展示层处理已有报告。

## 2026-09-29 名词解释加载动效（已部署）

`npm.cmd --prefix frontend run test -- tests/paper-experience.test.tsx -t "generates glossary terms only on click"`：1 项通过，其余 38 项跳过。前端生产构建退出 0，仅重部署 frontend；3001 前端代理健康检查及数据库健康返回 `ok`。

## 2026-09-29 智谱 GLM-4.7 结构化报告格式修复（已部署）

定向 provider 测试 `test_glm_47_disables_thinking_only_for_structured_requests` 通过（1 项）：确认仅 GLM-4.7 的 JSON 请求带 `thinking: {type: disabled}`，普通文本及其他智谱模型不带该参数。复用既有依赖镜像刷新 backend 并按 8001 重启；`/health` 与数据库返回 `ok`，运行设置确认 `zhipu / glm-4.7`。未发起真实付费模型调用，故尚未验证该模型对具体论文的生成结果。

## 2026-09-27 论文快速理解 Mermaid 图示（已部署）

首次按项目既有依赖镜像刷新 backend 源码镜像并构建 frontend 生产镜像，均退出 0；原 Harness Compose 使用 3001/8001 及既有论文数据/OCR 模型挂载部署，退出 0，backend/frontend healthy。`8001/health` 返回 `ok`，前端代理论文列表 HTTP 200、总数 10，收藏 0、已读 1、未读 9。根任务第 1 次真实快速理解生成成功并显示两张 Mermaid 图；页面无渲染错误，但图高分别为 1513/1603px，且模型输出缺图标题和多数箭头标签，未达视觉验收。前端随后调整图形宽度、间距和节点尺寸，后端加强图标题、箭头标签及 5–7 节点短文案；修正版前后端镜像第二次构建均退出 0，`up --no-build --detach --wait` 退出 0，两个服务再次 healthy。二次部署后健康检查与前端代理论文列表检查再次通过（HTTP 200，总数 10、已读 1、未读 9、收藏 0）。根任务第 2 次真实快速理解生成达到模型输出上限并失败，已有报告被保留；不得将其计为成功。后端随后仅将 quick 预算调为 16000 且超时下限为 180 秒，相关 provider 定向测试 1 项通过；只刷新 backend 源码镜像并用 `--no-deps --no-build` 重建部署 backend，命令退出 0、backend healthy，frontend 未重建/重启。部署后 `8001/health` 为 `ok`，前端代理论文列表仍 HTTP 200、总数 10、已读 1、未读 9、收藏 0。第 3 次对 paper 13 的快速理解生成成功，报告保存为 `quick-understanding-v6`；两张图均各有 7 个节点，所有连线均有标签（核心逻辑图 6 条、方法流程图 7 条）。浏览器 DOM 显示两图均 ready、无渲染错误；图尺寸为核心逻辑图 270×952px、方法流程图 503×809px，字体 16px。人工查看一次最终画面截图，未做第二组截图或其他浏览器截图回归。三次真实模型调用的证据分别保存在 `local_state/paper-diagram-2026-09-27/paper-13-analysis-final.json` 和 `before.json`；此前已有论文报告不会自动重生成，需用户手动重生成。两次前端构建均有既存 Autoprefixer `end` 值兼容性警告。详见[部署交接](docs/handoff/2026-09-27-mermaid-deployment.md)。

## 2026-09-27 论文库 500 恢复

前端论文库失败时，backend 容器已停止；Docker host 日志显示 2026-09-27 14:10:33 UTC 引擎停止、随后 Linux/WSL 引擎启动，backend 于 14:10:38 UTC 结束。未确定宿主机重启触发原因。为 Compose 两服务增加 `restart: unless-stopped`，`docker compose ... config --quiet` 退出 0；对当前两个容器执行 `docker update --restart unless-stopped` 后直接 `docker start` 原 backend 容器，未重建或重建容器。只读检查确认两个容器均为 `running unless-stopped`，后端 `http://127.0.0.1:8001/health` 为 HTTP 200，经前端代理的论文列表接口为 HTTP 200、返回 10 项。未运行全套测试、构建或模型调用。

## 2026-09-27 论文理解生成按钮等待动画（已部署）

`frontend/components/papers/AnalysisTabs.tsx` 的“重新生成中…”与空态“分析中…”按钮忙碌内容改为现有 LatticeLoader 动画和计时，覆盖快速理解、通俗理解、审稿人速解。使用 `FRONTEND_HOST_PORT=3001`、`BACKEND_HOST_PORT=8001` 的 Harness Compose 前端生产镜像构建退出 0，Next.js 编译、类型检查及静态页生成成功；随后仅 frontend 容器 Recreated/Started，部署命令退出 0。未运行额外测试、截图、浏览器复验或真实模型调用；后端未重建或重启。

## 2026-09-27 论文证据改进与名词解释（已部署）

实现者报告：后端相关定向检查最终 prompt-v5/兼容调整前 31 项通过，调整后最终 4 项通过；前端流程测试 2 项通过、TypeScript 检查通过；历史问答截断修正后，13 轮追问回归 1 项通过。后端复用现有依赖镜像构建退出 0；前端 Docker 构建两次均退出 0，第二次包含只发送最近 6 轮历史的修正。首次 Harness Compose 启动后后端 `/health` 返回 200；之后单独部署修正后的前端退出 0，服务显示 backend 8001、frontend 3001。[后端记录](docs/handoff/2026-09-27-paper-glossary-backend-deploy.log)、[前端构建与部署记录](docs/handoff/2026-09-27-paper-glossary-frontend-build.log)。

主任务通过真实 `/papers/13` 界面操作生成术语并提问一个无关通用概念；模型回答 107 个 Unicode 字符且标为通用知识，生成 12 个简释术语。共触发 2 次真实模型调用。前端修正后重新加载确认页签、输入框与生成按钮仍显示，刷新清除了本地会话；没有再调用模型。未重新生成长篇论文报告，未测试 OCR，也未做截图或全量测试。

## 2026-09-27 名词解释工具范围与帮助说明（已部署）

实现者报告定向测试 2/2 通过：`npm.cmd --prefix frontend run test -- tests/paper-experience.test.tsx tests/help.test.tsx -t 'hides research|groups all 40'`。随后补充帮助文案，明确三问挑战用于核对证据/边界/最小验证且不调用模型，外部比较会调用已配置文本模型；按要求未重跑测试。第三次前端 Docker 构建退出 0，Compose 仅重部署 frontend 退出 0，访问地址 `http://127.0.0.1:3001`；后端未构建或重启。[构建与部署记录](docs/handoff/2026-09-27-paper-glossary-frontend-build.log)。

主任务部署后对 `/papers/13` 作一次 DOM 检查：快速理解页签仍显示两块研究工具，点击名词解释后两块消失，术语面板与“基于本篇论文追问”仍显示。未调用模型或截图。

## 2026-09-27 论文解析与 AI 理解定向评价

对库中 #11（15 页）、#12（72 页）、#13（23 页）的原 PDF 做一次只读原生分页提取，与已存全文核对一致；统计独立分析上下文实际保留正文分别为 17,808/82,397（21.6%）、17,225/294,916（5.8%）、17,724/136,294（13.0%）。查看 #11 第 2 页、#12 第 40 页、#13 第 4/20 页原页，并对照 #13 已存快速/审稿报告的 8 个具体点。只读检查运行容器的解析、上下文裁切与失败持久化源码。唯一一次真实 DeepSeek 快速理解调用为 #11：HTTP 200 但返回 33 字失败占位、证据状态“尚不确定”；随后 GET 确认占位已持久化。按停止条件未调用 #12、未重试；未运行 OCR/视觉模型、测试套件或构建。具体证据与限制见[评价交接](docs/handoff/2026-09-27-paper-parsing-evaluation.md)。

## 2026-09-27 论文详情顶部字号（已部署）

本轮仅修改 `frontend/components/papers/reader-refinement.css` 和交接/冻结说明；未运行测试或浏览器截图。单次前端 Docker [构建](docs/handoff/2026-09-27-reader-font-freeze-build.log)与仅 frontend 部署退出 0，容器 Recreated/Started，正式 3001 已更新。最终 CSS 包含于成功构建，未做截图视觉复验。

## 2026-09-27 项目缓存清理（仅清理核验）

总控按[清理清单](docs/handoff/2026-09-27-cleanup-manifest.json)删除 18 个精确路径中的 1,198 个文件（1,375,831,701 B）。删除前核验目标的绝对路径、reparse point 与 Git 跟踪状态；删除后目标路径均不存在。生产前端 3001、后端 8001 持续运行；清后只读 GET `3001/help`、`8001/api/v1/settings` 均返回 200，未输出设置内容。Git 既有 245 条变更（含 102 条未跟踪）未重置。本项未运行构建、业务回归或全套测试；首次本地开发或构建将重建缓存。

## 2026-09-27 使用模式说明修正（已部署）

`npm.cmd --prefix frontend run test -- --run tests/help.test.tsx` 退出 0，1/1：37 条主题在分组中显示，搜索“三种模式区别”命中新说明；原 OCR、校园预算及重复配置搜索仍通过。单次前端 Docker [构建](docs/handoff/2026-09-27-help-study-modes-build.log)与仅 frontend 部署退出 0，容器 Recreated/Started，正式 3001 已更新。本轮未运行独立类型检查、全套或浏览器检查；未改任何模式业务行为。[交接](docs/handoff/2026-09-27-onboarding-repeat-help.md)。

## 2026-09-27 配置引导重复使用说明（已部署）

`npm.cmd --prefix frontend run test -- --run tests/help.test.tsx` 退出 0，1/1：36 条主题分组可见，“重复配置”搜索命中新说明且自动展开；原 OCR 与校园预算搜索继续通过。之后仅收窄“使用偏好”作用范围的文字，未重跑；最终文字包含于成功的单次前端 Docker [构建](docs/handoff/2026-09-27-help-onboarding-build.log)。仅 frontend 部署退出 0、容器 Recreated/Started，正式 3001 已更新。本轮未运行独立 TypeScript、全套或浏览器检查，也未更改或保存用户设置。[交接](docs/handoff/2026-09-27-onboarding-repeat-help.md)。

## 2026-09-27 帮助中心内容核对更新（已部署）

`npm.cmd --prefix frontend run test -- --run tests/help.test.tsx` 退出 0，1/1：35 条主题全部显示于五个稳定分组，新“校园资讯 AI 预算”可搜索并展开，原 OCR 搜索仍有效。`npx.cmd --prefix frontend tsc --noEmit --project frontend/tsconfig.json` 退出 0。随后仅修正 OCR、科研想法、学习包、金额预算与日期说明文字及相应旧断言，未重跑测试/类型检查；最终文字包含于成功的单次前端 Docker [构建](docs/handoff/2026-09-27-help-content-sync-build.log)。仅 frontend `up` 退出 0、容器 Recreated/Started，正式 3001 已部署。未运行全套或浏览器检查，没有调用真实业务接口。[交接](docs/handoff/2026-09-27-help-content-refresh.md)。

## 2026-09-27 首次设置向导模型目录同步（已部署）

`tests/onboarding-model-catalog.test.tsx` 定向 2/2 通过，覆盖与设置页同源的 18 供应商网格、Mock 默认模型、Anthropic 当前预设及自定义模型保存 payload。初次运行仅因测试把已选项的视觉勾号计入名称而有 1 项断言失败，调整断言读取名称元素后单文件复跑通过。`npx.cmd --prefix frontend tsc --noEmit --project frontend/tsconfig.json` 退出 0。唯一前端 Docker [构建](docs/handoff/2026-09-27-onboarding-model-catalog-build.log)与仅 frontend `up` 退出 0，容器 Recreated/Started，正式 3001 已部署；后端未动。未做浏览器检查或真实模型调用。

## 2026-09-27 校园资讯 AI 预算设置（已部署）

`tests/settings-campus-budget.test.tsx` 页面交互 2/2 通过：默认 20/2400 回显、档位与自定义切换、空/小数/负数阻止保存、0 不限及已存 100/4096 回显。最初测试因 Vitest 不解析页内 `@/` 别名及经典 JSX 缺 React 导入失败，修复测试入口后单文件通过；JSDOM 对既有 WarpText 的 WebGL 初始化发出非阻断警告。后端生成设置类型就位后，`npx.cmd --prefix frontend tsc --noEmit --project frontend/tsconfig.json` 退出 0。前后端各一次 Docker 构建退出 0（[后端日志](docs/handoff/2026-09-27-campus-budget-backend-build.log)、[前端日志](docs/handoff/2026-09-27-campus-budget-frontend-build.log)）；Compose 两容器 Started、backend Healthy，3001/8001 已部署。一次正式只读接口确认迁移 0028、当前 daily 20 / tokens 2400；未运行浏览器检查或真实付费批量请求。

后端定向验证：`backend/tests/test_campus_analysis.py` 7/7，`backend/tests/test_api.py -k campus_ai_budget_settings_keep_values_when_older_client_omits_them` 1/1（另 44 未选），`backend/tests/test_provider_expansion.py` 四项输出上限相关测试 4/4（另 18 未选）。涵盖持久设置省略不重置、0 不限、失败计数、优先排序、假 provider 参数与 Anthropic 明确上限冲突。之后将类内排序明确为创建时间加 ID，相关用例单独复跑 1/1。`backend/openapi.json` 与 `frontend/lib/api.generated.d.ts` 已再生；未运行后端全套或真实付费调用。本次后端镜像包含上一轮已完成 64 项定向验证的 providers 视觉共享改动。

## 2026-09-27 校园资讯卡片精简（已部署）

`npm.cmd --prefix frontend run test -- --run tests/campus.test.tsx` 退出 0，6/6 通过；包含 Mock 标识、重要未确认项与空日期兜底隐藏的用例。后端校园定向 7/7 通过。前后端各单次 Docker 构建退出 0（[前端日志](docs/handoff/2026-09-27-campus-card-cleanup-frontend-build.log)、[后端日志](docs/handoff/2026-09-27-campus-card-cleanup-backend-build.log)）；两容器 Recreated/Started，backend Healthy，3001/8001 已部署。后端三文件薄层复制未包含 providers 晚到改动。未运行本轮独立类型检查或正式浏览器检查；未执行付费批量分析。[交接](docs/handoff/2026-09-27-campus-card-cleanup.md)。

## 2026-09-27 设置页状态灯与供应商网格（已部署）

`npm.cmd --prefix frontend run test -- --run tests/glide-select.test.tsx tests/settings.test.ts tests/settings-model-picker.test.tsx`：设置 23/23、模型选择器 2/2 通过；GlideSelect 新网格键盘用例首次因测试环境未返回实际 CSS 列宽而失败，修正列数回退后仅重跑 `tests/glide-select.test.tsx`，3/3 通过。`npx.cmd --prefix frontend tsc --noEmit --project frontend/tsconfig.json` 退出 0（列数回退改动前执行，改动仅涉及局部 JS 表达式）。单次前端 Docker [构建](docs/handoff/2026-09-27-settings-provider-grid-build.log)与仅 frontend `up` 退出 0，容器 Recreated/Started，正式 3001 已更新。未做正式浏览器检查。[交接](docs/handoff/2026-09-27-settings-provider-grid.md)。

## 2026-09-27 校园资讯全景头图（已部署）

昼夜两张内置 imagegen 全景 PNG 已复制到校园头图资源目录；仅校园 hero 的 CSS/说明文字已改。单次 Docker 前端构建与仅 frontend `up` 均退出 0，容器 Recreated/Started，正式 3001 已更新（[日志](docs/handoff/2026-09-27-campus-panorama-header-build.log)）。本轮未运行单测或浏览器截图，尚无正式视觉验收。[交接](docs/handoff/2026-09-27-campus-panorama-header.md)。

## 2026-09-27 配置引导校门透明裁片（已部署）

两张内置 imagegen 透明 PNG 已复制到配置引导资源目录，局部 CSS 已换图并取消旧遮罩。单次 Docker 前端构建及仅 frontend `up` 均退出 0，容器 Recreated/Started，正式 3001 已更新（[日志](docs/handoff/2026-09-27-onboarding-gate-cutout-build.log)）。本轮未运行单测或浏览器截图；构建结果不作为视觉验收。[交接](docs/handoff/2026-09-27-onboarding-gate-cutout.md)。

## 2026-09-27 模型供应商目录与校园 AI 整理（正式代表项已验）

已实际完成：前端设置/模型选择器定向 23/23 与 TypeScript 检查通过；校园前端 5/5、后端 2/2；后端供应商相关 73/73；Claude token floor 补修 18 项定向通过。后端首轮复用依赖[构建](docs/handoff/2026-09-27-model-catalog-backend-build.log)及前端单次[构建](docs/handoff/2026-09-27-model-catalog-frontend-build.log)成功，3001/8001 Compose 部署成功。正式浏览器看到设置页 18 个供应商选项、已保存 DeepSeek Pro 未变；校园电赛卡片“竞赛创新 / 工程设计”和加大关注按钮（[截图](docs/handoff/2026-09-27-campus-classification-production.png)）。Claude token floor 的第二次快速后端构建与容器 recreate/start 均退出 0；补修后未另做正式运行检查。未验证真实厂商付费调用，也未提高 AI 日报当日 20 次额度。

## 2026-09-27 深色材质灯光（已部署）

三份定向测试文件合计 9/9，前端 TypeScript 检查通过。单次 Docker 前端[构建](docs/handoff/2026-09-27-night-material-build.log)成功，`up -d --no-deps frontend` 成功，正式 `localhost:3001` 更新，后端 `8001` 未动。正式浏览器检查学习页和论文库深色、深浅切换后恢复浅色：[学习截图](docs/handoff/2026-09-27-night-learning-production.png)可见膜层反光，[论文库截图](docs/handoff/2026-09-27-night-library-production.png)可见头图冷暖光，两页正文可读。八个目标页面未逐页截图，未检查手机；上传、帮助、科研想法只审查既有深色素材，科研数据、配置引导及首页未改。[交接](docs/handoff/2026-09-27-night-materials.md)。

## 2026-09-27 配置引导校园照片（已部署）

`energy-header-routes.test.tsx` 定向 5/5。两次实际 Docker 前端构建及两次 `up -d --no-deps frontend` 均退出 0（[首轮日志](docs/handoff/2026-09-27-onboarding-campus-build.log)、[最终日志](docs/handoff/2026-09-27-onboarding-campus-final-build.log)）；首轮正式检查发现深色背景简写重置尺寸、塔楼裁切和校门硬边，修正后第二次部署到正式 3001。最终[浅色](docs/handoff/2026-09-27-onboarding-campus-light-final.png)/[深色](docs/handoff/2026-09-27-onboarding-campus-dark-final.png)截图确认塔楼位置相同、校名完整、边缘渐变，检查后恢复浅色；初版截图不作最终证据。未独立运行 TypeScript 或全套测试，未查手机、未提交向导业务；后端和首页未改。[交接](docs/handoff/2026-09-27-onboarding-campus.md)。

## 2026-09-27 科研空态展示字（已部署）

前端 `tsc --noEmit` 退出 0。首次 Docker 调用因沙箱无法访问 `.docker/buildx`，未进入构建；权限放行后唯一实际前端[构建](docs/handoff/2026-09-27-research-display-build.log)退出 0，`up -d --no-deps frontend` 退出 0，正式 3001 已更新，后端未改。正式浅色[科研数据截图](docs/handoff/2026-09-27-research-display-production.png)显示站酷小薇蓝灰/铜金字形，[科研想法截图](docs/handoff/2026-09-27-ideas-empty-production.png)显示装饰字消失且原说明保留，各截一次。未运行单测/全套，未检查深色/手机，未作业务写入。附加 DOM 字体检查因 browser binding 未定义未执行，未声称 `document.fonts` 验证成功。[交接](docs/handoff/2026-09-27-research-display.md)。

## 2026-09-27 上传页去白框（字体待素材）

仅上传页说明白框与底部白色横条的 CSS 调整：前端单次构建退出 0，[日志](docs/handoff/2026-09-27-upload-note-clear-build.log)；`docker compose up -d --no-deps frontend` 退出 0，正式 `localhost:3001/upload` 单次[截图](docs/handoff/2026-09-27-upload-note-clear-production.png)确认两处白底消失。纯 CSS 更改未运行测试套件；可画榜书字体未替换，等待用户提供可用文件或路径。[交接](docs/handoff/2026-09-27-upload-note-font.md)。

## 2026-09-27 TechText 附件参考修正（已部署）

TechText 与 TitleMotion 定向测试 6/6、TypeScript 检查退出 0。开发 3002 `/library` 浅深主题观察静态、键盘与拖拽，错误日志为空。GPU 检查发现整盒焦点框遮字后设 `outline:none`；42px 标题中原 150px 粒子遮邻字后按 `size/150` 且最小 `.35` 缩放，保留 15 颗和原算法；该修正后 TypeScript 再次退出 0。前两次 Docker 构建各退出 0，但均未部署（[首次日志](docs/handoff/2026-09-27-techtext-reference-build.log)、[第二次日志](docs/handoff/2026-09-27-techtext-final-build.log)）。第三次缩放版[构建](docs/handoff/2026-09-27-techtext-scaled-build.log)与部署退出 0，正式浅色交互发现 `TitleMotion` 标签碰撞；负 margin 收窄后第四次[构建](docs/handoff/2026-09-27-techtext-spacing-build.log)及 `up --no-deps frontend` 退出 0，3001 已更新，后端未动。

正式 `/library` 刷新后 ArrowRight 可选字；[原始截图](docs/handoff/2026-09-27-techtext-production.png)确认所选字虚线轮廓、滑框四角、尺寸标签与微粒清楚，实心邻字和标题下方说明未被整盒框覆盖，标签与英文眉题有间隔。浏览器错误日志为空。正式页面只验浅色代表页，深色和拖拽是开发环境检查，未逐页或手机验收；最后两次纯 CSS 修正没有重跑定向测试，最终构建包含全部改动并通过类型检查。[交接](docs/handoff/2026-09-27-techtext-reference.md)。

## 2026-09-27 单篇论文追问输入动效（已部署）

初始两项定向测试先红，实施后追问 2/2；最终局部计时修复后追问计时/两种问答状态 3/3，相关问答/证据 4/4，Specular 3/3，TypeScript 检查退出 0。一次 Docker 前端构建退出 0（保留既有 Autoprefixer 告警），[日志](docs/handoff/2026-09-27-paper-prompt-build.log)；`up -d --no-deps frontend` 退出 0，仅替换 3001 前端，后端未动。

正式 `/papers/13` 刷新后显示新圆角 PromptBar，空草稿发送禁用；输入 15 字后计数 15/500、发送箭头可用，聚焦蓝色柔光清楚，浏览器错误日志为空。[原始区域截图](docs/handoff/2026-09-27-paper-prompt-production.png)。locator/evaluate 偶有 CDP 3 秒超时，截图证实输入成功；未确认精确 computed 尺寸、深色或手机运行表现。未发送真实 AI 问题、未调用付费模型或写入业务数据；忙碌/成功/失败和草稿保留由受控定向测试验证。[交接](docs/handoff/2026-09-27-paper-prompt-motion.md)。

## 2026-09-27 玻璃图标分栏（已部署）

前端论文库/GlassIcons 定向测试 12/12、科研数据 3/3；后端 `test_collection_state` 3/3（含迁移旧行默认状态），TypeScript 检查退出 0。`sqlite3.Connection.backup` 一致性备份保存至 `local_state/upgrade-snapshots/20260927-glass-collections/energy_copilot-before-0027.db`，文件 28,254,208 字节；未做恢复演练。后端仅七个生产文件的增量镜像构建退出 0。首轮前端构建退出 0、backend/frontend `up` 退出 0 且 healthy；正式库只读确认 Alembic `0027` 与两列。[首轮日志](docs/handoff/2026-09-27-glass-collections-frontend-build.log)。

正式论文库四分栏计数 10/0/0/10，收藏空态及未读 10 篇正确；深色字色与玻璃面 `rgba(24,58,79,.35)` 可读，390px 视口两列各约 163.6px、文档宽 375px 无溢出，错误日志为空；[原始截图](docs/handoff/2026-09-27-glass-library-production.png)。正式科研数据零条首查 tab 隐藏，已补修为四个零计数 tab 并重跑目标测试 3/3。最终前端二次构建与 `up` 退出 0，[日志](docs/handoff/2026-09-27-glass-collections-final-build.log)。正式 `/research-data` 四 tab 计数均为 0，点击收藏后选中态为 true，原空库说明保留，错误日志为空；[原始截图](docs/handoff/2026-09-27-glass-datasets-production.png)。最终补修仅改变数据集空库条件，未重跑此前正式论文库检查。未进行真实论文或数据集状态修改。[交接](docs/handoff/2026-09-27-glass-collections.md)。

## 2026-09-27 非首页可读性与能源视觉（已部署）

定向检查已执行：校园/学习统计 8/8、上传标题 2/2、论文库后端缩略图 helper 2 项与 API 1 项、前端 8/8、header 初次 11/11（含生命周期）及路由扩展 9/9；此前 TypeScript 检查退出 0。首轮 Docker 前端构建与 `up` 退出 0；基于旧镜像 tag 的缩略图后端增量构建、backend/frontend `up` 退出 0，服务 healthy。最终前端二次 Docker 构建与 `up` 整体退出 0，[构建日志](docs/handoff/2026-09-27-readability-final-build.log)。

浏览器只读检查覆盖论文库 PDF 嵌入图裁片 7 张/回退 2 张、学习浅深和 390px 无溢出、配置引导火箭移除、竞赛深色满幅、校园操作行与 14px 小字、帮助页宽度及科研数据书法字。论文库裁片从前 8 页最多 40 个嵌入图中筛选并按位置裁切，不截整页；`auto-fit` 最小 520px 与图片取消定高也属于论文库。学习 header 只用 PixelSnow 与全页 L1 背景。最终正式 `/learning` 新标签 PixelSnow GPU 检查无大圆斑，`scene=learning` 与雪粒 Canvas 在位，错误日志为空；[原始截图](docs/handoff/2026-09-27-learning-energy-production.png)已保存。正式 `/library` 卡片高 305.9px，visual/图片各 304.3px，底部无空白，7 张 PDF 插图裁片加载，错误日志为空。开发 3002 已停止。竞赛页终版视觉未另做正式复查；未做全页面截图或全部业务端到端验收，未执行真实上传、删除、模型调用。详情见[本轮交接](docs/handoff/2026-09-27-readability-energy.md)。

## 满幅科研材质背景（三页，已部署）

- 本轮执行 `npm.cmd --prefix frontend run test -- full-material-backdrop-routes.test.tsx full-material-backdrop-lifecycle.test.tsx` 一次：2 文件、3 测试通过，退出 0；覆盖三条路由映射、减少动态效果静态回退，以及图片加载期间切换减少动态效果时不创建 Canvas。
- 开发浏览器已检查 `/search` 浅/深背景覆盖；`/compare` 深色在滚动 y=658.4 时背景仍贴合视口（rect top=0、bottom=720、left=224、right=1264.8），未盖侧栏。`/knowledge` 深色两张卡片的 computed background 均为 `rgba(15, 30, 40, 0.77)`；390px 手机浅色视口中 document scrollWidth=375、无横向溢出，文字可读且晶格背景铺满。知识页 textarea 聚焦后 `data-active` 从 true 变 false；控制台 errors 为空。
- CSS 玻璃卡片优先级修正后未重复运行组件测试。Docker 前端构建退出 0（[日志](docs/handoff/2026-09-27-full-material-build.log)）；`up -d --no-deps frontend` 退出 0，只更新正式 3001 前端，后端未动。正式 `/compare` DOM 为 `data-kind=electrode`、1 个 Canvas，暗色卡片 computed background 为 `rgba(15, 30, 40, 0.77)`；[正式原始截图](docs/handoff/2026-09-27-full-material-compare.png)已保存并查看。开发服务已停止。本轮未提交业务写入；三张素材只作艺术材料示意，不代表实验结构模拟。

## 搜索多孔碳拆解构图纠偏（已部署）

- 仅修改 `/search` 的 carbon atlas CSS 构图，将半壳、层芯与离子链分开；限制各层滚动和指针位移。3002 桌面 1280px 与手机 390px 截图确认三物体分离、无叠压；滚动进度 1 时半壳左缘 935.7px、层芯右缘 863.3px，间隔约 72px。
- Docker 前端构建退出 0（[日志](docs/handoff/2026-09-26-carbon-separation-build.log)）；`up --no-deps frontend` 退出 0，正式 3001 已更新。本次纯 CSS 修正未新增单元测试；下方测试结果属于此前版本。

## 材质场景、标题与玻璃控件（本轮已部署）

- 本轮定向结果由各实施代理报告：新材质场景 3/3、标题语义与路由分配 2/2、Specular 与 WorkspaceShell 后续单独复跑 10/10。首次组合执行中，`tests/theme-pill-switch.test.tsx` 1 项与 `tests/dashboard-research.test.tsx` 6 项通过；同轮 Specular 测试夹具因缺少 `main.app-main` 失败，已修复，未为这两个通过的文件重复执行。`frontend/node_modules/.bin/tsc.cmd -p frontend/tsconfig.json --noEmit` 在 WarpText 恢复正常类型检查、TrueFocus 中文词组分段后退出 0。
- 三套透明 atlas 对应搜索石墨、问答电极层片、学习铜箔/隔膜卷绕；标题路由固定分配 Warp/Tech/Focus。以上为源码与定向检查，不是最终 GPU/全路由视觉验收。
- 最终 Docker 前端构建退出 0，[构建日志](docs/handoff/2026-09-26-material-title-glass-build.log)；`docker compose up -d --no-deps frontend` 退出 0，正式 3001 前端更新，后端未动。
- 正式浏览器检查搜索浅色、问答浅色、学习深色三种场景层次；搜索滚动 y=244.8 时 `data-progress` 由 0 到 1。390px 手机问答页初查文字遮挡，最后局部 CSS 修正后在正式 3001 复查，材料低于说明文字、三层可辨、无横向溢出。
- 搜索、保存科研想法、保存设置按钮的 computed style 为玻璃渐变；首页浅色胶囊点击后 html 主题 dark→light。正式问答页控制台 errors 为空。浏览器检查限上述代表入口，未声称所有页面全量截图通过。下方各节为此前版本的独立验证记录。

## Specular 镜面按钮（最新部署版）

- `tests/specular-interactions.test.tsx` 与 `tests/workspace-shell.test.tsx` 共 10/10 通过；TypeScript 检查通过。验证覆盖目标范围、原生点击与清理，不代表全路由视觉验收。
- 开发浏览器已确认上传页浅/深 GPU 镜面边缘；文件标签 overlay 精确包围目标并外扩 20px、`pointer-events: none`，禁用的上传提交按钮无高光，OGL error 为空。科研数据“展开材料”按钮经键盘 Shift 聚焦后 overlay 指向该按钮，点击后变“收拢材料”，原回调正常。
- 最后 anchor 后移、主题重绘和 removed 清理三项修正未重跑定向测试。唯一 Docker 前端构建退出 0，包含类型检查及 25 静态页，保留既有 Autoprefixer 警告；[构建日志](docs/handoff/2026-09-26-specular-build.log)。`up --no-deps frontend` 退出 0，仅更新 3001。正式上传页 anchor 存在，鼠标移近文件标签后一个 Canvas、target“选择 PDF ↗”、display block，浏览器 error logs 为空；[正式局部原始截图](design/non-home/specular-upload-production.png)。开发服务已 Ctrl+C 停止。正式检查只覆盖这一代表入口，未跑额外测试或业务写入。首页、导航、顶栏、GlideSelect、禁用控件、正文链接和输入框均在效果范围外。

## 校园页宽度修正（最新部署版）

- 旧版正式页 2560px 视口的只读 DOM：校园页面宽 1440px，右边界 x=1712；来源栏约 427.19px，资讯栏约 996.80px，证实共享宽度上限造成右侧空白。
- 本轮仅改 `campus.css`：校园页取消 1440px 上限，概览左栏保持最多约 428px，新增宽度留给右栏；950px 以下单列规则未变。最终前端构建和仅替换 3001 前端均退出 0，[日志](docs/handoff/2026-09-26-campus-width-build.log)。
- 正式 2560px 视口只做一次 DOM 检查：页面宽 2240px、left 272/right 2512，来源栏 428px、资讯栏 1796px；相对旧版右边界向右扩 800px，资讯栏由 996.80px 增至 1796px。文档宽 2560px，无横向溢出。未跑业务测试或截图；检查后视口已重置。

## 能源场景与局部控件（最新部署版）

- 已运行 `tests/branched-nav.test.tsx` 3/3、GlideSelect 相关 6 文件共 46 项、能源场景定向 5 项和修订定向 2 项；TypeScript 检查曾通过。以上为定向检查，不代表完整业务回归。
- 开发 GPU 检查看到搜索 A 浅/深、学习 B 深色及 390px 手机、问答 C 浅色；A 两帧角度变化，学习标题 TechText 动画字可见。深色 GlideSelect portal 高亮与 ArrowDown/Escape 正常；390px 下拉边界 left 42.8/right 332.4/bottom 573（高 844），文档宽 375，无横向溢出。早期截图出现的加载延迟不构成控件故障。
- 科研想法 h1 实际字重 600，指针位置探照遮罩 opacity 1，输入焦点后 0；空态两行书法 Canvas 可见。搜索场景 `data-active` 在搜索词输入前 true、点击后 false。科研数据底景的既有入场动画 `both` 覆盖问题已局部修正；浏览器 computed opacity .15、animation none。本轮浏览器检查未写入业务数据。
- 唯一一次最终 Docker 前端构建退出 0，包含类型检查，保留既有 Autoprefixer `end`/`flex-end` 警告；[构建日志](docs/handoff/2026-09-26-energy-scenes-build.log)。`up -d --no-deps frontend` 退出 0，只替换 3001 前端。正式 `/learning` DOM 为 roll 场景、Canvas 2、combobox 1，error logs 为空；[正式浅色 GPU 原始截图](design/non-home/2026-09-26-energy-motion-review/learning-production.png)。三张生成素材与 Ma Shan Zheng 字体 HEAD 200，临时 3002 已停止且无监听。科研数据局部底景 CSS 修正已通过 DOM，进入最终构建；其后无业务源码改动。正式检查未逐页截图、未触发真实业务写入或模型请求。[交接记录](docs/handoff/2026-09-26-energy-scenes-controls.md)。

## 校园来源目录分类（最新部署版）

- 校园页定向4/4通过，覆盖原API操作、渠道文案、刷新保留展开状态等。
- 开发浏览器检查真实机械工程学院3栏目展开，官网标签与按钮nowrap；暗色无横向溢出。最后官网短名、单列操作及浅绿状态字未重复截图/测试。
- 最终Docker前端构建退出0，包含类型检查，既有Autoprefixer警告保留；仅替换3001前端。正式DOM确认67官网栏目、46机构组及四类渠道说明。3002停止，未改真实来源启停状态。[完整记录](docs/handoff/2026-09-26-campus-source-directory.md)。

## React Bits 分类导航与局部动效（最新部署版）

- `tests/branched-nav.test.tsx` 3/3；既有 `tests/paper-experience.test.tsx -t Nav` 2/2（31跳过）；`tests/react-bits-page-decor.test.tsx` 2/2。场景测试覆盖路由范围及暂停信号传递，并非GPU像素测试。
- 实际浏览器确认分类折叠/Tab跳过隐藏链接、二级导航、手机打开聚焦首页和Escape关闭；代表性浅深页面检查。Ghost两帧形态变化；TextLoop offset持续变化，表单聚焦后1101.564保持不变。隐藏/减少动态效果/WebGL回退由源码及定向测试覆盖，未全面模拟设备。
- 最后视觉修正进入唯一一次最终Docker构建，退出0，类型检查和25静态页通过；既有Autoprefixer警告未处理。仅替换3001前端；正式搜索页五组导航和canvas确认，error为空。3002停止。未运行全套测试/首页哈希，也未提交业务数据或调用付费模型。[详细交付](docs/handoff/2026-09-26-react-bits-navigation-decor.md)。

## 科技材质分层（最终部署版）

- `tests/material-stack-scene.test.tsx`：1项通过，验证仅科研数据/比较路由接入和展开/收拢状态。上传定向4项此前通过；最后删除装饰SVG及CSS修正未重复业务测试。
- 浏览器：科研数据浅深真实透明材质无底色框，3张图像均加载1536px源图；点击展开后铜层translateY(-21px)、铝层translateY(26px)。手机比较390px视口、375px文档宽，无横向溢出。徽章碰撞已修正；最后桌面文字宽度由40%改30%/300px未重复截图。
- 最终 `docker compose ... build frontend` 退出0，保留既有Autoprefixer/缓存警告。[最终构建日志](docs/handoff/2026-09-26-material-stack-build.log)。只更新前端；生产DOM确认3材质层、展开按钮、无被否定的workspace-motion，PNG HTTP200。临时3002停止；未提交业务数据或模型请求。
- 同一轮较早的线框原型和其构建被用户否定，未部署；其通过的检查不能作为当前材质实现验证。

## 上传操作区清晰度（最新修正）

- `npm.cmd --prefix frontend run test -- tests/upload.test.tsx`：4/4 通过，覆盖超限、拖放、上传锁定与重置。未运行全量测试。
- 开发浏览器检查浅深两种外观；实际标题 28px、选择/提交字号 18px、控件高 50/48px。最终仅将误连带的帮助段落颜色恢复原值，未重复截图。
- 首次生产构建通过后，因上述作用域修正重新构建最终版，两次均退出 0，保留既有 Autoprefixer 警告。最终日志见 [构建日志](docs/handoff/2026-09-26-upload-clarity-final-build.log)。前端单独替换成功，正式 3001 浏览器确认新文案及无文件时提交禁用。未触发真实上传或模型请求；临时开发服务已停止。

## B 离子迁移科研想法（本轮最终工作区）

- `tests/ideas-ion.test.tsx` 定向 1 项通过，验证选择反馈及生成请求仅传明确选中的数据集 ID。
- 开发浏览器桌面浅深、手机单列已检查；桌面文档/视口1265/1265，手机375/375。6个SVG粒子transform随时间变化，输入聚焦后两次读取相同；减少动态效果/离屏/隐藏由源码审查覆盖。
- 首次浏览器发现全局header导致蓝色横框和标题挤压，修复后定点确认。最终手机遮罩.55未重复截图，已进入生产构建。
- 一次前端Docker构建成功，类型检查和25静态页通过；保留Autoprefixer `end`支持警告（本页一条及既有规则）。只替换3001前端，8001后端容器未变；ideas/两张WebP/代理health均200。生产浏览器确认新素材、6粒子、宽度1265无溢出、error为空。
- 当前实际数据集和想法无列表项，没有为了验收写入记录，也未调用模型/OCR/导出；未做完整业务写入端到端验收、全量测试或首页哈希。[交付和日志](docs/handoff/2026-09-26-ideas-ion.md)。

## 帮助与上传用户反馈修正（本轮最终代码）

- `tests/upload.test.tsx tests/help.test.tsx`：5 项通过。帮助指南未删除，上传行为仍用既有接口。
- 开发浏览器确认上传浅/深右侧铺图与开放表单，帮助 CTA 删除；深色且聚焦时 input 背景透明、border=0、box-shadow=none，外壳保留单层焦点框。没有重复全路由验收。
- 一次前端 Docker 生产构建成功，类型检查与 25 静态页通过；保留既有 Autoprefixer 警告。仅替换前端，3001 的 upload/help/代理health均200，8001后端容器未变。未重复生产截图、真实上传或模型/OCR。
- [完整记录及构建日志](docs/handoff/2026-09-26-layout-corrections.md)。后续 A/B/C 候选为生成示例图，不属于运行验证。

## 非首页动效升级（最终工作区与生产前端）

- 22 项定向测试通过：上传/帮助 5 项、LatticeLoader/壳层 9 项、论文插画分配 2 项、论文库 6 项。没有全量测试或首页哈希检查。
- 最终代码的一次 Docker 前端生产构建退出 0，Next.js 编译/类型检查及 25/25 静态页面生成成功。保留 9 条既有 Autoprefixer `end` 支持警告；[构建日志](docs/handoff/2026-09-26-motion-build.log)。
- 开发浏览器检查上传浅/深主题素材与 SVG 实际流动、帮助搜索 OCR、390px 手机帮助/导航、论文库现有 10 篇配图各异，破图和记录的 error 均为 0。修正首屏按钮位置及背景横向溢出后定点确认；最后帮助透明度/分类微调未重复截图。
- 仅 `up -d --no-deps frontend`，退出 0；生产 3001 的上传、帮助、论文库和代理健康均 HTTP 200。生产浏览器上传页标题为“储能科研学习平台”，读取新 WebP；scrollWidth/clientWidth 均 1265、error 为空。原后端 8001 容器 ID 未变且健康，临时开发服务已停止。
- 检查对象为本轮 2026-09-26 最终工作区和所构建镜像，非历史提交。减少动态效果/离屏暂停由源码审查覆盖，未逐项操作系统设置；未触发真实 PDF 上传、模型/OCR、删除或逐路由完整业务验收。详见 [完整边界](docs/handoff/2026-09-26-motion-upgrade.md)。

## 公众号官网公开索引（最终部署）

- 前端校园定向测试 **3/3 passed**；覆盖 link-only 与 unknown 展示、校方出处/微信原文链接、既有校园资讯仍可见，以及快速切分区时丢弃旧响应。后端本轮新增 **2 项 + 回归 2 项 passed**。
- 前端生产构建退出 0，部署至正式前端 3001 / 后端 8001。迁移 `0026`；升级前备份为 `local_state/upgrade-snapshots/20260925-public-links-before/`，原有 10 篇论文保留。
- CUA 实际检查 `/campus`：30 条去重链接、unknown 30、recent 0、archive 0；第一页 20 条、共 2 页；link-only 提示、公众号原文链接与校方列表页出处可见。前端代理 `GET /backend-api/api/v1/campus/public-links?scope=unknown&limit=100` 返回 HTTP 200、30 条，记录见 [生产检查快照](docs/handoff/2026-09-25-campus-public-links-frontend-check.json)。
- 本轮发现 35 条来源记录并按 URL 合并为 30 条，5 条有多个校方来源；发布时间全部为空。只读取官网页面的可见标题/链接，不访问微信正文、不调用模型、不生成摘要或截止提醒。
- 后端沿用已有依赖刷新源码部署；没有从零执行完整依赖镜像构建。未跑全量套件。AI 真实摘要仍未验收，受限小程序/群渠道也未接通。

## 校园质量迭代（最终后端与已部署前端）

- 后端 Python 3.12：`pytest tests/test_campus.py tests/test_campus_analysis.py -q --tb=short` 最终 **18 passed**；含真实新闻网空标题/日期装饰回归、日期分区、缓存预算、队列失效和 DeepSeek 请求参数。模型测试使用 fake。
- 前端校园交互 **1 passed**；本轮一次前端 Docker 生产构建通过。`node scripts/workspace/verify-campus-live.cjs` 在生产检查三个页签、来源/事件/提醒 200、无页面异常及校园内 alert，通过。之后无前端代码改动，仅后端修复，没有重复浏览器或截图。
- 最终后端源码刷新并重启 8001，health/database ok；前端 3001 代理 sources 返回 66 个来源；近期、未知、历史三个 API 正常。迁移 0025、既有论文 10 篇；68 条已读取新闻来源记录发布日期缺失数降为 0，纯日期错误标题为 0，修复未增加提醒。
- 真实 AI **未通过**：当日 20 次失败（7 ModelProviderError、13 ValueError），修正非思考模式/2400 输出预算及 evidence 格式说明后，最终样本被每日上限拦截、未调用。规则回退可用，不能把 fake 测试成功等同于真实 AI 成功。
- 后端复用已有依赖镜像刷新，不宣称从零依赖构建通过；未跑全量套件、首页哈希、OCR、论文写入。快照、备份、镜像及具体限制见 [质量迭代交接](docs/handoff/2026-09-25-campus-quality-integration.md)。

以下首版数据仅为历史验证。

## 校园公开资讯接入

最终生产快照（UTC `2026-09-25T07:04:55Z`）见 [只读检查 JSON](docs/handoff/2026-09-25-campus-live-check.json)：health/database 均 `ok`，迁移 `0024`，论文 10 篇，资讯 77 条、来源页 137 条、提醒 3 条；32 个来源均启用，状态为 6 `ok`、3 `partial`、2 `blocked`、21 `pending`。分组为未来技术学院 6、工科学院 15、学校级入口 2、书院 9。首个未来技术学院通知公告样本为 21 个链接、12 条详情、0 次失败；其余 pending/partial/blocked 按 JSON 状态如实呈现，不宣称全校覆盖。

最终后端部署已读取未来技术学院 `.contt_tit > span` 与机械学院 `.arc-info` 的明确发布日期。样本公告日期 `2026-06-11` 只作为发布日期且未产生提醒。最初入库的12条无发布日期事件将在常规下次刷新时更新，尚未声称已回填；活动时间未知仍显示，空/旧发布日期不会将其隐藏。来源按优先级与发布日期排序。Sol 报告最终后端定向测试 8 项通过；前端定向交互测试 1/1，生产浏览器 `/campus` 标题及 sources/events/notices 均200、无页面 JS 错误或校园页内 alert。前端最终镜像构建通过；后端最终源码使用已有依赖镜像刷新。上一轮从零构建曾因 Debian 下载 HTTP 502 失败，本轮未声称从零构建。

- 迁移 `0024` 已应用。部署前数据库备份位于 `local_state/upgrade-snapshots/20260925-campus-before/energy_copilot.db`，SQLite `quick_check` 通过；既有论文数 10。旧前后端镜像以 `:before-campus-20260925` 保留回退标记。
- 正式服务为前端 `http://localhost:3001`、后端 `http://127.0.0.1:8001`。校园来源、资讯和提醒 GET 均 HTTP 200，健康检查通过。生产浏览器打开 `/campus`，标题和来源列表可见，无页面 JS 错误或校园页面内 alert。首次脚本检查误将 Next.js 空白全局 route announcer 认作错误，改为只检查 `.campus-page [role=alert]` 后通过。
- 已启用 32 个固定来源：未来技术学院 6、工科学院 15、学校级入口 2、书院 9。首个真实来源样本为未来技术学院“通知公告”：21 条列表链接、12 条详情读取、0 次失败；最终数据库快照有 77 条资讯、137 条来源页面和 3 条提醒。其他来源状态见最终 JSON，不能推断都已成功，也不是全校栏目覆盖。
- Sol 报告最终后端修正版的 8 项定向测试通过；Luna 校园交互测试 1/1 通过，包含来源控制、关注/已读、日期原文、北京时间显示与原文链接。前端生产镜像因时间显示和请求竞态修正构建两次，第二次最终构建通过。后端采用复用已有依赖镜像刷新源码；上一轮从零镜像构建曾遇 Debian 下载 HTTP 502，本轮不声称从零构建。运行时 BeautifulSoup 为 `4.15.0`。
- 服务运行时来源正常每 12 小时检查；429 后延至 24 小时，401/403 会停用来源。关注、日期无来源冲突且至少有一个来源启用时，日期前 3、2、1 天及当天分别生成一次站内提醒。调度依赖后端持续运行，解析不调用模型。

本批未跑全量前后端套件、首页哈希/冻结检查或新增截图；未调用付费模型、OCR、上传或论文写入。当前覆盖固定公开来源栏目和有限列表窗口，每轮详情上限 12；不接入微信公众号、QQ/微信群或需登录的小程序。详细边界见 [校园资讯接入记录](docs/handoff/2026-09-25-campus-integration.md) 与[生产只读快照](docs/handoff/2026-09-25-campus-live-check.json)。

## 独立场景与插画修订（最新）

- `node scripts/workspace/check-visual-diversity.cjs` 退出 0：开发端口 3002 连接实际后端，禁止外部和写请求，无 API fixtures。帮助 Light 1440px、Dark 390px，日报 Light、引导 Dark、订阅 Light，共 5 次视图；页面/HTTP 错误 0，横向溢出 0。
- 帮助页每个主题下均读到 28 个图格、28 个不同位置；现有日报 4 条提醒读到 4 种不同配图。各页场景图格不同，桌面场景宽 920px，reduced-motion 下 animation 为 none。
- 原始结果见 `docs/non-home/diversity/review.json`；实际数据截图仅保留在本机 `local_state/visual-diversity-review/`，未拷入公开静态目录。
- 预览后最后收尾：蒙版顶部/底部更柔和，日报标题插画尺寸收小以免超出横幅，阅读器暗色背景降低透明度，并简化插画判断；没有再次截图。因此截图只对应收尾前视觉。
- `docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend` 完成并退出 0，包含上述最终修改。既有 globals/contest/research-tools CSS autoprefixer 警告保留，无构建错误。
- 只替换前端：设置 FRONTEND_HOST_PORT=3001、BACKEND_HOST_PORT=8001 后执行 Compose `up -d --no-deps frontend`，退出 0。生产代理健康为 ok，帮助页 200，返回新背景和专用帮助图集标记。
- 未运行全量测试、哈希检查、后台模型/OCR/上传/写入或后端镜像重建。没有重新逐页检查所有业务流程。

## 生产替换与真实后端联通（最新）

检查版本：包括配置引导蒙版背景与删除右下角装饰文案的当前前端，以及本轮前端端口自动避让启动器。前端构建后未再改前端源码；以下不是旧 fixture 结果。

- Compose 构建中，前端 Next 生产构建并导出镜像成功；后端标准完整构建因 Debian libatomic1 下载 502 失败。确认现有镜像 requirements 与源码一致后，基于已安装依赖镜像刷新后端源码成功（退出 0）。不声称后端从零构建通过。
- 启动器 3 项定向测试通过：前端空闲端口选择、Compose 可配置映射、IPv4 前后端健康探测。`start.ps1` 实际退出 0；后端 healthy，前端就绪，分别监听 8001/3001；另一项目保持 8000/3000 正常运行。
- 直接后端健康、前端代理健康、代理论文列表均 200；现有论文总数 10。
- Edge 生产只读抽查 `/onboarding`、`/library`、`/knowledge` 均 200，壳层存在；真实论文、问答状态和历史 GET 均 200；记录的页面/HTTP 错误为 0。
- 配置页 Light/Dark 日夜图片和透明蒙版均存在，标题分别为深色/浅色，无右下角装饰文案节点；1440×900 无横向溢出。未拍摄新截图。
- 浏览器禁用非本地与写请求，无请求被阻止，未提交设置或触发模型/OCR/上传。没有 API fixtures 注入，没有全量套件或哈希检查。复杂论文、写操作、模型能力和所有 19 页完整业务仍未在本轮逐一验证。

[详细部署记录](docs/handoff/2026-09-25-integration.md) · [实际浏览器结果](docs/handoff/2026-09-25-live-check.json)。以下保留历史批次结果，“未部署/未构建”只指其当时状态。

## 配置引导背景深化

- `PREVIEW_ROUTES=/onboarding node scripts/workspace/preview-remaining.cjs` 退出 0：Light／Dark 1920×1080 与 Light 390×844 共 3 次视图，无页面横向溢出或记录的页面／图片错误。检查的是 onboarding-atmosphere.css 接入和移除小方图后的版本。
- 只改配置页视觉与装饰动效，七步 handlers 保持。浏览器采用 reduced-motion，动效关闭路径与布局已呈现；慢速动画的整周期未录制或另行检查。没有运行类型／单元／全量测试、生产构建或哈希。未提交设置、调用模型或写入真实数据。
- 本页三张截图已覆盖上一版同名预览，targeted-recheck.json 为本次 3 次视图记录。

## 剩余九页视觉深化

- `node node_modules/typescript/bin/tsc --noEmit` 退出 0，仅执行一次。
- `node scripts/workspace/preview-remaining.cjs` 首批退出 0：九页 Light 桌面，加比较／诊断／引导 Dark、搜索／问答／设置窄屏，共 15 次视图，无横向溢出，记录的页面与资源错误为 0。
- 截图审查后修正 Dark 诊断服务名称／数字对比和系统／引导卡片样式优先级；仅针对 settings、diagnostics、maintenance、onboarding 复查 7 次视图，退出 0。15 个截图文件中相关截图更新为修正后版本。
- 比较与问答仅接收显式合成 POST 响应，搜索为合成来源结果。没有真实模型调用或数据写入；未操作配置保存、上传、索引、备份、清理。没有全量测试、生产构建或哈希检查。
- [截图与检查记录](docs/non-home/remaining/README.md)。源码实现和本次定向检查不能替代用户视觉审阅或生产业务验收。

## 横幅渐变与通用主题图片修正

- `node scripts/workspace/preview-banner-gradients.cjs` 最终退出 0，五类横幅（竞赛、论文库、订阅、学习、日报）双主题共 10 项检查通过；确认图片层有透明遮罩、底层无重复位图，并在出现通用主题卡片时检查正确日夜图片和占位 SVG 已移除。保留横幅和卡片局部截图。
- 首次检查在主题过渡中读到旧 background-image；确认主题变量已正确切换后，脚本改为等待图片层完成主题切换，通过。未据此增加业务代码或跑全量测试。
- 仅 Next dev、合成 API fixtures；没有真实数据写入、模型调用、生产构建、单元测试或哈希检查。移动端仅调整图片强度，未另做浏览器验收。[局部预览与检查记录](docs/non-home/tools/gradient-preview/)。

## 科研工具四页面

- 一次 `node scripts/workspace/preview-tools.cjs` 退出 0。Next dev + Edge 受控只读 fixtures；四路由 Light/Dark 1920×1080，以及四路由 Light 390×844，共 12 次视图检查、12 张截图，无页面横向溢出；记录的页面错误、资源错误和遗漏 fixtures 为 0。
- 仅开发模式页面抽查；没有运行生产构建、单元测试、全量套件或哈希检查。截图含开发指示器，不是干净生产验收截图。
- 未触发真实后端、模型或数据写入；上传、AI 生成、导出内容和完整业务流程未在本批验证。[结果与原始记录](docs/non-home/tools/README.md)。

## 学习中心与详情

- 定向 Vitest 20/20：learning 16、learning-analytics 4；包括原有学习操作、加载／错误、范围竞态、零活动、真实分布和键盘明细。
- 生产构建退出 0，类型检查和24个静态页面通过；受控 Edge 浏览器33张截图、30次视图／标签无溢出，交互通过，运行时错误与遗漏 fixtures 为0。此前已执行首页33文件冻结检查。以上均为已执行记录。
- 两次写请求均为显式拦截的测试创建／手动掌握；未调用真实后端、模型或操作真实学习数据。
- 最后收尾修正插画方形比例与筛选文字不换行，仅CSS。用户随后要求停止反复验证，因此没有再运行构建、截图、测试或哈希检查；现有截图对应收尾前。以后不默认全量测试或哈希检查，仅必要定向验证。
- [结果与边界](docs/non-home/learning/README.md)。

## 科研日报与论文研读

- 定向 Vitest **41/41**：research-daily 4、reader-refinement 4、paper-experience 33。验证实际返回统计、独立请求失败与 loading、缩略页定位及边界、报告优先顺序；既有单篇文档／公式／引用／手动笔记／删除确认检查通过。
- 最终 `npm.cmd --prefix frontend run build` 退出 0，类型检查与 24 个静态页面生成通过。后续仅 CSS 细节调整，因此追加构建和浏览器复核，没有重跑无关业务套件。
- `node scripts/workspace/verify-daily-reader.cjs`：Light/Dark、1920×1080／1440×900／390×844；全文／摘要、日报空状态和两种独立请求失败。27 张原生截图、23 次视图无横向溢出；双主题页码参数、缩略切页、解析工具展开、手动笔记保存及图表原页预览通过。运行时错误、遗漏 fixtures 为 0。[结果与截图](docs/non-home/daily-reader/README.md)。
- 首轮交互因测试脚本未选中图表而失败，修正步骤后通过。截图审查另修正文案字号、状态条颜色、旧灰色报告底层、横幅背景接缝、缩略页选中样式的优先级；不将首轮失败算作通过。
- `python scripts/homepage/check-freeze.py`：33 个冻结文件完整。相关文件 `git diff --check` 退出 0。
- 全部 API 均显式拦截，合成 PDF 和页图来自同一受控六页文档。仅两次受控笔记 PUT；没有真实后端、模型、OCR 或研究数据写入，也未重建 Docker。复杂真实 PDF 未在本轮验证。上批论文库／订阅与本批日报／研读均已获用户视觉验收通过；本次确认不增加测试覆盖或改变上述验证边界。

## 视觉纠偏样板：论文库与研究订阅

- 定向 Vitest **18/18**：library-paper-state 6、subscriptions 4、visual-data 8。覆盖加载集合范围、证据／年份统计、预览与收藏；创建抽屉保留原参数、周期修改／名称确认取消；运行错误隔离；主题匹配、空／单条／密集记录、无效时间、键盘提示、图表响应式坐标及可访问 ID。最后图表修正仅重跑相关 8 项，没有重复全套测试。
- `npm.cmd --prefix frontend run build`：生产构建退出 0，通过类型检查并生成 24 个静态页面。新 CSS 的 flex-end 兼容性警告已修正；未新增依赖。
- `python scripts/homepage/check-freeze.py`：33 个冻结文件完整。
- `node scripts/workspace/verify-refinement.cjs`：两个样板页 Light/Dark，1920×1080、1440×900、390×844；检查图文卡实际网格、宽屏趋势图进入首屏、无横向溢出、图片请求成功、图表键盘焦点、创建抽屉 Tab／Escape／焦点恢复、订阅设置展开、论文预览，以及空／单条／错误状态。原生截图和 JSON 见 [结果目录](docs/non-home/refinement/README.md)。
- 首轮发现 samples.css 覆盖新卡片布局、窄栏图集裁切、CSS 生成的加号导致按钮精确可访问名称不匹配，以及固定 SVG 坐标造成留白；已修正并复核。响应式网格线终点追加回归测试。未将首轮失败当作通过。
- 浏览器仅使用显式受控 API fixtures，未操作真实论文库、启动订阅后台任务或调用模型。截图数量是测试数据；真实后端联通与其他非首页页面深层视觉不属于本轮验证。视觉是否接受仍由用户判断。

## 非首页 Phase 1

- 定向 Vitest 共 **87/87**：workspace-shell 7、workspace-drawer 11、workspace-primitives 1、library-paper-state 5、knowledge 3、compare 2、paper-experience 33、dashboard-research 6、search 19。搜索文件为 `tests/search.test.ts`；其余为 `.test.tsx`。最后 CSS 修正后只重跑生产构建与浏览器，没有重复无关后端或全量测试。
- `npm.cmd --prefix frontend run build`：最终生产构建退出 0，24 个静态页面生成并通过类型检查；无新增依赖。
- `node scripts/workspace/verify-phase1.cjs`：生产前端、19 个非首页路由双主题，56 次视图检查（含重复交互场景）、59 张不同原生截图；1920×1080，重点页另检查 1440×900、1366×768、390×844。页面／主区域无横向溢出；运行时 pageerror 与遗漏 API fixtures 均为 0。
- 实际浏览器核验搜索提交、论文预览、问答／比较证据页码与摘要回退、原生 modal 的 Tab 循环／Escape／关闭后焦点恢复、移动导航、跨首页主题切换与刷新持久化。证据边界仍由现有 API 数据提供。
- 视觉审查修正 Dark PDF 缺失提示、Dark 引用摘录、Light 学习卡片、移动抽屉标题布局。学习卡片正文对比度 14.73:1、Dark 引用摘录 12.12:1。独立审查指出的学习卡片白字白底已修正。
- `python scripts/homepage/check-freeze.py`：33 个冻结文件完整。新截图存于非首页验收目录，不覆盖原首页基线；主题切换截图等待实际导航文字颜色稳定，避免捕获过渡帧。
- [逐页与交互结果](docs/non-home/phase1/acceptance/verification.json)、[定向交互复核](docs/non-home/phase1/acceptance/interaction-verification.json)、[截图索引](docs/non-home/phase1/README.md)。浏览器全程显式拦截测试请求，未操作真实数据或付费模型；真实后端联通、复杂实际 PDF 与所有业务工作流端到端不在本次验证范围。
- 首轮运行暴露两处 fixture 缺字段，修正测试数据后继续；浏览器另发现焦点循环与移动导航进入时机问题，已修正并完成定向回归。没有将这些首轮失败记作通过。

## 此前：首页冻结与归档

- `node frontend/node_modules/typescript/bin/tsc --project frontend/tsconfig.home-hero.json`：退出0。
- frontend内 `node node_modules/vitest/vitest.mjs run tests/dashboard-research.test.tsx`：6/6通过。保留首次配置、实时摘要绑定、下半区、主题/快捷键、提醒失败状态的检查；WebGL在DOM单测中隔离、在浏览器中真实加载。
- frontend内 `node node_modules/next/dist/bin/next build`：退出0，所有业务路由生成；保留既有globals.css中autoprefixer兼容性警告，未借机修改其他页面样式。
- `node scripts/homepage/verify-home.cjs`：正式生产/dashboard、根重定向、八入口、资源200、主题持久化、上传导航、Ctrl+K、Storage hover和较矮窗口避让；证据与真实PNG见 docs/homepage/acceptance。
- 移动前后709文件SHA-256一致；30个被删除媒体副本与保留文件再次逐项SHA-256一致；详见 docs/handoff 清单。
- 真实后端当时未运行、Docker管道不可访问，浏览器使用显式受控API fixtures；没有读写真实论文、触发付费模型、运行全量后端测试或重建Docker镜像。
- 初次页面单测遇到Vitest经典JSX环境缺React全局；仅测试设置补齐后通过。较早V13测试的辅助射线坐标误差和旧记录完整保存在归档，不代表当前运行错误。

历史完整报告：archive/hero-development-2026-09-24/root-documents/TEST_REPORT.md。

## 储能编年史最终悬停修复补充（2026-10-03）

本轮Docker frontend build共4次成功：首次完整、素材绑定修正后缓存命中、浅色按钮覆盖修复增量、深色hover修复增量；frontend容器共替换3次，后端未重启。后两次仅因实际失败修复。生产构建约57.2s与63.8s（后两次），保留既有globals/workspace组件Autoprefixer/cache警告，未改对应源文件。9项Vitest及完整功能检查不再重复。
最终补充：目视发现深色悬停规则仍覆盖选中背景，局部保留html[data-theme]优先级并提高CTA元素级，重新增量构建/前端部署后仅验证此新问题。浅/深选中hover分别为rgb(90,129,126)/rgb(164,199,180)，对应文字与主题bg一致；CTA无全局渐变覆盖、前景背景不同，检查exit0。更新三张深色截图以等待主题过渡完成；功能全套未重复。悬停数据见docs/screenshots/chronicle-main/hover-runtime.json。


**首页品牌名称（2026-10-03，已部署3001）**：按用户确认保留三行英文，改为 Energy Storage / Research & Learning / Smart Platform，中文为“储能科研学习智慧平台”，首页品牌链接标签同步。Sol仅修改Hero.tsx一行，保留现有布局。一次前端生产构建与部署成功，3001实际文案与截图确认；未运行测试或全套检查。

## 2026-10-03 液流编年史四路线

- 命令：npm.cmd --prefix frontend run test -- tests/chronicle-flow.test.tsx tests/chronicle-revision.test.tsx tests/storage-chronicle.test.tsx --maxWorkers=1 --minWorkers=1。一次执行，3文件27项通过、exit0，5.89s。
- Docker frontend生产构建两次成功：第一次新内容，第二次纳入发现的市值来源标签修正；只部署一次前端3001。两日志在docs/handoff/2026-10-03-chronicle-flow-build.log及chronicle-flow-source-label-build.log。
- 实际3001 HTTP200，4路线各6章切换/进入详解/返回保持状态、对应图解码、参考资料折叠与原始链接通过；年份11/10/9/11。深色正文18px，390px无横溢，pageerror0。初次验证label严格匹配超时，修脚本locator后通过；附加单项检查使用真实共享主题按钮，不重跑全部路线。
- 未运行全量、后端或哈希检查。既有其他页面CSS/webpack警告未修改。截图及数据：[液流运行记录](docs/screenshots/chronicle-flow/runtime.json)。

## 2026-10-03 编年史CTA小箭头删除

仅改按钮文字；一次Docker frontend生产构建、仅前端3001部署成功，实际HTTP200且进入详解按钮无末尾箭头。未运行测试或截图。构建日志：docs/handoff/2026-10-03-chronicle-cta-build.log。

## 2026-10-03 编年史加粗及成本单位格式

新增chronicle-markdown.test.tsx两项，修改前2失败(exit1，1.44s)，source修复后2通过(exit0，1.41s)，未全测。一次Docker frontend生产构建和仅前端3001部署成功；实际论文与储能适配展开区各6标签正确strong、字面星号false，美元成本单位正常且无误生KaTeX。未截图。日志docs/handoff/2026-10-03-chronicle-markdown-build.log。


## 2026-10-03 氢4定向验证与部署

新5项行为最终均通过：首次4/5，唯一失败为测试预期“热量”与正确原文“燃料热值”不一致；只改该断言并单项复跑1通过/4跳过。首次red3/3失败确认未接路线。Docker frontend生产构建exit0、仅前端部署exit0/healthy。Edge实际HTTP200，四路线匹配实景/材料概念/政策原页加载、首年阅读返回、共享双主题、暂停阅读及390px无横溢通过，pageerror0。首次runtime图片加载前断言产生竞态，改为等待load后完成；未改产品、未复测旧批或截图。

命令：`npm.cmd --prefix frontend run test -- tests/chronicle-hydrogen.test.tsx --maxWorkers=1 --minWorkers=1`（20:29:57，4通过1失败，2.90s）；失败项命令追加`-t "hydrogen facts distinguish"`（20:30:35，1通过4跳过，1.62s，exit0）。Docker使用两份compose、FRONTEND_HOST_PORT=3001，仅build/up frontend。实际runtime记录：docs/handoff/2026-10-03-chronicle-hydrogen-runtime.json。


**首页搜索提示（2026-10-03，已部署3001）**：按用户截图，Sol仅删除Hero搜索框右侧⌘K提示；放大镜、搜索路由及实际Ctrl+K逻辑保留。一次前端生产构建/部署成功，3001实际搜索链接已不含提示，截图与备份在docs/homepage-proposal/2026-10-03-search-hint/。未运行测试。


## 2026-10-03 电磁批

新电磁4项red4失败确认未接入；green4通过，20:40:58，2.13s，exit0。唯一Docker frontend production build与仅frontend部署均exit0/healthy。Edge实际3001 HTTP200、两路线匹配素材/材料概念/政策原页加载、论文304Wh/m³与10MJ、双主题、暂停阅读、390px无溢出，pageerror0。首轮runtime全局同名论文按钮造成严格选择器歧义，限定编年史nav后完成检查，未改产品或复测旧批。

命令：`npm.cmd --prefix frontend run test -- tests/chronicle-electromagnetic.test.tsx --maxWorkers=1 --minWorkers=1`；runtime记录docs/handoff/2026-10-03-chronicle-electromagnetic-runtime.json。未全测/重复旧批/截图。


## 2026-10-03 首页底栏字号与滑动高亮（已部署3001）

Sol仅修改HomeDock.tsx、hero.css与homepage-photographic.test.tsx。按用户截图及GlideSelect附件，将现有真链接菜单加入220ms滑动暖金pill、175ms向上弹出；pointer/focus使用同一高亮位置，当前项加粗/加深，展开分类有金色标记，减少动态效果时停动画。底栏桌面标题clamp(18px,23u,25px)、小字clamp(12.5px,17u,18px)，窄屏16/12px；菜单18px、摘要14px、行49px。保留六分类、19子路由、开闭逻辑及原玻璃底色，搜索提示删除保留，无新依赖。

单份homepage-photographic定向新增断言旧实现先失败，修改后4项通过；一次前端生产构建、仅前端3001部署成功。实际1280×720标题18px/小字12.5px/菜单18px，活动项weight700、light rgb(8,37,54)，Tab切换pill从translateY(0px)移到49px，过渡0.22s；dark活动文字rgb(255,240,209)、金色半透明pill、分类底色透明。390×844页面无溢出，标题16px/小字12px，菜单x18.8–371.6/y370–676，Dock bottom830；默认尺寸与浅色已恢复。未全量/哈希/重复测试，后端不变。实际截图、三份改前基线与构建日志见docs/homepage-proposal/2026-10-03-dock-glide/。


## 2026-10-03 最终EC3与25路线完成

新EC4项red全部失败确认未接入；green首次3通过1失败（21:31:57，2.51s），失败仅为测试预期1000与正确原文1,000的千分位不同。修断言后只复跑失败1项，并在同命令运行受铅酸上线影响的旧2项：3通过19跳过、exit0（21:33:09，4.60s）。没有重跑旧18全组。

命令：`npm.cmd --prefix frontend run test -- tests/chronicle-electrochemical.test.tsx --maxWorkers=1 --minWorkers=1`；失败/相关旧项命令：`npm.cmd --prefix frontend run test -- tests/chronicle-electrochemical.test.tsx tests/storage-chronicle.test.tsx tests/chronicle-revision.test.tsx -t "final electrochemical papers|铅酸已研究路线|lead acid independent" --maxWorkers=1 --minWorkers=1`。

Docker前端生产构建exit0；因晚到Xcel2026官方公告补引用和当时MPUC待批准状态，追加一次必要生产构建exit0，之后仅frontend部署一次exit0/healthy。构建仍有其他页面原有Autoprefixer/缓存警告，未改无关CSS。

一次最终Edge3001实际HTTP200：三路线首年选择/返回、论文8,529/2200h/30kWh、无字面星号、材料概念/企业媒体/政策原页加载、全国电储图关闭、Xcel300MW/30GWh计划段及原始链接、双主题/暂停阅读/390px无横溢，pageerror0。记录见docs/handoff/2026-10-03-chronicle-electrochemical-runtime.json。

静态接入统计：25/25路线全部接入并部署正式3001：252时间节点、99材料/部件专题、150详解章节、正文约72464汉字，509个去重研究链接（章节Markdown链接与节点原始来源；不含图片/公司档案）。素材108记录/99可用。所有入口均有独立研究，不再有实际待整理路线。 本批新数据plain detail标记检查0。未全套/截图/哈希/其他业务回归。

## 2026-10-03 编年史图片修订（实际执行）

新增tests/chronicle-media-revision.test.tsx：3/3通过，exit0，22:38:02，2.18s。命令：npm.cmd --prefix frontend run test -- tests/chronicle-media-revision.test.tsx --maxWorkers=1 --minWorkers=1。覆盖精确2021节点优先、EM三类不同背景、实际切换与Reader同步。

一次docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend exit0；一次同配置up -d --no-deps --no-build --wait --wait-timeout 120 frontend exit0，Healthy，仅前端3001。已有StorageCityApplications样式Autoprefixer/cache warnings保留，未改邻近业务。

正式3001 Edge headless一次代表检查exit0：HTTP200；超级电容2021 INL→模组→Reader背景；绝热CAES厂房→膨胀机→肥城全景（图注明确非应城事件）；显热2025 Pornainen→Antora碳块→Antora公司模块；均实际加载naturalWidth>0。主题dark/light切换；390px无横向溢出，pageErrors=[]。未截图、未全量测试/哈希、未重测旧批。

## 2026-10-03 编年史巨大年份几何修复

- Red实测：旧3001、1280×900、潜热/储能适配，年份box y266.44–509.64，h2 y477.34–526.94，横向也重叠，垂直相交32.3px。
- Green：正式3001，Edge headless、reducedMotion reduce，1920/1280/390×light/dark六场景；每场景检查历史2024和储能适配“应用”的year/h2/intro真实rect，无相交、year在stage范围内、页面无横溢，exit0。1920舞台1656px左右列、1280舞台1016px与390舞台366px上下行；历史对应最小间距184.61/58.75/57.09px。
- `docker compose -f docker-compose.yml -f docker-compose.harness.yml build frontend` 最终exit0；早于宽桌面要求的初稿构建exit0但未部署。最终`up -d --no-deps --no-build --wait --wait-timeout 120 frontend` exit0/Healthy；端口3001/8001，仅frontend。
- 原有StorageCityApplications Autoprefixer/缓存警告保留。未跑单元或全量测试、未截图；证据docs/handoff/2026-10-03-chronicle-year-layout-runtime.json。
## 2026-10-03 编年史GlideSelect

`D:/claude code/node.js/node.exe node_modules/vitest/vitest.mjs run tests/chronicle-glide.test.tsx --maxWorkers=1 --minWorkers=1 --reporter=dot`（frontend cwd）：red2失败（原生select无新portal/swap），green2通过23:20:27，2.82s，exit0。初始项目根加--root运行失败于文件定位，无测试执行，不作red证据。两项覆盖四类联动/材料公司素材/详解状态、keyboard/outside与opt-in动画。

一次Docker `build frontend` exit0，`up -d --no-deps --no-build --wait --wait-timeout 120 frontend` exit0/Healthy，正式3001。原有非本页Autoprefixer/缓存警告未改。

Edge四场景1280/390×light/dark runtime exit0：四类menu在视口内且portal直属BODY；浅背景rgb(255,253,250)/文字rgb(22,41,67)，深背景rgb(23,54,83)/文字rgb(231,238,245)。展开0.18s、pill0.22s、label0.16s。潜热选项行44px，第二项pill translateY45与offsetTop45一致；企业标题和图片改变、Reader保留、键盘与外点关闭通过、pageerror0。没有穷举所有路线长选项、没有全套/截图；证据docs/handoff/2026-10-03-chronicle-glide-runtime.json。

## 2026-10-04 GitHub 发布准备

主控报告前端与后端 Docker 镜像构建均 exit 0，独立 TypeScript 检查 0 errors。发布树独立运行在3018/8019：health、dashboard、论文 API proxy、paper 1 figure thumbnail（image/png，61,989 bytes）及校园 sources 均HTTP 200。README所列六张公开截图均为1280×720初始视口；home-dark在fullPage接口失败后使用viewport截图，其余五张fullPage截图，未对图片做编辑。公开 `main` 推送 exit 0，首两个提交均采用 `[skip ci]`；未运行前后端全量测试。临时 3018/8019 容器、3019 dev 与合成演示数据已清理；原 3001/8001 未改动。此记录不包含远端元数据或关键文件核对。

最终远端确认：GitHub 官方 API 返回公开 `main` 提交 `7776424`、`Public=true`、`License=MIT`。独立发布工作树与 remote 一致且 clean，共807个跟踪文件、6张截图、147个编年史文件、8个校园后端文件；确认目录为 `outputs/github-release`，不是原开发仓库。未运行新增测试。



