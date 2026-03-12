+++
date = '2026-03-03T19:00:00+08:00'
draft = false
title = 'CLAUDE.md 最佳实践：写出真正有效的配置文件'
description = '如何为 Claude Code 编写高效的 CLAUDE.md 文件。实用模式、7 种项目类型示例，以及 CLAUDE.md vs .cursorrules vs AGENTS.md 对比。'
toc = true
tags = ['Claude Code', 'CLAUDE.md', 'Best Practices', 'AI Development', 'AGENTS.md']
categories = ['AI Guides']
keywords = ['CLAUDE.md 指南', 'claude code claude.md', '如何编写 CLAUDE.md', 'CLAUDE.md 最佳实践', 'CLAUDE.md 示例', 'CLAUDE.md vs cursorrules', 'CLAUDE.md vs AGENTS.md', 'claude code 配置']

[[params.faqItems]]
question = "CLAUDE.md 是什么？它如何工作？"
answer = "CLAUDE.md 是一个 Markdown 文件，Claude Code 在每次会话开始时自动加载。它相当于持久记忆——你只需写一次项目规则、编码标准和工作流指令，Claude 就会在每次对话中自动遵循，无需反复提醒。"

[[params.faqItems]]
question = "CLAUDE.md 文件应该放在哪里？"
answer = "Claude Code 支持多个位置：~/.claude/CLAUDE.md 用于所有项目的全局偏好设置，./CLAUDE.md 放在项目根目录用于团队共享规则（提交到 Git），./CLAUDE.local.md 用于个人覆盖配置（不提交），.claude/rules/*.md 用于模块化规则文件。后加载的文件会覆盖先加载的。"

[[params.faqItems]]
question = "CLAUDE.md 应该写多长？"
answer = "主 CLAUDE.md 建议控制在 200 行以内。LLM 可靠地遵循大约 150-200 条离散指令，而 Claude Code 的系统提示词已经占用了约 50 条。如果需要更多内容，使用 @ 导入引用单独的架构文档、测试指南或 API 规范文件。"

[[params.faqItems]]
question = "CLAUDE.md、AGENTS.md 和 .cursorrules 有什么区别？"
answer = "CLAUDE.md 是 Claude Code 专用的，由 Claude Code 自动加载。AGENTS.md 是跨工具标准，支持 30 多种 AI 编码工具，包括 Codex CLI、Gemini CLI、Cursor 和 Claude Code。.cursorrules 是 Cursor 专用的。对于使用多种工具的团队，建议将 AGENTS.md 作为权威来源，然后在 CLAUDE.md 中用 'See @AGENTS.md' 引用。"

[[params.faqItems]]
question = "CLAUDE.md 和 AGENTS.md 可以一起使用吗？"
answer = "可以，而且这是使用多种 AI 工具的团队的推荐做法。将通用规则放在 AGENTS.md 中，然后创建一个只有一行的 CLAUDE.md：'See @AGENTS.md'。在该行下方添加任何 Claude 专属指令（如 Skill 引用或模型偏好）。"
+++

![CLAUDE.md 最佳实践指南：编写高效的 Claude Code 配置文件](cover.webp)

大多数 CLAUDE.md 文件写得很糟糕。它们要么是空的，要么塞满了 500 行自动生成的样板文本，要么充斥着"写干净的代码"这类模糊指令——而 Claude 本来就在尽力做到这一点。

一份写得好的 CLAUDE.md 能将 Claude Code 从一个通用助手转变为了解你的技术栈、遵循你的规范、避免项目特定陷阱的团队成员。一份写得差的则浪费上下文 token，给你一种虚假的掌控感。

本指南聚焦于**如何做**——编写真正能改变 Claude 行为的 CLAUDE.md 实用模式。你将看到不同项目类型的真实示例、让 CLAUDE.md 失效的具体错误，以及 CLAUDE.md vs AGENTS.md vs .cursorrules 的清晰对比。如果你需要先了解基础知识（CLAUDE.md 是什么、如何加载、三层系统），请先阅读我们的 [CLAUDE.md 入门指南](/posts/ai/2026-02-28-claude-code-claudemd-guide/)。

## CLAUDE.md 的加载机制

在编写有效规则之前，你需要了解加载机制。[Claude Code](https://docs.anthropic.com/en/docs/claude-code/memory) 会按特定优先级从多个位置自动加载 CLAUDE.md 文件：

| 优先级 | 位置 | 作用域 | 纳入 Git？ |
|--------|------|--------|:----------:|
| 1（最低） | `~/.claude/CLAUDE.md` | 所有项目（全局） | 不适用 |
| 2 | `./CLAUDE.md` | 当前项目（团队） | 是 |
| 3 | `./.claude/rules/*.md` | 当前项目（模块化） | 是 |
| 4（最高） | `./CLAUDE.local.md` | 当前项目（个人） | 否 |

关键行为：

- **自动加载**：你不需要告诉 Claude 去读取 CLAUDE.md，它会在会话启动时自动完成。
- **递归扫描**：Claude Code 从当前目录向上遍历，加载每一个找到的 CLAUDE.md。在 monorepo 中，当 Claude 处理前端文件时，`frontend/CLAUDE.md` 会被自动加载。
- **覆盖顺序**：后加载（更高优先级）的文件覆盖先加载的。你的个人 `CLAUDE.local.md` 会覆盖团队的 `CLAUDE.md`。
- **@ 导入**：任何 CLAUDE.md 都可以通过 `@path/to/file.md` 引用其他文件，Claude 会一并加载。

这意味着你可以分层配置：适用于所有项目的全局偏好、与团队共享的项目规则，以及保留在本地的个人覆盖配置。

## 高效 CLAUDE.md 的 6 大原则

### 原则 1：写指令，不写描述

CLAUDE.md 是一套指令集，不是文档。每一行都应该告诉 Claude **做什么**。

**差——描述性的：**

```markdown
## 关于本项目
这个项目是一个用 Next.js 15 和 TypeScript 构建的电商平台。
我们通常偏好函数式编程模式，力求保持代码整洁和可维护。
团队重视可读性和……
```

**好——命令式的：**

```markdown
## 技术栈
- Next.js 15 (App Router) + TypeScript 5.7 (strict mode)
- Tailwind CSS + shadcn/ui + Zustand
- PostgreSQL + Prisma

## 规则
- 仅使用函数组件，禁止类组件。
- 所有函数必须有 TypeScript 类型注解。
- 函数不超过 30 行，重复逻辑提取为辅助函数。
```

第一个版本像 README 的项目介绍。Claude 不需要你推销项目——它需要指令。第二个版本减少了 40% 的 token，但可操作性提升了 100%。

### 原则 2：只包含能改变行为的规则

CLAUDE.md 中的每条规则都应通过这个测试：**"如果删掉这条规则，Claude 的输出会变差吗？"**

未通过测试的规则：

- "写干净、可维护的代码" —— Claude 本来就在这么做
- "遵循最佳实践" —— 太模糊，无法改变行为
- "使用有意义的变量名" —— Claude 默认就会这样做
- "正确处理错误" —— 不够具体

通过测试的规则：

- "所有数据库查询必须按 `tenantId` 过滤" —— 项目特定的不变量
- "使用 Zustand 进行状态管理，不用 Redux 或 Context API" —— 明确的技术选择
- "测试文件放在源文件旁边的 `__tests__/` 中，不放在单独的 `tests/` 目录" —— 结构性决策
- "禁止使用 `console.log`，使用 `src/lib/logger` 中的 `logger` 工具" —— 具体的覆盖规则

如果没有这条规则 Claude 也会这样做，那这条规则就是在浪费上下文 token。

### 原则 3：控制在 200 行以内

关于 LLM 指令遵循的研究表明，超过约 150-200 条离散指令后收益递减。Claude Code 的系统提示词已经占用了约 50 条，留给你大约 150 条有效指令。

500 行的 CLAUDE.md 不会给你 3 倍的控制力——反而会给你**更少**的控制力，因为重要规则被噪音淹没了。

**当你的 CLAUDE.md 超过 200 行时：**

```markdown
# 项目配置

## 架构
@docs/architecture.md

## API 规范
@docs/api-conventions.md

## 测试标准
@docs/testing-guide.md

## 部署
@docs/deploy-runbook.md
```

保持主 CLAUDE.md 作为简洁的索引。将详细文档移到通过 `@` 导入引用的单独文件中。

### 原则 4：强调关键规则

并非所有规则都同等重要。有些是偏好（"优先用 `const` 而非 `let`"）。有些是绝不能违反的不变量（"所有查询必须按租户 ID 过滤"）。

对于关键规则，使用强烈的措辞：

```markdown
## 关键规则

- IMPORTANT：所有数据库查询必须按 `tenantId` 过滤，没有例外。
  多租户数据泄露属于安全事故。
- NEVER 将 `.env` 文件或 API 密钥提交到 Git。
- NEVER 删除或修改数据库迁移文件。只能创建新的迁移。
- YOU MUST 在创建任何提交前运行 `pnpm test`。
```

`IMPORTANT`、`MUST`、`NEVER` 和 `ALWAYS` 等词汇可以显著提高关键指令的遵从率。但要谨慎使用——如果一切都标为"IMPORTANT"，那就什么都不重要了。

### 原则 5：不要复制 Linter 规则

Claude Code 会读取你项目的配置文件——`eslintrc`、`prettier.config`、`tsconfig.json`、`.editorconfig`、`pyproject.toml`。如果一条规则已经被工具强制执行，在 CLAUDE.md 中重复就是浪费 token。

**不要放在 CLAUDE.md 中**（已由工具处理）：

- 缩进风格（Prettier/EditorConfig）
- 导入排序（eslint-plugin-import）
- 行长度限制（Black/Prettier）
- 尾随逗号（Prettier）
- 类型检查严格度（tsconfig.json）

**应该放在 CLAUDE.md 中**（linter 无法强制执行的）：

- 架构模式（"Service 层处理业务逻辑，路由层保持精简。"）
- 业务逻辑约束（"所有价格以分存储，不以元存储。"）
- 超出语法范围的命名规范（"功能开关使用 `isEnabled` 前缀。"）
- 工作流指令（"提交前运行测试。"）
- 技术选型（"使用 Zustand，不用 Redux。"）

### 原则 6：测试和迭代

写完 CLAUDE.md 后，测试它：

1. 启动一个新的 Claude Code 会话
2. 让 Claude 执行一个应该触发你某条规则的任务
3. 检查它是否遵循了该规则
4. 如果没有，说明规则要么太模糊、埋得太深，要么被其他指令所矛盾

例如，如果你的 CLAUDE.md 说"所有 API 输入验证使用 Zod"，让 Claude 创建一个新的 API 端点。它是否包含了 Zod schema？如果没有，重写规则使其更突出，或用 `MUST` 加强强调。

像对待代码一样对待 CLAUDE.md——它需要测试、迭代和维护。

## 不同项目类型的真实示例

### 示例 1：React/Next.js 前端

````markdown
# SaaS 仪表盘

## 技术栈
- Next.js 15 (App Router) + TypeScript 5.7 (strict)
- Tailwind CSS + shadcn/ui
- Zustand 管理客户端状态
- TanStack Query 管理服务端状态
- Vitest + Testing Library

## 命令
```bash
pnpm dev           # 开发服务器 localhost:3000
pnpm build         # 生产构建
pnpm test          # 运行测试
pnpm lint          # ESLint 检查
pnpm db:push       # 推送 Prisma schema
```

## 规则
- 仅使用函数组件，禁止类组件。
- Props 接口命名为 `[Component]Props`（如 `UserCardProps`）。
- 文件名：kebab-case。组件名：PascalCase。
- 所有 API 调用使用 TanStack Query 的 `useQuery`/`useMutation`。
- 禁止 `any` 类型。如果确实未知，使用 `unknown`。
- 所有面向用户的文本必须使用 i18n 系统（`t()` 函数）。

## 关键规则
- NEVER 直接从 `node_modules` 导入，使用 `src/lib/` 中的重新导出。
- 所有数据库查询 MUST 按 `organizationId` 过滤（多租户）。
- NEVER 提交 `.env.local` 或在客户端代码中暴露 API 密钥。
````

### 示例 2：Python FastAPI 后端

````markdown
# 支付服务 API

## 技术栈
- Python 3.12 + FastAPI 0.115
- SQLAlchemy 2.0 + Alembic
- PostgreSQL 16 + Redis 7
- Poetry 管理依赖
- pytest 测试

## 命令
```bash
poetry run uvicorn src.main:app --reload    # 开发服务器
poetry run pytest -x -v                     # 测试（首次失败即停止）
poetry run alembic upgrade head             # 应用迁移
poetry run ruff check . && ruff format .    # 检查 + 格式化
```

## 架构
- 路由层保持精简：验证输入 → 调用服务 → 返回响应。
- 业务逻辑放在 `src/services/` 中。
- 数据库操作通过 `src/repositories/` 中的仓储类。
- 后台任务使用 Celery，定义在 `src/tasks/` 中。

## 规则
- 所有函数必须有类型注解，没有例外。
- 所有请求/响应验证使用 Pydantic 模型。
- 文档字符串使用 Google 风格。
- NEVER 执行原始 SQL 查询，使用 SQLAlchemy ORM。
- 所有金额以整数（分）存储，在 API 边界转换。
- 新端点 MUST 至少有一个正常路径和一个错误路径的测试。
````

### 示例 3：Monorepo

````markdown
# Acme 平台 Monorepo

## 结构
```
apps/
├── web/           # Next.js 客户门户（见 apps/web/CLAUDE.md）
├── admin/         # Next.js 管理后台（见 apps/admin/CLAUDE.md）
└── api/           # FastAPI 后端（见 apps/api/CLAUDE.md）
packages/
├── ui/            # 共享组件库
├── config/        # 共享配置（ESLint, TypeScript, Tailwind）
└── types/         # 共享 TypeScript 类型
```

## 全局规则（适用于所有应用）
- 包管理器：pnpm。NEVER 使用 npm 或 yarn。
- 提交格式：`type(scope): description`（如 `feat(web): add login page`）
- 范围：web, admin, api, ui, config, types, infra
- 所有 PR 必须通过 CI 才能合并。
- 共享类型放在 `packages/types/` 中。NEVER 重复类型定义。

## 命令
```bash
pnpm install              # 安装所有依赖
pnpm --filter web dev     # 运行 web 应用
pnpm --filter api dev     # 运行 API
pnpm -r test              # 运行所有测试
pnpm -r build             # 构建所有包
```

## 跨应用规则
- 前端应用仅通过 API 获取数据，禁止直接访问数据库。
- `packages/ui/` 中的共享组件必须与框架无关。
- API 变更必须保持向后兼容。破坏性变更需要版本控制。
````

### 示例 4：移动应用（React Native）

````markdown
# HealthTrack 移动应用

## 技术栈
- React Native 0.76 + Expo SDK 52
- TypeScript 5.7 (strict)
- Zustand + MMKV 本地存储
- React Navigation v7

## 命令
```bash
npx expo start        # 开发服务器
npx expo run:ios      # 在 iOS 模拟器运行
npx expo run:android  # 在 Android 模拟器运行
pnpm test             # Jest 测试
```

## 规则
- 优先使用 Expo API。如果 Expo 已覆盖的功能，不要安装原生 RN 模块。
- 页面放在 `src/screens/`，组件放在 `src/components/`。
- 导航类型 MUST 在 `src/navigation/types.ts` 中定义。
- 使用 `StyleSheet.create()` 定义样式，禁止内联样式对象。
- 所有网络请求通过 `src/api/client.ts`，禁止直接调用 fetch。
- IMPORTANT：必须在 iOS 和 Android 上都测试。平台特定代码使用 `.ios.tsx` / `.android.tsx` 后缀。
- NEVER 在 AsyncStorage 中存储敏感数据（token、密码），使用 expo-secure-store。
````

### 示例 5：Go 微服务

````markdown
# 通知服务

## 技术栈
- Go 1.23
- Chi 路由 + sqlc 数据库查询
- PostgreSQL 16 + Redis 7
- Docker 本地开发

## 命令
```bash
go run ./cmd/server              # 运行服务器
go test ./...                    # 运行所有测试
make migrate-up                  # 应用迁移
make generate                    # 重新生成 sqlc + protobuf
docker compose up -d             # 启动本地依赖
```

## 规则
- 遵循标准 Go 项目布局。入口在 `cmd/`，包在 `internal/`。
- 错误处理：用 `fmt.Errorf("context: %w", err)` 包装错误。不要丢弃错误。
- 接口由消费者定义，而非实现者。
- 数据库查询在 `internal/db/` 中由 sqlc 生成。编辑 `.sql` 文件，然后运行 `make generate`。
- NEVER 直接修改生成的代码。修改源文件（SQL、proto）然后重新生成。
- 日志：使用 `slog` 的结构化日志。禁止 `fmt.Println` 或 `log.Println`。
- Context 必须是任何执行 I/O 的函数的第一个参数。
````

### 示例 6：Hugo 博客（像本站一样）

这是本博客实际使用的模式：

````markdown
# AI 工程博客

## 技术栈
- Hugo v0.153.2+（Extended）
- 主题：hermit-V2（git submodule）

## 命令
```bash
hugo server -D         # 含草稿预览
hugo server            # 不含草稿预览
hugo --minify          # 生产构建
```

## 内容规则
- 所有新文章 MUST 使用英文撰写。
- NEVER 修改已有的中文文章。
- Front matter 使用 TOML 格式（+++）。
- 分类：仅限 'AI Guides' 或 'Comparisons'，不可自定义分类。

## 文章结构
- 目录：content/posts/ai/YYYY-MM-DD-english-slug/index.md
- 封面图：MUST 命名为 cover.webp（1200x630px，<200KB）
- 封面图 MUST 在 front matter 之后第一行引用
- 标签：3-5 个英文标签
- 描述：120-160 字符，包含主关键词

## Git
- 工作分支：code
- 提交信息：中文
- 推送到 code 触发自动部署
````

### 示例 7：全局用户配置

放在 `~/.claude/CLAUDE.md`——适用于每个项目：

```markdown
# 开发者配置

我是一名高级全栈工程师。主要语言：TypeScript、Python、Go。

## 偏好
- 所有对话用中文回复
- 提交信息用中文
- 代码注释用英文
- 偏好函数式模式而非面向对象
- 函数不超过 30 行
- 使用描述性变量名——除了循环计数器外不用单字母

## 工作流
- 约定式提交格式：type: description
- 每次提交前运行 linter
- 小而聚焦的提交优于大批量提交
- 当在两种方案间犹豫时，选择更简单的那个
```

## CLAUDE.md vs .cursorrules vs AGENTS.md

如果你的团队使用多种 AI 编码工具，你需要了解这三个配置文件之间的关系。

### 快速对比

| 特性 | CLAUDE.md | .cursorrules | AGENTS.md |
|------|-----------|--------------|-----------|
| **工具** | 仅 Claude Code | 仅 Cursor | 30+ 工具（跨平台） |
| **自动加载** | 是 | 是（在 Cursor 中） | 是（被支持的工具） |
| **文件位置** | 根目录、子目录、`~/.claude/` | 仅根目录 | 根目录、子目录 |
| **多层级** | 是（全局 + 项目 + 个人） | 否（单文件） | 是（目录层级） |
| **@ 导入** | 是 | 否 | 取决于工具 |
| **标准制定方** | [Anthropic](https://docs.anthropic.com/en/docs/claude-code/memory) | Cursor 专有 | [Linux Foundation](https://github.com/anthropics/agents-md) |
| **采用量** | Claude Code 用户 | Cursor 用户 | 60,000+ 仓库 |

### 何时使用什么

**独立开发者，只用 Claude Code**：使用 CLAUDE.md，够用了。

**团队只用 Cursor**：使用 `.cursorrules`（或 Cursor 更新的 `.cursor/rules/` 系统）。

**团队使用多种 AI 工具**（Claude Code + Cursor + Copilot + Codex CLI）：将通用规则写在 AGENTS.md 中。然后：

- CLAUDE.md → 一行：`See @AGENTS.md`
- .cursorrules → 复制相关规则（Cursor 不以相同方式支持 `@` 导入）

**开源项目**：使用 AGENTS.md。它有最广泛的工具兼容性。超过 60,000 个仓库已采用，并由 Linux Foundation 下的 [Agentic AI Foundation](https://github.com/anthropics/agents-md) 支持。

### 推荐的多工具配置方案

以下是在 Claude Code 搭配其他工具使用时有效的模式：

**第一步**：编写包含所有通用规则的 `AGENTS.md`：

```markdown
# 仓库准则

## 技术栈
- Next.js 15 + TypeScript 5.7
- Tailwind CSS + shadcn/ui
- PostgreSQL + Prisma

## 编码标准
- 仅使用函数组件
- Props 接口命名为 [Component]Props
- 所有 API 调用必须处理加载态和错误态

## 测试
- Vitest + Testing Library
- 新功能需要测试
- 提交前运行 pnpm test
```

**第二步**：创建精简的 `CLAUDE.md`：

```markdown
See @AGENTS.md

## Claude 专属配置
- 上下文变长时使用 /compact
- 常规任务用 Sonnet，架构决策用 Opus
- 编写 Skills 时，遵循 .claude/skills/ 中的模式
```

**第三步**：可选地创建 `.cursorrules`，包含同样的通用规则（因为 Cursor 原生读取 `.cursorrules`）。

这样，每个 AI 工具都读取相同的核心指令。Claude 专属功能如 [Skills](/posts/ai/2026-02-28-claude-code-skills-guide/) 和 [Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) 留在 CLAUDE.md 中，各归其位。

## 10 个常见错误（及修复方法）

### 1. 写成了小说

**症状**：一个 500 行的 CLAUDE.md，包含项目历史、设计哲学、团队介绍和会议纪要。

**修复**：无情地删减。对每一行问："如果删掉这行，Claude 的输出会变差吗？"如果不会，删掉。Claude 需要指令，不需要背景故事。

### 2. 过于模糊

**症状**：像"写干净的代码"或"遵循最佳实践"这样的规则。

**修复**：让规则具体且可测试。不是"正确处理错误"，而是"所有异步函数必须有 try/catch 块。使用 logger 工具记录错误。返回适当的 HTTP 状态码。"

### 3. 复制 Linter 规则

**症状**：列出每一条 ESLint 或 Prettier 规则。当 `.editorconfig` 已经指定了 2 空格缩进时还要再写一遍。

**修复**：只包含自动化工具无法强制执行的规则——架构模式、业务逻辑约束、工作流指令。

### 4. 从不更新

**症状**：CLAUDE.md 写于 6 个月前。技术栈已变、规范已演进、一半的指令已过时。

**修复**：每月审查 CLAUDE.md。当 Claude 反复犯同样的错误时添加规则。当规则不再相关时删除。像对待活文档一样对待它。

### 5. 混淆 README 和 CLAUDE.md 内容

**症状**：大段解释项目做什么、为什么构建、徽章、截图。

**修复**：README 回答"这是什么？"CLAUDE.md 回答"我应该如何参与开发？"让它们分开。详细对比请参阅我们的 [CLAUDE.md vs README.md 对比](/posts/ai/2026-01-31-claudemd-vs-readme/)。

### 6. 在共享文件中放个人偏好

**症状**：你的 CLAUDE.md 说"用中文回复"，但你的队友想要英文。偏好设置产生合并冲突。

**修复**：共享标准放在 `./CLAUDE.md` 中。个人偏好放在 `./CLAUDE.local.md` 中（加入 `.gitignore`）。通用个人偏好放在 `~/.claude/CLAUDE.md` 中。

### 7. 忽略子目录 CLAUDE.md 文件

**症状**：monorepo 中只有一个巨大的根 CLAUDE.md，试图同时涵盖前端 React 规则和后端 Python 规则。

**修复**：按目录拆分。根 CLAUDE.md 放共享规则（Git 规范、CI 流程）。`frontend/CLAUDE.md` 放 React/TypeScript 规则。`backend/CLAUDE.md` 放 Python/FastAPI 规则。Claude 会根据上下文加载正确的文件。

### 8. 不使用 @ 导入

**症状**：一个 400 行的 CLAUDE.md，难以导航和维护。

**修复**：拆分为聚焦的文件。主 CLAUDE.md 变成目录，用 `@` 导入指向详细文档。每个导入的文件覆盖一个主题。

### 9. 规则矛盾

**症状**：第 15 行说"使用 Redux 进行状态管理"。第 87 行说"客户端状态优先使用 Zustand"。Claude 被搞混了，两个都不能一致执行。

**修复**：审查矛盾。每个决策使用单一权威来源。当从一种方式迁移到另一种时，要明确说明："遗留代码使用 Redux。所有新代码 MUST 使用 Zustand。"

### 10. 把 CLAUDE.md 当作一劳永逸

**症状**：你运行一次 `/init`，接受生成的文件，然后再也不碰它。

**修复**：`/init` 是起点，不是终点。审查输出，添加团队的特定规则，删除通用内容，并随时间推移添加规则——当你发现 Claude 在你的项目中哪里容易出错时。

## 高级模式

### "经验教训"部分

你能添加的最有价值的部分之一是记录 Claude 在你项目中犯过的错误。这是 [Claude Code 的创建者推荐的](https://x.com/amanrsanger/status/1917312117418262599)：

```markdown
## 经验教训（不要重复这些错误）
- 本项目使用 ESM 模块。NEVER 使用 require() 或 module.exports。
- `user` 表有软删除列 `deleted_at`。所有查询必须添加
  `WHERE deleted_at IS NULL`，除非明确查询已删除的用户。
- 测试不得使用生产数据库。使用 conftest.py 中的测试 fixtures。
- /api/v1/upload 端点有 nginx 强制的 10MB 限制，不是应用层的。
  不要添加应用层的大小验证——已经被处理了。
```

每次 Claude 犯错时，添加到这里。随着时间推移，这个部分会成为你项目的 AI 机构记忆——相当于入职文档中说"顺便注意，这里有个坑"。

### 带上下文的条件规则

对于在不同情况下有不同规则的项目：

```markdown
## API 开发
- 创建新端点时：参考 src/api/v1/users.py 中的模式
- 修改已有端点时：保持向后兼容。添加新字段，不要重命名或删除现有字段。
- 编写迁移时：NEVER 修改或删除现有迁移文件。创建新的。

## 前端开发
- 创建新页面时：使用 src/app/(dashboard)/template/page.tsx 中的模板
- 添加表单时：使用 react-hook-form + Zod。参见 src/components/forms/ 中的模式。
- 添加新 API 调用时：在 src/hooks/api/ 中使用 TanStack Query 添加 query/mutation。
```

这种模式为 Claude 提供了特定上下文的指令，而不会用仅在某些时候适用的规则膨胀文件。

### Rules 文件实现模块化组织

Claude Code 支持 `.claude/rules/*.md`，将规则组织到自动加载的独立文件中：

```
.claude/
└── rules/
    ├── coding-standards.md
    ├── git-conventions.md
    ├── testing-requirements.md
    └── security-policies.md
```

每个文件都会自动加载。对于希望模块化组织但不想在 CLAUDE.md 中维护索引的项目，这比 `@` 导入更清晰。

### CLAUDE.md + Hooks：自动化执行

你的 CLAUDE.md 可以通过 [Claude Code Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) 引用自动化检查：

```markdown
## 自动化检查（不要手动重复这些）
- Pre-commit：ESLint + Prettier 通过 hooks 自动运行
- Pre-push：完整测试套件自动运行
- 见 .claude/settings.json 了解 hook 配置

## 你仍然必须做的
- 写有意义的提交信息
- 为新业务逻辑添加测试
- 当端点变更时更新 API 文档
```

这防止 Claude 手动运行 hooks 已经处理的检查，避免重复工作。

## 快速上手清单

从零开始？按以下步骤操作：

1. **运行 `/init`** —— 获得自动生成的起点
2. **删除废话** —— 移除 Claude 不需要指令也会做的内容
3. **添加技术栈** —— 框架、语言、数据库、包管理器（每项一行）
4. **添加命令** —— build、test、lint、deploy（一个代码块）
5. **添加团队规则** —— 命名规范、架构模式、Git 工作流
6. **添加关键规则** —— 带 MUST/NEVER 强调的业务不变量
7. **添加经验教训** —— Claude 犯过的你不想重复的错误
8. **测试** —— 启动新会话，给 Claude 一个任务，验证规则遵从度
9. **提交到 Git** —— `git add CLAUDE.md`
10. **添加 `.gitignore` 条目** —— `CLAUDE.local.md` 用于个人覆盖
11. **设置全局配置** —— `~/.claude/CLAUDE.md` 用于通用偏好
12. **每月维护** —— 删除过时规则，添加新规则，保持精简

## 相关阅读

- [CLAUDE.md 指南：给 AI 完美的上下文](/posts/ai/2026-02-28-claude-code-claudemd-guide/) —— CLAUDE.md 基础知识和三层系统
- [CLAUDE.md vs README.md](/posts/ai/2026-01-31-claudemd-vs-readme/) —— 为什么这两个文件服务于不同受众
- [Claude Code 设置指南 2026](/posts/ai/2026-02-25-claude-code-setup-guide/) —— 安装、认证和首个项目设置
- [Claude Code Hooks 指南](/posts/ai/2026-02-28-claude-code-hooks-guide/) —— 在 Claude Code 操作前后自动执行动作
- [Claude Code Skills 指南](/posts/ai/2026-02-28-claude-code-skills-guide/) —— 构建补充 CLAUDE.md 的可复用任务工作流
- [Claude Code 十大错误](/posts/ai/2026-02-25-claude-code-mistakes/) —— 常见陷阱，包括忽略 CLAUDE.md
- [Claude Code 定价 2026](/posts/ai/2026-02-25-claude-code-pricing/) —— 选择适合你使用量的计划

---

CLAUDE.md 不是魔法，它只是一个纯文本的指令文件。但维护一份好的 CLAUDE.md 和不维护之间的差距，就是一个了解你项目的 AI 和一个在猜测的 AI 之间的差距。写紧凑的规则，测试它们，保持更新，让 Claude 处理剩下的。
