---
name: blog-growth
description: Use when user says "今天写什么", "博客诊断", "blog growth", "运营博客", or any daily blog operations request. Triggers data-driven content creation workflow combining Search Console + Google Analytics analysis, trending topic research, and parallel article production.
---

# Daily Blog Growth Engine

## Overview

数据驱动的博客增长工作流。通过 GSC + GA 双数据源诊断 → 中英文差异化选题 → 并行产出 → 分发外链，形成完整的增长闭环。

**核心原则**：
1. 不靠猜，靠数据——每个决策都有 GSC/GA 数据支撑
2. 中英文是两个市场——选题、角度、关键词独立决策
3. CTR 修复优先于写新文章——优化老文章的 ROI 通常更高
4. 每篇文章都写中英文——但角度可以不同

## When to Use

- 用户说"今天写什么文章"、"博客诊断"、"运营博客"、"blog growth"
- 每日/每周定期博客运营
- 需要数据驱动的选题建议
- 需要流量诊断和优化建议

**When NOT to use**: 用户已有明确选题只需写作时，用 `blog-writer` skill。

## Workflow

```
诊断(GSC+GA) → 对比(环比) → 差异化选题(中/英) → 优化决策 → 并行生产 → 发布 → 分发
```

---

## Phase 1: 双数据源诊断 (GSC + GA)

### 1.1 GSC 数据（搜索表现）

通过 RUBE MCP 连接 Google Search Console，并行拉取 4 组数据：

**连接配置**：
```
site_url: "sc-domain:heyuan110.com"
data_state: "final"
```

| 查询 | 维度 | 时间范围 | row_limit | 用途 |
|------|------|---------|-----------|------|
| 搜索词表现 | `["query"]` | 近 30 天 | 25000 | 找关键词机会 |
| 页面表现 | `["page"]` | 近 30 天 | 5000 | 找优化目标 |
| 每日趋势 | `["date"]` | 近 30 天 | 50 | 看流量走势 |
| 上期页面（环比用） | `["page"]` | 60-30 天前 | 5000 | 周环比分析 |

### 1.2 GA 数据（用户行为）

通过 RUBE MCP 连接 Google Analytics，并行拉取 5 组数据：

**连接配置**：
```
property: "properties/519433466"
```

| 报告 | 维度 | 指标 | 用途 |
|------|------|------|------|
| 整体概况 | 无（双日期范围） | activeUsers, sessions, screenPageViews, engagementRate, averageSessionDuration | 总量趋势 |
| Top 页面 | pagePath | screenPageViews, activeUsers, engagementRate, averageSessionDuration | 找热门和隐藏宝石 |
| 流量来源 | sessionDefaultChannelGroup | sessions, activeUsers, engagementRate | 渠道健康度 |
| 每日趋势 | date | activeUsers, sessions, screenPageViews | 日度走势 |
| 设备分布 | deviceCategory | sessions, activeUsers, engagementRate | 移动端优先级判断 |

### 1.3 数据处理（在 RUBE_REMOTE_BASH_TOOL 中执行）

数据量大时用远程沙箱处理，提取以下关键指标：

**GSC 关键指标**：
- Top 15 页面（按 clicks 排序）
- 高展示低 CTR 页面（impressions > 200, CTR < 2%）
- 零点击高展示关键词（clicks = 0, impressions > 100）
- 周环比变化（上升/下降最多的页面）

**GA 关键指标**：
- 整体环比（用户、PV、互动率、时长）
- Top 20 页面（按 PV 排序，含互动率和时长）
- 隐藏宝石（互动率 > 45%, 时长 > 200s, 但 GSC 点击 < 50）
- 中文 vs 英文页面对比（PV、用户数、互动率）

**交叉分析**：
- GSC 高展示 + GA 低互动 → 内容质量需优化
- GA 高互动 + GSC 低搜索流量 → SEO 需优化（标题/描述/FAQ）
- 中文 CTR vs 英文 CTR → 判断哪个市场 ROI 更高

### 1.4 历史对比

检查是否存在历史报告：
```bash
ls plans/reports/ 2>/dev/null
```
如果有上期报告，对比核心指标变化趋势，评估上次优化的效果。

---

## Phase 2: 中英文差异化选题

### 2.1 分离中英文搜索需求

将 GSC 关键词按语言分类（中文含汉字，其余为英文），分别聚类分析：

**中文热搜集群**（按展示量排序）：
- OpenClaw 相关
- Claude Code 相关
- 定价/限制 相关
- MCP/Skill 相关
- AI 工具对比

**英文热搜集群**（按展示量排序）：
- Claude pricing/limits
- Harness engineering
- AI tool comparisons
- Framework reviews
- Setup guides

### 2.2 选题决策矩阵

| 选题来源 | 说明 | 优先级 |
|---------|------|--------|
| **CTR 修复型** | 高展示低 CTR 的老文章 → 优化 title/description/FAQ | 最高（不写新文章就能涨） |
| **数据缺口型** | 高展示零点击的搜索词 → 写精准匹配新文章 | 高 |
| **隐藏宝石型** | GA 高互动但 GSC 低流量 → SEO 优化现有好内容 | 高 |
| **趋势追热型** | 热搜话题 + 博客有相关基础 → 快速产出 | 中（注意中英文热点差异） |
| **系列深耕型** | 已有主题集群 → 继续扩充建立权威 | 中 |
| **内链补缺型** | 缺少 Related Reading 的文章 → 批量补内链 | 高（零成本排名提升） |

### 2.3 中英文角度差异化

每篇文章都写中英文，但角度不同：

| 维度 | 中文版 | 英文版 |
|------|--------|--------|
| 风格 | 实操教程、手把手、接地气 | 原理分析、架构设计、国际视角 |
| 关键词 | 中文搜索词 | 英文搜索词（完全独立） |
| 举例 | 飞书、国产工具、国内生态 | GitHub, global tools, international context |
| 类比 | 中文读者熟悉的比喻 | 英文读者熟悉的比喻 |

### 2.4 选题输出格式

向用户展示 3-5 个选题建议：

```markdown
### 建议 1: [文章标题]
- **来源**: CTR修复 / 数据缺口 / 隐藏宝石 / 热搜追踪 / 系列深耕
- **中文热度**: GSC 展示 XX，GA 互动率 XX%
- **英文热度**: GSC 展示 XX，GA 互动率 XX%
- **中文角度**: xxx
- **英文角度**: xxx
- **预期效果**: 从现有 XX 展示中多获取 XX 点击
- **难度**: 低/中/高
- **类型**: 新文章 / 老文章优化 / 内链补充
```

---

## Phase 3: 热搜追踪

### 3.1 分别追踪中英文热点

**英文热搜**（WebSearch）：
- `"Claude Code" OR "AI coding agent" 2026 trending`
- `"harness engineering" OR "AI agent framework" 2026`
- `site:news.ycombinator.com AI coding 2026`

**中文热搜**（WebSearch）：
- `"AI 编程" OR "Claude Code" 最新 2026`
- `"OpenClaw" OR "小龙虾" 新功能 2026`
- `AI 编程工具 国内 2026`

### 3.2 热搜评估

| 标准 | 权重 | 说明 |
|------|------|------|
| 与博客定位匹配度 | 高 | 必须是 AI/编程/工具相关 |
| 搜索量潜力 | 高 | 有明确搜索需求 |
| **中英文热度差** | 高 | 优先选两边都火的，或单侧热度极大的 |
| 竞争程度 | 中 | 避开大站已占据的词 |
| 时效性 | 中 | 新工具/新版本抢先发 |
| 与现有内容关联度 | 中 | 能形成内链、扩充主题集群更好 |

---

## Phase 4: 优化执行（不写新文章的高 ROI 动作）

在写新文章之前，先检查是否有更高 ROI 的优化动作：

### 4.1 批量补 FAQ 结构化数据

检查高展示页面是否有 `[[params.faqItems]]`：
```bash
for dir in /path/to/content/posts/ai/*/; do
  has_faq=$(grep -c 'params.faqItems' "${dir}index.md" 2>/dev/null || echo 0)
  # 报告缺少 FAQ 的高展示页面
done
```

每篇补 3-5 个 FAQ，预期 CTR 提升 50-200%。

### 4.2 批量内链优化

检查文章是否有 Related Reading：
```bash
grep -rL "Related Reading" content/posts/ai/*/index.md | wc -l
```

缺少内链的文章补 4-6 个相关链接。按集群组织：
- Claude Code 集群互链
- OpenClaw 集群互链
- AI 工具对比集群互链
- 跨集群桥接链接

### 4.3 老文章 SEO 优化

针对高展示低 CTR 的老文章：
- 优化 title（关键词前置，50-60 字符，含年份和数字）
- 优化 description（120-160 字符，直接回答搜索问题）
- 扩充 keywords（加入 GSC 中实际有展示的搜索词）
- 补充 FAQ 结构化数据
- 不修改原始 date 字段

---

## Phase 5: 并行生产

### 5.1 写作规则

**⚠️ 必须使用 blog-writer skill 写文章**。调用 `/blog-writer` 或在 Agent prompt 中包含 blog-writer 的完整规范。

**每篇文章都写中英文**：
- `index.md` — 英文版（必须）
- `index.zh.md` — 中文版（必须）
- 两个版本角度可以不同（见 Phase 2.3）
- 中文版必须是原创级质量，不是翻译

### 5.2 Agent 分派

使用 Agent tool 并行启动多个 agent：

```
Agent 1: 新文章写作（调用 blog-writer skill）
Agent 2: 新文章写作（同上）
Agent 3: 老文章批量优化（FAQ + 内链 + SEO）
```

### 5.3 新文章 Agent 指令要点

- 目标关键词和搜索数据（来自 Phase 1-3）
- 中文角度 vs 英文角度（来自 Phase 2.3）
- 必须遵循 AGENTS.md 中的所有规则
- 文章目录路径 `content/posts/ai/YYYY-MM-DD-slug/`
- 新文章默认不添加 categories
- 4+ 内链到已有相关文章
- 3-5 个 FAQ 结构化数据

---

## Phase 6: 发布 + 分发

### 6.1 发布流程

```bash
# 1. 验证构建
hugo --minify

# 2. 逐个 stage（不用 git add -A）
git add content/posts/ai/新文章/

# 3. 中文 commit message
git commit -m "描述"

# 4. Push 到 code 分支（自动触发部署）
git push origin code
```

### 6.2 分发外链

发布后调用 `blog-distributor` skill（或 `/distribute`）：
- 英文文章 → dev.to 草稿（自动，canonical_url 指回原文）
- 中文文章 → 生成掘金/V2EX 格式（手动粘贴）
- 深度文章 → HN 投稿建议

### 6.3 保存报告

将本次诊断数据保存到 `plans/reports/YYYY-MM-DD-report.md`（私有仓库 blog-ops），便于下次对比。

---

## Quick Reference

### Search Console 关键阈值

| 场景 | 阈值 | 动作 |
|------|------|------|
| 高展示低点击 | impressions > 200, CTR < 2% | 优化 title/description + 补 FAQ |
| 零点击高展示 | clicks = 0, impressions > 100 | 写精准匹配新文章 |
| 高展示低排名 | impressions > 200, position > 15 | 优化内容深度 + 内链 |
| 排名上升中 | position 改善 > 3 位 | 继续深耕该主题 |
| 新文章冷启动 | 发布 > 7 天, impressions < 10 | 检查标题/关键词 |

### GA 关键阈值

| 场景 | 阈值 | 动作 |
|------|------|------|
| 隐藏宝石 | 互动率 > 45%, GSC 点击 < 50 | SEO 优化（标题/描述/FAQ） |
| 内容质量问题 | PV > 500, 互动率 < 25% | 改善内容匹配度 |
| 中文版缺失 | 英文版 PV > 500, 无 index.zh.md | 补中文版 |

### 内容矩阵策略

围绕高流量主题持续产出，形成搜索权威（每个集群 10+ 篇）：
- **Claude Code 集群**：指南 → 定价 → Hooks → Worktree → Teams → 安全 → 对比
- **OpenClaw 集群**：入门 → 多Agent → 自动化 → 记忆 → Tavily → 架构
- **Harness Engineering 系列**：总览 → CLAUDE.md → Sub-Agent → 架构约束
- **AI 工具对比**：vs Copilot → vs Codex → vs Cursor → 三方对比 → 年度横评

### 中英文差异化速查

| 中文热点（国内关注） | 英文热点（国际关注） |
|-------------------|-------------------|
| OpenClaw 多Agent 配置 | Claude pricing/limits |
| MCP vs Skill 区别 | Harness engineering |
| 国产 AI 工具评测 | Claw Code / open source |
| Claude Code 入门教程 | AI tool comparisons |
| 飞书/企微集成 | MCP server development |

---

## Common Mistakes

| 错误 | 正确做法 |
|------|---------|
| 只看 GSC 不看 GA | GSC 看搜索机会，GA 看内容质量，必须交叉分析 |
| 中英文写一样的内容 | 角度和关键词要差异化，中文偏实操，英文偏原理 |
| 只写新文章不优化老文章 | 优化老文章（FAQ + 内链 + SEO）ROI 通常更高 |
| 追热点但不匹配博客定位 | 热点必须与 AI/编程/工具相关 |
| 写完不分发 | 发布后用 `/distribute` 同步到 dev.to + 掘金 |
| 不保存诊断报告 | 每次诊断保存到 plans/reports/，下次对比趋势 |
| 新文章不做内链 | 每篇新文章至少 4-6 个内链 |
| 不用 blog-writer skill | 写文章必须用 `/blog-writer`，确保格式和质量一致 |
| 忽略 FAQ 结构化数据 | 每篇文章都应有 3-5 个 `[[params.faqItems]]` |
