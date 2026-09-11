+++
date = '2026-01-13T08:00:00+08:00'
title = 'Vercel 发布 Agent Browser：专为 AI 代理打造的浏览器自动化工具'
description = 'Vercel 开源了 Agent Browser，一个专为 AI 代理设计的浏览器自动化 CLI 工具，采用 Rust + Node.js 架构，支持快照驱动的交互模式'
toc = true
tags = ['AI', 'Vercel', 'Browser Automation', 'Agent', 'CLI']
categories = ['AI工具']
keywords = ['Vercel Agent Browser', 'AI 浏览器自动化', '无头浏览器 CLI', 'Playwright 替代方案', 'AI Agent 浏览器工具']
+++
![Agent Browser](cover.webp)

Vercel 近期开源了一款名为 **Agent Browser** 的命令行工具，这是一个专为 AI 代理设计的浏览器自动化解决方案。它结合了 Rust 的高性能与 Node.js 的灵活性，为 AI 工作流提供了可靠的浏览器交互能力。

## 一、什么是 Agent Browser？

Agent Browser 是一个无头浏览器自动化 CLI 工具，主要面向 AI 代理场景。与传统的浏览器自动化工具不同，它采用了**快照驱动**的交互模式，特别适合 AI 代理的工作方式。

核心理念：让 AI 代理能够像人一样"看到"网页，并与之交互。

## 二、核心特性

### 1. 高性能架构

Agent Browser 采用**客户端-守护进程架构**：

- **Rust CLI**：原生编译，启动快、资源占用低
- **Node.js 守护进程**：管理 Playwright 浏览器实例
- **持久化连接**：支持快速重复操作

### 2. AI 优化的快照模式

这是 Agent Browser 最大的亮点。传统自动化工具需要复杂的选择器来定位元素，而 Agent Browser 使用**访问性树快照**：

```bash
# 获取页面快照，返回带引用的交互元素
agent-browser snapshot -i --json
```

快照返回的每个元素都带有唯一引用（如 `@e1`、`@e2`），AI 代理可以直接使用这些引用进行交互，无需编写复杂的 CSS/XPath 选择器。

### 3. 完整的浏览器控制能力

**导航操作**：
- 打开 URL、前进、后退、刷新
- 多标签页管理

**交互操作**：
- 点击、填表、输入、悬停
- 复选框、下拉菜单选择
- 文件上传、滚动

**信息获取**：
- 文本提取、属性获取
- 截图、PDF 生成
- 网络请求监控

**高级功能**：
- JavaScript 执行
- 网络拦截和请求模拟
- Cookie、存储管理
- 多会话隔离

## 三、安装与使用

### 1. 安装

```bash
# 通过 npm 安装
npm install -g agent-browser

# 下载 Chromium
agent-browser install
```

### 2. 典型工作流

Agent Browser 的推荐使用方式是**快照-交互-验证**循环：

```bash
# 1. 打开目标页面
agent-browser open https://example.com

# 2. 获取页面快照（仅交互元素）
agent-browser snapshot -i --json

# 3. 使用元素引用进行交互
agent-browser click @e5
agent-browser fill @e3 "Hello World"

# 4. 重新快照验证结果
agent-browser snapshot -i --json
```

### 3. 高级用法示例

**登录并保存会话状态**：

```bash
# 登录网站
agent-browser open https://example.com/login
agent-browser fill @username "user@example.com"
agent-browser fill @password "password"
agent-browser click @submit

# 保存认证状态供后续使用
agent-browser save-auth ./auth-state.json
```

**并行多会话**：

```bash
# 创建隔离的浏览器会话
agent-browser open https://site1.com --session session1
agent-browser open https://site2.com --session session2
```

## 四、技术架构

```
┌─────────────────┐     ┌──────────────────────┐
│   Rust CLI      │────▶│   Node.js Daemon     │
│   (原生性能)    │     │   (Playwright)       │
└─────────────────┘     └──────────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │    Chromium      │
                        │    浏览器实例    │
                        └──────────────────┘
```

这种架构的优势：
- **启动速度快**：Rust CLI 毫秒级启动
- **资源高效**：守护进程复用浏览器实例
- **跨平台**：支持 Windows、macOS、Linux

## 五、与 Claude Code 集成

Agent Browser 还提供了专门的 **Claude Code Skill**，可以无缝集成到 AI 编程助手中。安装后，Claude Code 可以直接调用浏览器自动化能力，实现：

- 自动化 Web 测试
- 表单填充
- 截图和数据抓取
- 网页内容分析

### 1. 安装 Skill 到本地

**第一步**：创建 skill 目录

```bash
mkdir -p ~/.claude/skills/agent-browser
```

**第二步**：下载官方 SKILL.md

```bash
curl -o ~/.claude/skills/agent-browser/SKILL.md \
  https://raw.githubusercontent.com/vercel-labs/agent-browser/main/skills/agent-browser/SKILL.md
```

或者手动创建 `~/.claude/skills/agent-browser/SKILL.md`，内容如下：

```markdown
---
name: agent-browser
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction.
---

# Browser Automation with agent-browser

## Quick start

agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser

## Core workflow

1. Navigate: agent-browser open <url>
2. Snapshot: agent-browser snapshot -i (returns elements with refs like @e1, @e2)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes
```

**第三步**：重启 Claude Code

安装完成后，重启 Claude Code 即可使用。在对话中输入 `/agent-browser` 即可调用该 skill。

### 2. Skill 常用命令速查

| 命令 | 说明 |
|------|------|
| `agent-browser open <url>` | 打开网页 |
| `agent-browser snapshot -i` | 获取交互元素快照 |
| `agent-browser click @e1` | 点击元素 |
| `agent-browser fill @e2 "text"` | 填充输入框 |
| `agent-browser screenshot` | 截图 |
| `agent-browser wait @e1` | 等待元素出现 |
| `agent-browser close` | 关闭浏览器 |

### 3. 实战示例：自动登录

```bash
# 打开登录页
agent-browser open https://example.com/login

# 获取页面元素
agent-browser snapshot -i
# 输出: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

# 填写表单并提交
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3

# 等待跳转完成
agent-browser wait --load networkidle

# 保存登录状态供后续使用
agent-browser state save auth.json
```

## 六、适用场景

- **AI 代理开发**：构建能够浏览网页的 AI 助手
- **自动化测试**：Web 应用的 E2E 测试
- **数据抓取**：结构化网页数据提取
- **RPA 流程**：自动化重复性网页操作

## 七、总结

Agent Browser 填补了 AI 代理领域浏览器自动化工具的空白。它的快照驱动模式非常契合 AI 的工作方式——获取当前状态，做出决策，执行操作。

如果你正在开发需要网页交互能力的 AI 代理，Agent Browser 绝对值得一试。

**项目地址**：[https://github.com/vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)

**开源协议**：Apache 2.0

## 相关阅读

- [Claude Code 浏览器自动化怎么选？5 套方案实测对比（2026）](/zh/posts/ai/2026-01-28-claude-code-browser-automation/) — 浏览器自动化方案横评
- [Playwright CLI + Skill 三段式：把 AI 浏览器自动化做到 0 Token](/zh/posts/ai/2026-04-18-playwright-cli-skill-zero-token-automation/) — 低 Token 浏览器自动化的工程技巧
- [Chrome DevTools MCP 完整配置指南](/zh/posts/ai/2026-03-17-chrome-devtools-mcp-guide/) — 另一条让 AI 操作浏览器的路径
- [MCP 协议全面解析：AI 连接万物的通用标准](/zh/posts/ai/2026-02-20-mcp-protocol-guide/) — Agent Browser 背后的协议基础

## 系列文章导航

这是「AI Agent 浏览器自动化」系列的第 1 篇。这条线的演进：headless 驱动 → 接管真实浏览器 → 把 token 砍到底 → 共享你的登录态：

1. **本文**：Vercel Agent Browser — 为 Agent 而不是测试套件设计的 snapshot 式 CLI
2. [Claude Code 浏览器自动化：5 套方案实测对比](/zh/posts/ai/2026-01-28-claude-code-browser-automation/) — 这条线的地图：token 成本、速度、稳定性
3. [Chrome DevTools MCP 2026 配置教程](/zh/posts/ai/2026-03-17-chrome-devtools-mcp-guide/) — 接管真实浏览器，以及 9222 端口的坑
4. [Playwright CLI + Skill 三段式：0 Token 自动化](/zh/posts/ai/2026-04-18-playwright-cli-skill-zero-token-automation/) — 去掉 MCP token 税的三段式写法
5. [Claude Code 截图 MCP 配置](/zh/posts/ai/2026-07-21-claude-code-screenshot-mcp-frontend-debugging/) — 前端调试闭环，10,220 对 65 token
6. [ubrowser 实测](/zh/posts/ai/2026-07-27-ubrowser-review/) — 设计对了，仓库死了
7. ego lite 实测：把你登录好的浏览器交给 Claude Code（即将发布）— 用 Spaces 把登录态交给 Agent
