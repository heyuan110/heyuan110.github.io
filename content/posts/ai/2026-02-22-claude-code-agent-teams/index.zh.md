+++
date = '2026-02-22T08:00:00+08:00'
draft = false
title = 'Claude Code 多 Agent 协作教程 2026：Agent Teams 配置与实战'
description = '手把手配置 Claude Code Agent Teams：多 Agent 并行开发原理、Team Lead + Teammate 架构、Opus+Sonnet 混合编排省钱、命令速查表，将小时级工作压缩到分钟级。'
toc = true
tags = ['Claude Code', 'Agent Teams', 'AI Coding', 'Multi-Agent', 'Anthropic']
categories = ['AI实战']
keywords = ['Claude Code 多 Agent 协作', 'Claude Code Agent Teams 教程', 'AI 多智能体编程 2026', 'Claude Code 并行开发', 'Agent Teams 配置方法', 'Claude Code 团队协作', 'Opus Sonnet 混合编排', '多 Agent 编程实战']

[[params.faqItems]]
question = "Claude Code Agent Teams 是什么？"
answer = "Agent Teams 是 Anthropic 发布的实验性功能，让多个 Claude Code 实例组成团队并行协作。一个 Team Lead 负责分配任务，多个 Teammate 独立执行并互相通信，将小时级的串行工作压缩到分钟级。"

[[params.faqItems]]
question = "Agent Teams 和 Subagent 有什么区别？"
answer = "Subagent 只能向主 Agent 单向报告结果；Agent Teams 的 Teammate 之间可以直接互发消息、共享任务列表、自主协调。适合需要多人讨论和跨模块协作的复杂开发场景。"

[[params.faqItems]]
question = "Agent Teams 怎么省钱？"
answer = "使用 Opus+Sonnet 混合编排策略：Team Lead 用 Opus 做任务拆分和综合决策，Teammate 用 Sonnet 做具体执行。Sonnet token 成本约为 Opus 的 1/5，整体成本可降低 60% 以上。"

[[params.faqItems]]
question = "Agent Teams 需要什么订阅计划？"
answer = "Agent Teams 需要 Claude Max 订阅（$100/月或 $200/月），因为每个 Teammate 都是独立的 Claude Code 实例，会消耗额外的 token 额度。Pro 计划的额度通常不够用。"
+++

2 月 5 日，Anthropic 随 Claude Opus 4.6 一同发布了 **Claude Code Agent Teams** —— 一项让多个 Claude Code 实例组成团队、并行协作的实验性功能。如果说之前的 Subagent 是"你派出去跑腿的助手"，那 Agent Teams 就是"一支能互相讨论、自主协调的工程小队"。对于需要跨模块开发、多视角审查、并行调试的复杂场景，Agent Teams 可以将小时级的串行工作压缩到分钟级完成。

本文基于[官方文档](https://code.claude.com/docs/en/agent-teams)和实际使用经验，从架构原理到实战案例，完整拆解 Agent Teams 的核心能力。如果你还不熟悉 Claude Code 的基础用法，建议先阅读 [Claude Code 完全指南](/zh/posts/ai/2026-01-14-claude-code-guide/)。

## 什么是 Agent Teams

Agent Teams 的核心架构非常直观：**一个 Team Lead + 多个 Teammate**。

| 组件 | 职责 |
|------|------|
| **Team Lead** | 主 Claude Code 会话，负责创建团队、分配任务、综合结果 |
| **Teammates** | 独立的 Claude Code 实例，各自拥有独立 context window |
| **Task List** | 共享任务列表，支持依赖追踪和自动解锁 |
| **Mailbox** | Agent 间的消息系统，支持点对点和广播通信 |

### 与 Subagent 的关键区别

这是理解 Agent Teams 价值的核心：**Subagent 只能向上报告，Teammate 可以互相通信**。

| 维度 | Subagent | Agent Teams |
|------|----------|-------------|
| **上下文** | 独立 context，结果返回给调用者 | 独立 context，完全自主运行 |
| **通信方式** | 只能向主 Agent 报告结果 | Teammate 之间可以直接互发消息 |
| **协调机制** | 主 Agent 统一管理 | 共享任务列表 + 自协调 |
| **适用场景** | 聚焦任务，只需返回结果 | 需要讨论、协作的复杂工作 |
| **Token 消耗** | 较低，结果摘要返回主 context | 较高，每个 Teammate 独立消耗 |

**通俗理解**：Subagent 像是你派出去的外卖骑手，送完回来报告就行。Agent Teams 像是一个工程小组，成员之间可以随时沟通"你那边接口改了吗？"、"我发现了一个问题，你那边也看看"。

## 快速上手

### 第一步：启用功能

Agent Teams 目前是实验性功能，需要手动启用。有两种方式：

**方式一：环境变量**

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**方式二：settings.json（推荐，持久化）**

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 第二步：用自然语言创建团队

启用后，直接用自然语言告诉 Claude 你需要什么样的团队：

```
创建一个 Agent 团队来开发用户通知功能。
分配三个 Teammate：
- 一个负责后端 API 开发
- 一个负责前端 UI 组件
- 一个负责编写集成测试
```

Claude 会自动创建团队、分配任务列表、启动各个 Teammate。

### 第三步：选择显示模式

Agent Teams 支持两种显示模式：

- **In-process（默认）**：所有 Teammate 运行在同一个终端内。用 `Shift+Down` 在 Teammate 之间切换，用 `Ctrl+T` 查看任务列表。任何终端都能用。
- **Split panes**：每个 Teammate 拥有独立窗格，需要 tmux 或 iTerm2。可以同时看到所有人的输出。

```bash
# 强制使用 in-process 模式
claude --teammate-mode in-process
```

或在 settings.json 中配置：

```json
{
  "teammateMode": "in-process"
}
```

### 第四步：直接与 Teammate 对话

每个 Teammate 都是完整的 Claude Code 会话，你可以随时直接跟某个 Teammate 对话：

- **In-process 模式**：`Shift+Down` 切换到目标 Teammate，直接输入消息
- **Split panes 模式**：点击对应窗格即可交互

## 实战案例

### 场景一：前端 + 后端 + 测试三人协作

这是 Agent Teams 最典型的应用场景 —— 跨层协调开发：

```
创建一个 Agent 团队来实现用户资料编辑功能：

Teammate 1 - 后端开发：
- 设计并实现 PUT /api/users/:id 接口
- 处理数据验证和数据库更新
- 文件范围：src/api/users.ts, src/models/user.ts

Teammate 2 - 前端开发：
- 实现个人资料编辑表单组件
- 对接后端 API，处理表单状态
- 文件范围：src/components/ProfileEdit.tsx, src/hooks/useProfile.ts

Teammate 3 - 测试工程师：
- 为 API 接口编写单元测试
- 为前端组件编写集成测试
- 文件范围：tests/api/users.test.ts, tests/components/ProfileEdit.test.tsx

要求每个 Teammate 完成后互相通知，确保接口契约一致。
```

**为什么有效**：三个 Teammate 各自负责不同的文件集，避免了文件冲突。他们可以通过消息系统确认接口定义，保持前后端契约一致。串行开发可能需要 30-40 分钟，Agent Teams 可以在 10-15 分钟内并行完成。

### 场景二：多假设并行调试

当 bug 原因不明时，Agent Teams 的"竞争假设"模式特别强大：

```
用户反馈应用在发送一条消息后就断开连接。
创建 5 个 Teammate 分别调查不同假设：
1. WebSocket 连接管理问题
2. 认证 token 过期处理
3. 服务端心跳机制
4. 客户端重连逻辑
5. 负载均衡 session 亲和性

让他们像科学辩论一样互相质疑对方的理论，
最终在 findings.md 中记录达成共识的结论。
```

**为什么有效**：单个 Agent 调试容易"锚定"在第一个看起来合理的解释上。多个 Agent 互相质疑，能有效避免确认偏误，最终存活下来的假设更可能是真正的根因。

### 场景三：代码审查 + 文档生成并行

```
创建一个 Agent 团队来审查 PR #142，分配三个审查者：
- 一个聚焦安全性分析（token 处理、输入验证、注入风险）
- 一个聚焦性能影响（N+1 查询、内存泄漏、并发问题）
- 一个聚焦测试覆盖率（边界条件、错误路径、集成测试）

审查完成后，综合所有发现生成审查报告。
```

单个审查者容易偏向某一类问题，多角度并行审查能确保安全、性能、测试覆盖都得到充分关注。

## 高级功能

### 要求 Teammate 先提交方案

对于高风险任务，可以要求 Teammate 在实施前先提交方案由 Lead 审批：

```
派一个架构师 Teammate 重构认证模块，
要求先提交方案等待审批再动手实现。
只批准包含测试计划的方案。
```

Teammate 会进入只读的 Plan 模式，提交方案后由 Lead 审批。被拒绝则修改后重新提交，通过后才开始实施。

### 用 Hooks 强制质量门禁

通过 [Hooks](/zh/posts/ai/2026-01-14-claude-code-guide/) 机制，可以在关键节点插入自动检查：

- **`TeammateIdle`**：Teammate 即将空闲时触发。返回 exit code 2 可以发送反馈让 Teammate 继续工作。
- **`TaskCompleted`**：任务被标记完成时触发。返回 exit code 2 可以阻止完成并发送反馈。

### 指定模型

可以为 Teammate 指定不同的模型，用较便宜的模型处理简单任务：

```
创建 4 个 Teammate 并行重构这些模块。
每个 Teammate 使用 Sonnet 模型。
```

## 最佳实践

### 什么时候该用 Agent Teams

**适合的场景**：
- 工作可以自然地按领域并行拆分（前端/后端/测试）
- 需要多视角同时审查（安全/性能/测试覆盖）
- Bug 原因不明，需要并行探索多个假设
- 新模块开发，各模块间耦合度低

**不适合的场景**：
- 任务是严格串行的（每一步依赖上一步的结果）
- 多人需要编辑同一个文件
- 任务简单到单个 Agent 就能高效完成
- 预算敏感，Token 消耗是主要顾虑

### 任务拆分原则

- **粒度适中**：太小则协调开销超过收益，太大则 Teammate 脱节太久
- **文件隔离**：每个 Teammate 负责不同的文件集，避免写冲突
- **明确交付物**：每个任务应产出可验证的成果（一个函数、一个测试文件、一份报告）
- **建议每个 Teammate 分配 5-6 个任务**，保持忙碌且便于 Lead 调度

### Token 成本考量

Agent Teams 的 Token 消耗大约是单会话的 **3-4 倍**。每个 Teammate 拥有独立的 context window，消耗独立计算。

**成本优化策略**：
- 先用单会话评估任务复杂度，确认值得并行再启用 Agent Teams
- 为简单子任务指定 Sonnet 等较便宜的模型
- 及时关闭完成工作的 Teammate，避免空闲消耗
- 新手建议从 2-3 个 Teammate 起步，逐步增加

## 与其他并行方案对比

Claude Code 提供了三种并行工作方式，各有适用场景。关于 Worktree 的详细用法，可以参考 [Claude Code Worktree 实战指南](/zh/posts/ai/2026-02-20-claude-code-worktree/)。

| 维度 | Agent Teams | Subagent | Worktree |
|------|-------------|----------|----------|
| **通信** | Teammate 间直接通信 | 只能向主 Agent 报告 | 无自动通信 |
| **协调** | 共享任务列表，自协调 | 主 Agent 统一管理 | 完全手动 |
| **并发安全** | 文件锁防冲突 | 单 session 内安全 | Git 分支隔离 |
| **Token 消耗** | 高（3-4x） | 中 | 低（独立会话） |
| **适用场景** | 需要讨论协作的复杂任务 | 聚焦的独立子任务 | 长期并行的独立功能 |
| **学习曲线** | 中等 | 低 | 低 |

**选型建议**：
- 子任务独立、只需要结果 -> **Subagent**
- 需要跨角色沟通和协调 -> **Agent Teams**
- 独立功能分支、长期并行开发 -> **Worktree**

更多 Claude Code 的最新功能变化，可以查看 [Claude Code 2 月更新](/zh/posts/ai/2026-02-22-claude-code-february-updates/)。

## 命令速查表

| 操作 | 命令 / 按键 |
|------|-------------|
| 启用 Agent Teams | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| 切换 Teammate（in-process） | `Shift+Down` |
| 查看任务列表 | `Ctrl+T` |
| 进入 Teammate 会话 | `Enter`（选中 Teammate 后） |
| 退出 Teammate 会话 | `Escape` |
| 强制 in-process 模式 | `claude --teammate-mode in-process` |
| 关闭某个 Teammate | 告诉 Lead："关闭 researcher Teammate" |
| 清理团队资源 | 告诉 Lead："Clean up the team" |
| 列出 tmux 会话 | `tmux ls` |
| 杀掉残留 tmux 会话 | `tmux kill-session -t <session-name>` |

## 常见问题

### Agent Teams 支持 VS Code 终端的 Split panes 模式吗？

不支持。Split panes 模式需要 tmux 或 iTerm2。VS Code 集成终端、Windows Terminal、Ghostty 均不支持 Split panes。但 **In-process 模式在任何终端都能正常工作**，功能完全一致，只是所有 Teammate 共享同一个终端窗口。

### Teammate 可以再创建自己的团队吗？

不可以。Agent Teams **不支持嵌套**。只有 Team Lead 可以管理团队，Teammate 不能再 spawn 自己的 Teammate 或创建子团队。同样，一个 Lead 同一时间只能管理一个团队。

### 使用 Agent Teams 时遇到 Teammate 不出现怎么办？

几个排查方向：
1. In-process 模式下，Teammate 可能已在运行但不可见，按 `Shift+Down` 切换查看
2. 确认任务复杂度足够 —— Claude 会根据任务判断是否需要创建团队
3. 如果使用 Split panes，确认 tmux 已安装：`which tmux`
4. iTerm2 用户需确认 `it2` CLI 已安装且 Python API 已启用

### Token 消耗 3-4x，值得吗？

取决于场景。对于代码审查、多假设调试、跨层特性开发这类天然并行的工作，Agent Teams 能将 1-2 小时的串行工作压缩到 15-20 分钟。**时间价值远大于额外的 Token 成本**。但对于简单的顺序任务，单会话 + Subagent 是更经济的选择。如果你对 Claude Code 的其他高级能力也感兴趣，推荐阅读 [Superpowers 深度解析](/zh/posts/ai/2026-02-01-superpowers-deep-dive/)。

## 总结

Agent Teams 是 Claude Code 从"单兵作战"迈向"团队协作"的重要一步。它的核心价值不仅在于并行加速，更在于**多视角协作**带来的质量提升 —— 多个 Agent 互相审查、质疑、补充，比单个 Agent 反复思考更容易找到盲区。

目前 Agent Teams 仍处于实验阶段，存在 session 恢复、任务状态同步等已知限制。但对于跨层开发、多假设调试、并行审查这些高价值场景，它已经展现出了显著的效率提升。建议从简单的审查和研究任务开始尝试，逐步积累经验后再用于更复杂的开发场景。

## 相关阅读

- [Claude Code --teammate-mode 详解：让多个 Agent 真正协作起来](/zh/posts/ai/2026-02-28-claude-code-teams-guide/) — Agent Teams 机制的另一视角
- [Sub-Agent 架构设计：什么时候该拆子 Agent，Opus/Sonnet/Haiku 怎么分工](/zh/posts/ai/2026-04-13-harness-subagent-architecture/) — 拆 Agent 的工程化方法
- [多智能体编排：4 种真正有效的架构模式](/zh/posts/ai/2026-02-26-multi-agent-orchestration/) — 多 Agent 的编排模式
- [OpenClaw 多 Agent 配置实战：别让 LLM 做编排](/zh/posts/ai/2026-04-02-openclaw-multi-agent-setup-guide/) — 在 Claude Code 之外的多 Agent 落地
- [Harness Engineering 实战：模型是 AI Agent 里最不重要的部分](/zh/posts/ai/2026-03-30-harness-engineering-guide/) — 多 Agent 系统背后的 harness 设计
