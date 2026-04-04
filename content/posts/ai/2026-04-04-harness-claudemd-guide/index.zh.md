+++
date = '2026-04-04T09:00:00+08:00'
draft = false
title = 'CLAUDE.md 怎么写才有效？Harness Engineering 实战篇（附模板）'
description = '基于 ETH Zurich 研究的 CLAUDE.md 写法指南：60 行以内效果最好，AI 生成的冗长版本反而降低 20%。含原则、反模式、三种项目模板和效果度量方法。'
toc = true
tags = ['Harness Engineering', 'Claude Code', 'CLAUDE.md', 'AI Agents', 'AI Engineering']
keywords = ['CLAUDE.md 最佳实践', 'CLAUDE.md 怎么写', 'CLAUDE.md 教程 2026', 'Harness Engineering CLAUDE.md', 'CLAUDE.md 反模式', 'CLAUDE.md 模板', 'ETH Zurich CLAUDE.md 研究', 'Claude Code 配置文件']

[[params.faqItems]]
question = "CLAUDE.md 应该写多长？"
answer = "ETH Zurich 的研究表明，人工编写的 60 行以内文件效果最好。AI 生成的长文件（200 行以上）反而让 Agent 表现下降 20%，同时增加 token 开销。核心原则：每一行都必须能防止一个真实错误。如果删掉某行不会导致 Claude 犯错，就果断删掉。"

[[params.faqItems]]
question = "CLAUDE.md 和 AGENTS.md 有什么区别？"
answer = "CLAUDE.md 是 Anthropic 为 Claude Code 定制的配置文件，支持层级作用域、@import 语法和用户级覆盖。AGENTS.md 是 Linux 基金会旗下 Agentic AI Foundation 推动的开放标准，GitHub 上超过 6 万个仓库在用，兼容 Codex、Cursor、Copilot 等多种工具。如果团队同时用多种 AI 工具，把共享规则放 AGENTS.md，Claude 专属功能放 CLAUDE.md。"

[[params.faqItems]]
question = "能不能用 AI 来生成 CLAUDE.md？"
answer = "不建议。ETH Zurich 测试了 138 个 agentfile，发现 AI 生成的文件成功率反而下降，token 成本增加约 20%。Agent 花了 14-22% 的额外推理 token 来处理冗长指令，却没有提升任务完成率。CLAUDE.md 应该人工编写，基于 Agent 实际犯过的错误来添加规则。"

[[params.faqItems]]
question = "CLAUDE.md 里不该放什么？"
answer = "不要放：代码风格规则（用 linter 代替）、目录结构说明（Agent 自己能读文件系统）、Claude 本来就知道的语言规范、完整的 API 文档（给链接就行）、代码库概述、工具偏好指令。最常见的错误是把 CLAUDE.md 当文档写，但它不是文档——它是约束注入文件。"

[[params.faqItems]]
question = "怎么判断 CLAUDE.md 是否有效？"
answer = "跟踪三个指标：一次成功率（Agent 第一次就做对的比例）、重复纠正率（你是否在多个会话中反复说同样的话）、探索性工具调用数（Agent 开始工作前是否需要大量 find/grep）。有效的 CLAUDE.md 能消除重复纠正，减少探索性调用。"
+++

![简洁的代码编辑器中展示精简的 CLAUDE.md 文件，配合驾驭工程的引导轨道和反馈循环](cover.webp)

这是[驾驭工程系列](/posts/ai/2026-04-04-harness-engineering-guide/)的**第二篇**。第一篇讲了完整框架——什么是驾驭工程、为什么重要、Guide 和 Sensor 的核心概念。这篇深入拆解驾驭系统中最重要的 Guide 组件：`CLAUDE.md` 文件。

核心公式回顾：**Agent = 模型 + 驾驭系统**。驾驭系统是模型之外的一切——工具、约束、反馈循环、配置文件。`CLAUDE.md` 是最核心的前馈控制器，在 Agent 开始生成之前就引导它的行为方向。

大多数 CLAUDE.md 写得不好。不是不用心，而是优化方向错了：该写约束的时候写成了文档，该写具体指令的时候写了一堆 Agent 本来就知道的东西，甚至直接让 AI 生成——结果适得其反。

这篇指南告诉你什么写法真正有效，有研究数据和实战案例支撑。

## ETH Zurich 研究：数据说了什么

2026 年初，ETH Zurich 的研究团队发布了一项[大规模研究](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)，在 Claude Code、Codex、Qwen Code 等多个 AI 编程 Agent 上测试了 138 个 agentfile，覆盖 300 个 SWE-bench Lite 任务和一个 138 任务的新基准 AGENTbench。

结果出人意料：

| 文件类型 | 性能影响 | 成本影响 |
|---------|---------|---------|
| 人工编写、精简（<60 行） | 成功率 +4% | 持平 |
| AI 生成、冗长（200+ 行） | 成功率 -3% | token 成本 +20% |
| 不用 agentfile | 基准线 | 基准线 |

**AI 生成的文件让 Agent 变差了。** Agent 多花了 14-22% 的推理 token 来处理冗长指令，执行步骤更多，调用工具更多——但任务完成率并没有提升。

研究团队的结论很直接：**完全不要用 AI 生成的 agentfile，人工编写的也只保留 Agent 无法自行推断的信息。**

这和[驾驭工程框架](/posts/ai/2026-04-04-harness-engineering-guide/)的预测一致。Guide 的作用是缩小解空间。冗长的文件不是在缩小——是在淹没。一个 Agent 收到 300 行指令，得先花推理算力判断哪些指令跟当前任务相关，留给实际任务的算力就少了。

## 60 行原则

ETH Zurich 的研究、Anthropic 的内部使用数据和社区基准测试指向同一个结论：**CLAUDE.md 控制在 60 行以内。**

这不是拍脑袋的数字，背后是 LLM 处理上下文的机制：

1. **注意力是有限的。** CLAUDE.md 的每一行都在和任务相关的上下文争夺注意力权重。
2. **精准胜过数量。** 一条精确的约束比十条模糊的建议能防止更多错误。
3. **约束会相互稀释。** 每多一行不必要的内容，所有其他行获得的关注度都在降低。

### 石蕊测试

对 CLAUDE.md 的每一行，问自己：**"删掉这行，Claude 会犯一个具体的、可观察到的错误吗？"**

如果答案是"不会"，删掉。要狠。

通过测试的行：
- `Use pnpm, not npm`（Claude 默认用 npm）
- `All API responses use shared Result<T> type`（Claude 无法推断）
- `Tests live next to source: foo.ts → foo.test.ts`（项目特定惯例）

没通过测试的行：
- `Write clean, well-documented code`（Claude 本来就这么做）
- `Follow best practices`（太模糊，约束不了任何事）
- `This is a TypeScript project using React`（Claude 看一眼代码就知道）

## 该放什么，不该放什么

### 该放：Agent 无法自行推断的具体信息

```markdown
## Commands
- `pnpm test` — run tests (not npm test)
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — strict TypeScript

## Conventions
- All API handlers return Result<T, AppError> type
- Database migrations use reversible format (up + down)
- Commit messages follow Conventional Commits
- Feature branches: feat/description, bug fixes: fix/description

## Architecture Decisions
- No circular imports between modules (enforced by eslint-plugin-import)
- Frontend never imports from backend directly — use shared types package
- All external API calls go through src/lib/api-client.ts
```

### 不该放：Claude 已经知道的东西

| 类别 | 例子 | 为什么不该放 |
|------|------|------------|
| 语言基础 | "Use TypeScript strict mode" | Claude 读 tsconfig.json 就知道 |
| 框架惯例 | "Use React hooks, not class components" | Claude 了解现代 React |
| 通用建议 | "Write unit tests for critical code" | 太模糊，没有可执行的约束 |
| 目录列表 | "src/ contains source code" | Claude 能读文件系统 |
| 代码库概述 | "This app has a frontend and backend" | Claude 从文件结构就能推断 |
| 工具偏好 | "Use grep to search" | Claude 自己会选合适的工具 |

### 反模式大赏

以下是生产环境中见过的真实反模式：

**反模式一：文档倾倒**

```markdown
# 差：247 行项目文档
## Project Overview
This is a full-stack e-commerce application built with Next.js 14,
using the App Router pattern with React Server Components...
[再来 200 多行架构描述]
```

失败原因：这是 README，不是指令文件。Claude 从代码就能推断架构。你用 247 行上下文预算传达了零个可操作的约束。

**反模式二：AI 生成的宣言**

```markdown
# 差：让 AI "帮我写个 CLAUDE.md"
## Code Quality Standards
- Write clean, maintainable code following industry best practices
- Use meaningful variable names that clearly convey purpose
- Add comprehensive comments for complex logic
- Ensure proper error handling throughout the codebase
- Follow the DRY principle to avoid code duplication
```

失败原因：每一行都是 Claude 默认就会做的事。这个文件信号量为零，却占了注意力预算。ETH Zurich 的研究发现这类文件让性能**下降** 3%。

**反模式三：万能文件**

```markdown
# 差：500+ 行，什么都塞进去
## Database
[40 行数据库惯例]
## Authentication
[30 行认证模式]
## Deployment
[25 行部署流程]
## API Design
[35 行 REST 惯例]
## Testing
[50 行测试策略]
...
```

失败原因：什么都重要就等于什么都不重要。Agent 无法区分关键约束和可有可无的偏好。应该用 [Skills 做渐进式披露](/posts/ai/2026-01-08-claudecode-skill-guide/)。

## 渐进式披露：用 Skills 分层

"我的 CLAUDE.md 太长了"的解法不是"写短一点"，而是**把领域知识迁移到按需加载的 Skills 里**。

这就是[驾驭工程](/posts/ai/2026-04-04-harness-engineering-guide/)中的渐进式披露模式：

```
CLAUDE.md（始终加载，<60 行）
  → 全局约束
  → 构建/测试命令
  → 关键架构决策

Skills（按需加载）
  → 数据库迁移规则
  → API 设计规范
  → 部署流程
  → 测试惯例
```

### 实际操作

你的 CLAUDE.md 保持精简：

```markdown
# CLAUDE.md

## Project
- TypeScript monorepo, pnpm workspaces
- React frontend (packages/web), Express backend (packages/api)

## Commands
- `pnpm test` — run all tests
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — TypeScript strict mode

## Critical Rules
- All API responses use Result<T, AppError>
- No direct database queries outside packages/db
- Never modify shared types without running full test suite
```

领域知识放到 Skills 里：

```markdown
# .claude/skills/database-migration.md
---
name: database-migration
description: Rules for creating or modifying database migrations
---

## Migration Rules
- Always create reversible migrations (up + down)
- Use transactions for DDL changes
- Never modify an existing migration file — create a new one
- Test against production schema copy before merging
- Migration files: YYYYMMDDHHMMSS_description.ts
```

Claude 处理数据库迁移时，这个 Skill 自动加载。处理前端组件时，数据库规则不会占用上下文。Agent 的上下文窗口保持干净，每条指令在相关的时候才获得完整的注意力。

关于 Skills 的详细用法，参考 [Claude Code Skills 指南](/posts/ai/2026-01-08-claudecode-skill-guide/)和 [Skill 模式大全](/posts/ai/2026-01-12-claudecode-skill-patterns/)。

## CLAUDE.md 与 AGENTS.md：什么时候用哪个

2025 年以来，生态里有两套 Agent 指令文件标准：

| 特性 | CLAUDE.md | AGENTS.md |
|------|-----------|-----------|
| **适用范围** | 仅 Claude Code | 任何 AI 编程工具 |
| **标准组织** | Anthropic | Linux 基金会（Agentic AI Foundation） |
| **采用规模** | Claude Code 原生 | GitHub 6 万+ 仓库 |
| **层级作用域** | 支持（根目录、子目录、用户级） | 部分（仅子目录） |
| **导入系统** | `@import` 语法，支持递归 | 无 |
| **用户级覆盖** | `~/.claude/CLAUDE.md` | 无 |
| **本地文件（不提交）** | `.claude/CLAUDE.local.md` | 无 |

### 实用规则

团队**只用 Claude Code**：全部放 CLAUDE.md。

团队**同时用多种 AI 工具**（Cursor、Copilot、Codex 等）：共享规则放 AGENTS.md，Claude 专属功能放 CLAUDE.md：

```markdown
# CLAUDE.md
See @AGENTS.md for shared project conventions.

## Claude-Specific
- Use sub-agents for codebase exploration tasks
- Prefer Sonnet for test generation, Opus for architecture decisions
- Run typecheck hook after every file edit
```

很多成熟的开源项目已经在用这种模式——共享规则放 AGENTS.md，Claude 专属配置放 CLAUDE.md，各取所需。

更深入的对比参考 [CLAUDE.md vs README.md](/posts/ai/2026-01-31-claudemd-vs-readme/)。

## 常见项目模板

### Monorepo（TypeScript）

```markdown
# CLAUDE.md — 28 行

## Project
- TypeScript monorepo, pnpm workspaces
- Packages: web (React), api (Express), shared (types + utils), db (Prisma)

## Commands
- `pnpm test` — all tests
- `pnpm test --filter=web` — frontend tests only
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — TypeScript strict

## Rules
- Cross-package imports only through package.json exports
- Shared types in packages/shared — never duplicate
- API handlers return Result<T, AppError>
- No circular dependencies (enforced by eslint-plugin-import)

## Testing
- Unit tests next to source: foo.ts → foo.test.ts
- Integration tests in __tests__/ at package root
- Mock external services, never real API calls in tests

## Git
- Conventional commits (feat:, fix:, refactor:, test:, docs:)
- One PR per feature, squash merge to main
```

### API 服务（Python）

```markdown
# CLAUDE.md — 24 行

## Project
- Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic migrations
- Package manager: uv (not pip)

## Commands
- `uv run pytest` — run tests
- `uv run ruff check .` — linting
- `uv run mypy .` — type checking
- `uv run alembic upgrade head` — apply migrations

## Rules
- All endpoints return ResponseModel[T] wrapper
- Database access only through repository pattern (src/repos/)
- Environment variables via pydantic-settings, never os.getenv
- New endpoints need: handler, schema, test, OpenAPI docstring

## Migrations
- Always reversible (upgrade + downgrade)
- One migration per PR
- Never edit existing migrations
```

### 前端应用（React）

```markdown
# CLAUDE.md — 22 行

## Project
- React 19, TypeScript, Vite, Tailwind CSS 4
- State: Zustand for global, React Query for server state

## Commands
- `npm run dev` — dev server (port 3000)
- `npm test` — Vitest
- `npm run lint` — ESLint + Prettier
- `npm run typecheck` — tsc --noEmit

## Rules
- Components in src/components/, one component per file
- Custom hooks in src/hooks/, prefixed with use*
- No inline styles — Tailwind classes only
- Server state through React Query, never useEffect + fetch
- All user-facing text through i18n (src/i18n/)

## Testing
- Component tests with Testing Library
- Mock API calls with MSW, never fetch mocking
```

注意共同点：每个模板**不超过 30 行**，只包含**无法自行推断的具体信息**，聚焦于**防止真实错误的约束**。

## 配置加载层级

Claude Code 从多个位置加载 CLAUDE.md，按特定顺序合并：

```
~/.claude/CLAUDE.md          （用户级，所有项目）
  ↓ 合并
./CLAUDE.md                   （项目根目录）
  ↓ 合并
./packages/web/CLAUDE.md      （子目录，最接近编辑文件的）
  ↓ 合并
./.claude/CLAUDE.local.md     （本地覆盖，不提交到 Git）
```

策略性地使用这个层级：

| 层级 | 放什么 | 例子 |
|------|-------|------|
| **用户级** (`~/.claude/`) | 个人偏好、全局工具配置 | "Use vim keybindings in diffs" |
| **项目根目录** (`./`) | 团队惯例、构建命令 | "pnpm, not npm" |
| **子目录** (`./packages/web/`) | 包级别规则 | "React components use .tsx extension" |
| **本地文件** (`.claude/CLAUDE.local.md`) | 机器特定覆盖 | "Database runs on port 5433 locally" |

关键点：**离编辑文件越近的规则优先级越高**。根目录 CLAUDE.md 说"用 Jest"，但 `packages/web/CLAUDE.md` 说"用 Vitest"，编辑那个包的文件时 Agent 会用 Vitest。

## 效果度量

CLAUDE.md 是驾驭系统的组件。和任何工程产物一样，它应该被度量。跟踪这三个指标：

### 1. 一次成功率

**指标：** Claude 第一次就产出正确结果、不需要纠正的任务比例。

**测量方式：** 回顾最近 20 次 Claude Code 会话。统计多少次零纠正、多少次需要"不是这样，应该这样做"。

**目标：** 驾驭良好的项目 70% 以上。低于 50% 说明 CLAUDE.md 缺少关键约束。

### 2. 重复纠正率

**指标：** 跨多个会话重复告诉 Claude 同一件事的频率。

**测量方式：** 记录一周。每次纠正 Claude，记下说了什么。如果同样的纠正出现 3 次以上，它应该写进 CLAUDE.md。

**目标：** 零重复纠正。每一条重复纠正都是 CLAUDE.md 少了一行。

### 3. 探索性工具调用

**指标：** Claude 在开始实际工作前，为了解项目结构而进行的工具调用次数。

**测量方式：** 检查典型会话中 Claude 的工具使用。如果它一开始就跑 `find`、`grep` 或读一堆文件来理解项目结构，说明 CLAUDE.md 缺少定位信息。

**目标：** Claude 应该在 2-3 次工具调用内开始处理实际任务。

### 反馈循环

这些指标反哺你的 CLAUDE.md：

```
检测到重复纠正
  → 添加约束到 CLAUDE.md
  → 验证是否减少了纠正
  → 如果 CLAUDE.md 超过 60 行
    → 把最不关键的规则迁移到 Skills
```

这就是[Guide + Sensor 模式](/posts/ai/2026-04-04-harness-engineering-guide/)的实战应用：你的观察（Sensor）改进你的 CLAUDE.md（Guide），Guide 减少未来的错误，错误的减少又改变你的观察。

## 实战案例：一个 Hugo 技术博客的配置

以一个典型的 Hugo 多语言技术博客为例，展示层级模式的实际运用：

**`CLAUDE.md`**（极简指向）：
```markdown
see @AGENTS.md
```

**`AGENTS.md`**（~80 行有效规则）：
- 交互语言约定（对话用中文，内容用英文）
- Git 分支和部署流程
- 构建命令（`hugo server -D` / `hugo --minify`）
- 多语言规则（英文默认，中文可选）
- Front matter 模板和必填字段
- 图片格式规则（仅 WebP，封面 1200x630）
- 内容策略红线（禁止无搜索意图的日志类帖子）

~80 行已经在研究推荐的上限附近了。但它有效，因为每一行都在防止一个具体错误——用错分支、用错语言、漏了 front matter 字段、图片格式不对。

领域特定知识（部署流程、主题自定义规则）放在独立的文档文件里，Claude 需要时按需读取，不放在始终加载的配置中。

## 提交前清单

提交 CLAUDE.md 之前，逐项检查：

- [ ] **60 行以内**——数一数
- [ ] **每一行防止一个具体错误**——做石蕊测试
- [ ] **没有可推断的信息**——没有 Claude 能从代码看出来的东西
- [ ] **没有泛泛的建议**——没有"write clean code"或"follow best practices"
- [ ] **命令是精确的**——`pnpm test`，不是"run the tests"
- [ ] **领域知识在 Skills 里**——不是全塞进主文件
- [ ] **人工编写的**——不是 AI 生成的
- [ ] **在真实任务中验证过**——不是理论上的

## 延伸阅读

- [驾驭工程：为什么 AI Agent 周围的系统比模型更重要](/posts/ai/2026-04-04-harness-engineering-guide/) — 本系列第一篇
- [CLAUDE.md 指南：给 Claude Code 持久记忆](/posts/ai/2026-01-12-claudemd-memory-guide/) — CLAUDE.md 入门
- [CLAUDE.md vs README.md](/posts/ai/2026-01-31-claudemd-vs-readme/) — 理解两种文件的不同用途
- [Claude Code Skills 指南](/posts/ai/2026-01-08-claudecode-skill-guide/) — 用 Skills 做渐进式披露
- [Claude Code 最佳实践](/posts/ai/2026-01-06-claudecode-best-practices/) — Claude Code 基础工作流技巧
- [Superpowers 深度解析](/posts/ai/2026-02-01-superpowers-deep-dive/) — 一个真实的 Skills 驾驭系统实战
