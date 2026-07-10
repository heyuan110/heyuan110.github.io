+++
date = '2026-03-10T14:00:00+08:00'
draft = false
title = 'AI 开发环境搭建：2026 年工具、配置与 Dotfiles 完全指南'
description = 'AI 开发环境搭建 2026 完全指南：Claude Code 负责规划推理 + Cursor 负责日常编码的组合月均约 40 美元即可覆盖几乎所有场景。涵盖 CLAUDE.md、MCP 服务器、tmux、Dotfiles 配置，附可直接复制的模板与 Shell 别名。'
toc = true
tags = ['AI Development', 'Developer Setup', 'Claude Code', 'Workflow']
categories = ['AI Guides']
keywords = ['AI 开发环境搭建', '2026 AI 编程工具', 'AI 开发工作流', 'Claude Code 配置', 'Cursor 配置', 'AI 编程环境']

[[params.faqItems]]
question = "2026 年最好用的 AI 编程工具是什么？"
answer = "没有单一的最佳工具。最高效的方案是将 Claude Code（负责规划和复杂推理）与 Cursor（负责日常编码实现）组合使用。这套多工具策略每月约 40 美元，几乎能覆盖所有开发场景。"

[[params.faqItems]]
question = "Claude Code 和 Cursor 都需要付费吗？"
answer = "最佳性价比方案是 Claude Code Max（20 美元/月，5 倍用量）加上 Cursor Pro（20 美元/月）。每月总计 40 美元，既有深度推理能力用于架构和规划，又有快速的 IDE 集成编码能力用于实现。"

[[params.faqItems]]
question = "CLAUDE.md 是什么？为什么需要它？"
answer = "CLAUDE.md 是放在项目根目录的配置文件，用于告诉 Claude Code 你的项目规范、编码标准和偏好。它能显著提升 AI 输出质量，因为它为 AI 提供了关于你代码库的持久化上下文信息。"

[[params.faqItems]]
question = "可以在 Cursor 里使用 Claude Code 吗？"
answer = "可以。Claude Code 能在任何终端中运行，包括 Cursor 的集成终端。很多开发者就是这样用的：在终端面板用 Claude Code 做规划，在编辑器面板用 Cursor 的 Agent 模式来实现代码。"

[[params.faqItems]]
question = "MCP 服务器是什么？需要配置吗？"
answer = "MCP（Model Context Protocol）服务器用于将 AI 工具连接到外部服务，比如数据库、API 和文档。它不是必需的，但强烈推荐配置——有了它，Claude Code 就能直接与你的实际基础设施交互，而不仅仅是读取代码文件。"

[[params.faqItems]]
question = "如何有效控制 AI 工具的成本？"
answer = "将 Claude Code 用于高价值任务（架构设计、调试、复杂重构），将 Cursor 用于常规编码。养成会话管理习惯——任务之间清除上下文，简单查询使用紧凑模式，避免不必要地重复读取大型代码库。"
+++

![AI 开发环境搭建指南：涵盖 2026 年工具、配置和 Dotfiles](cover.webp)

AI 工具的效果取决于你的配置。大多数开发者安装完 Claude Code 或 Cursor 后，直接用默认设置就开始干活，然后纳闷为什么 AI 的输出总是那么泛泛而谈。平庸的 AI 辅助和真正变革性的生产力提升之间，差距就在于**配置**——那些 dotfiles、模板、Shell 别名和工作流模式，能把通用的 AI 工具变成真正理解*你的*代码库和*你的*开发规范的利器。

本指南完整记录了我每天使用的 AI 开发环境。读完之后，你将拥有一套生产级的配置方案，把多个 AI 工具整合成连贯的工作流，并附带可直接复制修改的配置文件。

## 现代 AI 开发技术栈

在开始安装之前，先理清整体架构。2026 年高效的 AI 开发环境不是单一工具——而是一套**互补的工具栈**，各司其职，发挥所长。

完整的技术栈如下：

| 层级 | 工具 | 职责 |
|------|------|------|
| **规划与推理** | Claude Code | 架构决策、复杂调试、跨文件重构 |
| **日常编码** | Cursor | 写代码、行内编辑、快速迭代 |
| **终端复用** | tmux / Zellij | 并行会话、持久化工作区 |
| **版本控制** | Git + AI 工作流 | AI 友好的提交策略、分支管理 |
| **外部服务** | MCP 服务器 | 连接 AI 到数据库、文档、API |
| **自动化** | Hooks 与脚本 | 确定性规则，覆盖 AI 行为 |

核心理念是：**Claude Code 擅长思考，Cursor 擅长输出。** 当你需要 AI 理解复杂问题、评估权衡或规划多步骤变更时，用 Claude Code。当你知道该写什么、需要快速流畅地实现时，切换到 Cursor。

这就是我们在 [Claude Code vs Cursor 对比](/zh/posts/ai/2026-02-28-claude-code-vs-cursor/) 中介绍的多工具策略，不过这里我们聚焦于**实际配置**，而非概念层面的差异。

## 核心工具配置

### Claude Code：你的 AI 推理引擎

Claude Code 是 Anthropic 推出的终端 AI 编程智能体。与 IDE 插件只能建议代码片段不同，Claude Code 作为自主代理运行——它能阅读整个代码库、规划多步骤变更、执行 Shell 命令，并持续迭代直到任务完成。

如需深入了解 Claude Code 的全部功能，请参阅 [Claude Code 完全指南](/zh/posts/ai/2026-02-28-claude-code-complete-guide/)。

#### 安装

```bash
# 通过原生安装器安装（推荐）
curl -fsSL https://cli.claude.ai/install.sh | sh

# 或通过 npm 安装（如果你更习惯包管理器）
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

安装完成后进行认证：

```bash
# 启动 Claude Code，按照提示完成认证
claude

# 或者直接认证
claude auth login
```

#### CLAUDE.md 配置文件

这是你能创建的**最有影响力**的配置。项目根目录下的 `CLAUDE.md` 文件告诉 Claude Code 关于你项目的一切——编码规范、目录结构、常用命令，以及需要注意的事项。

以下是一个生产可用的模板：

````markdown
# CLAUDE.md

## 项目概览
- **技术栈**：Node.js / TypeScript / PostgreSQL / React
- **架构**：Monorepo，使用 packages/ 目录
- **Node 版本**：22（使用 nvm 管理）

## 常用命令
```bash
# 开发
npm run dev          # 启动开发服务器（端口 3000）
npm run test         # 运行测试
npm run test:watch   # 监听模式运行测试
npm run lint         # ESLint + Prettier 检查
npm run typecheck    # TypeScript 类型检查

# 数据库
npm run db:migrate   # 执行待运行的迁移
npm run db:seed      # 填充开发数据
npm run db:reset     # 重置并重新填充数据库
```

## 代码规范
- 使用函数式组件配合 Hooks（禁止使用 class 组件）
- 所有 API 路由放在 `src/routes/` 下，遵循 REST 规范
- 数据库查询使用 `src/repositories/` 中的 Repository 模式
- 错误处理统一使用 `src/utils/errors.ts` 中的 AppError 类
- 测试文件与源文件同目录放置（如 `user.service.test.ts`）

## 重要规则
- 绝对不要修改 `src/generated/` 下的文件——它们是自动生成的
- 提交前必须运行 `npm run typecheck`
- 数据库迁移必须可回滚
- API 响应必须遵循 `src/utils/response.ts` 中的格式

## 架构说明
- 认证：JWT + Refresh Token 轮换
- 文件上传：通过预签名 URL 存储到 S3（禁止本地存储）
- 后台任务：BullMQ + Redis
- 缓存：Redis，API 响应默认 5 分钟 TTL
````

如需了解如何编写高质量的 CLAUDE.md，请参阅 [CLAUDE.md 完全指南](/zh/posts/ai/2026-02-28-claude-code-claudemd-guide/)。

**编写 CLAUDE.md 的核心原则：**

1. **命令要准确** —— Claude Code 会直接执行这些命令，所以必须正确
2. **明确说明禁止做的事** —— 否定约束能有效防止 AI 犯常见错误
3. **包含架构上下文** —— AI 需要理解代码*为什么*这样组织，而不仅仅是*怎么*组织的
4. **保持更新** —— 过时的 CLAUDE.md 比没有还糟糕

#### MCP 服务器配置

MCP（Model Context Protocol）服务器将 Claude Code 的能力扩展到本地文件系统之外。它让 AI 可以与数据库、文档服务、浏览器自动化工具等进行交互。

MCP 配置文件位于 `~/.claude/mcp.json`（全局）或 `.claude/mcp.json`（项目级）：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "description": "Library documentation lookup"
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      },
      "description": "Direct database access"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"],
      "description": "Browser automation for testing"
    }
  }
}
```

如需了解 10+ 种 MCP 服务器的完整配置，请参阅 [Claude Code MCP 服务器配置指南](/zh/posts/ai/2026-02-28-claude-code-mcp-setup/)。

**我推荐的 MCP 组合：**

- **Context7** —— 实时库文档查询（告别 AI 编造的 API）
- **PostgreSQL/MySQL** —— 调试时让 Claude Code 直接查询数据库
- **Playwright** —— 端到端测试的浏览器自动化
- **Sentry** —— 将错误报告直接拉入 AI 上下文

#### Hooks：确定性自动化

Hooks 让你定义在 Claude Code 操作前后自动执行的规则。与提示词不同（AI 可能会忽略），Hooks 是**确定性的**——它们必定会执行。

在项目中创建 `.claude/hooks.json`：

```json
{
  "hooks": {
    "preCommit": {
      "command": "npm run lint && npm run typecheck",
      "description": "Run lint and type checks before any commit"
    },
    "postFileEdit": {
      "pattern": "*.test.ts",
      "command": "npm run test -- --related",
      "description": "Run related tests after editing test files"
    }
  }
}
```

完整的 Hooks 使用指南请参阅 [Claude Code Hooks 指南](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/)。

### Cursor：你的 AI 编码引擎

Claude Code 负责深度思考，Cursor 负责快速输出。它是你实际写代码的 IDE——行内补全、Agent 模式处理较大改动、聊天面板用于快速提问。

#### 关键设置

打开 Cursor 设置（macOS 上 `Cmd+,`）并配置：

```json
{
  "cursor.agent.model": "claude-sonnet-4-20250514",
  "cursor.autocomplete.enabled": true,
  "cursor.chat.defaultModel": "claude-sonnet-4-20250514",
  "editor.fontSize": 14,
  "editor.minimap.enabled": false,
  "terminal.integrated.fontSize": 13
}
```

**模型选择建议**：大多数 Agent 任务使用 Claude Sonnet（速度快且能力强）。遇到复杂的架构决策或需要最高推理质量时，切换到 Claude Opus。

#### .cursorrules 文件

类似于 CLAUDE.md，项目根目录下的 `.cursorrules` 文件用于配置 Cursor 的行为：

```
You are an expert TypeScript/React developer working on a production application.

## Code Style
- Use TypeScript strict mode
- Prefer named exports over default exports
- Use Zod for runtime validation
- Use React Query for server state management

## Project Structure
- Components: src/components/{feature}/{ComponentName}.tsx
- Hooks: src/hooks/use{HookName}.ts
- API routes: src/routes/{resource}.routes.ts

## Rules
- Never use `any` type — use `unknown` and narrow
- All API responses go through the response utility
- Components must have displayName for debugging
- Prefer composition over inheritance
```

#### Agent 模式工作流

Cursor 的 Agent 模式（`Cmd+I` 或 Composer 面板）是其实现能力的核心：

1. 在 Composer 上下文中选择相关文件
2. 描述你想要的变更
3. 在接受前审查 diff
4. 运行测试验证

**进阶技巧**：用 Claude Code 规划好一个功能后，把方案粘贴到 Cursor 的 Agent 模式中。Claude Code 的详细方案能直接转化为高质量的 Cursor 实现。

### 终端配置：粘合层

你的终端是 Claude Code 运行的地方，优化终端配置收益巨大。

#### tmux / Zellij 配置

使用终端复用器来维护持久化的 AI 会话：

```bash
# ~/.tmux.conf — AI 开发布局
# 前缀键
set -g prefix C-a
unbind C-b

# 创建 AI 开发布局
# Pane 0: Claude Code 会话
# Pane 1: 运行开发服务器
# Pane 2: Git 操作
bind-key A split-window -h \; \
  split-window -v \; \
  select-pane -t 0 \; \
  send-keys 'claude' C-m \; \
  select-pane -t 1 \; \
  send-keys 'npm run dev' C-m \; \
  select-pane -t 2

# 增大回滚缓冲区以容纳 AI 输出
set -g history-limit 50000

# 更好的复制模式，方便复制 AI 响应
setw -g mode-keys vi
```

如果你更喜欢现代化的替代方案，Zellij 提供了类似的体验，配置格式更加友好：

```kdl
// ~/.config/zellij/layouts/ai-dev.kdl
layout {
    pane split_direction="vertical" {
        pane size="60%" {
            command "claude"
            name "AI Agent"
        }
        pane split_direction="horizontal" {
            pane {
                command "npm"
                args "run" "dev"
                name "Dev Server"
            }
            pane {
                name "Git / Shell"
            }
        }
    }
}
```

#### AI 工具的 Shell 别名

添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
# ===== AI 开发别名 =====

# Claude Code 快捷命令
alias cc="claude"
alias ccc="claude --continue"        # 继续上次对话
alias ccr="claude --resume"          # 恢复特定会话
alias ccp="claude --print"           # 单次模式（非交互式）
alias ccm="claude --model opus"      # 复杂任务用 Opus
alias ccs="claude --model sonnet"    # 快速任务用 Sonnet

# 常用 Claude Code 任务
alias ccplan="claude 'Read the codebase and create an implementation plan for:'"
alias cctest="claude 'Write comprehensive tests for the changes in the last commit'"
alias ccreview="claude 'Review the code changes in the current branch and suggest improvements'"
alias ccfix="claude 'Fix the failing tests and lint errors'"
alias ccdoc="claude 'Generate documentation for the public API in this project'"

# Git + AI 工作流
alias gaic="claude 'Create a well-formatted commit message for the staged changes and commit them'"
alias gapr="claude 'Create a pull request with a detailed description for the current branch'"

# 项目初始化
alias ainit="cp ~/.dotfiles/templates/CLAUDE.md . && cp ~/.dotfiles/templates/.cursorrules . && echo 'AI config files created'"

# 省钱模式
alias ccheap="claude --model haiku"  # 简单任务用 Haiku
```

#### Claude Code 终端集成

Claude Code 能在任何终端中运行，包括 Cursor 的集成终端。这是多工具工作流的基础：

1. 用 Cursor 打开你的项目
2. 打开集成终端（`Ctrl+` `` ` ``）
3. 在终端中运行 `claude`
4. 现在你同时拥有了 Claude Code（规划）和 Cursor（实现）

这种配置让你永远不用离开编辑器。Claude Code 的推理输出显示在终端面板，Cursor 在编辑器面板处理文件编辑。

### Git：AI 友好的提交工作流

AI 生成的代码需要严格的版本控制。以下是最佳实践的 Git 配置：

```bash
# ~/.gitconfig AI 开发相关配置

[alias]
    # AI 辅助提交：暂存所有文件，让 AI 写提交信息
    aic = "!f() { git add -A && claude --print 'Write a concise commit message for these changes. Follow conventional commits format.' | git commit -F -; }; f"

    # 提交前用 AI 审查变更
    air = "!f() { git diff --staged | claude --print 'Review this diff. Are there any issues, bugs, or improvements?'; }; f"

    # 用 AI 生成分支描述
    aib = "!f() { git log main..HEAD --oneline | claude --print 'Summarize what this branch does based on the commit history'; }; f"

[commit]
    # 适用于 AI 辅助开发的提交模板
    template = ~/.gitmessage

[diff]
    # 更适合 AI 生成代码的 diff 算法
    algorithm = histogram
```

在 `~/.gitmessage` 创建提交信息模板：

```
# <type>(<scope>): <description>
#
# 类型：feat, fix, refactor, test, docs, chore, perf
# 范围：可选，受影响的模块或区域
#
# 正文：解释"为什么"，而不是"做了什么"（diff 已经展示了"做了什么"）
#
# 脚注：BREAKING CHANGE, Closes #issue
#
# AI 辅助：标注哪些部分是 AI 生成的
```

**AI 开发的分支策略：**

- `main` —— 生产环境，受保护
- `feature/*` —— AI 辅助的功能分支
- 在开始 AI 编程会话之前，总是先创建新分支
- 频繁提交 —— AI 智能体会修改大量文件，小步提交让回滚更容易

## 多工具协作策略

### 什么时候用哪个工具

这个决策矩阵能帮你每天节省大量时间：

| 任务 | 最佳工具 | 原因 |
|------|----------|------|
| 理解陌生代码库 | Claude Code | 超大上下文窗口，深度推理 |
| 规划新功能 | Claude Code | 结构化思考，架构感知 |
| 编写实现代码 | Cursor | 快速补全，行内编辑 |
| 调试复杂问题 | Claude Code | 能读日志、执行命令、跨文件追踪 |
| 快速代码修改 | Cursor | 行内编辑模式更快 |
| 编写测试 | Claude Code | 更擅长覆盖各种边界情况 |
| 代码审查 | Claude Code | 更深入的分析，安全意识更强 |
| 跨文件重构 | Claude Code | Agent 循环处理多文件变更 |
| 修改单个函数 | Cursor | 行内 Agent 模式，即时反馈 |
| 编写文档 | Claude Code | 更擅长结构化的全面文档 |

### Claude Code 规划 + Cursor 实现

这是持续产出最佳结果的工作流：

**第一步：用 Claude Code 规划**

```
你：我需要给 API 加一个限流系统。
    我们用的是 Express.js + Redis。

Claude Code：[阅读代码库，分析中间件链，
             提出基于滑动窗口算法的架构方案，
             找出所有需要保护的路由，
             建议限流追踪的数据库 Schema]
```

**第二步：用 Cursor 实现**

把 Claude Code 的方案交给 Cursor 的 Agent 模式：

```
根据以下方案实现限流系统：
[粘贴 Claude Code 的架构方案]

先从 Redis 限流中间件开始。
```

Cursor 会生成代码文件，你在接受前逐一审查 diff。

**第三步：用 Claude Code 编写测试**

```
你：给我们刚才添加的限流中间件写测试。
    覆盖以下边界情况：窗口过期、并发请求、
    Redis 连接中断。
```

Claude Code 的推理能力能产出比自动补全工具更全面的测试套件。

### 每月 40 美元的最优方案

你不需要在 AI 工具上花几百美元。以下是高性价比的配置：

| 工具 | 方案 | 月费 | 你得到的 |
|------|------|------|----------|
| Claude Code | Max (5x) | $20 | 深度推理，复杂任务 |
| Cursor | Pro | $20 | 快速实现，自动补全 |
| **合计** | | **$40** | **完整 AI 开发工具栈** |

如需详细的 Claude Code 定价分析，请参阅 [Claude Code 价格指南](/zh/posts/ai/2026-02-25-claude-code-pricing/)。

**成本优化技巧：**

- 日常任务使用 Claude Code 的 Sonnet 模型（比 Opus 便宜）
- 只在架构决策和复杂调试时使用 Opus
- 简单补全用 Cursor 的自动补全（比 Agent 模式消耗更少的额度）
- 不主动使用 Claude Code 时关闭会话，避免空闲消耗 Token
- 对于一次性查询，使用 `--print` 模式替代交互式会话

## 你需要的配置文件

以下是完整配置方案中的每个文件，方便直接复制使用。

### CLAUDE.md 模板

前面的模板覆盖了大多数项目。以下是针对特定技术栈的补充部分：

**Python 项目：**

````markdown
## Python 环境
- Python 3.12+，通过 pyenv 管理
- 包管理器：uv（不是 pip）
- 虚拟环境：`.venv/`（由 uv 自动创建）

## 命令
```bash
uv run pytest              # 运行测试
uv run ruff check .        # 代码检查
uv run mypy src/           # 类型检查
uv run python -m src.main  # 运行应用
```

## 代码风格
- 所有函数签名必须有类型标注
- 数据验证使用 Pydantic v2
- 所有 I/O 操作使用异步函数
- 文档字符串使用 Google 格式
````

**Go 项目：**

````markdown
## Go 环境
- Go 1.23+
- Module：github.com/yourorg/yourproject

## 命令
```bash
go test ./...           # 运行所有测试
go vet ./...            # 静态分析
golangci-lint run       # 综合代码检查
go build -o bin/app .   # 构建二进制文件
```

## 规范
- 错误包装：fmt.Errorf("context: %w", err)
- 接口定义放在使用方的包中
- 使用表驱动测试
- 禁止使用 init() 函数
````

### .cursorrules 模板

一个更完善的模板：

```
You are a senior developer working on a production {LANGUAGE} application.

## Response Style
- Be concise. No explanations unless asked.
- Show code changes as diffs when possible.
- If unsure about project conventions, check existing code first.

## Code Quality
- All code must pass the existing linter configuration
- Write tests for new functionality
- Prefer readability over cleverness
- Use existing utilities and helpers before creating new ones

## Architecture
- Follow existing patterns in the codebase
- New files go in the appropriate directory per the project structure
- Database changes require migrations (never modify schema directly)
- API changes require updating the OpenAPI spec

## Forbidden
- Do not use deprecated APIs or libraries
- Do not add new dependencies without explicit approval
- Do not modify CI/CD configuration files
- Do not change environment variable names
```

### Shell 别名合集

终端部分的完整别名集，外加额外的实用工具：

```bash
# ~/.zshrc 或 ~/.bashrc — AI 开发专区

# ===== Claude Code =====
alias cc="claude"
alias ccc="claude --continue"
alias ccr="claude --resume"
alias ccp="claude --print"
alias ccm="claude --model opus"
alias ccs="claude --model sonnet"

# ===== 常用任务 =====
alias ccplan="claude 'Read the codebase and create an implementation plan for:'"
alias cctest="claude 'Write comprehensive tests for the changes in the last commit'"
alias ccreview="claude 'Review the staged changes and suggest improvements'"
alias ccfix="claude 'Fix the failing tests and lint errors'"

# ===== Git + AI =====
alias gaic="claude 'Create a commit message for staged changes and commit'"
alias gapr="claude 'Create a PR description for the current branch'"

# ===== 会话管理 =====
alias ccls="claude sessions list"         # 列出最近会话
alias cclast="claude --resume last"       # 恢复最近一次会话

# ===== 项目初始化 =====
ainit() {
    echo "正在创建 AI 配置文件..."
    [ ! -f CLAUDE.md ] && cp ~/.dotfiles/templates/CLAUDE.md . && echo "  已创建 CLAUDE.md"
    [ ! -f .cursorrules ] && cp ~/.dotfiles/templates/.cursorrules . && echo "  已创建 .cursorrules"
    [ ! -d .claude ] && mkdir -p .claude && echo "  已创建 .claude/"
    echo "完成。请编辑文件以匹配你的项目。"
}
```

### MCP 服务器配置

除了前面展示的基础配置，以下是更完整的 `~/.claude/mcp.json`：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "description": "Real-time library documentation"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"],
      "description": "Browser automation and testing"
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-memory"],
      "description": "Persistent memory across sessions"
    }
  }
}
```

对于数据库连接和其他特定服务的 MCP 服务器，使用项目级配置 `.claude/mcp.json`，避免全局暴露凭据。

## 完整工作流：从想法到上线功能

以下是完整的工作流，逐步展示何时以及如何在工具之间切换。

### 第一步：需求分析（Claude Code）

```bash
# 启动新的 Claude Code 会话
claude

# 提供完整上下文
> 我需要给应用添加邮件通知功能。
> 用户应该能配置通知偏好。
> 技术栈是 Express.js、PostgreSQL 和 React。
> 请分析代码库，提出实现方案。
```

Claude Code 会阅读你的项目结构，理解现有模式，产出详细方案，涵盖数据库变更、API 端点、前端组件和后台任务配置。

**耗时：10-15 分钟**（手动需要 1-2 小时）

### 第二步：架构评审（Claude Code）

```bash
# 继续同一个 Claude Code 会话
> 审查一下这个方案的潜在问题：
> - 与现有的认证中间件兼容吗？
> - 数据库迁移有什么风险？
> - 对 API 限流有什么影响？
```

这是 Claude Code 推理能力大显身手的环节。它会识别冲突、提出改进建议、标记你可能忽略的风险。

### 第三步：编码实现（Cursor）

切换到 Cursor。打开 Agent 模式，粘贴方案：

```
实现邮件通知系统的第一阶段：
1. 创建 notification_preferences 表的数据库迁移
2. 添加 NotificationPreference 模型
3. 创建 CRUD API 路由

[粘贴 Claude Code 方案的相关部分]
```

在接受每个文件变更前审查。Cursor 的 diff 视图让这个过程很快。

### 第四步：编写测试（Claude Code）

回到终端：

```bash
# 继续 Claude Code 会话
claude --continue

> 给我们刚实现的通知偏好 API 写测试。
> 覆盖：CRUD 操作、校验错误、认证要求、
> 数据库约束。
```

### 第五步：集成测试（双管齐下）

```bash
# Claude Code：运行完整测试套件
> 运行测试套件，修复所有失败的用例。

# 然后在 Cursor 中：快速修复剩余问题
# 使用行内编辑模式做精确修改
```

### 第六步：代码审查与 PR（Claude Code）

```bash
> 审查这个分支上的所有变更。
> 然后创建一个带有详细描述的 Pull Request。
```

Claude Code 会分析每个变更的文件，撰写详尽的 PR 描述，并通过 GitHub CLI 创建 PR。

**中等功能的总耗时：2-3 小时**（不用 AI 工具需要 6-8 小时）

这与许多项目的实际效率提升数据吻合：需求分析提速约 40%，架构设计提速约 30%，编码提速约 50%，测试编写提速约 60%。这些数字来自真实的使用追踪，而非基准测试。

## 效率提升技巧

### 上下文管理

上下文是影响 AI 输出质量的最关键因素。以下是管理方法：

**一开始就给全上下文。** 不要让 AI 去猜。如果你在修 bug，把错误信息、相关代码、你已经尝试过的方法全都给出来。

**积极维护 CLAUDE.md。** 当你新增模式或变更规范时及时更新。一份维护良好的 CLAUDE.md 比任何提示词技巧都有价值。

**任务之间清除上下文。** 不相关的任务请启动新的 Claude Code 会话。上一个任务遗留的上下文会干扰 AI，产出更差的结果。

**引用具体文件。** 不要说"修复登录 bug"，而要说"修复 src/middleware/auth.ts 中的认证错误——JWT 验证在 Token 过期时会失败。"

### 会话纪律

养成以下习惯：

1. **一个会话，一个任务。** 不要在同一个 AI 会话中混合功能开发和 Bug 修复。
2. **切换工具前先提交。** 在 Claude Code 和 Cursor 之间切换前保存状态。
3. **审查一切。** AI 生成的代码是初稿。提交前逐行阅读。
4. **增量开发。** 把大功能拆成小步骤。让 AI 完全完成每一步后再进入下一步。这是经验丰富的 AI 开发者一致推荐的"增量开发"原则。
5. **每一步都要人工验证。** 永远不要盲目接受 AI 的输出。验证逻辑、检查边界情况、运行测试。AI 是你的助手，不是你的替代品。

### 成本优化

让你的 AI 工具开支保持高效：

- **模型选择很重要。** 80% 的任务使用 Sonnet。只在真正复杂的问题上使用 Opus——架构决策、隐蔽 Bug、安全审查。
- **单次模式节省 Token。** 对于快速查询，使用 `claude --print "你的问题"` 替代交互式会话。
- **简单任务用紧凑模式。** 只需要快速回答时，使用 Claude Code 的紧凑模式减少上下文加载。
- **批量提问。** 与其开五个会话问五个相关问题，不如在一个会话中全部问完。
- **关闭空闲会话。** 每个活跃的 Claude Code 会话都在内存中维护上下文。用完就关掉。

如需详细的定价策略，请参阅 [Claude Code 定价：方案、成本与优化](/zh/posts/ai/2026-02-25-claude-code-pricing/)。

## 总结

AI 开发环境不只是一堆工具的集合——它是一个**系统**。每个组件相互增强：

- **CLAUDE.md** 确保 Claude Code 理解你的项目，无需每次会话重新解释
- **Shell 别名** 降低使用摩擦，让你真正用起来而不是退回手动操作
- **MCP 服务器** 将 AI 连接到你的真实基础设施
- **Hooks** 强制执行 AI 无法绕过的质量关卡
- **多工具策略** 将每个任务分配给最合适的工具
- **会话纪律** 保持上下文清晰、成本可控

从基础开始——安装 Claude Code 和 Cursor，创建 CLAUDE.md 文件，添加 Shell 别名。然后随着熟练度的提升，逐步加入 MCP 服务器、Hooks 和高级配置。关键是开始建立与 AI 工具协作的肌肉记忆，让它成为你日常工作流的一部分。

2026 年脱颖而出的开发者，不是用最花哨 AI 工具的人，而是搭建了一套**配置得当的环境**，让 AI 辅助变得无缝、可靠且经济高效的人。这篇指南给了你基础，剩下的就是实践了。

## 常见问题

请查看页面顶部的 FAQ 部分，获取关于 AI 开发环境搭建、工具选择、成本和配置的常见问题解答。

## 相关阅读

以下指南对本文涉及的各个主题做了更深入的讲解：

- [Claude Code Guide 2026: Everything You Need to Know](/zh/posts/ai/2026-02-28-claude-code-complete-guide/) — Claude Code 全部功能的完整概览
- [The Complete CLAUDE.md Guide](/zh/posts/ai/2026-02-28-claude-code-claudemd-guide/) — 掌握让 Claude Code 高效工作的配置文件
- [Claude Code MCP Server Setup Guide](/zh/posts/ai/2026-02-28-claude-code-mcp-setup/) — 将 Claude Code 连接到外部服务
- [Claude Code Hooks Guide](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/) — 自动化质量关卡与工作流
- [Claude Code Pricing: Plans, Costs, and Optimization](/zh/posts/ai/2026-02-25-claude-code-pricing/) — 理解成本并优化支出
- [Claude Code vs Cursor: Which AI Coding Tool Should You Use?](/zh/posts/ai/2026-02-28-claude-code-vs-cursor/) — 两款工具的详细对比
- [Codex CLI Deep Dive: Setup, Config, and Power User Tips](/zh/posts/ai/2026-03-10-codex-cli-deep-dive/) — OpenAI 的终端 AI 智能体
- [Google Antigravity Review](/zh/posts/ai/2026-03-10-google-antigravity-review/) — Google 最新的 AI 开发产品
- [What Is Vibe Coding? The AI-First Development Philosophy](/zh/posts/ai/2026-02-28-vibe-coding-explained/) — 理解更广泛的 AI 编程运动
