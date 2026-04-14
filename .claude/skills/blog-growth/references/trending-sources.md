# 热搜追踪：渠道与判断标准

## 英文热点渠道（WebSearch）

| 渠道 | 搜索方式 | 发现什么 |
|------|---------|---------|
| Hacker News | `site:news.ycombinator.com AI coding {current_year}` | 技术社区最关心的话题 |
| Reddit | `site:reddit.com "AI coding" OR "Claude Code" {current_year}` | 开发者讨论热点 |
| TechCrunch/TheVerge | `site:techcrunch.com AI developer tools {current_year}` | 产品发布和融资新闻 |
| GitHub Trending | WebSearch `github trending AI agent {current_month}` | 新开源项目 |
| Product Hunt | WebSearch `producthunt.com AI coding agent` | 新产品发布 |
| Martin Fowler/ThoughtWorks | `site:martinfowler.com` 最新文章 | 工程方法论趋势 |

## 中文热点渠道（WebSearch）

| 渠道 | 搜索方式 | 发现什么 |
|------|---------|---------|
| 知乎热榜 | `site:zhihu.com AI 编程 {current_month}` | 国内开发者关注的话题 |
| 掘金/InfoQ | `site:juejin.cn AI 编程工具 {current_year}` | 国内技术社区热点 |
| 36氪/量子位 | `site:36kr.com AI 编程 {current_year}` | 国内 AI 产品新闻 |
| V2EX | `site:v2ex.com AI 编程 Claude` | 极客社区讨论 |
| 微信公众号 | WebSearch `微信公众号 AI 编程 最新` | 国内深度文章 |
| GitHub 中文社区 | WebSearch `github 中文 AI agent 新项目 {current_month}` | 国内开源动态 |

**使用原则**：从 GSC 数据中的高频主题词出发去上述渠道搜索，不要预设关键词。

## 真热点 vs 伪热点

| 信号 | 真热点 | 伪热点 |
|------|--------|--------|
| 多个渠道同时出现 | ✅ HN + Reddit + TechCrunch 都在讨论 | ❌ 只在一个小博客看到 |
| GSC 已有展示 | ✅ 搜索词展示量在上升 | ❌ 搜索量为零 |
| 时效性触发器 | ✅ 新版本发布、融资、开源、争议事件 | ❌ 概念讨论，无具体事件 |
| 与博客定位匹配 | ✅ AI/编程/工具/工程方法论 | ❌ 纯商业新闻/八卦 |
| 搜索结果竞争度 | ✅ 第一页还没有深度文章 | ❌ 大站已经覆盖得很好 |

## 热搜优先级评分

| 标准 | 权重 | 说明 |
|------|------|------|
| 与博客定位匹配度 | 高 | 必须是 AI/编程/工具相关 |
| 搜索量潜力 | 高 | GSC 已有展示，或多渠道讨论 |
| 中英文热度差 | 高 | 优先两边都火，或单侧热度极大 |
| 竞争程度 | 中 | Google 第一页是否已有深度文章 |
| 时效性 | 中 | 事件发生 1-3 天内发布最佳 |
| 与现有内容关联度 | 中 | 能形成内链、扩充集群更好 |
