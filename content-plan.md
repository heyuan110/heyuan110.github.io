# Bruce on AI Engineering — 内容规划 (50 篇)

> 围绕 5 个主题集群建立系列文章，每个主题至少 10 篇。
> 采用 **1 篇 Pillar（核心长文）+ 9 篇 Supporting（子话题）** 结构，互相内链形成主题集群。

---

## 分类和标签策略

| 主题集群 | 分类 (category) | 主标签 (tag) |
|---------|----------------|-------------|
| Claude Code | AI Guides | Claude Code |
| AI Agent Framework | AI Guides | AI Agent |
| AI Coding Tools | Comparisons / AI Guides | AI Coding Tools |
| AI Engineering Workflow | AI Guides | AI Workflow |
| Tool Comparisons | Comparisons | 按具体工具打标签 |

---

## Cluster 1: Claude Code（AI Guides）

| # | 类型 | 标题 | 商业意图 | 状态 | 中文素材 |
|---|------|------|---------|------|---------|
| 1 | Pillar | Claude Code Complete Guide 2026: From Setup to Advanced Workflows | 高 | ⬜ | — |
| 2 | Setup | Claude Code Installation & First Project: Step-by-Step | 高 | ✅ | — |
| 3 | Guide | CLAUDE.md Guide: Give AI Perfect Project Context Every Time | 中 | ✅ | ✅ `claudemd-memory-guide` + `claudemd-vs-readme` |
| 4 | Guide | Claude Code MCP Setup: Connect AI to Any External Service | 高 | ✅ | ✅ `claude-code-mcp-server-tutorial` |
| 5 | Guide | Claude Code Hooks: 12 Ready-to-Use Automation Configs | 中 | ✅ | ✅ `claude-code-hooks-guide` |
| 6 | Guide | Claude Code Skills: Teach AI Your Custom Workflows | 中 | ✅ | ✅ `claudecode-skill-guide` + `claude-code-skills-top20` |
| 7 | Guide | Claude Code Worktree: Run Multiple AI Tasks in Parallel | 中 | ✅ | ✅ `claude-code-worktree` |
| 8 | Guide | Claude Code for Teams: Multi-Agent Collaboration Patterns | 高 | ✅ | ✅ `claude-code-agent-teams` |
| 9 | Pricing | Claude Code Pricing 2026: Is the Max Plan Worth $200/Month? | 高 | ✅ | — |
| 10 | Guide | 10 Claude Code Mistakes Beginners Make (And How to Fix Them) | 中 | ✅ | — |

### Claude Code 推荐写作顺序

| 顺序 | 文章 | 理由 |
|------|------|------|
| **1** | #9 Pricing（定价分析） | 最快变现，最快发布，1500-2000 字即可 |
| **2** | #2 Setup（安装教程） | 搜索量大，新手刚需 |
| **3** | #10 10 Mistakes（避坑指南） | 点击率高，易传播 |
| **4** | #3 CLAUDE.md Guide | 差异化内容，竞品少 |
| **5** | #4 MCP Setup | 高商业意图，实战刚需 |
| **6** | #5 Hooks | 进阶用户搜索 |
| **7** | #6 Skills | 进阶用户搜索 |
| **8** | #7 Worktree | 进阶用户搜索 |
| **9** | #8 Teams / Multi-Agent | 企业用户关注 |
| **10** | #1 **Pillar（完全指南）** | 最后写，汇总所有内链 |

> Pillar 放最后：因为它需要链接到其他 9 篇文章，先把子文章写完，Pillar 自然就是一篇高质量的导航长文。

---

## Cluster 2: AI Agent Framework（AI Guides）

| # | 类型 | 标题 | 商业意图 | 状态 | 中文素材 |
|---|------|------|---------|------|---------|
| 11 | Pillar | AI Agent Frameworks Compared 2026: LangChain vs CrewAI vs AutoGen | 高 | ⬜ | — |
| 12 | Guide | How to Build an AI Agent from Scratch with Python | 高 | ⬜ | ✅ `build-magic-code`（已英文） |
| 13 | Guide | MCP Protocol Explained: The Universal Standard for AI Tools | 高 | ⬜ | ✅ `mcp-protocol-guide` |
| 14 | Setup | Building MCP Servers: TypeScript Tutorial from Zero to Deploy | 高 | ⬜ | ✅ `claude-code-mcp-server-tutorial` |
| 15 | Guide | Multi-Agent Orchestration: Patterns That Actually Work | 中 | ⬜ | ✅ `openclaw-multi-agent-guide` + `agent-manager-patterns` |
| 16 | Guide | RAG Pipeline Setup: Vector Database + LLM Integration Guide | 高 | ⬜ | ✅ `vectordatabase`（部分） |
| 17 | Guide | AI Agent Memory Systems: RAG vs Context Engineering | 中 | ⬜ | ✅ `claude-mem-deep-dive` + `context-engineering-deep-dive` |
| 18 | Guide | AI Agent Security: Protecting Automated Workflows | 中 | ⬜ | ✅ `mcp-security-guide` + `claude-code-security` |
| 19 | Guide | From Prototype to Production: AI Agent Deployment Checklist | 高 | ⬜ | ✅ `prototype-to-production` |
| 20 | Review | OpenClaw Deep Dive: Architecture, Setup, and Real-World Usage | 中 | ⬜ | ✅ `openclaw-architecture-deep-dive` + `openclaw-usage-tutorial` |

### AI Agent Framework 推荐写作顺序

| 顺序 | 文章 | 理由 |
|------|------|------|
| **1** | #13 MCP Protocol Explained | 搜索量大，MCP 是 2026 热词，有现成中文素材 |
| **2** | #14 Building MCP Servers | 紧接 MCP 话题，实战教程搜索意图强 |
| **3** | #12 Build AI Agent from Scratch | 已有英文版 `build-magic-code`，可扩展为独立教程 |
| **4** | #19 Prototype to Production | 高商业意图，企业开发者关注 |
| **5** | #16 RAG Pipeline Setup | 热门话题，向量数据库 + LLM 集成 |
| **6** | #18 AI Agent Security | 安全话题差异化强，竞品少 |
| **7** | #15 Multi-Agent Orchestration | 进阶内容，有多篇中文素材合并 |
| **8** | #17 Memory Systems | 深度技术话题 |
| **9** | #20 OpenClaw Deep Dive | 项目专属评测 |
| **10** | #11 **Pillar（框架对比）** | 最后写，汇总所有内链 |

---

## Cluster 3: AI Coding Tools（Comparisons + AI Guides）

| # | 类型 | 标题 | 商业意图 | 状态 | 中文素材 |
|---|------|------|---------|------|---------|
| 21 | Pillar | Best AI Coding Tools 2026: Complete Comparison & Ranking | 高 | ⬜ | — |
| 22 | Setup | Cursor Setup Guide: Installation to Advanced Agent Mode | 高 | ⬜ | ✅ `cursor-agent-best-practices` |
| 23 | Comparison | GitHub Copilot vs Claude Code vs Cursor: Real-World Benchmarks | 高 | ⬜ | ✅ `claude-code-vs-cursor-vs-windsurf-2026` |
| 24 | Review | Codex CLI Deep Dive: OpenAI's Terminal AI Assistant | 高 | ⬜ | ✅ `codex-cli-mastery-guide` |
| 25 | Review | Windsurf Review: Is Codeium's AI IDE Worth Switching To? | 高 | ⬜ | — |
| 26 | Best Tools | Best VS Code AI Extensions 2026: Ranked by Real Usage | 高 | ⬜ | — |
| 27 | Pricing | AI Coding Tools Pricing 2026: Free vs Paid Tier Breakdown | 高 | ⬜ | — |
| 28 | Guide | How to Pick the Right AI Coding Tool for Your Tech Stack | 高 | ⬜ | — |
| 29 | Comparison | AI Code Review Tools: Top 5 Options Head-to-Head | 高 | ⬜ | — |
| 30 | Guide | Devin vs Human Developers: What AI Agents Do Well (And Don't) | 中 | ⬜ | ✅ `agentic-coding-trends-2026`（部分） |

### AI Coding Tools 推荐写作顺序

| 顺序 | 文章 | 理由 |
|------|------|------|
| **1** | #23 Copilot vs Claude Code vs Cursor | 最高搜索量对比类关键词，有中文素材改写 |
| **2** | #27 AI Coding Tools Pricing | 定价对比搜索意图强，变现快 |
| **3** | #24 Codex CLI Deep Dive | 有中文素材，OpenAI 竞品关注度高 |
| **4** | #22 Cursor Setup Guide | 有中文素材，Cursor 用户群大 |
| **5** | #25 Windsurf Review | 无中文素材但需求大，新鲜评测 |
| **6** | #26 Best VS Code AI Extensions | 长尾流量，工具合集类 SEO 友好 |
| **7** | #28 Pick the Right Tool | 指导类内容，内链价值高 |
| **8** | #29 AI Code Review Tools | 细分领域对比 |
| **9** | #30 Devin vs Human | 话题性强，引流内容 |
| **10** | #21 **Pillar（工具总览）** | 最后写，汇总所有内链 |

---

## Cluster 4: AI Engineering Workflow（AI Guides）

| # | 类型 | 标题 | 商业意图 | 状态 | 中文素材 |
|---|------|------|---------|------|---------|
| 31 | Pillar | AI Engineering Workflow 2026: Idea to Production Playbook | 高 | ⬜ | — |
| 32 | Guide | Context Engineering: The Most Underrated AI Development Skill | 中 | ⬜ | ✅ `context-engineering-deep-dive` |
| 33 | Guide | Prompt Engineering for Production: Patterns That Scale | 高 | ⬜ | — |
| 34 | Guide | AI-Assisted Testing: Generate Unit Tests with Claude Code | 中 | ⬜ | ✅ `unit-test-report-tools`（部分） |
| 35 | Guide | AI Dev Environment Setup: Tools, Configs, and Dotfiles | 高 | ⬜ | ✅ `ai-dev-workflow` + `ai-workflow-real-guide` |
| 36 | Guide | Vibe Coding Explained: What It Is and How to Do It Right | 中 | ⬜ | ✅ `vibe-coding-guide` + `secure-vibe-coding` |
| 37 | Guide | AI Pair Programming Patterns for Maximum Productivity | 中 | ⬜ | — |
| 38 | Guide | High-Frequency Commits: Ship 100+ Commits/Day Without Chaos | 中 | ⬜ | ✅ `high-frequency-commits-strategy` |
| 39 | Guide | CI/CD for AI-Assisted Development: Quality at Scale | 中 | ⬜ | — |
| 40 | Guide | Technical Writing with AI: Better Docs in Half the Time | 中 | ⬜ | — |

### AI Engineering Workflow 推荐写作顺序

| 顺序 | 文章 | 理由 |
|------|------|------|
| **1** | #36 Vibe Coding Explained | 2026 年度热词，搜索量暴涨，有两篇中文素材 |
| **2** | #35 AI Dev Environment Setup | 高商业意图，新手必看，有中文素材 |
| **3** | #33 Prompt Engineering for Production | 经典常青话题，搜索量稳定 |
| **4** | #32 Context Engineering | 差异化概念，斯坦福课程背书 |
| **5** | #38 High-Frequency Commits | 有中文素材，实战方法论 |
| **6** | #34 AI-Assisted Testing | 实战向，开发者刚需 |
| **7** | #37 AI Pair Programming | 补充 Vibe Coding 的系统方法 |
| **8** | #39 CI/CD for AI Dev | 工程化进阶内容 |
| **9** | #40 Technical Writing with AI | 长尾内容 |
| **10** | #31 **Pillar（工作流总览）** | 最后写，汇总所有内链 |

---

## Cluster 5: Tool Comparisons（Comparisons）

| # | 类型 | 标题 | 商业意图 | 状态 | 中文素材 |
|---|------|------|---------|------|---------|
| 41 | Pillar | AI Developer Tools Landscape 2026: The Complete Map | 高 | ⬜ | — |
| 42 | Comparison | Claude Code vs Cursor: Which Wins for Real Projects? | 高 | ⬜ | ✅ `claude-code-vs-cursor-vs-windsurf-2026`（部分） |
| 43 | Comparison | Claude vs GPT-4o vs Gemini: Best LLM for Coding in 2026 | 高 | ⬜ | ✅ `claude-code-vs-codex`（部分） |
| 44 | Comparison | Vector Databases Compared: Pinecone vs Weaviate vs Qdrant | 高 | ⬜ | ✅ `vectordatabase` |
| 45 | Comparison | LangChain vs LlamaIndex: Which RAG Framework to Use | 高 | ⬜ | — |
| 46 | Comparison | Browser Automation 2026: Playwright vs Puppeteer vs Selenium | 高 | ⬜ | — |
| 47 | Comparison | Vercel vs Netlify vs Cloudflare: Best Deploy for AI Apps | 高 | ⬜ | — |
| 48 | Comparison | MCP vs Custom API: When to Use Which Integration | 中 | ⬜ | ✅ `mcp-protocol-guide`（部分） |
| 49 | Comparison | Self-Hosted vs Cloud AI: Cost Analysis for Small Teams | 高 | ⬜ | — |
| 50 | Best Tools | Top 10 AI Tools Every Developer Should Use in 2026 | 高 | ⬜ | — |

### Tool Comparisons 推荐写作顺序

| 顺序 | 文章 | 理由 |
|------|------|------|
| **1** | #42 Claude Code vs Cursor | 最热门双工具对比，搜索量极高 |
| **2** | #43 Claude vs GPT-4o vs Gemini | LLM 三巨头对比，流量密码 |
| **3** | #50 Top 10 AI Tools | 合集类文章 SEO 效果好，引流能力强 |
| **4** | #44 Vector Databases Compared | 有中文素材，技术深度高 |
| **5** | #45 LangChain vs LlamaIndex | RAG 框架热门对比 |
| **6** | #49 Self-Hosted vs Cloud AI | 成本分析，决策者关注 |
| **7** | #46 Browser Automation | 工具对比经典长青话题 |
| **8** | #47 Deploy Platforms | 部署平台对比 |
| **9** | #48 MCP vs Custom API | 有部分中文素材 |
| **10** | #41 **Pillar（工具全景）** | 最后写，汇总所有内链 |

---

## 内链结构策略

```
每个 Pillar 文章 ←-- 链接所有 9 篇 Supporting 文章
每篇 Supporting --→ 链接回 Pillar + 2-3 篇同集群文章
跨集群链接：Comparisons 类引用对应 Guides 类的深度文章
```

---

## 整体执行顺序

| 阶段 | 时间 | 任务 | 状态 |
|------|------|------|------|
| Phase 1 | 第 1 周 | Claude Code 集群前 3 篇（#9 Pricing → #2 Setup → #10 Mistakes） | ✅ 已完成 |
| Phase 2 | 第 2-3 周 | Claude Code 剩余 7 篇（#3→#4→#5→#6→#7→#8→#1） | ✅ 6/7 完成（剩 #1 Pillar） |
| Phase 3 | 第 4-5 周 | 每个集群首篇高搜索量文章（#13、#23、#36、#42） | ⬜ |
| Phase 4 | 第 6-8 周 | 有中文素材的文章优先改写（约 20 篇） | ⬜ |
| Phase 5 | 第 9-12 周 | 无素材的新文章 + 5 篇 Pillar | ⬜ |

### Phase 2 详细计划（当前阶段）

优先改写有中文素材的文章，效率最高：

| 顺序 | 文章 | 预计工作量 | 来源 |
|------|------|-----------|------|
| **1** | #3 CLAUDE.md Guide | 中（合并 2 篇中文） | `claudemd-memory-guide` + `claudemd-vs-readme` |
| **2** | #4 MCP Setup | 中（改写 1 篇中文） | `claude-code-mcp-server-tutorial` |
| **3** | #5 Hooks Guide | 低（改写 1 篇中文） | `claude-code-hooks-guide` |
| **4** | #6 Skills Guide | 中（合并 2 篇中文） | `claudecode-skill-guide` + `claude-code-skills-top20` |
| **5** | #7 Worktree Guide | 低（改写 1 篇中文） | `claude-code-worktree` |
| **6** | #8 Teams Guide | 低（改写 1 篇中文） | `claude-code-agent-teams` |
| **7** | #1 Pillar（完全指南） | 高（新写，汇总内链） | 所有 Cluster 1 文章完成后 |

### Phase 3 跨集群首发文章

每个集群选 1 篇最高搜索量 + 有中文素材的文章，快速铺开覆盖面：

| 集群 | 文章 | 理由 |
|------|------|------|
| Cluster 2 | #13 MCP Protocol Explained | MCP 热词 + 中文素材 |
| Cluster 3 | #23 Copilot vs Claude vs Cursor | 最热门对比关键词 + 中文素材 |
| Cluster 4 | #36 Vibe Coding Explained | 2026 热词 + 两篇中文素材 |
| Cluster 5 | #42 Claude Code vs Cursor | 搜索量极高 + 中文素材 |

---

## 中文素材统计

| 项目 | 数量 |
|------|------|
| 规划文章总数 | 50 篇 |
| 已完成英文文章 | 10 篇（#2, #3, #4, #5, #6, #7, #8, #9, #10 + Rate Limits） |
| 有中文素材可改写 | 27 篇 |
| 需全新创作 | 20 篇 |
| 改写效率提升 | 有素材的文章预计写作时间减少 50-60% |

---

## 关键策略

1. **文章类型优先级**: Guide > Setup > Comparison > Best Tools > Workflow > Review
2. **先写高商业意图文章**: 搜 pricing/setup/comparison 的人更接近转化
3. **Pillar 最后写**: 子文章先完成，Pillar 汇总所有内链
4. **每篇文章 2000+ 字**: 确保内容深度满足 AdSense 要求
5. **所有新内容用英文**: 中文内容保留但不再新增
6. **中文素材优先改写**: 有现成中文文章的优先改写为英文，效率最高
7. **改写 ≠ 翻译**: 改写时重新组织结构、补充最新信息、优化 SEO 标题
8. **跨集群并行**: Phase 3 开始同时推进多个集群，避免单一集群疲劳
