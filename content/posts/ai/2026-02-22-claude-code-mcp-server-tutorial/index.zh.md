+++
date = '2026-02-22T12:00:00+08:00'
draft = false
title = '用 Claude Code 从零开发 MCP Server：TypeScript 实战教程（2026）'
description = '手把手教你用 Claude Code 开发自定义 MCP Server，从项目初始化到工具定义、调试、发布，附完整代码和避坑指南。适合想给 AI 扩展能力的开发者。'
toc = true
tags = ['Claude Code', 'MCP', 'TypeScript', 'AI 编程', 'MCP Server']
categories = ['AI实战']
keywords = ['MCP Server 开发', 'MCP Server 教程', 'Claude Code MCP', 'MCP TypeScript', 'Model Context Protocol', 'AI 工具开发', 'MCP Server 中文教程']
+++

**MCP Server** 是 2026 年 AI 工具生态的核心基础设施。Gartner 预测，到 2026 年底将有 40% 的企业应用嵌入 AI Agent。而 **Claude Code** 作为当下最强的 AI 编程工具之一，本身就是一个强大的 MCP 客户端。学会开发 MCP Server，就等于掌握了给 AI 装上新手脚的能力。

这篇文章将带你从零开始，用 Claude Code + TypeScript 开发一个完整的 MCP Server，从项目初始化到调试发布，全程实战。

## MCP 是什么？一个类比就够了

**MCP（Model Context Protocol）** 是 Anthropic 在 2024 年底提出的开放协议。官方给了一个很精准的类比：**MCP 就是 AI 世界的 USB-C**。

就像 USB-C 让你的笔记本电脑可以连接显示器、硬盘、键盘等各种设备一样，MCP 让 AI 模型可以连接数据库、API、文件系统等各种外部工具。

MCP 架构分三层：

```
┌─────────────────────────────────────────────┐
│           MCP 客户端（Host）                 │
│   Claude Code / Cursor / VS Code Copilot    │
├─────────────────────────────────────────────┤
│           MCP 协议层（Protocol）              │
│         JSON-RPC 2.0 + STDIO/HTTP           │
├─────────────────────────────────────────────┤
│           MCP 服务端（Server）                │
│   你开发的工具 / 数据源 / 提示模板            │
└─────────────────────────────────────────────┘
```

一个 MCP Server 可以提供三种能力：

| 能力 | 说明 | 举例 |
|------|------|------|
| **Tools（工具）** | 让 AI 执行操作 | 查天气、查数据库、发消息 |
| **Resources（资源）** | 让 AI 读取数据 | 配置文件、用户信息、日志 |
| **Prompts（提示模板）** | 预定义的交互模板 | 代码审查模板、摘要模板 |

其中 **Tools** 是最常用的能力，也是本文重点。

## 为什么用 Claude Code 开发 MCP Server

你可能会问：开发 MCP Server 用什么 IDE 都行，为什么特别推荐 Claude Code？

三个理由：

1. **Claude Code 本身就是 MCP 客户端**。开发完直接 `claude mcp add` 就能测试，不需要额外配置客户端。
2. **边写边测的开发体验**。Claude Code 可以直接调用你新注册的 Tool，实时验证效果。
3. **AI 辅助开发 AI 工具**。用 Claude Code 写 MCP Server 的代码，本身就是一种"AI 开发 AI 插件"的体验，效率极高。

## 环境准备

开始之前，确保你的开发环境满足以下条件：

| 依赖 | 最低版本 | 检查命令 |
|------|----------|----------|
| Node.js | >= 18 | `node -v` |
| npm | >= 9 | `npm -v` |
| Claude Code | 最新版 | `claude --version` |
| TypeScript | >= 5.0 | `npx tsc --version` |

如果都准备好了，开始动手。

## 实战：开发一个天气查询 MCP Server

我们先从最经典的入门案例开始 -- 一个天气查询工具。麻雀虽小，五脏俱全，它涵盖了 MCP Server 开发的核心流程。

### 第一步：初始化项目

```bash
mkdir weather-mcp-server
cd weather-mcp-server
npm init -y
```

安装依赖：

```bash
npm install @modelcontextprotocol/server zod
npm install -D typescript @types/node
```

这里用到两个核心包：

- **@modelcontextprotocol/server**：MCP Server SDK，提供 `McpServer`、`StdioServerTransport` 等核心类
- **zod**：Schema 验证库，MCP SDK v2 用它来定义工具的输入输出格式

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
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

更新 `package.json`，添加关键字段：

```json
{
  "name": "weather-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "weather-mcp-server": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

**注意**：`"type": "module"` 是必须的，MCP SDK 使用 ESM 模块。

### 第二步：编写 MCP Server 核心代码

创建 `src/index.ts`，这是整个 Server 的入口文件：

```typescript
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/server";
import { StdioServerTransport } from "@modelcontextprotocol/server";
import * as z from "zod";

// 1. 创建 Server 实例
const server = new McpServer({
  name: "weather-server",
  version: "1.0.0",
});

// 2. 模拟天气数据（实际项目中替换为真实 API 调用）
function getWeatherData(city: string): {
  city: string;
  temperature: number;
  condition: string;
  humidity: number;
} {
  // 模拟数据，实际开发中这里调用天气 API
  const weatherMap: Record<string, { temperature: number; condition: string; humidity: number }> = {
    "北京": { temperature: -2, condition: "晴", humidity: 30 },
    "上海": { temperature: 8, condition: "多云", humidity: 65 },
    "广州": { temperature: 18, condition: "阴", humidity: 75 },
    "深圳": { temperature: 20, condition: "晴", humidity: 70 },
    "杭州": { temperature: 6, condition: "小雨", humidity: 80 },
  };

  const data = weatherMap[city];
  if (!data) {
    return { city, temperature: 15, condition: "未知", humidity: 50 };
  }
  return { city, ...data };
}

// 3. 注册工具：获取天气
server.registerTool(
  "get_weather",
  {
    title: "获取天气",
    description: "查询指定城市的当前天气信息，包括温度、天气状况和湿度",
    inputSchema: z.object({
      city: z.string().describe("城市名称，如：北京、上海、广州"),
    }),
  },
  async ({ city }) => {
    const weather = getWeatherData(city);
    const text = `${weather.city}当前天气：${weather.condition}，温度 ${weather.temperature}°C，湿度 ${weather.humidity}%`;

    return {
      content: [{ type: "text", text }],
    };
  }
);

// 4. 注册工具：对比两个城市天气
server.registerTool(
  "compare_weather",
  {
    title: "对比天气",
    description: "对比两个城市的天气情况",
    inputSchema: z.object({
      city1: z.string().describe("第一个城市"),
      city2: z.string().describe("第二个城市"),
    }),
  },
  async ({ city1, city2 }) => {
    const w1 = getWeatherData(city1);
    const w2 = getWeatherData(city2);
    const diff = w1.temperature - w2.temperature;

    const text = [
      `天气对比：${w1.city} vs ${w2.city}`,
      `---`,
      `${w1.city}：${w1.condition}，${w1.temperature}°C，湿度 ${w1.humidity}%`,
      `${w2.city}：${w2.condition}，${w2.temperature}°C，湿度 ${w2.humidity}%`,
      `---`,
      `温差：${Math.abs(diff)}°C（${diff > 0 ? w1.city + "更暖" : w2.city + "更暖"}）`,
    ].join("\n");

    return {
      content: [{ type: "text", text }],
    };
  }
);

// 5. 启动 STDIO Transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server 已启动"); // 注意：用 console.error
}

main().catch(console.error);
```

代码解析几个关键点：

- **`McpServer`**：MCP Server 的核心类，所有工具、资源、提示模板都注册到它上面
- **`registerTool`**：v2 SDK 的工具注册方法，接收工具名、配置对象、处理函数三个参数
- **`inputSchema`**：用 Zod 定义输入参数的类型和描述，AI 客户端会根据这个 schema 来构造调用参数
- **`StdioServerTransport`**：通过标准输入输出通信，这是本地 MCP Server 最常用的传输方式
- **`console.error` 而不是 `console.log`**：这一点非常重要，下面会专门讲

### 第三步：编译和测试

编译 TypeScript：

```bash
npx tsc
```

给入口文件添加执行权限：

```bash
chmod +x dist/index.js
```

### 第四步：在 Claude Code 中测试

这是最激动人心的环节。用 `claude mcp add` 把你的 Server 注册到 Claude Code：

```bash
claude mcp add weather-server node /你的项目绝对路径/dist/index.js
```

然后启动 Claude Code，直接和它对话：

```
> 帮我查一下北京的天气

> 对比一下上海和广州的天气
```

Claude Code 会自动发现你注册的 `get_weather` 和 `compare_weather` 工具，并调用它们返回结果。

要验证 MCP Server 是否正确加载，可以用：

```bash
claude mcp list
```

## 进阶：添加 Resources 和 Prompts

掌握了 Tools 之后，我们来看另外两种能力。

### 注册 Resource（资源）

Resources 让 AI 可以读取你的数据。比如暴露一个支持的城市列表：

```typescript
server.registerResource(
  "supported-cities",
  "weather://cities",
  {
    title: "支持的城市列表",
    description: "返回所有支持查询天气的城市",
    mimeType: "application/json",
  },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        text: JSON.stringify(["北京", "上海", "广州", "深圳", "杭州"]),
      },
    ],
  })
);
```

### 注册 Prompt（提示模板）

Prompts 是预定义的交互模板，可以让用户快速触发常见场景：

```typescript
server.registerPrompt(
  "travel-advice",
  {
    title: "出行建议",
    description: "根据目的地天气给出出行穿搭建议",
    argsSchema: z.object({
      destination: z.string().describe("目的地城市"),
    }),
  },
  ({ destination }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `请根据${destination}的当前天气，给出出行穿搭和注意事项建议。`,
        },
      },
    ],
  })
);
```

## MCP Server 调试技巧

开发 MCP Server 时，调试是最容易踩坑的环节。以下是几个关键技巧。

### console.error 而不是 console.log

这是新手最常犯的错误。MCP 使用 **STDIO 协议**通信，`stdout`（标准输出）是数据通道，你的 `console.log` 会被当成协议消息解析，导致通信错乱。

**正确做法**：所有日志输出使用 `console.error`，它走的是 `stderr`（标准错误输出），不会干扰协议通信。

```typescript
// 错误 - 会破坏 STDIO 协议
console.log("调试信息");

// 正确 - 走 stderr，不影响通信
console.error("调试信息");
```

### 使用 SDK 内置日志

MCP SDK v2 提供了结构化日志能力，可以在工具处理函数中向客户端发送日志：

```typescript
server.registerTool(
  "fetch-data",
  {
    description: "获取数据",
    inputSchema: z.object({ url: z.string() }),
  },
  async ({ url }, ctx) => {
    await ctx.mcpReq.log("info", `正在请求 ${url}`);
    const res = await fetch(url);
    await ctx.mcpReq.log("debug", `响应状态: ${res.status}`);
    const text = await res.text();
    return { content: [{ type: "text", text }] };
  }
);
```

需要在创建 Server 时启用 logging 能力：

```typescript
const server = new McpServer(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { logging: {} } }
);
```

### Claude Code 中查看 MCP 日志

如果 MCP Server 启动失败或行为异常，可以用以下方式排查：

```bash
# 查看已注册的 MCP Server 状态
claude mcp list

# 移除并重新添加（重启 Server）
claude mcp remove weather-server
claude mcp add weather-server node /path/to/dist/index.js
```

### 常见错误速查

| 现象 | 原因 | 解决方案 |
|------|------|----------|
| Server 无法启动 | package.json 缺少 `"type": "module"` | 添加 `"type": "module"` |
| 工具不被识别 | `inputSchema` 格式错误 | 确保用 `z.object()` 包裹 |
| 通信错乱 | 使用了 `console.log` | 改为 `console.error` |
| 类型错误 | SDK 版本不匹配 | 确认使用 `@modelcontextprotocol/server` v2 |
| 工具调用无响应 | 处理函数未返回 content | 确保返回 `{ content: [...] }` |

## 发布你的 MCP Server

当你的 MCP Server 开发测试完成后，可以发布到 npm 让更多人使用。

### 准备发布

确保 `package.json` 包含以下字段：

```json
{
  "name": "@your-scope/weather-mcp-server",
  "version": "1.0.0",
  "description": "一个查询天气的 MCP Server",
  "type": "module",
  "bin": {
    "weather-mcp-server": "./dist/index.js"
  },
  "files": ["dist"],
  "keywords": ["mcp", "mcp-server", "weather"],
  "license": "MIT"
}
```

### 发布到 npm

```bash
npm run build
npm publish --access public
```

发布后，其他人只需要一行命令就能使用：

```bash
claude mcp add weather-server npx @your-scope/weather-mcp-server
```

### 提交到社区

你还可以把项目提交到 [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) 仓库，让更多开发者发现你的工具。

## 总结

通过这篇教程，你已经掌握了 MCP Server 开发的核心流程：

1. **理解 MCP 架构**：Client - Protocol - Server 三层模型
2. **用 TypeScript + SDK v2 开发**：`McpServer` + `registerTool` + `StdioServerTransport`
3. **在 Claude Code 中测试**：`claude mcp add` 一行命令即测
4. **调试避坑**：`console.error` 代替 `console.log`，善用结构化日志
5. **发布分享**：npm publish + awesome-mcp-servers

MCP 的生态正在快速成长，越早上手，越早享受 AI 工具链的红利。

## 常见问题（FAQ）

### MCP Server 和传统 REST API 有什么区别？

MCP Server 是专为 AI 客户端设计的协议，使用 JSON-RPC 2.0 通信。与 REST API 的最大区别在于：MCP 提供了标准化的工具发现机制（AI 可以自动列出所有可用工具和参数），而 REST API 需要人工阅读文档。此外，MCP 支持 STDIO 传输，可以作为本地进程运行，不需要启动 HTTP 服务。

### 开发 MCP Server 必须用 TypeScript 吗？

不是必须的。MCP 官方提供了 TypeScript、Python、C# 等多语言 SDK。但 TypeScript SDK 是生态最成熟、文档最完善的，推荐优先使用。

### MCP SDK v1 和 v2 有什么区别？

v2 的主要变化包括：包名从 `@modelcontextprotocol/sdk` 拆分为 `@modelcontextprotocol/server` 和 `@modelcontextprotocol/client`；工具注册方法从 `server.tool()` 变为 `server.registerTool()`；输入校验必须使用 `z.object()` 包裹完整的 Zod Schema。如果你看到的教程还在用 `server.tool()`，说明是 v1 的写法，建议迁移到 v2。

### 一个 MCP Server 可以注册多少个工具？

协议本身没有限制。但实际使用中，建议一个 MCP Server 聚焦一个领域，注册 3-10 个相关工具即可。工具太多会影响 AI 的工具选择准确率。

### Claude Code 以外的客户端也能用我开发的 MCP Server 吗？

可以。任何支持 MCP 协议的客户端都能使用，包括 Cursor、VS Code Copilot（通过插件）、Continue 等。这就是标准协议的好处 -- 一次开发，到处使用。

## 相关阅读

- [Claude Code 浏览器自动化实战](/zh/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Claude Code 完全指南](/zh/posts/ai/2026-01-14-claude-code-guide/)
- [OpenClaw Skills Top20 排行榜](/zh/posts/ai/2026-01-20-claude-code-skills-top20/)
