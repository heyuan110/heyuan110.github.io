+++
date = '2026-01-28T23:30:00+08:00'
draft = false
title = 'Moltbot Wizard 完全指南：打造你的私人 AI 助手'
description = 'Moltbot 是一款开源的个人 AI 助手，通过 Wizard 向导可以快速配置 Gateway、消息渠道和 Skills。本文手把手教你从零开始搭建属于自己的 AI 管家。'
toc = true
tags = ['Moltbot', 'AI 助手', 'Clawdbot', '个人AI', '开源']
categories = ['AI实战']
keywords = ['Moltbot', 'Clawdbot', 'AI助手', 'Wizard配置', '个人AI助手搭建']
+++

想象一下这个场景：你在微信群里@一下 AI，它就能帮你订机票、查天气、写代码、管理日程，甚至能记住你上周聊过的所有内容。这不是科幻电影，这就是 **Moltbot**——一个你可以完全掌控的私人 AI 助手。

本文将带你深入了解 Moltbot 的 Wizard（配置向导），从"这是啥"到"我会用"，一篇搞定。

## 一、背景：为什么需要 Moltbot？

### 现有 AI 助手的痛点

我们每天都在用各种 AI 助手——ChatGPT、Claude、文心一言。但它们都有一个共同的问题：**你不是主人，只是租客**。

- **数据不在你手里**：聊天记录、个人偏好全存在别人服务器上
- **功能受限**：想让 AI 帮你发微信？抱歉，做不到
- **平台分散**：工作用 Slack，生活用微信，每个平台都要单独配置
- **无法定制**：AI 的"性格"和能力完全由平台决定

### Moltbot 的解决方案

Moltbot（前身叫 Clawdbot，因商标问题改名）是由 PSPDFKit 创始人 Peter Steinberger 创建的开源项目，在 GitHub 上已获得超过 68,000 星。

它的核心理念是：**把 AI 助手的控制权交还给你**。

```
┌─────────────────────────────────────────────────────────────┐
│                        你的设备                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Moltbot Gateway                    │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │ Claude  │  │ GPT-5   │  │ Gemini  │  ...更多    │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘            │   │
│  │       └────────────┼────────────┘                  │   │
│  │                    ▼                                │   │
│  │            ┌──────────────┐                        │   │
│  │            │   AI Agent   │ ← 你定制的"AI性格"      │   │
│  │            └──────┬───────┘                        │   │
│  └───────────────────┼─────────────────────────────────┘   │
│                      ▼                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ WhatsApp│  │Telegram │  │ Discord │  │ iMessage│ ...   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
└─────────────────────────────────────────────────────────────┘
```

简单来说，Moltbot 就像一个"AI 中转站"：
- **上游**连接各种 AI 模型（Claude、GPT、Gemini 等）
- **下游**连接你常用的聊天软件（微信、Telegram、Discord 等）
- **中间**是你自己定制的 AI Agent，有独立的记忆、技能和个性

## 二、Wizard 是什么？

### 一键配置的魔法

如果让你手动配置 Moltbot，你需要：
1. 写 JSON 配置文件
2. 配置各平台的 API Token
3. 设置守护进程
4. 调试网络连接
5. 安装各种依赖

这对非技术用户来说简直是噩梦。

**Wizard（配置向导）** 就是为了解决这个问题而生的。它是一个交互式命令行工具，会一步步问你问题，然后自动完成所有配置。就像装机时的"下一步、下一步、完成"一样简单。

```bash
moltbot onboard
```

一条命令，启动魔法。

### Wizard 会做什么？

| 配置项 | 说明 | 为什么重要 |
|--------|------|-----------|
| **模型认证** | 配置 Claude、GPT 等 AI 的 API Key | 让 AI 有"大脑" |
| **工作空间** | 设置 Agent 的工作目录和启动文件 | Agent 的"家" |
| **Gateway** | 配置网关端口、认证方式 | 消息中转的"枢纽" |
| **渠道** | 连接 WhatsApp、Telegram 等 | 对话的"入口" |
| **守护进程** | 让 Moltbot 后台常驻运行 | 7×24 小时在线 |
| **Skills** | 安装各种能力插件 | 让 AI 会更多"技能" |

## 三、准备工作

### 系统要求

- **操作系统**：macOS、Linux 或 Windows（需要 WSL2）
- **Node.js**：22 或更高版本
- **网络**：需要能访问 AI 服务商的 API

### 获取 API Key

在开始之前，你需要至少准备一个 AI 模型的 API Key。推荐使用 **Anthropic**（Claude）：

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册账号并获取 API Key
3. 记下这个 Key，待会要用

> **小贴士**：如果你已经在用 Claude Code CLI，Wizard 可以自动复用它的认证信息。

### 安装 Moltbot

**Linux/macOS**：
```bash
curl -fsSL https://molt.bot/install.sh | bash
```

**Windows（PowerShell）**：
```powershell
iwr -useb https://molt.bot/install.ps1 | iex
```

安装完成后，验证一下：
```bash
moltbot --version
```

## 四、启动 Wizard：分步详解

### 启动向导

```bash
moltbot onboard
```

运行后，你会看到一个选择界面：

```
? How would you like to proceed?
> QuickStart (recommended defaults)
  Advanced (full control)
```

### QuickStart vs Advanced

| 模式 | 适合谁 | 特点 |
|------|--------|------|
| **QuickStart** | 新手、想快速体验 | 使用推荐默认值，最少的问题 |
| **Advanced** | 进阶用户、有特殊需求 | 完全控制每一个配置项 |

新手建议选 **QuickStart**，这样 Wizard 会自动设置：
- 本地 Gateway（端口 18789）
- Token 认证（自动生成）
- Telegram/WhatsApp 使用白名单模式

### 步骤 1：选择 AI 模型

```
? Which model provider would you like to use?
> Anthropic API key (recommended)
  Anthropic OAuth (Claude Code CLI)
  OpenAI API key
  OpenAI Code (Codex) subscription
  Vercel AI Gateway (multi-model proxy)
  MiniMax M2.1
  Moonshot (Kimi K2)
  Skip
```

**各选项解释**：

| 选项 | 说明 | 建议 |
|------|------|------|
| **Anthropic API key** | 直接使用 Claude API | ✅ 推荐新手使用 |
| **Anthropic OAuth** | 复用 Claude Code CLI 认证 | 如果你已安装 Claude Code |
| **OpenAI API key** | 使用 GPT 系列模型 | GPT 用户首选 |
| **Vercel AI Gateway** | 支持多模型切换的代理 | 想用多种模型时选择 |
| **Moonshot** | 国产 Kimi 模型 | 国内用户友好 |

选择 "Anthropic API key" 后，粘贴你的 API Key：

```
? Enter your Anthropic API key: sk-ant-api03-xxxxx
```

Wizard 会自动验证 Key 是否有效。

### 步骤 2：设置工作空间

```
? Where should the agent workspace be?
> ~/clawd (default)
  Custom location
```

工作空间是 Agent 存放配置、记忆、会话的地方。默认的 `~/clawd` 就很好，除非你有特殊需求。

工作空间结构：
```
~/clawd/
├── IDENTITY.md      # Agent 的"人设"
├── BOOT.md          # 启动指令
├── TOOLS.md         # 可用工具说明
├── SOUL.md          # 核心行为准则
└── sessions/        # 会话记录
```

### 步骤 3：配置 Gateway

Gateway 是 Moltbot 的核心，所有消息都要经过它。

```
? Gateway port: 18789
? Gateway bind address:
> loopback (127.0.0.1, recommended for single user)
  all interfaces (0.0.0.0, for remote access)
? Enable authentication?
> Yes (recommended)
  No
```

**关键概念解释**：

**Gateway（网关）** 就像家里的路由器——所有设备上网都要经过它，所有消息流转也都要经过 Gateway。

**loopback vs all interfaces**：
- `loopback`：只有本机能访问，最安全
- `all interfaces`：允许其他设备访问，需要配合认证使用

**为什么要开启认证？**

即使是本机运行，也建议开启 Token 认证。因为你的电脑上可能有其他程序在运行，认证可以防止恶意程序冒充你与 AI 对话。

### 步骤 4：连接消息渠道

这是最激动人心的部分——让 AI 进入你的聊天软件！

```
? Which channels would you like to set up?
  ◉ WhatsApp
  ◉ Telegram
  ◯ Discord
  ◯ Google Chat
  ◯ Signal
  ◯ iMessage
```

#### 配置 Telegram

如果选择了 Telegram，Wizard 会问你：

```
? Enter your Telegram bot token:
```

获取 Bot Token 的步骤：
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot`
3. 按提示设置机器人名称
4. BotFather 会返回一个 Token，格式如 `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. 把这个 Token 粘贴到 Wizard

#### 配置 WhatsApp

WhatsApp 稍微特殊，需要扫码登录：

```
? Set up WhatsApp now?
> Yes
  Skip for now
```

选择 Yes 后，终端会显示一个二维码。用 WhatsApp 扫描（设置 → 关联设备）即可。

> **注意**：WhatsApp 的配对信息存储在 `~/.clawdbot/credentials/whatsapp/` 目录下。

### 步骤 5：安装守护进程

```
? Install as background service?
> Yes (recommended)
  No
? Runtime:
> Node (recommended)
  Bun
```

守护进程让 Moltbot 开机自启、后台运行。

- **macOS**：创建 LaunchAgent
- **Linux**：创建 systemd 用户服务

选择 Node 运行时（Bun 还不够稳定）。

### 步骤 6：安装 Skills

Skills 是 Moltbot 的"技能包"，让 AI 能做更多事。

```
? Install recommended skills?
> Yes
  No
? Node package manager:
> npm
  pnpm
```

推荐安装的 Skills 包括：
- **web_search**：网页搜索
- **web_fetch**：抓取网页内容
- **exec**：执行系统命令
- **browser**：浏览器自动化

### 完成！

配置完成后，Wizard 会显示摘要：

```
✅ Configuration complete!

Gateway:     ws://127.0.0.1:18789
Workspace:   ~/clawd
Channels:    Telegram, WhatsApp
Model:       claude-sonnet-4-20250514

Next steps:
1. Run 'moltbot dashboard' to open the web UI
2. Send a message to your bot on Telegram or WhatsApp
3. Run 'moltbot status' to check system health
```

## 五、验证安装

### 检查状态

```bash
moltbot status
```

输出示例：
```
Gateway:     ✅ Running (ws://127.0.0.1:18789)
Agent:       ✅ Ready
Channels:
  Telegram:  ✅ Connected (@your_bot)
  WhatsApp:  ✅ Connected (+86 138xxxx)
Model:       claude-sonnet-4-20250514
```

### 打开控制面板

```bash
moltbot dashboard
```

浏览器会自动打开 `http://127.0.0.1:18789/`，这是 Moltbot 的 Web 控制台，你可以在这里：
- 实时查看对话
- 管理 Sessions
- 配置 Agent 设置

### 发送第一条消息

打开 Telegram，找到你创建的 Bot，发送：

```
你好！介绍一下你自己
```

如果一切正常，你会收到 AI 的回复。恭喜，你的私人 AI 助手上线了！

## 六、进阶配置

### 非交互式安装（适合自动化）

如果你需要在服务器上自动部署，可以用 `--non-interactive` 模式：

```bash
moltbot onboard --non-interactive \
  --mode local \
  --auth-choice anthropic-api-key \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node
```

### 添加多个 Agent

一个 Moltbot 可以运行多个 Agent，各自有独立的工作空间和会话。比如你可以创建一个"工作 Agent"和一个"生活 Agent"：

```bash
# 添加工作 Agent
moltbot agents add work --workspace ~/clawd-work

# 添加生活 Agent
moltbot agents add life --workspace ~/clawd-life
```

然后通过绑定规则，把不同的消息渠道路由到不同的 Agent。

### 远程模式

如果你想在 VPS 上运行 Gateway，在本地连接，可以使用远程模式：

```bash
# 在本地运行
moltbot onboard --mode remote
```

然后输入远程 Gateway 的 WebSocket 地址：
```
? Remote Gateway URL: ws://your-vps-ip:18789
? Authentication token: your-token
```

### 修改配置

已经完成初始配置后，想修改某些设置？用 `configure` 命令：

```bash
# 重新配置所有
moltbot configure

# 只配置特定部分
moltbot configure --section gateway
moltbot configure --section channels
moltbot configure --section skills
```

## 七、常见问题

### Q1：Gateway 启动失败，提示端口被占用？

```bash
# 检查谁占用了端口
lsof -i :18789

# 换个端口
moltbot configure --section gateway
```

### Q2：WhatsApp 扫码后一直连不上？

1. 确保手机和电脑在同一网络
2. 检查防火墙设置
3. 尝试重新配对：
   ```bash
   moltbot channels login whatsapp
   ```

### Q3：AI 响应很慢怎么办？

1. 检查网络到 AI 服务商的延迟
2. 考虑使用国内模型（如 Moonshot）
3. 或者使用代理：
   ```bash
   export HTTPS_PROXY=http://your-proxy:port
   moltbot gateway
   ```

### Q4：怎么给 AI 设置"人设"？

编辑工作空间里的 `IDENTITY.md`：

```bash
# 打开工作空间
cd ~/clawd

# 编辑人设文件
nano IDENTITY.md
```

示例人设：
```markdown
你是小明的私人助理，名叫"小智"。

性格特点：
- 说话简洁有条理
- 适度使用 emoji
- 记住用户的偏好

工作职责：
- 管理日程
- 回答技术问题
- 帮助写作和翻译
```

### Q5：配置文件在哪？

| 文件 | 位置 | 说明 |
|------|------|------|
| 主配置 | `~/.clawdbot/moltbot.json` | 所有配置项 |
| OAuth 凭证 | `~/.clawdbot/credentials/oauth.json` | OAuth 认证信息 |
| WhatsApp 数据 | `~/.clawdbot/credentials/whatsapp/` | WhatsApp 会话 |
| Agent 会话 | `~/.clawdbot/agents/<id>/sessions/` | 对话历史 |

## 八、安全建议

Moltbot 运行在你的设备上，有很高的权限。以下是一些安全最佳实践：

1. **始终开启 Gateway 认证**，即使是 loopback 模式
2. **不要在公网暴露 Gateway**，除非你知道自己在做什么
3. **定期更新** Moltbot 到最新版本
4. **谨慎授予 exec 权限**，这允许 AI 执行系统命令
5. **审查 Skills** 的来源，只安装可信的插件

对于群聊场景，建议开启沙盒模式：

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```

这会把非主会话的 Agent 隔离在 Docker 容器中运行。

## 总结

Moltbot Wizard 把复杂的配置过程简化成了"回答几个问题"。通过本文，你应该已经：

- ✅ 理解了 Moltbot 的架构和价值
- ✅ 完成了 Wizard 的全流程配置
- ✅ 成功连接了消息渠道
- ✅ 学会了进阶配置和故障排查

现在，你拥有了一个真正属于自己的 AI 助手。它了解你、记住你、并且只为你服务。

### 相关阅读

- [Clawdbot（Moltbot）：打造你的私人 AI 助手](/zh/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/)
- [Claude Code 完全指南](/zh/posts/ai/2026-01-14-claude-code-guide/)

---

**参考资料**：
- [Moltbot 官方文档](https://docs.molt.bot/)
- [Moltbot Wizard 配置页面](https://docs.molt.bot/start/wizard)
- [Moltbot GitHub 仓库](https://github.com/moltbot/moltbot)
- [TechCrunch: Everything you need to know about Moltbot](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/)
