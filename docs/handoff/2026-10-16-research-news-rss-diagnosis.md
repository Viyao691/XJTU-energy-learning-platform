# 科研日报 MIT RSS 失败诊断 · 2026-10-16

## 根因与线上证据

在现有 Web backend 容器内，使用项目 `app.state.paper_source_client_factory()`，以现有 `timeout=15, follow_redirects=True` 请求公开 RSS。只输出状态、耗时、字节、XML 条目数及安全格式分类，不输出正文、环境变量、请求/响应头、Cookie 或密钥。

| 来源 | HTTP | 字节 | XML item 数或异常 | 耗时（秒） |
|---|---:|---:|---|---:|
| MIT News 能源 | 200 | 3038 | ParseError | 2.838 |
| MIT News 人工智能 | 200 | 3038 | ParseError | 0.898 |
| EIA | 200 | 10701 | 17 | 0.794 |
| Clean Energy Wire | 200 | 110307 | 10 | 2.022 |
| ScienceDaily 能源 | 200 | 44434 | 60 | 1.192 |

随后对 MIT 能源源只做格式分类：`is_html=true`、`has_access_verification_markers=true`、`has_rss_root=false`，XML 错误位置为第1行第0列。MIT RSS 目录页及目录当前人工智能链接也各返回 HTTP200/3038字节/ParseError。故障在上游返回体到 RSS 解析之间：服务器收到网页/访问验证内容，并非有效 RSS；不是本轮观察中的 DNS、TLS、超时、HTTP403 或404。未识别具体防护产品，也不将站外搜索工具可读当作服务器可读证明。

[MIT 官方 RSS 目录](https://news.mit.edu/rss)仍列能源源；目录人工智能链接为 `https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml`。该官方链接在服务器同样未返回 RSS，因此没有盲目替换项目 URL。MIT 官方目录及限定 mit.edu 的检索未找到可证实的 FeedBurner 备用链接，未猜测地址、接入代理、模拟浏览器或绕过访问验证。

## 最小源码改动与边界

仅修改 `backend/app/services/research_news.py` 和对应测试：识别响应开头的 HTML 文档，抛出固定的安全格式错误；日报提示“来源返回网页或访问验证页，当前服务器暂时无法读取 RSS；其他来源仍可阅读，5分钟后重试”。保留失败来源原有缓存、现有去重和5分钟重试，不把 HTML 当作空 RSS 成功。有效 RSS 内嵌 HTML 摘要仍正常读取。

这只改善诊断和降级提示，不代表恢复了 MIT RSS。其他三源在本次服务器检查中可读；后续 MIT 恢复公开 RSS 后，现有重试即可再次获取。诊断阶段未部署；最终发布结果见同日 `2026-10-16-campus-news.md`。本次未激活校园来源、未启动校园资料抓取、未调用模型。

## 必要验证

最终发布后的公开日报 API 为 HTTP200，重新获取40条资讯，包含MIT能源、MIT人工智能、EIA、Clean Energy Wire、ScienceDaily五源，`warnings=[]`。说明上游读取在这次请求中已恢复；不把错误分类补丁解释为解除访问验证的原因，也不保证后续不会再次受到上游限制。先前HTML返回证据保留为本次故障时的观测。

Python 3.12.13，在 backend 目录运行：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_research_news.py -q --disable-warnings
```

先红：新增 HTTP200 HTML 测试发现旧实现没有抛出明确格式错误；随后验证有效 RSS 内 HTML 摘要不会被误判。最终 **11 passed**（8项既有、3项新增），警告为既有 `datetime.utcnow()` 弃用提示。全部网络单测使用 `httpx.MockTransport`；未运行全套检查。

## 校园公开 API 计数

同日只读请求正式 HTTPS 的公开 API，事件与来源接口均 HTTP200：

- 校园事件默认可见总数：0；`recent=0, unknown=0, archive=0`。
- 来源目录：67个；已启用来源：0个。

手机改为内容优先只能改善布局，不能凭空产生事件。当前线上没有已采集校园事件且没有已启用来源；本轮没有改变这些状态。
