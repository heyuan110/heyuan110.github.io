+++
date = '2026-01-29T21:00:00+08:00'
lastmod = '2026-02-22T10:00:00+08:00'
draft = false
title = 'Moltbot 是什么？8 万 Star 爆红项目的改名真相与安全避坑指南'
description = 'Moltbot（原 Clawdbot/OpenClaw）是 2026 年最火的开源 AI Agent，一周 8 万 Star，能 24 小时自主操控电脑。本文解析 Moltbot 改名原因、核心架构、安全隐患，帮你决定要不要用。'
toc = true
tags = ['OpenClaw', 'Moltbot', 'Clawdbot', 'AI Agent', '开源', '安全']
categories = ['AI原理']
keywords = ['Moltbot 是什么', 'Moltbot', 'OpenClaw', 'Moltbot 改名', 'Moltbot AI Agent', 'Clawdbot', 'Moltbot 介绍', 'Moltbot 原理', 'Moltbot 安全', 'moltbot是什么', 'moltbot改名', 'moltbot能做什么']
+++

**Moltbot 是什么？** 简单来说，Moltbot 是一个开源的个人 AI Agent（智能助手），它能 24 小时运行在你的电脑上，通过 Telegram、WhatsApp 等聊天工具接收指令，自主操作浏览器、处理邮件、执行各种任务——不只是聊天，而是真的帮你"干活"。它原名 Clawdbot，后改名 OpenClaw，是 2026 年初最火爆的开源 AI 项目之一。

2026 年 1 月，一只龙虾搅动了整个 AI 圈。这个名叫 Clawdbot 的开源项目在不到一周内拿下 8 万+ GitHub Star，让全球开发者疯狂下单 Mac Mini，甚至引发了一场加密货币骗局。随后，它因 Anthropic 的商标要求被迫改名为 **Moltbot**（"蜕壳"之意），又衍生出 **OpenClaw** 这一社区常用名称。围绕 Moltbot 改名的风波，至今仍是开源圈的热门话题。

这个 Moltbot AI Agent 到底有什么魔力？它是不是名副其实的"个人贾维斯"？背后又藏着多少你不知道的坑？

这篇文章，我们不聊安装教程（想看搭建指南可以移步[这篇文章](/zh/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/)），而是从架构原理、改名始末、安全风险等角度来深度剖析这个现象级项目，帮你全面了解 Moltbot 的背景与真相。

> 名称沿革说明：本文统一使用 **OpenClaw（原 Clawdbot，后更名 Moltbot）** 来指代同一项目在不同阶段的名称，便于你对照搜索结果与历史资料。

---

## 一、Moltbot 到底解决了什么问题？

### 1.1 从"聊天"到"干活"

过去两年，大家已经习惯了和 AI 聊天——问问题、写文案、翻译文章。但你有没有发现一个问题：**AI 只能"说"，不能"做"**。

你让 ChatGPT 帮你订机票，它只能告诉你"请打开携程网站，搜索……"。你让 Claude 帮你处理邮件，它只能说"建议你这样回复……"。

**Moltbot 不一样。** 它不只是给你建议，而是真的打开浏览器、登录你的邮箱、执行操作、把结果告诉你。

用冰河老师的话说：

> Clawdbot = Claude Code + Bot 化工作流。全自动写代码解决你生活中的各类任务，它就是小机器人。

### 1.2 从"坐在电脑前用"到"躺在沙发上用"

传统的 AI 工具有一个限制：你得坐在电脑前面用。打开浏览器，登录网页版 ChatGPT，一句一句地对话。

Moltbot 颠覆了这个模式。它 24 小时运行在你的电脑（或服务器）上，你通过 **Telegram、WhatsApp、iMessage** 等聊天工具远程发指令。

国外有个用户是这样描述的：

> "躺在床上看 Netflix 的时候，通过 Telegram 重建了整个网站。"

这才是 **AI Agent** 真正的价值——不是取代你的工作，而是在你不工作的时候帮你工作。

### 1.3 为什么大家疯抢 Mac Mini？

Moltbot 需要一台 24 小时运行的电脑。Mac Mini 成了首选，原因很简单：

- **低功耗**：待机只有 6-8 瓦，一个月电费不到 10 块钱
- **性能强**：M4 芯片跑 AI 工具绰绰有余
- **体积小**：放在桌角不占地方
- **macOS 生态**：原生支持 iMessage，这是 Windows/Linux 做不到的

有人甚至在炫耀自己有多少台 Mac Mini 组成的"AI 集群"。当然，你不需要这么夸张——一台就够了，甚至一台云服务器也能搞定。

---

## 二、技术架构拆解

Moltbot 的架构设计很巧妙，不是简单的"大模型套壳"，而是一套完整的 Agent 框架。

### 2.1 核心架构

```
┌──────────────────────────────────────────────────┐
│                    你的设备                        │
│                                                    │
│  ┌────────────┐    WebSocket     ┌──────────────┐ │
│  │  消息渠道   │◄──────────────►│   Gateway     │ │
│  │  Telegram   │    控制平面      │  网关服务      │ │
│  │  WhatsApp   │  ws://127.0.0.1 │  :18789       │ │
│  │  iMessage   │                 └──────┬───────┘ │
│  │  Discord    │                        │         │
│  │  Slack      │                        ▼         │
│  │  Signal     │                 ┌──────────────┐ │
│  │  Teams      │                 │   AI 大脑     │ │
│  └────────────┘                 │  Claude/GPT   │ │
│                                  │  /本地模型     │ │
│                                  └──────┬───────┘ │
│                                         │         │
│                                         ▼         │
│                                  ┌──────────────┐ │
│                                  │   工具层      │ │
│                                  │  浏览器控制    │ │
│                                  │  文件读写      │ │
│                                  │  Shell 执行    │ │
│                                  │  定时任务      │ │
│                                  │  50+ 集成     │ │
│                                  └──────────────┘ │
└──────────────────────────────────────────────────┘
```

整个系统分为四层：

1. **消息渠道层**：支持 12+ 聊天平台同时接入
2. **Gateway 网关层**：通过 WebSocket 统一管理所有连接，是整个系统的"中枢神经"
3. **AI 推理层**：支持 Anthropic Claude、OpenAI、本地模型等多种大脑
4. **工具执行层**：浏览器控制（CDP 协议）、文件操作、Shell 命令、定时任务、Webhook 等

### 2.2 关键技术细节

**Gateway 网关**：运行在 `ws://127.0.0.1:18789`，是所有客户端、工具和事件系统的连接中心。这个设计让 Moltbot 不仅仅是一个聊天机器人，而是一个可扩展的 Agent 平台。

**持久化记忆**：你的偏好、对话历史、项目上下文都以文件形式存储在本地（`~/.clawdbot/` 目录下）。不像 ChatGPT 那样每天重置，它会记住你上周随口提到的事情。

**Canvas 画布**：内置 A2UI（Agent-driven Visual Workspace），AI 可以在可视化画布上操作，支持更复杂的交互场景。

**语音能力**：支持语音唤醒和对话模式（Voice Wake & Talk），集成了 ElevenLabs，在 macOS/iOS/Android 上实现 "always-on speech"。

**技能系统**：支持 50+ 集成（Spotify、Obsidian、Gmail、GitHub 等），社区可以贡献自定义技能，AI 甚至可以自己编写新技能来扩展自身能力。

### 2.3 技术栈

| 项目 | 技术选型 |
|------|---------|
| 语言 | TypeScript |
| 包管理 | pnpm |
| 运行时 | Node.js ≥ 22 |
| 浏览器控制 | Chrome DevTools Protocol (CDP) |
| 通信协议 | WebSocket |
| 发布渠道 | stable / beta / dev 三轨制 |

---

## 三、改名风波：从 Clawdbot 到 Moltbot

### 3.1 事件经过

2026 年 1 月 27 日，项目创始人 Peter Steinberger 宣布：

> "Anthropic 要求我们更改名称（商标相关），说实话？'Molt' 完美契合——这正是龙虾成长的方式。"

"Molt" 在英文中是"蜕壳"的意思。龙虾要长大，必须脱掉旧壳，换上新壳。这个名字既保留了龙虾 🦞 吉祥物的精神，又暗示了项目在"蜕变升级"。

改名原因很直接：**Clawd 和 Claude 太像了**，容易让人误以为这是 Anthropic 的官方产品。

### 3.2 改名引发的加密货币骗局

但改名过程中出了一个大乱子。

Steinberger 在重命名 GitHub 组织和 X（Twitter）账号时，**释放旧账号和注册新账号之间出现了一个短暂的时间窗口**。加密货币骗子敏锐地抓住了这个机会：

1. **劫持旧账号**：骗子立刻抢注了被释放的 GitHub 组织名和 X 账号
2. **发行假代币**：利用劫持的"官方"账号推广一个名叫 CLAWD 的假代币
3. **疯狂炒作**：代币市值在数小时内被炒到 **1600 万美元**
4. **崩盘收割**：随后暴跌 90%，大量投资者血本无归

Peter Steinberger 紧急发声明：**他从未发行过任何代币，也没有任何计划这样做。** 任何声称与项目有关的加密货币都是骗局。

这个事件给所有开源项目敲了警钟：**改名是个高风险操作**，尤其是在项目知名度很高的时候。

---

## 四、安全！安全！安全！

这是本文最重要的部分。如果你只看一节，就看这节。

### 4.1 核心问题：AI 有了"手"之后

传统的 AI 聊天工具最多只是给你错误的建议，你可以选择不采纳。但 Moltbot 不同——**它可以直接操作你的电脑**。

这意味着：如果有人能控制你的 Moltbot，他们就相当于能控制你的电脑。

### 4.2 已发现的安全隐患

安全研究人员已经揭示了多个严重问题：

**隐患一：明文存储凭证**

Moltbot 将 API Key、OAuth 令牌等敏感信息以明文形式存储在 `~/.clawdbot/` 目录下。一旦你的电脑被入侵，这些凭证就会被直接读取。

**隐患二：反向代理认证绕过**

Moltbot 的认证系统默认信任来自 `localhost` 的连接。问题在于，很多人会在反向代理（如 Nginx）后面运行 Moltbot。此时**所有外部连接看起来都来自 127.0.0.1**，认证形同虚设。

安全研究员 @fmdz387 发现，大量 VPS 上的 Moltbot 实例暴露端口且无认证——这等于把自己的电脑"裸奔"在互联网上。

**隐患三：提示注入攻击**

安全研究员 Matvey Kukuy 做了一个演示：

1. 给一个 Moltbot 用户发送一封精心构造的邮件
2. 邮件内容包含隐藏的"指令"（提示注入）
3. 当 Moltbot 读取邮件时，AI 把恶意指令当成了合法操作
4. Moltbot 自动将用户最近 5 封邮件转发到攻击者的邮箱

**整个过程只需 5 分钟，用户完全不知情。**

**隐患四：信息窃取恶意软件**

安全公司 Hudson Rock 警告：像 RedLine、Lumma 这样的信息窃取恶意软件，很快就会开始专门针对 Moltbot 本地存储中的敏感数据。

**隐患五：假冒 VSCode 扩展**

Aikido 研究人员发现了一个伪装成 Clawdbot 的恶意 VSCode 扩展，安装后会在开发者机器上植入远程访问木马。

### 4.3 安全部署指南

如果你决定使用 Moltbot，请**务必**做到以下几点：

| 安全措施 | 说明 |
|---------|------|
| **不要以 root 运行** | 创建专用的低权限用户来运行 Moltbot |
| **不要裸奔端口** | 如果部署在 VPS 上，必须配置防火墙和认证 |
| **限制文件访问** | 只授予 Moltbot 访问特定文件夹的权限 |
| **从只读开始** | 先给只读权限，确认安全后再逐步开放写权限 |
| **使用 Docker 沙箱** | 在 Docker 容器中运行，限制工具访问范围 |
| **定期检查凭证** | 监控 `~/.clawdbot/` 目录下的敏感文件 |
| **注意提示注入** | 推荐使用 Claude Opus 4.5，其提示注入防护更强 |

正如苏打白在原帖中强调的：**"裸奔必死，请勿在无防护情况下暴露端口！"**

---

## 五、社区生态与资源

### 5.1 中文社区

@lyc_zh（YC 老师）建立了官方认可的最大中文社区，有问题可以进去交流。在 Moltbot 这样快速迭代的项目中，社区是最有价值的资源——因为官方文档永远跟不上变化速度。

### 5.2 高质量学习资源

| 类型 | 推荐资源 | 说明 |
|------|---------|------|
| 概念理解 | [@dotey 宝玉老师](https://x.com/dotey/status/2015335057741996521) | 深度解析 Moltbot 是什么，强烈推荐先看 |
| 概念扫盲 | [@binghe 冰河老师](https://x.com/binghe/status/2015288620387910016) | 文字版详解，120 万+阅读量 |
| 安装教程 | [@MiniMax_AI 官方教程](https://x.com/MiniMax_AI/status/2014380057301811685) | 官方出品的搭建指引 |
| 视频教程 | [@lxfater 铁锤老师](https://x.com/lxfater/status/2016020368524521812) | 完整入门视频 |
| 避坑指南 | [@mike_chong_zh 迈克老师](https://x.com/mike_chong_zh/status/2015633096373346557) | 几十小时踩坑总结 |
| VPS 部署 | [@discountifu 教程](https://x.com/discountifu/status/2016135549787226605) | 不用 Mac Mini 的替代方案 |
| 飞书接入 | [@akokoi1 开源方案](https://x.com/akokoi1/status/2016420074203287825) | 国内办公场景适配 |
| 安全警告 | [@servasyy_ai 黄老师](https://x.com/servasyy_ai/status/2015677935039213876) | 安全隐患深度解析 |

### 5.3 平替方案

如果你觉得 Moltbot 的风险太高，或者不想折腾，@YukerX 演示了[用 Claude Code 实现类似体验](https://x.com/YukerX/status/2015649479387722160)。虽然功能没那么强大，但胜在简单安全。

---

## 六、2026 年 2 月最新动态

本文初版写于 2026 年 1 月底。仅仅一个月后，OpenClaw/Moltbot 生态又发生了几件大事，这里做个集中更新。

### 6.1 创始人加入 OpenAI，项目转社区维护

2026 年 2 月 15 日，Peter Steinberger 宣布**加入 OpenAI**，OpenClaw 转为基金会维护的社区项目。这意味着 OpenClaw 不再是一个人的作品，而是正式进入社区化运营阶段。对用户来说，项目不会消失，但发展方向可能出现变化。

### 6.2 星标突破 18 万，成为 2026 年增长最快开源项目

截至 2026 年 2 月底，OpenClaw 在 GitHub 上的星标数已从 1 月底的 8 万飙升至 **18.6 万**，Fork 数超过 3.2 万，核心贡献者 130+，Discord 社区在线超 1.1 万人。[ClawHub 技能市场](https://clawdhub.com)已收录 **1700+** 技能插件。

### 6.3 Meta 等企业禁用 OpenClaw

与火爆形成鲜明对比的是，[Meta 等大型科技公司开始禁止员工在公司设备上使用 OpenClaw](https://www.resultsense.com/news/2026-02-20-openclaw-security-fears-lead-meta-and-other-firms-to-restrict-use)。SecurityScorecard 的报告显示，互联网上有超过 **13.5 万个暴露的 OpenClaw 实例**，其中 63% 存在安全漏洞。这进一步印证了本文第四章的安全警告——**部署不当，后果严重**。

### 6.4 Moltbook：150 万 AI Agent 的社交网络

最有趣的发展是 [Moltbook](https://www.techbrew.com/stories/2026/02/02/moltbook-ai-agent-social-network)——一个专为 AI Agent 设计的社交网络。由 Octane AI 联合创始人 Matt Schlicht 的 OpenClaw Agent（名叫 Clawd Clawderberg）自主创建，上线不到一个月就吸引了超过 **150 万 AI Agent** 入驻。这可能是 AI Agent 互操作的早期雏形。

### 6.5 版本快速迭代

| 版本 | 日期 | 关键更新 |
|------|------|---------|
| v2026.2.1 | 2月初 | 安全强化、系统提示升级、UI 优化 |
| v2026.2.17 | 2月17日 | 集成 Sonnet 4.6 模型、1M 上下文、子代理生成、iOS 分享扩展 |
| v2026.2.19 | 2月19日 | **Apple Watch MVP**、网关认证重构、40+ 安全修复 |

---

## 七、冷静思考：这事儿到底意味着什么？

### 7.1 它是"iPhone 时刻"吗？

有人说 Moltbot 是"个人 AI 的 iPhone 时刻"，也有人说它是"AGI 的早期体验"。但如果你冷静看，它更像是**一个方向的验证**——个人 AI Agent 的方向是对的，但现在的实现还很粗糙。

MacStories 称它为"个人 AI 助手的未来"。Andrej Karpathy 公开点赞。投资人 Chamath Palihapitiya 分享说 Moltbot 帮他"几分钟内省了 15% 的汽车保险费"。

但热度不等于成熟度。

### 7.2 真正的价值

Moltbot 最大的贡献不是技术本身，而是**打开了大众对"个人 AI Agent"的想象力**：

- AI 不应该只是回答问题的工具
- AI 应该能主动为你工作
- AI 应该 24 小时在线，随叫随到
- AI 应该记住你的一切偏好

这些理念，之前只在技术圈讨论。Moltbot 把它变成了一个普通人可以体验的东西。

### 7.3 需要警惕的问题

但我们也要清醒地看到：

1. **安全问题远未解决**：一个能操作你电脑的 AI，安全门槛极高。22% 的企业组织中已发现员工在非授权情况下使用 Moltbot
2. **开源不等于安全**：代码开源只意味着可以被审计，不意味着已经安全
3. **明文存储凭证**是不可接受的设计缺陷
4. **"自主 Agent"的哲学问题**：你真的信任 AI 自主替你做决策吗？从只读权限开始，而非上来就给完整系统访问

### 7.4 理性建议

苏打白在原帖开头说了一句话，我觉得非常中肯：

> "不想折腾？跳过也没事，你不会因此错过一个亿，也不用焦虑，把它当个新资讯听听就好。"

如果你是技术爱好者，可以尝试部署一下，但请**务必做好安全防护**。如果你不是技术背景，建议**先观望**，等产品更成熟、安全问题解决得更好之后再上手。

工具只是手段，不是目的。

---

## 总结

Moltbot（原 Clawdbot）在短短一周内从默默无闻到 8 万 Star，再到被迫改名、遭遇加密骗局，经历了一个开源项目能遇到的几乎所有戏剧性事件。

它验证了一个重要方向：**个人 AI Agent 的时代正在到来。** 但同时也暴露了这个方向面临的核心挑战——安全、信任和权限边界。

如果你对这个领域感兴趣，可以从了解 Moltbot 的架构开始，思考 AI Agent 的未来走向。如果你只是好奇，那现在你已经知道了它是什么、为什么火、以及需要注意什么——这就够了。

龙虾蜕壳之后会长大。这个项目也一样，期待它变得更成熟、更安全。

---

## 相关阅读

- [ClawdBot：海外爆火的个人 AI 管家，30 分钟搭建指南](/zh/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/) - 新手友好的搭建教程
- [Claude Code 完全指南：终端里的全能 AI 助手](/zh/posts/ai/2026-01-14-claude-code-guide/) - 程序员专属的 AI 编程助手
- [Agent Skills：AI 编程的新范式](/zh/posts/ai/2026-01-19-agent-skills-new-programming/) - 理解 AI Agent 的技能系统
- [AI 开发工作流的变革](/zh/posts/ai/2026-01-19-ai-dev-workflow/) - AI Agent 如何改变我们的工作方式
- [AGI 已经来了？Anthropic CEO 的深度分析](/zh/posts/ai/2026-01-26-agi-is-here/) - AI 发展的宏观趋势

---

## 参考资源

- [Moltbot 官网](https://molt.bot)（原 clawd.bot）
- [Moltbot GitHub](https://github.com/moltbot/moltbot)（⭐ 186,000+ Star）
- [Moltbot 官方文档](https://docs.molt.bot)
- [Moltbot Discord 社区](https://discord.com/invite/clawd)
- [ClawdHub 技能市场](https://clawdhub.com)
- [TechCrunch 深度报道](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/)
- [苏打白原帖](https://x.com/sodawhite_dev/status/2016486967932817705)

---

## 常见问题（FAQ）

### Moltbot 是什么？

Moltbot 是一个开源的个人 AI Agent 项目，由 Peter Steinberger 创建。它可以 24 小时运行在你的电脑或服务器上，通过 Telegram、WhatsApp、iMessage 等聊天工具接收你的指令，自主操作浏览器、处理邮件、管理文件、执行 Shell 命令等。简单理解就是：**一个真正能帮你干活的 AI 助手，而不是只会聊天的 AI**。它支持 Claude、GPT 等多种大模型作为"大脑"，并拥有 50+ 技能集成。

### Moltbot 为什么改名？

Moltbot 最初叫 **Clawdbot**，因为 "Clawd" 与 Anthropic 的产品 "Claude" 发音和拼写过于相似，Anthropic 出于商标保护要求项目更改名称。2026 年 1 月 27 日，创始人 Peter Steinberger 将项目改名为 Moltbot。"Molt" 是英文"蜕壳"的意思，寓意龙虾脱掉旧壳、长出新壳的成长过程，与项目的龙虾吉祥物完美呼应。

### Moltbot 和 OpenClaw 是什么关系？

Moltbot 和 OpenClaw 指的是**同一个项目在不同阶段的名称**。该项目最初叫 Clawdbot，因商标问题改名为 Moltbot，社区中又常被称为 OpenClaw。三个名字指向同一个开源 AI Agent 项目，只是称呼不同。在搜索资料时，用任意一个名字都能找到相关内容。

### Moltbot 安全吗？

**目前 Moltbot 存在多个已知安全隐患**，使用时需要格外谨慎。主要风险包括：明文存储 API Key 等敏感凭证、反向代理场景下认证可被绕过、容易遭受提示注入攻击等。安全研究员已演示过通过一封恶意邮件就能窃取用户数据的攻击路径。如果你决定使用，务必做到：不以 root 运行、不暴露端口、使用 Docker 沙箱、从只读权限开始。详细的安全部署建议请参考本文第四章。

### Moltbot 能做什么？

Moltbot 可以帮你完成各种实际工作任务，主要包括：**浏览器自动化**（自动打开网页、填表、提交）、**邮件处理**（读取、回复、转发邮件）、**日程管理**（创建、查询日历事件）、**文件操作**（读写、整理文件）、**Shell 命令执行**、**信息搜索和总结**等。通过 ClawHub 技能市场的 1700+ 插件，还能对接 Spotify、Obsidian、GitHub 等服务。简单来说，你能在电脑上做的事，Moltbot 基本都能帮你做。

### Moltbot 创始人 Peter Steinberger 是谁？

Peter Steinberger 是奥地利软件开发者，OpenClaw（原 Clawdbot/Moltbot）的创始人。他此前创立了 PSPDFKit（一家 PDF SDK 公司），在 iOS/macOS 开发社区颇有影响力。2026 年 2 月 15 日，Steinberger 宣布加入 OpenAI，OpenClaw 项目转为基金会维护的社区项目。

### Moltbot 现在有多少 Star？

截至 2026 年 2 月底，OpenClaw（Moltbot）在 GitHub 上已获得 **18.6 万+ Star**，Fork 数超过 3.2 万，是 2026 年增长最快的开源项目之一。ClawHub 技能市场收录了 1700+ 插件。

### Moltbot 和 Claude Code 有什么区别？

两者的定位不同。**Claude Code** 是 Anthropic 官方推出的终端 AI 编程助手，专注于代码开发场景，在终端中使用。**Moltbot** 则是一个通用的个人 AI Agent，覆盖生活和工作的各种场景（邮件、日程、浏览器操作、文件管理等），通过聊天工具远程控制。如果你只需要编程辅助，Claude Code 更简单安全；如果你想要一个全能的 AI 管家，可以考虑 Moltbot，但需要做好安全防护。

## 相关阅读 / Related

- [AI 自动化导航 Hub](/zh/posts/ai/ai-automation-hub/)
- [Clawdbot：个人 AI 助手实战](/zh/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/)
- [OpenClaw 自动化的坑与避坑](/zh/posts/ai/2026-02-14-openclaw-automation-pitfalls/)
- [OpenClaw 超详细上手教程](/zh/posts/ai/2026-02-12-openclaw-usage-tutorial/)
- [OpenClaw 与 OpenAI 关系深度分析](/zh/posts/ai/2026-02-16-openclaw-openai-analysis/)
- [Moltbot 是什么？3 分钟看懂](/zh/posts/ai/2026-02-18-what-is-moltbot/)
