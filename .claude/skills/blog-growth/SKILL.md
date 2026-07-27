---
name: blog-growth
description: "博客增长引擎。用户说「今天写什么」「博客诊断」「运营博客」「blog growth」时触发。通过 GSC + GA 双数据源诊断、中英文差异化选题、热搜追踪、并行产出和分发外链，形成完整的数据驱动增长闭环。"
---

# 博客增长引擎

## 概述

数据驱动的博客增长工作流。通过 GSC + GA 双数据源诊断 → 中英文差异化选题 → 并行产出 → 分发外链，形成完整的增长闭环。

**核心原则**：
1. 不靠猜，靠数据——每个决策都有 GSC/GA 数据支撑
2. **剖析先行**——任何选题建议之前，必须先按 1.5 契约把带数字的剖析结论展示给用户（两种模式都不可跳过）
3. 中英文是两个市场——选题、角度、关键词独立决策
4. CTR 修复优先于写新文章——优化老文章的 ROI 通常更高
5. 每篇文章都写中英文——但角度可以不同

## 使用场景

- 用户说"今天写什么文章"、"博客诊断"、"运营博客"、"blog growth"
- 每日/每周定期博客运营
- 需要数据驱动的选题建议
- 需要流量诊断和优化建议

**不适用场景**：用户已有明确选题只需写作时，用 `blog-writer` skill。

## 两种运行模式 ⭐

**数据剖析是两种模式的必经第一站（2026-07-27 用户定调）**：任何模式都必须先完成第一步的双数据源剖析、并按「1.5 剖析输出契约」把结论展示给用户，然后才能出选题。区别只在数据新鲜度和附加环节：

| 用户意图 | 模式 | 数据来源 | 附加环节 | 执行步骤 | 预期耗时 |
|---------|------|---------|---------|---------|---------|
| "今天写什么"、"有什么选题"、单个选题可行性评估 | **Quick** | 当天已拉的 `latest-metrics.json`（<24h 可复用）；否则跑本地脚本刷新（~30 秒） | 跳过第三步热搜 | 1 → 2 → **Checkpoint** → 5-6 | 5-8 分钟 |
| "博客诊断"、"运营博客"、"周度回顾"、"完整分析" | **Full** | 强制跑本地脚本刷新 | 热搜追踪 + 历史报告环比 | 1 → 2 → 3 → 4 → **Checkpoint** → 5 → 6 | 15-30 分钟 |

**判断规则**：
- 用户没明说 → 默认 Quick（仍然要做剖析，只是数据可复用当天缓存）
- 明确说"诊断""完整""详细分析"→ Full
- 要求"评估某一个选题"→ Quick，剖析可聚焦该选题相关查询，但大盘表仍要给

## 工作流

```
         ┌─ Quick: 1(可复用当天数据) → 2 → Checkpoint → 5-6  (5-8 分钟)
入口 ──┤
         └─ Full:  1(强制刷新) → 2 → 3 → 4 → Checkpoint → 5 → 6  (15-30 分钟)
```

**关键原则**：任何模式都必须在第 5 步「并行生产」前停下等用户确认选题。不要自动 spawn 写文章 agent。

---

## 第零步：加载本地资源（必选，Quick 和 Full 都跑）

**在调用任何外部 API 之前，先把本地已知信息装进上下文**。这省时、省 token，且是 API 失败时的降级数据源。

| 资源 | 路径 | 读取时机 | 用途 |
|------|------|---------|------|
| MEMORY | `~/.claude/projects/*/memory/MEMORY.md` | 总是（系统自动注入） | 已知 GSC 基准、重点待修文章、CTR 基准值 |
| 选题计划 | `content-plan.md`（项目根）| 总是 | 未写文章清单（如 104 篇计划、N1-N6 优先级） |
| 诊断报告 | `plans/reports/YYYY-MM-DD-*.md` | 总是 | 上期数据与已知结论，用于环比和避免重复劳动 |
| 现有文章 | `content/posts/ai/*/index.md` | 按需 | 老文章优化目标、内链候选 |

**读取顺序**：MEMORY（已注入） → `Glob plans/reports/*.md` 取最近一份 → `Read content-plan.md`。

### 降级路径（API 不可用时）

| 问题 | 降级 |
|------|------|
| GSC 返回空 / 鉴权失败 | 只用 MEMORY 已知基准 + content-plan 出选题；明确标注「基于 MEMORY 快照，非实时」 |
| GA 不可用 | 只跑 GSC 分析，互动率维度跳过；在报告中标注 |
| 无历史报告 | 跳过环比，只做当期快照 |
| MEMORY 数据陈旧（>14 天） | 强制调 GSC 刷新，之后把新数据写回 MEMORY |
| 聚类后某语言关键词 < 10 个 | 不做聚类，直接列 Top 5 单词 |

### 数据新鲜度规则

MEMORY 和历史报告是**背景知识**（已知幽灵曝光、CTR 基准），不能替代当次剖析。数据本体的取用顺序：
1. `plans/reports/latest-metrics.json` 存在且 <24h → 直接复用（本地脚本产物，含 GSC+GA4 全量）
2. 否则跑本地脚本刷新（见 1.0，~30 秒，成本极低，不要为省这一步而用陈旧数据）

---

## 第一步：双数据源剖析（GSC + GA，两种模式都必跑）

### 1.0 数据获取首选路径：本地脚本（不是 MCP）

**首选**个人服务账号 headless 拉数（稳定、~30 秒、可定时，详见 MEMORY `gsc-ga-api-access`）：

```bash
unset GOOGLE_APPLICATION_CREDENTIALS   # 用户 shell 的 GAC 指向公司 key，必须排除
SA_KEY=~/.config/blog-metrics/sa.json python3 scripts/fetch-blog-metrics.py --days 28
# 输出 plans/reports/latest-metrics.json：
#   gsc.queries / gsc.pages_current / gsc.pages_prior / gsc.dates
#   ga4.overview_current / overview_prior / top_pages / channels / daily / devices
```

MCP（1.1/1.2）只作为脚本失败时的备选路径。

### 1.1 GSC 数据（备选路径：MCP）

通过 **GSC MCP** 连接 Google Search Console，并行拉取 4 组数据。

**MCP 来源**（2026-04-23 起 RUBE 将于 5/15 停服，已迁移到独立开源 MCP）：
- 推荐：`mcp-search-console` / `mcp-gsc`（[AminForou/mcp-gsc](https://github.com/AminForou/mcp-gsc)）
- 过渡期（~5/15 前）：RUBE MCP 仍可用

**工具名约定**（运行时根据当前 MCP 配置动态解析，下方是语义签名）：
- `list_properties` — 获取站点列表
- `get_search_analytics` — 核心查询（对应 RUBE 的 `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`）

**连接配置**：
```
# site_url 不要写死，运行时通过 list_properties 动态获取
# 从返回的 siteEntry 中选择 sc-domain 类型的站点
data_state: "final"
```

| 查询 | 维度 | 时间范围 | row_limit | 用途 |
|------|------|---------|-----------|------|
| 搜索词表现 | `["query"]` | 近 30 天 | 25000 | 找关键词机会 |
| 页面表现 | `["page"]` | 近 30 天 | 5000 | 找优化目标 |
| 每日趋势 | `["date"]` | 近 30 天 | 50 | 看流量走势 |
| 上期页面（环比用） | `["page"]` | 60-30 天前 | 5000 | 周环比分析 |

### 1.2 GA 数据（备选路径：MCP）

通过 **GA4 MCP** 连接 Google Analytics，并行拉取 5 组数据。

**MCP 来源**（2026-04-23 迁移说明）：
- 推荐：`ga4-mcp-server`（[surendranb/google-analytics-mcp](https://github.com/surendranb/google-analytics-mcp)）
- 过渡期（~5/15 前）：RUBE MCP 仍可用

**工具名约定**：
- `search_schema` / `list_dimension_categories` — Schema 发现
- `get_ga4_data` — 核心报告（对应 RUBE 的 `GOOGLE_ANALYTICS_RUN_REPORT`）

**连接配置**：
```
# property ID 不要写死在 skill 里，运行时通过 API 动态获取：
# 方案 A (ga4-mcp-server): 通过环境变量 GA4_PROPERTY_ID 预配置
# 方案 B (RUBE 过渡期): GOOGLE_ANALYTICS_LIST_ACCOUNTS_V1_BETA → GOOGLE_ANALYTICS_LIST_PROPERTIES_FILTERED
```

| 报告 | 维度 | 指标 | 用途 |
|------|------|------|------|
| 整体概况 | 无（双日期范围） | activeUsers, sessions, screenPageViews, engagementRate, averageSessionDuration | 总量趋势 |
| Top 页面 | pagePath | screenPageViews, activeUsers, engagementRate, averageSessionDuration | 找热门和隐藏宝石 |
| 流量来源 | sessionDefaultChannelGroup | sessions, activeUsers, engagementRate | 渠道健康度 |
| 每日趋势 | date | activeUsers, sessions, screenPageViews | 日度走势 |
| 设备分布 | deviceCategory | sessions, activeUsers, engagementRate | 移动端优先级判断 |

### 1.3 数据处理（本地 Bash + python3 执行）

数据量大时用本地 `python3 << 'PYEOF'` 脚本处理（RUBE 过渡期也可用其远程沙箱），提取以下关键指标：

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

检查是否存在历史诊断报告（保存在项目本地的诊断报告目录中）。
如果有上期报告，对比核心指标变化趋势，评估上次优化的效果。

### 1.5 剖析输出契约（必须展示给用户，选题建议之前）⭐

剖析结果必须**先于选题建议**、按以下结构完整展示。每条结论都是**带数字的判断句**——「中文页点击 -300，跌幅集中在订阅政策类」合格；「中文流量有所下降」不合格。

依次输出五个板块：

1. **大盘表**：指标（GSC 点击/展示/CTR、GA4 用户）× 本期 × 环比 × **一句话判读**。判读列必须套用已知修正系数：展示暴跌先查是否幽灵曝光退潮（零点击成本，不是坏事）；CTR 翻倍先查是否分母坍塌（不算成绩）；GA4 绝对值先按 hostName 过滤并警惕 Direct 渠道机器人（互动率 <20% 即可疑）——这三条见 MEMORY `ghost-impressions-decay` / `ga4-bot-traffic`。
2. **结构发现（3-5 条）**：本次数据里最值钱的判断，每条 = 现象 + 数字 + 对行动的含义（如「下跌全在中文页(-300)，英文页 +12 → 别救退潮集群，投英文冷库」）。中英文市场必须分开看（点击/展示/CTR 三指标各自环比）。
3. **高展示低 CTR 清单**：impr>1500 且 CTR<1% 的页面，按展示降序，**排除 MEMORY 已判定的幽灵页**（hermes/pricing 类）并注明排除了什么。
4. **数据缺口词**：impr≥100、clicks≤2、pos≤20 的搜索词，过滤幽灵词根后按展示降序，标注语言（🀄/EN）；「有词无文」的要点名说出来——这是新文金矿。
5. **隐藏宝石**：GA 互动率>45% 且时长>200s 但 GSC 点击<50 的页面——内容已被读者验证、纯搜索问题，SEO 优化即可收割。

之后才进入第二步选题，且每个选题建议必须能指回上面某个板块的具体数字。

---

## 第二步：中英文差异化选题

### 2.1 分离中英文搜索需求

将 GSC 关键词按语言分类（中文含汉字，其余为英文），然后**动态聚类**。

聚类算法详见 [references/clustering-algorithm.md](references/clustering-algorithm.md)。核心原则：**不要预设固定集群**，每次运行都从数据中动态发现当前的热点集群。

输出格式：
```
中文搜索 Top 5 集群（按展示量）：
1. [集群名] — XX 个关键词，总展示 XX
2. ...

英文搜索 Top 5 集群（按展示量）：
1. [集群名] — XX 个关键词，总展示 XX
2. ...
```

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
| 关键词 | 中文搜索词（从 GSC 中文聚类提取） | 英文搜索词（从 GSC 英文聚类提取） |
| 举例 | 国内读者熟悉的产品和场景 | 国际读者熟悉的产品和场景 |
| 类比 | 中文语境下自然的比喻 | 英文语境下自然的比喻 |

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

## 第三步：热搜追踪（Full 模式）

从 GSC 高频主题词出发，去外部渠道搜索最新动态，判断是真热点还是伪热点。

**渠道、真伪判断、优先级权重详见 [references/trending-sources.md](references/trending-sources.md)**。

核心原则：
- 中英文渠道完全不同，分别搜索
- 多渠道同时出现才是真热点
- 热点必须与 AI / 编程 / 工具相关，否则跳过

---

## 第四步：优化执行（不写新文章的高回报动作）

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

缺少内链的文章补 4-6 个相关链接。从目录名自动提取主题词：
```bash
ls content/posts/ai/ | sed 's/^[0-9-]*//' | tr '-' '\n' | sort | uniq -c | sort -rn | head -20
```
同集群文章互链，跨集群做桥接链接。

### 4.3 老文章 SEO 优化

针对高展示低 CTR 的老文章：
- 优化 title（关键词前置，50-60 字符，含年份和数字）
- 优化 description（120-160 字符，直接回答搜索问题）
- 扩充 keywords（加入 GSC 中实际有展示的搜索词）
- 补充 FAQ 结构化数据
- 不修改原始 date 字段

---

## 🛑 Checkpoint：用户确认（必选，不可跳过）

**在第五步之前必须停下**。向用户展示并等待明确回复：

```markdown
## 候选选题（N 个）

### 选题 1: [标题]
- **类型**: 新文章 / 老文章优化 / 内链补充
- **数据依据**: GSC 展示 XX，CTR XX%；MEMORY 记录：[如有]
- **中文角度**: ...
- **英文角度**: ...
- **预期收益**: 从现有 XX 展示多拿 XX 点击
- **工作量**: 低/中/高

### 选题 2: ...

---
请回复：
1. 选哪个（或哪几个并行）？
2. 中文先还是英文先？或两个一起？
3. 有无要调整的角度？
```

**硬规则**：
- 用户没明确回复「选 N」之前，不启动任何写文章 Agent
- 用户只说"开始吧"而没指定哪个 → 追问哪一个（不自作主张）
- 同时启动多篇文章前，确认用户是否接受并行（每篇消耗显著 token）

违反此 checkpoint = 白烧 token、写出用户不想要的东西。

---

## 第五步：并行生产（用户确认后执行）

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
- 必须遵循项目配置文件中的所有写作规则
- 文章目录路径 `content/posts/ai/YYYY-MM-DD-slug/`
- 新文章默认不添加 categories
- 4+ 内链到已有相关文章
- 3-5 个 FAQ 结构化数据

---

## 第六步：发布 + 分发

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

### 6.3 保存报告 + 回写 MEMORY

**两处都要写，不要只写一处**：

1. **完整报告** → `plans/reports/YYYY-MM-DD-report.md`（下次做环比用）
2. **关键发现回写 MEMORY**（`~/.claude/projects/*/memory/MEMORY.md`）：
   - 新发现的高 ROI 优化目标（高展示低 CTR）
   - 整体流量环比（绝对数字 + 百分比）
   - 新形成的头部主题集群及文章数
   - **只写有「惊喜价值」的信息**——不写流水账、不写已能从代码推导的结构信息（参考 CLAUDE.md 里 "What NOT to save"）

示例 MEMORY 更新片段：
```
- GSC ({date_range}): XX clicks, {up/down}{pct}% vs prior
- New CTR issue: {article} ({impressions} impr, {ctr}% CTR)
- Cluster shift: {topic_old} → {topic_new} now top
```

---

## 速查与常见错误

GSC / GA 关键阈值、内容矩阵策略、中英文热度判断、常见错误清单 —— 详见 **[references/thresholds.md](references/thresholds.md)**。

典型陷阱（记住这 3 个就够）：
1. 只看 GSC 不看 GA → 必须交叉分析
2. 中英文写一样的内容 → 角度必须差异化
3. 跳过 Checkpoint 直接 spawn Agent → 会白烧 token
