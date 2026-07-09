+++
date = '2026-02-20T11:00:00+08:00'
draft = false
title = 'MCP 协议全面解析：AI 连接万物的通用标准'
description = 'MCP 协议（Model Context Protocol）被称为 AI 领域的 USB-C：2024 年 11 月由 Anthropic 发布，现已捐赠 Linux Foundation，SDK 月下载破 9700 万。详解架构设计、六大核心能力与 Function Calling 对比。'
toc = true
tags = ['MCP', 'Model Context Protocol', 'AI Architecture', 'Claude Code']
categories = ['AI Guides']
keywords = ['MCP 协议', 'Model Context Protocol', 'MCP Server', 'MCP Apps', 'AI 工具集成', 'Agentic AI Foundation']
+++

当 AI 模型需要查询数据库、调用 API、读取文件时，过去每个模型提供商都有自己的一套接口方式，开发者不得不为不同平台重复编写集成代码。MCP（Model Context Protocol，模型上下文协议）的出现彻底改变了这一局面——它被称为"AI 领域的 USB-C"，为 AI 应用连接外部系统提供了一个通用的开放标准。

从 2024 年 11 月 Anthropic 首次发布，到如今捐赠给 Linux Foundation、获得 OpenAI 和 Google 等巨头的共同支持，MCP 已经从一个内部实验迅速演变为行业标准。SDK 月下载量突破 9700 万次，公开运行的 MCP Server 超过万个，几乎所有主流 AI 平台都已接入支持。

本文将从协议架构、核心能力、最新的 MCP Apps 功能、与 Function Calling 的对比，到实际开发实践，对 MCP 进行一次全面的梳理和解析。

## MCP 是什么

### 通俗解释

想象一个场景：你有一台笔记本电脑，需要连接显示器、键盘、移动硬盘等各种外设。如果每个外设都需要不同的接口和驱动，使用体验将非常糟糕。USB 协议的出现统一了这一切——一个接口，连接万物。

MCP 在 AI 领域扮演着类似的角色。过去，让 AI 模型访问 GitHub 仓库、查询 PostgreSQL 数据库、调用 Slack 消息，每个集成都需要写一套定制代码。MCP 定义了一个标准化的协议，让任何 MCP 兼容的 AI 应用都能与任何 MCP Server 通信，无论背后连接的是什么工具或服务。

### 技术定义

MCP 是一个基于 JSON-RPC 2.0 的开放协议，定义了 AI 应用（Client）与外部能力提供方（Server）之间的标准化通信方式。它规定了如何发现能力、如何调用工具、如何传递上下文，以及如何处理双向交互。

协议的核心设计理念是：

- **解耦**：AI 模型与工具实现完全分离，互不依赖
- **标准化**：一次开发的 MCP Server，可被所有兼容客户端使用
- **安全性**：内置权限控制和沙箱机制
- **可组合**：多个 MCP Server 可同时挂载，能力自由组合

## MCP 的架构设计

MCP 采用经典的 Client-Server 架构，通过 Transport 层抽象实现灵活的通信方式。整体分为三层：

### Host（宿主应用）

Host 是用户直接交互的 AI 应用程序，比如 Claude Desktop、VS Code、ChatGPT 等。Host 内部集成了 MCP Client，负责管理与一个或多个 MCP Server 的连接。

### Client（客户端）

MCP Client 嵌入在 Host 应用中，负责：

- 与 MCP Server 建立连接
- 发送请求（调用工具、获取资源等）
- 接收 Server 的响应和通知
- 在 Host 应用的需求和 MCP 协议之间进行翻译

一个 Host 可以同时维护多个 Client 实例，每个 Client 连接一个 Server。比如在 [Claude Code](/posts/ai/2026-02-19-claude-code-vs-codex/) 中，你可以同时配置 GitHub Server、Playwright Server、文件系统 Server 等。

### Server（服务端）

MCP Server 是能力的实际提供者。每个 Server 通常聚焦于一个特定的集成点，暴露相应的工具、资源和提示词模板。例如：

- GitHub Server：提供仓库管理、Issue 操作、PR 审查等能力
- PostgreSQL Server：提供数据库查询和管理能力
- Playwright Server：提供[浏览器自动化](/posts/ai/2026-01-28-claude-code-browser-automation/)能力
- Figma Server：提供[设计稿读取和操作](/posts/ai/2026-02-19-figma-code-to-canvas/)能力

### Transport（传输层）

MCP 支持多种传输方式，在不同版本中有所演进：

**STDIO（标准输入输出）**

适用于本地场景，Server 与 Client 运行在同一台机器上。通过进程的标准输入输出流进行通信，简单直接，是本地开发最常用的方式。

**Streamable HTTP**

这是 2025 年 3 月规范更新中引入的新传输方式，取代了之前的 HTTP+SSE 方案。Server 提供一个统一的 HTTP 端点，同时支持 POST 和 GET 方法，并可选择性地使用 Server-Sent Events（SSE）进行流式传输。相比之前的方案，Streamable HTTP 只需要单一端点就能实现双向通信，大大简化了部署和使用。

## MCP 的核心能力

MCP 规范定义了六大核心特性，分为服务端原语和客户端能力两类。

### 服务端原语

**Tools（工具）**

Tools 是 MCP 最核心也是最常用的能力。它允许 Server 暴露可执行的函数，由 AI 模型决定何时调用。例如：

- 发送一封邮件
- 查询数据库
- 创建一个 GitHub Issue
- 执行一段代码

工具调用遵循"模型发起、用户确认、Server 执行"的流程，确保人始终在环路中。

**Resources（资源）**

Resources 允许 Server 向 Client 暴露只读数据，作为 LLM 交互的上下文信息。资源可以是静态的（如配置文件、文档模板），也可以是动态的（如数据库记录、实时数据）。

与 Tools 不同，Resources 由应用程序或用户主动选择使用，而非由模型自动调用。这种设计让上下文的注入更加可控。

**Prompts（提示词模板）**

Prompts 允许 Server 暴露结构化的消息模板，引导 AI 模型按照特定的方式进行交互。这对于复杂工作流特别有用——Server 可以预定义一组最佳实践的提示词，确保模型在执行特定任务时获得最优的指令格式。

### 客户端与高级能力

**Sampling（采样）**

Sampling 允许 Server 通过 Client 请求 LLM 的补全能力。这意味着 Server 可以利用模型的推理能力来辅助自身的决策过程，实现更复杂的 agentic 行为，同时保持安全性和隐私控制——因为请求始终通过 Client 中转。

**Roots（根目录）**

Roots 是 Client 告诉 Server 可以访问哪些文件系统路径的机制。通过定义安全的、特定的目录作为"根"，避免 Server 获得无限制的文件访问权限。

**Elicitation（信息获取）**

Elicitation 允许 Server 在工具执行过程中暂停，通过 Client 向用户请求额外的输入信息。Server 可以发送结构化的请求，说明需要什么信息，由 Client 向用户展示并获取同意。

## MCP Apps：从工具调用到交互式 UI

2026 年 1 月，MCP 生态迎来了一次重大进化——MCP Apps 正式发布。这一扩展让 MCP 从纯粹的"工具调用-文本返回"模式，跨入了可交互的 UI 时代。

### 什么是 MCP Apps

传统的 MCP 工具调用，Server 返回的是文本或结构化数据，由 Client 负责渲染展示。MCP Apps 打破了这个限制——工具调用现在可以返回交互式 UI 组件，直接在对话界面中渲染。

这意味着，一次工具调用可以返回：

- 可视化仪表盘
- 交互式表单
- 数据图表
- 多步骤工作流界面
- 实时预览组件

### 技术实现

MCP Apps 基于 HTML 内容渲染，所有 UI 运行在沙箱化的 iframe 中。核心安全保障包括：

- iframe 无法访问父窗口
- 不能发起任意网络请求
- 权限严格受限

这一设计在提供丰富交互能力的同时，确保了安全隔离。

### 客户端支持

目前已支持 MCP Apps 的客户端包括 ChatGPT、Claude、Goose 和 Visual Studio Code，其中 VS Code 是首个提供完整 MCP Apps 支持的 AI 代码编辑器。更多客户端正在接入中。

MCP Apps 的诞生，融合了 MCP-UI 和 OpenAI Apps SDK 的成果，是 OpenAI 与 MCP-UI 团队合作制定的共享开放标准，这本身就体现了 MCP 生态的开放协作精神。

## MCP 捐赠 Linux Foundation 的意义

2025 年底，Anthropic 宣布将 MCP 捐赠给 Linux Foundation 新成立的 Agentic AI Foundation（AAIF）。这个基金会由 Anthropic、Block 和 OpenAI 共同发起，得到了 Google、Microsoft、Amazon Web Services、Cloudflare 和 Bloomberg 的支持。

与 MCP 一同成为 AAIF 创始项目的还有 Block 的 Goose（一个开源 AI 代理框架）和 OpenAI 的 AGENTS.md（Agent 行为规范标准）。

### 为什么这件事如此重要

**中立治理**

由单一公司主导的协议，其他公司总会有所顾虑。Linux Foundation 提供了一个中立的基础设施，让维护者可以独立运作，不受任何单一公司的技术方向主导。这极大地降低了其他企业采纳 MCP 的心理门槛。

**行业共识**

当 OpenAI、Google、Microsoft 这些曾经各自为政的巨头，都愿意坐到同一张桌子前支持同一个协议时，这传递了一个明确信号：MCP 不是 Anthropic 的协议，而是整个行业的协议。

**长期可持续**

开源协议的生命力取决于社区和治理结构。Linux Foundation 有着丰富的开源项目治理经验（Linux、Kubernetes、Node.js 等），能够确保 MCP 的长期健康发展。

## 与 Function Calling 的对比

很多开发者的第一个问题是：已经有了 Function Calling / Tool Use，为什么还需要 MCP？这是一个好问题，两者确实解决相关但不同的问题。

| 对比维度 | Function Calling | MCP |
|---------|-----------------|-----|
| **协议标准** | 各厂商私有格式（OpenAI、Anthropic 各有一套） | 开放标准，跨厂商通用 |
| **架构模式** | 工具定义嵌入 LLM 请求中 | 独立的 Client-Server 架构 |
| **可移植性** | 切换模型提供商需重写集成代码 | 一次开发，所有兼容客户端可用 |
| **工具发现** | 每次请求手动传入工具列表 | Server 动态注册，Client 自动发现 |
| **复用性** | 工具定义散落在各项目中 | Server 独立部署、版本控制、跨项目共享 |
| **双向通信** | 单向（Client 到 Server） | 双向（Server 可回调 Client） |
| **适用场景** | 简单原型、少量工具 | 生产环境、多工具组合、企业级应用 |
| **维护成本** | 工具少时简单，规模化后难以维护 | 初始投入稍高，长期维护成本低 |

**关键结论**：Function Calling 和 MCP 不是互斥的，而是互补的。Function Calling 是模型层面的能力（模型理解何时需要调用工具），MCP 是基础设施层面的协议（标准化工具的发现、调用和交互方式）。在实际的 MCP 实现中，模型仍然通过类似 Function Calling 的机制来决定调用哪个工具。

简单项目、快速原型选 Function Calling 直接高效；生产环境、多模型支持、工具需要跨项目共享时，MCP 是更好的选择。

## 如何开发 MCP Server

开发一个 MCP Server 比想象中简单。以 Python 为例，使用官方推荐的 FastMCP 框架，几十行代码就能创建一个功能完整的 Server。

### 基本示例

以下是一个简单的天气查询 MCP Server 示例：

```python
from mcp.server.fastmcp import FastMCP

# 创建 Server 实例
mcp = FastMCP("weather-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 实际项目中这里会调用天气 API
    return f"{city} 当前天气：晴，温度 22°C"

@mcp.resource("config://settings")
async def get_settings() -> str:
    """暴露 Server 配置信息"""
    return "默认温度单位: 摄氏度"

@mcp.prompt("weather-report")
async def weather_prompt(city: str) -> str:
    """天气报告的提示词模板"""
    return f"请为 {city} 生成一份详细的天气报告，包括温度、湿度、风力和未来三天预报。"

if __name__ == "__main__":
    mcp.run()
```

### 开发要点

**工具设计原则**

- 每个工具聚焦单一功能，保持原子性
- 提供清晰的描述和参数说明（AI 模型依赖这些信息决定何时调用）
- 做好错误处理，返回有意义的错误信息

**安全考虑**

OWASP 在 2026 年 2 月发布了《MCP Server 安全开发实践指南》，核心建议包括：

- 对所有输入进行验证和清理
- 实施最小权限原则
- 避免暴露敏感信息
- 做好速率限制和日志记录

**多语言支持**

MCP SDK 提供了多种语言的官方支持：

- **Python**：FastMCP 框架，最为成熟
- **TypeScript/JavaScript**：适合 Web 开发者
- **.NET**：Microsoft 提供了官方模板和 NuGet 包
- **Go / Java**：社区维护的 SDK

### 部署方式

本地 Server 使用 STDIO 传输即可，配置简单。远程部署推荐使用 Streamable HTTP 传输，可通过 Docker 容器化部署。值得注意的是，自 2025 年 5 月以来，远程 MCP Server 的数量增长了近 4 倍，80% 的热门 MCP Server 都提供了远程部署支持。

## MCP 生态现状与展望

### 当前生态

MCP 的生态增长速度令人瞩目：

- **Server 数量**：公开注册的 MCP Server 超过万个，涵盖数据库、版本控制、通信工具、云服务等各个领域
- **SDK 下载量**：月下载量突破 9700 万次
- **客户端支持**：Claude Desktop、ChatGPT、VS Code、Cursor、Windsurf、[Claude Code](/posts/ai/2026-01-13-claude-cowork/) 等主流 AI 应用均已支持
- **企业采纳**：Gartner 预测到 2026 年底，40% 的企业应用将包含特定任务的 AI Agent，较 2025 年的不到 5% 大幅增长
- **市场规模**：全球 MCP Server 市场预计从 2025 年的 27 亿美元增长到 2034 年的 55 亿美元

### 2026 年趋势

**企业级成熟**

2026 年是 MCP 从实验走向企业大规模采用的关键一年。预计到年底，75% 的 API 网关厂商和 50% 的 iPaaS 厂商将集成 MCP 功能。

**规范标准化**

MCP 预计在 2026 年实现完全标准化，包括稳定的规范版本和全面的合规框架，为更广泛的企业采纳提供基础。

**交互能力进化**

MCP Apps 的发布只是开始。未来我们将看到更丰富的 UI 组件、更强的跨 Server 协作能力，以及与 A2A（Agent-to-Agent）协议的深度整合。

## 常见问题

**MCP 只能用于 Anthropic 的产品吗？**

不是。MCP 是一个完全开放的协议，已捐赠给 Linux Foundation。OpenAI、Google、Microsoft 等公司都是 Agentic AI Foundation 的支持者。任何 AI 应用和模型都可以实现 MCP 支持。

**MCP Server 开发门槛高吗？**

不高。使用 Python 的 FastMCP 框架或 TypeScript SDK，一个基本的 MCP Server 可以在几十行代码内完成。官方文档和社区教程都非常丰富。

**MCP 会取代 Function Calling 吗？**

不会取代，而是互补。Function Calling 是模型理解工具调用意图的机制，MCP 是标准化工具暴露和调用的协议。在 MCP 的实现中，底层仍然依赖模型的 Function Calling 能力。

**MCP 的安全性如何保障？**

MCP 在协议层面内置了多重安全机制：工具调用需要用户确认、Roots 限制文件系统访问范围、MCP Apps 运行在沙箱 iframe 中。此外，OWASP 也已发布专门的 MCP 安全开发指南。

**已有的 REST API 和 MCP Server 如何选择？**

如果你的工具只需要被特定应用调用，REST API 已经够用。但如果你希望工具能被任何 AI 应用发现和使用，MCP Server 是更好的选择。许多 MCP Server 本身就是对现有 REST API 的封装。

## 总结

MCP 的出现，解决了 AI 应用生态中一个长期存在的痛点：缺乏统一的工具集成标准。从 Anthropic 的内部实验，到捐赠给 Linux Foundation 成为行业共治的开放标准，MCP 走出了一条教科书式的开源协议发展路径。

协议本身的设计足够优雅——Client-Server 架构保证了灵活性，JSON-RPC 基础保证了通用性，Resources / Tools / Prompts 三大原语覆盖了绝大多数集成场景。而 MCP Apps 的推出更是将协议的能力边界从数据交换扩展到了交互式 UI，打开了全新的想象空间。

对于开发者而言，现在正是学习和投入 MCP 生态的最佳时机。无论是开发自己的 MCP Server 来暴露现有服务的能力，还是在 AI 应用中集成 MCP Client 来获得丰富的工具生态，MCP 都提供了成熟的 SDK 和完善的文档支持。

AI 连接万物的时代，需要一个通用的"接口标准"。MCP，正是这个标准。

## 相关阅读

- [MCP 协议详解：AI 工具的通用连接标准](/zh/posts/ai/2026-02-28-mcp-protocol-explained/) — MCP 协议的另一视角深度解读
- [MCP 安全实战指南：AI Agent 时代的攻防博弈与防护策略](/zh/posts/ai/2026-02-23-mcp-security-guide/) — 协议之上的安全防护
- [用 TypeScript 构建 MCP Server：从零到发布完整教程](/zh/posts/ai/2026-03-02-building-mcp-servers-typescript/) — 动手写一个 MCP Server
- [用 Python 构建 MCP 服务器：完整分步教程](/zh/posts/ai/2026-03-05-build-mcp-server-python/) — Python 版 MCP Server 教程
- [2026 年最值得装的 18 个 MCP 服务器：Claude Code 实测精选](/zh/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — MCP 生态当前最值得装的服务器
- [MCP、Skills、Hooks 到底有什么区别？](/zh/posts/ai/2026-04-02-mcp-vs-skills-claude-code/) — 把 MCP 放回 Claude Code 扩展机制中对比
