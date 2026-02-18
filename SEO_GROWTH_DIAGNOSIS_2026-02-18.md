# heyuan110.com SEO 增长执行报告（只读分析版）

> 范围：`/Users/bruce.he/heyuan110.github.io`（未改动业务文件）  
> 目标：索引清理 + 高展示低点击改写 + AI/Linux 内容簇内链方案

## 0) 结论（先看这个）

- 当前核心瓶颈不是内容量，而是索引入口噪音（尤其 tags）过高。  
- 主站 sitemap 规模与 GSC「已发现-尚未编入索引」高度吻合，说明大量低价值聚合页占用了抓取预算。  
- 优先顺序：**索引降噪 > 高展示页 CTR 提升 > 主题簇内链重构**。

---

## 1) 索引清理清单（规则 + 示例 + 风险）

### P0（本周必须）

### 1.1 文章详情页保留索引
- 动作：保留 `index,follow` + 保留在 sitemap
- 示例：
  - `/posts/ai/2026-01-28-claude-code-browser-automation/`
  - `/posts/ai/2026-01-29-moltbot-deep-dive/`
  - `/posts/docker/2026-01-19-docker-compose-complete-guide/`
  - `/posts/linux/2020-06-29-curl/`
- 风险：不要直接 noindex 老文，先改写+内链，30/60 天再淘汰。

### 1.2 Tag 词条页整体降级
- 动作：`tags` 页统一 `noindex,follow`；并从 sitemap 移除 `tags/*`
- 示例：
  - `/tags/`
  - `/tags/claude-code/`
  - `/tags/ai-agent/`
  - `/tags/docker/`
- 风险：短期已索引数可能下降，属于健康收敛。

### 1.3 重复聚合页 canonical 统一
- 动作：重复聚合页 canonical 到主聚合页（或 noindex）
- 典型对：
  - `/docker-categories/` ↔ `/categories/docker/`
  - `/linux-categories/` ↔ `/categories/linux/`
  - `/go-categories/` ↔ `/categories/go/`
  - `/java-categories/` ↔ `/categories/java/`
- 风险：避免直接删页，优先 canonical 或 301。

### P1（下周）

### 1.4 web-toolbox 分层索引
- 保留索引（高意图）：
  - `/web-toolbox/social-video-downloader.html`
  - `/web-toolbox/pdf-merge.html`
  - `/web-toolbox/pdf-split.html`
  - `/web-toolbox/pdf-compress.html`
  - `/web-toolbox/ocr-tool.html`
  - `/web-toolbox/regex-tester.html`
  - `/web-toolbox/json-viewer.html`
- 建议 noindex（低意图/弱搜索）：
  - `/web-toolbox/angel-number.html`
  - `/web-toolbox/numerology.html`
  - `/web-toolbox/relative-calculator.html`
  - `/web-toolbox/metronome.html`
  - `/web-toolbox/paint-board.html`

### 1.5 非落地目录禁止抓取
- 目录示例：
  - `/web-toolbox/docs/`
  - `/web-toolbox/.playwright-cli/`
  - `/web-toolbox/.playwright-mcp/`
  - `/web-toolbox/.claude/`

### P2（持续）

### 1.6 薄内容老文二选一
- 有潜力：扩写升级继续索引
- 无潜力：noindex + 移出 sitemap

---

## 2) 10 个高展示低点击页面改写稿（可直接落地）

> 除第 3 条（静态 HTML）外，其他按 Hugo front matter（TOML）

### 1) `/posts/ai/2026-01-28-claude-code-browser-automation/`
```toml
title = "Claude Code 浏览器自动化怎么选？4 套方案实测对比（Agent Browser vs Playwright CLI/MCP vs DevTools）"
description = "2026 实测对比 Claude Code 四种浏览器自动化方案：速度、Token 成本、稳定性、适用场景一次讲清，附选型结论与落地命令。"
```

### 2) `/posts/ai/2026-01-29-moltbot-deep-dive/`
```toml
title = "Moltbot 深度解析（2026）：为什么爆火、为何改名、有哪些安全风险？"
description = "一文看懂 Moltbot（原 Clawdbot）的爆火逻辑、改名始末与真实安全风险，含架构拆解、骗局复盘与部署避坑建议。"
```

### 3) `/web-toolbox/social-video-downloader.html`
- `<title>`: `TikTok/X/Instagram Video Downloader (No Watermark, HD) | Free Online Tool`
- `<meta name="description">`: `Download public videos from TikTok, X (Twitter), Instagram Reels, Facebook and YouTube in HD. No app install, no login, one-click online downloader.`

### 4) `/posts/docker/2026-01-19-docker-compose-complete-guide/`
```toml
title = "Docker Compose 完全指南（2026）：安装、docker-compose.yml、实战部署一篇搞定"
description = "从 Docker 基础到 Docker Compose 实战：安装配置、compose.yml 核心字段、WordPress/Node+MySQL 案例与生产环境最佳实践。"
```

### 5) `/posts/docker/2026-01-24-docker-compose-yml-explained/`
```toml
title = "docker-compose.yml 详解（含 compose.yaml）：services、volumes、networks 实战模板"
description = "逐字段讲透 docker-compose.yml/compose.yaml：services、volumes、networks、depends_on、healthcheck，并附可直接复用的配置模板。"
```

### 6) `/posts/linux/2020-06-29-curl/`
```toml
title = "curl 命令大全（Linux/macOS）：GET/POST、文件上传下载、鉴权与调试实战"
description = "最常用 curl 命令一文速查：GET/POST/PUT/DELETE、JSON 请求、上传下载、代理、证书、耗时分析与故障排查示例。"
```

### 7) `/posts/linux/2020-06-28-traceroute/`
```toml
title = "traceroute 命令详解：网络延迟定位与路由故障排查（Linux/macOS/Windows）"
description = "从 TTL 原理到输出解读，系统讲解 traceroute 在 Linux/macOS/Windows 的用法差异，快速定位网络慢点与故障节点。"
```

### 8) `/posts/docker/2019-11-14-docker-commands/`
```toml
title = "Docker 常用命令速查（2026更新）：镜像、容器、网络、数据卷一页掌握"
description = "高频 Docker 命令速查：pull/run/exec/logs、镜像清理、网络管理、数据卷挂载，附 MySQL/Nginx/Redis 常用启动示例。"
```

### 9) `/posts/linux/2020-07-04-aws-cli/`
```toml
title = "AWS CLI 完全指南：安装配置、S3/EC2 常用命令与权限排错"
description = "AWS CLI 从零上手：安装、aws configure、S3/EC2/IAM 高频命令、常见报错与权限问题排查，适合运维与开发日常使用。"
```

### 10) `/posts/ai/2026-02-12-codex-cli-mastery-guide/`
```toml
title = "Codex CLI 实战指南：20+ 高效技巧（模型切换、会话恢复、MCP 集成）"
description = "面向开发者的 Codex CLI 进阶教程：别名配置、模型选择、会话恢复、授权模式、MCP 集成与 AGENTS.md 工作流实战。"
```

---

## 3) AI + Linux 内容簇内链图

### Cluster A：AI 自动化
- Hub（建议新建）：`/posts/ai/ai-automation-hub/`
- Pillar：
  - `/posts/ai/2025-01-14-claude-code-guide/`
  - `/posts/ai/2026-01-28-claude-code-browser-automation/`
  - `/posts/ai/2026-02-12-openclaw-usage-tutorial/`
  - `/posts/ai/2026-01-29-moltbot-deep-dive/`
  - `/posts/ai/2026-02-12-codex-cli-mastery-guide/`
- Satellite（示例）：
  - `/posts/ai/2025-01-23-claude-code-commands/`
  - `/posts/ai/2026-01-08-claudecode-skill-guide/`
  - `/posts/ai/2026-01-12-claudemd-memory-guide/`
  - `/posts/ai/2026-02-18-claude-code-hooks-guide/`
  - `/posts/ai/2026-01-31-openclaw-memory-strategy/`
  - `/posts/ai/2026-02-14-openclaw-automation-pitfalls/`
  - `/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/`
- 链接规则：Satellite -> Hub + 对应 Pillar；Pillar 之间互链。

### Cluster B：Linux 运维基础
- Hub（建议新建）：`/posts/linux/linux-ops-basics-hub/`
- Pillar：
  - `/posts/linux/2020-03-19-linux-mac-commands/`
  - `/posts/linux/2020-06-29-curl/`
  - `/posts/linux/2020-06-28-traceroute/`
  - `/posts/docker/2026-01-19-docker-compose-complete-guide/`
  - `/posts/linux/2020-07-04-aws-cli/`
- Satellite：
  - `/posts/linux/2015-06-17-shell-zsh/`
  - `/posts/linux/2019-05-13-linux-shell-vars/`
  - `/posts/linux/2018-10-06-ip-cidr/`
  - `/posts/docker/2019-11-14-docker-commands/`
  - `/posts/docker/2026-01-24-docker-compose-yml-explained/`
- 链接规则：卫星文回链 Hub；`curl`/`traceroute`/`linux-mac-commands` 三角互链。

---

## 4) 7 天落地顺序

- Day1：确定索引白名单/黑名单（posts 保留；tags 降级）
- Day2：模板层 robots + sitemap 规则改造
- Day3：上线 10 条 title/description（先上前 5 条）
- Day4：重复聚合 canonical/301 统一
- Day5：上线 AI Hub + Linux Hub（先简版）
- Day6：web-toolbox 分层索引 + sitemap 校准
- Day7：GSC 重新提交 sitemap，记录 14 天复盘基线

---

## 5) 动作归类

### 只改文案即可
- 标题/描述改写
- 首段重写（问题导向）
- 文末相关阅读内链块

### 需模板/构建层调整
- tags/taxonomy noindex 规则
- sitemap 输出范围收敛
- 重复聚合 canonical/301
- web-toolbox 非落地目录抓取限制
