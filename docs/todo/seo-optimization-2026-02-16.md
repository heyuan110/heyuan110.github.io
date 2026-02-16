# SEO 优化待办清单

> 基于 2026-02-16 Google Search Console 数据分析生成
> 过去 28 天数据，站点刚起步阶段

## 当前流量数据

| 排名 | 文章 | 点击数 | 趋势 | 搜索排名 |
|------|------|--------|------|---------|
| 1 | Claude Code 浏览器自动化方案对比 | 115 | 从 0 起步 | **中文搜索第 1** |
| 2 | Moltbot 深度解析 | 24 | 从 0 起步 | - |
| 3 | Social Video Downloader（工具页） | 14 | 从 0 起步 | - |
| 4 | Claude Cowork | 10 | 从 0 起步 | - |
| 5 | Handheld Danmaku（工具页） | 9 | 从 0 起步 | - |
| 6 | 首页 | 5 | 持平 | - |
| 7 | curl 命令完全指南 | 4 | +100% | - |
| 8 | Web Toolbox 首页 | 4 | 从 0 起步 | - |

## 已完成

- [x] 修复 Claude Cowork 文章 SEO：YAML→TOML、添加 keywords、分类 AI工具→AI实战、tags 更具体
- [x] 8 篇文章补充「相关阅读」内链（claudecode-best-practices, claudecode-skill-guide, claude-code-commands, claudecode-skill-patterns, openclaw-claude-code-workflow, ai-dev-workflow, agent-skills-new-programming, claude-cowork）
- [x] 高流量文章入链数提升：浏览器自动化 4→9，Moltbot 2→5
- [x] 修复隐私页面 BreadcrumbList 结构化数据（name 缺失 + 双斜杠 URL）

---

## 短期待办（1-2 周内）

### P0：更新 Moltbot 文章适配 OpenClaw 新名

- **文件**：`content/posts/ai/2026-01-29-moltbot-deep-dive/index.md`
- **原因**：Moltbot 已改名为 OpenClaw，但文章标题和内容仍以 Moltbot 为主，漏掉了 "OpenClaw" 搜索流量
- **操作**：
  - [ ] title 中追加 OpenClaw 关键词，如「Moltbot/OpenClaw 深度解析：从爆火到改名…」
  - [ ] tags 中添加 `OpenClaw`
  - [ ] keywords 中添加 `OpenClaw`
  - [ ] 正文开头补充一段 "注：Moltbot 已更名为 OpenClaw" 的说明
  - [ ] description 中加入 OpenClaw

### P0：浏览器自动化文章补充 Playwright CLI 新方案

- **文件**：`content/posts/ai/2026-01-28-claude-code-browser-automation/index.md`
- **原因**：竞品分析发现 Playwright CLI 是新方案（号称 Token 消耗降低 4 倍），你的文章目前未覆盖，可能被竞品超越
- **操作**：
  - [x] 研究 Playwright CLI（参考 https://testcollab.com/blog/playwright-cli）
  - [x] 在文章中新增一个章节介绍这个方案
  - [x] 更新对比表格，加入第四个方案
  - [x] 更新 description 和 keywords
  - [x] 标题添加「2026 最新」提升时效性搜索匹配
  - [x] 更新实战选型指南、FAQ、总结推荐

### P1：检查其余文章的 Front Matter 规范性

- **原因**：Claude Cowork 文章暴露了早期文章的 SEO 缺陷（YAML 格式、缺 keywords、分类非标）
- **操作**：
  - [ ] 批量扫描所有 AI 文章，找出使用 YAML（`---`）而非 TOML（`+++`）的文章
  - [ ] 找出缺少 `keywords` 字段的文章
  - [ ] 找出分类不在标准列表（AI原理/AI实战）中的文章
  - [ ] 逐一修复

---

## 中期待办（持续进行）

### 新文章选题（按优先级）

| 优先级 | 选题 | 理由 |
|--------|------|------|
| **P0** | 「Claude Code vs Cursor vs Windsurf 2026 对比」 | 「对比类」是验证过的高流量内容类型，开发者工具对比搜索量大 |
| **P1** | 「Claude Code 最佳插件/MCP 推荐 2026」 | Claude Code 热度极高（ARR 10 亿美元），插件推荐类内容搜索量大 |
| **P1** | 「MCP 协议入门指南：AI Agent 工具集成标准」 | MCP 是 2026 年 Agent 工具集成事实标准，中文深度内容少 |
| **P2** | 「2026 AI Agent 框架盘点：AutoGen vs LangChain vs CrewAI」 | 盘点类文章搜索量大，适合获取长尾流量 |

### 内容策略

- [ ] **多写「对比类」和「排行榜」内容**——浏览器自动化对比 115 clicks 证明这个类型有效
- [ ] **标题加年份**——如 "2026 最新"、"2026 完全指南"，提升时效性搜索匹配
- [ ] **紧跟热点更新已有文章**——OpenClaw 创始人加入 OpenAI 等事件是更新文章的好时机
- [ ] **每篇新文章必须有 3+ 内链**——指向已有的高流量文章，形成主题集群

### 内链策略

- [ ] 每篇新文章的「相关阅读」必须包含至少 1 篇高流量文章
- [ ] 定期检查高流量文章的入链数，确保核心文章有足够的内链支撑
- [ ] 目标：每篇核心文章被 10+ 篇其他文章引用

---

## 竞品监控

| 竞品 | 关注点 |
|------|--------|
| [53AI](https://www.53ai.com/) | 可能转载/改编你的内容，监控排名变化 |
| [菜鸟教程 OpenClaw](https://www.runoob.com/ai-agent/openclaw-clawdbot-tutorial.html) | 权威流量大，你需要更深度的差异化内容 |
| [知乎 AI Agent 专栏](https://www.zhihu.com/) | 中文 AI 内容主要聚集地 |
| [Simon Willison's TILs](https://til.simonwillison.net/) | 英文 Claude Code 内容标杆 |

---

## 关键指标目标

| 指标 | 当前 | 1 个月目标 | 3 个月目标 |
|------|------|-----------|-----------|
| 日均点击数 | ~7 | 15+ | 50+ |
| 有流量的页面数 | 8 | 15+ | 30+ |
| 单篇最高点击 | 115 | 200+ | 500+ |
| 中文搜索排名第 1 的文章 | 1 篇 | 3+ 篇 | 5+ 篇 |
