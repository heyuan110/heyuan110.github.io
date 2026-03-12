+++
date = '2026-03-05T09:00:00+08:00'
draft = false
title = 'OpenClaw 安装配置完全指南：从零搭建你的私人 AI Agent'
description = 'OpenClaw 完整安装教程，涵盖一键安装、Telegram/WhatsApp 消息平台对接、AI 模型配置、Skills 插件管理、多 Agent 协作入门以及安全加固最佳实践。'
toc = true
tags = ['OpenClaw', 'AI Agents', 'Self-Hosted AI', 'Telegram Bot', 'Automation']
categories = ['AI Guides']
keywords = ['OpenClaw 安装教程', 'OpenClaw 配置', 'OpenClaw 使用指南', 'Moltbot 安装', 'OpenClaw Telegram', 'OpenClaw WhatsApp', '私人 AI Agent 搭建', 'OpenClaw 入门']

[[params.faqItems]]
question = "OpenClaw 的系统要求是什么？"
answer = "OpenClaw 需要 Node.js 20 以上版本、至少 16GB 内存（多 Agent 建议 32GB），支持 macOS、Linux 和 Windows（WSL2）。推荐使用 Apple Mac Mini M4 或类似 ARM 设备 7×24 小时运行，功耗低且 AI 推理性能强。"

[[params.faqItems]]
question = "OpenClaw 和 Moltbot、Clawdbot 是同一个项目吗？"
answer = "是的。OpenClaw、Moltbot 和 Clawdbot 是同一个项目在不同阶段的名称。最初叫 Clawdbot，因 Anthropic 商标问题改名 Moltbot，最终定名 OpenClaw。现在所有文档和命令统一使用 OpenClaw。"

[[params.faqItems]]
question = "运行 OpenClaw 要花多少钱？"
answer = "OpenClaw 本身免费开源，你只需为 AI 模型的 API 调用付费。根据使用量不同，月均费用大约 5-30 美元。日常任务用 Claude Sonnet 或 GPT-4.1 就能控制成本。也可以通过 Ollama 跑免费的本地模型。"

[[params.faqItems]]
question = "OpenClaw 能控制浏览器和自动化任务吗？"
answer = "可以。OpenClaw 支持内置的浏览器自动化 Skill，能执行 Shell 命令、读写本地文件、发送邮件、管理日历，还能把多个步骤串联成复杂的自动化工作流——所有操作都可以通过 Telegram、WhatsApp 等消息平台触发。"

[[params.faqItems]]
question = "在自己电脑上跑 OpenClaw 安全吗？"
answer = "OpenClaw 提供多层安全防护：沙箱模式限制文件系统访问范围，配对模式要求设备授权，权限控制可以限定每个 Agent 可用的工具，所有数据都保存在本地。任何对外暴露的部署都建议开启沙箱模式和配对认证。"
+++

![OpenClaw 安装配置指南：涵盖安装部署、参数配置和私人 AI Agent 自动化](cover.webp)

想拥有一个 7×24 小时运行在自己电脑上、通过 Telegram 或 WhatsApp 就能下达指令、而且真正帮你执行任务而不只是聊天的私人 AI Agent？[OpenClaw](https://github.com/openclaw/openclaw) 就是干这个的。它是一个开源 AI Agent 网关，能把你的电脑变成 AI 自动化的指挥中心。

本文将带你走完 OpenClaw 的全流程：从安装、对接消息平台、配置 AI 模型、安装 Skills 插件，到安全加固。读完之后，你就能拥有一个随时随地可以发消息调度的私人 AI Agent。

## OpenClaw 是什么（为什么有三个名字？）

OpenClaw 是奥地利开发者 **Peter Steinberger**（[@steipete](https://github.com/steipete)）创建的开源私人 AI Agent 项目。上线第一周就斩获 80,000+ GitHub Stars，目前已突破 247,000+，是开源史上增长最快的项目之一。

但如果你之前搜过相关资料，可能会看到三个名字在互换使用。来捋一下：

| 名称 | 时间段 | 原因 |
|------|--------|------|
| **Clawdbot** | 2026 年初 | 项目爆火时的原始名称 |
| **Moltbot** | 2026 年 1-2 月 | 因与 Anthropic 商标"Claude"过于相似而改名 |
| **OpenClaw** | 2026 年 2 月至今 | 最终定名，所有文档和仓库统一使用 |

**这三个名字指的是同一个项目。** 如果你看到旧教程里写的是 Moltbot 或 Clawdbot，核心概念完全相通——换个名字就行。当前的文档和 CLI 命令统一用 `openclaw`。

关于命名历史和核心架构的详细介绍，请参考 [MoltBot（OpenClaw）完全解读：架构与发展历程](/posts/ai/2026-02-18-what-is-moltbot/)。

### OpenClaw 与众不同在哪里

ChatGPT 或 Claude 的 Web 界面只能生成文本，而 OpenClaw 是一个**执行引擎**，它能：

- 在你的电脑上运行 Shell 命令
- 操控浏览器并与 Web 应用交互
- 读写本地文件系统
- 跨平台发送消息（Telegram、WhatsApp、Discord、iMessage）
- 定时执行周期性任务
- 管理邮件、日历和通知
- 将多个操作串联成复杂的工作流

简单来说，就像是从"找个同事帮你出主意"升级成"让他坐到你电脑前直接干活"。

## 系统要求

开始之前，确认你的设备满足以下条件：

### 硬件

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| **内存** | 16 GB | 32 GB（多 Agent 场景） |
| **CPU** | 任何现代 x86/ARM | Apple Silicon M 系列 |
| **存储** | 10 GB 可用空间 | 50 GB+（跑本地模型需要） |
| **网络** | 稳定联网 | 有线以太网优先 |

**最佳方案是 Apple Mac Mini M4** ——功耗极低（电费几乎可以忽略）、AI 推理性能出色、体积小巧可以塞到显示器后面。很多 OpenClaw 重度用户就是这样把它当无头服务器用的。

如果你打算同时跑本地 AI 模型，内存建议升到 32 GB 以上。如果只用云端 API（Claude、GPT），16 GB 完全够用。

### 软件

| 依赖项 | 版本 | 安装方式 |
|--------|------|---------|
| **Node.js** | 20+ | `brew install node` 或 [nodejs.org](https://nodejs.org/) |
| **npm/pnpm** | 最新版 | Node.js 自带 / `npm i -g pnpm` |
| **Git** | 任意 | `brew install git` 或系统自带 |
| **操作系统** | macOS / Linux / WSL2 | 原生 Windows 不支持，请使用 WSL2 |

验证你的环境：

```bash
# 检查 Node.js 版本（必须 20+）
node --version

# 检查 npm
npm --version

# 检查 git
git --version
```

## 安装步骤

### 方式一：一键安装（推荐）

最快上手方式——一条命令搞定：

```bash
# macOS / Linux
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows（WSL2 / PowerShell）
iwr -useb https://openclaw.ai/install.ps1 | iex
```

脚本会全局安装 OpenClaw CLI，并在 `~/.openclaw/` 下创建所需的目录结构。

### 方式二：通过 npm 安装

如果你更习惯用 npm 管理：

```bash
# 全局安装
npm install -g openclaw@latest

# 或用 pnpm
pnpm add -g openclaw@latest
```

### 方式三：Docker

适合容器化部署（服务器环境推荐）：

```bash
# 拉取官方镜像
docker pull openclaw/openclaw:latest

# 启动并挂载持久化存储
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/data/openclaw \
  openclaw/openclaw:latest
```

### 验证安装

安装完成后，确认一切正常：

```bash
# 查看版本
openclaw --version

# 查看可用命令
openclaw help
```

如果能看到版本号和命令列表就说明安装成功。如果提示"command not found"，请确认 npm 全局 bin 目录已加入 PATH。

## 初始配置：引导向导

OpenClaw 自带引导向导，会帮你完成最关键的配置步骤。这是上手的最佳方式：

```bash
openclaw onboard --install-daemon
```

`--install-daemon` 参数会额外把 OpenClaw 注册为后台服务，开机自动启动（macOS 用 `launchd`，Linux 用 `systemd`）。

向导会引导你完成：

1. **模型认证** ——连接 AI 模型供应商（Claude API、OpenAI API 或本地模型）
2. **网关配置** ——设置端口、安全令牌和基本参数
3. **频道对接** ——连接 Telegram、WhatsApp、Discord 等消息平台
4. **配对与白名单** ——控制谁能向你的 Agent 发送指令
5. **守护进程** ——可选的后台服务安装

如果你之前用过 Moltbot Wizard，这是它的升级版。更多背景请参考 [Moltbot Wizard 使用指南](/posts/ai/2026-01-28-moltbot-wizard-guide/)。

### 手动配置（备选方案）

如果你更喜欢手动编辑配置文件，主配置位于：

```
~/.openclaw/openclaw.json
```

这是一个 **JSON5** 格式文件（支持注释和末尾逗号）。下面是一个最小可运行配置：

```json5
{
  // 网关设置
  "gateway": {
    "port": 18789,
    "token": "你的安全令牌"  // 用于 TUI 和 API 访问
  },

  // 默认 Agent 配置
  "agents": {
    "main": {
      "model": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514"
      }
    }
  }
}
```

**注意**：OpenClaw 使用严格的 Schema 校验，配置字段名写错会导致网关无法启动。遇到问题时，运行 `openclaw doctor` 可以快速定位。

## 对接消息平台

OpenClaw 的核心体验是通过你日常使用的消息应用来交互。以下是主流平台的对接方法。

### Telegram（最受欢迎）

Telegram 是最简单也是最多人选择的平台，流程如下：

**1. 创建 Telegram Bot**

打开 Telegram，搜索 [@BotFather](https://t.me/BotFather)，发送：

```
/newbot
```

按提示为 Bot 命名，BotFather 会给你一个 **Bot Token**——复制保存好。

**2. 将 Token 添加到 OpenClaw**

可以通过向导添加，也可以手动编辑 `openclaw.json`：

```json5
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的_TELEGRAM_BOT_TOKEN",
      // 可选：限制为特定的 Chat ID
      "allowedChatIds": [123456789]
    }
  }
}
```

**3. 开始对话**

网关启动后，在 Telegram 里打开你的 Bot 发条消息，OpenClaw 会通过 Bot 回复你。

**安全提示**：务必设置 `allowedChatIds`，将 Bot 限制为你个人的 Telegram 账号。否则任何找到你 Bot 的人都能向它下达指令。

### WhatsApp

WhatsApp 通过 WhatsApp Web 协议对接：

```json5
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "pairing": true  // 需要扫码配对
    }
  }
}
```

启动网关后，终端会显示一个二维码。用手机 WhatsApp 扫码（设置 > 已关联设备 > 关联设备）。

**注意**：WhatsApp 由于使用非官方 API，连接稳定性不如 Telegram。追求最可靠体验的话，推荐 Telegram。

### Discord

Discord 需要先创建 Bot 应用：

1. 前往 [Discord 开发者门户](https://discord.com/developers/applications)
2. 创建新应用并添加 Bot
3. 复制 Bot Token
4. 将 Bot 邀请到你的服务器并赋予相应权限

```json5
{
  "channels": {
    "discord": {
      "enabled": true,
      "botToken": "你的_DISCORD_BOT_TOKEN",
      "allowedGuildIds": ["你的服务器ID"]
    }
  }
}
```

### Web 控制台

即使不连接任何消息平台，你也可以通过内置的 Web 界面与 OpenClaw 交互：

```bash
# 启动网关
openclaw gateway --port 18789

# 打开控制台（或直接访问 http://127.0.0.1:18789/）
openclaw dashboard
```

Web 控制台适合测试、监控 Agent 状态、以及不方便拿手机时的会话管理。

## 配置 AI 模型

OpenClaw 不绑定任何模型。你可以用云端 API、本地模型，也可以混合使用。

### Claude API（Anthropic）

Claude 是 OpenClaw 用户最常选择的模型，配置方法：

**1. 获取 API Key**

到 [console.anthropic.com](https://console.anthropic.com/) 注册并创建 API Key。

**2. 添加到 OpenClaw**

```json5
{
  "agents": {
    "main": {
      "model": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514"
      },
      "auth": {
        "anthropic": {
          "apiKey": "sk-ant-api03-你的KEY"
        }
      }
    }
  }
}
```

**Anthropic 模型选择**：

| 模型 | 适用场景 | 费用 |
|------|---------|------|
| `claude-opus-4-20250514` | 复杂推理、多步骤任务 | $$$ |
| `claude-sonnet-4-20250514` | 通用场景（推荐默认选项） | $$ |
| `claude-haiku-3-20250307` | 快速回复、简单任务 | $ |

大多数场景下，**Claude Sonnet** 在质量和成本之间的平衡最好。

### OpenAI API

```json5
{
  "agents": {
    "main": {
      "model": {
        "provider": "openai",
        "name": "gpt-4.1"
      },
      "auth": {
        "openai": {
          "apiKey": "sk-你的OPENAI-KEY"
        }
      }
    }
  }
}
```

从 [OpenClaw 2026.3.1](/posts/ai/2026-03-03-openclaw-2026-3-1-new-features/) 版本开始，OpenAI 模型默认使用 WebSocket 传输以获得更快的流式响应。

### 本地模型（Ollama）

如果你想完全在本地运行，零 API 费用：

**1. 安装 Ollama**

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**2. 拉取模型**

```bash
# 通用能力较强的模型
ollama pull llama3.1:70b

# 轻量模型，适合测试
ollama pull llama3.1:8b
```

**3. 配置 OpenClaw**

```json5
{
  "agents": {
    "main": {
      "model": {
        "provider": "ollama",
        "name": "llama3.1:70b",
        "endpoint": "http://localhost:11434"
      }
    }
  }
}
```

**实话实说**：本地模型在 Agent 场景下的能力和 Claude 或 GPT-4.1 差距明显。回答简单问题还行，但多步骤工具调用就力不从心了。如果你是认真搞自动化的，云端 API 的费用很值得。

### 混合模型策略

一个更实用的方案是为不同任务分配不同模型：

```json5
{
  "agents": {
    // 主力 Agent：用强模型处理复杂任务
    "main": {
      "model": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514"
      }
    },
    // 快速 Agent：用便宜模型处理简单查询
    "quick": {
      "model": {
        "provider": "anthropic",
        "name": "claude-haiku-3-20250307"
      }
    },
    // 本地 Agent：零成本处理基础任务
    "local": {
      "model": {
        "provider": "ollama",
        "name": "llama3.1:8b"
      }
    }
  }
}
```

这样既能控制成本，又能确保复杂任务获得足够的模型能力。

## 启动网关

网关是 OpenClaw 的核心进程——在后台运行，连接消息平台、维护会话、将消息路由到对应的 Agent。

### 前台启动（用于调试）

```bash
openclaw gateway --port 18789
```

终端会输出日志，方便初始调试。

### 注册为后台服务

如果在引导阶段已经用了 `--install-daemon`，后台服务就已经设好了。否则手动设置：

```bash
# macOS（launchd）
openclaw daemon install
openclaw daemon start

# Linux（systemd）
openclaw daemon install
sudo systemctl start openclaw
```

### 确认网关运行状态

```bash
# 快速状态检查
openclaw status

# 详细健康检查
openclaw health

# 深度诊断
openclaw status --deep
```

### 查看日志

```bash
# 实时跟踪日志
openclaw logs --follow

# 查看最近 100 行
openclaw logs --tail 100
```

## 终端交互界面（TUI）

除了消息平台，OpenClaw 还提供强大的终端交互界面：

```bash
openclaw tui
```

### 常用快捷键

| 按键 | 功能 |
|------|------|
| `Enter` | 发送消息 |
| `Esc` | 中止当前响应 |
| `Ctrl+C` | 清空输入（连按两次退出） |
| `Ctrl+D` | 退出 TUI |
| `Ctrl+L` | 模型选择器 |
| `Ctrl+G` | Agent 选择器 |
| `Ctrl+P` | 会话选择器 |
| `Ctrl+O` | 切换工具输出显示 |

### 消息投递到平台

默认情况下，TUI 的回复**不会**转发到消息平台。这是一个安全设计——你不会希望测试消息意外出现在 Telegram 聊天里。

如需开启投递：

```bash
# 在 TUI 中输入: /deliver on

# 或启动时直接启用
openclaw tui --deliver
```

## 安装 Skills 插件

Skills 是让 OpenClaw 具备各种超能力的插件系统。官方市场 [ClawHub](https://clawhub.ai/) 上有 5,700+ 社区贡献的 Skills。

### 安装 ClawHub CLI

```bash
# 安装包管理器
npm i -g clawdhub

# 验证
clawdhub --version
```

**注意**：命令是 `clawdhub`（带字母"d"），不是 `clawhub`。很多旧教程写错了。

### 推荐首装的 Skills

大多数用户第一批会装这三个：

```bash
# 网络搜索能力
clawdhub install tavily-search

# Skill 发现（帮你找到需要的 Skill）
clawdhub install find-skills

# 主动行为（Agent 主动发起操作）
clawdhub install proactive-agent
```

**注意**：`proactive-agent` 以前叫 `proactive-agent-1-2-4`，旧名称在 ClawHub 上已失效，请用 `proactive-agent`。

### 常用 ClawHub 命令

| 命令 | 说明 |
|------|------|
| `clawdhub search "关键词"` | 搜索 Skills |
| `clawdhub install <slug>` | 安装 Skill |
| `clawdhub list` | 列出已安装的 Skills |
| `clawdhub update --all` | 更新所有 Skills |
| `clawdhub info <slug>` | 查看 Skill 详情 |

### 关于 Skills 数量的坑

一个常见错误是一口气装几十个 Skills，然后期望一切自动运转。实际上 Skills 越多，Agent 需要管理的上下文就越大，容易导致行为混乱和 Token 费用飙升。

建议从 3-5 个核心 Skills 起步，有明确需求时再添加。关于这个问题的深入分析，推荐阅读 [OpenClaw 自动化踩坑实录：3 个 Skills 远远不够](/posts/ai/2026-02-14-openclaw-automation-pitfalls/)。

## 多 Agent 配置入门

OpenClaw 最强大的功能之一就是在一个实例上运行多个专精 Agent。与其让一个 Agent 什么都干，不如为不同领域创建各自专注的 Agent。

### 为什么要用多个 Agent？

一个 Agent 同时负责调研、编码、写作和个人事务，迟早会撞上三面墙：

1. **记忆膨胀** ——随着跨领域上下文的积累，Agent 越来越慢
2. **上下文污染** ——编程知识渗入写作任务，反之亦然
3. **成本爆炸** ——每次请求都携带大量无关上下文，Token 消耗飙升

多 Agent 架构通过缩小每个 Agent 的职责范围来解决这些问题。

### 基础双 Agent 配置

一个实用的双 Agent 配置示例：

```json5
{
  "agents": {
    // 个人助手：处理日常事务，绑定 Telegram
    "assistant": {
      "model": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514"
      },
      "workspace": "~/.openclaw/workspace-assistant",
      "routes": ["telegram-personal"]
    },

    // 调研 Agent：处理调研任务，绑定 WhatsApp
    "research": {
      "model": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514"
      },
      "workspace": "~/.openclaw/workspace-research",
      "routes": ["whatsapp-main"]
    }
  }
}
```

每个 Agent 拥有独立的：

- **工作空间** ——独立的记忆、提示词和文件
- **路由** ——绑定到特定的消息频道
- **模型配置** ——可以使用不同的模型或 API Key

### 通过命令行管理 Agent 路由

从 [OpenClaw 2026.3.1](/posts/ai/2026-03-03-openclaw-2026-3-1-new-features/) 版本开始，支持命令行管理路由：

```bash
# 将 Agent 绑定到消息账号
openclaw agents bind --agent assistant --account telegram-personal

# 查看所有绑定关系
openclaw agents bindings

# 解绑
openclaw agents unbind --agent research --account whatsapp-main
```

关于多 Agent 的高级模式——包括层级式、流水线式和协作式架构——请阅读 [OpenClaw 多 Agent 深度指南](/posts/ai/2026-02-23-openclaw-multi-agent-guide/)。

### 工作空间结构

每个 Agent 的工作空间遵循以下目录结构：

```
~/.openclaw/workspace-<agentId>/
├── SOUL.md         # Agent 人设与角色定义
├── AGENTS.md       # 行为规则与约束
├── USER.md         # 关于你的信息（共享偏好）
├── PROMPT.md       # 自定义提示词模板
├── IDENTITY.md     # Agent 身份定义
└── memory/         # 持久化记忆存储
    └── 2026-03-05.md
```

`SOUL.md` 文件定义了每个 Agent 的独特个性。比如个人助手的 SOUL.md 可以写"你是一个专注于效率和日程规划的私人助手"，而调研 Agent 的则写"你是一个严谨的调研分析师，提供充分引用的深度分析"。

关于 OpenClaw 如何跨 Agent 管理记忆的详解，请参考 [OpenClaw 记忆策略分析](/posts/ai/2026-01-31-openclaw-memory-strategy/)。

## 安全最佳实践

OpenClaw 运行在你的个人电脑上，可以执行命令。安全不是可选项。以下是你必须配置的安全措施。

### 1. 启用沙箱模式

沙箱模式限制 Agent 在文件系统上的访问范围：

```json5
{
  "security": {
    "sandbox": {
      "enabled": true,
      "allowedPaths": [
        "~/.openclaw/workspace",
        "~/Documents/openclaw-work"
      ],
      "blockedPaths": [
        "~/.ssh",
        "~/.aws",
        "~/.gnupg"
      ]
    }
  }
}
```

不开沙箱的话，Agent 可以读写你用户账号下的任何文件——包括 SSH 密钥、云服务凭证和浏览器 Cookie。**请务必开启沙箱模式。**

### 2. 启用配对模式

配对模式要求设备授权后才能发送指令：

```json5
{
  "security": {
    "pairing": {
      "enabled": true,
      "requireApproval": true
    }
  }
}
```

开启后，新设备必须经过审批才能与你的 Agent 交互。这能防止陌生人通过你的 Telegram Bot 在你电脑上执行命令。

### 3. 限制工具权限

控制每个 Agent 可以使用哪些工具：

```json5
{
  "agents": {
    "assistant": {
      "tools": {
        "allowed": ["web-search", "calendar", "email"],
        "blocked": ["shell-exec", "file-write"]
      }
    },
    "devops": {
      "tools": {
        "allowed": ["shell-exec", "file-read", "file-write"],
        "blocked": ["email", "browser"]
      }
    }
  }
}
```

原则是：每个 Agent 只能访问它实际需要的工具。日历助手不需要 Shell 权限。

### 4. 设置网关令牌

为 TUI 和 API 访问设置一个强令牌：

```json5
{
  "gateway": {
    "token": "至少32位的随机字符串"
  }
}
```

生成方式：

```bash
openssl rand -hex 32
```

### 5. 配置 Chat ID 白名单

每个消息平台都要限制只允许已知账号访问：

```json5
{
  "channels": {
    "telegram": {
      "allowedChatIds": [123456789],   // 你的 Telegram 用户 ID
      "allowedGroupIds": [-100123456]  // 指定群组
    }
  }
}
```

查看你的 Telegram 用户 ID，可以在 Telegram 上给 [@userinfobot](https://t.me/userinfobot) 发条消息。

### 安全检查清单

在将 OpenClaw 暴露到任何网络之前，请逐项确认：

- [ ] 沙箱模式已启用，并设置了明确的路径白名单
- [ ] 所有频道都启用了配对模式
- [ ] 网关令牌已设置（32 位以上）
- [ ] 每个频道都配置了 Chat/User ID 白名单
- [ ] 敏感目录已屏蔽（`~/.ssh`、`~/.aws` 等）
- [ ] 每个 Agent 的工具权限已按需限定

## 常见问题与排查

### 网关无法启动

**现象**：`openclaw gateway` 立即退出或显示 Schema 校验错误。

**解决**：运行诊断命令：

```bash
openclaw doctor --fix
```

该命令会检查配置文件的 Schema 错误、缺失字段和权限问题。`--fix` 参数会尝试自动修复。

常见原因：
- `openclaw.json` 中有拼写错误（严格 Schema 校验）
- 端口 18789 被占用——更换端口或终止占用进程
- Node.js 版本过低（需要 20+）

### Telegram Bot 无响应

**现象**：给 Telegram Bot 发消息，但没有回复。

**排查步骤**：

1. 网关是否在运行？用 `openclaw status` 检查
2. Bot Token 是否正确？在 BotFather 里再次核对
3. 你的 Chat ID 是否在白名单中？临时移除 `allowedChatIds` 测试
4. 查看日志中是否有报错：`openclaw logs --follow`

### Token 用量/费用过高

**现象**：API 账单超出预期。

**解决方案**：

- 简单任务用便宜模型（Haiku 处理通知，Sonnet 处理正经活儿）
- 减少已安装的 Skills 数量（每个 Skill 都会增加系统提示词）
- 启用会话隔离——不要让无关对话共享上下文
- 在模型配置中设置 Token 限制

```json5
{
  "agents": {
    "main": {
      "model": {
        "maxTokens": 4096,  // 限制输出长度
        "maxInputTokens": 32000  // 限制输入上下文
      }
    }
  }
}
```

### Agent 似乎很困惑或"忘记"上下文

**现象**：Agent 给出矛盾的回答或跟丢任务线索。

**原因与解决**：

- **Skills 太多**：精简到核心几个。每个 Skill 都会增加系统提示词噪音
- **会话污染**：不相关的任务使用独立会话（TUI 中输入 `/session new`）
- **记忆过载**：定期清理旧记忆，或拆分成多个 Agent
- **模型选错**：本地模型和小模型处理复杂多步骤任务比较吃力

### WhatsApp 频繁断连

WhatsApp 使用的是非官方协议，断连在所难免。缓解方法：

```bash
# 检查连接状态
openclaw status --deep

# 重新连接
openclaw channels reconnect whatsapp
```

如果断连频繁，建议把 Telegram 作为主频道。

### 还需要帮助？

```bash
# 完整诊断报告
openclaw doctor

# 自动修复常见问题
openclaw doctor --fix

# 社区支持
# GitHub: https://github.com/openclaw/openclaw/issues
# Discord: https://discord.gg/openclaw
```

## 你的第一个自动化工作流

一切就绪后，来跑一个简单的自动化任务，验证端到端流程是否畅通。

### 每日新闻简报

通过 Telegram 给你的 Agent 发送这条消息：

```
每天早上 8 点，搜索当天最重要的 5 条 AI 新闻，
每条用 2-3 句话总结，然后把摘要发到这里。
```

装了 `tavily-search` 和 `proactive-agent` 之后，Agent 会：

1. 创建一个每天早上 8 点的定时任务
2. 用搜索 Skill 获取最新新闻
3. 总结搜索结果
4. 通过 Telegram 把简报发给你

### 快速任务委派

试试通过消息平台发送这些实用指令：

```
搜一下 4 月份从上海飞东京最便宜的航班，
给我列出前 3 个选项和价格。
```

```
读一下 ~/Documents/contract.pdf，
用要点列出里面的关键条款。
```

```
每小时检查一次 https://example.com，
如果网站挂了就提醒我。
```

这些例子体现了 OpenClaw 的真正价值——你掏出手机发条消息，Agent 就在你的电脑上完成剩下的工作。

## 接下来学什么

现在你已经有了一个可用的 OpenClaw 环境：消息平台已对接、AI 模型已配置、安全措施已到位。根据你的下一步需求，推荐继续阅读：

**深入理解架构：**
- [OpenClaw 架构深度剖析](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) ——了解内部设计与扩展点

**掌握多 Agent 模式：**
- [OpenClaw 多 Agent 深度指南](/posts/ai/2026-02-23-openclaw-multi-agent-guide/) ——层级式 Agent、流水线工作流、协作模式

**避开常见坑：**
- [OpenClaw 自动化踩坑实录](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) ——规模化运行时会遇到什么问题，以及如何解决

**了解开发工作流：**
- [OpenClaw 作者如何使用 Claude Code](/posts/ai/2026-01-31-openclaw-claude-code-workflow/) ——一个 200K+ Star 项目背后的开发方法论

**跟进最新动态：**
- [OpenClaw 2026.3.1 新功能](/posts/ai/2026-03-03-openclaw-2026-3-1-new-features/) ——WebSocket 传输、K8s 支持、Agent 路由 CLI

## 相关阅读

- [MoltBot（OpenClaw）完全解读：架构与发展历程](/posts/ai/2026-02-18-what-is-moltbot/) ——全面讲解 OpenClaw 是什么以及它的演变过程
- [OpenClaw 记忆策略分析](/posts/ai/2026-01-31-openclaw-memory-strategy/) ——OpenClaw 如何在会话之间管理持久化记忆
- [OpenClaw 架构深度剖析](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) ——内部架构与系统设计
- [OpenClaw 多 Agent 深度指南](/posts/ai/2026-02-23-openclaw-multi-agent-guide/) ——高级多 Agent 协作模式
- [OpenClaw 自动化踩坑实录](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) ——真实自动化场景中的经验教训
