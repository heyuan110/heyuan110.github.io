+++
date = '2026-03-05T14:00:00+08:00'
draft = false
title = '用 Python 构建 MCP 服务器：完整分步教程'
description = '用 Python 构建 MCP 服务器分步教程：基于 FastMCP 装饰器 API，不到 50 行代码就能跑起一个服务器，要求 Python 3.10+。涵盖工具/资源/提示词三种能力、MCP Inspector 测试、接入 Claude Code 与 SQLite 实战案例。'
toc = true
tags = ['MCP', 'Python', 'Claude Code', 'AI Agent', 'Tutorial']
categories = ['AI Guides']
keywords = ['构建 MCP 服务器 Python', 'MCP 服务器 Python 教程', 'Python MCP 服务器', 'FastMCP 教程', 'Model Context Protocol Python', 'MCP Python SDK', '用 Python 创建 MCP 工具']

[[params.faqItems]]
question = "构建 MCP 服务器需要什么版本的 Python？"
answer = "需要 Python 3.10 或更高版本。MCP Python SDK 官方支持 Python 3.10、3.11、3.12 和 3.13。SDK 使用了类型提示和 match 语句等现代 Python 特性，这些需要 3.10+。"

[[params.faqItems]]
question = "FastMCP 是什么？它和 MCP Python SDK 是什么关系？"
answer = "FastMCP 是官方 MCP Python SDK（PyPI 上的 mcp 包）中包含的高级框架。它提供了基于装饰器的 API 来构建 MCP 服务器——你可以用 @mcp.tool()、@mcp.resource() 和 @mcp.prompt() 来注册能力。这是构建 Python MCP 服务器的推荐方式。"

[[params.faqItems]]
question = "可以用 pip 代替 uv 来安装 MCP Python SDK 吗？"
answer = "可以。使用 pip install mcp[cli] 安装包含 CLI 工具的完整包，或者 pip install mcp 只安装库。不过推荐使用 uv，因为它速度更快，能自动处理虚拟环境，而且是官方 MCP 文档使用的工具。"

[[params.faqItems]]
question = "在连接 Claude Code 之前如何测试 Python MCP 服务器？"
answer = "运行 mcp dev server.py 启动 MCP Inspector，它是一个位于 http://127.0.0.1:6274 的 Web 测试界面。你可以交互式地测试每个工具、资源和提示词。测试通过后，用 claude mcp add 连接到 Claude Code。"

[[params.faqItems]]
question = "用 Python 和 TypeScript 构建 MCP 服务器有什么区别？"
answer = "两种语言都有官方 SDK。Python 使用基于装饰器的注册方式（@mcp.tool()），而 TypeScript 使用方法调用（server.registerTool()）。Python 更适合数据科学、ML 管道和脚本任务。TypeScript 的 SDK 稍微更成熟。协议是完全相同的——任一语言构建的服务器都可以与任何 MCP 客户端配合使用。"
+++

![用 Python 和 FastMCP 分步构建 MCP 服务器教程](cover.webp)

Python 是 AI 开发者最常用的语言，而 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 让构建自定义 MCP 服务器变得非常简单。借助基于装饰器的 FastMCP 框架，你只需不到 50 行代码就能从零开始搭建一个可运行的服务器。

本教程将带你从头开始构建 Python MCP 服务器。你将创建工具、资源和提示词，正确处理错误，使用 MCP Inspector 测试，连接到 Claude Code，并构建一个实用的 SQLite 数据库服务器。所有代码示例都是完整且可运行的。

## 什么是 MCP？为什么要构建自定义服务器

**MCP（Model Context Protocol，模型上下文协议）** 是一个开放标准，它让 AI 模型能够连接到外部工具、数据库和服务。可以把它想象成 AI 的 USB-C——一个通用协议，适用于 Claude Code、Cursor、VS Code Copilot 以及任何兼容 MCP 的客户端。

MCP 服务器暴露三种类型的能力：

| 能力 | 作用 | 示例 |
|------|------|------|
| **工具（Tools）** | 让 AI 执行操作 | 查询数据库、调用 API |
| **资源（Resources）** | 让 AI 读取数据 | 配置文件、日志、系统信息 |
| **提示词（Prompts）** | 可复用的交互模板 | 代码审查模板、分析模板 |

关于 MCP 架构的深入了解，请参阅 [MCP 协议详解：AI 工具的通用标准](/zh/posts/ai/2026-02-28-mcp-protocol-explained/)。如果你已经用 TypeScript 构建过服务器，请参阅 [用 TypeScript 构建 MCP 服务器](/zh/posts/ai/2026-03-02-building-mcp-servers-typescript/) 进行对比。

本教程聚焦于 **Python**——非常适合数据科学工作流、ML 管道以及 Python 已经是你主要语言的脚本任务。

## 前置要求

| 依赖 | 最低版本 | 检查命令 |
|------|----------|----------|
| Python | >= 3.10 | `python3 --version` |
| uv（推荐） | 最新版 | `uv --version` |
| pip（替代） | >= 22.0 | `pip --version` |
| Claude Code | 最新版 | `claude --version` |

### 安装 uv（推荐）

[uv](https://docs.astral.sh/uv/) 是一个快速的 Python 包管理器，能自动处理虚拟环境。MCP 官方文档将其作为默认工具。

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者用 Homebrew
brew install uv

# 验证安装
uv --version
```

如果你更喜欢 pip，本教程中每个 `uv` 命令都会附带对应的 pip 等效命令。

## 项目设置

### 第一步：初始化项目

```bash
# 用 uv 创建项目
uv init weather-mcp-server
cd weather-mcp-server

# 添加带 CLI 工具的 MCP SDK
uv add "mcp[cli]"
```

用 pip 的替代方式：

```bash
mkdir weather-mcp-server
cd weather-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]"
```

### 第二步：配置 pyproject.toml

编辑 `uv init` 创建的 `pyproject.toml`：

```toml
[project]
name = "weather-mcp-server"
version = "1.0.0"
description = "MCP server providing weather data to AI assistants"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
weather-mcp-server = "weather_mcp_server.server:main"
```

`[project.scripts]` 入口点很重要——它让用户在安装包后可以直接作为命令运行你的服务器。

### 第三步：创建项目结构

```bash
mkdir -p src/weather_mcp_server
touch src/weather_mcp_server/__init__.py
touch src/weather_mcp_server/server.py
```

项目布局：

```
weather-mcp-server/
├── pyproject.toml
├── src/
│   └── weather_mcp_server/
│       ├── __init__.py
│       └── server.py       # 主服务器代码
└── README.md
```

## 构建你的第一个服务器：天气工具

打开 `src/weather_mcp_server/server.py`，编写服务器代码：

```python
"""天气 MCP 服务器 - 为 AI 助手提供天气数据。"""

from mcp.server.fastmcp import FastMCP

# 创建 FastMCP 服务器实例
mcp = FastMCP("weather-server")

# 模拟天气数据（在生产环境中替换为真实 API）
WEATHER_DATA = {
    "New York": {"temp_c": 2, "condition": "Cloudy", "humidity": 65, "wind_kmh": 20},
    "San Francisco": {"temp_c": 14, "condition": "Sunny", "humidity": 70, "wind_kmh": 15},
    "London": {"temp_c": 8, "condition": "Rainy", "humidity": 85, "wind_kmh": 25},
    "Tokyo": {"temp_c": 10, "condition": "Clear", "humidity": 55, "wind_kmh": 10},
    "Sydney": {"temp_c": 25, "condition": "Sunny", "humidity": 60, "wind_kmh": 18},
    "Berlin": {"temp_c": 5, "condition": "Overcast", "humidity": 75, "wind_kmh": 22},
}


@mcp.tool()
def get_weather(city: str) -> str:
    """获取指定城市的当前天气。

    Args:
        city: 城市名称，例如 "New York"、"London"、"Tokyo"

    Returns:
        天气报告，包含温度、天气状况、湿度和风速。
    """
    data = WEATHER_DATA.get(city)
    if not data:
        return f"没有 '{city}' 的天气数据。可用城市：{', '.join(WEATHER_DATA.keys())}"

    return (
        f"{city} 的天气：\n"
        f"  温度：{data['temp_c']}°C\n"
        f"  天气：{data['condition']}\n"
        f"  湿度：{data['humidity']}%\n"
        f"  风速：{data['wind_kmh']} km/h"
    )


@mcp.tool()
def compare_weather(city1: str, city2: str) -> str:
    """比较两个城市的天气。

    Args:
        city1: 第一个城市名称
        city2: 第二个城市名称

    Returns:
        两个城市的天气并排对比，包含温差。
    """
    data1 = WEATHER_DATA.get(city1)
    data2 = WEATHER_DATA.get(city2)

    if not data1:
        return f"没有 '{city1}' 的数据。可用城市：{', '.join(WEATHER_DATA.keys())}"
    if not data2:
        return f"没有 '{city2}' 的数据。可用城市：{', '.join(WEATHER_DATA.keys())}"

    diff = data1["temp_c"] - data2["temp_c"]
    warmer = city1 if diff > 0 else city2

    return (
        f"天气对比：{city1} vs {city2}\n"
        f"{'─' * 40}\n"
        f"{city1}：{data1['condition']}，{data1['temp_c']}°C，"
        f"湿度 {data1['humidity']}%，风速 {data1['wind_kmh']} km/h\n"
        f"{city2}：{data2['condition']}，{data2['temp_c']}°C，"
        f"湿度 {data2['humidity']}%，风速 {data2['wind_kmh']} km/h\n"
        f"{'─' * 40}\n"
        f"温差：{abs(diff)}°C（{warmer} 更暖）"
    )


def main():
    """服务器入口点。"""
    mcp.run()


if __name__ == "__main__":
    main()
```

代码中的关键概念：

- **`FastMCP("weather-server")`** 创建服务器实例。名称用于向 MCP 客户端标识你的服务器。
- **`@mcp.tool()`** 将一个函数注册为 MCP 工具。函数的 docstring 会成为工具描述，AI 客户端据此决定何时调用它。
- **类型提示很重要。** SDK 读取 `city: str` 来生成输入 schema。AI 客户端使用此 schema 来构造正确的工具调用。
- **`mcp.run()`** 默认以 STDIO 传输方式启动服务器——这是本地 MCP 服务器的标准方式。

这就是全部所需。没有样板 JSON-RPC 处理，没有手动 schema 定义。FastMCP 从你的函数签名和 docstring 中自动推导一切。

## 添加资源

资源让 AI 客户端可以从你的服务器读取数据。与工具（执行操作）不同，资源用于暴露信息。

将以下代码添加到 `server.py`：

```python
@mcp.resource("weather://cities")
def list_cities() -> str:
    """列出所有有天气数据的城市。

    返回支持的城市名称的 JSON 数组。
    """
    import json
    return json.dumps(list(WEATHER_DATA.keys()), indent=2)


@mcp.resource("weather://city/{city_name}")
def get_city_details(city_name: str) -> str:
    """以 JSON 格式获取指定城市的详细天气数据。

    此资源模板接受 URL 中的任意城市名称。
    """
    import json
    data = WEATHER_DATA.get(city_name)
    if not data:
        return json.dumps({"error": f"未找到城市 '{city_name}'"})
    return json.dumps({"city": city_name, **data}, indent=2)
```

第二个资源使用了**资源模板**——URI 中的 `{city_name}` 是一个动态参数。当客户端请求 `weather://city/Tokyo` 时，FastMCP 会将 `"Tokyo"` 作为 `city_name` 传入。

资源与工具的对比：

| 方面 | 资源 | 工具 |
|------|------|------|
| 用途 | 读取数据 | 执行操作 |
| 类比 | GET 请求 | POST 请求 |
| 副作用 | 无 | 可能有副作用 |
| 发现方式 | 客户端浏览可用资源 | 客户端查看带 schema 的工具列表 |

## 添加提示词

提示词是可复用的交互模板。它们帮助用户（和 AI 客户端）以结构化方式调用服务器的能力。

```python
@mcp.prompt()
def travel_advisory(destination: str) -> str:
    """根据目的地的当前天气获取旅行建议。

    Args:
        destination: 你计划前往的城市
    """
    data = WEATHER_DATA.get(destination)
    if not data:
        return f"请查看 {destination} 的天气状况，并建议合适的穿着和旅行贴士。"

    return (
        f"{destination} 当前天气为 {data['condition']}，"
        f"温度 {data['temp_c']}°C，湿度 {data['humidity']}%，"
        f"风速 {data['wind_kmh']} km/h。\n\n"
        f"根据这些条件，请建议：\n"
        f"1. 适合携带的衣物\n"
        f"2. 天气相关的旅行贴士\n"
        f"3. 户外活动的最佳时段"
    )


@mcp.prompt()
def weather_report(cities: str = "all") -> str:
    """生成全面的天气报告。

    Args:
        cities: 逗号分隔的城市名称，或 "all" 表示所有城市
    """
    if cities == "all":
        city_list = list(WEATHER_DATA.keys())
    else:
        city_list = [c.strip() for c in cities.split(",")]

    city_str = ", ".join(city_list)
    return (
        f"请为以下城市生成专业的天气报告：{city_str}。\n\n"
        f"包含：\n"
        f"- 当前天气概况\n"
        f"- 温度趋势\n"
        f"- 旅行建议\n"
        f"- 天气预警（如有）"
    )
```

提示词是用户主动调用的——它们出现在客户端的提示词库中，可以手动选择。它们不会像工具那样被 AI 自动调用。

## 错误处理与日志最佳实践

生产级 MCP 服务器需要正确的错误处理。以下是有效的模式。

### 返回错误，而非抛出异常

MCP 工具应该将错误信息作为字符串返回，而不是抛出异常。这能让 AI 模型理解出了什么问题。

```python
import httpx

@mcp.tool()
async def fetch_weather_api(city: str) -> str:
    """从外部 API 获取实时天气数据。

    Args:
        city: 要查询的城市名称
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.weatherapi.com/v1/current.json",
                params={"key": "YOUR_API_KEY", "q": city},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()

            current = data["current"]
            return (
                f"{city} 的天气：\n"
                f"  温度：{current['temp_c']}°C\n"
                f"  天气：{current['condition']['text']}\n"
                f"  湿度：{current['humidity']}%\n"
                f"  风速：{current['wind_kph']} km/h"
            )

    except httpx.TimeoutException:
        return f"错误：获取 '{city}' 天气时请求超时。请稍后重试。"
    except httpx.HTTPStatusError as e:
        return f"错误：API 为 '{city}' 返回了状态码 {e.response.status_code}。"
    except Exception as e:
        return f"错误：无法获取 '{city}' 的天气：{str(e)}"
```

### 使用 Context 对象进行日志记录

FastMCP 提供了 `Context` 对象，用于结构化日志记录和进度报告：

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def analyze_weather_trends(city: str, ctx: Context) -> str:
    """分析城市的天气趋势，带进度报告。

    Args:
        city: 要分析的城市名称
    """
    # 日志消息（发送到 MCP 客户端）
    await ctx.info(f"开始分析 {city} 的天气")

    # 报告进度（对长时间运行的操作很有用）
    await ctx.report_progress(0, 3)

    await ctx.debug("正在获取当前数据...")
    data = WEATHER_DATA.get(city)
    if not data:
        await ctx.warning(f"未找到 {city} 的数据")
        return f"没有 '{city}' 的可用数据"

    await ctx.report_progress(1, 3)

    await ctx.debug("正在计算分析结果...")
    # 模拟分析工作
    analysis = f"{city} 的天气分析：{data['condition']} 天气，{data['temp_c']}°C"

    await ctx.report_progress(2, 3)

    await ctx.info(f"{city} 的分析完成")
    await ctx.report_progress(3, 3)

    return analysis
```

Context 对象提供以下日志方法：

| 方法 | 用途 |
|------|------|
| `ctx.debug()` | 详细调试信息 |
| `ctx.info()` | 一般信息 |
| `ctx.warning()` | 警告消息 |
| `ctx.error()` | 错误消息 |
| `ctx.report_progress(current, total)` | 长任务的进度更新 |

### 使用 stderr 进行调试输出

和 TypeScript MCP 服务器一样，**不要用 `print()` 进行调试**。MCP 使用 STDIO 进行通信——stdout 上的任何内容都会被解释为协议消息。

```python
import sys

# 错误方式 - 破坏 STDIO 协议
print("Debug: processing request")

# 正确方式 - 使用 stderr，不会干扰协议
print("Debug: processing request", file=sys.stderr)
```

实际开发中，优先使用 Context 日志方法而非 print 语句。它们通过 MCP 协议向客户端发送结构化日志消息。

## 本地测试服务器

### 使用 MCP Inspector

MCP SDK 包含一个内置测试工具叫 **MCP Inspector**。它启动一个 Web 界面，让你可以交互式地测试每个工具、资源和提示词。

```bash
# 启动 Inspector
mcp dev src/weather_mcp_server/server.py

# 或者用 uv（如果不在激活的 venv 中）
uv run mcp dev src/weather_mcp_server/server.py
```

这会在 `http://127.0.0.1:6274` 打开一个 Web 界面。在那里你可以：

1. **点击 Connect** 建立与服务器的连接
2. **浏览 Tools 标签** — 查看所有注册的工具及其 schema
3. **测试工具** — 填入参数并点击 Execute
4. **浏览 Resources** — 列出并读取所有注册的资源
5. **测试 Prompts** — 选择一个提示词并提供参数

Inspector 是开发过程中的主要调试工具。用它来验证：

- 工具参数是否正确定义
- 返回值格式是否正确
- 错误处理是否按预期工作

### 直接运行服务器

快速测试（不使用 Inspector）：

```bash
# 以 stdio 传输方式运行（默认）
mcp run src/weather_mcp_server/server.py
```

## 连接到 Claude Code

服务器在 Inspector 中测试通过后，将其连接到 Claude Code。

### 注册服务器

```bash
# 使用 uv（推荐 - 自动处理虚拟环境）
claude mcp add weather-server -- uv run --directory /absolute/path/to/weather-mcp-server mcp run src/weather_mcp_server/server.py

# 或者使用 pyproject.toml 中定义的脚本入口点
claude mcp add weather-server -- uv run --directory /absolute/path/to/weather-mcp-server weather-mcp-server
```

如果用 pip 安装到虚拟环境中：

```bash
claude mcp add weather-server /absolute/path/to/weather-mcp-server/.venv/bin/python -m weather_mcp_server.server
```

### 验证和测试

```bash
# 检查服务器是否已注册
claude mcp list
```

现在打开 Claude Code 进行测试：

```
> 东京的天气怎么样？

> 比较一下纽约和伦敦的天气

> 列出天气服务器中所有可用的城市
```

Claude Code 会自动发现你的工具并调用它们。有关 Claude Code 中 MCP 配置的更多详情，请参阅 [Claude Code MCP 设置：将 AI 连接到任何外部服务](/zh/posts/ai/2026-02-28-claude-code-mcp-setup/)。

### 修改代码后重启

修改服务器代码后，需要重启：

```bash
claude mcp remove weather-server
claude mcp add weather-server -- uv run --directory /absolute/path/to/weather-mcp-server mcp run src/weather_mcp_server/server.py
```

## 实战示例：SQLite 数据库服务器

让我们构建一个你在生产中会实际用到的东西——一个让 AI 助手查询 SQLite 数据库的 MCP 服务器。这是自定义 MCP 服务器最常见的用例之一。

创建新文件 `src/weather_mcp_server/db_server.py`：

```python
"""SQLite MCP 服务器 - 让 AI 助手以只读方式访问 SQLite 数据库。"""

import sqlite3
import json
from pathlib import Path
from contextlib import closing

from mcp.server.fastmcp import FastMCP, Context

# 创建服务器
mcp = FastMCP("sqlite-server")

# 数据库路径 - 根据你的项目配置
DB_PATH = Path("./data/example.db")


def get_connection() -> sqlite3.Connection:
    """创建带安全设置的数据库连接。"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # 以字典形式返回行
    conn.execute("PRAGMA journal_mode=WAL")  # 更好的并发读取性能
    return conn


def init_sample_db():
    """创建示例数据库用于演示。"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            owner_id INTEGER REFERENCES users(id),
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            project_id INTEGER REFERENCES projects(id),
            assignee_id INTEGER REFERENCES users(id),
            status TEXT DEFAULT 'todo',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 如果表为空则插入示例数据
        INSERT OR IGNORE INTO users (id, name, email, role) VALUES
            (1, 'Alice Chen', 'alice@example.com', 'admin'),
            (2, 'Bob Smith', 'bob@example.com', 'developer'),
            (3, 'Carol Wu', 'carol@example.com', 'developer'),
            (4, 'Dave Brown', 'dave@example.com', 'designer');

        INSERT OR IGNORE INTO projects (id, name, description, owner_id, status) VALUES
            (1, 'MCP Server', 'Build custom MCP servers', 1, 'active'),
            (2, 'Web Dashboard', 'Admin dashboard redesign', 4, 'active'),
            (3, 'API Migration', 'Migrate REST to GraphQL', 2, 'completed');

        INSERT OR IGNORE INTO tasks (id, title, project_id, assignee_id, status, priority) VALUES
            (1, 'Set up project structure', 1, 1, 'done', 'high'),
            (2, 'Implement weather tool', 1, 2, 'in_progress', 'high'),
            (3, 'Write unit tests', 1, 3, 'todo', 'medium'),
            (4, 'Design dashboard layout', 2, 4, 'in_progress', 'high'),
            (5, 'Implement auth flow', 2, 2, 'todo', 'high'),
            (6, 'Write API docs', 3, 3, 'done', 'low'),
            (7, 'Performance optimization', 1, 2, 'todo', 'medium');
    """)

    conn.commit()
    conn.close()


@mcp.tool()
def query_database(sql: str) -> str:
    """对数据库执行只读 SQL 查询。

    仅允许 SELECT 语句。查询在只读事务中运行以防止任何数据修改。

    Args:
        sql: 要执行的 SELECT SQL 查询

    Returns:
        格式化的 JSON 字符串形式的查询结果，或错误消息。
    """
    # 安全性：仅允许 SELECT 语句
    normalized = sql.strip().upper()
    if not normalized.startswith("SELECT"):
        return "错误：仅允许 SELECT 查询。此服务器提供只读访问。"

    # 阻止危险关键字（包括子查询中的）
    dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "EXEC"]
    for keyword in dangerous_keywords:
        if keyword in normalized:
            return f"错误：不允许 '{keyword}' 语句。"

    try:
        with closing(get_connection()) as conn:
            cursor = conn.execute(sql)
            columns = [description[0] for description in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return json.dumps({
                "columns": columns,
                "row_count": len(rows),
                "rows": rows,
            }, indent=2, default=str)

    except sqlite3.OperationalError as e:
        return f"SQL 错误：{str(e)}"
    except Exception as e:
        return f"执行查询时出错：{str(e)}"


@mcp.tool()
def list_tables() -> str:
    """列出数据库中所有表及其列定义。

    Returns:
        每个表及其列的格式化描述。
    """
    try:
        with closing(get_connection()) as conn:
            # 获取所有表名
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]

            result = []
            for table in tables:
                # 获取每个表的列信息
                cursor = conn.execute(f"PRAGMA table_info({table})")
                columns = []
                for col in cursor.fetchall():
                    col_name = col[1]
                    col_type = col[2]
                    not_null = "NOT NULL" if col[3] else ""
                    pk = "PRIMARY KEY" if col[5] else ""
                    columns.append(f"    {col_name} {col_type} {pk} {not_null}".strip())

                # 获取行数
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]

                result.append(
                    f"表：{table}（{row_count} 行）\n" +
                    "\n".join(columns)
                )

            return "\n\n".join(result)

    except Exception as e:
        return f"列出表时出错：{str(e)}"


@mcp.tool()
async def describe_table(table_name: str, ctx: Context) -> str:
    """获取指定表的详细 schema 和示例数据。

    Args:
        table_name: 要描述的表名

    Returns:
        表 schema、示例行和基本统计信息。
    """
    await ctx.info(f"正在描述表：{table_name}")

    try:
        with closing(get_connection()) as conn:
            # 验证表是否存在
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if not cursor.fetchone():
                return f"错误：表 '{table_name}' 不存在。"

            # 获取 schema
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            schema_lines = [f"'{table_name}' 的 Schema："]
            for col in columns:
                schema_lines.append(
                    f"  {col[1]} ({col[2]})"
                    + (" PRIMARY KEY" if col[5] else "")
                    + (" NOT NULL" if col[3] else "")
                    + (f" DEFAULT {col[4]}" if col[4] else "")
                )

            # 获取行数
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            # 获取示例行（前 5 行）
            cursor = conn.execute(f"SELECT * FROM {table_name} LIMIT 5")
            col_names = [desc[0] for desc in cursor.description]
            sample_rows = [dict(zip(col_names, row)) for row in cursor.fetchall()]

            result = "\n".join(schema_lines)
            result += f"\n\n总行数：{count}"
            result += f"\n\n示例数据（前 5 行）：\n{json.dumps(sample_rows, indent=2, default=str)}"

            return result

    except Exception as e:
        return f"描述表时出错：{str(e)}"


@mcp.resource("db://schema")
def get_full_schema() -> str:
    """以资源形式获取完整的数据库 schema。

    这对于需要在编写查询前了解数据库结构的 AI 助手很有用。
    """
    try:
        with closing(get_connection()) as conn:
            cursor = conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
            )
            statements = [row[0] for row in cursor.fetchall()]
            return "\n\n".join(statements)
    except Exception as e:
        return f"错误：{str(e)}"


@mcp.prompt()
def data_analysis(question: str) -> str:
    """根据数据库 schema 生成数据分析提示词。

    Args:
        question: 你想回答的数据问题
    """
    schema = get_full_schema()
    return (
        f"你可以访问一个具有以下 schema 的 SQLite 数据库：\n\n"
        f"{schema}\n\n"
        f"用户想知道：{question}\n\n"
        f"请使用 query_database 工具编写并执行合适的 SQL 查询，"
        f"然后清楚地解释结果。"
    )


def main():
    """初始化示例数据库并启动服务器。"""
    init_sample_db()
    mcp.run()


if __name__ == "__main__":
    main()
```

### 测试数据库服务器

```bash
# 使用 MCP Inspector 测试
mcp dev src/weather_mcp_server/db_server.py
```

连接到 Claude Code：

```bash
claude mcp add sqlite-server -- uv run --directory /absolute/path/to/weather-mcp-server python src/weather_mcp_server/db_server.py
```

现在你可以用自然语言向 Claude Code 提问关于数据的问题：

```
> 数据库里有哪些表？

> 显示所有活跃的项目及其负责人

> 每个开发者有多少任务？按状态分组

> 找出所有未完成的高优先级任务
```

AI 会编写 SQL 查询，调用你的 `query_database` 工具，并呈现结果——全部自动完成。

这个模式适用于任何 SQLite 数据库。将 `DB_PATH` 指向你项目的数据库文件，Claude Code 就能立即获得查询能力。关于通过 MCP 暴露数据库的安全最佳实践，请参阅 [MCP 安全指南](/zh/posts/ai/2026-02-23-mcp-security-guide/)。

## 部署选项

### 本地 STDIO（默认）

本地开发的标准传输方式。服务器作为子进程运行，通过 stdin/stdout 通信。

```python
# 这是调用 mcp.run() 时的默认方式
mcp.run()

# 显式指定 stdio 传输
mcp.run(transport="stdio")
```

这是 Claude Code 和大多数本地客户端使用的方式。无需网络配置。

### SSE 用于远程访问

Server-Sent Events 传输方式支持通过 HTTP 进行远程连接：

```python
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

从 Claude Code 通过网络连接：

```bash
claude mcp add remote-weather --url http://your-server:8000/sse
```

### Streamable HTTP（最新）

最新的传输选项——支持流式的双向 HTTP：

```python
mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

Streamable HTTP 是生产环境远程部署的推荐传输方式。它支持双向通信，并能通过标准 HTTP 代理和负载均衡器工作。

### Docker 部署

对于生产服务器，Docker 提供隔离性和可重现性：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装 uv 以快速解析依赖
RUN pip install uv

# 复制项目文件
COPY pyproject.toml .
COPY src/ ./src/

# 安装依赖
RUN uv pip install --system -e .

# 以 streamable-http 传输方式运行用于远程访问
EXPOSE 8000
CMD ["python", "-m", "weather_mcp_server.server"]
```

修改服务器以在生产环境中使用适当的传输方式：

```python
import os

def main():
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "stdio":
        mcp.run()
    else:
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("MCP_PORT", "8000")),
        )
```

## 发布到 MCP 生态系统

当你的服务器准备好供他人使用时，可以发布它。

### 发布到 PyPI

```bash
# 构建包
uv build

# 发布到 PyPI
uv publish
```

发布后，任何人都可以使用你的服务器：

```bash
# 用户使用 uvx（uv 的工具运行器）安装并运行
claude mcp add weather-server -- uvx weather-mcp-server

# 或者用 pip
pip install weather-mcp-server
claude mcp add weather-server weather-mcp-server
```

### 与社区分享

将你的服务器提交到 [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) 仓库和 [MCP 官方服务器注册表](https://modelcontextprotocol.io/examples)。查看 [Claude Code 最佳 MCP 服务器](/zh/posts/ai/2026-03-05-best-mcp-servers-claude-code/) 了解文档规范的 MCP 服务器列表是什么样的。

## 常见错误与解决方案

| 症状 | 原因 | 解决方案 |
|------|------|----------|
| 服务器无法启动 | Python < 3.10 | 升级到 Python 3.10+ |
| `ModuleNotFoundError: mcp` | SDK 未安装在正确的环境中 | 运行 `uv add "mcp[cli]"` 或激活 venv |
| 工具未被发现 | 函数参数缺少类型提示 | 添加类型提示：`def my_tool(name: str)` |
| `print()` 破坏协议 | stdout 被用于调试 | 使用 `print(..., file=sys.stderr)` 或 `ctx.info()` |
| 服务器静默崩溃 | 工具中有未处理的异常 | 用 try/except 包装并返回错误字符串 |
| 资源未找到 | URI scheme 错误 | 检查 URI 完全匹配，例如 `weather://cities` |
| 连接被拒绝 | 服务器未运行或路径错误 | 用 `claude mcp list` 验证并检查路径 |
| 代码修改后工具过时 | 服务器需要重启 | 先 `claude mcp remove` 再重新 `claude mcp add` |

## 常见问题

### 构建 MCP 服务器需要什么版本的 Python？

需要 Python 3.10 或更高版本。MCP Python SDK 官方支持 Python 3.10、3.11、3.12 和 3.13。SDK 使用了类型提示和 match 语句等现代 Python 特性，这些需要 3.10+。

### FastMCP 是什么？它和 MCP Python SDK 是什么关系？

FastMCP 是官方 MCP Python SDK（PyPI 上的 `mcp` 包）中包含的高级框架。它提供了基于装饰器的 API 来构建 MCP 服务器——你可以用 `@mcp.tool()`、`@mcp.resource()` 和 `@mcp.prompt()` 来注册能力。这是构建 Python MCP 服务器的推荐方式。

### 可以用 pip 代替 uv 来安装 MCP Python SDK 吗？

可以。使用 `pip install "mcp[cli]"` 安装包含 CLI 工具的完整包，或者 `pip install mcp` 只安装库。不过推荐使用 uv，因为它速度更快，能自动处理虚拟环境，而且是官方 MCP 文档使用的工具。

### 在连接 Claude Code 之前如何测试 Python MCP 服务器？

运行 `mcp dev server.py` 启动 MCP Inspector，它是一个位于 `http://127.0.0.1:6274` 的 Web 测试界面。你可以交互式地测试每个工具、资源和提示词。测试通过后，用 `claude mcp add` 连接到 Claude Code。

### 用 Python 和 TypeScript 构建 MCP 服务器有什么区别？

两种语言都有官方 SDK。Python 使用基于装饰器的注册方式（`@mcp.tool()`），而 TypeScript 使用方法调用（`server.registerTool()`）。Python 更适合数据科学、ML 管道和脚本任务。TypeScript 的 SDK 稍微更成熟。协议是完全相同的——任一语言构建的服务器都可以与任何 MCP 客户端配合使用。

## 总结

用 Python 构建 MCP 服务器遵循一个清晰的工作流：

1. **设置** — `uv init` + `uv add "mcp[cli]"` + 创建 `pyproject.toml`
2. **构建工具** — 使用 `@mcp.tool()` 配合类型参数和 docstring
3. **添加资源** — 使用 `@mcp.resource()` 提供只读数据访问
4. **添加提示词** — 使用 `@mcp.prompt()` 创建可复用模板
5. **测试** — `mcp dev server.py` 启动 MCP Inspector
6. **连接** — `claude mcp add` 将服务器注册到 Claude Code
7. **部署** — 本地用 STDIO，远程用 streamable-http，生产用 Docker
8. **发布** — `uv build` + `uv publish` 到 PyPI

MCP 生态系统正在快速增长——仅 Python SDK 每月下载量就达数百万次。你构建的每个服务器都能立即与 Claude Code、Cursor、VS Code Copilot 以及未来任何兼容 MCP 的工具一起使用。现在就开始构建吧。

## 相关阅读

- [MCP 协议详解：AI 工具的通用标准](/zh/posts/ai/2026-02-28-mcp-protocol-explained/) — 深入了解 MCP 架构和概念
- [用 TypeScript 构建 MCP 服务器：从零到部署教程](/zh/posts/ai/2026-03-02-building-mcp-servers-typescript/) — 本教程的 TypeScript 版本
- [Claude Code MCP 设置：将 AI 连接到任何外部服务](/zh/posts/ai/2026-02-28-claude-code-mcp-setup/) — Claude Code 中 MCP 配置的完整指南
- [Claude Code 最佳 MCP 服务器：2026 年必备的 18 个工具](/zh/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — 精选的最佳社区 MCP 服务器列表
