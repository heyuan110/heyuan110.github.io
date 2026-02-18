+++
date = '2026-02-18T10:00:00+08:00'
draft = false
title = 'MoltBot 是什么？一文读懂这个现象级 AI Agent 的前世今生'
description = 'MoltBot（现 OpenClaw）是 2026 年最火的开源个人 AI Agent，能通过 Telegram/WhatsApp 远程操控电脑执行真实任务。本文从零详解 MoltBot 原理、核心功能、三次改名历史、与其他 AI Agent 对比及快速上手教程。'
toc = true
tags = ['MoltBot', 'AI Agent', 'OpenClaw', 'Clawdbot', '个人AI助手']
categories = ['AI原理']
keywords = ['moltbot 是什么', 'moltbot ai agent', 'moltbot 改名', 'moltbot 原理', 'moltbot 介绍', 'moltbot 能做什么', 'openclaw', 'clawdbot']
+++

如果你最近在技术社区看到 "MoltBot" 这个词却一头雾水，这篇文章就是为你写的。

**一句话定义：MoltBot（现已改名 OpenClaw）是一个开源的个人 AI Agent，运行在你自己的电脑上，通过 Telegram、WhatsApp 等聊天工具接收指令，能真正替你操作电脑、执行任务。**

它不是又一个聊天机器人，而是一个能"动手干活"的 AI 助手。下面我们从零开始，彻底搞清楚 MoltBot 是什么、怎么工作、以及你该不该用它。

---

## 一、MoltBot 是什么

### 1.1 基本定义

MoltBot 是由奥地利开发者 **Peter Steinberger** 创建的开源个人 AI 助手项目。它的核心理念可以用一句话概括：

> **让 AI 从"只会说"变成"能动手"。**

传统的 AI 工具（ChatGPT、Claude 网页版等）只能给你文字建议。你问它"帮我订明天上午的机票"，它只能回复一段操作指引。而 MoltBot 不同——它能直接打开浏览器、登录你的账号、完成预订、把确认信息发回给你。

用更技术的语言说：MoltBot 是一个 **自主式 AI Agent（Autonomous AI Agent）**，具备以下核心特征：

- **本地运行**：部署在你自己的电脑或服务器上，数据不离开你的设备
- **消息驱动**：通过 Telegram、WhatsApp、Discord、iMessage 等聊天平台交互
- **自主执行**：能运行 Shell 命令、操作浏览器、读写文件、调用 API
- **持久记忆**：记住你的偏好、习惯和历史对话，越用越懂你
- **技能可扩展**：支持 5700+ 社区技能插件，能力无限延伸

### 1.2 MoltBot 能做什么

具体来说，MoltBot 可以帮你完成这些真实任务：

| 场景 | 具体操作 |
|------|---------|
| **邮件管理** | 自动分类邮件、撰写回复、转发重要邮件摘要给你 |
| **日程安排** | 读取日历、创建会议、发送会议邀请 |
| **信息检索** | 浏览网页、阅读 PDF、汇总研究报告 |
| **文件操作** | 整理文件夹、批量重命名、数据格式转换 |
| **代码辅助** | 执行脚本、部署项目、监控服务器状态 |
| **生活助手** | 比价购物、航班值机、追踪快递 |
| **定时任务** | 每天早上推送新闻摘要、定期备份数据 |
| **社交媒体** | 发布内容、监控提及、整理评论 |

一个被广泛引用的真实案例：有用户声称"躺在沙发上看 Netflix 的时候，通过 Telegram 让 MoltBot 重建了整个网站"。

### 1.3 它和 ChatGPT / Claude 有什么区别

这是很多人最困惑的问题。简单对比：

| 特性 | ChatGPT / Claude 网页版 | MoltBot |
|------|----------------------|---------|
| **运行位置** | 云端（OpenAI / Anthropic 服务器） | 你自己的电脑 |
| **交互方式** | 浏览器网页 | Telegram / WhatsApp 等 |
| **能力边界** | 只能生成文字 | 能操作电脑、执行任务 |
| **数据隐私** | 数据上传到云端 | 数据留在本地 |
| **持久记忆** | 有限（对话窗口级别） | 持久（跨天、跨周记忆） |
| **7x24 在线** | 需要你主动打开 | 后台持续运行 |
| **费用** | 订阅制（$20/月起） | 开源免费 + API 调用费 |

核心区别在于：**ChatGPT 是一个对话工具，MoltBot 是一个执行引擎。**

---

## 二、MoltBot 的核心功能

### 2.1 多平台消息接入

MoltBot 支持 12+ 聊天平台同时接入：

- Telegram（最常用，配置最简单）
- WhatsApp
- Discord
- iMessage（需要 macOS）
- Slack
- Signal
- Microsoft Teams
- Google Chat
- WebChat（内置网页界面）

你可以在任何一个平台向 MoltBot 发消息，它都能收到并执行。这意味着你不需要坐在电脑前，**随时随地都能指挥你的 AI 助手**。

### 2.2 浏览器自动化

MoltBot 通过 Chrome DevTools Protocol（CDP）控制浏览器，能完成几乎所有你在浏览器中手动操作的事情：

- 打开网页、填写表单、点击按钮
- 登录网站（使用你预存的凭证）
- 截图并发回给你
- 提取网页数据

### 2.3 持久化记忆系统

这是 MoltBot 最有价值的功能之一。它的记忆以 Markdown 文件形式存储在本地（`~/.clawdbot/` 目录下），包括：

- **对话历史**：记住你上周、上个月说过的话
- **用户偏好**：知道你喜欢什么风格的邮件回复、常用的工作流程
- **项目上下文**：了解你正在进行的项目的背景信息
- **学习成果**：从错误中学习，下次做得更好

与 ChatGPT 的短期记忆不同，MoltBot 的记忆是**跨会话、跨天数持久化的**。它不会因为你关闭聊天窗口就忘记一切。

想深入了解记忆系统的设计，可以参考 [OpenClaw 记忆系统策略解析](/posts/ai/2026-01-31-openclaw-memory-strategy/)。

### 2.4 技能系统（Skills）

MoltBot 的技能系统是它可扩展性的基础。截至 2026 年 2 月，**ClawHub 技能市场已有 5700+ 社区贡献的技能**，覆盖：

- 音乐控制（Spotify 集成）
- 笔记管理（Obsidian 集成）
- 邮件处理（Gmail 集成）
- 代码托管（GitHub 集成）
- 智能家居控制
- 金融交易与 DeFi 协议集成
- 预测市场接入

技能的本质是 **Markdown 文件 + 可执行脚本** 的组合。Markdown 文件用自然语言描述技能的用途和使用时机，可执行脚本（Python、Bash 等）实现具体功能。AI 根据 Markdown 描述判断何时调用哪个技能。

更值得关注的是，MoltBot 能**自己编写新技能来扩展自身能力**——这是真正的 Agent 自我进化。

### 2.5 定时任务与主动监控

通过 cron 集成和心跳机制，MoltBot 不需要你主动发指令，就能：

- 每天早上推送新闻摘要
- 监控服务器状态，异常时自动告警
- 追踪股票价格，到达阈值时通知你
- 定期备份指定文件夹
- 检查 API 健康状态

这让 MoltBot 从一个"被动应答者"变成了"主动执行者"。

### 2.6 语音交互

MoltBot 集成了 ElevenLabs 语音服务，支持：

- 语音唤醒（Voice Wake）
- 语音对话模式（Talk Mode）
- 在 macOS / iOS / Android 上实现 "always-on speech"

你可以像对 Siri 或 Alexa 说话一样，对 MoltBot 下达语音指令。

---

## 三、MoltBot 的工作原理

### 3.1 整体架构

MoltBot 的架构分为四层，每一层都有明确的职责：

```
+--------------------------------------------------+
|                  你的设备（本地）                    |
|                                                    |
|  +------------+    WebSocket     +--------------+  |
|  |  消息渠道   |<--------------->|   Gateway    |  |
|  |  Telegram   |   ws://127.0.0.1|   网关服务    |  |
|  |  WhatsApp   |      :18789     |   :18789     |  |
|  |  Discord    |                 +------+-------+  |
|  |  iMessage   |                        |          |
|  |  ...        |                        v          |
|  +------------+                 +--------------+   |
|                                 |   AI 推理层   |   |
|                                 |  Claude / GPT |   |
|                                 |  / 本地模型    |   |
|                                 +------+-------+   |
|                                        |           |
|                                        v           |
|                                 +--------------+   |
|                                 |   工具执行层   |   |
|                                 |  浏览器控制    |   |
|                                 |  文件读写      |   |
|                                 |  Shell 执行    |   |
|                                 |  定时任务      |   |
|                                 |  5700+ 技能   |   |
|                                 +--------------+   |
+--------------------------------------------------+
```

**第一层：消息渠道层**
负责接收你从各个聊天平台发来的消息，并将其标准化为统一格式。不管你从 Telegram 还是 WhatsApp 发消息，到达 Gateway 时格式是一样的。

**第二层：Gateway 网关层**
运行在 `ws://127.0.0.1:18789`，是整个系统的"中枢神经"。它管理所有客户端连接、认证会话、工具编排，是 MoltBot 从"聊天机器人"升级为"Agent 平台"的关键。

**第三层：AI 推理层**
这是 MoltBot 的"大脑"。它接收标准化消息后，结合上下文（记忆、可用技能、系统状态），通过大语言模型（LLM）决定下一步该做什么。MoltBot 采用了一种叫做 **Mega Prompt** 的技术，将你的指令、可用数据和系统状态动态融合，让 AI 做出最优判断。

MoltBot 是模型无关的（model-agnostic），支持：
- **云端模型**：Anthropic Claude（推荐）、OpenAI GPT 系列、DeepSeek
- **本地模型**：通过 Ollama 运行 Llama 等开源模型（免费但能力较弱）

**第四层：工具执行层**
AI 做出决策后，由工具层负责实际执行。包括浏览器控制（CDP 协议）、文件操作、Shell 命令、HTTP 请求、定时任务等。

### 3.2 一次请求的完整流程

以"帮我查看今天的邮件并摘要"为例：

```
1. 你在 Telegram 发送消息："帮我看看今天有什么重要邮件"

2. Telegram Bot API 将消息推送到本地 Gateway

3. Gateway 将消息标准化，传递给 AI 推理层

4. AI 推理层查阅记忆（你用的是 Gmail）和可用技能，
   决定调用 "Gmail 邮件读取" 技能

5. 工具层执行 Gmail API 调用，获取今日邮件列表

6. AI 推理层对邮件内容进行分析和摘要

7. 摘要结果通过 Gateway 返回到 Telegram

8. 你在手机上看到摘要消息
```

整个过程耗时通常在 10-30 秒，取决于邮件数量和 API 响应速度。

### 3.3 技术栈

| 组件 | 技术选型 |
|------|---------|
| 编程语言 | TypeScript |
| 包管理器 | pnpm |
| 运行时 | Node.js >= 22 |
| 浏览器控制 | Chrome DevTools Protocol (CDP) |
| 通信协议 | WebSocket |
| 记忆存储 | 本地 Markdown 文件 |
| 发布渠道 | stable / beta / dev 三轨制 |

想了解更详细的架构剖析，推荐阅读 [OpenClaw 架构深度解析](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/)。

---

## 四、改名历史：从 Clawdbot 到 MoltBot 到 OpenClaw

MoltBot 的改名故事本身就是一个值得记录的开源社区事件，**它在不到一周内完成了三次更名，堪称开源史上最快的品牌重塑**。

### 4.1 第一阶段：Clawdbot（2025年11月 - 2026年1月27日）

项目最初叫 **Clawdbot**，由 Peter Steinberger 于 2025 年 11 月发布。"Clawd" 是 "Claude" 的谐音变体（龙虾的爪子 = Claw），因为项目最初主要基于 Anthropic 的 Claude 模型。

项目在 2026 年 1 月中旬开始病毒式传播，**不到一周就拿下 8 万+ GitHub Star**，成为当时增长最快的开源项目之一。

### 4.2 第二阶段：MoltBot（2026年1月27日 - 1月29日）

2026 年 1 月 27 日，Anthropic 以商标相似为由，要求项目更名。"Clawd" 和 "Claude" 在视觉和发音上太过接近，容易让人误以为是 Anthropic 官方产品。

Steinberger 将项目改名为 **MoltBot**。"Molt" 在英文中是"蜕壳"的意思——龙虾要长大，必须脱掉旧壳。这个名字既保留了龙虾吉祥物的精神，又暗喻项目的"蜕变升级"。

然而改名过程中发生了严重的安全事件。Steinberger 在重命名 GitHub 组织和 X（Twitter）账号时，**释放旧账号和注册新账号之间出现了约 10 秒的时间窗口**。职业"账号狙击手"（handle snipers）立刻抢注了被释放的账号，加密货币骗子随即利用劫持的"官方"账号推广一个名叫 $CLAWD 的假代币。该代币市值在数小时内被炒到 1600 万美元，随后暴跌 90%。

### 4.3 第三阶段：OpenClaw（2026年1月29日至今）

仅两天后的 1 月 29 日，项目再次更名为 **OpenClaw**。新名字强调了两层含义：

- **Open**：开源精神
- **Claw**：龙虾的传承

这次更名也是为了与改名风波中的安全事件做一次彻底的切割。

### 4.4 最新动态：创始人加入 OpenAI

2026 年 2 月 15 日，Sam Altman 宣布 Peter Steinberger 加入 OpenAI，负责"下一代个人 Agent"的开发。Steinberger 表示："我想改变世界，而不是建一个更大的公司。与 OpenAI 合作是把这个愿景带给每个人的最快方式。"

OpenClaw 项目将移交给一个独立的开源基金会，由 OpenAI 提供支持，继续保持开源。

更多关于这个事件的分析，可以阅读 [OpenClaw 创始人加入 OpenAI 意味着什么](/posts/ai/2026-02-16-openclaw-openai-analysis/)。

> **总结改名时间线**：Clawdbot（2025.11）-> MoltBot（2026.1.27）-> OpenClaw（2026.1.29）。不管用哪个名字搜索，说的都是同一个项目。

---

## 五、MoltBot 与其他 AI Agent 的对比

2026 年是 AI Agent 元年，市面上涌现了大量类似产品。MoltBot（OpenClaw）在其中处于什么位置？

### 5.1 主要竞品对比

| 特性 | MoltBot/OpenClaw | Claude Code | Manus | HyperWrite |
|------|-----------------|-------------|-------|------------|
| **定位** | 个人全能助手 | 开发者编程助手 | 通用 AI Agent | 浏览器自动化 |
| **开源** | 是 | 否 | 否 | 否 |
| **运行位置** | 本地自托管 | 本地终端 | 云端 | 浏览器扩展 |
| **交互方式** | 聊天平台 | 命令行 | 网页界面 | 浏览器 |
| **数据隐私** | 数据不离开本地 | 代码不离开本地 | 数据在云端 | 数据在云端 |
| **上手难度** | 中等（需部署） | 低（直接安装） | 低（网页访问） | 低（安装扩展） |
| **适用人群** | 技术爱好者 | 开发者 | 所有人 | 所有人 |
| **持久记忆** | 有（本地文件） | 有（CLAUDE.md） | 有限 | 无 |
| **自主执行** | 强（24/7 后台） | 中（需要终端） | 强 | 中 |

### 5.2 什么时候该选 MoltBot

**适合你的场景**：

- 你重视数据隐私，不想把个人数据上传到云端
- 你有一台可以 24 小时运行的设备（Mac Mini、VPS 等）
- 你需要一个能跨平台（邮件、日历、浏览器、文件系统）统一操作的助手
- 你享受折腾和定制的乐趣
- 你希望 AI 助手能记住你的长期偏好

**不适合你的场景**：

- 你没有技术背景，不想折腾部署
- 你只需要一个编程助手（用 [Claude Code](/posts/ai/2025-01-14-claude-code-guide/) 更合适）
- 你对安全风险零容忍（MoltBot 的安全机制仍在完善中）
- 你只是偶尔需要 AI 帮忙（直接用 ChatGPT/Claude 网页版就够了）

### 5.3 MoltBot 生态圈

MoltBot 不只是一个工具，它已经形成了一个小生态：

- **OpenClaw**：核心 Agent 项目
- **MoltBook**：AI Agent 社交网络，超过 160 万 AI Agent 注册，被称为"Agent 互联网的首页"
- **MoltWorker**：Cloudflare 推出的云端版本，不需要本地硬件
- **ClawHub**：技能市场，5700+ 社区贡献的技能插件

想了解 MoltBook 的故事，可以阅读 [MoltBook：当 AI Agent 有了自己的社交网络](/posts/ai/2026-02-01-moltbook-ai-agent-social-network/)。

---

## 六、上手指南：快速部署 MoltBot

### 6.1 硬件需求

MoltBot 需要一台 24 小时运行的设备。推荐方案：

| 方案 | 成本 | 优势 | 劣势 |
|------|------|------|------|
| **Mac Mini M4** | 约 4000 元 | 低功耗（6-8W）、支持 iMessage | 初始投入高 |
| **云服务器 VPS** | 约 50-100 元/月 | 无需本地硬件 | 不支持 iMessage |
| **旧笔记本/台式机** | 0 元（已有） | 零成本 | 功耗高、噪音大 |
| **树莓派 5** | 约 500 元 | 超低功耗、体积小 | 性能有限 |

### 6.2 安装步骤

**前提条件**：
- Node.js >= 22
- pnpm（包管理器）
- 一个 LLM 的 API Key（推荐 Anthropic Claude）

**一键安装**：

```bash
curl -sSL https://get.moltbot.org/install.sh | bash
```

安装程序会自动检测你的操作系统并完成配置。安装完成后，MoltBot 会启动一个交互式终端界面（TUI），引导你完成初始设置。

**Docker 安装**（推荐，更安全）：

```bash
# 拉取镜像
docker pull openclaw/openclaw:latest

# 运行容器
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  -e ANTHROPIC_API_KEY=your-api-key-here \
  openclaw/openclaw:latest
```

### 6.3 配置 Telegram 接入

以最常用的 Telegram 为例：

```
步骤 1：在 Telegram 中搜索 @BotFather，发送 /newbot 创建机器人
步骤 2：获取 Bot Token
步骤 3：在 MoltBot 配置中填入 Token
步骤 4：向你的 Bot 发送第一条消息
```

在 MoltBot 的 TUI 界面中选择 "Messaging" -> "Telegram"，粘贴你的 Bot Token 即可。

### 6.4 第一次对话

配置完成后，尝试在 Telegram 中发送：

```
帮我检查一下当前系统的磁盘使用情况
```

MoltBot 会执行 `df -h` 命令，并将结果以易读的格式回复给你。

再试试更复杂的任务：

```
帮我写一个 Python 脚本，每小时检查一次 example.com 是否正常响应，
如果不正常就通过 Telegram 通知我
```

MoltBot 会编写脚本、设置 cron 定时任务，并配置通知——全部自动完成。

### 6.5 安全配置（必做）

在开始使用之前，请**务必**完成以下安全配置：

```bash
# 1. 创建专用低权限用户
sudo useradd -m -s /bin/bash openclaw-user
sudo su - openclaw-user

# 2. 限制文件访问范围
chmod 700 ~/.openclaw

# 3. 配置防火墙（如果在 VPS 上）
# 只允许本地访问 Gateway 端口
sudo ufw deny 18789
sudo ufw allow from 127.0.0.1 to any port 18789
```

更详细的安全部署指南，请参考 [Moltbot 深度解析中的安全章节](/posts/ai/2026-01-29-moltbot-deep-dive/)。

---

## 七、安全风险与注意事项

MoltBot 虽然强大，但"能操作你电脑的 AI"本身就是一把双刃剑。在使用前，你必须了解以下风险：

### 7.1 已知安全隐患

1. **明文存储凭证**：API Key、OAuth 令牌以明文存储在本地文件中
2. **提示注入攻击**：恶意邮件可能诱导 MoltBot 执行非预期操作
3. **反向代理认证绕过**：在 Nginx 后运行时，认证可能失效
4. **信息窃取恶意软件**：已有恶意软件专门针对 MoltBot 的本地存储

Palo Alto Networks 将 MoltBot 称为安全"致命三合一"：拥有私人数据访问权、暴露于不可信内容、且能执行外部通信并保留记忆。

### 7.2 安全使用原则

| 原则 | 具体做法 |
|------|---------|
| **最小权限** | 不要以 root 运行，创建专用低权限用户 |
| **渐进授权** | 从只读权限开始，确认安全后再逐步开放 |
| **网络隔离** | 不要裸露端口到公网，使用防火墙 |
| **容器化** | 优先使用 Docker 运行，限制访问范围 |
| **定期审查** | 定期检查 `~/.openclaw/` 目录下的凭证文件 |
| **选好模型** | Claude Opus 4.5 的提示注入防护相对更强 |

想了解更多自动化中的安全陷阱，推荐阅读 [OpenClaw 自动化的那些坑](/posts/ai/2026-02-14-openclaw-automation-pitfalls/)。

---

## 八、常见问题

### MoltBot 和 OpenClaw 是同一个东西吗？

是的。项目经历了三次改名：Clawdbot -> MoltBot -> OpenClaw。目前官方名称是 OpenClaw，但很多人仍然习惯叫它 MoltBot。所有三个名字指的都是同一个项目。

### MoltBot 是免费的吗？

MoltBot（OpenClaw）本身是开源免费的。但你需要为 AI 模型的 API 调用付费（如 Anthropic Claude API）。如果使用本地模型（通过 Ollama），则完全免费，但智能程度会有所下降。

### MoltBot 需要什么配置的电脑？

对硬件要求不高。Mac Mini M4 是社区最推荐的方案（低功耗 + macOS 生态）。VPS（2核4G 以上）也完全可以。MoltBot 本身不做 AI 推理，AI 运算在云端完成。

### MoltBot 安全吗？

有风险。它能操作你的电脑，一旦被利用就等同于电脑被入侵。建议在 Docker 容器中运行、使用低权限用户、不要暴露端口。对安全零容忍的用户建议先观望。

### MoltBot 和 MoltBook 是什么关系？

MoltBot（OpenClaw）是个人 AI Agent 项目。MoltBook 是一个 AI Agent 社交网络平台（由 Matt Schlicht 创建），两者是独立项目，但 MoltBook 最初是为 MoltBot Agent 设计的社交空间。

### 现在还值得入坑 MoltBot 吗？

如果你是技术爱好者，想体验"个人 AI Agent"的未来形态，值得一试。但要做好安全防护，并对不稳定性有心理准备。如果只是好奇，读完这篇文章了解一下就够了。

---

## 总结

MoltBot（现 OpenClaw）代表了 AI 发展的一个重要方向：**从对话式 AI 到行动式 AI 的跨越**。它让 AI 不再只是回答问题的工具，而是能真正替你执行任务的数字助手。

从 2025 年 11 月创建到 2026 年 2 月创始人加入 OpenAI，这个项目在短短几个月内经历了爆发式增长、三次改名、加密骗局、安全争议和商业化转型。它的故事本身就是 AI Agent 时代的一个缩影。

对于大多数人来说，**MoltBot 的意义不在于你是否需要立刻使用它，而在于它展示了一种全新的人机交互范式**——AI 在后台持续运行，记住你的一切偏好，随时准备为你工作。这个方向，大概率会成为未来几年 AI 产品的主流形态。

---

## 相关阅读

- [Moltbot 深度解析：从爆火到改名，个人 AI Agent 的机遇与暗礁](/posts/ai/2026-01-29-moltbot-deep-dive/) - 深度分析文章
- [OpenClaw 架构深度解析](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) - 技术架构详解
- [OpenClaw 实用教程](/posts/ai/2026-02-12-openclaw-usage-tutorial/) - 实操教程
- [OpenClaw 记忆系统策略解析](/posts/ai/2026-01-31-openclaw-memory-strategy/) - 记忆系统设计
- [OpenClaw 自动化的那些坑](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) - 避坑指南
- [OpenClaw 创始人加入 OpenAI 意味着什么](/posts/ai/2026-02-16-openclaw-openai-analysis/) - 最新动态分析
- [MoltBook：当 AI Agent 有了自己的社交网络](/posts/ai/2026-02-01-moltbook-ai-agent-social-network/) - 生态延伸
- [ClawdBot 搭建指南](/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/) - 新手安装教程
- [Claude Code 完全指南](/posts/ai/2025-01-14-claude-code-guide/) - 另一种 AI Agent 体验

---

## 参考资源

- [OpenClaw 官网](https://molt.bot)
- [OpenClaw GitHub](https://github.com/moltbot/moltbot)（145,000+ Star）
- [OpenClaw 官方文档](https://docs.openclaw.ai/start/getting-started)
- [ClawHub 技能市场](https://clawdhub.com)
- [TechCrunch: 关于 Clawdbot (MoltBot) 你需要知道的一切](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/)
- [TechCrunch: OpenClaw 创始人加入 OpenAI](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)
- [CNBC: 从 Clawdbot 到 MoltBot 到 OpenClaw](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html)
- [Palo Alto Networks: MoltBot 安全风险分析](https://www.paloaltonetworks.com/blog/network-security/why-moltbot-may-signal-ai-crisis/)
- [Cloudflare: MoltWorker 云端方案](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/)
