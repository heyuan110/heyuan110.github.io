+++
date = '2026-02-28T09:00:00+08:00'
draft = false
title = 'Claude Code MCP 配置指南：让 AI 连接任何外部服务'
description = '完整的 MCP Server 配置教程——安装社区服务器、用 TypeScript 从零构建自定义服务器，以及高效调试技巧。'
toc = true
tags = ['Claude Code', 'MCP', 'TypeScript', 'Tutorial']
categories = ['AI Guides']
keywords = ['Claude Code MCP 配置', 'MCP 服务器教程', 'Model Context Protocol', 'MCP TypeScript 教程', '构建 MCP 服务器', 'Claude Code 扩展']
+++

![Claude Code MCP 配置——将 AI 连接到外部服务](cover.webp)

开箱即用的 Claude Code 可以读取文件、运行 Shell 命令和搜索代码。但如果你需要它查询 Postgres 数据库、发送 Slack 消息，或者调用公司内部 API 呢？

这正是 MCP 要解决的问题。**[Model Context Protocol（模型上下文协议）](https://modelcontextprotocol.io)** 是一个开放标准，让你可以将任何外部服务接入 Claude Code——无需 prompt 黑魔法、无需手动复制粘贴数据、无需脆弱的临时方案。你可以把它理解为 **AI 的 USB-C**：一个通用连接器，连接你的 AI 助手和所有你需要的工具。

本指南涵盖了从安装第一个社区 MCP 服务器到用 TypeScript 从零构建自定义服务器的全部内容。读完之后，你将掌握如何让 Claude Code 与任何东西对话。

> **前置条件**：你需要已经安装并配置好 Claude Code。如果还没有，请先参考我们的 [Claude Code 安装指南](/posts/ai/2026-02-25-claude-code-setup-guide/)。

## MCP 是什么？60 秒搞懂架构

MCP 全称 **Model Context Protocol（模型上下文协议）**。Anthropic 于 2024 年末将其作为开放规范发布，此后它已成为扩展 AI 编程工具的标准方式。

架构如下：

```
┌─────────────────────────────────────────────────────┐
│              MCP 客户端（宿主）                        │
│     Claude Code / Cursor / VS Code Copilot          │
├─────────────────────────────────────────────────────┤
│              MCP 协议层                              │
│           JSON-RPC 2.0 over STDIO 或 HTTP            │
├─────────────────────────────────────────────────────┤
│              MCP 服务器                              │
│      你的自定义工具、数据源、提示词模板                  │
└─────────────────────────────────────────────────────┘
```

**客户端**（Claude Code）发送请求。**服务器**（你的代码或社区包）处理请求。**协议**定义了它们之间的消息格式。

一个 MCP 服务器可以暴露三种能力：

| 能力 | 作用 | 示例 |
|------|------|------|
| **Tools（工具）** | 让 AI 执行操作 | 查询数据库、发送通知、创建 GitHub Issue |
| **Resources（资源）** | 让 AI 读取数据 | 配置文件、用户资料、API 文档 |
| **Prompts（提示词）** | 预定义的交互模板 | 代码审查清单、Bug 报告格式、部署摘要 |

**Tools** 是最常用的能力。当 Claude Code 询问"我可以调用 `query_database` 工具吗？"时，这个工具就是由 MCP 服务器提供的。

### 为什么不直接用 Shell 命令？

你可能会想：Claude Code 已经可以运行 Shell 命令了，为什么还要用 MCP？

三个原因：

1. **安全性**。MCP 工具有明确的 schema。Claude 精确知道一个工具接受哪些参数，而不是构造任意的 Shell 命令。
2. **可发现性**。Claude 自动看到所有可用的 MCP 工具，并知道何时使用它们。无需在 prompt 中解释"你可以用 `curl` 调用我们的 API"。
3. **可复用性**。一个 MCP 服务器可以在所有兼容 MCP 的客户端中使用——Claude Code、Cursor、Windsurf 等等。一次编写，到处使用。

## 安装社区 MCP 服务器

最快的入门方式是安装别人已经构建好的服务器。社区已经为 GitHub、Slack、PostgreSQL、文件系统操作等数十个服务创建了 [MCP 服务器](https://github.com/modelcontextprotocol/servers)。

### `claude mcp add` 命令

向 Claude Code 添加 MCP 服务器只需一条命令：

```bash
claude mcp add <名称> <命令> [参数...]
```

例如，添加官方的文件系统 MCP 服务器：

```bash
claude mcp add filesystem npx @anthropic/mcp-filesystem /path/to/allowed/directory
```

这告诉 Claude Code："有一个叫 `filesystem` 的 MCP 服务器。通过运行 `npx @anthropic/mcp-filesystem /path/to/allowed/directory` 来启动它。"

### 常用社区 MCP 服务器

以下是你现在就可以安装的最实用的 MCP 服务器：

#### GitHub（官方）

```bash
claude mcp add github npx @anthropic/mcp-github
```

让 Claude Code 能够创建 Issue、开 Pull Request、搜索仓库和管理分支——完全不用切换到浏览器。

**必需**：设置 `GITHUB_TOKEN` 环境变量：

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

或者内联传递：

```bash
claude mcp add github -e GITHUB_TOKEN=ghp_your_token_here npx @anthropic/mcp-github
```

#### Slack

```bash
claude mcp add slack npx @anthropic/mcp-slack
```

让 Claude Code 读取和发送 Slack 消息、搜索频道、发布更新。当长时间运行的任务完成时，自动通知非常有用。（配合 [Claude Code Hooks](/posts/ai/2026-02-18-claude-code-hooks-guide/) 可实现完整自动化。）

**必需**：设置 `SLACK_BOT_TOKEN` 和 `SLACK_TEAM_ID`。

#### PostgreSQL

```bash
claude mcp add postgres npx @anthropic/mcp-postgres "postgresql://user:pass@localhost:5432/mydb"
```

Claude 现在可以直接查询你的数据库。它能看到你的 schema、编写 SQL 并返回结果。对于调试数据问题或生成报告非常有用。

#### 文件系统（扩展版）

```bash
claude mcp add filesystem npx @anthropic/mcp-filesystem /Users/you/projects
```

虽然 Claude Code 本身已有内置的文件访问功能，但文件系统 MCP 服务器提供了额外的操作，如目录树可视化、文件监听和高级搜索。

#### Context7（文档查询）

```bash
claude mcp add context7 npx @anthropic/mcp-context7
```

在查询时获取最新的库文档。当 Claude 需要使用它不确定的库 API 时，Context7 会拉取最新文档，而不是依赖训练数据。

### 作用域选项：项目级 vs 用户级

默认情况下，`claude mcp add` 将服务器添加到**项目**作用域——它仅在当前目录下可用。

你可以更改作用域：

```bash
# 在所有项目中可用（用户作用域）
claude mcp add --scope user github npx @anthropic/mcp-github

# 仅在当前项目中可用（项目作用域——默认）
claude mcp add --scope project postgres npx @anthropic/mcp-postgres "postgresql://..."
```

**最佳实践**：对项目特定的服务器（数据库、项目 API）使用**项目作用域**，对通用工具（GitHub、Slack、文件系统）使用**用户作用域**。

## 管理 MCP 服务器

### 列出所有已配置的服务器

```bash
claude mcp list
```

输出如下：

```
Project servers:
  postgres: npx @anthropic/mcp-postgres postgresql://user:pass@localhost:5432/mydb

User servers:
  github: npx @anthropic/mcp-github
  slack: npx @anthropic/mcp-slack
```

### 移除服务器

```bash
claude mcp remove <名称>
```

例如：

```bash
claude mcp remove postgres
```

### 在 Claude Code 中检查服务器状态

在 Claude Code 会话中，你可以验证 MCP 服务器是否已连接：

```
/mcp
```

这个斜杠命令会显示所有已配置 MCP 服务器的状态，包括它们是否正在运行以及暴露了哪些工具。

### 更新服务器

通过 npm 分发的社区 MCP 服务器在你使用 `npx` 运行时会自动更新（它总是获取最新版本）。如果你需要特定版本：

```bash
claude mcp add github npx @anthropic/mcp-github@2.1.0
```

## 从零构建你自己的 MCP 服务器（TypeScript）

社区服务器涵盖了常见用例。但 MCP 的真正威力在于构建针对你特定工作流的服务器。让我们一步步来构建一个。

我们将创建一个**天气服务** MCP 服务器——简单到可以快速理解，同时展示你在实际项目中需要的所有模式。

### 第 1 步：初始化项目

```bash
mkdir mcp-weather-server
cd mcp-weather-server
npm init -y
```

安装 MCP SDK 和 Zod（用于输入验证）：

```bash
npm install @modelcontextprotocol/server zod
npm install -D typescript @types/node
```

### 第 2 步：配置 TypeScript 和 package.json

创建 `tsconfig.json`：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

更新 `package.json`——关键部分如下：

```json
{
  "name": "mcp-weather-server",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "mcp-weather-server": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

**重要**：你必须设置 `"type": "module"`。MCP SDK 使用 ES 模块，没有这个设置你会遇到晦涩的导入错误。

### 第 3 步：编写服务器代码

创建 `src/index.ts`：

```typescript
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio.js";
import { z } from "zod";

// 创建 MCP 服务器
const server = new McpServer({
  name: "weather-server",
  version: "1.0.0",
});

// 定义工具：获取当前天气
server.registerTool(
  "get_weather",
  {
    title: "Get Weather",
    description: "Get the current weather for a city",
    inputSchema: {
      city: z.string().describe("City name, e.g. 'Tokyo' or 'New York'"),
      units: z
        .enum(["celsius", "fahrenheit"])
        .default("celsius")
        .describe("Temperature units"),
    },
  },
  async ({ city, units }) => {
    // 在实际服务器中，你会在这里调用天气 API
    // 本示例返回模拟数据
    const temperature = units === "celsius" ? 22 : 72;
    const unitLabel = units === "celsius" ? "C" : "F";

    // 重要：日志输出必须使用 console.error，绝不要用 console.log
    console.error(`Fetching weather for ${city}...`);

    return {
      content: [
        {
          type: "text" as const,
          text: JSON.stringify(
            {
              city,
              temperature: `${temperature} ${unitLabel}`,
              condition: "Partly cloudy",
              humidity: "65%",
              wind: "12 km/h NW",
            },
            null,
            2
          ),
        },
      ],
    };
  }
);

// 使用 STDIO 传输层启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP server is running");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

拆解一下关键部分：

- **`McpServer`**：SDK 的主服务器类。
- **`registerTool()`**：注册一个工具，包含名称、schema 和处理函数。
- **`inputSchema` 配合 Zod**：定义工具接受的参数、类型和描述。Claude 通过读取这些描述来理解如何使用工具。
- **`StdioServerTransport`**：通过 stdin/stdout 通信。这是 Claude Code 对本地 MCP 服务器的预期方式。
- **`console.error` 输出日志**：这一点至关重要。Stdout 是 MCP 协议通道。如果你使用 `console.log`，你的日志消息会破坏 JSON-RPC 消息并导致服务器崩溃。

### 第 4 步：构建和测试

编译 TypeScript：

```bash
npm run build
```

使入口文件可执行：

```bash
chmod +x dist/index.js
```

将服务器注册到 Claude Code：

```bash
claude mcp add weather node /absolute/path/to/mcp-weather-server/dist/index.js
```

**重要**：使用 `dist/index.js` 的绝对路径，不要用相对路径。

现在启动 Claude Code 试试：

```
东京现在天气怎么样？
```

Claude Code 应该会自动识别到 `get_weather` 工具并调用它。

### 第 5 步：添加资源（Resources）

Resources 让 Claude 可以从你的服务器读取数据，而无需调用工具。它们适合用于配置、文档或任何 Claude 可能需要作为上下文的数据。

在 `src/index.ts` 中的 `main()` 函数之前添加以下代码：

```typescript
// 定义资源：支持的城市列表
server.resource("supported-cities", "weather://cities", async (uri) => {
  return {
    contents: [
      {
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify([
          "Tokyo",
          "New York",
          "London",
          "Paris",
          "Sydney",
          "Berlin",
          "Singapore",
        ]),
      },
    ],
  };
});
```

重新构建后（`npm run build`），Claude Code 可以在进行天气查询之前读取支持的城市列表作为上下文。

### 第 6 步：添加提示词模板（Prompts）

Prompts 是预定义的交互模板。当你希望 Claude 遵循特定格式时非常有用。

```typescript
// 定义提示词模板：天气简报
server.prompt(
  "daily-briefing",
  { city: z.string().describe("City for the weather briefing") },
  ({ city }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Generate a morning weather briefing for ${city}. Include:
1. Current conditions
2. High/low temperatures for the day
3. Chance of rain
4. Recommendation for what to wear

Keep it concise and friendly.`,
        },
      },
    ],
  })
);
```

现在当用户调用 `/mcp` 并选择 `daily-briefing` 提示词时，Claude Code 将按照指定格式生成天气简报。

## 调试 MCP 服务器

MCP 服务器通过 stdio 通信，这使得调试方式与典型的 Web 服务器不同。以下是有效的调试技巧。

### 黄金法则：用 console.error，不要用 console.log

这是最常见的 MCP 服务器 Bug，值得反复强调：

```typescript
// 错误 - 这会破坏 JSON-RPC 协议通道
console.log("Processing request...");

// 正确 - 这会输出到 stderr，是安全的
console.error("Processing request...");
```

当你使用 `console.log` 时，你的消息会混入 stdout 上的 JSON-RPC 消息中。MCP 客户端收到了垃圾数据，服务器就会崩溃并给出一个毫无帮助的错误。

### 启用 SDK 调试日志

设置 `MCP_DEBUG` 环境变量来查看协议级消息：

```bash
MCP_DEBUG=1 node dist/index.js
```

或者在注册到 Claude Code 时：

```bash
claude mcp add weather -e MCP_DEBUG=1 node /path/to/dist/index.js
```

### 常见错误及修复

| 错误 | 原因 | 修复方法 |
|------|------|----------|
| `SyntaxError: Cannot use import statement` | package.json 中缺少 `"type": "module"` | 在 package.json 中添加 `"type": "module"` |
| `ERR_MODULE_NOT_FOUND` | 导入路径错误 | 即使是 TypeScript 文件，导入时也要使用 `.js` 扩展名 |
| 服务器启动了但没有工具出现 | `registerTool()` 在 `connect()` 之后才调用 | 在调用 `server.connect()` 之前注册所有工具 |
| 客户端报 `Unexpected token` | 使用了 `console.log` 而不是 `console.error` | 将所有 `console.log` 替换为 `console.error` |
| 服务器超时 | 长时间运行的操作没有进度反馈 | 添加超时和进度回调 |
| 启动服务器时报 `ENOENT` | `claude mcp add` 中的路径错误 | 使用构建后 JS 文件的绝对路径 |
| 工具出现了但静默失败 | 处理函数抛出了未捕获的错误 | 用 try/catch 包裹处理函数并使用 `console.error` |

### 无需 Claude Code 的独立测试

你可以使用 MCP Inspector 手动测试你的 MCP 服务器：

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

这会打开一个 Web UI，你可以浏览工具、用测试输入调用它们，并查看原始的 JSON-RPC 消息。在连接到 Claude Code 之前进行调试非常有价值。

### 在 Claude Code 中查看服务器日志

当 Claude Code 运行时，MCP 服务器的 stderr 输出会存到 Claude Code 的日志目录：

```bash
# macOS
ls ~/Library/Logs/Claude\ Code/mcp*.log

# Linux
ls ~/.local/share/claude-code/logs/mcp*.log
```

## 发布你的 MCP 服务器

服务器工作正常后，你可能想与他人分享。

### 发布到 npm

1. 确保 `package.json` 有正确的 `name`、`version`、`bin` 和 `description` 字段：

```json
{
  "name": "mcp-weather-server",
  "version": "1.0.0",
  "description": "MCP server that provides weather data",
  "type": "module",
  "bin": {
    "mcp-weather-server": "./dist/index.js"
  },
  "files": ["dist"],
  "keywords": ["mcp", "mcp-server", "weather"]
}
```

2. 构建并发布：

```bash
npm run build
npm publish
```

3. 现在任何人都可以使用你的服务器了：

```bash
claude mcp add weather npx mcp-weather-server
```

### 在 awesome-mcp-servers 上列出

[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) 仓库是 MCP 服务器的社区索引。提交 Pull Request 即可添加你的服务器。

### 私有分发

对于公司内部服务器，可以发布到私有 npm 仓库或通过 Git 分发：

```bash
# 从私有 Git 仓库安装
claude mcp add internal-tools npx github:your-org/internal-mcp-tools
```

## 实战 MCP 模式

天气示例教的是基础。以下是生产级 MCP 服务器的设计模式。

### 模式 1：数据库查询服务器

让 Claude 安全查询你的数据库：

```typescript
import { McpServer } from "@modelcontextprotocol/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio.js";
import { z } from "zod";
import pg from "pg";

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
});

const server = new McpServer({
  name: "db-query-server",
  version: "1.0.0",
});

server.registerTool(
  "query_database",
  {
    title: "Query Database",
    description: "Run a read-only SQL query against the database",
    inputSchema: {
      sql: z.string().describe("SQL query to execute (SELECT only)"),
    },
  },
  async ({ sql }) => {
    // 安全措施：只允许 SELECT 查询
    const normalized = sql.trim().toUpperCase();
    if (!normalized.startsWith("SELECT")) {
      return {
        content: [
          {
            type: "text" as const,
            text: "Error: Only SELECT queries are allowed",
          },
        ],
        isError: true,
      };
    }

    try {
      const result = await pool.query(sql);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(result.rows, null, 2),
          },
        ],
      };
    } catch (error) {
      console.error("Query failed:", error);
      return {
        content: [
          {
            type: "text" as const,
            text: `Query error: ${(error as Error).message}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// 将 schema 作为资源暴露，让 Claude 理解数据库结构
server.resource("schema", "db://schema", async (uri) => {
  const result = await pool.query(`
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position
  `);
  return {
    contents: [
      {
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify(result.rows, null, 2),
      },
    ],
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

**关键洞察**：将数据库 schema 作为 Resource 暴露，意味着 Claude 自动理解你的表结构，无需每次会话都解释。这显著提高了查询准确性。

### 模式 2：API 封装服务器

将公司内部 API 封装为 MCP 服务器：

```typescript
server.registerTool(
  "get_customer",
  {
    title: "Get Customer",
    description: "Look up a customer by ID or email",
    inputSchema: {
      identifier: z
        .string()
        .describe("Customer ID (cust_xxx) or email address"),
    },
  },
  async ({ identifier }) => {
    const isEmail = identifier.includes("@");
    const endpoint = isEmail
      ? `/api/customers?email=${encodeURIComponent(identifier)}`
      : `/api/customers/${identifier}`;

    const response = await fetch(`${process.env.API_BASE_URL}${endpoint}`, {
      headers: {
        Authorization: `Bearer ${process.env.API_TOKEN}`,
      },
    });

    if (!response.ok) {
      return {
        content: [
          {
            type: "text" as const,
            text: `API error: ${response.status} ${response.statusText}`,
          },
        ],
        isError: true,
      };
    }

    const customer = await response.json();
    return {
      content: [
        {
          type: "text" as const,
          text: JSON.stringify(customer, null, 2),
        },
      ],
    };
  }
);
```

**小技巧**：注册时使用 `-e` 标志注入 API 凭据：

```bash
claude mcp add customer-api \
  -e API_BASE_URL=https://api.internal.company.com \
  -e API_TOKEN=your_token_here \
  node /path/to/dist/index.js
```

### 模式 3：多工具服务器

实际的服务器通常暴露多个相关工具。将相关功能组合到一个服务器中：

```typescript
const server = new McpServer({
  name: "project-management",
  version: "1.0.0",
});

// 工具 1：列出任务
server.registerTool(
  "list_tasks",
  {
    title: "List Tasks",
    description: "List tasks from the project board, optionally filtered",
    inputSchema: {
      status: z
        .enum(["todo", "in_progress", "done"])
        .optional()
        .describe("Filter by status"),
      assignee: z
        .string()
        .optional()
        .describe("Filter by assignee username"),
    },
  },
  async ({ status, assignee }) => {
    // 实现代码
  }
);

// 工具 2：创建任务
server.registerTool(
  "create_task",
  {
    title: "Create Task",
    description: "Create a new task on the project board",
    inputSchema: {
      title: z.string().describe("Task title"),
      description: z.string().optional().describe("Task description"),
      assignee: z.string().optional().describe("Username to assign to"),
      priority: z
        .enum(["low", "medium", "high", "critical"])
        .default("medium")
        .describe("Task priority"),
    },
  },
  async ({ title, description, assignee, priority }) => {
    // 实现代码
  }
);

// 工具 3：更新任务状态
server.registerTool(
  "update_task_status",
  {
    title: "Update Task Status",
    description: "Change the status of an existing task",
    inputSchema: {
      taskId: z.string().describe("Task ID"),
      status: z
        .enum(["todo", "in_progress", "done"])
        .describe("New status"),
    },
  },
  async ({ taskId, status }) => {
    // 实现代码
  }
);
```

**设计原则**：将共享相同认证、数据源或领域的工具分组。不要每个工具创建一个服务器——那会浪费资源。也不要把不相关的工具放在一起——那会增加维护难度。

## 将 MCP 与 CLAUDE.md 和 Hooks 结合使用

当 MCP 服务器与其他 Claude Code 功能结合时，会变得更加强大。

### MCP + CLAUDE.md

在你的 [CLAUDE.md 文件](/posts/ai/2026-02-28-claude-code-claudemd-guide/)中，你可以告诉 Claude 何时以及如何使用特定的 MCP 工具：

```markdown
## MCP Tools

- Use the `query_database` tool to check data before making schema changes
- Always use `get_customer` to verify customer data instead of guessing
- After completing a task, use `send_slack_message` to notify #dev-updates
```

这为 Claude 在不同情况下该使用哪些工具提供了明确指导。

### MCP + Hooks

[Claude Code Hooks](/posts/ai/2026-02-18-claude-code-hooks-guide/) 可以围绕 MCP 工具使用实现自动化操作。例如，你可以设置一个 Hook 来记录每次 MCP 工具调用，用于审计：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__*",
        "command": "echo \"$(date): Tool $CLAUDE_TOOL_NAME called\" >> ~/.claude/mcp-audit.log"
      }
    ]
  }
}
```

## 避免常见 MCP 错误的技巧

如果你是 Claude Code 新手，你可能会觉得我们的 [10 个常见 Claude Code 错误](/posts/ai/2026-02-25-claude-code-mistakes/)清单很有帮助。以下是 MCP 相关的常见坑：

1. **使用 `console.log` 而不是 `console.error`**。这是 MCP 服务器崩溃的第一大原因。Stdout 是为 JSON-RPC 协议消息保留的。你所有的调试输出必须通过 `console.error` 发送到 stderr。

2. **忘记在 package.json 中设置 `"type": "module"`**。MCP SDK 使用 ES 模块导入。没有这个设置，Node.js 会尝试 CommonJS 解析并报出令人困惑的错误。

3. **在 `claude mcp add` 中使用相对路径**。务必使用绝对路径。Claude Code 从它自己的工作目录解析 MCP 命令，而不是你的。

4. **没有为 Zod schema 添加 `.describe()`**。Claude 读取描述来理解每个参数的含义。没有描述，它只能猜测——而且经常猜错。

5. **在一个服务器中放入太多不相关的工具**。如果你的服务器有 20 多个跨不同领域的工具，Claude 会搞不清该用哪个。保持服务器聚焦。

6. **没有在工具处理函数中处理错误**。处理函数中未捕获的异常会导致整个 MCP 服务器崩溃。务必用 try/catch 包裹你的处理逻辑。

7. **修改代码后忘记重新构建**。TypeScript 的修改需要 `npm run build` 才能生效。服务器运行的是 `dist/` 目录，不是 `src/`。

## 常见问题

### MCP 与 REST API 有什么区别？

REST API 是为应用之间通信设计的。MCP 是为 AI 与工具之间通信设计的。主要区别：

- **发现机制**：MCP 服务器主动宣告自己的能力（工具、资源、提示词）。REST API 需要外部文档。
- **Schema**：MCP 使用带有人类可读描述的 Zod schema。REST 使用 OpenAPI/Swagger。
- **传输层**：MCP 通常使用 stdio 进行本地服务器通信（无端口冲突、无 HTTP 开销）。REST 需要运行 HTTP 服务器。
- **生命周期**：Claude Code 自动管理 MCP 服务器进程——需要时启动，完成后停止。

你完全可以将 REST API 封装为 MCP 服务器（参见上面的模式 2）。这通常是最佳方案。

### TypeScript 还是 Python SDK：该选哪个？

两者都是官方支持的。根据你的团队来选择：

| 因素 | TypeScript | Python |
|------|-----------|--------|
| 包名 | `@modelcontextprotocol/server` | `mcp[cli]` |
| 适合 | Web/Node.js 团队 | 数据科学、机器学习团队 |
| 类型安全 | Zod schema | Pydantic 模型 |
| 生态系统 | npm，更大的 MCP 社区 | pip，更适合数据工具 |
| Claude Code 集成 | 优秀（原生 Node.js） | 优秀（通过 uvx 或 python） |

对于 Claude Code 用户，TypeScript 略有优势，因为 Claude Code 本身运行在 Node.js 上，并且对 TypeScript 有更强的理解能力。

### MCP 服务器能在其他 AI 工具中使用吗？

可以。MCP 是一个开放标准。同一个服务器可以在以下工具中使用：

- **Claude Code**（CLI）
- **Claude 桌面应用**
- **Cursor**（IDE）
- **Windsurf**（IDE）
- **VS Code** 配合 Copilot MCP 扩展
- **Cline**（VS Code 扩展）

各客户端的配置方式不同，但服务器代码完全相同。这就是协议的意义所在。

### 可以同时运行多少个 MCP 服务器？

没有硬性限制，但每个服务器都是一个独立进程，会消耗内存。实用指南：

- **3-5 个服务器**：性能影响不明显
- **5-10 个服务器**：启动时间略有增加
- **10+ 个服务器**：考虑合并相关服务器或使用按需激活

### MCP 服务器能访问我的文件吗？

只有你授权才行。MCP 服务器作为普通进程运行，拥有你赋予的任何权限。除非你明确传递目录路径作为参数或你的服务器代码读取文件，否则它无法访问你的文件系统。

Claude Code 在调用 MCP 工具之前始终会征求你的许可，除非你在 [设置或 CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) 中预先批准了它。

## 快速参考

### 常用命令

```bash
# 添加 MCP 服务器（项目作用域）
claude mcp add <名称> <命令> [参数...]

# 带环境变量添加
claude mcp add <名称> -e KEY=value <命令> [参数...]

# 添加到用户作用域（所有项目可用）
claude mcp add --scope user <名称> <命令> [参数...]

# 列出所有已配置的服务器
claude mcp list

# 移除服务器
claude mcp remove <名称>

# 检查服务器状态（在 Claude Code 内）
/mcp
```

### 最简 MCP 服务器模板

```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.registerTool(
  "my_tool",
  {
    title: "My Tool",
    description: "What this tool does",
    inputSchema: {
      param: z.string().describe("What this parameter is for"),
    },
  },
  async ({ param }) => {
    console.error(`Processing: ${param}`); // 只能用 stderr！
    return {
      content: [{ type: "text" as const, text: `Result: ${param}` }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### package.json 必备配置

```json
{
  "type": "module",
  "bin": { "my-server": "./dist/index.js" },
  "dependencies": {
    "@modelcontextprotocol/server": "^2.0.0",
    "zod": "^3.23.0"
  }
}
```

## 下一步可以构建什么

现在你已经理解了 MCP，这里有一些项目创意可以尝试：

1. **Jira/Linear MCP 服务器** — 不离开终端就能创建和更新工单
2. **监控面板服务器** — 让 Claude 查询你的 Datadog/Grafana 指标
3. **代码审查服务器** — 将团队的审查清单作为 MCP 提示词暴露
4. **部署服务器** — 让 Claude 触发部署，并内置安全检查
5. **文档服务器** — 从 Claude Code 中搜索你的内部文档和 Wiki

每一个都遵循本指南中涵盖的相同模式：初始化项目、用 Zod schema 定义工具、正确处理错误，然后用 `claude mcp add` 注册。

## 相关阅读

- [Claude Code 安装指南 2026](/posts/ai/2026-02-25-claude-code-setup-guide/) — 安装和配置 Claude Code
- [10 个 Claude Code 新手常犯错误](/posts/ai/2026-02-25-claude-code-mistakes/) — 避免最常见的坑
- [Claude Code Hooks 指南](/posts/ai/2026-02-18-claude-code-hooks-guide/) — 自动化你的 Claude Code 工作流
- [CLAUDE.md 指南](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — 配置项目上下文以获得更好的 AI 效果
