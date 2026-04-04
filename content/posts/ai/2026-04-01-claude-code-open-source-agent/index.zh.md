+++
date = '2026-04-01T10:00:00+08:00'
draft = false
title = 'Claude Code 开源风波：源码泄露到社区重写的全过程'
description = '深度技术分析 Claude Code 开源版 — 基于 Claude Code 泄露架构的 Python + Rust 开源重写。涵盖源码泄露事件始末、架构对比、法律风险评估，以及是否值得从 Claude Code 切换。'
toc = true
tags = ['Claude Code 开源版', 'Open Source', 'AI Coding Tools', 'Claude Code', 'Agent Framework']
keywords = ['Claude Code 开源版 评测', 'Claude Code 源码泄露', '开源 AI 编程工具', 'Claude Code 开源版 对比 Claude Code', 'AI Agent 框架', '代理架构']

[params]
  faq = [
    ['Claude Code 开源版 是什么？', 'Claude Code 开源版 是一个用 Python 和 Rust 编写的开源 AI 编程代理框架。它是在 2026 年 3 月 Anthropic 意外泄露 Claude Code 源码后，基于公开架构模式进行的全新重写。'],
    ['使用 Claude Code 开源版 合法吗？', 'Claude Code 开源版 声称是洁净室实现，没有直接复制专有代码。但法律风险尚未经过司法检验，建议个人研究使用风险较低，商业使用需谨慎评估。'],
    ['Claude Code 开源版 和 Claude Code 有什么区别？', 'Claude Code 开源版 用 Python + Rust 编写（非 TypeScript），支持多个 LLM 提供商（非仅 Claude），采用 MIT 开源协议。Claude Code 则是 Anthropic 官方维护的成熟商业产品。'],
    ['我该从 Claude Code 切换到 Claude Code 开源版 吗？', '对大多数开发者来说不建议切换。Claude Code 更稳定、生态更完善。Claude Code 开源版 更适合研究者、框架开发者，以及需要完全控制代理架构或使用非 Claude 模型的场景。']
  ]
+++

![Claude Code 开源版 开源代理框架可视化](cover.webp)

2026 年 3 月 31 日凌晨，一个被遗忘的 `.npmignore` 配置项，把 Anthropic 旗下 Claude Code 的 51.2 万行 TypeScript 源码原封不动地推送到了 npm 公共仓库。这次意外让整个 AI 编程工具领域最核心的"黑箱"——连接大模型与工具链的 Agent 控制层——彻底暴露在阳光下。

两天后，**Claude Code 开源版** 以"洁净室重写"的姿态上线 GitHub，瞬间成为 GitHub 历史上涨星最快的项目，首日突破 10 万星标。这篇文章从技术角度拆解这个项目：它到底做了什么、架构上有什么独到之处、以及你是否应该关注它。

## 源码泄露事件回顾

安全研究员 **Chaofan Shou** 最先发现 Claude Code 的 npm 包中附带了一个 59.8 MB 的 source map 文件，其中完整包含了约 1,906 个未经混淆的 TypeScript 源文件。

Anthropic 确认这是一次[发布打包错误](https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/)，而非安全入侵。但事态的发展远超预期：

- **镜像仓库在几分钟内扩散**，GitHub 上的备份被 fork 超过 4.15 万次
- **同一时段 npm 还遭遇了 axios 供应链攻击**——3 月 31 日 UTC 时间 00:21 至 03:29 之间安装 Claude Code 的用户可能拉到了含远程木马的恶意依赖
- **核心架构被彻底公开**：单一 Agent 循环、40+ 工具集、按需加载的 Skill 系统、上下文压缩、子代理生成、任务依赖图、Worktree 隔离——全部以源码形式展现

社区反应两极分化。一部分人认为 CLI 工具本就该开源——毕竟 Google 的 Gemini CLI 和 OpenAI 的 Codex 都已经开源。另一部分人则担忧基于泄露代码构建项目的知识产权风险。

## Claude Code 开源版 到底是什么

Claude Code 开源版 的作者是韩国开发者 **Sigrid Jin**（GitHub: [@instructkr](https://github.com/instructkr)），几周前他还参加了 Claude Code 在旧金山举办的一周年活动。泄露事件发生后，他通宵利用 oh-my-codex（一个基于 OpenAI Codex 的编排工具）完成了初始版本。

项目定位为**洁净室重写**——基于公开可观察到的架构模式重新实现，不直接复制专有代码。这个定位在法律上是否站得住脚，我后面会详细讨论。

### 技术架构

代码库采用双语言架构：

| 组件 | 语言 | 占比 | 职责 |
|------|------|------|------|
| Agent 编排层 | Python | 27.1% | LLM 集成、命令解析、工具调度 |
| 运行时执行层 | Rust | 72.9% | 高性能执行、内存安全保证 |

Rust 层组织为 **6 个 crate 的工作空间，包含 16 个运行时模块**，目标是达到生产级性能。`dev/rust` 分支跟踪正在进行的迁移工作。

### 核心能力

- **19 个权限控制工具**：文件读写、Bash 执行、Git 操作、网页抓取、LSP 集成、Notebook 编辑、子代理生成
- **15 个斜杠命令**：会话管理、模型切换、成本追踪、上下文压缩
- **多模型支持**：提供商无关设计，支持 Claude、OpenAI 及本地模型——这是与 Claude Code 最核心的差异
- **MCP 集成**：6 种传输类型、自动名称规范化、OAuth 支持。关于 MCP 的安全考量，可参考我的 [MCP 安全分析](/posts/ai/2026-03-10-mcp-security-2026/)

## 架构深度对比

我长期使用 Claude Code，也研究过其[代理架构原理](/posts/ai/2026-04-04-harness-engineering-guide/)。以下是两者在关键架构层面的对比。

### Agent 循环

两个系统遵循相同的基本模式：接收输入 → 构建带上下文的 Prompt → 调用 LLM → 解析工具调用响应 → 执行工具 → 结果反馈到下一轮迭代。

Claude Code 是一个紧耦合的 TypeScript 单体包，与 Anthropic API 深度绑定。Claude Code 开源版 将其拆分为 Python 编排层 + Rust 运行时，并实现了显式的模型提供商抽象。

### 工具系统

Claude Code 内置约 40 个工具，Claude Code 开源版 目前实现了 19 个，权限模型类似——三级访问控制（允许/拒绝/询问），支持按工具粒度的策略配置。工具数量的差距既有主动精简的因素（去掉低频工具），也因为项目仍在成熟中。

### 上下文管理

两者都通过**会话记录压缩**来管理上下文窗口——对旧的对话轮次进行摘要以控制 Token 用量。Claude Code 的实现更精细，具有多层记忆和持久化知识图谱。Claude Code 开源版 有基础的会话持久化，但深度不及 Claude Code 的[记忆策略](/posts/ai/2026-01-31-openclaw-memory-strategy/)。

### 多代理编排

Claude Code 开源版 称之为 "swarms"——主代理为独立子任务生成子代理并行执行。Claude Code 也有类似的[子代理机制](/posts/ai/2025-12-26-claudecode-skill%26subagent/)，不过生成模型有所不同。实际生产场景中，Claude Code 的子代理系统经过了更充分的验证。

### 各自优势一览

**Claude Code 开源版 的优势：** 完全开源可审查、多模型支持、Rust 性能层、MIT 协议自由使用

**Claude Code 的优势：** 产品打磨成熟度高、与 Claude 模型深度优化、生态完善（Skills、Hooks、CLAUDE.md）、有官方团队持续维护

## 法律和伦理风险

这是绕不开的核心问题。

**洁净室抗辩的困境：** 严格意义上的洁净室开发要求实现者从未接触过原始专有代码。但 Claude Code 开源版 恰恰是在看到泄露架构后、直接作为回应而构建的——这让洁净室声明打了折扣。

**独立审计的发现：** 项目声称代码审计确认不包含 Anthropic 的专有代码或模型权重。这回答了最窄的法律问题（有没有直接复制），但没回答更宽的问题（架构本身是否构成受保护的商业秘密）。

**实际风险评估：**
- **版权法**保护的是表达形式而非思想。用不同语言重新实现架构模式，通常被视为合法
- **商业秘密**一旦被公开披露（哪怕是意外），保护效力会大幅削弱
- **截至 2026 年 4 月**，Anthropic 没有对 Claude Code 开源版 或镜像仓库发起 DMCA 下架

我的判断：个人研究和学习使用，风险很低。基于它构建商业产品，在法律环境明确之前需要额外谨慎。Anthropic 的沉默不等于默许。

## 你该用 Claude Code 开源版 吗？

**适合使用 Claude Code 开源版 的场景：**
- 研究 Agent 架构的学术/技术探索
- 为特定领域构建自定义代理框架
- 需要多模型提供商支持
- 想深入了解生产级 AI 编程代理的内部运作
- 参与开源 AI 工具生态建设

**应该继续用 Claude Code 的场景：**
- 日常开发需要稳定可靠的工具
- 企业环境中有法律合规要求
- 已深度依赖 Claude Code 生态（Skills、Hooks、CLAUDE.md）
- 稳定性优先于可定制性

更多 AI 编程工具的横向对比，可以参考我的 [2026 年 AI 编程代理对比](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/)。

## 对 AI 工具生态的启示

Claude Code 开源版 现象揭示了一个重要事实：**Agent 控制层不是护城河，模型才是。**

Google Gemini CLI 开源了，OpenAI Codex 开源了，现在 Claude Code 的架构也被独立重现了。趋势很清楚——连接 LLM 和你的文件系统的那层"壳"正在走向通用化。

真正的价值在于：模型的代码推理能力、Prompt 工程的精细度、生态集成的深度、以及边界情况的处理能力。Anthropic 的竞争优势从来不是那个 TypeScript CLI 包装器，而是 Claude 理解复杂代码库的能力。这一点没有改变。

## 快速上手

```bash
git clone https://github.com/instructkr/claw-code.git
cd claw-code
pip install -r requirements.txt
python src/main.py
```

**注意事项：**
- 项目仍在活跃开发中，随时可能有破坏性变更
- Rust 迁移进行中，部分模块仍为纯 Python
- 社区文档相比 Claude Code 还很薄弱
- MCP Server 兼容性可能与 Claude Code 的实现有差异

## 总结

Claude Code 开源版 是一个技术上令人印象深刻的项目，诞生于一次意外事件。它证明了 Agent 控制层的模式已经被充分理解，能在几天内被重新实现。但技术上能做到和生产可用之间，差距仍然很大。

对大多数开发者来说，Claude Code 仍然是日常工作的更优选择。但 Claude Code 开源版 作为参考实现、研究平台和行业风向标，有着不可忽视的价值。10 万+ 的星标不只是跟风——它反映了开发者对 AI 代理透明性的真实需求。

问题已经不是 Agent 架构该不该开源，而是整个行业会多快走到那一步。

---

*延伸阅读：*
- [代理架构工程：AI 编程工具背后的设计原理](/posts/ai/2026-04-04-harness-engineering-guide/)
- [Claude Code 完全指南](/posts/ai/2026-01-14-claude-code-guide/)
- [2026 年 AI 编程代理横向对比](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/)
- [MCP 安全分析 2026](/posts/ai/2026-03-10-mcp-security-2026/)
