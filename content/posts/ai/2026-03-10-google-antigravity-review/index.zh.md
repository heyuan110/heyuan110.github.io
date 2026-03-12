+++
date = '2026-03-07T10:00:00+08:00'
draft = false
title = 'Google Antigravity 深度测评：这款免费 Agent-First IDE 到底怎么样？'
description = 'Google Antigravity IDE 深度体验报告——基于 Gemini 3 的免费 Agent-First 开发平台。涵盖安装配置、核心功能、Manager View 以及与 Cursor 和 Claude Code 的详细对比。'
toc = true
tags = ['Google Antigravity', 'AI Coding Tools', 'AI IDE', 'Gemini']
categories = ['AI Guides']
keywords = ['google antigravity', 'google antigravity 测评', 'google antigravity ide', 'antigravity 对比 cursor', 'antigravity 对比 claude code', '免费 ai ide 2026', 'google antigravity 安装', 'gemini 3 编程', 'agent first ide', 'antigravity 下载']

[[params.faqItems]]
question = "Google Antigravity 是免费的吗？"
answer = "是的。Google Antigravity 在公开预览期间对个人用户免费。同时也提供 $20/月的 Pro 版本，拥有更高的用量限制和 Gemini 3 Pro 的优先访问权。"

[[params.faqItems]]
question = "Google Antigravity 支持哪些 AI 模型？"
answer = "Antigravity 支持 Gemini 3 Pro（Google 最新模型）、Gemini 3 Flash（更快更经济）、Claude Sonnet 4.6（Anthropic）以及 GPT-OSS-120B（OpenAI 开源版本）。默认使用 Gemini 3 Pro。"

[[params.faqItems]]
question = "Google Antigravity 支持 MCP 吗？"
answer = "暂时不支持。不同于 Cursor、Claude Code 和 Codex CLI，Antigravity 目前不支持 Model Context Protocol，而是使用 Google 自己的扩展系统。预计未来的更新中会加入 MCP 支持。"

[[params.faqItems]]
question = "Antigravity 和 Cursor 相比怎么样？"
answer = "Antigravity 是 Agent-First（AI 自主工作），而 Cursor 是 Editor-First（你写代码，AI 辅助）。Antigravity 免费，Cursor 需要 $20/月。Cursor 的 VS Code 兼容性更好，Antigravity 在自主多步骤任务上表现更出色。"

[[params.faqItems]]
question = "Antigravity 能用 VS Code 的扩展吗？"
answer = "部分可以。Antigravity 是深度修改的 VS Code 分支，很多扩展能直接用。但由于 Antigravity 自带的 Agent 集成层，部分扩展可能存在兼容性问题。社区扩展市场正在不断壮大。"
+++

![Google Antigravity 测评：基于 Gemini 3 的免费 Agent-First IDE](cover.webp)

AI 编程工具这个赛道，隔三差五就有新产品号称要"颠覆一切"。大多数都是说说而已。但 Google Antigravity——2025 年 11 月随 Gemini 3 一同发布，目前已进入公开预览——可能真的做到了一些不一样的东西。它免费、以 Agent 为核心，对编程的理解方式和 [Cursor](/posts/ai/2026-01-19-cursor-agent-best-practices/) 以及 [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) 有本质区别。

经过几周的日常使用，以下是我的真实感受：它哪里做得好、哪里还不行、以及你是否值得切换过去。

## Antigravity 有什么不同

大多数 AI 编程工具的做法是在已有的编辑器上"嫁接"智能能力。Antigravity 反过来了：**AI Agent 才是主界面**，编辑器反倒是辅助。

核心理念是：你不再自己写代码然后找 AI 帮忙，而是描述你想要什么，**让 Agent 替你完成**——规划、编码、测试、验证，全程自主执行。

这不只是营销话术，整个架构确实体现了这种理念：

```
┌─────────────────────────────────────┐
│        Google Antigravity           │
│                                     │
│  ┌───────────┐  ┌───────────────┐   │
│  │  编辑器   │  │  管理视图     │   │
│  │  视图     │  │  (Manager     │   │
│  │ (VS Code  │  │   View)       │   │
│  │  分支)    │  │  Agent 任务   │   │
│  │           │  │  控制中心     │   │
│  └───────────┘  └───────────────┘   │
│                                     │
│  ┌─────────────────────────────────┐│
│  │  Agents（自主工作者）            ││
│  │  - 根据描述规划任务              ││
│  │  - 编写和修改代码                ││
│  │  - 运行测试和命令                ││
│  │  - 浏览网页做调研                ││
│  │  - 生成 Artifact（可验证产出）   ││
│  └─────────────────────────────────┘│
│                                     │
│  Gemini 3 Pro / Flash / Claude /    │
│  GPT-OSS                            │
└─────────────────────────────────────┘
```

## 安装与配置

### 下载

前往 [antigravity.google/download](https://antigravity.google/) 选择对应版本：
- **macOS**：Intel 和 Apple Silicon 各有独立安装包
- **Windows**：64 位 Windows 10+
- **Linux**：需要 glibc 2.28+

### 首次启动

安装向导会引导你完成以下步骤：

1. **登录** Google 账号
2. **选择开发模式**（下面会详细介绍）
3. **导入 VS Code 配置**（可选——主题、快捷键和大部分扩展都能迁移过来）

### 三种开发模式

这是 Antigravity 开始展现差异化的地方：

| 模式 | 工作方式 | 适用场景 |
|------|---------|---------|
| **Agent 驱动** ("Autopilot") | AI 自主写代码，你负责审查 | 原型开发、代码脚手架、重复性任务 |
| **审查驱动** | AI 每个操作都要你批准 | 生产代码、学习新代码库 |
| **Agent 辅助**（推荐） | 你写代码，AI 处理安全的自动化操作 | 日常开发、团队协作项目 |

**我的建议**：先用 **Agent 辅助模式**。它在效率和掌控力之间取得了最好的平衡。等你需要快速出原型或者生成样板代码时，再切到 Agent 驱动模式。

## 双界面：编辑器视图 vs 管理视图

### 编辑器视图

这个界面看起来很熟悉——基本就是 VS Code 加了一个 AI Agent 侧边栏。你能用到：
- 标准的代码编辑功能，语法高亮、扩展等一应俱全
- 一个 Agent 面板，可以用自然语言描述任务
- 由 Gemini 3 驱动的行内补全和建议
- 终端集成

如果你之前用过 Cursor 或 VS Code，上手毫无障碍。

### Manager View：真正的创新

这才是 Antigravity 的杀手锏。Manager View 是一个**任务控制仪表盘**，你可以：

- **同时派发多个 Agent**——把 5 个不同的 Bug 分给 5 个 Agent 并行处理
- **实时监控 Agent 进度**，带状态更新
- **审查 Artifact**——Agent 会生成可验证的交付物（任务清单、实现方案、截图，甚至浏览器录屏）
- **在变更生效前进行批准或拒绝**

你可以把它理解为管理一个初级开发团队——你分配任务，他们独立完成，你在合并前审查产出。

**这就是核心竞争力。** 目前没有任何其他工具——不管是 Cursor、[Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) 还是 Codex CLI——能在可视化界面中提供这种级别的并行 Agent 调度能力。

## 支持的 AI 模型

Antigravity 不会把你锁定在 Google 自家模型上：

| 模型 | 提供商 | 优势 | 可用性 |
|------|-------|------|-------|
| **Gemini 3 Pro** | Google | 综合推理能力最强，多模态 | 默认模型，免费版可用 |
| **Gemini 3 Flash** | Google | 更快，更省资源 | 免费版可用 |
| **Claude Sonnet 4.6** | Anthropic | 代码质量高，返工率低 | 免费版可用 |
| **GPT-OSS-120B** | OpenAI | 开源，适合对数据敏感的项目 | 免费版可用 |

多模型支持做得出乎意料的好。你可以给不同的 Agent 指定不同的模型——比如用 Gemini 3 Pro 做架构规划，用 Claude Sonnet 做具体实现。

**还缺什么**：Claude Opus 4.6 和 GPT-5 目前不可用。如果你需要最强的推理能力，还是得用 [Claude Code](/posts/ai/2026-02-25-claude-code-pricing/) 或 [Codex CLI](/posts/ai/2026-03-10-codex-cli-deep-dive/)。

## Artifact：用透明性建立信任

Antigravity 最聪明的设计之一就是 **Artifact 机制**。Agent 不只是展示工具调用和输出结果，而是生成结构化的交付物：

- **任务清单**——执行前的分步计划
- **实现方案**——架构决策及其理由
- **截图**——UI 变更的可视化证据
- **浏览器录屏**——Agent 网页调研过程的录像
- **测试结果**——变更的自动化验证

这一点很重要，因为自主 Agent 最大的问题就是信任。"它真的按我说的做了吗？有没有搞坏什么东西？" Artifact 让你不用逐行看代码 diff 就能获得可验证的证据。

## Antigravity 的优势

### 1. 并行 Agent 工作流

同时派 5 个 Agent 处理 5 个任务，这**确实比串行工具快**。实际使用中，对于独立任务（比如修复多个 Bug 或为不同模块添加测试），我观察到了 3-4 倍的吞吐量提升。

### 2. 零成本入门

公开预览期间对个人用户免费。不需要信用卡，没有试用期限制。对比一下：
- [Claude Code](/posts/ai/2026-02-25-claude-code-pricing/)：$20-$200/月
- [Cursor](/posts/ai/2026-02-28-claude-code-vs-cursor/)：$20/月 + 超额费用
- [Codex CLI](/posts/ai/2026-03-10-codex-cli-deep-dive/)：$20-$200/月（ChatGPT 订阅）

对于学生、业余爱好者或者正在评估 AI 编程工具的开发者来说，这个价格无人能敌。

### 3. 可视化 Agent 管理

Manager View 让不想在终端里操作的人也能轻松使用 Agent 调度。如果你更喜欢图形界面而不是命令行，Antigravity 是最友好的选择。

### 4. 多模型灵活切换

能在 Gemini、Claude 和 GPT 模型之间自由选择，并为不同的 Agent 指定不同模型——这是其他 IDE 都没有的独特优势。

## Antigravity 的不足

### 1. 不支持 MCP

这是最大的短板。[MCP（Model Context Protocol）](/posts/ai/2026-02-28-mcp-protocol-explained/)已经成为 AI 工具连接外部服务的通用标准，Claude Code、Cursor 和 Codex CLI 都支持。Antigravity 用的是 Google 自己的扩展系统。

这意味着你无法使用那些连接数据库、Figma、Sentry、GitHub 等[上百种服务的 MCP 服务器](/posts/ai/2026-03-05-best-mcp-servers-claude-code/)。Google 表示 MCP 支持即将到来，但目前还没有。

### 2. Gemini 3 vs Opus 4.6 的复杂推理能力

Gemini 3 Pro 在大多数编程任务上表现优秀。但在深度复杂推理方面——多步骤架构决策、大代码库中微妙 Bug 的定位——Claude Opus 4.6 仍然占优。多位开发者的反馈表明，Claude Code 产生的代码返工率比其他工具低约 30%。

### 3. Agent 在复杂任务上的可靠性

自主 Agent 在定义明确的任务上表现很好（修复这个 Bug、添加这个测试、搭建这个组件）。但面对模糊的、开放性的任务（"把这个模块重构得更好维护"），Agent 有时候会兜圈子或做出不太靠谱的架构选择。

这不是 Antigravity 独有的问题——这是当前 AI Agent 的固有局限。但 Agent-First 的设计意味着你会比其他默认保持人工参与的工具更频繁地遇到这种情况。

### 4. 扩展兼容性

虽然 Antigravity 是 VS Code 的分支，但并非所有扩展都能完美运行。自定义的 Agent 集成层可能与一些热门扩展产生冲突。扩展市场在增长中，但规模还不及 VS Code。

## Antigravity vs Cursor vs Claude Code

| 特性 | Antigravity | Cursor | Claude Code |
|------|-------------|--------|-------------|
| **设计理念** | Agent-First | Editor-First | Terminal-First |
| **价格** | 免费（预览期） | $20/月 | $20-$200/月 |
| **最强模型** | Gemini 3 Pro | 多模型 | Claude Opus 4.6 |
| **并行 Agent** | 有（Manager View） | 无 | 通过 [Worktree](/posts/ai/2026-02-28-claude-code-worktree-guide/) |
| **MCP 支持** | 无 | 有 | 有 |
| **VS Code 兼容** | 部分（分支） | 完全（分支） | 不适用（终端） |
| **推理深度** | 好 | 好 | 最强 |
| **Agent 自主性** | 最高 | 中等 | 高 |
| **代码返工率** | 中等 | 中等 | 最低（约少 30%） |
| **最适合** | 原型开发、并行任务 | 日常 IDE 工作流 | 复杂推理、自动化 |

### 我的推荐

**选 Antigravity 的场景**：原型开发、处理多个独立任务、想要免费方案、或者偏好可视化的 Agent 管理。

**选 Cursor 的场景**：想要熟悉的 VS Code 体验加 AI 辅助、需要完整的扩展兼容性、或者希望掌控每一处改动。

**选 [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) 的场景**：需要深度推理处理复杂任务、想要基于终端的自动化、需要 MCP 集成、或者在做大规模[多 Agent 协同](/posts/ai/2026-02-22-claude-code-agent-teams/)。

**2026 年的最优组合**：很多开发者正在用 Antigravity 做快速原型 + Claude Code 处理复杂任务。$0 + $100/月（Claude Max 5x），这个组合相当强大。

## 充分发挥 Antigravity 的使用技巧

### 1. 从 Agent 辅助模式开始

别一上来就开"Autopilot"。先在 Agent 辅助模式下熟悉工具的行为模式，建立信任后再逐步放开更多自主权。

### 2. Manager View 适合独立任务

Manager View 在处理**独立、定义明确的任务**时最出色。"修复这 5 个 Bug"或"给这 3 个模块加单元测试"是理想的使用场景。不要用它来处理相互依赖的任务。

### 3. 策略性地分配模型

- **Gemini 3 Pro**：架构规划、复杂实现
- **Gemini 3 Flash**：快速修复、格式调整、简单新增
- **Claude Sonnet 4.6**：高质量代码，减少迭代次数

### 4. 批准前先审查 Artifact

不要自动批准 Agent 的变更。仔细看 Artifact——特别是实现方案和测试结果。这是你的质量关卡。

### 5. 保持任务小而具体

"构建登录系统"对自主 Agent 来说太模糊了。"创建一个包含邮箱/密码字段的登录表单组件，带表单验证，以及调用 /api/auth 接口的提交处理函数"——这才能给 Agent 一个明确的目标。

## 更大的视角：Antigravity 对 AI 编程意味着什么

Antigravity 代表了 AI 编程工具思维方式的一次真正转变。这个行业已经经历了三个阶段：

1. **自动补全时代**（2022-2024）：Copilot、Tabnine——AI 提示下一行代码
2. **Agent 辅助时代**（2024-2025）：Cursor、Claude Code——AI 帮你写代码
3. **Agent 优先时代**（2026）：Antigravity——AI 来写，你来管

Agent-First 的方式能否成为主流，取决于一个关键因素：**可靠性**。如果 Agent 能持续产出生产级别的代码而不需要人类反复干预，那 Antigravity 的路线就赢了。如果 Agent 仍然需要大量审查，那 Cursor 这样 Editor-First 的工具效率反而更高。

目前的状态介于两者之间。Antigravity 在它擅长的任务上表现出色，但还没有准备好在复杂的、关键的生产工作中取代人类判断。

## 最终评价

**评分：8/10**

Google Antigravity 是 2026 年最具创新性的 AI 编程工具。Manager View、多模型支持和零成本入门使它确实有吸引力。MCP 支持的缺失和 Agent 可靠性的偶发问题让它暂时无法在复杂工作上取代 Claude Code，也无法在日常 IDE 使用上取代 Cursor。

**值得一试吗？** 毫无疑问——反正免费。装上它，花一个下午在 Manager View 里体验并行 Agent 调度，自己做判断。最差的结果也不过是多了一个强力工具。

---

*本测评基于 Google Antigravity 2026 年 3 月公开预览版。功能和定价可能随产品迭代而变化。*

## 延伸阅读

- [Claude Code Complete Guide 2026](/posts/ai/2026-02-28-claude-code-complete-guide/) — Terminal-First 的替代方案
- [Claude Code vs Cursor: Which Wins?](/posts/ai/2026-02-28-claude-code-vs-cursor/) — Editor-First vs Terminal-First 对比
- [Codex CLI Deep Dive](/posts/ai/2026-03-10-codex-cli-deep-dive/) — OpenAI 的终端 AI 助手
- [Claude Code Pricing 2026](/posts/ai/2026-02-25-claude-code-pricing/) — 所有工具的费用对比
- [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) — Antigravity 暂时不支持的那个标准
- [Vibe Coding Explained](/posts/ai/2026-02-28-vibe-coding-explained/) — Antigravity 所体现的编程理念
