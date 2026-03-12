+++
date = '2026-03-07T18:00:00+08:00'
draft = false
title = '用 Python 从零构建 AI 编程 Agent（完整实战教程）'
description = '手把手教你用 Python 实现 AI Agent，涵盖 Agentic Loop、Function Calling 和工具调用机制。250 行代码，从聊天机器人进化为自主编程助手。'
toc = true
tags = ['Python', 'AI Agent', 'Agentic Loop', 'Tutorial']
categories = ['AI Guides']
keywords = ['Python AI Agent 教程', 'AI Agent 开发', 'Agentic Loop 实现', 'Function Calling 教程', '从零构建编程助手', 'AI Agent 原理', 'Python 工具调用', 'OpenAI Function Calling']

[[params.faqItems]]
question = "用 Python 构建一个 AI Agent 需要多少行代码？"
answer = "大约 250 行 Python 代码就能构建一个功能完整的 AI 编程 Agent，包含 Agentic Loop、6 个工具（读写文件、编辑文件、执行命令、搜索代码、列出目录）以及富文本终端界面。"

[[params.faqItems]]
question = "什么是 Agentic Loop？为什么它很重要？"
answer = "Agentic Loop 是一种 while 循环模式，AI 在循环中反复调用工具、观察结果、决定下一步行动——完全自主——直到任务完成。这是 Claude Code、Cursor、Copilot 等所有现代 AI 编程工具背后的核心架构。"

[[params.faqItems]]
question = "Tool Use 和 Function Calling 有什么区别？"
answer = "Tool Use 和 Function Calling 指的是同一个概念。OpenAI 称之为 Function Calling，Anthropic 称之为 Tool Use。两者都允许 LLM 请求你的代码执行特定函数，由 LLM 决定调用哪个函数以及传递什么参数。"

[[params.faqItems]]
question = "这个 AI Agent 架构可以用 GPT-4 以外的模型吗？"
answer = "可以。因为本教程使用 OpenAI Python SDK 的标准接口，你只需更改 base URL 和 API key，就能换成任何支持 Function Calling 的模型——包括 DeepSeek、Qwen、Claude（通过兼容端点）或通过 Ollama 运行的本地模型。"
+++

![用 Python 从零构建 AI 编程 Agent——完整实战教程，涵盖 Agentic Loop 与工具调用](cover.webp)

每一款 AI 编程工具——[Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/)、Cursor、Copilot——底层跑的都是同一套架构。这篇教程带你亲手搭建这套架构：一个终端 AI 编程 Agent，从零开始，250 行代码，能读文件、写代码、跑命令、自主做多步决策。

不用框架，不加抽象层，只有 Python 和对 AI Agent 运行原理的透彻理解。

## 我们要做什么

教程结束时，你会得到一个名为 **MagicCode** 的 AI 编程 Agent，它能：

- 读写项目中的文件
- 执行 Shell 命令并观察结果
- 在代码库中搜索模式
- 对现有文件做精确编辑
- 自主串联多个操作来完成复杂任务

我们分四个版本逐步构建：

| 版本 | 功能 | 代码行数 | 核心概念 |
|------|------|----------|----------|
| V1 | 基础对话 | 20 | Chat Completions API |
| V2 | 流式输出 | 30 | Token 流式传输 |
| V3 | 富文本终端 | 35 | Markdown 渲染 |
| V4 | 完整 Agent + 工具 | 250 | Agentic Loop + Function Calling |

每个版本都能独立运行，随时可以停下来，手里都有一个可用的东西。

## 为什么要从零构建 AI Agent？

用 AI 编程工具是一回事，理解它怎么工作是另一回事。

当你理解了架构，就能定制它、扩展它、调试它，或者在同样的基础上造出全新的东西。本教程要讲的三个概念——**Agentic Loop**、**工具调用（Function Calling）**和**消息协议**——正是当今市面上每一款 AI 编程 Agent 的核心。

这也是一次[上下文工程](/posts/ai/2026-03-10-context-engineering-guide/)的实战练习——设计 AI 接收什么信息、以何种方式接收。你在本教程中编写的系统提示词、工具定义和对话历史，都是直接影响 Agent 质量的上下文工程决策。

## 架构解析：Agent 和聊天机器人的本质区别

动手写代码之前，先回答一个根本问题：**AI Agent 和普通聊天机器人到底差在哪？**

### 聊天机器人 vs. Agent

聊天机器人回复消息，Agent 采取行动。

```
聊天机器人：
  你："写个 hello world 程序。"
  AI："代码如下：print('hello world')"
  你：（手动复制粘贴、保存、运行）

Agent：
  你："写个 hello world 程序。"
  AI：（创建 hello.py → 写入代码 → 运行 → 报告结果）
```

区别就在于**工具调用**。Agent 拥有工具——读文件、写文件、执行命令——并且自主决定何时、如何使用它们。

### Agentic Loop

实现自主行为的核心模式叫做 **Agentic Loop**：

```
┌─────────────────────────────────────────────┐
│                                             │
│   用户发送消息                                │
│       ↓                                     │
│   LLM 接收消息 + 工具定义                     │
│       ↓                                     │
│   LLM 决策：回复文本还是调用工具？              │
│       ↓                                     │
│   ┌─ 文本回复 → 返回给用户                    │
│   │                                         │
│   └─ 工具调用 → 执行工具                      │
│          ↓                                  │
│      将结果发回 LLM                           │
│          ↓                                  │
│      LLM 再次决策（循环）──────────┐           │
│                                   │         │
│      （重复直到任务完成）  ◄────────┘          │
│                                             │
└─────────────────────────────────────────────┘
```

这就是多步推理的实现方式。AI 不是给你一个一次性答案，而是像开发者一样工作：看代码、思考要做什么、做修改、验证结果、重复。

### Function Calling 的工作原理

OpenAI 和 Anthropic 的 API 都原生支持工具调用（OpenAI 称之为 "Function Calling"）：

1. **你定义工具**——名称、描述、参数 Schema——传给 API
2. **LLM 选择**在回复中调用一个或多个工具
3. **你的代码执行**工具，将结果以 `role: "tool"` 消息的形式发回
4. **LLM 继续**基于结果进行推理

关键洞察：**AI 从不亲自执行工具。** 它只决定调用*哪个*工具、传递*什么参数*。实际执行全由你的 Python 代码负责。这就是安全基础——执行边界完全在你掌控之中。

## 环境准备

你需要三样东西：

- **Python 3.10+**（推荐 3.12+）
- **OpenAI API Key**，从 [platform.openai.com](https://platform.openai.com) 获取
- **一个终端**（任何终端都行）

### 项目初始化

```bash
mkdir magiccode && cd magiccode

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install openai rich prompt_toolkit
```

三个依赖：

| 库 | 用途 |
|----|------|
| `openai` | API 调用，原生支持 Function Calling |
| `rich` | Markdown 渲染、语法高亮、面板 |
| `prompt_toolkit` | 增强终端输入，支持历史记录 |

### 配置 API Key

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

把这行加到 `~/.zshrc` 或 `~/.bashrc`，这样每次开终端都能自动生效。

## V1：20 行代码打地基

从最简单的开始。V1 就是一个朴素的对话循环——没有流式输出、没有工具、没有 UI。20 行代码，验证 API 调用能跑通。

```python
#!/usr/bin/env python3
"""MagicCode v1 — 20 行的终端 AI 助手"""
from openai import OpenAI

client = OpenAI()  # 从环境变量读取 OPENAI_API_KEY
history = [{"role": "system", "content": "You are MagicCode, a terminal AI coding assistant. Be concise and helpful."}]

print("MagicCode v1 — 输入 'exit' 退出")
while True:
    user_input = input("\nYou > ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    print(f"\n{reply}")
```

保存为 `v1_basic.py`，运行：

```bash
python v1_basic.py
```

能跑——但它只会*说*，不会*做*。就像一个能制定作战计划、却没有军队的参谋。

### V1 的关键概念

**`history` 列表**就是对话记忆。每条用户消息和 AI 回复都被追加进去，整个列表随每次 API 调用一起发送。没有什么神奇的持久化机制——就是一个不断增长的消息数组。这也是为什么长对话会撞上 Token 限制，而且费用越来越高。

**`system` 消息**定义了 AI 的角色和行为规则。它的作用和 Claude Code 中的 [CLAUDE.md 文件](/posts/ai/2026-02-28-claude-code-claudemd-guide/)一样——告诉模型自己是谁、该怎么做。

## V2：流式输出——打字机效果

V1 有一个体验问题：在生成长回复时，你得盯着空白终端干等，等模型生成完毕后所有文字一股脑出现。流式输出解决了这个问题——Token 生成一个、显示一个。

```python
#!/usr/bin/env python3
"""MagicCode v2 — 带流式输出"""
from openai import OpenAI

client = OpenAI()
history = [{"role": "system", "content": "You are MagicCode, a terminal AI coding assistant. Be concise and professional."}]

print("MagicCode v2（流式输出）— 输入 'exit' 退出")
while True:
    user_input = input("\nYou > ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    history.append({"role": "user", "content": user_input})

    print("\nAI: ", end="", flush=True)
    full_reply = ""

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        stream=True,  # 关键改动
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            full_reply += delta

    print()  # 回复结束后换行
    history.append({"role": "assistant", "content": full_reply})
```

改动只有一处：设置 `stream=True`，然后遍历 chunk，逐个打印 `delta.content`。

`flush=True` 参数比你想象的更重要。没有它，Python 会缓冲输出，你看到的就不是流畅的逐字符显示，而是一阵一阵的文字突然蹦出来。

## V3：Rich 富文本终端 + Markdown 渲染

终端不一定非得丑。用 `rich` 库，你能在终端里实现 Markdown 渲染、语法高亮、彩色面板和漂亮的排版。

```python
#!/usr/bin/env python3
"""MagicCode v3 — Rich Markdown 渲染 + 实时流式显示"""
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live

client = OpenAI()
console = Console()
history = [{"role": "system", "content": "You are MagicCode, a terminal AI coding assistant. Format responses in Markdown."}]

console.print(Panel(
    "[bold cyan]MagicCode v3[/] — 终端 AI 编程助手\n输入 'exit' 退出",
    border_style="cyan"
))

while True:
    console.print()
    user_input = console.input("[bold green]You >[/] ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    history.append({"role": "user", "content": user_input})

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
                    title="MagicCode",
                    border_style="blue",
                ))

    history.append({"role": "assistant", "content": full_reply})
```

`Rich.Live` 组件在新内容流入时持续重新渲染面板。你可以看着 Markdown 表格、代码块和格式化文本在终端里实时成型。

## V4：工具系统——让 Agent 拥有双手

前三个版本是不断打磨的聊天机器人。现在我们赋予 AI 真正的能力——读文件、写文件、执行命令。这是它从聊天机器人蜕变为 **Agent** 的转折点。

这是本教程最核心的部分。

### 第一步：定义工具

OpenAI 的 Function Calling 要求工具定义遵循特定的 JSON Schema 格式。每个工具需要名称、描述和参数 Schema：

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file. Returns the content with line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to read"
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
            "description": "Write content to a file. Creates parent directories if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Complete file content"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command. Times out after 30 seconds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List directory contents (ignores node_modules, .git, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path", "default": "."},
                },
                "required": [],
            },
        },
    },
]
```

工具定义的重要性超出你的预期。模型通过阅读这些描述来决定*何时*、*如何*使用每个工具。好的工具定义有三个原则：

- **直觉化命名**：`read_file` 一目了然，`rf` 则不然
- **具体的描述**：模型靠描述来判断何时该用某个工具
- **精确的参数 Schema**：必填 vs 可选、类型和默认值都会影响模型的行为

### 第二步：实现工具执行

AI 负责决定调用什么，**你的代码负责真正干活。** 这种分离是整个架构的安全基石：

```python
import os
import subprocess

def execute_tool(name: str, params: dict) -> str:
    """执行工具调用，返回字符串结果。"""
    try:
        if name == "read_file":
            with open(params["path"], "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
            numbered = "\n".join(
                f"{i+1:4d} | {line}" for i, line in enumerate(lines)
            )
            return f"{params['path']} ({len(lines)} lines)\n{numbered}"

        elif name == "write_file":
            path = params["path"]
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(params["content"])
            return f"Written to {path} ({len(params['content'])} chars)"

        elif name == "run_command":
            cmd = params["command"]
            # 安全检查：拦截危险命令
            dangerous = ["rm -rf /", "mkfs", "dd if=", "> /dev/sd"]
            if any(d in cmd for d in dangerous):
                return "Refused to execute dangerous command"
            result = subprocess.run(
                cmd, shell=True, capture_output=True,
                text=True, timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\n--- stderr ---\n" + result.stderr
            return output.strip() or "(Command completed with no output)"

        elif name == "list_files":
            path = params.get("path", ".")
            entries = sorted(os.listdir(path))
            result = []
            for entry in entries:
                full = os.path.join(path, entry)
                prefix = "[dir]" if os.path.isdir(full) else "[file]"
                result.append(f"{prefix} {entry}")
            return "\n".join(result) or "Empty directory"

    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
```

几个值得注意的设计决策：

1. **`read_file` 返回带行号的内容**——方便 AI 后续编辑时精确定位
2. **`write_file` 自动创建目录**——`os.makedirs(exist_ok=True)` 消除了"目录不存在"的错误
3. **`run_command` 有安全黑名单**——简单但有效的危险操作防护
4. **所有工具返回字符串**——这是 API 的要求，工具结果必须是可序列化的文本

### 第三步：构建 Agentic Loop

这是**整个项目的核心**。不到 40 行代码，实现了自主决策、多步工具执行和自驱动任务完成：

```python
def chat(user_input: str):
    """Agentic Loop：AI 自主决策循环。"""
    history.append({"role": "user", "content": user_input})

    while True:
        # 1. 带工具定义调用 LLM
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history,
            tools=TOOLS,          # 传入工具定义
        )
        message = response.choices[0].message

        # 2. 将 AI 的完整回复存入历史
        history.append(message)

        # 3. 显示文本内容
        if message.content:
            console.print(Panel(Markdown(message.content), title="MagicCode"))

        # 4. 没有工具调用？任务完成——退出循环
        if not message.tool_calls:
            break

        # 5. 执行每个工具调用，将结果反馈回去
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            console.print(f"  Tool: {name}({args})")
            result = execute_tool(name, args)

            # 以 role="tool" 消息的形式发送工具结果
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
        # 回到 while 循环顶部——AI 继续思考
```

**精妙之处在于 `while True` 循环。** 一个用户请求可以触发十几次工具调用，每一次都基于上一次的结果做出决策。来看一个真实的多轮执行过程：

```
用户："给 main.py 加上错误处理"

第 1 轮：
  AI："让我先看看项目结构。"
  工具：list_files(".")、read_file("main.py")
  → 执行，发回结果

第 2 轮：
  AI："看到问题了，我来加 try-except..."
  工具：edit_file("main.py", old_text, new_text)
  → 执行，发回结果

第 3 轮：
  AI："改好了，跑下测试验证一下。"
  工具：run_command("python -m pytest")
  → 执行，发回结果

第 4 轮：
  AI："全部测试通过。以下是我做的修改..."
  工具：无 → 循环退出
```

AI 计划、行动、观察、调整——全程自主。这就是"Agentic"的含义。

### 理解消息协议

发送给 API 的 `history` 数组遵循特定结构。理解它对调试至关重要：

```python
[
    # System 消息——定义行为
    {"role": "system", "content": "You are MagicCode..."},

    # 用户消息
    {"role": "user", "content": "Write me a hello world program"},

    # AI 回复——包含工具调用
    {
        "role": "assistant",
        "content": "I'll create the file for you.",
        "tool_calls": [{
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "write_file",
                "arguments": '{"path":"hello.py","content":"print(\'hello world\')"}'
            }
        }]
    },

    # 工具结果——通过 tool_call_id 匹配
    {
        "role": "tool",
        "tool_call_id": "call_abc123",
        "content": "Written to hello.py (20 chars)"
    },

    # AI 继续推理...
]
```

两个能帮你省下大量调试时间的细节：

- **工具结果使用 `role: "tool"`**，不是 `role: "user"`。模型对这两者的处理方式不同——它知道这些数据来自工具执行，而非人类输入。
- **`tool_call_id` 必须精确匹配。** 每个工具结果都必须引用对应 `tool_call` 的 `id`。ID 不匹配会导致 API 报错。

## 完整源码：250 行的完整 Agent

现在把所有部分整合成一个生产级的完整实现。我们再加两个工具（`edit_file` 做精确文本替换，`search_code` 做代码搜索），一个防止死循环的安全阀，以及清晰的面向对象结构。

完整的 `magic.py`：

```python
#!/usr/bin/env python3
"""
MagicCode — 从零构建的终端 AI 编程助手
演示：Agentic Loop | 工具调用 | 流式输出 | Rich UI
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
client = OpenAI()  # 从环境变量读取 OPENAI_API_KEY

SYSTEM_PROMPT = """You are MagicCode, a powerful terminal AI coding assistant.

## Your Tools
- read_file: Read file contents (with line numbers)
- write_file: Write to files (auto-creates directories)
- edit_file: Replace specific text in a file
- run_command: Execute shell commands (30s timeout)
- list_files: List directory structure
- search_code: Search for patterns in code

## Working Principles
1. Always read a file before modifying it
2. Break complex tasks into steps; verify each step
3. Never execute destructive commands (rm -rf, format, etc.)
4. Respond in Markdown format"""

# ========== 工具定义 ==========
def _fn(name, desc, params, required):
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object", "properties": params, "required": required},
    }}

TOOLS = [
    _fn("read_file", "Read file contents. Returns text with line numbers.",
        {"path": {"type": "string", "description": "File path"}}, ["path"]),
    _fn("write_file", "Write content to a file. Creates directories if needed.",
        {"path": {"type": "string", "description": "File path"},
         "content": {"type": "string", "description": "Complete file content"}},
        ["path", "content"]),
    _fn("edit_file", "Replace old_text with new_text in a file (first match).",
        {"path": {"type": "string", "description": "File path"},
         "old_text": {"type": "string", "description": "Text to find"},
         "new_text": {"type": "string", "description": "Replacement text"}},
        ["path", "old_text", "new_text"]),
    _fn("run_command", "Execute a shell command with 30-second timeout.",
        {"command": {"type": "string", "description": "Shell command"}},
        ["command"]),
    _fn("list_files", "Recursively list directory structure (max 3 levels).",
        {"path": {"type": "string", "description": "Directory path"}}, []),
    _fn("search_code", "Search for a pattern across all files in a directory.",
        {"pattern": {"type": "string", "description": "Search pattern"},
         "path": {"type": "string", "description": "Search directory"}},
        ["pattern"]),
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
            return f"{params['path']} ({len(lines)} lines)\n{numbered}"

        elif name == "write_file":
            path = params["path"]
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(params["content"])
            return f"Written to {path} ({len(params['content'])} chars)"

        elif name == "edit_file":
            path = params["path"]
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if params["old_text"] not in content:
                return "Error: Target text not found in file"
            new_content = content.replace(params["old_text"], params["new_text"], 1)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return f"Edited {path}"

        elif name == "run_command":
            cmd = params["command"]
            dangerous = ["rm -rf /", "mkfs", "dd if=", "> /dev/sd"]
            if any(d in cmd for d in dangerous):
                return "Refused to execute dangerous command"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\n--- stderr ---\n" + result.stderr
            return output.strip() or "(No output)"

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
                        lines.append(f"{prefix}[dir] {e}/")
                        walk(full, prefix + "  ", depth + 1)
                    else:
                        lines.append(f"{prefix}[file] {e}")
            walk(path)
            return "\n".join(lines[:200]) or "Empty directory"

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
            return "\n".join(matches) or f"No matches for '{pattern}'"

    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"

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
                    title="MagicCode", border_style="blue", padding=(1, 2),
                ))

            # 没有工具调用意味着任务完成
            if not message.tool_calls:
                break

            # 执行每个工具调用
            for tc in message.tool_calls:
                tool_count += 1
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                info = json.dumps(args, ensure_ascii=False)
                if len(info) > 120: info = info[:120] + "..."
                self.console.print(f"  [yellow][{tool_count}] {name}[/] [dim]{info}[/]")

                result = execute_tool(name, args)
                preview = result[:100].replace("\n", " ")
                self.console.print(f"  [green]  Done[/] [dim]{preview}[/]")

                self.history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            # 安全阀：防止死循环
            if tool_count > 20:
                self.console.print("[red]Tool call limit reached (20)[/]")
                break

    def run(self):
        self.console.print(Panel(
            "[bold cyan]MagicCode[/] — 你的终端 AI 编程助手\n\n"
            "  [green]工具[/]: 读写文件 | 执行命令 | 搜索代码 | 编辑文件\n"
            "  [green]命令[/]: exit 退出 | clear 清空历史",
            border_style="cyan", padding=(1, 2),
        ))
        self.console.print(f"  [dim]工作目录: {os.getcwd()}[/]")
        self.console.print(f"  [dim]模型: {MODEL}[/]\n")

        while True:
            try:
                user_input = self.console.input("[bold green]You >[/] ")
                cmd = user_input.strip().lower()
                if cmd in ("exit", "quit"): break
                elif cmd == "clear":
                    self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    self.console.print("[dim]历史已清空[/]")
                    continue
                elif not cmd: continue
                self.chat(user_input)
                self.console.print()
            except KeyboardInterrupt:
                self.console.print("\n[cyan]再见！[/]")
                break

if __name__ == "__main__":
    MagicCode().run()
```

保存为 `magic.py`，运行：

```bash
python magic.py
```

试着让它创建文件、读回来、修改它，或者执行命令。观察 Agentic Loop 的运作——AI 自主串联多个工具调用来完成你的请求。

## 6 个工具 vs 生产级 Agent

你可能会问：6 个工具够用吗？看看 MagicCode 和 [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) 等生产级 Agent 的对比：

| 能力 | MagicCode | Claude Code |
|------|-----------|-------------|
| 读文件 | `read_file` | Read 工具 |
| 写文件 | `write_file` | Write 工具 |
| 编辑文件 | `edit_file` | Edit 工具 |
| 执行命令 | `run_command` | Bash 工具 |
| 列出目录 | `list_files` | Glob 工具 |
| 搜索代码 | `search_code` | Grep 工具 |
| MCP 集成 | 未包含 | 支持 |
| 多文件 Diff | 未包含 | 支持 |
| Notebook 编辑 | 未包含 | 支持 |
| 网页搜索 | 未包含 | 支持 |

Claude Code 大约有 15 个内置工具。我们的 6 个工具覆盖了日常使用场景的大约 **80%**。剩下的 20% 主要是 [MCP 集成](/posts/ai/2026-02-28-mcp-protocol-explained/)和 Notebook 编辑等高级功能——有用，但不是架构的核心。

## 五种扩展方向

基础已经打好。以下五种扩展能让 MagicCode 更接近生产级工具。

### 1. 权限确认

生产级 Agent 在写文件或执行命令前会征求确认：

```python
def execute_tool_with_confirm(name, params):
    # 只读操作：直接执行
    if name in ("read_file", "list_files", "search_code"):
        return execute_tool(name, params)

    # 写操作：需要用户批准
    console.print(f"[yellow]工具请求执行: {name}({params})[/]")
    confirm = console.input("[bold]允许？(y/n) [/]")
    if confirm.lower() == "y":
        return execute_tool(name, params)
    return "User denied this operation"
```

### 2. 项目上下文加载

[Claude Code 会自动读取项目根目录的 CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) 来理解上下文。你也可以这样做：

```python
def load_project_context():
    """加载项目配置文件作为上下文。"""
    context = ""
    for name in ["CLAUDE.md", "AGENTS.md", "README.md"]:
        if os.path.exists(name):
            with open(name, "r") as f:
                context += f"\n\n--- {name} ---\n{f.read()}"
    return context

# 追加到系统提示词
project_ctx = load_project_context()
if project_ctx:
    SYSTEM_PROMPT += f"\n\n## Project Context\n{project_ctx}"
```

### 3. 随意切换模型

MagicCode 不绑定 GPT。任何支持 Function Calling 的模型都能用。OpenAI SDK 的兼容接口让切换变得轻而易举：

```python
from openai import OpenAI

# DeepSeek
client = OpenAI(api_key="your-key", base_url="https://api.deepseek.com/v1")

# 本地 Ollama
client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
```

这也是本教程使用 OpenAI SDK 的原因之一——它是事实上的标准接口，几乎所有模型提供商都提供兼容端点。

### 4. 对话持久化

目前退出程序后对话历史就丢了。用 JSON 把它保存下来：

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

### 5. Token 用量追踪

API 调用是要花钱的。加个用量追踪很简单：

```python
total_input_tokens = 0
total_output_tokens = 0

# 每次 API 调用后：
total_input_tokens += response.usage.prompt_tokens
total_output_tokens += response.usage.completion_tokens

# 退出时：
console.print(f"[dim]Token 统计 — 输入: {total_input_tokens} | 输出: {total_output_tokens}[/]")
```

## 常见坑和解决办法

构建第一个 Agent 时，你大概率会踩几个坑。应对方法如下：

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `tool_call_id` 不匹配报错 | 工具结果没引用正确的调用 ID | 始终使用响应中的 `tool_call.id`，不要自己生成 |
| Agent 无限循环 | 没有退出条件或模型一直调用工具 | 加 `tool_count` 限制（我们用的是 20） |
| 模型不用工具 | 工具描述太模糊 | 写具体、可操作的描述 |
| 大文件导致崩溃 | 整个文件读进内存 | 加文件大小检查，截断大文件 |
| 命令卡住 | `subprocess.run` 没设超时 | 始终设置 `timeout=30`（或合适的值） |

## 与更广泛的 AI Agent 生态的关联

你在这里构建的架构不只是练手——它和整个行业用的是同一套模式。根据 [Anthropic 关于构建有效 Agent 的研究](https://www.anthropic.com/engineering/building-effective-agents)，带工具调用的 Agentic Loop 是所有生产级 AI Agent 的基础模式。

如果你想看这套模式如何扩展到生产级，可以把你构建的东西和我们 [AI 编程 Agent 横评](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/)中涵盖的 Agent 做对比。你会发现每一个的核心都是同样的三个组件——LLM API、工具定义、Agentic Loop。

要深入了解工具集成的演进方向，可以看我们的 [MCP 协议指南](/posts/ai/2026-02-28-mcp-protocol-explained/)，它标准化了 AI Agent 发现和连接外部工具的方式。

如果你想了解上下文工程原则（比如你设计的系统提示词和工具描述）如何大规模应用，[OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) 是一份优秀的外部资源。

## 核心要点

现代 AI 编程 Agent 的整个架构归结为**三件事**：

1. **一个支持 Function Calling 的 LLM API**
2. **描述可用能力的工具定义**
3. **一个编排思考与行动循环的 Agentic Loop**

掌握这三个概念，你就理解了 Claude Code、Cursor Agent、Copilot Workspace 以及市面上所有 AI 编程工具的核心架构。

完整代码就在这篇文章里——复制、粘贴、运行。从 20 行到 250 行，从聊天机器人到自主 Agent，你现在拥有了在这套模式上构建任何东西的基础。

## 延伸阅读

- [Claude Code 完全指南](/posts/ai/2026-02-28-claude-code-complete-guide/) — 深入掌握 Claude Code 的高效用法
- [CLAUDE.md 终极指南](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — AI 编程助手如何理解项目上下文
- [MCP 协议详解](/posts/ai/2026-02-28-mcp-protocol-explained/) — AI 工具集成的通用标准
- [上下文工程指南](/posts/ai/2026-03-10-context-engineering-guide/) — 系统提示词设计与上下文管理
- [2026 AI 编程 Agent 横评](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/) — 顶级 AI 编程工具对比
- [Vibe Coding 详解](/posts/ai/2026-02-28-vibe-coding-explained/) — 自然语言驱动的 AI 编程
