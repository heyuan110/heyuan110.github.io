+++
date = '2026-03-13T15:00:00+08:00'
draft = false
title = 'GitHub Agent HQ 实战指南：在 VS Code 中同时驾驭三大 AI 编程助手'
description = '手把手教你配置 GitHub Agent HQ，在 VS Code 里同时运行 Claude、Codex 和 Copilot，掌握多 Agent 协作工作流，附实际场景和工具对比。'
toc = true
tags = ['GitHub Copilot', 'AI Coding Tools', 'VS Code', 'Claude', 'Multi-Agent']
keywords = ['GitHub Agent HQ 教程', 'VS Code 多 Agent 开发', 'Claude Codex Copilot 同时使用', 'AI 编程助手对比', 'Agent HQ 设置指南']
+++

![GitHub Agent HQ multi-agent development dashboard showing Claude, Codex, and Copilot panels in VS Code](cover.webp)

用一个 AI 编程助手写代码已经很高效了。但如果能同时跑三个——对比它们的思路、发挥各自的长处、挑出最优解——那写代码的方式会发生根本性变化。

GitHub Agent HQ 让这件事在 VS Code 里就能完成。这个产品在 GitHub Universe 2025 上首次亮相，2026 年 2 月进入公测，支持在同一个界面里运行 [Anthropic Claude](https://www.anthropic.com/)、[OpenAI Codex](https://openai.com/index/codex/) 和 [GitHub Copilot](https://github.com/features/copilot)。你可以把它理解为 AI Agent 的指挥中心：分配任务、监控进度、对比结果、合并最佳方案，全程不用切换工具。

这篇指南会带你完成 Agent HQ 的配置，搭建高效的多 Agent 工作流，并帮你判断什么时候该用它，什么时候 Claude Code CLI 或 Cursor 更合适。

## GitHub Agent HQ 是什么？

Agent HQ 是 GitHub 推出的多 AI Agent 编排平台，横跨 GitHub 网页端、VS Code 和 GitHub 移动端。你不再被锁定在某一个 AI 助手上，而是拥有一支 Agent 团队，可以独立或并行地分配任务。

核心理念很简单：**不同的 Agent 各有所长**，与其依赖一个模型干所有事，不如利用它们的差异化优势拿到更好的结果。

### 你能得到什么

| 功能 | 说明 |
|------|------|
| **多 Agent 接入** | 在同一界面运行 Claude、Codex 和 Copilot |
| **会话管理** | 监控和管理多个并发 Agent 会话 |
| **Agent 对比** | 把同一任务分给多个 Agent，横向比较输出 |
| **本地 + 云端模式** | 交互式本地 Agent 或自主运行的云端 Agent |
| **统一管控** | 企业级权限控制、审计日志和使用指标 |
| **原生 GitHub 集成** | Agent 产出直接变成 PR、评论和 Issue 更新 |

### 当前支持的 Agent（2026 年 3 月）

- **GitHub Copilot** — GitHub 原生 Agent，与平台深度集成
- **Claude**（Anthropic）— 擅长多文件重构、架构分析和细致的代码审查
- **Codex**（OpenAI）— 代码生成快、算法实现强、原型搭建效率高

Google、Cognition 和 xAI 的 Agent 已在规划中，预计后续版本加入。

## 前置条件和订阅要求

开始之前，确认以下几项：

1. **VS Code v1.109 或更高版本** — 2026 年 1 月的更新加入了多 Agent 支持
2. **符合要求的 GitHub 订阅**：
   - **Copilot Pro+** — 三个 Agent 全部可用
   - **Copilot Enterprise** — 全部可用，外加企业管控功能
   - Copilot Individual 和 Business 目前还不支持 Claude 和 Codex（计划 2026 年内开放）
3. **VS Code 中已安装 GitHub Copilot 扩展**

每个 Agent 会话会消耗一次高级请求配额。

## 在 VS Code 中配置 Agent HQ

### 第一步：更新 VS Code

确认版本号在 1.109 以上：

```
帮助 → 关于 → 版本 1.109+
```

如果版本较低，去 [code.visualstudio.com](https://code.visualstudio.com/) 下载最新版。

### 第二步：安装必要扩展

打开扩展面板（`Ctrl+Shift+X` / `Cmd+Shift+X`），安装：

- **GitHub Copilot**（所有 Agent 的基础）
- **GitHub Copilot Chat**（用于对话交互）

如果需要 Codex 支持，按提示安装 **OpenAI Codex** 扩展即可。

### 第三步：启用 Agent 功能

打开 VS Code 设置（`Ctrl+,` / `Cmd+,`），添加以下配置：

```json
{
  "chat.agent.enabled": true,
  "github.copilot.chat.claudeAgent.enabled": true
}
```

> **注意：** 在企业环境中，`chat.agent.enabled` 可能由组织统一管理。如果发现设置被锁定，请联系管理员。

### 第四步：验证配置

打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`），搜索 **"Agent Sessions"**。看到 Agent Sessions 视图就说明配置成功了。

## 理解三种 Agent 模式

Agent HQ 支持三种执行模式。选对模式比选对模型更重要：

### 本地 Agent

在本机运行，拥有完整的工作区访问权限。适合：
- 需要实时引导 Agent 的探索性编程
- 需要快速反馈循环的任务
- 上下文频繁变化的调试场景

**启动方式：** 打开 Chat 视图 → 点击 `+` 下拉菜单 → 选择 Agent 类型（Copilot、Claude 或 Codex） → 选择 "Local"

### 云端 Agent

在远程基础设施上运行，与 GitHub PR 深度集成。适合：
- 能提前描述清楚、不需要盯着的任务
- 需要团队可见性的工作（结果直接变成 PR）
- 耗时较长的任务

**启动方式：** 同样的下拉菜单 → 选择 Agent → 选择 "Cloud"

### 后台 Agent（Copilot CLI）

在后台通过 Git worktree 自主运行。适合：
- 不希望影响当前工作的独立改动
- 批量任务，如全项目更新依赖或修复 lint 错误
- 你想委派出去继续做别的事

**启动方式：** 在 Copilot CLI 会话中使用 `/delegate` 命令

| Agent 模式 | 运行位置 | 交互方式 | 适用场景 |
|-----------|---------|---------|---------|
| 本地 | 本机 | 交互式，实时 | 探索性任务、调试 |
| 云端 | 远程服务器 | 异步，自主运行 | 明确的任务、团队协作 |
| 后台 | 本机（CLI） | 异步，无人值守 | 独立改动、批量操作 |

## 真正好用的多 Agent 工作流

Agent HQ 的价值不在于有三个 Agent，而在于你知道什么时候用哪个、怎么配合。以下是实测有效的几种工作流：

### 工作流一：竞争式起草

把同一个任务分配给三个 Agent，对比它们的方案。

**适用场景：** 架构决策、复杂重构，或者存在多种合理解法的任务。

**具体操作：**

1. 开三个 Agent 会话（每个 Agent 一个）
2. 给出相同的指令——例如："重构认证模块，支持 OAuth2 和 API Key 两种认证方式"
3. 让三个 Agent 并行工作
4. 对比输出：看代码结构、错误处理方式、测试覆盖度
5. 从每个方案中挑出最好的部分进行组合

这种方式特别有价值，因为 Claude 通常产出结构清晰、文档详尽的方案；Codex 往往给出更精简的实现；而 Copilot 能利用对你仓库的深度理解做出更贴合上下文的输出。

### 工作流二：专家流水线

根据各 Agent 的强项，在任务的不同阶段使用不同的 Agent。

**示例流水线：**

```
Claude（规划）  →  Codex（实现）  →  Copilot（集成）
```

1. **Claude** — "为我们的 API 设计一个缓存层。对比 Redis 和内存缓存方案，定义接口，列出需要处理的边界情况。" Claude 最擅长这类架构分析。
2. **Codex** — "根据这个设计方案实现缓存层：[粘贴 Claude 的输出]。" Codex 把规格说明变成代码的速度很快。
3. **Copilot** — "把这个缓存模块集成到现有的 API handler 中，并更新测试。" Copilot 对你的仓库结构最熟悉。

### 工作流三：交叉审查

用一个 Agent 来审查另一个 Agent 的输出。

```
Agent A（写代码）  →  Agent B（审查和质疑）
```

这能发现单个 Agent 的盲区。举个例子：

1. 让 Codex 生成一个数据库迁移脚本
2. 让 Claude 审查其中的边界情况、数据完整性风险和回滚安全性
3. 根据 Claude 的审查意见进行修复

### 工作流四：并行调研 + 实现

让子 Agent 做调研，主 Agent 专注实现。

1. 启动一个本地 Claude 会话来做主要开发
2. 启动一个 Copilot 子 Agent 扫描代码库中的现有模式和规范
3. 启动一个 Codex 子 Agent 查阅相关库的文档
4. 把调研结果反馈给 Claude 的上下文

VS Code 的子 Agent 功能会隔离各 Agent 的上下文，并行执行不会干扰你的主会话。

## Agent HQ vs Claude Code CLI vs Cursor vs 独立 Copilot

如果你已经在用这些工具，可能会想知道 Agent HQ 到底是锦上添花还是画蛇添足。以下是客观对比：

### Agent HQ vs Claude Code CLI

[Claude Code CLI](/posts/ai/2026-01-14-claude-code-guide/) 是 Anthropic 推出的终端编程 Agent，不依赖任何 IDE。

| 维度 | Agent HQ（VS Code 中的 Claude） | Claude Code CLI |
|------|-------------------------------|-----------------|
| **界面** | VS Code 图形界面，可视化 diff | 终端，纯文本 |
| **多 Agent** | 同时运行 Claude + Codex + Copilot | 仅 Claude |
| **工作流** | 点击操作，会话面板 | 命令驱动，可脚本化 |
| **上下文** | VS Code 工作区上下文 | 完整文件系统 + Shell 访问 |
| **Hook 和自动化** | 有限 | 丰富（前后置 Hook、[worktree](/posts/ai/2026-02-20-claude-code-worktree/)） |
| **适合** | 团队协作、可视化工作流、Agent 对比 | 高级用户、自动化、CI/CD 集成 |

**结论：** 想要多 Agent 对比和可视化会话管理，Agent HQ 更强。想要极致的控制力、脚本化能力和[深度自动化](/posts/ai/2026-02-18-claude-code-hooks-guide/)，Claude Code CLI 依然是更好的选择。

### Agent HQ vs Cursor

[Cursor](/posts/ai/2026-03-08-cursor-setup-guide/) 是基于 VS Code 魔改的 AI 原生 IDE，有自己的 Agent 模式。

| 维度 | Agent HQ | Cursor |
|------|----------|--------|
| **Agent 选择** | Claude、Codex、Copilot | 多种模型但单 Agent 工作流 |
| **IDE** | 标准 VS Code | VS Code 分支（独立应用） |
| **扩展** | 完整的 VS Code 扩展市场 | 大部分 VS Code 扩展可用 |
| **多 Agent** | 原生支持，一等公民 | 不支持 |
| **价格** | Copilot Pro+（$39/月） | Cursor Pro（$20/月）+ API 费用 |

**结论：** 如果多 Agent 工作流对你重要，Cursor 目前没有对等方案。如果你更喜欢紧密集成的单 Agent 体验和优秀的行内补全，[Cursor 仍然很强](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/)。

### Agent HQ vs 独立 Copilot

Agent HQ 本质上是 Copilot 的升级版。之前 Copilot 能做的事一样都没少，只是多了 Claude 和 Codex。如果你的订阅等级够，没有理由不升级。

更详细的工具对比可以参考我们的 [2026 年 AI 编程 Agent 全面评测](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/)。

## 实用建议和最佳实践

### 1. 先用好一个 Agent，再扩展到三个

不要一上来就每个任务都开三个 Agent。先分别熟悉它们的特点：

- **Copilot** — 自动补全快，擅长仓库特有的代码模式，行内体验最好
- **Claude** — 考虑周全，善于分析取舍，多文件改动能力强
- **Codex** — 生成速度快，算法任务在行，输出简洁

了解各自的强项之后，你自然会知道什么时候该用多 Agent 协作。

### 2. 多 Agent 任务要写好 Prompt

对比 Agent 时，要给出一模一样的、具体的指令。模糊的 Prompt 只会产生无意义的差异。别这样写：

```
# 太模糊了——Agent 会因为随机原因产生不同结果
"改善错误处理"
```

要这样写：

```
# 具体明确——差异才能体现真正的思路差别
"重构 src/api/handlers.ts 中的错误处理：
1. 用类型化错误类替换通用 try/catch
2. 为瞬态网络故障添加重试逻辑
3. 返回符合 ErrorResponse 类型的结构化错误响应
4. 为每个错误路径编写单元测试"
```

### 3. 用云端 Agent 做过夜任务

下班前把定义清楚的任务交给云端 Agent，第二天早上回来直接看 PR 审查结果。这种方式特别适合：

- 带测试验证的依赖更新
- 数据迁移脚本
- 文档生成
- 测试覆盖率提升

### 4. 注意会话配额

每个 Agent 会话消耗一次高级请求。每个小任务都开三个 Agent 会很快烧光配额。多 Agent 工作流应该留给那些真正需要多角度思考的重要决策。

### 5. 永远不要盲目接受 Agent 的输出

GitHub 官方公告说得很直白：*"Agent 仍然会犯错。正因如此，它们的输出设计为可审查、可对比、可质疑的，而不是无脑接受。"*

Agent HQ 基于审查的工作流（草稿 PR、行内评论）就是围绕这个原则设计的。Agent 产出的每一行代码都应该经过和人写的代码一样的 Code Review 流程。

## 企业管控功能

对于团队和组织，Agent HQ 提供了一套管控工具，解决 AI 编程工具最大的顾虑——控制权：

- **权限控制** — 管理员定义团队可以使用哪些 Agent 和模型
- **审计日志** — 完整的活动追踪，满足合规和问责需求
- **代码质量集成** — 自动对 Agent 输出进行安全性和可维护性检查（公测中）
- **使用指标看板** — 追踪组织内的采纳率和效果
- **策略执行** — 设定哪些任务 Agent 可以自主完成，哪些需要人工审批

这套管控层是 Agent HQ 的重要差异化优势。Claude Code CLI 和 Cursor 把权限管理交给了开发者个人，Agent HQ 把它集中化了——在大规模团队中这很重要。

## 当前局限性

Agent HQ 目前还在公测阶段，有一些需要了解的不足：

1. **订阅门槛** — Claude 和 Codex 要求 Copilot Pro+（$39/月）或 Enterprise，对很多个人开发者来说偏贵
2. **会话配额** — 每个 Agent 会话消耗高级请求，频繁使用三 Agent 工作流开销不小
3. **跨会话无共享上下文** — 各会话独立运行没有共享记忆，Agent 之间传递上下文需要手动操作
4. **云端 Agent 启动慢** — 云端会话可能需要几分钟才能启动，不适合快速提问
5. **Agent 定制能力有限** — 除了 Prompt 工程之外无法调整 Agent 行为（不像 [Claude Code 的 CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) 或[自定义 Skills](/posts/ai/2026-02-28-claude-code-skills-guide/)）

## 常见问题

**Q：必须三个 Agent 都用才有价值吗？**

不是。哪怕只用两个——比如 Copilot 做自动补全、Claude 做复杂重构——都能明显感受到价值。三 Agent 对比是进阶玩法，不是必须的。

**Q：Copilot Free 或 Copilot Individual 能用 Agent HQ 吗？**

目前 Claude 和 Codex 的接入需要 Copilot Pro+ 或 Enterprise。低级别订阅可以用 Copilot 的 Agent 模式，但没有多 Agent 能力。

**Q：Agent HQ 能替代 Claude Code CLI 吗？**

不完全能。Claude Code CLI 有更深的终端集成、[Hook 自动化](/posts/ai/2026-02-18-claude-code-hooks-guide/)和 [worktree 工作流](/posts/ai/2026-02-28-claude-code-worktree-guide/)，这些 Agent HQ 做不到。两者服务于不同的工作流——Agent HQ 适合可视化多 Agent 协作，CLI 适合自动化和脚本化。

**Q：Agent HQ 怎么处理代码隐私？**

Agent 的输出通过 GitHub 基础设施处理，隐私保障与 Copilot 一致。企业客户有额外的数据驻留和保留控制。详情请查看 [GitHub 的 Copilot 隐私文档](https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-policies-and-features-for-copilot-in-your-organization)。

**Q：Agent HQ 只能在 VS Code 里用吗？**

不是。你可以在 github.com（仓库里的 Agents 标签）、GitHub 移动端和 VS Code 中启动 Agent 会话。云端 Agent 的结果在所有平台同步。

## 延伸阅读

- [2026 年 AI 编程 Agent 全面评测（7 款工具实测）](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/) — Agent HQ 各 Agent 的单独表现对比
- [Claude Code vs GitHub Copilot 2026：两个都用之后的选择建议](/posts/ai/2026-03-05-claude-code-vs-copilot/) — Copilot 与 Claude 的详细对比
- [Claude Code vs Codex CLI：8 个维度正面对决](/posts/ai/2026-02-19-claude-code-vs-codex/) — Claude 与 Codex 深度对比
- [Claude Code vs Cursor vs Windsurf 2026：速度、成本与控制力](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/) — 更广泛的 AI IDE 对比
- [GitHub Copilot vs Claude Code vs Cursor：2026 年三方对比](/posts/ai/2026-02-28-copilot-vs-claude-vs-cursor/) — 三款工具横评
