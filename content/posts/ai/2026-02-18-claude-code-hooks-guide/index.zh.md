+++
date = '2026-02-18T11:00:00+08:00'
draft = false
title = 'Claude Code Hooks 实战指南：12 个即用配置让 AI 自动守规矩'
description = '深入讲解 Claude Code Hooks 机制，涵盖 15 个生命周期事件、3 种 Hook 类型（command/prompt/agent）、12 个可直接复制使用的实战配置。从自动格式化、敏感文件保护、危险命令拦截到 Slack 通知一网打尽，附完整组合配置方案。'
toc = true
tags = ['Claude Code', 'AI 编程', 'Hooks', '自动化', '开发效率']
categories = ['AI实战']
keywords = ['Claude Code Hooks', 'Claude Code 自动化', 'Claude Code 配置', 'PreToolUse', 'PostToolUse', 'AI 编程工作流']
+++

用 Claude Code 写代码，你一定遇到过这些问题：

- Claude 改完文件，格式乱了，每次都要手动跑 `prettier`
- Claude 不小心改了 `.env` 或 `package-lock.json`，你发现时已经晚了
- Claude 说"搞定了"，但测试根本没跑过
- 离开电脑去倒杯咖啡，回来不知道 Claude 是不是在等你

这些问题的本质是：**Claude 是概率性的，但你的工作流需要确定性的保障**。

Hooks 就是解决方案。它是 Claude Code 提供的生命周期钩子机制——你定义规则，Claude Code 在关键节点自动执行。不靠 AI "记住"，而是靠代码"保证"。

本文会给你 12 个可以直接复制粘贴到配置文件里的 Hooks 配置，覆盖从代码格式化到安全防护的核心场景。

## 一、Hooks 是什么？三分钟搞懂核心概念

### 1.1 一句话定义

Hooks 是你定义的 Shell 命令（或 AI 提示词），在 Claude Code 运行的特定时刻自动触发。

打个比方：如果 Claude Code 是一个员工，Hooks 就是你贴在他工位上的便利贴——"每次改完代码记得格式化"、"不要碰 .env 文件"、"交付前先跑测试"。区别在于，便利贴会被忽略，但 **Hooks 一定会执行**。

### 1.2 三种 Hook 类型

| 类型 | 关键字 | 工作方式 | 适用场景 |
|------|--------|---------|---------|
| **命令型** | `command` | 执行 Shell 命令 | 格式化、文件保护、通知 |
| **提示型** | `prompt` | 让 AI（默认 Haiku）做单轮判断 | 任务完成度检查 |
| **Agent 型** | `agent` | 启动子 Agent 多轮验证 | 运行测试、检查代码质量 |

90% 的场景用 `command` 类型就够了。`prompt` 和 `agent` 类型用于需要"判断力"的场景——比如让 AI 检查"任务是否真的做完了"。

### 1.3 15 个生命周期事件

每个事件对应 Claude Code 运行过程中的一个关键时刻：

```
SessionStart          ──────────────────── 会话启动或恢复
    │
UserPromptSubmit      ──────────────────── 用户提交 Prompt
    │
    ├── PreToolUse    ──────────────────── 工具调用前（可拦截）
    │       │
    │   PermissionRequest ───────────────── 弹出权限确认
    │       │
    │   PostToolUse   ──────────────────── 工具调用成功后
    │   PostToolUseFailure ──────────────── 工具调用失败后
    │
    ├── SubagentStart ──────────────────── 子 Agent 启动
    │   SubagentStop  ──────────────────── 子 Agent 结束
    │
    ├── PreCompact    ──────────────────── 上下文压缩前
    │
    ├── Notification  ──────────────────── 通知（等待输入等）
    │
    ├── TaskCompleted ──────────────────── 任务标记完成时
    │
    ├── TeammateIdle  ──────────────────── Agent 团队成员闲置
    │
Stop                  ──────────────────── Claude 完成回复
    │
SessionEnd            ──────────────────── 会话结束
```

其中最常用的四个事件：

- **PreToolUse**：工具执行前，可以拦截危险操作
- **PostToolUse**：工具执行后，适合自动格式化、自动提交
- **Notification**：Claude 等待输入时，适合发送通知
- **Stop**：Claude 完成回复时，适合做最终验证

### 1.4 配置文件放在哪？

| 位置 | 作用范围 | 是否可提交到 Git |
|------|---------|---------------|
| `~/.claude/settings.json` | 所有项目 | 否（你的机器专属） |
| `.claude/settings.json` | 当前项目 | 是（团队共享） |
| `.claude/settings.local.json` | 当前项目 | 否（被 gitignore） |

**推荐策略**：
- 个人习惯（如桌面通知）放 `~/.claude/settings.json`
- 团队规范（如代码格式化）放 `.claude/settings.json` 并提交到仓库
- 本地调试用的放 `.claude/settings.local.json`

## 二、5 分钟上手：你的第一个 Hook

最快的方式是用 `/hooks` 交互菜单。但我更推荐直接编辑配置文件——因为这样可以版本控制、团队共享，而且配置格式一目了然。

### 2.1 桌面通知：Claude 等你时不用盯着终端

这是最简单也最实用的 Hook。当 Claude 需要你输入或确认权限时，系统会弹出桌面通知。

编辑 `~/.claude/settings.json`，添加以下配置：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code 需要你的注意\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

> Linux 用户把 `osascript` 那行换成 `notify-send 'Claude Code' 'Claude Code 需要你的注意'`。

保存后重启 Claude Code（或在 `/hooks` 菜单中确认），让 Claude 执行一个需要权限的操作，然后切到其他窗口——你应该会看到桌面通知弹出来。

### 2.2 配置结构详解

每个 Hook 配置由三部分组成：

```json
{
  "hooks": {
    "事件名": [           // 在哪个时刻触发
      {
        "matcher": "模式",  // 过滤条件（正则表达式）
        "hooks": [          // 要执行的 Hook 列表
          {
            "type": "command",       // Hook 类型
            "command": "Shell 命令",  // 要执行的命令
            "timeout": 30            // 超时时间（秒，可选）
          }
        ]
      }
    ]
  }
}
```

**matcher 匹配规则**：

| 事件 | matcher 匹配的内容 | 示例 |
|------|-------------------|------|
| PreToolUse / PostToolUse | 工具名称 | `Bash`、`Edit\|Write`、`mcp__.*` |
| SessionStart | 会话启动方式 | `startup`、`resume`、`compact` |
| Notification | 通知类型 | `permission_prompt`、`idle_prompt` |
| SessionEnd | 结束原因 | `clear`、`logout` |

matcher 为空字符串表示匹配所有情况。

## 三、12 个实战配置（直接复制使用）

### 配置 1：自动格式化（Prettier）

每次 Claude 编辑或创建文件后，自动运行 Prettier 格式化。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

**工作原理**：
1. `PostToolUse` 事件触发时，Claude Code 把工具调用信息以 JSON 格式传给 stdin
2. `jq -r '.tool_input.file_path'` 从 JSON 中提取被编辑的文件路径
3. `xargs npx prettier --write` 对该文件执行格式化
4. `2>/dev/null; exit 0` 确保即使 Prettier 报错（比如文件类型不支持），Hook 也不会阻塞 Claude

**前置依赖**：项目中需要安装 Prettier（`npm install -D prettier`），系统需要安装 `jq`（`brew install jq`）。

### 配置 2：自动格式化（ESLint）

如果你用 ESLint 而不是 Prettier：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if echo \"$FILE\" | grep -qE '\\.(js|ts|jsx|tsx)$'; then npx eslint --fix \"$FILE\" 2>/dev/null; fi; exit 0"
          }
        ]
      }
    ]
  }
}
```

这里加了文件类型过滤——只对 `.js`、`.ts`、`.jsx`、`.tsx` 文件执行 ESLint，避免对 Markdown 或 JSON 文件报错。

### 配置 3：保护敏感文件

防止 Claude 修改 `.env`、`package-lock.json`、`.git/` 等文件。

先创建脚本 `.claude/hooks/protect-files.sh`：

```bash
#!/bin/bash
# protect-files.sh — 阻止 Claude 修改敏感文件

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# 保护列表：根据项目需要自行添加
PROTECTED_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  "package-lock.json"
  "yarn.lock"
  "pnpm-lock.yaml"
  ".git/"
  "node_modules/"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "已阻止：$FILE_PATH 匹配保护规则 '$pattern'" >&2
    exit 2  # exit 2 = 阻止操作，并将 stderr 内容反馈给 Claude
  fi
done

exit 0  # exit 0 = 允许操作
```

然后赋予执行权限并注册 Hook：

```bash
chmod +x .claude/hooks/protect-files.sh
```

在 `.claude/settings.json` 中添加：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

**关键细节**：
- `exit 2` 会阻止 Claude 的操作，并把 stderr 中的消息反馈给 Claude，让它知道为什么被阻止
- `exit 0` 允许操作继续
- `$CLAUDE_PROJECT_DIR` 是 Claude Code 自动设置的环境变量，指向项目根目录

### 配置 4：阻止危险 Shell 命令

防止 Claude 执行 `rm -rf`、`DROP TABLE`、`git push --force` 等高危命令。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'CMD=$(jq -r \".tool_input.command\" <<< \"$(cat)\"); DANGEROUS=(\"rm -rf /\" \"rm -rf ~\" \"DROP TABLE\" \"git push --force\" \"git reset --hard\" \"dd if=\" \"mkfs\" \":(){ :|:& };:\"); for p in \"${DANGEROUS[@]}\"; do if echo \"$CMD\" | grep -qiF \"$p\"; then echo \"已阻止危险命令: $CMD (匹配: $p)\" >&2; exit 2; fi; done; exit 0'"
          }
        ]
      }
    ]
  }
}
```

这个 Hook 检查 Claude 即将执行的每条 Shell 命令，如果包含危险模式就直接阻止。Claude 会收到阻止原因，并尝试用安全的替代方案完成任务。

### 配置 5：Git 自动暂存

Claude 每次编辑文件后，自动把修改的文件 `git add`，方便后续提交。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); git add \"$FILE\" 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

### 配置 6：记录所有 Bash 命令

把 Claude 执行的每条 Bash 命令记录到日志文件，方便审计和回溯。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'INPUT=$(cat); CMD=$(echo \"$INPUT\" | jq -r \".tool_input.command\"); echo \"[$(date +\"%Y-%m-%d %H:%M:%S\")] $CMD\" >> \"$CLAUDE_PROJECT_DIR\"/.claude/command-log.txt'"
          }
        ]
      }
    ]
  }
}
```

每条记录包含时间戳和命令内容，日志文件保存在 `.claude/command-log.txt`。

### 配置 7：上下文压缩后重新注入关键信息

当 Claude 的上下文窗口满了，会触发自动压缩（compaction），可能丢失关键信息。用 `SessionStart` 的 `compact` matcher 可以在压缩后重新注入重要上下文。

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo '重要提醒：\n1. 本项目使用 pnpm，不要用 npm\n2. 提交前必须运行 pnpm test\n3. Git commit message 用中文\n4. 当前迭代重点：用户认证模块重构'"
          }
        ]
      }
    ]
  }
}
```

Hook 的 stdout 输出会被注入到 Claude 的上下文中。你也可以把 `echo` 换成动态命令，比如：

```json
{
  "type": "command",
  "command": "echo '最近 5 次提交：' && git log --oneline -5"
}
```

### 配置 8：Stop Hook —— 让 Claude 真正做完才停

这是最有"魔法"的 Hook 之一。用 `prompt` 类型让 AI 检查 Claude 是否真的完成了所有任务：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "检查 Claude 是否完成了用户要求的所有任务。如果有任何任务未完成、测试未通过、或者代码有明显问题，请返回 {\"ok\": false, \"reason\": \"具体说明还需要做什么\"}。如果所有任务都已完成，返回 {\"ok\": true}。"
          }
        ]
      }
    ]
  }
}
```

**工作原理**：
1. Claude 每次准备停下来时，触发 `Stop` 事件
2. `prompt` 类型的 Hook 会把上下文发给一个轻量模型（默认 Haiku）做评估
3. 如果返回 `"ok": false`，Claude 会继续工作，并把 `reason` 作为下一步指令
4. 如果返回 `"ok": true`，Claude 正常停止

**防止无限循环**：Hook 输入中有一个 `stop_hook_active` 字段，当它为 `true` 时说明这已经是 Stop Hook 触发后的继续工作，你的脚本应该直接放行。如果用 `command` 类型实现：

```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # 放行，避免无限循环
fi
# ... 你的检查逻辑
```

### 配置 9：Agent Hook —— 自动跑测试验证

比 `prompt` 更强大，`agent` 类型可以启动一个子 Agent，拥有读文件、执行命令等能力：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "验证所有单元测试是否通过。运行测试命令并检查结果。如果有测试失败，返回 {\"ok\": false, \"reason\": \"失败的测试: ...\"}。$ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

这个 Hook 会在 Claude 完成工作后自动运行测试。如果测试失败，Claude 会继续修复，直到所有测试通过。

### 配置 10：自动权限放行（只读操作）

每次 Claude 要读文件、搜索文件时都弹权限确认？用 `PreToolUse` 自动放行只读操作：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Glob|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}'"
          }
        ]
      }
    ]
  }
}
```

**permissionDecision 的三个选项**：
- `"allow"`：直接允许，不弹确认框
- `"deny"`：直接拒绝，配合 `permissionDecisionReason` 告诉 Claude 原因
- `"ask"`：正常弹出确认框（默认行为）

### 配置 11：替换低效命令

当 Claude 想用 `grep` 时，自动提示它用 `rg`（ripgrep）替代：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'CMD=$(jq -r \".tool_input.command\" <<< \"$(cat)\"); if echo \"$CMD\" | grep -q \"^grep \"; then echo \"{\\\"hookSpecificOutput\\\":{\\\"hookEventName\\\":\\\"PreToolUse\\\",\\\"permissionDecision\\\":\\\"deny\\\",\\\"permissionDecisionReason\\\":\\\"请用 rg (ripgrep) 替代 grep，性能更好\\\"}}\"; else exit 0; fi'"
          }
        ]
      }
    ]
  }
}
```

Claude 会收到反馈 "请用 rg (ripgrep) 替代 grep"，然后自动改用 `rg`。

### 配置 12：Slack 通知（当 Claude 需要你时）

把通知发到 Slack，不用盯着桌面：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt|idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST 'https://hooks.slack.com/services/你的/webhook/地址' -H 'Content-Type: application/json' -d '{\"text\": \"Claude Code 正在等你操作\"}' > /dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

把 `https://hooks.slack.com/services/你的/webhook/地址` 替换成你的 Slack Webhook URL。

## 四、Hook 的输入输出机制

理解 Hook 怎么跟 Claude Code 通信，才能写出更复杂的 Hook。

### 4.1 输入（stdin）

每个事件触发时，Claude Code 会以 JSON 格式把上下文信息传给 Hook 的 stdin。例如，当 Claude 执行 Bash 命令时，`PreToolUse` Hook 收到的数据：

```json
{
  "session_id": "abc123",
  "cwd": "/Users/you/project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

不同事件有不同的字段。关键字段对照：

| 事件 | 核心字段 |
|------|---------|
| PreToolUse / PostToolUse | `tool_name`、`tool_input` |
| UserPromptSubmit | `prompt`（用户输入的原始文本） |
| SessionStart | `source`（startup / resume / compact） |
| Stop | `stop_hook_active`（是否在 Stop Hook 续写中） |

### 4.2 输出（stdout / stderr / exit code）

Hook 通过三种方式返回结果：

| 机制 | 作用 |
|------|------|
| **exit 0** | 允许操作继续。stdout 内容会注入 Claude 上下文（仅 SessionStart 和 UserPromptSubmit 事件） |
| **exit 2** | 阻止操作。stderr 内容作为反馈发送给 Claude |
| **其他 exit code** | 操作继续，stderr 写入日志但不展示给 Claude |
| **JSON stdout** | exit 0 时输出 JSON，可实现结构化控制（如 permissionDecision） |

### 4.3 调试技巧

调试 Hook 的两个好方法：

**方法 1：手动测试 Hook 脚本**

```bash
# 模拟一个 PreToolUse 事件
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | bash .claude/hooks/protect-files.sh
echo $?  # 查看 exit code，应该是 2（阻止）
```

**方法 2：开启 Claude Code 的详细模式**

在 Claude Code 中按 `Ctrl+O` 切换详细模式，Hook 的 stderr 输出和执行结果会显示在 transcript 中。或者启动时加 `--debug` 参数：

```bash
claude --debug
```

## 五、组合配置：一个完整的项目 Hook 方案

把上面的配置组合起来，形成一套完整的项目级 Hook 方案。以下是一个 TypeScript + React 项目的真实配置：

`.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'CMD=$(jq -r \".tool_input.command\" <<< \"$(cat)\"); DANGEROUS=(\"rm -rf /\" \"rm -rf ~\" \"git push --force\" \"git reset --hard\"); for p in \"${DANGEROUS[@]}\"; do if echo \"$CMD\" | grep -qiF \"$p\"; then echo \"已阻止危险命令: $CMD\" >&2; exit 2; fi; done; exit 0'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'INPUT=$(cat); CMD=$(echo \"$INPUT\" | jq -r \".tool_input.command\"); echo \"[$(date +\"%Y-%m-%d %H:%M:%S\")] $CMD\" >> \"$CLAUDE_PROJECT_DIR\"/.claude/command-log.txt'"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo '项目规范提醒：\n- 使用 pnpm\n- commit message 用中文\n- 提交前运行 pnpm test\n\n最近提交：' && git log --oneline -5"
          }
        ]
      }
    ]
  }
}
```

`~/.claude/settings.json`（个人全局配置）：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code 需要你的注意\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

这套配置的效果：

| 层级 | 配置内容 | 生效范围 |
|------|---------|---------|
| 全局 | 桌面通知 | 所有项目 |
| 项目 | 文件保护 + 危险命令拦截 | 当前项目 |
| 项目 | 自动格式化 + 命令日志 | 当前项目 |
| 项目 | 压缩后上下文重注入 | 当前项目 |

## 六、进阶技巧

### 6.1 用脚本文件代替内联命令

当 Hook 逻辑变复杂时，建议把命令提取到独立脚本文件：

```
.claude/
├── hooks/
│   ├── protect-files.sh      # 文件保护
│   ├── format-code.sh        # 代码格式化
│   ├── log-commands.sh       # 命令日志
│   └── validate-commit.sh    # 提交验证
└── settings.json
```

脚本文件的优势：
- 逻辑清晰，容易维护
- 可以添加注释
- 可以独立测试
- 避免 JSON 中的转义地狱

### 6.2 匹配 MCP 工具

如果你使用了 MCP Server（比如 GitHub MCP），MCP 工具的命名格式是 `mcp__<server>__<tool>`。用正则匹配：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__github__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"GitHub MCP 工具被调用: $(jq -r '.tool_name')\" >&2"
          }
        ]
      }
    ]
  }
}
```

### 6.3 常见坑和解决方案

**坑 1：Shell Profile 污染 JSON 输出**

如果你的 `~/.zshrc` 或 `~/.bashrc` 里有 `echo "Shell ready"` 这样的语句，Hook 执行时会把这些输出混进 JSON，导致解析失败。

**解决方案**：用交互式 Shell 判断包裹：

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

`$-` 包含 Shell 标志，`i` 表示交互式。Hook 在非交互式 Shell 中运行，所以 `echo` 会被跳过。

**坑 2：Stop Hook 无限循环**

如果 Stop Hook 总是返回 `"ok": false`，Claude 会一直工作下去。**务必检查 `stop_hook_active` 字段**——当它为 `true` 时，说明 Claude 已经在 Stop Hook 触发后的继续工作中，你的 Hook 应该放行。

**坑 3：Hook 不触发**

排查清单：
1. `/hooks` 菜单中能看到这个 Hook 吗？
2. matcher 是否区分大小写？（是的，`bash` 不等于 `Bash`）
3. 手动编辑的配置文件需要重启 Claude Code 或在 `/hooks` 菜单中确认才生效
4. JSON 格式是否合法？（不允许尾逗号和注释）

## 七、Hooks vs Skills vs MCP：怎么选？

这三种扩展机制经常被混淆，其实它们解决的问题完全不同：

| 维度 | Hooks | Skills | MCP |
|------|-------|--------|-----|
| **本质** | 生命周期钩子 | 知识文档 | 工具接口协议 |
| **触发方式** | 自动触发，不依赖 AI 判断 | AI 根据上下文自动匹配 | AI 选择调用 |
| **确定性** | 100% 确定执行 | 概率性（AI 可能不触发） | 概率性 |
| **能力** | 拦截/放行/执行命令 | 提供专业知识和流程指导 | 连接外部工具和服务 |
| **典型用途** | 格式化、安全防护、通知 | 代码审查规范、写作风格 | GitHub 操作、数据库查询 |

**选择原则**：
- **必须执行的规则** --> Hooks（"每次改文件都要格式化"）
- **需要专业知识指导** --> Skills（"按我们公司的标准审查代码"）
- **需要外部工具能力** --> MCP（"帮我在 GitHub 创建 Issue"）

三者可以组合使用。比如：用 MCP 连接 GitHub，用 Skill 定义 PR 审查标准，用 Hook 确保每次提交前都跑测试。

## 八、总结

Hooks 是 Claude Code 从"有用的 AI 助手"进化为"可靠的自动化工作伙伴"的关键一步。它解决的核心问题是：**把"应该做的事"从"希望 AI 记住"变成"系统保证执行"**。

本文给出的 12 个配置覆盖了最常见的场景：

| 编号 | 场景 | 事件类型 | Hook 类型 |
|------|------|---------|----------|
| 1 | 自动格式化（Prettier） | PostToolUse | command |
| 2 | 自动格式化（ESLint） | PostToolUse | command |
| 3 | 保护敏感文件 | PreToolUse | command |
| 4 | 阻止危险命令 | PreToolUse | command |
| 5 | Git 自动暂存 | PostToolUse | command |
| 6 | Bash 命令日志 | PostToolUse | command |
| 7 | 压缩后上下文重注入 | SessionStart | command |
| 8 | 任务完成度检查 | Stop | prompt |
| 9 | 自动跑测试 | Stop | agent |
| 10 | 自动放行只读操作 | PreToolUse | command |
| 11 | 替换低效命令 | PreToolUse | command |
| 12 | Slack 通知 | Notification | command |

建议从最简单的桌面通知和自动格式化开始，逐步添加文件保护和命令安全检查。一旦习惯了这套机制，你会发现 Claude Code 变得可靠得多——因为你不再"希望"它做对，而是"保证"它做对。

---

**参考资料**：

- [Claude Code Hooks 官方文档](https://code.claude.com/docs/en/hooks-guide)
- [Hooks 参考手册（事件 Schema 和高级功能）](https://code.claude.com/docs/en/hooks)
- [Claude Code Hooks 示例集合](https://github.com/karanb192/claude-code-hooks)
- [Hooks 完全指南（含 20+ 示例）](https://aiorg.dev/blog/claude-code-hooks)

## 相关阅读

- [Claude Code 浏览器自动化方案对比（2026 最新）](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Claude Code + Draw Things：Mac 本地 AI 自动配图完全指南](/posts/ai/2026-02-16-claude-code-draw-things-workflow/)
- [Claude Code Skill 完全指南：让 AI 学会你的工作流程](/posts/ai/2026-01-08-claudecode-skill-guide/)
- [Skill 与 MCP 的区别：两种扩展 AI 能力的方式](/posts/ai/2026-01-06-skill&mcp/)
- [Claude Code 记忆术：一个文件让 AI 永远记住你是谁](/posts/ai/2026-01-12-claudemd-memory-guide/)
- [OpenClaw 作者的 Claude Code 开发方法论](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)
