+++
date = '2026-02-28T08:00:00+08:00'
draft = false
title = 'CLAUDE.md 完全指南：让 AI 每次都精准理解你的项目'
description = '深入掌握 CLAUDE.md 配置方法，让 Claude Code 每次会话都自动获取完整项目上下文。涵盖三层配置体系、实用模板和真实项目案例。'
toc = true
tags = ['Claude Code', 'CLAUDE.md', 'Configuration', 'Best Practices']
categories = ['AI Guides']
keywords = ['CLAUDE.md 指南', 'CLAUDE.md 教程', 'Claude Code 配置', 'Claude Code 项目上下文', 'CLAUDE.md 最佳实践', 'Claude Code 记忆文件', 'CLAUDE.md 模板']
+++

![CLAUDE.md 配置指南——为 Claude Code 提供完美项目上下文](cover.webp)

每次启动新的 Claude Code 会话，你都要重复同样的话："我们用 pnpm，不要用 npm。""遵守 ESLint 规则。""commit 消息用 conventional 格式。""这是一个 Next.js 15 + TypeScript 项目。"

日复一日，会话接会话。

CLAUDE.md 能彻底解决这个问题。它是一个纯 Markdown 文件，Claude Code 会在每次会话开始时自动读取。把项目上下文写一次，Claude 就永远遵守——再也不需要反复提醒。

本指南涵盖全部内容：CLAUDE.md 是什么、三层配置体系、四种管理方式、可直接复制的模板，以及来自真实项目的高级技巧。如果你是 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 新手，建议先阅读我们的[安装指南](/posts/ai/2026-02-25-claude-code-setup-guide/)。

## 什么是 CLAUDE.md？

CLAUDE.md 是 [Claude Code 的记忆文件](https://docs.anthropic.com/en/docs/claude-code/memory)。它是一个标准的 Markdown 文档，放在项目根目录（或其他位置，后面会详细说明），每次启动对话时都会被自动加载到上下文中。

可以这样理解：当新员工入职时，你会给他一份入职文档。CLAUDE.md 就是那份入职文档——只不过新员工是一个 AI 智能体。

### CLAUDE.md 里放什么

- 项目技术栈和架构
- 编码规范和风格规则
- 常用命令（构建、测试、代码检查、部署）
- 目录结构概览
- 工作流说明（Git 规范、PR 流程）
- Claude 反复犯错、你已经厌倦纠正的任何事情

### 什么时候加载？

每次启动 Claude Code 或开始新对话时，它会自动搜索并加载 CLAUDE.md 文件。你不需要提及它、引用它或让 Claude 去读它，这一切自动发生。

Claude Code 还会递归扫描父目录中的 CLAUDE.md 文件。如果你有一个 monorepo，其中包含 `frontend/CLAUDE.md` 和 `backend/CLAUDE.md`，当 Claude 在相应子目录中工作时，会自动加载对应的文件。

### 一个简单示例

以下是一个最简版的 CLAUDE.md，但已经能产生明显效果：

```markdown
# E-commerce API

## Stack
- Node.js 22 + Express + TypeScript
- PostgreSQL + Prisma ORM
- Redis for caching

## Commands
- Dev: pnpm dev
- Test: pnpm test
- Lint: pnpm lint
- Build: pnpm build

## Rules
- Use functional style. No classes except Prisma models.
- All API endpoints must have input validation with Zod.
- Never use console.log in production code. Use the logger utility.
- Commit message format: type: description (e.g., feat: add user auth)
```

仅仅 15 行，写起来只要两分钟，却能在每次会话中省去大量重复解释。

## 三层配置体系

CLAUDE.md 不是单个文件——它是一个为不同作用域设计的三层体系。每一层有不同用途，后面的层会覆盖前面的。

### 第一层：全局配置 — `~/.claude/CLAUDE.md`

这个文件放在你的 home 目录下，适用于你使用 Claude Code 处理的**所有项目**。

**适合放什么：**

- 你的姓名和角色
- 通用编码偏好（注释语言、commit 风格）
- 适用于所有项目的个人习惯

**示例：**

```markdown
# About Me

I'm Alex, a full-stack engineer working primarily with TypeScript and Python.

## Universal Preferences

- Write commit messages in conventional commit format
- Prefer functional programming patterns over OOP
- Keep functions under 40 lines — split if longer
- Use descriptive variable names, never single letters
- When unsure between two approaches, pick the simpler one
```

### 第二层：项目配置 — `./CLAUDE.md`

这个文件放在项目根目录，**会提交到 Git**，所以团队每个成员都共享相同的 AI 上下文。

**适合放什么：**

- 项目专属的技术栈
- 团队编码规范
- 目录结构
- 构建和测试命令
- 架构决策

**示例：**

````markdown
# SaaS Dashboard

## Stack
- Next.js 15 (App Router) + TypeScript 5.7
- Tailwind CSS + shadcn/ui
- Zustand for state management
- Prisma + PostgreSQL

## Project Structure
```
src/
├── app/          # Next.js App Router pages
├── components/   # Reusable components
│   ├── ui/       # Base UI components (shadcn)
│   └── features/ # Business logic components
├── lib/          # Utilities and config
├── hooks/        # Custom React hooks
├── stores/       # Zustand stores
├── types/        # TypeScript type definitions
└── services/     # API client layer
```

## Commands
- Dev: pnpm dev
- Build: pnpm build
- Test: pnpm vitest
- Lint: pnpm lint

## Coding Standards
- File names: kebab-case (e.g., user-profile.tsx)
- Component names: PascalCase (e.g., UserProfile)
- Functions/variables: camelCase (e.g., getUserById)
- Constants: UPPER_SNAKE_CASE (e.g., MAX_RETRY_COUNT)
- All components must be functional with hooks
- Props must have TypeScript interfaces

## Git Rules
- Commit format: type: description
- Types: feat / fix / refactor / docs / test / chore
- Always run pnpm lint before committing
````

### 第三层：个人配置 — `./CLAUDE.local.md`

这个文件也放在项目根目录，但**不提交到 Git**（需要加到 `.gitignore`）。它用于你在特定项目上的个人覆盖配置。

**适合放什么：**

- 与团队标准不同的个人偏好
- 本地环境的特殊情况
- 临时调试笔记
- 正在试验的指令

**示例：**

```markdown
# Personal Overrides

- I'm working on the payment module this sprint — prioritize that context
- My local PostgreSQL runs on port 5433 (not the default 5432)
- When writing tests, add verbose comments — I'm learning the testing patterns
- Draft comments in English first, I'll review before committing
```

### 优先级顺序

当存在多个 CLAUDE.md 文件时，Claude Code 按以下顺序加载：

```
全局 (~/.claude/CLAUDE.md)
  → 项目 (./CLAUDE.md)
    → 个人 (./CLAUDE.local.md)
```

**后加载的文件会覆盖先加载的。** 如果你的全局配置写了"用英文写注释"，但项目配置写了"用西班牙文写注释"，那西班牙文生效。

速查表如下：

| 层级 | 文件路径 | 提交到 Git？ | 作用范围 |
|------|----------|-------------|---------|
| 全局 | `~/.claude/CLAUDE.md` | 不适用 | 所有项目 |
| 项目 | `./CLAUDE.md` | 是 | 当前项目（团队共享） |
| 个人 | `./CLAUDE.local.md` | 否 | 当前项目（仅自己） |

> **注意：** Claude Code 还支持组织级策略文件 `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS）以及 `.claude/rules/*.md` 规则配置。这些属于企业级用法，超出本文范围。

## 四种管理 CLAUDE.md 的方式

你不必每次都从零开始手写 CLAUDE.md。Claude Code 提供了四种方法，分别适用于不同场景。

### 方式一：`/init` — 从项目自动生成

最快的上手方式。在项目目录中运行 Claude Code，然后输入：

```
/init
```

Claude 会分析你的 `package.json`、`tsconfig.json`、`.eslintrc`、目录结构和其他配置文件，然后自动生成一份 CLAUDE.md 草稿。

**优点：** 速度快，能准确捕捉你的实际技术栈。

**缺点：** 输出比较通用，你需要手动添加团队特有的规则和工作流说明。

**适用场景：** 新项目，或首次为已有项目添加 CLAUDE.md。

### 方式二：`#` 语法 — 随时添加规则

在任何对话中，输入以 `#` 开头的内容就能将规则追加到 CLAUDE.md：

```
# Always handle loading and error states in API calls
```

Claude 会立即将这条规则添加到你的项目 CLAUDE.md 中。

**优点：** 零摩擦——想到就加。

**缺点：** 规则会越积越多且缺乏组织，需要定期清理。

**适用场景：** 你发现 Claude 总是犯同样的错误，一次修正、永久记住。

### 方式三：`/memory` — 可视化编辑器

输入 `/memory` 打开交互界面，可以查看和编辑 CLAUDE.md 的内容。你可以选择编辑哪一层（全局、项目或个人）。

**优点：** 一览全局，方便重新组织和清理。

**缺点：** 需要暂时离开编码流程。

**适用场景：** 定期维护——重新组织、删除过时规则、调整结构。

### 方式四：`@` 引用 — 模块化配置

当 CLAUDE.md 变得过长时，可以拆分成多个文件并用 `@` 引用：

```markdown
# Project Config

@docs/architecture.md
@docs/api-conventions.md
@docs/testing-guide.md
@AGENTS.md
```

Claude Code 会读取引用的文件并将其内容纳入上下文。

**优点：** 保持 CLAUDE.md 简短有序，每个引用文件可以独立维护。

**缺点：** 需要管理更多文件，引用的文件必须存在于指定路径。

**适用场景：** 大型项目、monorepo，或 CLAUDE.md 超过 200 行时。

## 可直接复制的模板

以下三个开箱即用的模板，选择适合你情况的，修改具体内容即可。

### 模板一：个人开发者（全局配置）

放在 `~/.claude/CLAUDE.md`：

```markdown
# Developer Profile

I'm [Your Name], a [your role] working with [primary languages].

## Coding Preferences

- Prefer functional programming over OOP
- Variable names must be descriptive — no a, b, temp
- Keep functions under 40 lines
- Code should be self-documenting; minimize comments
- When adding comments, make them explain "why", not "what"

## Workflow

- Run lint before every commit
- Commit frequently in small increments
- No TypeScript errors allowed before committing
- Write tests for any non-trivial business logic

## Things I Dislike

- Over-engineering and unnecessary abstractions
- Design patterns used for the sake of patterns
- Deeply nested callbacks or promises (use async/await)
- Magic numbers — extract to named constants
```

### 模板二：团队项目（项目配置）

放在项目根目录的 `./CLAUDE.md`：

`````markdown
# [Project Name]

[One-line description of what this project does]

## Stack

- Framework: Next.js 15 (App Router)
- Language: TypeScript 5.7 (strict mode)
- Styling: Tailwind CSS + shadcn/ui
- State: Zustand
- Database: PostgreSQL + Prisma
- Testing: Vitest + Testing Library
- Package manager: pnpm

## Directory Structure

```
src/
├── app/          # Pages and layouts (App Router)
├── components/   # Reusable UI components
├── lib/          # Utilities, helpers, config
├── hooks/        # Custom React hooks
├── stores/       # Zustand state stores
├── types/        # Shared TypeScript types
└── services/     # API client functions
```

## Commands

```bash
pnpm dev          # Start dev server
pnpm build        # Production build
pnpm test         # Run tests
pnpm lint         # Lint check
pnpm db:push      # Push schema to database
pnpm db:migrate   # Run database migrations
```

## Coding Rules

- Use functional components with hooks. No class components.
- Props must have TypeScript interfaces, named [Component]Props.
- File names: kebab-case. Component names: PascalCase.
- All API calls must handle loading and error states.
- No `any` type. Use `unknown` if the type is truly unknowable.
- Sensitive values in .env.local only. Never commit secrets.

## Git Conventions

- Commit format: `type: short description`
- Types: feat | fix | refactor | docs | test | chore
- Branch naming: feature/description or fix/description
- Always run `pnpm lint` before committing
- New features require unit tests

## Important Notes

- This is a multi-tenant SaaS app. All database queries MUST filter by tenantId.
- Never import from `node_modules` directly — use the re-exports in `lib/`.
- Rate limiting is handled by middleware. Do not add rate limiting in individual routes.
`````

### 模板三：Python 后端（项目配置）

放在 Python 项目根目录的 `./CLAUDE.md`：

`````markdown
# [Project Name]

[One-line description]

## Stack

- Python 3.12 + FastAPI
- SQLAlchemy 2.0 + Alembic for migrations
- PostgreSQL 16
- Redis for caching and task queue
- Celery for background tasks
- Poetry for dependency management

## Project Structure

```
src/
├── api/           # FastAPI route handlers
│   └── v1/        # Versioned endpoints
├── core/          # App config, security, dependencies
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic request/response schemas
├── services/      # Business logic layer
├── tasks/         # Celery background tasks
└── utils/         # Helper functions
tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── conftest.py    # Shared fixtures
```

## Commands

```bash
poetry install              # Install dependencies
poetry run uvicorn src.main:app --reload  # Dev server
poetry run pytest           # Run all tests
poetry run pytest -x -v     # Run tests, stop on first failure
poetry run alembic upgrade head  # Apply migrations
poetry run black .          # Format code
poetry run ruff check .     # Lint
```

## Coding Rules

- Follow PEP 8. Use Black for formatting (line length 88).
- All functions must have type hints.
- Docstrings use Google style.
- Use Pydantic for all request/response validation.
- Service layer handles business logic. Routes are thin — validate, call service, return response.
- All database operations go through the repository pattern in services/.

## Testing Rules

- Every endpoint needs at least one happy-path and one error-path test.
- Use pytest fixtures for database setup/teardown.
- Mock external API calls. Never make real HTTP requests in tests.
`````

## CLAUDE.md 与 README.md 的区别

这两个文件看起来相似，但面向的受众完全不同。把它们混淆是开发者最常犯的错误之一。

| 维度 | README.md | CLAUDE.md |
|------|-----------|-----------|
| **受众** | 人类开发者 | AI 智能体（Claude Code） |
| **目的** | 解释项目是什么 | 指导如何在项目中工作 |
| **语气** | 描述性、解释性 | 命令式、直接 |
| **内容** | 是什么、为什么、如何开始 | 必须做、禁止做、怎么做 |
| **格式** | 表格、图表、徽章、链接 | 精简列表、代码块、规则 |
| **优化方向** | 便于人类扫读 | 对 LLM 的 token 效率友好 |

### 同一主题，两种不同写法

以"技术栈"为例。

**README.md** — 为人类快速浏览格式化：

```markdown
| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React + TypeScript | 19.x / 5.7 |
| Backend | FastAPI + SQLAlchemy | 0.115 / 2.0 |
| Database | PostgreSQL | 16 |
| Cache | Redis | 7.x |
```

**CLAUDE.md** — 为 token 效率压缩：

```markdown
- Frontend: React 19 + TypeScript 5.7 + Vite 6
- Backend: FastAPI 0.115 + SQLAlchemy 2.0 + PostgreSQL 16 + Redis 7
```

相同的信息，不同的包装方式。

### 内容边界

| 内容 | README.md | CLAUDE.md |
|------|:---------:|:---------:|
| 这个项目是什么？ | 是 | 否 |
| 技术栈/版本 | 是（表格） | 是（精简列表） |
| 如何入门 | 是（分步骤） | 否 |
| 构建/测试命令 | 是（详细） | 是（一个代码块） |
| 环境要求 | 是 | 否 |
| Git commit 规范 | 否 | 是 |
| 编码标准 | 否 | 是 |
| 测试规则 | 否 | 是 |
| 开发工作流 | 否 | 是 |
| 架构概览 | 是 | 简短指引 |
| 许可证 | 是 | 否 |

**经验法则：** README 回答"这是什么？"，CLAUDE.md 回答"我应该怎么干活？"

## CLAUDE.md 与 AGENTS.md 的关系

业界正在推动一个标准化方案，让 AI 智能体统一接收项目上下文，这就是 AGENTS.md。

### 什么是 AGENTS.md？

AGENTS.md 是一个跨工具标准，用于向 AI 编码智能体提供项目指令。最初在 2025 年中提出，目前由 Linux 基金会下属的 Agentic AI Foundation 管理。

截至 2026 年初，支持 AGENTS.md 的工具包括：

- **OpenAI Codex CLI**
- **Google Gemini CLI**
- **GitHub Copilot**
- **Cursor**
- **Windsurf**
- **Devin**
- **[Claude Code](https://github.com/anthropics/claude-code)**（通过 `@` 引用）
- 以及 20 多个其他工具

已有超过 60,000 个开源仓库采用了 AGENTS.md。

### CLAUDE.md vs AGENTS.md：何时用哪个

| 场景 | 建议 |
|------|------|
| 团队只使用 Claude Code | CLAUDE.md 就够了 |
| 团队使用多种 AI 工具 | 以 AGENTS.md 为主要配置源 |
| 开源项目 | AGENTS.md（兼容性最广） |
| 需要 Claude 专属指令 | CLAUDE.md 放 Claude 专属规则 + AGENTS.md 放通用规则 |

### 如何同时使用两者

最常见的做法是将主要指令写在 AGENTS.md 中，然后让 CLAUDE.md 引用它：

```markdown
See @AGENTS.md
```

就这么简单。CLAUDE.md 一行话，所有指令放在 AGENTS.md 里。这样 Cursor 直接读 AGENTS.md，Copilot 直接读 AGENTS.md，Claude Code 通过 `@` 引用来读取。

你也可以创建符号链接：

```bash
# 所有内容写在 AGENTS.md，为 Claude Code 创建符号链接
ln -s AGENTS.md CLAUDE.md
```

如果你需要 Claude 专属规则（比如 Skill 引用或 Claude 特有的工作流指令），把这些放在 CLAUDE.md 中，通用规则放在 AGENTS.md：

```markdown
# Claude-Specific Config

See @AGENTS.md

## Claude-Only Rules
- Use /compact when context gets long
- Prefer Sonnet for routine tasks, switch to Opus for architecture decisions
- When writing Skills, follow the pattern in .claude/skills/
```

## 编写原则：如何写出高效的 CLAUDE.md

写得差的 CLAUDE.md 可能比没有更糟。以下是区分有效配置和噪音的原则。

### 1. 控制在 300 行以内

研究表明，LLM 能可靠遵循大约 150-200 条独立指令。Claude Code 的系统提示已经占用了约 50 个位置，留给你的最多 150 条——而大多数项目需要的远少于此。

如果 CLAUDE.md 超过 300 行，用 `@` 引用拆分。主文件保持为简洁的索引。

### 2. 使用祈使句

写指令，不要写描述。

| 差（描述性） | 好（祈使式） |
|---|---|
| "项目使用 TypeScript 严格模式" | "使用 TypeScript 严格模式" |
| "我们倾向于使用函数式组件" | "使用函数式组件，禁止 class 组件。" |
| "最好能有测试" | "为所有新端点编写测试" |
| "团队一般遵循..." | "遵循 conventional commit 格式" |

Claude 是一个执行指令的智能体，不是阅读文档的同事。直接了当。

### 3. 不要重复 linter 已有的规则

如果你的 `.eslintrc` 已经强制 2 空格缩进，就不要在 CLAUDE.md 中重复。Claude Code 会自动读取项目的 linter 配置文件。

**不要放在 CLAUDE.md 中：**
- 缩进规则（Prettier/ESLint 处理）
- import 排序（eslint-plugin-import 处理）
- 尾逗号（Prettier 处理）
- 行宽限制（Black/Prettier 处理）

**应该放在 CLAUDE.md 中：**
- 架构模式（"数据库访问使用 repository 模式"）
- 业务逻辑规则（"所有查询必须按 tenantId 过滤"）
- 工作流指令（"提交前运行测试"）
- linter 无法强制的命名规范

### 4. 大型配置使用 @ 引用

保持 CLAUDE.md 像简洁的目录，详细文档放到其他地方：

```markdown
# Project Config

## Architecture
@docs/architecture.md

## API Conventions
@docs/api-conventions.md

## Testing Guide
@docs/testing-guide.md
```

每个引用文件应聚焦一个主题，可独立维护。

### 5. 测试你的规则

写完 CLAUDE.md 后，问 Claude 一个应该触发你某条规则的问题。如果它没有遵循，说明指令可能太模糊或埋得太深。

比如，如果你的 CLAUDE.md 写了"所有 API 端点必须使用 Zod 验证输入"，就让 Claude 创建一个新端点。它有没有包含 Zod 验证？如果没有，就重写规则，让它更醒目或更具体。

### 6. 强调关键规则

对于绝对不能违反的规则，增加强调：

```markdown
- IMPORTANT: All database queries MUST filter by tenantId. No exceptions.
- NEVER commit .env files or API keys to Git.
- YOU MUST run the test suite before creating any pull request.
```

`IMPORTANT`、`MUST`、`NEVER`、`ALWAYS` 这类词能提高关键指令的遵循率。

## 高级技巧

### Monorepo 的模块化配置

在 monorepo 中，不同目录可能有不同的规范。使用子目录 CLAUDE.md 文件：

```
my-monorepo/
├── CLAUDE.md              # 共享规则（Git 规范、CI）
├── frontend/
│   ├── CLAUDE.md          # React/TypeScript 规则
│   └── src/
├── backend/
│   ├── CLAUDE.md          # Python/FastAPI 规则
│   └── src/
└── infra/
    ├── CLAUDE.md          # Terraform/AWS 规则
    └── modules/
```

Claude Code 会加载根目录的 CLAUDE.md，再加上它正在处理的文件所在子目录的 CLAUDE.md。

### CLAUDE.md + Skills 组合

CLAUDE.md 定义环境，[Skills](/posts/ai/2026-02-28-claude-code-skills-guide/) 定义特定任务的工作流。它们是互补关系。

**CLAUDE.md** 设定标准：

```markdown
## Code Review Standards
- All new code must have unit tests
- No console.log in production code
- No hardcoded configuration values
- Functions must have JSDoc comments
```

**一个 Skill** 定义审查流程：

```markdown
---
name: code-review
description: Review code changes against project standards
---

# Code Review Skill

1. Read git diff for staged changes
2. Check each file against the Code Review Standards in CLAUDE.md
3. List violations with file, line, and suggested fix
4. Summarize: total issues found, severity breakdown
```

Skill 会自动引用 CLAUDE.md 中的规则——无需重复。更多关于组合使用的内容，请参阅我们的 [Skills 指南](/posts/ai/2026-02-28-claude-code-skills-guide/)。

### CLAUDE.md + Hooks 集成

[Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) 让你在 Claude Code 操作前后自动执行动作。你的 CLAUDE.md 可以引用 hook 行为：

```markdown
## Automated Checks
- Pre-commit hooks run ESLint and Prettier automatically
- Post-save hooks run the test suite for changed files
- See .claude/settings.json for hook configuration
```

这样能告诉 Claude 哪些检查已经自动化了，避免它手动重复执行。

### 团队最佳实践

1. **把 CLAUDE.md 提交到 Git。** 它是团队基础设施，就像 `.eslintrc` 或 `tsconfig.json` 一样。每个人都应该共享相同的 AI 上下文。

2. **把 CLAUDE.local.md 加入 .gitignore。** 个人偏好不应该强加给队友。

3. **在 PR 中审查 CLAUDE.md 的变更。** 当有人添加规则时，团队应该达成一致——就像修改 linter 规则一样。

4. **定期更新。** 项目演进时更新 CLAUDE.md。Claude 反复犯同样的错时添加规则。规则过时时删除它。

5. **用于新成员入职。** 你的 CLAUDE.md 对人类也有用。新开发者可以通过阅读它快速了解编码规范和工作流——即使他们不用 Claude Code。

## 常见错误

### 错误一：写成长篇小说

500 行的 CLAUDE.md，里面塞满了项目历史、设计哲学和会议记录。Claude 不需要你的背景故事，它需要的是指令。

**修正：** 大刀阔斧地删减。对每一行问自己："如果我删掉这行，Claude 写出的代码会更差吗？"如果答案是否，就删掉。

### 错误二：太模糊

"写干净的代码"或"遵循最佳实践"这类规则毫无意义。Claude 本来就在尝试写干净的代码。模糊的指令浪费 token 却不改变行为。

**修正：** 让规则具体且可验证。不要写"写干净的代码"，而要写"函数不超过 30 行。重复逻辑提取为辅助函数。"

### 错误三：把 README 的内容混进 CLAUDE.md

大段解释项目是做什么的、为什么创建、面向谁。Claude 不需要被说服——它需要被指挥。

**修正：** 项目描述放在 README.md 里。CLAUDE.md 只放可执行的指令。

### 错误四：重复 linter 规则

把每条 ESLint 或 Prettier 规则都列在 CLAUDE.md 中。Claude Code 已经会读取你的 linter 配置文件了。

**修正：** 只放 linter 无法强制的规则：架构模式、业务逻辑约束和工作流指令。

### 错误五：写完就忘

写了一次 CLAUDE.md 就再也不管了。半年后技术栈变了，规范演进了，一半的指令已经过时。

**修正：** 把"审查 CLAUDE.md"加入 sprint 回顾的检查清单。删除过时规则，添加新模式的规则。

### 错误六：忘了 CLAUDE.local.md

把个人偏好放在共享的 CLAUDE.md 里，导致队友之间产生冲突。

**修正：** 共享标准放 CLAUDE.md，个人偏好放 CLAUDE.local.md。把 `CLAUDE.local.md` 加入 `.gitignore`。

## 快速入门清单

不知道从哪里开始？按以下步骤操作：

1. **在项目中运行 `/init`** — 获得一个自动生成的起点
2. **审查和精简** — 删除 Claude 自己能搞明白的内容
3. **添加团队规则** — 编码规范、Git 约定、架构约束
4. **添加常用命令** — 构建、测试、代码检查、部署
5. **添加关键规则** — 必须遵循的业务逻辑不变量
6. **测试它** — 让 Claude 做一个任务，验证它是否遵循你的规则
7. **提交它** — `git add CLAUDE.md && git commit -m "feat: add CLAUDE.md"`
8. **创建 `.gitignore` 条目** — 添加 `CLAUDE.local.md` 用于个人覆盖
9. **设置全局配置** — 把通用偏好添加到 `~/.claude/CLAUDE.md`
10. **持续维护** — 每月审查，项目演进时更新

## 相关阅读

如果你正在搭建完整的 Claude Code 工作流，以下指南涵盖了其他模块：

- **[Claude Code 安装指南 2026](/posts/ai/2026-02-25-claude-code-setup-guide/)** — 安装、认证和首次项目配置
- **[Claude Code 定价 2026](/posts/ai/2026-02-25-claude-code-pricing/)** — 了解成本、选择合适方案、优化 token 用量
- **[Claude Code 十大常见错误](/posts/ai/2026-02-25-claude-code-mistakes/)** — 常见陷阱及避坑方法（第一个错误就是不写 CLAUDE.md）
- **[Claude Code Hooks 指南](/posts/ai/2026-02-28-claude-code-hooks-guide/)** — 在 Claude Code 操作前后自动执行动作
- **[Claude Code Skills 指南](/posts/ai/2026-02-28-claude-code-skills-guide/)** — 构建可复用的任务工作流，与 CLAUDE.md 互补

---

CLAUDE.md 是那种花 10 分钟配置、能持续收益数月的功能。有良好 CLAUDE.md 和没有的 Claude Code 用户之间，差距是显而易见的：更少的纠正、更一致的代码、更少的 token 浪费，以及更顺畅的工作流。

写一次，保持更新，剩下的交给 Claude。
