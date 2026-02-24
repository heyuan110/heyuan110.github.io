+++
date = '2026-02-24T10:00:00+08:00'
draft = false
title = '从零手搓一个 Claude Code：用 Python 打造你自己的终端 AI 编程助手'
description = '深度拆解 Claude Code 核心架构——Agentic Loop 原理，用 Python + OpenAI API 从零构建一个支持工具调用（Function Calling）、流式输出、多轮自主决策的终端 AI 编程助手 MagicCode。从 20 行代码到 250 行完整实现，附源码和逐步演进教程。'
toc = true
tags = ['Claude Code', 'AI 编程', 'Python', 'Agentic Loop', 'Tool Use']
categories = ['AI实战']
keywords = ['手搓 Claude Code', 'MagicCode', '终端 AI 编程助手', 'Agentic Loop', 'Tool Use', 'OpenAI API', 'Function Calling']
+++

![MagicCode 终端 AI 编程助手演示效果](cover.webp)

[Claude Code](/posts/ai/2025-01-14-claude-code-guide/) 是目前最强的终端 AI 编程工具，但你有没有想过——**它到底是怎么工作的？**

用别人的工具是一回事，理解它的核心原理是另一回事。当你搞懂了 Claude Code 的底层架构，你就能自己造一个、改一个、甚至造出更适合自己工作流的版本。

本文将从零开始，用 Python 一步步构建一个名为 **MagicCode** 的终端 AI 编程助手。从第一行代码写起，让你彻底搞懂 Claude Code 这类工具的核心原理。

读完这篇文章，你将收获：

- 理解 Claude Code 的核心架构——**Agentic Loop**
- 掌握 AI **Tool Use（工具调用/Function Calling）** 的完整实现
- 获得一个可运行的终端 AI 编程助手源码
- 具备扩展和定制自己 AI 工具的能力

## 一、先搞懂原理：Claude Code 为什么这么强？

在写代码之前，我们得先搞清楚一个核心问题：**Claude Code 和普通的 AI 聊天有什么本质区别？**

答案是三个字：**[工具调用（Tool Use）](/posts/ai/2026-01-19-agent-skills-new-programming/)**。

### 1.1 普通 AI 聊天 vs 终端 AI 助手

普通 AI 聊天是这样的：

```
你：帮我写个 hello world
AI：好的，这是代码 print("hello world")
你：（复制粘贴到编辑器，手动保存，手动运行）
```

Claude Code 是这样的：

```
你：帮我写个 hello world
AI：（自动创建 hello.py → 写入代码 → 运行 → 告诉你结果）
```

区别在哪？**AI 不只是"说"，它能"做"。** 它拥有一组工具——读文件、写文件、执行命令——并且能自主决定什么时候用哪个工具。

### 1.2 核心架构：Agentic Loop

Claude Code 的灵魂是一个叫 **[Agentic Loop（自主决策循环）](/posts/ai/2026-02-23-agentic-coding-trends-2026/)** 的模式：

![MagicCode 核心架构 - Agentic Loop 流程图](02-architecture.webp)

用大白话说就是：

1. **用户说话** → 传给 LLM
2. **LLM 思考** → 决定是直接回答，还是先用个工具
3. **如果用工具** → 执行工具，把结果传回给 LLM
4. **LLM 继续想** → 可能再用一个工具，也可能直接回答
5. **重复 3-4** → 直到 LLM 认为任务完成

这就是为什么 Claude Code 能处理复杂任务的原因——它不是一次性给你答案，而是像人一样 **"看一看、想一想、做一做、再看看"**，循环往复直到搞定。

### 1.3 Tool Use / Function Calling 是怎么工作的？

OpenAI 和 Anthropic 的 API 都原生支持 Tool Use（OpenAI 叫 Function Calling）。原理很简单：

1. 你告诉 AI："你有这些工具可以用"（传入工具定义）
2. AI 在回复时可以选择调用工具（返回 `tool_calls` 列表）
3. 你执行工具，把结果传回去（`role: "tool"` 消息）
4. AI 根据工具结果继续回答

**AI 不执行工具，你的代码执行。** AI 只是决定"我要用什么工具、传什么参数"，真正的执行逻辑在你的 Python 代码里。这也是为什么你可以完全控制安全边界。

## 二、环境准备

### 2.1 前置条件

- Python 3.10+（推荐 3.12+）
- 一个 OpenAI API Key（[platform.openai.com](https://platform.openai.com)）
- 终端工具（iTerm2 / Terminal / Windows Terminal 都行）

### 2.2 创建项目

```bash
# 创建项目目录
mkdir magiccode && cd magiccode

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install openai rich prompt_toolkit
```

三个依赖，各司其职：

| 库 | 作用 | 为什么需要 |
|---|---|---|
| `openai` | OpenAI 官方 SDK | 调用 GPT API，支持 Function Calling |
| `rich` | 终端 UI 美化 | Markdown 渲染、彩色输出、面板 |
| `prompt_toolkit` | 增强输入 | 历史记录、自动补全（可选） |

### 2.3 配置 API Key

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

> 建议写到 `~/.zshrc` 或 `~/.bashrc` 里，避免每次手动设置。

## 三、从 20 行代码开始：V1 最简版

**不要上来就搞大而全。** 先用最少的代码跑通核心流程，再逐步添加功能。这是 AI 时代的开发哲学——**先让它能说话，再让它能干活。**

![MagicCode V1 基础版代码](04-v1-code.webp)

```python
#!/usr/bin/env python3
"""MagicCode v1 — 20 行实现终端 AI 助手"""
from openai import OpenAI

client = OpenAI()  # 自动读取 OPENAI_API_KEY
history = [{"role": "system", "content": "你是 MagicCode，一个终端 AI 编程助手。用中文回答，代码用英文。"}]

print("🪄 MagicCode v1 - 输入 exit 退出")
while True:
    user_input = input("\n你 > ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    print(f"\n🤖 {reply}")
```

保存为 `v1_basic.py`，运行：

```bash
python v1_basic.py
```

**这就是一个能用的 AI 聊天助手了。** 但它只能"说"不能"做"——就像一个只会纸上谈兵的军师。

### 关键概念解析

**`history` 列表**：这是对话记忆。每次对话都把用户消息和 AI 回复追加进去，这样 AI 才能记住之前聊过什么。这也是为什么你跟 ChatGPT 聊天时它能记住上下文——本质就是把历史消息全部传给 API。

**`system` 消息**：系统提示词，定义 AI 的角色和行为规范。这相当于 Claude Code 的 [`CLAUDE.md`](/posts/ai/2026-01-12-claudemd-memory-guide/)——告诉 AI 它是谁、该怎么做。注意 OpenAI 的 system 消息是作为 messages 列表的第一条传入的。

## 四、加入流式输出：V2 打字机效果

V1 有个大问题：AI 思考的时候你只能干等，等它想完了一次性把整段回复扔出来。体验很糟。

**流式输出（Streaming）** 是解决方案——AI 每生成一个 token 就实时传过来，就像有人在打字一样。

```python
#!/usr/bin/env python3
"""MagicCode v2 — 流式输出版"""
from openai import OpenAI

client = OpenAI()
history = [{"role": "system", "content": "你是 MagicCode，一个终端 AI 编程助手。用中文回答，代码用英文。简洁专业。"}]

print("🪄 MagicCode v2 (streaming) - 输入 exit 退出")
while True:
    user_input = input("\n你 > ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    history.append({"role": "user", "content": user_input})

    # 关键改动：加上 stream=True
    print("\n🤖 ", end="", flush=True)
    full_reply = ""

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        stream=True,  # ← 开启流式输出
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            full_reply += delta

    print()  # 换行
    history.append({"role": "assistant", "content": full_reply})
```

关键变化：加上 `stream=True`，然后遍历 `chunk.choices[0].delta.content` 逐 token 输出。

> `flush=True` 很重要，它告诉 Python 立即把字符写到终端，而不是等缓冲区满了再输出。没有这个参数，你会看到文字一块一块蹦出来，而不是一个字一个字流出来。

## 五、终端美化：V3 用 Rich 渲染 Markdown

终端不等于丑。用 `rich` 库，我们可以让输出像 IDE 一样漂亮——代码高亮、列表格式化、面板边框、彩色标签。

```python
#!/usr/bin/env python3
"""MagicCode v3 — Rich Markdown 渲染版"""
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live

client = OpenAI()
console = Console()
history = [{"role": "system", "content": "你是 MagicCode，一个终端 AI 编程助手。用 Markdown 格式回答。"}]

console.print(Panel(
    "🪄 [bold cyan]MagicCode v3[/] - 终端 AI 编程助手\n输入 exit 退出",
    border_style="cyan"
))

while True:
    console.print()
    user_input = console.input("[bold green]你 >[/] ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    history.append({"role": "user", "content": user_input})

    # 流式输出 + 实时 Markdown 渲染
    full_reply = ""
    stream = client.chat.completions.create(
        model="gpt-4o", messages=history, stream=True,
    )
    with Live(console=console, refresh_per_second=8) as live:
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_reply += delta
                live.update(Panel(
                    Markdown(full_reply),
                    title="🤖 MagicCode",
                    border_style="blue",
                ))

    history.append({"role": "assistant", "content": full_reply})
```

`Rich.Live` 组件会不断刷新显示区域，实现"实时渲染"效果——你能看到 Markdown 表格、代码块随着内容的增加逐渐成型，就像看着一幅画被一笔一笔画出来。

## 六、灵魂登场——工具系统：V4 让 AI 能"做事"

前面三个版本，AI 只是在"聊天"。现在，我们要给它装上手脚——**让它能读文件、写文件、执行命令。**

这是 Claude Code 和普通聊天机器人的根本区别，也是本文最核心的部分。

### 6.1 定义工具

OpenAI 的 Function Calling 工具定义格式如下——外层包一个 `type: "function"`，函数的参数描述用 `parameters`：

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容。支持任意文本文件。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "文件路径"
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "将内容写入文件。文件不存在会自动创建。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "content": {"type": "string", "description": "完整文件内容"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "执行终端命令。有 30 秒超时。",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "shell 命令"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "列出目录结构（自动忽略 node_modules、.git 等）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "目录路径", "default": "."},
                },
                "required": [],
            },
        },
    },
]
```

一个好的工具定义需要做到：
- **名字直觉化**：`read_file` 比 `rf` 清晰
- **描述够具体**：AI 根据描述来判断什么时候用什么工具
- **参数有约束**：必填/选填、类型、默认值都要写清楚

### 6.2 实现工具执行

AI 只决定"用什么工具、传什么参数"，**真正的执行逻辑由我们的 Python 代码负责**。这是安全性的基石——你可以在这里加任何校验和限制：

```python
import os
import subprocess

def execute_tool(name: str, params: dict) -> str:
    """执行工具调用，返回字符串结果"""
    try:
        if name == "read_file":
            with open(params["path"], "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
            # 加行号，方便 AI 精确定位
            numbered = "\n".join(
                f"{i+1:4d} | {line}" for i, line in enumerate(lines)
            )
            return f"📄 {params['path']}（{len(lines)} 行）\n{numbered}"

        elif name == "write_file":
            path = params["path"]
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(params["content"])
            return f"✅ 已写入 {path}（{len(params['content'])} 字符）"

        elif name == "run_command":
            cmd = params["command"]
            # 🛡️ 安全检查：拒绝危险命令
            dangerous = ["rm -rf /", "mkfs", "dd if=", "> /dev/sd"]
            if any(d in cmd for d in dangerous):
                return "❌ 拒绝执行危险命令"
            result = subprocess.run(
                cmd, shell=True, capture_output=True,
                text=True, timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\n--- stderr ---\n" + result.stderr
            return output.strip() or "（命令执行成功，无输出）"

        elif name == "list_files":
            path = params.get("path", ".")
            entries = sorted(os.listdir(path))
            result = []
            for entry in entries:
                full = os.path.join(path, entry)
                icon = "📁" if os.path.isdir(full) else "📄"
                result.append(f"{icon} {entry}")
            return "\n".join(result) or "目录为空"

    except Exception as e:
        return f"❌ {type(e).__name__}: {e}"
```

几个重要的设计决策：

1. **read_file 返回带行号的内容**：这样 AI 在后续的 edit_file 操作中能精确定位要修改的位置
2. **write_file 自动创建目录**：`os.makedirs(exist_ok=True)` 避免"目录不存在"的报错
3. **run_command 有安全检查**：黑名单机制，防止 AI 执行危险操作（关于 AI 编程的安全最佳实践，推荐阅读 [Secure Vibe Coding 安全攻防指南](/posts/ai/2026-02-24-secure-vibe-coding/)）
4. **统一返回字符串**：工具结果必须是字符串类型，这是 API 的要求

### 6.3 实现 Agentic Loop

这是整个项目的**灵魂代码**——不到 40 行，却实现了 AI 自主决策、多轮工具调用、循环执行直到任务完成的完整逻辑：

![Agentic Loop 核心代码](05-agentic-loop.webp)

```python
def chat(user_input: str):
    """Agentic Loop：AI 自主决策循环"""
    history.append({"role": "user", "content": user_input})

    while True:
        # 1️⃣ 调用 LLM（携带工具定义）
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history,
            tools=TOOLS,          # ← 关键：传入工具列表
        )
        message = response.choices[0].message

        # 2️⃣ 把 AI 的完整回复存入历史
        history.append(message)

        # 3️⃣ 处理文本回复
        if message.content:
            console.print(Panel(Markdown(message.content), title="🤖 MagicCode"))

        # 4️⃣ 如果没有工具调用，说明任务完成，退出循环
        if not message.tool_calls:
            break

        # 5️⃣ 执行每个工具调用，把结果反馈给 AI
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            console.print(f"  🔧 {name}({args})")
            result = execute_tool(name, args)

            # 工具结果以 role="tool" 消息反馈
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
        # → 回到 while 循环顶部，AI 继续思考
```

**这段代码的精妙之处在于 `while True` 循环。** AI 的一次回复里可能同时包含文本和工具调用：

```
AI 第 1 轮回复：
  content: "好的，让我先看看项目结构"
  tool_calls: [list_files("."), read_file("package.json")]

→ 执行工具，把结果反馈给 AI

AI 第 2 轮回复：
  content: "我看到这是个 Node.js 项目，让我修改..."
  tool_calls: [write_file("index.js", ...)]

→ 执行工具，把结果反馈给 AI

AI 第 3 轮回复：
  content: "修改完成，让我运行测试验证"
  tool_calls: [run_command("npm test")]

→ 执行工具，把结果反馈给 AI

AI 第 4 轮回复：
  content: "✅ 所有测试通过！我做了以下改动..."
  tool_calls: null（没有工具调用 → 循环结束）
```

**一个用户请求，AI 可能调用十几次工具**，每次都基于上一步的结果决定下一步做什么。这就是 Agentic 的含义——AI 具有自主性。

### 6.4 消息格式详解

理解消息格式对调试至关重要。整个对话的 `history` 看起来像这样：

```python
[
    # 系统消息
    {"role": "system", "content": "你是 MagicCode..."},

    # 用户消息
    {"role": "user", "content": "帮我写个 hello world"},

    # AI 回复（包含工具调用）
    {
        "role": "assistant",
        "content": "好的，我来创建文件",
        "tool_calls": [{
            "id": "call_xxx",
            "type": "function",
            "function": {
                "name": "write_file",
                "arguments": '{"path":"hello.py","content":"print(\'hello\')"}'
            }
        }]
    },

    # 工具执行结果
    {
        "role": "tool",
        "tool_call_id": "call_xxx",
        "content": "✅ 已写入 hello.py（16 字符）"
    },

    # AI 继续回复
    {
        "role": "assistant",
        "content": "文件已创建，现在运行它",
        "tool_calls": [{
            "id": "call_yyy",
            "type": "function",
            "function": {"name": "run_command", "arguments": '{"command":"python hello.py"}'}
        }]
    },

    # ... 循环继续
]
```

注意两个关键点：
- **工具结果用 `role: "tool"` 发送**：和普通 user 消息区分开，AI 知道这是工具执行的结果
- **`tool_call_id` 必须匹配**：每个工具结果都要带上对应 `tool_call` 的 `id`，这样 AI 才知道哪个结果对应哪个工具调用

## 七、完整源码：MagicCode 终极版

把前面所有能力组合起来，再加上一些实用的增强（edit_file 精确编辑、search_code 代码搜索、安全阀防止无限循环），就是完整的 MagicCode。

以下是核心文件 `magic.py` 的完整代码，约 250 行：

```python
#!/usr/bin/env python3
"""
MagicCode - 从零手搓的终端 AI 编程助手
功能：工具调用 | Markdown 渲染 | Agentic Loop
"""
import os
import json
import glob
import subprocess
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# ========== 配置 ==========
MODEL = os.getenv("MAGIC_MODEL", "gpt-4o")
client = OpenAI()  # 自动读取 OPENAI_API_KEY

SYSTEM_PROMPT = """你是 MagicCode，一个强大的终端 AI 编程助手。

## 核心能力
你拥有以下工具：
- read_file: 读取文件内容（带行号）
- write_file: 写入文件（自动创建目录）
- edit_file: 精确替换文件中的指定内容
- run_command: 执行终端命令（30s 超时）
- list_files: 列出目录结构
- search_code: 在代码中搜索关键词

## 工作原则
1. 修改文件前必须先 read_file 查看当前内容
2. 复杂任务分步完成，每步验证
3. 不执行危险命令（rm -rf、格式化等）
4. 用中文回答，代码用英文，Markdown 格式输出"""

# ========== 工具定义 ==========
def _fn(name, desc, params, required):
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object", "properties": params, "required": required},
    }}

TOOLS = [
    _fn("read_file", "读取文件内容，返回带行号的文本。",
        {"path": {"type": "string", "description": "文件路径"}}, ["path"]),
    _fn("write_file", "将内容写入文件，自动创建不存在的目录。",
        {"path": {"type": "string", "description": "文件路径"},
         "content": {"type": "string", "description": "完整文件内容"}}, ["path", "content"]),
    _fn("edit_file", "精确编辑：将文件中的 old_text 替换为 new_text。",
        {"path": {"type": "string", "description": "文件路径"},
         "old_text": {"type": "string", "description": "要替换的原文本"},
         "new_text": {"type": "string", "description": "替换后的新文本"}}, ["path", "old_text", "new_text"]),
    _fn("run_command", "执行 shell 命令，30 秒超时。",
        {"command": {"type": "string", "description": "命令"}}, ["command"]),
    _fn("list_files", "递归列出目录结构（最多 3 层，自动忽略 .git 等）。",
        {"path": {"type": "string", "description": "目录路径"}}, []),
    _fn("search_code", "在项目中搜索包含关键词的代码行。",
        {"pattern": {"type": "string", "description": "搜索关键词"},
         "path": {"type": "string", "description": "搜索目录"}}, ["pattern"]),
]

IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

# ========== 工具执行 ==========
def execute_tool(name: str, params: dict) -> str:
    try:
        if name == "read_file":
            with open(params["path"], "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            lines = content.split("\n")
            numbered = "\n".join(f"{i+1:4d} | {line}" for i, line in enumerate(lines))
            return f"📄 {params['path']}（{len(lines)} 行）\n{numbered}"

        elif name == "write_file":
            path = params["path"]
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(params["content"])
            return f"✅ 已写入 {path}（{len(params['content'])} 字符）"

        elif name == "edit_file":
            path = params["path"]
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if params["old_text"] not in content:
                return "❌ 未找到要替换的文本"
            new_content = content.replace(params["old_text"], params["new_text"], 1)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return f"✅ 已编辑 {path}"

        elif name == "run_command":
            cmd = params["command"]
            dangerous = ["rm -rf /", "mkfs", "dd if=", "> /dev/sd"]
            if any(d in cmd for d in dangerous):
                return "❌ 拒绝执行危险命令"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\n--- stderr ---\n" + result.stderr
            return output.strip() or "（无输出）"

        elif name == "list_files":
            path = params.get("path", ".")
            lines = []
            def walk(d, prefix="", depth=0):
                if depth >= 3: return
                try: entries = sorted(os.listdir(d))
                except PermissionError: return
                for e in entries:
                    full = os.path.join(d, e)
                    if e in IGNORED_DIRS or e.startswith("."): continue
                    if os.path.isdir(full):
                        lines.append(f"{prefix}📁 {e}/")
                        walk(full, prefix + "  ", depth + 1)
                    else:
                        lines.append(f"{prefix}📄 {e}")
            walk(path)
            return "\n".join(lines[:200]) or "目录为空"

        elif name == "search_code":
            pattern = params["pattern"]
            path = params.get("path", ".")
            matches = []
            for fp in glob.glob(os.path.join(path, "**", "*"), recursive=True):
                if any(d in fp for d in IGNORED_DIRS) or not os.path.isfile(fp):
                    continue
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as f:
                        for i, line in enumerate(f, 1):
                            if pattern.lower() in line.lower():
                                matches.append(f"{fp}:{i}: {line.rstrip()}")
                                if len(matches) >= 50: break
                except OSError: continue
                if len(matches) >= 50: break
            return "\n".join(matches) or f"未找到 '{pattern}'"

    except Exception as e:
        return f"❌ {type(e).__name__}: {e}"

# ========== Agentic Loop ==========
class MagicCode:
    def __init__(self):
        self.console = Console()
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def chat(self, user_input: str):
        self.history.append({"role": "user", "content": user_input})
        tool_count = 0

        while True:
            response = client.chat.completions.create(
                model=MODEL, messages=self.history, tools=TOOLS,
            )
            message = response.choices[0].message
            self.history.append(message)

            # 显示文本回复
            if message.content:
                self.console.print(Panel(
                    Markdown(message.content),
                    title="🤖 MagicCode", border_style="blue", padding=(1, 2),
                ))

            # 没有工具调用 → 任务完成
            if not message.tool_calls:
                break

            # 执行每个工具调用
            for tc in message.tool_calls:
                tool_count += 1
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                info = json.dumps(args, ensure_ascii=False)
                if len(info) > 120: info = info[:120] + "..."
                self.console.print(f"  [yellow]🔧 [{tool_count}] {name}[/] [dim]{info}[/]")

                result = execute_tool(name, args)
                preview = result[:100].replace("\n", " ")
                self.console.print(f"  [green]  ✓[/] [dim]{preview}[/]")

                self.history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            if tool_count > 20:
                self.console.print("[red]⚠️ 已达到工具调用上限（20次）[/]")
                break

    def run(self):
        self.console.print(Panel(
            "[bold cyan]🪄 MagicCode[/] — 你的终端 AI 编程助手\n\n"
            "  [green]能力[/]：读写文件 | 执行命令 | 搜索代码 | 精确编辑\n"
            "  [green]命令[/]：exit 退出 | clear 清空历史",
            border_style="cyan", padding=(1, 2),
        ))
        self.console.print(f"  [dim]📂 {os.getcwd()}[/]")
        self.console.print(f"  [dim]🧠 {MODEL}[/]\n")

        while True:
            try:
                user_input = self.console.input("[bold green]✦ 你 >[/] ")
                cmd = user_input.strip().lower()
                if cmd in ("exit", "quit"): break
                elif cmd == "clear":
                    self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    self.console.print("[dim]🗑️ 历史已清空[/]")
                    continue
                elif not cmd: continue
                self.chat(user_input)
                self.console.print()
            except KeyboardInterrupt:
                self.console.print("\n[cyan]👋 再见！[/]")
                break

if __name__ == "__main__":
    MagicCode().run()
```

保存为 `magic.py`，运行：

```bash
python magic.py
```

## 八、工具能力对照

你可能好奇：这 6 个工具够用吗？来看看和 Claude Code 的对照：

![MagicCode 与 Claude Code 工具能力对照](03-tools-table.webp)

Claude Code 的 15 个内置工具中，我们用 6 个工具覆盖了 **80% 的日常使用场景**。剩下的 20% 主要是 [MCP 集成](/posts/ai/2026-02-20-mcp-protocol-guide/)、多文件 diff、notebook 编辑等高级功能——这些是锦上添花，不影响核心体验。如果你对 MCP 集成感兴趣，可以看看 [MCP Server 开发教程](/posts/ai/2026-02-22-claude-code-mcp-server-tutorial/)。

## 九、进阶：五个值得继续做的方向

基础版搞定后，下面五个方向可以让你的 MagicCode 更接近生产级工具：

### 9.1 权限确认机制

Claude Code 在执行写文件或命令前会弹窗让你确认（更多关于 Claude Code 的安全机制，可以参考 [Claude Code Security 深度解析](/posts/ai/2026-02-22-claude-code-security/)）。实现起来很简单：

```python
def execute_tool_with_confirm(name, params):
    # 读操作直接执行
    if name in ("read_file", "list_files", "search_code"):
        return execute_tool(name, params)

    # 写操作需要用户确认
    console.print(f"[yellow]⚠️ {name}({params})[/]")
    confirm = console.input("[bold]允许执行？(y/n) [/]")
    if confirm.lower() == "y":
        return execute_tool(name, params)
    return "用户拒绝了此操作"
```

### 9.2 CLAUDE.md 项目感知

[Claude Code 会自动读取项目根目录的 `CLAUDE.md` 文件来理解项目上下文](/posts/ai/2026-01-12-claudemd-memory-guide/)。我们可以在启动时做同样的事：

```python
def load_project_context():
    """读取项目配置文件作为上下文"""
    context = ""
    for name in ["CLAUDE.md", "AGENTS.md", "README.md"]:
        if os.path.exists(name):
            with open(name, "r") as f:
                context += f"\n\n--- {name} ---\n{f.read()}"
    return context

# 在 SYSTEM_PROMPT 后追加项目上下文
project_ctx = load_project_context()
if project_ctx:
    SYSTEM_PROMPT += f"\n\n## 项目上下文\n{project_ctx}"
```

### 9.3 对话历史持久化

目前退出程序对话历史就没了。可以用 JSON 文件保存：

```python
import json

HISTORY_FILE = ".magiccode_history.json"

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, default=str)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []
```

### 9.4 换用其他模型

MagicCode 不绑定 GPT。只要模型支持 Function Calling，都能用。通过 OpenAI 兼容接口接入其他模型：

```python
from openai import OpenAI

# 使用 DeepSeek
client = OpenAI(api_key="your-key", base_url="https://api.deepseek.com/v1")

# 使用 Qwen（通义千问）
client = OpenAI(api_key="your-key", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 使用本地 Ollama
client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
```

因为用了 OpenAI SDK，所有兼容 OpenAI 格式的模型都能无缝切换——这也是为什么我们选择 OpenAI SDK 的原因。

### 9.5 Token 用量监控

API 是按 token 计费的，加个用量统计很有必要：

```python
total_input_tokens = 0
total_output_tokens = 0

# 在每次 API 调用后累计
total_input_tokens += response.usage.prompt_tokens
total_output_tokens += response.usage.completion_tokens

# 在 exit 时显示
console.print(f"[dim]本次会话 Token 用量：输入 {total_input_tokens} | 输出 {total_output_tokens}[/]")
```

## 十、总结

通过这篇文章，我们从 20 行的基础聊天开始，逐步构建了一个具备完整能力的终端 AI 编程助手：

| 版本 | 能力 | 代码量 | 关键技术 |
|------|------|--------|----------|
| V1 | 基础对话 | 20 行 | Chat Completions API |
| V2 | 流式输出 | 30 行 | Streaming |
| V3 | 终端美化 | 35 行 | Rich + Markdown |
| V4 | 工具系统 + Agentic Loop | 250 行 | Function Calling + 自主循环 |

**核心就三个东西**：LLM API + 工具定义 + Agentic Loop。掌握了这三个，你就掌握了 [Claude Code](/posts/ai/2025-01-14-claude-code-guide/)、[Cursor Agent](/posts/ai/2026-01-19-cursor-agent-best-practices/)、Copilot Workspace 等所有 AI 编程工具的核心架构。

完整代码已在文中给出，复制粘贴就能跑。如果你在实践中遇到问题，欢迎留言交流。

> 授人以鱼不如授人以渔。比起用别人的工具，不如搞懂它是怎么造的——然后造一个更适合自己的。

## 相关阅读

如果你对 AI 编程工具的原理和实战感兴趣，推荐继续阅读：

- [Claude Code 从入门到精通完全指南](/posts/ai/2025-01-14-claude-code-guide/) — 想深入使用 Claude Code，从这篇开始
- [CLAUDE.md 记忆术：一个文件让 AI 永远记住你是谁](/posts/ai/2026-01-12-claudemd-memory-guide/) — 理解 AI 编程助手的"项目感知"机制
- [上下文工程：AI 编程最被低估的核心能力](/posts/ai/2026-02-24-context-engineering-deep-dive/) — 深入理解 system prompt 和上下文设计
- [MCP 协议全面解析：AI 连接万物的通用标准](/posts/ai/2026-02-20-mcp-protocol-guide/) — 了解 AI 工具扩展的未来方向
- [2026 Agentic Coding 趋势报告](/posts/ai/2026-02-23-agentic-coding-trends-2026/) — Agentic Loop 模式正在重塑整个编程行业
- [Claude Code Hooks 实战指南](/posts/ai/2026-02-18-claude-code-hooks-guide/) — Claude Code 的自动化扩展机制
- [Vibe Coding 完全指南](/posts/ai/2026-02-22-vibe-coding-guide/) — 用自然语言驱动 AI 编程的方法论
