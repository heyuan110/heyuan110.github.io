+++
date = '2026-03-05T19:00:00+08:00'
draft = false
title = 'Claude Code 斜杠命令、快捷键与 CLI 完全参考手册'
description = '全面整理 Claude Code 的每个斜杠命令、键盘快捷键、CLI 参数和环境变量，以及如何用 Skills 创建自定义命令。'
toc = true
tags = ['Claude Code', 'Commands', 'CLI Reference', 'Productivity']
categories = ['AI Guides']
keywords = ['claude code 斜杠命令', 'claude code 命令大全', 'claude code 自定义命令', 'claude code 快捷键', 'claude code CLI 参数', 'claude code 环境变量', 'claude code 参考手册']

[[params.faqItems]]
question = "什么是 Claude Code 斜杠命令？"
answer = "斜杠命令是 Claude Code 交互会话中的内置快捷操作，以 / 开头。比如清除上下文（/clear）、查看费用（/cost）、切换模型（/model）、运行诊断（/doctor）等。在会话中输入 / 可查看所有可用命令，输入 /help 查看完整列表。"

[[params.faqItems]]
question = "如何在 Claude Code 中创建自定义斜杠命令？"
answer = "在 .claude/skills/<技能名>/ 目录下创建 SKILL.md 文件，包含 YAML 前置元数据（name、description）和 Markdown 指令。技能名即为斜杠命令名。例如 .claude/skills/deploy/SKILL.md 会创建 /deploy 命令。技能还可以根据对话上下文自动触发，无需手动调用。"

[[params.faqItems]]
question = "Claude Code 中 /compact 和 /clear 有什么区别？"
answer = "/compact 会压缩对话历史但保留关键上下文，减少 token 消耗。当上下文窗口快满但你还在处理同一任务时使用。/clear 会完全重置对话，删除所有历史记录。当你要切换到一个完全无关的任务时使用 /clear。"

[[params.faqItems]]
question = "如何在非交互（print）模式下使用 Claude Code？"
answer = "使用 -p 或 --print 参数：claude -p '你的查询'。它会发送一个查询并在响应后退出，非常适合脚本和 CI/CD 流水线。可配合 --output-format json 获取机器可读输出、--max-turns 限制代理循环次数、--allowedTools 控制权限。"

[[params.faqItems]]
question = "Claude Code 支持哪些键盘快捷键？"
answer = "常用快捷键包括：Escape 取消生成、Ctrl+C 退出、Ctrl+R 反向搜索历史、Ctrl+T 切换任务列表、Ctrl+O 切换详细输出、Shift+Tab 切换权限模式、Ctrl+B 将运行中的命令放到后台。在会话中按 ? 可查看终端支持的所有快捷键。"
+++

![Claude Code 斜杠命令、键盘快捷键和 CLI 参数完整参考指南](cover.webp)

Claude Code 内置了超过 40 个斜杠命令、数十个键盘快捷键和丰富的 CLI 参数。大多数开发者只用到其中五六个，其余功能一直沉睡在角落——这意味着你错过了节省时间、降低 token 成本和自动化重复工作流的机会。

这就是你应该收藏的参考手册。每个斜杠命令的作用和使用场景，每个值得记住的快捷键，每个用于脚本和自动化的 CLI 参数，以及如何用 Skills 构建自定义命令。

不废话，直接上 2026 年 Claude Code 的完整命令参考。

## 内置斜杠命令

在输入框开头输入 `/` 即可查看所有可用命令。输入 `/` 后继续打字可以过滤列表。以下是按用途分类的所有内置命令。

### 会话管理

这些命令控制对话的生命周期——开始新会话、恢复旧工作、管理上下文。

| 命令 | 功能说明 |
|------|---------|
| `/clear` | 清除对话历史，从头开始。别名：`/reset`、`/new` |
| `/compact [指令]` | 压缩对话以节省上下文。可选择性地指定保留内容：`/compact retain the API design decisions` |
| `/resume [session]` | 通过 ID 或名称恢复之前的会话，或打开会话选择器。别名：`/continue` |
| `/fork [name]` | 从当前节点将对话分叉到新会话 |
| `/rename [name]` | 重命名当前会话。不提供名称时，会根据历史自动生成 |
| `/rewind` | 将代码和对话恢复到之前的节点。别名：`/checkpoint` |
| `/exit` | 退出 Claude Code。别名：`/quit` |

**什么时候用哪个：**

- **`/compact`**：当上下文使用率超过 80% 但你还在处理同一任务时。添加聚焦指令控制保留内容：`/compact keep the database schema and error handling patterns`
- **`/clear`**：当切换到完全不同的任务时。旧上下文会干扰 Claude 的判断
- **`/resume`**：当你昨天关闭了会话，想从上次中断的地方继续

```bash
# 先检查上下文使用情况
/context

# 如果上下文快满了，带聚焦指令压缩
/compact retain the authentication flow and test results

# 如果要完全切换任务，清除所有内容
/clear
```

### 信息与诊断

显示当前状态的命令——费用、状态、上下文使用率和环境健康状况。

| 命令 | 功能说明 |
|------|---------|
| `/cost` | 显示当前会话的 token 使用量和费用 |
| `/usage` | 显示套餐使用限制和速率限制状态 |
| `/context` | 以彩色方格图可视化上下文窗口使用情况 |
| `/status` | 显示版本、模型、账户和连接信息 |
| `/doctor` | 对 Claude Code 安装进行诊断 |
| `/help` | 列出所有可用命令 |
| `/stats` | 可视化每日使用量、会话历史和连续使用天数 |
| `/diff` | 打开交互式 diff 查看器，显示未提交更改和每轮 diff |
| `/export [filename]` | 将对话导出为纯文本到文件或剪贴板 |
| `/copy` | 复制最近一条助手回复到剪贴板。有代码块时显示选择器 |
| `/release-notes` | 查看完整更新日志 |
| `/insights` | 生成分析 Claude Code 使用情况的报告 |

**高级技巧：** 在长会话中定期运行 `/cost`。一次代理循环消耗的 token 可能比你预想的快得多。如果费用在攀升，用 `/compact` 缩减上下文大小，或用 `/model sonnet` 切换到更便宜的模型。

```bash
# 快速会话健康检查
/cost          # 我花了多少钱？
/context       # 上下文窗口满了多少？
/usage         # 我快到速率限制了吗？
```

### 模型与模式控制

切换模型、切换模式、改变 Claude 的行为方式。

| 命令 | 功能说明 |
|------|---------|
| `/model [model]` | 切换模型。使用左右方向键调整推理深度 |
| `/fast [on\|off]` | 切换快速模式（相同模型，更快输出） |
| `/plan` | 进入计划模式——Claude 在执行前先提出方案 |
| `/vim` | 在 Vim 和普通编辑模式之间切换 |
| `/output-style [style]` | 切换输出风格：Default、Explanatory 或 Learning |
| `/theme` | 更改颜色主题（浅色、深色、色盲友好等选项） |

**模型切换策略：** 大多数任务从 Sonnet 开始——它能以更低成本处理 80% 的工作。遇到复杂架构决策、隐蔽 bug 或需要深度推理的任务时切换到 Opus。难点处理完后再切回来。

```bash
# 用 Sonnet 开始会话（默认，更便宜）
/model sonnet

# 遇到棘手 bug？切换到 Opus
/model opus

# 难点处理完了，切回来
/model sonnet
```

### 配置与权限

管理设置、权限、认证和项目配置。

| 命令 | 功能说明 |
|------|---------|
| `/config` | 打开设置界面。别名：`/settings` |
| `/permissions` | 查看或更新工具权限。别名：`/allowed-tools` |
| `/init` | 用 CLAUDE.md 文件初始化项目 |
| `/memory` | 编辑 CLAUDE.md 记忆文件，切换自动记忆 |
| `/login` | 登录 Anthropic 账户 |
| `/logout` | 登出 Anthropic 账户 |
| `/hooks` | 配置和管理生命周期钩子 |
| `/agents` | 管理子代理配置 |
| `/skills` | 列出可用技能 |
| `/mcp` | 管理 MCP 服务器连接 |
| `/plugin` | 管理 Claude Code 插件 |
| `/terminal-setup` | 配置终端快捷键（Shift+Enter 等） |
| `/keybindings` | 打开或创建快捷键配置 |
| `/sandbox` | 切换沙盒模式以隔离执行 |
| `/extra-usage` | 配置达到速率限制时的额外用量 |
| `/privacy-settings` | 查看和更新隐私设置（仅 Pro/Max） |
| `/statusline` | 配置终端状态栏显示 |

### 代码审查与 PR 工作流

用于处理 Pull Request 和代码审查的命令。

| 命令 | 功能说明 |
|------|---------|
| `/review` | 审查 PR 的质量、正确性和安全性。传入 PR 编号或留空列出打开的 PR |
| `/pr-comments [PR]` | 获取并显示 GitHub PR 的评论。自动检测当前分支的 PR |
| `/security-review` | 分析待提交更改中的安全漏洞 |
| `/install-github-app` | 设置 Claude GitHub Actions 自动 PR 审查 |

这些命令需要安装并认证 `gh` CLI。如果还没设置：

```bash
# 安装 GitHub CLI
brew install gh

# 认证
gh auth login

# 现在可以在 Claude Code 中使用 PR 命令了
/review 42        # 审查 PR #42
/pr-comments      # 显示当前分支 PR 的评论
/security-review  # 对未提交更改进行安全审计
```

### 工作目录与集成

| 命令 | 功能说明 |
|------|---------|
| `/add-dir <path>` | 向会话添加新的工作目录 |
| `/ide` | 管理 IDE 集成并显示状态 |
| `/chrome` | 配置 Chrome 浏览器集成 |
| `/remote-control` | 使会话可从 claude.ai 远程控制。别名：`/rc` |
| `/desktop` | 在 Claude Code Desktop 应用中继续会话（macOS/Windows）。别名：`/app` |
| `/tasks` | 列出和管理后台任务 |
| `/feedback [report]` | 提交 Claude Code 反馈。别名：`/bug` |

## 键盘快捷键

记住哪怕几个快捷键都能明显加快你的工作流。把它们当成 IDE 快捷键——前期投入，每次会话都有回报。

### 必备快捷键（先学这些）

| 快捷键 | 功能说明 | 使用场景 |
|--------|---------|---------|
| `Escape` | 取消当前生成 | Claude 走偏了 |
| `Escape` + `Escape` | 撤回或摘要 | 撤销 Claude 的上一步操作 |
| `Ctrl+C` | 退出会话 | 工作结束（按两次） |
| `Ctrl+R` | 反向搜索历史 | 查找之前输入过的提示词 |
| `Ctrl+T` | 切换任务列表 | 跟踪多步骤工作进度 |
| `Shift+Tab` | 切换权限模式 | 在自动接受、计划和普通模式之间切换 |
| `?` | 显示可用快捷键 | 忘了某个快捷键 |

### 导航与编辑

| 快捷键 | 功能说明 |
|--------|---------|
| `Up/Down` 方向键 | 浏览命令历史 |
| `Ctrl+K` | 删除到行尾 |
| `Ctrl+U` | 删除整行 |
| `Ctrl+Y` | 粘贴已删除的文本 |
| `Alt+B` | 光标向后移动一个单词 |
| `Alt+F` | 光标向前移动一个单词 |
| `Ctrl+L` | 清除终端屏幕（保留历史） |

### 模式与显示切换

| 快捷键 | 功能说明 |
|--------|---------|
| `Ctrl+O` | 切换详细输出（查看详细工具使用情况） |
| `Ctrl+B` | 将运行中的任务放到后台（tmux 用户：按两次） |
| `Ctrl+G` | 在外部文本编辑器中打开当前提示词 |
| `Option+P` / `Alt+P` | 不清除提示词的情况下切换模型 |
| `Option+T` / `Alt+T` | 切换扩展思考 |

### 多行输入

编写多行提示词需要特殊按键组合，因为 Enter 会直接提交消息。

| 方法 | 快捷键 | 备注 |
|------|--------|------|
| 反斜杠转义 | `\` + `Enter` | 所有终端通用 |
| macOS 默认 | `Option+Enter` | macOS 默认方式 |
| Shift+Enter | `Shift+Enter` | 在 iTerm2、WezTerm、Ghostty、Kitty 中开箱即用 |
| 换行符 | `Ctrl+J` | 所有终端通用 |
| 粘贴模式 | 直接粘贴 | 适用于代码块和日志 |

如果 Shift+Enter 在你的终端不起作用，运行 `/terminal-setup` 安装快捷键绑定。

### 快速输入前缀

| 前缀 | 功能说明 | 示例 |
|------|---------|------|
| `/` | 斜杠命令或技能 | `/compact retain error patterns` |
| `!` | 直接执行 bash 命令 | `! git status` |
| `@` | 文件路径自动补全 | `@src/main.ts` |

`!` 前缀非常强大——它直接运行 shell 命令并将输出添加到对话上下文中，而不需要 Claude 解释或批准。用它在保持上下文的同时做快速检查：

```bash
! npm test                # 运行测试，输出进入上下文
! git log --oneline -5    # 检查最近的提交
! cat .env.example        # 显示文件内容
```

## CLI 参数参考

CLI 参数让你从命令行自定义 Claude Code 的行为。它们对脚本、CI/CD 流水线和自动化至关重要。

### 会话控制

| 参数 | 说明 | 示例 |
|------|------|------|
| `--continue`, `-c` | 恢复最近的对话 | `claude -c` |
| `--resume`, `-r` | 通过 ID 或名称恢复会话 | `claude -r auth-refactor` |
| `--from-pr` | 恢复关联到某个 PR 的会话 | `claude --from-pr 123` |
| `--fork-session` | 恢复时分叉到新会话 | `claude -r abc123 --fork-session` |
| `--session-id` | 使用特定的会话 UUID | `claude --session-id "550e8400-..."` |
| `--worktree`, `-w` | 在隔离的 git worktree 中启动 | `claude -w feature-auth` |

### 模型与行为

| 参数 | 说明 | 示例 |
|------|------|------|
| `--model` | 设置模型（`sonnet`、`opus` 或完整名称） | `claude --model opus` |
| `--fallback-model` | 过载时自动降级（print 模式） | `claude -p --fallback-model sonnet "query"` |
| `--permission-mode` | 以特定权限模式启动 | `claude --permission-mode plan` |
| `--agent` | 为会话指定代理 | `claude --agent my-custom-agent` |
| `--agents` | 通过 JSON 定义自定义子代理 | 见下方示例 |

### Print 模式（非交互式）

Print 模式（`-p`）是用 Claude Code 编写脚本的关键。它发送查询然后退出——没有交互式会话。

| 参数 | 说明 | 示例 |
|------|------|------|
| `--print`, `-p` | 非交互模式 | `claude -p "explain this codebase"` |
| `--output-format` | 输出格式：`text`、`json` 或 `stream-json` | `claude -p --output-format json "query"` |
| `--json-schema` | 用 JSON Schema 验证输出 | `claude -p --json-schema '{...}' "query"` |
| `--max-turns` | 限制代理轮数 | `claude -p --max-turns 3 "query"` |
| `--max-budget-usd` | 为此次运行设置费用上限 | `claude -p --max-budget-usd 5.00 "query"` |
| `--input-format` | 输入格式：`text` 或 `stream-json` | `claude -p --input-format stream-json` |

**实用脚本示例：**

```bash
# 生成 API 文档并保存到文件
claude -p "Generate API documentation for src/api/" --output-format text > api-docs.md

# 以 JSON 格式获取结构化分析
claude -p "Analyze the error handling in this project" --output-format json | jq '.result'

# 限制耗费较高的操作的花费
claude -p --max-budget-usd 2.00 --max-turns 5 "Refactor the auth module"

# 通过管道传入内容进行分析
cat error.log | claude -p "What caused this crash?"

# CI/CD：带预算上限检查代码质量
claude -p --max-budget-usd 1.00 --output-format json \
  "Review the last commit for security issues" | jq '.result'
```

### 权限与工具控制

| 参数 | 说明 | 示例 |
|------|------|------|
| `--allowedTools` | 无需权限确认即可运行的工具 | `--allowedTools "Bash(git log:*)" "Read"` |
| `--disallowedTools` | 完全阻止的工具 | `--disallowedTools "Bash(rm *)" "Edit"` |
| `--tools` | 限制可用的内置工具 | `--tools "Bash,Edit,Read"` |
| `--dangerously-skip-permissions` | 跳过所有权限确认（极度谨慎使用） | 不建议在生产环境使用 |

**`--allowedTools` 参数是完全跳过权限的更安全替代方案。** 你可以实现自动化而不给 Claude 全部权限：

```bash
# 只允许读取操作和 git 命令
claude -p --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Read" "Grep" "Glob" \
  "Generate a code review for the last 3 commits"
```

### 系统提示词自定义

| 参数 | 说明 | 使用场景 |
|------|------|---------|
| `--system-prompt` | 替换整个系统提示词 | 完全控制行为 |
| `--system-prompt-file` | 用文件内容替换 | 版本控制的提示词 |
| `--append-system-prompt` | 追加到默认提示词 | 在保持默认功能的同时添加额外规则 |
| `--append-system-prompt-file` | 追加文件内容 | 从文件加载规则 |

大多数情况下，`--append-system-prompt` 是最安全的选项——它保留 Claude Code 的内置能力，同时添加你的自定义规则：

```bash
# 添加项目特定规则
claude --append-system-prompt "Always use TypeScript. Never use any. Include JSDoc comments."

# 从文件加载规则以保持团队一致性
claude --append-system-prompt-file ./team-rules.txt
```

### MCP 与扩展

| 参数 | 说明 | 示例 |
|------|------|------|
| `--mcp-config` | 从 JSON 文件加载 MCP 服务器 | `claude --mcp-config ./mcp.json` |
| `--strict-mcp-config` | 只使用 `--mcp-config` 中的服务器 | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--chrome` | 启用 Chrome 浏览器集成 | `claude --chrome` |
| `--plugin-dir` | 从目录加载插件 | `claude --plugin-dir ./my-plugins` |
| `--add-dir` | 添加额外工作目录 | `claude --add-dir ../apps ../lib` |

### 其他常用参数

| 参数 | 说明 |
|------|------|
| `--verbose` | 详细日志输出，显示完整的逐轮信息 |
| `--debug` | 启用调试模式，可按类别过滤：`--debug "api,mcp"` |
| `--version`, `-v` | 显示版本号 |
| `--ide` | 启动时自动连接 IDE |
| `--init` | 启动时运行初始化钩子 |
| `--remote` | 在 claude.ai 上创建 Web 会话 |
| `--teleport` | 在本地终端恢复 Web 会话 |
| `--disable-slash-commands` | 禁用此会话的所有技能和命令 |
| `--settings` | 从 JSON 文件加载额外设置 |

## 使用 Skills 创建自定义命令

内置命令覆盖了通用需求。但你的团队有特定的工作流——部署清单、代码审查流程、文档格式等。这就是自定义命令的用武之地。

Claude Code 支持两种方式：传统斜杠命令（`.claude/commands/` 中的文件）和更新的 Skills 系统（`.claude/skills/` 中的文件）。**Skills 是推荐方式**——它能做到命令能做的一切，还额外支持自动触发和辅助文件。

### 创建自定义 Skill

一个 Skill 就是包含 `SKILL.md` 文件的文件夹，文件中有 YAML 前置元数据和 Markdown 指令。

**第 1 步：** 创建技能目录。

```bash
# 项目级技能（通过 Git 与团队共享）
mkdir -p .claude/skills/deploy

# 个人技能（在你所有项目中可用）
mkdir -p ~/.claude/skills/deploy
```

**第 2 步：** 编写 SKILL.md 文件。

````yaml
---
name: deploy
description: Deploy the application to staging or production. Use when the user mentions deploying, releasing, or shipping.
---

# Deployment Workflow

## Pre-deployment Checks
1. Run the full test suite: `npm test`
2. Check for uncommitted changes: `git status`
3. Verify you're on the correct branch

## Deploy Steps
1. Build the production bundle: `npm run build`
2. Run database migrations if needed
3. Deploy using: `./scripts/deploy.sh <environment>`
4. Verify the deployment health check

## Post-deployment
1. Monitor error rates for 15 minutes
2. Run smoke tests against the deployed environment
3. Update the deployment log
````

**第 3 步：** 使用它。

```bash
# 手动调用
/deploy

# 或者直接描述你想做什么——Claude 会自动检测到对应技能
"Deploy the latest changes to staging"
```

### Skill 前置元数据选项

YAML 前置元数据控制技能的激活方式和时机：

```yaml
---
name: code-review
description: Thorough code review following team standards
# 可选字段：
user_invocable: true       # 允许手动 /code-review 调用（默认：true）
auto_invocable: true       # 允许 Claude 自动触发（默认：true）
model: opus                # 强制使用特定模型
tools:                     # 限制此技能可用的工具
  - Read
  - Grep
  - Glob
---
```

### Skills 与传统命令对比

| 特性 | 传统命令 | Skills |
|------|---------|--------|
| 位置 | `.claude/commands/name.md` | `.claude/skills/name/SKILL.md` |
| 调用方式 | 仅手动（`/name`） | 自动触发 + 手动 |
| 辅助文件 | 不支持 | 支持（模板、脚本、示例放在同一目录） |
| 前置元数据 | 可选 | 完全控制（模型、工具、调用方式） |
| 状态 | 仍然可用 | 推荐使用 |

传统命令继续有效。如果你有现成的 `.claude/commands/` 文件，它们会继续工作。方便时再迁移——或者不迁移也行。同名的 Skill 和命令会优先解析为 Skill。

要深入了解构建高级 Skills，请参阅 [Claude Code Skills 指南](/posts/ai/2026-02-28-claude-code-skills-guide/)。

## 环境变量

环境变量从更底层配置 Claude Code，比设置或参数更深入。在 shell 配置文件（`~/.zshrc`、`~/.bashrc`）中设置，或按会话设置。

### 认证

| 变量 | 用途 |
|------|------|
| `ANTHROPIC_API_KEY` | 你的 Anthropic API 密钥。不设置则使用订阅认证 |
| `ANTHROPIC_AUTH_TOKEN` | 自定义 Authorization 头值（加 `Bearer ` 前缀） |

### 云服务提供商配置

| 变量 | 用途 |
|------|------|
| `CLAUDE_CODE_USE_BEDROCK` | 设为 `1` 通过 AWS Bedrock 路由 |
| `CLAUDE_CODE_USE_VERTEX` | 设为 `1` 通过 Google Vertex AI 路由 |
| `CLAUDE_CODE_USE_FOUNDRY` | 设为 `1` 通过 Microsoft Foundry 路由 |

### 模型配置

| 变量 | 用途 |
|------|------|
| `ANTHROPIC_MODEL` | 覆盖默认模型 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 默认 Sonnet 级别模型 ID |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | 默认 Opus 级别模型 ID |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 默认 Haiku 级别模型 ID |
| `CLAUDE_CODE_EFFORT_LEVEL` | 思考深度：`low`、`medium` 或 `high` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | 最大输出 token 数（默认 32,000；最大 64,000） |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 子代理使用的模型 |

### Bash 执行

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `BASH_DEFAULT_TIMEOUT_MS` | bash 命令默认超时 | 视情况而定 |
| `BASH_MAX_TIMEOUT_MS` | 模型可设置的最大超时 | 视情况而定 |
| `BASH_MAX_OUTPUT_LENGTH` | 截断前的最大字符数 | 视情况而定 |
| `CLAUDE_CODE_SHELL` | 覆盖自动 shell 检测 | 自动 |
| `CLAUDE_CODE_SHELL_PREFIX` | 包装所有 bash 命令的前缀 | 无 |

### 功能开关

| 变量 | 设为 `1` 以... |
|------|----------------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | 禁用自动记忆 |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 禁用后台任务功能 |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | 禁用快速模式 |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | 从系统提示词中移除 git 工作流指令 |
| `DISABLE_AUTOUPDATER` | 禁用自动更新 |
| `DISABLE_PROMPT_CACHING` | 禁用提示词缓存 |
| `DISABLE_COST_WARNINGS` | 隐藏费用警告消息 |

**设置环境变量：**

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_CODE_EFFORT_LEVEL="high"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000

# 单次会话覆盖
CLAUDE_CODE_EFFORT_LEVEL=low claude -p "Quick summary of this file"

# AWS Bedrock 用户
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
```

## 高级使用技巧

### 1. 链式命令提升上下文效率

不要发多条消息，而是在请求前一次性提供完整上下文：

```bash
# 不好：多轮对话，浪费 token
"What does the auth module do?"
"Now add rate limiting to it"
"Now write tests for the rate limiting"

# 好：单条提示词，完整上下文
"Add rate limiting to the auth module in src/auth/ and write tests.
 Rate limit: 100 requests per minute per IP.
 Use the existing Redis connection for storage.
 Follow the test patterns in tests/auth/"
```

### 2. 用 /cost 监控费用

养成每 15-20 分钟在活跃会话中检查 `/cost` 的习惯。在 Claude 读取文件、编辑、运行测试和迭代的代理循环中，token 消耗可能会飙升。

如果费用增长超出预期：
- 运行 `/compact` 缩减上下文大小
- 用 `/model sonnet` 切换到不太复杂的子任务
- 将大任务拆分为更小、更专注的会话

### 3. 策略性使用 /compact

`/compact` 不只是上下文满了时的紧急按钮。要主动使用它：

```bash
# 完成一个子任务后，在开始下一个前压缩
/compact retain the API schema and test results, discard the debugging steps

# 在复杂操作前腾出空间
/compact keep only the project architecture and current task requirements
```

### 4. 脚本化重复工作流

将 `-p` 模式与 shell 脚本结合，用于经常执行的任务：

```bash
#!/bin/bash
# daily-review.sh -- 每日代码审查例程

echo "=== 审查昨日更改 ==="
claude -p --max-budget-usd 1.00 --output-format text \
  "Review all commits from the last 24 hours. Flag any security issues,
   missing tests, or code quality problems. Be concise." \
  --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Bash(git show:*)" "Read" "Grep"

echo "=== 完成 ==="
```

### 5. 后台运行耗时命令

当 Claude 正在执行慢命令（测试、构建、部署）时，按 `Ctrl+B` 将其放到后台。你可以在命令完成期间继续编写提示词：

```bash
# Claude 开始运行 "npm test"（需要 2 分钟）
# 按 Ctrl+B 放到后台
# 继续输入你的下一条指令
# Claude 完成后自动获取输出
```

### 6. 用 Vim 模式编写复杂提示词

如果你经常写长篇详细的提示词，用 `/vim` 启用 Vim 模式。你可以在 Claude Code 输入框中使用完整的 Vim 导航（hjkl、单词移动、文本对象）和编辑（dd、ciw、yy）功能。随时用 `/vim` 切换回普通模式。

### 7. 定义子代理处理专项任务

用 `--agents` 参数创建专注的子代理，让 Claude 委派任务给它们：

```bash
claude --agents '{
  "test-writer": {
    "description": "Writes comprehensive tests. Use after any code change.",
    "prompt": "You write thorough tests. Cover happy path, edge cases, and error conditions.",
    "tools": ["Read", "Edit", "Bash"],
    "model": "sonnet"
  },
  "security-reviewer": {
    "description": "Reviews code for security vulnerabilities.",
    "prompt": "You are a security expert. Find injection, auth, and data exposure risks.",
    "tools": ["Read", "Grep", "Glob"],
    "model": "opus"
  }
}'
```

## 速查卡片

以下是快速参考表。打印出来、钉到墙上，或在第二个终端中打开。

**日常必备：**

| 操作 | 命令 |
|------|------|
| 检查费用 | `/cost` |
| 检查上下文使用情况 | `/context` |
| 压缩上下文 | `/compact [focus]` |
| 从头开始 | `/clear` |
| 切换模型 | `/model sonnet` 或 `/model opus` |
| 恢复上次会话 | `claude -c` |
| 运行诊断 | `/doctor` |

**键盘快捷键：**

| 操作 | 快捷键 |
|------|--------|
| 取消生成 | `Escape` |
| 撤销 Claude 的操作 | `Escape` + `Escape` |
| 搜索历史 | `Ctrl+R` |
| 切换任务列表 | `Ctrl+T` |
| 详细输出 | `Ctrl+O` |
| 切换权限模式 | `Shift+Tab` |
| 后台运行命令 | `Ctrl+B` |
| 切换模型 | `Alt+P` |

**脚本模式模板：**

```bash
claude -p "your query" \
  --output-format json \
  --max-turns 5 \
  --max-budget-usd 2.00 \
  --allowedTools "Read" "Grep" "Glob"
```

## 相关阅读

- [Claude Code Guide 2026: Everything You Need to Know](/posts/ai/2026-02-28-claude-code-complete-guide/) -- 链接所有 Claude Code 指南的中心页面
- [Claude Code Hooks: Automate Your AI Workflow](/posts/ai/2026-03-05-claude-code-hooks-guide/) -- 使用生命周期钩子实现确定性自动化
- [Claude Code Skills Guide: Create Custom Workflows](/posts/ai/2026-02-28-claude-code-skills-guide/) -- 深入了解构建 Skills
- [CLAUDE.md Best Practices: Write Files That Actually Work](/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) -- 高效的项目配置
- [Install Claude Code in 5 Minutes](/posts/ai/2026-02-25-claude-code-setup-guide/) -- 从零开始入门
- [10 Claude Code Mistakes Beginners Make](/posts/ai/2026-02-25-claude-code-mistakes/) -- 避免常见陷阱
