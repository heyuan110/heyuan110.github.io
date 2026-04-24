+++
date = '2026-01-31 06:00:02'
draft = false
title = 'CLAUDE.md vs README.md：一个给 AI 看，一个给人看'
description = 'CLAUDE.md 和 README.md 有什么区别？本文结合 OpenClaw（124k Star）的 AGENTS.md 实践和自己项目的真实案例，讲清楚怎么写好这两个文件，让 AI Agent 和人类开发者各得其所。'
tags = ['Claude Code', 'CLAUDE.md', 'AGENTS.md', 'AI Agent', 'Anthropic']
categories = ['AI']
keywords = ['CLAUDE.md 怎么写', 'CLAUDE.md vs README.md', 'AGENTS.md', 'Claude Code 记忆系统', 'AI Agent 项目配置']
toc = true
+++

![CLAUDE.md vs README.md](cover.webp)

## 一、你的项目里，AI 和人在读同一份说明书

你用 Claude Code 写代码，打开一个项目，AI 第一件事是读 `CLAUDE.md`。你的同事打开同一个项目，第一件事是读 `README.md`。

问题来了：这两个文件你都认真写了吗？还是只写了 README，指望 AI 自己"看懂"？

实际情况是——AI 看 README 就像你看一份全是法律术语的合同：信息都在，但找不到重点。README 告诉人类"这个项目是什么"，但 AI 需要的是"我该怎么做"。

这篇文章讲清楚一件事：**README.md 是给人看的项目说明，CLAUDE.md 是给 AI Agent 看的指令集，两者不应互相替代。**

---

## 二、先搞清楚：CLAUDE.md 到底是什么？

### 2.1 一句话定义

> **CLAUDE.md** 是 Claude Code 的记忆系统——一个 Markdown 文件，Claude Code 每次启动时自动加载，里面写的是项目规则、代码规范、工作流程等指令。截至 2026 年 1 月，Claude Code 在 GitHub 上有 6.26 万 Star（[来源](https://github.com/anthropics/claude-code)）。

你可以把它理解成：README 是给新同事写的入职手册，CLAUDE.md 是给 AI 助理写的工作守则。

### 2.2 Claude Code 的记忆层级

Claude Code 按以下顺序加载记忆文件，优先级从高到低：

| 层级 | 位置 | 共享范围 |
|------|------|----------|
| 组织策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md` | 整个组织 |
| 项目记忆 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队（提交到 Git） |
| 项目规则 | `./.claude/rules/*.md` | 团队（提交到 Git） |
| 个人记忆 | `~/.claude/CLAUDE.md` | 仅自己（所有项目） |
| 项目本地 | `./CLAUDE.local.md` | 仅自己（当前项目） |

来源：[Anthropic 官方文档](https://docs.anthropic.com/en/docs/claude-code/memory)

关键点：Claude Code 从当前目录向上递归查找 `CLAUDE.md`，子目录的 `CLAUDE.md` 只在读取该目录下文件时才加载。这意味着你可以给 `frontend/` 和 `backend/` 分别写不同的规则。

### 2.3 和 README.md 的根本区别

| 维度 | README.md | CLAUDE.md |
|------|-----------|-----------|
| 读者 | 人类开发者 | AI Agent |
| 目的 | 理解项目、快速上手 | 约束 Agent 行为 |
| 语气 | 说明文，可以有背景介绍 | 祈使句，只写规则 |
| 内容 | 是什么、怎么跑、项目结构 | 必须做什么、不能做什么、怎么做 |
| 格式 | 表格、树形图、链接，视觉优先 | 紧凑列表、代码块，token 效率优先 |

---

## 三、看看 124k Star 的项目怎么做的

### 3.1 OpenClaw 的做法

[OpenClaw](https://github.com/openclaw/openclaw)（12.4 万 Star，[来源](https://github.com/openclaw/openclaw)，截至 2026 年 1 月）是一个个人 AI 助手项目，它的做法很有意思：

**CLAUDE.md 只有一行：**

```
AGENTS.md
```

没了。它把所有 AI Agent 指令放在 `AGENTS.md` 里，`CLAUDE.md` 只是个指针。

**AGENTS.md 的结构（精简版）：**

```markdown
# Repository Guidelines
- Repo: https://github.com/openclaw/openclaw

## Project Structure & Module Organization
- Source code: `src/` (CLI in `src/cli`, commands in `src/commands`...)
- Tests: colocated `*.test.ts`.

## Build, Test, and Development Commands
- Runtime: Node 22+
- Install: `pnpm install`
- Tests: `pnpm test` (vitest)
- Lint: `pnpm lint` (oxlint)

## Coding Style & Naming Conventions
- TypeScript (ESM). Prefer strict typing; avoid `any`.
- Keep files under ~700 LOC.

## Commit & Pull Request Guidelines
- Create commits with `scripts/committer "<msg>" <file...>`
- Goal: merge PRs. Prefer rebase when commits are clean.

## Agent-Specific Notes
- Never edit `node_modules`.
- When answering questions, verify in code; do not guess.
```

注意几个特点：

1. **每条规则都是祈使句**——"avoid `any`"、"never edit"、"verify in code"
2. **不解释为什么**——AI 不需要被说服，只需要被告知
3. **有专门的 Agent-Specific Notes**——比如 "不要编辑 node_modules"，这种话你不会写在 README 里

### 3.2 为什么用 AGENTS.md？

这涉及一个行业趋势。2025 年 8 月，`AGENTS.md` 规范正式发布（[GitHub 仓库](https://github.com/agentsmd/agents.md)，1.63 万 Star），现已由 Linux 基金会下的 Agentic AI Foundation 管理。

截至 2026 年 1 月，支持 AGENTS.md 的工具包括：OpenAI Codex、Google Gemini CLI、Cursor、Windsurf、GitHub Copilot、Devin 等 20+ 款（[来源](https://agents.md/)）。超过 6 万个开源项目已采用。

Claude Code 目前不原生支持 AGENTS.md，但社区的通用做法是：

```bash
# 方案一：符号链接
mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md

# 方案二：CLAUDE.md 引用 AGENTS.md（利用 @ 导入语法）
echo 'See @AGENTS.md' > CLAUDE.md
```

OpenClaw 选择同时维护 `CLAUDE.md` 和 `AGENTS.md`，让不同的 AI 工具都能找到入口。

---

## 四、我自己项目的实践

### 4.1 踩过的坑

我之前做的一个跨境电商 SaaS 系统，前端 Vue 3 + 后端 Django。最初的 CLAUDE.md 是这样写的：

```markdown
# 项目 - Claude Code 配置

## 项目概述

这是一个跨境电商多租户 SaaS 后台管理系统，采用 Monorepo 结构。

## 重要规则

### Git 提交规则 ⚠️

**每次改完代码或做大改动前，必须先提交代码并推送到远程仓库。**

- 完成一个功能点后立即提交并 push
- ...
```

问题在哪？

- "项目概述"是给人看的——AI 不需要被介绍"这是什么项目"
- "重要规则 ⚠️"——emoji 和强调词对 AI 没有额外效果
- 186 行，大量重复信息（技术栈在"项目概述"写一遍，在"技术栈"又写一遍）

### 4.2 重写后的样子

参考 OpenClaw 的风格，压缩到 85 行：

```markdown
# Repository Guidelines

- Repo: `git@example.com:myteam/erp.git`, branch: `main`
- Monorepo: 跨境电商多租户 SaaS 后台管理系统

## Project Structure

- 前端: `frontend/` (Vue 3.5 + TypeScript 5.8 + Vite 6.3 + Ant Design Vue 4.2 + Pinia)
- 后端: `backend/` (Django 5.2 + DRF 3.16 + SimpleJWT + MySQL 8.0 + 七牛云存储)

## Coding Style

### 后端
- 所有模型继承 `TimestampedModel` + `SoftDeleteModel`。
- 所有业务数据必须带 `merchant_id` 字段 (多租户隔离)。
- ViewSet 的 `get_queryset` 必须过滤 `merchant_id`。

## Commit & Push Guidelines

- 完成一个功能点后立即 commit + push。
- **commit 后必须 `git push`，不能只 commit 不 push。**
- 提交信息格式: `type: 简短描述`
```

对比变化：

| 指标 | 重写前 | 重写后 |
|------|--------|--------|
| 行数 | 186 | 85 |
| 语气 | 说明文混合 | 纯指令式 |
| 废话 | "项目概述"、"重要规则" | 无 |
| 重复 | 技术栈写了两遍 | 只写一遍 |

### 4.3 同一件事，两个文件怎么写

以"技术栈"为例：

**README.md（给人看）——用表格，带版本号，方便扫一眼：**

```markdown
| 层 | 技术 | 版本 |
|---|------|------|
| 前端 | Vue + TypeScript + Ant Design Vue | 3.5 / 5.8 / 4.2 |
| 后端 | Django + Django REST Framework | 5.2 / 3.16 |
| 数据库 | MySQL | 8.0 |
```

**CLAUDE.md（给 AI 看）——压成一行，省 token：**

```markdown
- 后端: `backend/` (Django 5.2 + DRF 3.16 + SimpleJWT + MySQL 8.0 + 七牛云存储)
```

再看"Git 规范"：

**README.md** 里不写 Git 规范——这不是新人上手要知道的事。

**CLAUDE.md** 里必须写——因为 AI 每次改完代码都要决定是否提交：

```markdown
- commit 后必须 `git push`，不能只 commit 不 push。
```

---

## 五、怎么写好 CLAUDE.md？

### 5.1 六条原则

根据 [Anthropic 官方最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices) 和 [Builder.io 社区指南](https://www.builder.io/blog/claude-md-guide)（2026 年 1 月），总结如下：

**1. 每条规则问自己：删掉它，AI 会犯错吗？** 如果不会，就删。目标控制在 300 行以内。研究表明 AI 能稳定遵循的指令上限约 150-200 条（[来源](https://www.builder.io/blog/claude-md-guide)），Claude Code 系统提示已占约 50 条。

**2. 代码风格交给 Linter，不要交给 LLM。** "永远不要派 LLM 去做 Linter 的活"——与其在 CLAUDE.md 写"缩进用 2 空格"，不如配好 `.eslintrc`。

**3. 用指针，不要复制。** 不要把代码片段嵌入 CLAUDE.md，用 `file:line` 引用。也可以用 `@` 导入语法引用其他文件：`@docs/backend/api-spec.md`。

**4. 领域知识放 Skill，不放 CLAUDE.md。** CLAUDE.md 每次会话都加载，领域知识按需加载更高效。参考：[Skill 开发指南](/posts/ai/2026-01-08-claudecode-skill-guide/)。

**5. 像对待代码一样对待 CLAUDE.md。** 提交到 Git，定期审查，删除过时规则。

**6. 关键规则加强调。** `IMPORTANT` 或 `YOU MUST` 可以提高 AI 对特定规则的遵循率。

### 5.2 推荐的 CLAUDE.md 结构

```markdown
# Repository Guidelines          ← 一行 repo 地址 + 一句话定位
## Project Structure              ← 目录和技术栈，压缩成列表
## Build & Dev Commands           ← 一个代码块搞定所有命令
## Workflow                       ← 开发流程，编号列表
## Commit & Push Guidelines       ← Git 规则
## Coding Style                   ← 前后端代码规范
## Testing                        ← 测试目录结构 + 运行方式
## Dependencies                   ← 依赖管理规则
## Docs                           ← 文档体系 + 索引
```

### 5.3 推荐的 README.md 结构

```markdown
# 项目名                          ← 一句话介绍
## 技术栈                         ← 表格，带版本号
## 快速开始                       ← Docker 一键启动 + 本地启动
## 项目结构                       ← 树形图
## 业务模块                       ← 功能概览
## 文档                           ← 链接列表
## License                        ← 许可证
```

---

## 六、内容边界：什么放哪里

| 内容 | README.md | CLAUDE.md | 都不放 |
|------|:---------:|:---------:|:------:|
| 项目是什么 | O | | |
| 技术栈版本 | O | O（压缩版） | |
| 启动命令 | O（分步骤） | O（一个代码块） | |
| 环境要求（Node >= 20） | O | | |
| Git 提交规则 | | O | |
| 代码规范 | | O | |
| 测试规范 | | O | |
| 开发流程 | | O | |
| 开发计划 / TODO | | | O（用 Issue） |
| License | O | | |
| 业务模块介绍 | O | | |

原则：**README 回答 "What"，CLAUDE.md 回答 "How"。TODO 不属于任何一个。**

---

## 七、进阶：用 Skill 维护 CLAUDE.md

如果你经常修改 CLAUDE.md，可以写一个 Skill 来规范维护过程。我在项目里创建了 `.claude/skills/maintain-claude-md/SKILL.md`：

```markdown
---
name: maintain-claude-md
description: 维护项目 CLAUDE.md 文件。
allowed-tools: Read, Edit, Write, Grep, Glob
---

# 维护 CLAUDE.md

## 写作原则
1. 指令式语言，祈使句，不解释"为什么"。
2. 零废话，不写"项目概述"、"背景介绍"。
3. 信息密度最大化，能一行写完的不拆两行。
4. 扁平结构，最多两级标题。
5. 只写可执行的规则，没有"建议"、"尽量"。
6. 不写 TODO / 开发计划。

## 更新规范
- 读取当前 CLAUDE.md，理解现有结构。
- 增量修改，不重写整个文件。
- 新增规则插入对应 section 末尾。
```

调用方式：`/maintain-claude-md 新增 Redis 缓存相关规则`

更多 Skill 用法参考：[Claude Code Skills Top20](/posts/ai/2026-01-20-claude-code-skills-top20/)

---

## 八、常见问题

### 8.1 CLAUDE.md 要提交到 Git 吗？

**答案：** 要。它是团队共享的 AI 协作规范，和 `.eslintrc` 一样属于项目基础设施。个人偏好用 `CLAUDE.local.md`（自动加入 `.gitignore`）。

### 8.2 CLAUDE.md 和 AGENTS.md 选哪个？

**答案：** 如果只用 Claude Code，写 CLAUDE.md 就够了。如果团队用多个 AI 工具（Cursor、Copilot、Codex 等），建议用 AGENTS.md 写主体内容，CLAUDE.md 做指针或符号链接。

### 8.3 CLAUDE.md 写多长合适？

**答案：** 300 行以内。AI 能稳定遵循的指令上限约 150-200 条（[来源](https://www.builder.io/blog/claude-md-guide)），写太多反而降低遵循率。用 `@` 导入语法拆分到子文件。

### 8.4 README.md 里要不要提 CLAUDE.md？

**答案：** 不需要。README 面向的是人类开发者，CLAUDE.md 是项目内部的 AI 配置文件，就像你不会在 README 里介绍 `.eslintrc` 的内容一样。

---

## 九、总结

| | README.md | CLAUDE.md |
|---|-----------|-----------|
| 一句话 | 给人看的入职手册 | 给 AI 看的工作守则 |
| 核心问题 | "这是什么项目？怎么跑？" | "你必须怎么做？" |
| 写作风格 | 说明文 | 指令集 |
| 行业趋势 | 不变 | 正在向 AGENTS.md 标准收敛 |

两个文件各管各的事。README 写好了，新人能 5 分钟跑起项目。CLAUDE.md 写好了，AI 能按你的规范写代码，不用每次对话都重复"记得 push"、"记得过滤 merchant_id"。

都不难写，但都值得认真写。

---

## 十、相关链接

- [Claude Code GitHub](https://github.com/anthropics/claude-code)（6.26 万 Star）
- [AGENTS.md 规范](https://github.com/agentsmd/agents.md)（1.63 万 Star）
- [OpenClaw](https://github.com/openclaw/openclaw)（12.4 万 Star）
- [Anthropic 官方文档：Manage Claude's memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Claude Code 最佳实践 - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
- [The Complete Guide to CLAUDE.md - Builder.io](https://www.builder.io/blog/claude-md-guide)

---

## 十一、延伸阅读

- [Claude Code 完全指南](/posts/ai/2026-01-14-claude-code-guide/) - 从零开始上手 Claude Code
- [CLAUDE.md 记忆系统详解](/posts/ai/2026-01-12-claudemd-memory-guide/) - 深入理解记忆层级和加载机制
- [Claude Code Skill 开发指南](/posts/ai/2026-01-08-claudecode-skill-guide/) - 编写自定义 Skill
- [Claude Code Skills Top20](/posts/ai/2026-01-20-claude-code-skills-top20/) - 最实用的 20 个 Skill
- [AI 开发工作流](/posts/ai/2026-01-19-ai-dev-workflow/) - Claude Code 驱动的完整开发流程
- [Claude Code 最佳实践](/posts/ai/2026-01-06-claudecode-best-practices/) - 提升 AI 编码效率的实战技巧

---

如果这篇文章对你有帮助，欢迎在评论区分享你的 CLAUDE.md 写法！

---

> 本文更新于 2026 年 1 月 | 基于 Claude Code v1.x 撰写

## 相关阅读

- [Claude Code 记忆术：一个文件让 AI 永远记住你是谁](/zh/posts/ai/2026-01-12-claudemd-memory-guide/) — CLAUDE.md 记忆机制
- [CLAUDE.md 完全指南：让 AI 每次都精准理解你的项目](/zh/posts/ai/2026-02-28-claude-code-claudemd-guide/) — 更完整的 CLAUDE.md 指南
- [CLAUDE.md 最佳实践：我把 90 行砍到 50 行，Agent 表现反而提升 — Harness #2](/zh/posts/ai/2026-03-31-harness-claudemd-guide/) — 精简 CLAUDE.md 的工程方法
- [CLAUDE.md 最佳实践：写出真正有效的配置文件](/zh/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) — 另一视角的最佳实践
- [上下文工程：2026 年最被低估的 AI 开发技能](/zh/posts/ai/2026-03-10-context-engineering-guide/) — CLAUDE.md 背后的底层原理
