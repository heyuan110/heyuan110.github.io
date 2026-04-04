+++
date = '2026-04-02T14:00:00+08:00'
draft = false
title = 'OpenClaw 多 Agent 配置完全指南：从单兵到团队协作的实操教程'
description = '手把手教你配置 OpenClaw 多 Agent 系统。涵盖 Agent 创建、工作区隔离、绑定路由、sessions_send 通信、飞书集成，以及四种生产级协作模式的完整配置示例。'
toc = true
tags = ['OpenClaw', 'Multi-Agent', 'AI Architecture', 'Feishu', 'Agent Orchestration']
keywords = ['OpenClaw 多Agent配置', 'openclaw 多agent教程', 'openclaw 飞书集成', 'openclaw bindings配置', 'sessions_send', 'openclaw.json配置', '多agent协作模式', 'openclaw agents add']

[[params.faqItems]]
question = "OpenClaw 多 Agent 怎么配置？"
answer = "用 'openclaw agents add <名称>' 逐个创建 Agent，每个 Agent 会获得独立的工作区（SOUL.md、AGENTS.md、记忆等），存储在 ~/.openclaw/agents/<agentId>/ 下。然后在 openclaw.json 的 bindings 中配置消息路由规则，指定哪个频道/群组的消息交给哪个 Agent 处理。"

[[params.faqItems]]
question = "OpenClaw bindings 路由规则的优先级是什么？"
answer = "bindings 采用「最精确匹配优先」策略：精确的 peer（聊天/群组 ID）匹配优先级最高，其次是频道+账号匹配，再次是频道级默认，最后是标记了 default: true 的兜底 Agent。同一优先级下，配置中靠前的规则胜出。"

[[params.faqItems]]
question = "sessions_send 是什么？怎么配置 Agent 之间的通信？"
answer = "sessions_send 是 OpenClaw 内置的 Agent 间通信工具。在 openclaw.json 的 tools.agentToAgent 下配置，需要设置 enabled: true 和 allow 白名单。支持最多 5 轮乒乓对话（maxPingPongTurns），Agent 可以回复 REPLY_SKIP 提前结束。默认关闭，必须手动开启。"

[[params.faqItems]]
question = "OpenClaw 怎么接入飞书？"
answer = "OpenClaw 2026.2.26 起内置飞书 Channel，无需额外安装插件。在飞书开放平台创建机器人应用，获取 appId 和 appSecret，配置到 openclaw.json 的 channels.feishu 中。飞书使用 WebSocket 事件订阅，不需要公网地址。多 Agent 路由在 2026.3.13 版本后完全支持。"

[[params.faqItems]]
question = "应该用哪种多 Agent 协作模式？"
answer = "从 Supervisor 模式起步：一个协调者 Agent 接收所有请求，通过 sessions_send 分发给专家 Agent。覆盖 80% 场景。当 Supervisor 成为瓶颈时再升级到 Router（按频道直接路由）、Pipeline（串行流水线）或 Parallel（并行拆分）模式。"
+++

![OpenClaw 多 Agent 配置指南：架构、路由与协作模式](cover.webp)

你的 OpenClaw 用了两周，越来越不对劲——问它写文章，它突然蹦出上周的代码调试记录；让它查竞品，它把写作群里的聊天记忆混进来。响应也越来越慢，记忆索引膨胀到了 200MB。

这不是模型变笨了，是架构问题：**一个 Agent 扛不住无限多的上下文领域**。解法不是换更大的模型，而是拆——多个专精 Agent，各管各的工作区、记忆和模型。

这篇教程手把手带你完成 OpenClaw 多 Agent 的完整配置。如果你还没装过 OpenClaw，先看 [OpenClaw 安装配置指南](/posts/ai/2026-03-05-openclaw-setup-guide/)。

---

## 为什么要多 Agent？单 Agent 的天花板

一个 Agent 跑得久了，三个问题一定会出现：

1. **记忆污染**——Agent 在回答问题时，会从无关领域拉取记忆。问博客草稿的事，它把上周的 debug 笔记也搜出来了
2. **人设冲突**——一个 SOUL.md 里同时写「严谨的技术写手」和「随意的朋友」，两种人格必然互相泄漏
3. **模型不匹配**——写代码需要 Claude Sonnet，头脑风暴用 GLM-4.7 效果更好，一个 Agent 只能配一个模型

多 Agent 架构把这三个问题全解决了。每个 Agent 独立的工作区、记忆、人设、模型配置。底层原理参考 [OpenClaw 架构深度解析](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/)。

---

## 核心概念：一个 Agent 由什么组成

在 OpenClaw 里，每个 Agent 是三样东西的组合：

| 组件 | 路径 | 作用 |
|------|------|------|
| **工作区** | `~/openclaw-agents/<名称>/` | SOUL.md、AGENTS.md、USER.md、TOOLS.md、MEMORY.md |
| **Agent 目录** | `~/.openclaw/agents/<agentId>/` | 认证配置、模型注册、Agent 专属设置 |
| **会话存储** | `~/.openclaw/agents/<agentId>/sessions/` | 聊天记录、路由状态 |

**铁律**：永远不要让两个 Agent 共享 Agent 目录。共享会导致认证冲突、会话串台、记忆交叉污染。

---

## 第一步：创建 Agent 工作区

### 用 CLI 创建 Agent

```bash
# 创建协调者 Agent（团队管理者）
openclaw agents add supervisor

# 创建专家 Agent
openclaw agents add writer
openclaw agents add coder
openclaw agents add researcher
```

每条命令会自动生成一个工作区目录，包含模板文件：

```
~/openclaw-agents/writer/
├── AGENTS.md      # Agent 能力和规则
├── SOUL.md        # 人设、语气、价值观
├── USER.md        # 用户偏好和上下文
├── TOOLS.md       # 可用工具和限制
├── MEMORY.md      # 持久记忆笔记
├── HEARTBEAT.md   # 主动巡检规则
└── IDENTITY.md    # 名称、头像、元数据
```

### 命名规则

- 只允许小写字母、数字和连字符（`a-z`、`0-9`、`-`）
- 必须以字母开头
- 不能以连字符结尾
- 示例：`writer`、`code-reviewer`、`research-v2`

### 为每个 Agent 定制 SOUL.md

每个 Agent 必须有独立的 SOUL.md。以下是写手 Agent 的示例：

```markdown
# 写手 Agent

你是一名专注于 AI 工程领域的技术内容写作者。

## 规则
- 使用清晰直接的语言
- 用具体案例代替抽象解释
- 每篇文章 1500-2500 字
- 适当加入代码片段
- 禁止生成占位内容——每个章节都必须有实质内容

## 语气
专业但不端着。不说废话，不用套话。

## 可用工具
- tavily-search（网络搜索）
- memory_search（回忆历史文章）
- read/write（文件读写）

## 禁用工具
- exec（不许执行命令）
- browser（不许操作浏览器）
```

---

## 第二步：为每个 Agent 配置不同模型

不同 Agent 用不同模型，发挥各自优势：

```bash
# Supervisor：快速便宜，只做路由决策
openclaw agents config set supervisor model claude-3.5-haiku

# 写手：强推理，长文生成
openclaw agents config set writer model deepseek-r1

# 程序员：最强代码模型
openclaw agents config set coder model claude-sonnet-4

# 研究员：工具调用和信息综合能力强
openclaw agents config set researcher model gpt-4.1
```

### 模型选择策略

| Agent 类型 | 推荐模型 | 理由 |
|-----------|----------|------|
| Supervisor | Claude Haiku / GPT-4.1-mini | 路由决策快、成本低 |
| 写手 | DeepSeek-R1 / Claude Sonnet | 长文生成能力强 |
| 程序员 | Claude Sonnet / Codex | 代码质量最好 |
| 研究员 | GPT-4.1 / Claude Sonnet | 工具调用和综合分析能力强 |
| 创意 | GLM-4.7 / DeepSeek | 发散思维，创意好 |

关键洞察：**Supervisor 不需要最贵的模型**。它只做分发决策，把昂贵的 API 调用留给干活的专家 Agent。

---

## 第三步：配置 Bindings（消息路由）

Bindings 是 openclaw.json 中的确定性路由规则，决定哪条消息交给哪个 Agent。

### 完整配置示例

```json
{
  "agents": {
    "list": [
      {
        "id": "supervisor",
        "workspace": "~/openclaw-agents/supervisor",
        "default": true
      },
      {
        "id": "writer",
        "workspace": "~/openclaw-agents/writer"
      },
      {
        "id": "coder",
        "workspace": "~/openclaw-agents/coder"
      },
      {
        "id": "researcher",
        "workspace": "~/openclaw-agents/researcher"
      }
    ]
  },
  "bindings": [
    {
      "channel": "telegram",
      "peer": "writing_group_id",
      "agent": "writer"
    },
    {
      "channel": "telegram",
      "peer": "coding_group_id",
      "agent": "coder"
    },
    {
      "channel": "feishu",
      "account": "work-bot",
      "agent": "supervisor"
    },
    {
      "channel": "feishu",
      "account": "writing-bot",
      "agent": "writer"
    },
    {
      "channel": "telegram",
      "agent": "supervisor"
    }
  ]
}
```

### Binding 优先级（最精确匹配优先）

1. **精确 peer 匹配**（最高）——特定群组/聊天 ID → 特定 Agent
2. **频道+账号匹配**——某个频道的某个账号
3. **频道级默认**——该频道类型的所有消息
4. **兜底默认**——标记了 `"default": true` 的 Agent（或列表中第一个）

同一优先级下，**配置中靠前的规则胜出**。

### 验证路由配置

配好之后一定要验证：

```bash
# 查看所有活跃的 bindings
openclaw gateway --bindings

# 探测特定频道的路由情况
openclaw gateway --probe telegram

# 探测飞书频道
openclaw gateway --probe feishu
```

---

## 第四步：配置 Agent 间通信（sessions_send）

如果你需要 Agent 之间互相交流（不是被动接收路由消息，而是主动发消息给另一个 Agent），就需要配置 `sessions_send`。

### 开启 Agent 间通信

在 `openclaw.json` 中添加：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["supervisor", "writer", "coder", "researcher"],
      "maxPingPongTurns": 3
    }
  }
}
```

### sessions_send 工作流程

用一个实际场景说明：

1. 用户对 **Supervisor** 说：「帮我写一篇 OpenClaw 安全配置的文章」
2. **Supervisor** 调用 `sessions_send` 发给 **Researcher**：「查找最新的 OpenClaw 安全功能和漏洞」
3. **Researcher** 完成调研，回复结果
4. **Supervisor** 调用 `sessions_send` 发给 **Writer**：「基于以下调研写一篇 2000 字的文章：[调研结果]」
5. **Writer** 写完文章，回复
6. **Supervisor** 汇总结果，交付给用户

### 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | `false` | 总开关，默认关闭 |
| `allow` | `[]` | 允许通信的 Agent ID 白名单 |
| `maxPingPongTurns` | `5` | 最大乒乓对话轮数（0-5） |

### 防递归规则（重要！）

必须在 Supervisor 的 SOUL.md 中写明防递归规则：

```markdown
## 协调规则
- 绝对不接受专家 Agent 回传的任务
- 收到专家的输出后，只做汇总和收尾，不再二次分发
- 如果专家完不成任务，直接向用户报告失败，不要换个说法重试
```

不加这条规则，很容易出现循环委派，快速烧掉大量 token。

---

## 第五步：Agent 级沙箱和工具权限

每个 Agent 只给它需要的工具。权限过多会带来安全风险，也会让模型在过多工具选项中迷失。

```json
{
  "agents": {
    "list": [
      {
        "id": "writer",
        "workspace": "~/openclaw-agents/writer",
        "sandbox": {
          "enabled": true,
          "allowedPaths": ["~/writing/", "~/drafts/"]
        },
        "tools": {
          "allow": ["tavily-search", "memory_search", "read", "write"],
          "deny": ["exec", "browser", "shell"]
        }
      },
      {
        "id": "coder",
        "workspace": "~/openclaw-agents/coder",
        "sandbox": {
          "enabled": true,
          "allowedPaths": ["~/projects/"]
        },
        "tools": {
          "allow": ["exec", "read", "write", "browser", "memory_search"],
          "deny": ["tavily-search"]
        }
      }
    ]
  }
}
```

### 沙箱配置建议

| Agent 类型 | 文件权限 | 工具权限 | 说明 |
|-----------|----------|----------|------|
| 写手 | 只读写内容目录 | 搜索+读写 | 禁止执行命令 |
| 程序员 | 项目目录 | 全部开发工具 | 限制目录范围 |
| 研究员 | 无文件写权限 | 仅搜索工具 | 只读不写 |
| 家庭/共享 | 只读沙箱 | 仅回答问题 | 不能修改任何东西 |

更多工具权限配置技巧，参考 [OpenClaw 自动化避坑指南](/posts/ai/2026-03-05-openclaw-automation-pitfalls/)。

---

## 飞书集成：企业级多 Agent 部署

飞书是国内企业用得最多的办公平台，OpenClaw 从 2026.2.26 起原生支持飞书 Channel，2026.3.13 起完整支持多 Agent 路由。

### 架构：一个机器人对应一个 Agent

推荐做法：在飞书开放平台创建多个机器人应用，每个机器人绑定一个 OpenClaw Agent。

#### 第一步：创建飞书机器人

1. 打开 [飞书开放平台](https://open.feishu.cn/app) → 创建企业自建应用
2. 为每个 Agent 创建一个机器人：
   - `工作助手`（绑定 supervisor）
   - `写作助手`（绑定 writer）
   - `代码助手`（绑定 coder）
3. 获取每个机器人的 `App ID` 和 `App Secret`

#### 第二步：配置权限（Scopes）

每个机器人至少需要这些权限：

| 权限 | 说明 |
|------|------|
| `im:message` | 收发消息 |
| `im:message.group_at_msg` | 接收群内 @消息 |
| `contact:user.base:readonly` | 读取用户信息 |

根据 Agent 需要，额外添加：
- `docs:doc` — 读写飞书文档
- `calendar:calendar` — 日历操作
- `task:task` — 任务管理
- `bitable:app` — 多维表格操作

#### 第三步：配置 openclaw.json

```json
{
  "channels": {
    "feishu": [
      {
        "account": "work-bot",
        "appId": "cli_xxx_work",
        "appSecret": "your_work_secret"
      },
      {
        "account": "writing-bot",
        "appId": "cli_xxx_write",
        "appSecret": "your_write_secret"
      },
      {
        "account": "code-bot",
        "appId": "cli_xxx_code",
        "appSecret": "your_code_secret"
      }
    ]
  },
  "bindings": [
    {
      "channel": "feishu",
      "account": "work-bot",
      "agent": "supervisor"
    },
    {
      "channel": "feishu",
      "account": "writing-bot",
      "agent": "writer"
    },
    {
      "channel": "feishu",
      "account": "code-bot",
      "agent": "coder"
    }
  ]
}
```

#### 第四步：启动并验证

```bash
# 重启 Gateway
openclaw gateway restart

# 验证飞书连接状态
openclaw gateway --probe feishu

# 查看路由绑定
openclaw gateway --bindings
```

### 飞书特有优势

- **不需要公网地址**——飞书使用 WebSocket 事件订阅，OpenClaw 主动连接飞书服务器，不需要 ngrok 或公网 IP
- **实时状态反馈**——消息卡片中显示「思考中/生成中/完成」状态
- **丰富的企业能力**——Agent 可以直接操作飞书文档、日历、任务、多维表格、群消息
- **敏感操作确认**——关键操作会弹出确认按钮，用户确认后才执行

---

## 四种生产级协作模式

### 模式一：Supervisor（推荐起步）

```
用户 → Supervisor → Writer
                  → Coder
                  → Researcher
```

一个协调者 Agent 接收所有请求，根据任务类型分发给对应的专家 Agent，收集结果后统一回复用户。

**适用场景**：个人助手、小团队、混合领域任务。

**配置复杂度**：低——一个 Supervisor + 2-4 个专家。

**典型配置**：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["supervisor", "writer", "coder", "researcher"],
      "maxPingPongTurns": 3
    }
  }
}
```

### 模式二：Router（按频道直接路由）

```
Telegram 写作群 → Writer
Telegram 代码群 → Coder
飞书工作机器人   → Supervisor
WhatsApp 私人   → Personal Agent
```

通过 bindings 把不同频道/群组的消息直接路由到对应 Agent，不需要 Supervisor 中转。零额外 token 消耗。

**适用场景**：每个频道/群有明确用途的团队。

**配置复杂度**：低——只需 bindings，不需要 Agent 间通信。

### 模式三：Pipeline（串行流水线）

```
用户 → Researcher → Writer → Editor → 用户
```

每个 Agent 的输出作为下一个 Agent 的输入。研究 Agent 收集素材，写手 Agent 基于素材写文章，编辑 Agent 润色成稿。

**适用场景**：内容生产、代码审查链、数据处理流程。

**配置复杂度**：中——需要 `sessions_send` + 明确的交接协议。

### 模式四：Parallel（并行执行）

```
             → Researcher A（主题1）
用户 → Supervisor → Researcher B（主题2） → Supervisor → 用户
             → Researcher C（主题3）
```

Supervisor 把一个大任务拆成多个子任务，分发给多个 Agent 同时执行，汇总结果后交付。

**适用场景**：大规模调研、多文件代码生成、批量处理。

**配置复杂度**：高——需要仔细的结果聚合和错误处理。

### 选型参考

| 场景 | 推荐模式 | 原因 |
|------|----------|------|
| 个人全能助手 | Supervisor | 灵活路由，随时加专家 |
| 团队各群各司其职 | Router | 零开销，直接路由 |
| 博客内容生产 | Pipeline | 调研→写作→编辑 流水线 |
| 10 家竞品同时分析 | Parallel | 并行执行提速 |

---

## 成本控制

多 Agent 意味着 API 成本倍增——每次 `sessions_send` 都是独立的 API 调用。控制成本的五个方法：

1. **简单任务让 Supervisor 直接回答**——一句话能答完的不要委派给专家
2. **路由用便宜模型**——Supervisor 用 Haiku，贵的模型只给专家
3. **限制乒乓轮数**——`maxPingPongTurns` 设 2-3，不要用默认的 5
4. **合并相似 Agent**——如果两个 Agent 处理 80% 以上相同类型的任务，合并它们
5. **能用 Router 就不用 Supervisor**——基于频道的路由没有额外 token 开销

更多记忆优化策略，参考 [OpenClaw 记忆策略指南](/posts/ai/2026-01-31-openclaw-memory-strategy/)。

---

## 常见问题排查

### Agent 收不到消息

检查 binding 优先级。一个更宽泛的 binding 可能在你的精确规则之前截获了消息。用 `openclaw gateway --bindings` 查看实际路由顺序。

### sessions_send 静默失败

确认目标 Agent 在 `agentToAgent.allow` 白名单中。Agent 间通信默认关闭，必须手动开启。

### 记忆交叉污染

确保每个 Agent 有独立的 `agentDir`。用 `openclaw agents list` 检查每个 Agent 的路径是否唯一。共享目录是记忆串台的根源。

### Token 成本飙升

检查 Supervisor 是不是在用 Claude Sonnet 做每一次路由决策。换成 Haiku 或 GPT-4.1-mini，立刻降低 80% 的路由成本。

---

## 推荐起步配置

大多数个人用户，从这个 3 Agent 配置开始：

| Agent | 模型 | 角色 | 绑定频道 |
|-------|------|------|----------|
| supervisor | claude-3.5-haiku | 路由分发+简单问答 | 所有频道的默认 |
| writer | deepseek-r1 | 写文章、文档、邮件 | 写作专用群 |
| coder | claude-sonnet-4 | 写代码、调试、代码审查 | 代码专用群 |

当你发现 Supervisor 频繁需要做复杂的网络搜索时，加一个 researcher Agent。只有在确实有明确分工需求时才加更多专家——一个配置良好的 3 Agent 团队比配置混乱的 10 Agent 团队强得多。

OpenClaw 项目本身的开发方法论，可以看 [OpenClaw 创始人如何用 Claude Code 并行开发](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)。

---

## 延伸阅读

多 Agent 配置只是起点。配好之后继续探索：

- **[OpenClaw Tavily 集成指南](/posts/ai/2026-03-05-openclaw-tavily-integration/)**——给研究员 Agent 加上实时网络搜索
- **[OpenClaw 使用教程](/posts/ai/2026-02-12-openclaw-usage-tutorial/)**——从零开始的新手指南
- **[OpenClaw 安装配置指南](/posts/ai/2026-03-05-openclaw-setup-guide/)**——完整安装和基础配置
- **Lobster 工作流引擎**——用 YAML 编排确定性多 Agent 流水线（OpenClaw 2026.4 即将推出）
- **ACP（Agent Communication Protocol）**——把 IDE 桥接到 OpenClaw Agent 的编码工作流
