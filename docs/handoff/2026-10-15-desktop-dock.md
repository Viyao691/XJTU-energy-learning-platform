# 首页电脑端菜单局部修订

用户要求：选中入口不要黄色下划线；仅电脑端把展开选项框增大并和入口对齐、增大字体。只修改 `frontend/components/home-hero/hero.css`：删除选中按钮::after装饰，min-width901px下菜单width100%、字号clamp16–22px、行高至少48px。手机保持160px/14px/44px，黄色装饰线在各端移除。焦点/悬停轮廓仍作为键盘与鼠标反馈。

生产构建含类型检查通过。浏览器实看1920×1080系统菜单，入口/弹层宽均245.9px、左边缘相同、选项22px、伪元素none；360×800菜单160px/14px。截图 `.verification/dock/desktop-menu.jpg`，不是线上账号操作录屏。

Web镜像 `energy-research-web:web-20261015-dock`，BUILD_ID `8yDvKZd36uWibrAIGi575`。仅前端轻量更新6,662,572字节，服务健康、真实HTTPS首页200且版本匹配；API仍compact、数据库0033不变。服务器旧环境备份在 `/srv/energy-research-web/releases/20261015-dock`。以CURRENT_STATUS最新记录为准，原手机视频与快照保留历史版本。
