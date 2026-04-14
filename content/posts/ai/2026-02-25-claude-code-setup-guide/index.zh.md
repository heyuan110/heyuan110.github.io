+++
date = '2026-02-25T12:00:00+08:00'
draft = false
title = 'Claude Code 安装配置完全指南 2026：10 分钟从零上手'
description = 'Claude Code 2026 最新安装教程：终端一条命令安装、API Key 与 OAuth 登录、VS Code/JetBrains 集成、CLAUDE.md 配置、权限设置，附常见报错排查，10 分钟搞定。'
toc = true
tags = ['Claude Code', 'Setup', 'Tutorial', 'Getting Started']
categories = ['AI Guides']
keywords = ['Claude Code 安装', 'Claude Code 配置', 'Claude Code 教程', 'Claude Code 使用指南', 'Claude Code 入门', 'Claude Code VS Code', 'Claude Code 怎么用', 'Claude Code 安装失败']

[[params.faqItems]]
question = "Claude Code 怎么安装？需要 Node.js 吗？"
answer = "2026 年起不再需要 Node.js。macOS/Linux 一条命令就能装好：curl -fsSL https://claude.ai/install.sh | bash。Windows 用 PowerShell 执行 irm https://claude.ai/install.ps1 | iex。原生安装器会自动下载二进制到 ~/.local/bin/claude 并配置 PATH。"

[[params.faqItems]]
question = "Claude Code 安装后提示 command not found 怎么办？"
answer = "通常是 PATH 没配好。执行 echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.zshrc 后 source ~/.zshrc 即可（bash 用户换成 .bashrc）。也可以直接运行 claude doctor 诊断配置问题，它会提示所有缺失项。"

[[params.faqItems]]
question = "Claude Code 必须付费吗？可以用 API Key 吗？"
answer = "必须有 Pro/Max 订阅或 API Key。两种方式都能用：Pro（20 美元/月）订阅用户首次启动 claude 会自动 OAuth 登录；API 用户在 console.anthropic.com 拿到 Key，设置 ANTHROPIC_API_KEY 环境变量即可。企业用户还可以走 AWS Bedrock 或 GCP Vertex AI。"

[[params.faqItems]]
question = "Claude Code 在 VS Code 里怎么用？"
answer = "先在终端装好 Claude Code，然后在 VS Code 扩展面板搜索「Claude Code」安装官方扩展（Cursor/Windsurf 同样适用）。装好后支持内联编辑、Diff 预览、检查点回滚、多会话和 @filename 文件引用。JetBrains 系列（IntelliJ/PyCharm/WebStorm）也有原生插件。"

[[params.faqItems]]
question = "Claude Code 默认用什么模型？该怎么选？"
answer = "默认是 Sonnet 4.6，日常 80% 任务都够用。用 /model opus 切到 Opus 4.6（成本 1.67x）做复杂重构和架构设计；简单提问用 /model haiku（0.33x）省钱。不建议所有任务都上 Opus——用量会被快速吃光。"
+++

![Claude Code 安装配置指南：终端安装与 IDE 集成](cover.webp)

你一定听说过 Claude Code，也许还看过各种炫酷的演示视频。现在，是时候亲自上手体验了。

好消息是：从零开始到完成安装配置，整个过程大约只需要 10 分钟。这篇指南会带你走完全部流程——安装、认证、配置、IDE 集成，以及运行你的第一个实战任务。

读完这篇文章，你将拥有一个在终端和 IDE 中都能正常运行的 Claude Code 环境，并做好开始 AI 编程的一切准备。

## 前置条件

在开始之前，确认以下环境已就绪：

- **操作系统**：macOS 13+、Ubuntu 20.04+ / Debian 10+，或 Windows 10+（需要 Git Bash 或 WSL 2）
- **内存**：至少 4 GB
- **网络连接**：必须联网（Claude Code 依赖 Anthropic 的 API 服务）
- **Anthropic 账号**：如果还没有，可以在 [claude.ai](https://claude.ai) 注册
- **付费计划或 API 密钥**：Claude Code 需要 Pro/Max 订阅（$20+/月）或一个有余额的 API 密钥。详细的方案对比可以参考我们的 [Claude Code 定价指南](/posts/ai/2026-02-25-claude-code-pricing/)。

> Node.js **不再需要了**。2026 版的原生安装器会搞定一切。如果你之前是通过 npm 安装的，可以迁移到新方式——下面会讲到。

## 第一步：安装 Claude Code

### macOS / Linux（推荐方式）

打开终端，运行一条命令就行：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

完事。安装器会把二进制文件下载到 `~/.local/bin/claude`，并自动添加到你的 PATH 中。

想要体验最新的前沿功能而非稳定版？

```bash
curl -fsSL https://claude.ai/install.sh | bash -s latest
```

### Windows

**PowerShell：**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**命令提示符：**
```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**WSL 2**（推荐给想要完整 Linux 体验的 Windows 用户）：
```bash
# 在 WSL 2 终端中运行
curl -fsSL https://claude.ai/install.sh | bash
```

### 验证安装

```bash
claude --version
```

看到版本号就说明成功了。如果提示 "command not found"，手动把 `~/.local/bin` 加到 PATH：

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

（如果你用的是 Bash，把 `.zshrc` 换成 `.bashrc`。）

### 从 npm 安装迁移

如果你之前通过 `npm install -g @anthropic-ai/claude-code` 安装过，迁移到原生安装器很简单：

```bash
claude install
```

npm 安装方式已经废弃了。原生安装器更快、支持自动更新，而且不需要 Node.js。

### 运行健康检查

```bash
claude doctor
```

这个命令会诊断常见问题——缺失的依赖、PATH 配置、认证状态等等。觉得哪里不对劲的时候就跑一下。

## 第二步：完成认证

Claude Code 需要验证你的身份。有三种认证方式：

### 方式 A：Anthropic 账号（Pro/Max 订阅用户）

如果你有 Pro（$20/月）或 Max（$100–200/月）订阅，这是最简单的方式：

```bash
claude
```

首次启动时，Claude Code 会自动打开浏览器完成 OAuth 认证。授权连接后就可以直接用了，不需要管理任何 API 密钥。

### 方式 B：API 密钥（按量付费）

如果你更喜欢按 Token 付费，或者没有订阅：

1. 从 [console.anthropic.com](https://console.anthropic.com) 获取 API 密钥
2. 设置环境变量：

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

要持久化的话，写入 `~/.zshrc` 或 `~/.bashrc`：

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
```

### 方式 C：云服务商（企业用户）

通过 AWS 或 GCP 接入的企业用户：

**Amazon Bedrock：**
```bash
export CLAUDE_CODE_USE_BEDROCK=1
# 按常规方式配置 AWS 凭证（aws configure、IAM 角色等）
```

**Google Vertex AI：**
```bash
export CLAUDE_CODE_USE_VERTEX=1
# 配置 GCP 凭证（gcloud auth、服务账号等）
```

两种方式都支持 LLM 网关代理，适配企业网络环境。

## 第三步：选择模型

Claude Code 默认使用 **Sonnet 4.6**——在速度、能力和成本之间取得了最佳平衡，非常适合日常编程。当然你也有其他选择。

进入 Claude Code 后，用 `/model` 命令切换模型：

| 命令 | 模型 | 适用场景 | 相对成本 |
|------|------|---------|---------|
| `/model sonnet` | Sonnet 4.6 | 日常编程（默认） | 1x |
| `/model opus` | Opus 4.6 | 复杂架构、多步推理 | 1.67x |
| `/model haiku` | Haiku 4.5 | 快速提问、简单任务 | 0.33x |

**我的建议**：80% 的工作用 Sonnet 就够了。碰到复杂的多文件重构、系统设计或特别棘手的 Bug 时，切到 Opus。简单查询和快速提问用 Haiku。

## 第四步：配置 CLAUDE.md

这是提升 Claude Code 效果最立竿见影的一件事。[CLAUDE.md 文件](/posts/ai/2026-01-12-claudemd-memory-guide/) 是放在项目根目录的一个 Markdown 文档，它告诉 Claude Code 关于你项目的一切必要信息。

现在就创建一个：

```bash
touch CLAUDE.md
```

这里给一个不错的起步模板：

````markdown
# 项目说明

## 概述
[简要描述这个项目是做什么的]

## 技术栈
- 语言：[例如 TypeScript、Python、Go]
- 框架：[例如 Next.js 15、FastAPI、Gin]
- 数据库：[例如 PostgreSQL、MongoDB]
- 测试：[例如 Jest、pytest、go test]

## 代码规范
- [例如：使用函数组件 + Hooks，不使用类组件]
- [例如：所有函数必须有类型注解]
- [例如：测试文件放在源文件旁边的 __tests__/ 目录中]

## 常用命令
```bash
# 运行测试
npm test

# 启动开发服务器
npm run dev

# 代码检查
npm run lint

# 构建
npm run build
```

## 架构说明
- [例如：API 路由在 src/app/api/ 下]
- [例如：共享类型定义在 src/types/ 下]
- [例如：数据库迁移文件在 prisma/migrations/ 下]

## 重要规则
- [例如：不要修改 vendor/ 目录下的文件]
- [例如：提交前必须跑测试]
- [例如：所有密钥使用环境变量，绝对不要硬编码]
````

Claude Code 在每次会话开始时都会读取这个文件。一份好的 CLAUDE.md 可以省去你每次都要重新解释项目结构、编码规范和个人偏好的麻烦——既省 Token 又提升回答质量。

## 第五步：配置权限

默认情况下，Claude Code 采用谨慎模式——在修改文件或执行命令之前都会请求你的许可。你可以通过 `settings.json` 来自定义。

### 快速权限配置

创建项目级别的配置文件：

```bash
mkdir -p .claude
```

然后创建 `.claude/settings.json`：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Bash(npm run build)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

这样就预批准了安全的命令（代码检查、测试、Git 读取），同时拦截危险操作（删除文件、读取密钥）。其他操作会逐一弹窗请求你的确认。

把 `.claude/settings.json` 提交到仓库，这样整个团队就能共享相同的权限规则。

### 权限模式

Claude Code 提供了几种信任级别：

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| **Default** | 写入/命令前询问 | 学习 Claude Code、不确定的任务 |
| **Sandbox** | 在定义的边界内自由操作 | 日常专业开发 |
| **Trust** | 自动批准一切 | 受信任的自动化流水线 |
| **Read-only** | 不执行工具，仅分析 | 代码评审、方案规划 |

大多数开发者日常工作会选择 Sandbox 模式——权限弹窗减少约 84%，同时仍然保持安全边界。

## 第六步：IDE 集成（可选但强烈推荐）

Claude Code 在独立终端中就能很好地工作，但 IDE 集成能带来可视化编辑、Diff 预览和检查点管理等额外功能。

### VS Code / Cursor / Windsurf

安装 Claude Code 扩展：

1. 打开 VS Code（或 Cursor / Windsurf）
2. 进入扩展面板（`Cmd+Shift+X`）
3. 搜索 "Claude Code"
4. 安装官方 Anthropic 扩展

安装后你会获得：
- **内联编辑**：在文件中直接查看 Claude 的修改，确认后再应用
- **检查点**：快照当前代码状态，需要时可以回滚
- **多会话**：在不同标签页中运行多个 Claude Code 会话
- **文件引用**：用 `@filename` 引用特定文件或行范围

### JetBrains（IntelliJ、PyCharm、WebStorm 等）

JetBrains IDE 也有原生的 Claude Code 集成：

1. 进入 `Settings > Plugins`
2. 搜索 "Claude Code"
3. 安装并重启

JetBrains 集成同样支持内联 Diff 显示和检查点系统。

## 第七步：运行你的第一个实战任务

一切就绪，来做点实际的事情。

进入一个项目目录，启动 Claude Code：

```bash
cd ~/my-project
claude
```

### 可以尝试的入门命令

在深入使用之前，试试这些：

| 类型 | 可以这样说 |
|------|-----------|
| **探索** | "这个项目是做什么的？给我一个全局概览。" |
| **理解** | "解释一下这个代码库中的认证流程是怎么工作的。" |
| **修复** | "登录流程有个 Bug——用户刷新 Token 后会收到 403。找到并修复它。" |
| **构建** | "添加一个 /health 端点，返回应用版本和数据库连接状态。" |
| **测试** | "给 UserService 类写单元测试，目标覆盖率 90%。" |
| **重构** | "api/routes.ts 中的错误处理不一致，统一规范一下。" |

### 看看 Agentic Loop 的实际效果

给 Claude Code 一个复杂任务，观察它的执行过程：

```
You > 给 API 端点添加速率限制

🔧 [1] list_files({"path": "src/api"})
  ✓ 找到 8 个路由文件

🔧 [2] read_file({"path": "src/api/routes.ts"})
  ✓ 读取了 245 行

🔧 [3] read_file({"path": "package.json"})
  ✓ 读取依赖列表

🔧 [4] run_command({"command": "npm install express-rate-limit"})
  ✓ 安装了 express-rate-limit

🔧 [5] write_file({"path": "src/middleware/rateLimiter.ts"})
  ✓ 创建了速率限制中间件

🔧 [6] edit_file({"path": "src/api/routes.ts"})
  ✓ 对所有路由应用了速率限制

🔧 [7] run_command({"command": "npm test"})
  ✓ 全部 47 个测试通过

✅ 速率限制已添加。每个 IP 在 15 分钟内最多 100 次请求。
   修改的文件：src/middleware/rateLimiter.ts（新建）、src/api/routes.ts
```

这就是 [Agentic Loop](/posts/ai/2026-02-24-build-magic-code/)——Claude Code 自主规划、执行、验证，把多个工具调用串联起来直到任务完成。一条指令，七次工具调用，零人工干预。

### 留意你的用量

跑了几个任务之后，看看花了多少：

```
/cost
```

这会显示当前会话的 Token 用量和估算费用。如果你用的是 API 按量付费，这能帮你了解消耗速度。

## 常用斜杠命令速查

| 命令 | 功能 |
|------|------|
| `/help` | 显示所有可用命令 |
| `/model` | 在 Opus / Sonnet / Haiku 之间切换 |
| `/cost` | 查看会话 Token 用量和估算费用 |
| `/compact` | 压缩对话历史（节省 Token） |
| `/clear` | 重置对话（重新开始） |
| `/doctor` | 诊断配置问题 |
| `/rewind` | 回滚到之前的检查点 |
| `/theme` | 更换视觉主题 |
| `/terminal-setup` | 配置多行输入快捷键 |

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Shift+Enter` | 多行输入（iTerm2、WezTerm、Kitty、Ghostty） |
| `Ctrl+R` | 搜索提示历史 |
| `Ctrl+T` | 切换任务列表 |
| `Esc Esc`（连按两次） | 回退到上一个检查点 |
| `Shift+Tab` | 在计划模式中自动接受编辑 |
| `?` | 显示所有键盘快捷键 |

> **macOS 用户提示**：如果 `Alt` 组合键不生效，进入终端的偏好设置，把 `Option` 键设为 `Meta` 键。

## 常见问题排查

### 安装后提示 "command not found"

PATH 中没有包含 `~/.local/bin`，手动添加：

```bash
export PATH="$HOME/.local/bin:$PATH"
# 持久化：
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### WSL 中提示 "exec: node: not found"

WSL 可能调用了 Windows 的 Node.js 而非 Linux 本地的。在 WSL 中原生安装 Node.js：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 18
```

### 企业代理环境下的证书错误

公司的 SSL 审查在干扰连接。设置 CA 证书包：

```bash
export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca-bundle.crt
export HTTPS_PROXY=http://proxy.company.com:8080
```

### 响应缓慢或超时

- 检查网络连接
- 如果正在用 Opus，试试 `/model sonnet`（Sonnet 更快）
- 运行 `/compact` 压缩对话体积
- 如果会话运行了很长时间，关掉重开

### 触发速率限制

如果看到速率限制警告：
- 等几分钟（限制会在滚动时间窗口内重置）
- 切换到更轻量的模型：`/model haiku`
- 考虑升级计划（Pro → Max 5x）
- 如果用的是 API，检查你的 [速率限制](https://docs.anthropic.com/en/api/rate-limits)

## 接下来做什么

你已经准备就绪了。以下是进阶的方向：

1. **[正式配置 CLAUDE.md](/posts/ai/2026-01-12-claudemd-memory-guide/)** — 提升效率最大的一步
2. **[学习 Claude Code Hooks](/posts/ai/2026-02-18-claude-code-hooks-guide/)** — 自动化每次改动的代码检查、测试和格式化
3. **[了解定价方案](/posts/ai/2026-02-25-claude-code-pricing/)** — 根据你的使用量选择合适的方案
4. **[自己动手实现 Claude Code](/posts/ai/2026-02-24-build-magic-code/)** — 深入理解底层的 Agentic Loop 架构
5. **[掌握 Claude Code 高级技巧](/posts/ai/2025-01-23-claude-code-commands/)** — 24 个进阶用法

Claude Code 给的上下文越充分，它的表现就越好。花点时间打磨你的 CLAUDE.md，配置合理的权限，从小任务开始再逐步交付复杂的重构。用不了一周，你就会纳闷以前没有它是怎么写代码的。

## 相关阅读

- [Claude Code 2026 定价：Max 方案值不值？](/posts/ai/2026-02-25-claude-code-pricing/) — 完整的费用拆解
- [CLAUDE.md 指南：给 AI 完美的项目上下文](/posts/ai/2026-01-12-claudemd-memory-guide/) — 高效使用 Claude Code 的必备知识
- [Claude Code 完全指南](/posts/ai/2026-01-14-claude-code-guide/) — 所有功能的深度解析
- [Claude Code Hooks：12 种自动化配置](/posts/ai/2026-02-18-claude-code-hooks-guide/) — 自动化你的工作流
- [从零构建自己的 Claude Code](/posts/ai/2026-02-24-build-magic-code/) — 理解底层架构
- [Claude Code vs Cursor vs Windsurf](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/) — 哪个工具更适合你？
