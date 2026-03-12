+++
date = '2026-02-22T12:00:00+08:00'
draft = false
title = 'Build an MCP Server with Claude Code: TypeScript Tutorial (2026)'
description = 'Learn how to build a custom MCP Server using Claude Code and TypeScript. Covers project setup, tool registration, debugging, and publishing to npm with full code examples.'
toc = true
tags = ['Claude Code', 'MCP', 'TypeScript', 'AI Development', 'MCP Server']
categories = ['AI Guides']
keywords = ['MCP Server tutorial', 'build MCP Server', 'Claude Code MCP', 'MCP TypeScript', 'Model Context Protocol', 'MCP Server development', 'MCP tools']
+++

**MCP Servers** are becoming the backbone of the AI tool ecosystem in 2026. Gartner predicts that 40% of enterprise applications will embed AI agents by end of year. **Claude Code**, one of the most capable AI coding tools available today, doubles as a full-featured MCP client. Learning to build MCP Servers means learning to extend what AI can do.

This tutorial walks you through building a complete MCP Server from scratch using Claude Code and TypeScript -- from project initialization to debugging and publishing.

## What Is MCP? One Analogy Is All You Need

**MCP (Model Context Protocol)** is an open protocol introduced by Anthropic in late 2024. The official analogy nails it: **MCP is the USB-C of the AI world**.

Just as USB-C lets your laptop connect to monitors, drives, keyboards, and other peripherals through a single standard, MCP lets AI models connect to databases, APIs, file systems, and other external tools through a unified protocol.

The MCP architecture has three layers:

```
┌─────────────────────────────────────────────┐
│           MCP Client (Host)                 │
│   Claude Code / Cursor / VS Code Copilot    │
├─────────────────────────────────────────────┤
│           MCP Protocol Layer                │
│         JSON-RPC 2.0 + STDIO/HTTP           │
├─────────────────────────────────────────────┤
│           MCP Server                        │
│   Your tools / data sources / prompts       │
└─────────────────────────────────────────────┘
```

An MCP Server can expose three types of capabilities:

| Capability | What It Does | Examples |
|------------|-------------|----------|
| **Tools** | Let AI perform actions | Check weather, query databases, send messages |
| **Resources** | Let AI read data | Config files, user profiles, logs |
| **Prompts** | Predefined interaction templates | Code review templates, summary templates |

**Tools** are by far the most commonly used capability, and they are the focus of this tutorial.

## Why Build MCP Servers with Claude Code

You might wonder: you can build an MCP Server in any editor, so why use Claude Code specifically?

Three reasons:

1. **Claude Code is already an MCP client.** Once you build your server, just run `claude mcp add` and start testing immediately -- no separate client setup needed.
2. **Instant feedback loop.** Claude Code can call your newly registered tools in real time, so you see results as you build.
3. **AI building AI tools.** Using Claude Code to write MCP Server code is the ultimate meta-experience -- AI helping you build AI plugins. It is remarkably productive.

## Prerequisites

Before we start, make sure your development environment meets these requirements:

| Dependency | Minimum Version | Check Command |
|------------|----------------|---------------|
| Node.js | >= 18 | `node -v` |
| npm | >= 9 | `npm -v` |
| Claude Code | Latest | `claude --version` |
| TypeScript | >= 5.0 | `npx tsc --version` |

All set? Let's build.

## Hands-On: Building a Weather MCP Server

We will start with the classic starter project -- a weather lookup tool. It is small but covers every core concept of MCP Server development.

### Step 1: Initialize the Project

```bash
mkdir weather-mcp-server
cd weather-mcp-server
npm init -y
```

Install dependencies:

```bash
npm install @modelcontextprotocol/server zod
npm install -D typescript @types/node
```

Two key packages here:

- **@modelcontextprotocol/server**: The MCP Server SDK, providing core classes like `McpServer` and `StdioServerTransport`
- **zod**: Schema validation library used by MCP SDK v2 to define input and output shapes for tools

Create `tsconfig.json`:

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

Update `package.json` with the required fields:

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

**Important**: `"type": "module"` is mandatory. The MCP SDK uses ESM modules.

### Step 2: Write the MCP Server Code

Create `src/index.ts` -- this is the entry point for your entire server:

```typescript
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/server";
import { StdioServerTransport } from "@modelcontextprotocol/server";
import * as z from "zod";

// 1. Create the server instance
const server = new McpServer({
  name: "weather-server",
  version: "1.0.0",
});

// 2. Mock weather data (replace with a real API in production)
function getWeatherData(city: string): {
  city: string;
  temperature: number;
  condition: string;
  humidity: number;
} {
  const weatherMap: Record<string, { temperature: number; condition: string; humidity: number }> = {
    "New York": { temperature: 3, condition: "Cloudy", humidity: 55 },
    "London": { temperature: 8, condition: "Rainy", humidity: 80 },
    "Tokyo": { temperature: 12, condition: "Sunny", humidity: 45 },
    "Sydney": { temperature: 25, condition: "Sunny", humidity: 60 },
    "Berlin": { temperature: 1, condition: "Overcast", humidity: 70 },
  };

  const data = weatherMap[city];
  if (!data) {
    return { city, temperature: 15, condition: "Unknown", humidity: 50 };
  }
  return { city, ...data };
}

// 3. Register tool: get weather
server.registerTool(
  "get_weather",
  {
    title: "Get Weather",
    description: "Get current weather for a specified city, including temperature, conditions, and humidity",
    inputSchema: z.object({
      city: z.string().describe("City name, e.g.: New York, London, Tokyo"),
    }),
  },
  async ({ city }) => {
    const weather = getWeatherData(city);
    const text = `Current weather in ${weather.city}: ${weather.condition}, ${weather.temperature}°C, humidity ${weather.humidity}%`;

    return {
      content: [{ type: "text", text }],
    };
  }
);

// 4. Register tool: compare weather between two cities
server.registerTool(
  "compare_weather",
  {
    title: "Compare Weather",
    description: "Compare the weather between two cities",
    inputSchema: z.object({
      city1: z.string().describe("First city"),
      city2: z.string().describe("Second city"),
    }),
  },
  async ({ city1, city2 }) => {
    const w1 = getWeatherData(city1);
    const w2 = getWeatherData(city2);
    const diff = w1.temperature - w2.temperature;

    const text = [
      `Weather Comparison: ${w1.city} vs ${w2.city}`,
      `---`,
      `${w1.city}: ${w1.condition}, ${w1.temperature}°C, humidity ${w1.humidity}%`,
      `${w2.city}: ${w2.condition}, ${w2.temperature}°C, humidity ${w2.humidity}%`,
      `---`,
      `Temperature difference: ${Math.abs(diff)}°C (${diff > 0 ? w1.city + " is warmer" : w2.city + " is warmer"})`,
    ].join("\n");

    return {
      content: [{ type: "text", text }],
    };
  }
);

// 5. Start the STDIO transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server started"); // Note: use console.error, not console.log
}

main().catch(console.error);
```

A few key points about this code:

- **`McpServer`**: The core class of an MCP Server. All tools, resources, and prompts get registered on this instance.
- **`registerTool`**: The v2 SDK method for registering tools. It takes three arguments: tool name, config object, and handler function.
- **`inputSchema`**: Uses Zod to define parameter types and descriptions. AI clients use this schema to construct their tool calls.
- **`StdioServerTransport`**: Communicates over standard input/output. This is the most common transport for local MCP Servers.
- **`console.error` instead of `console.log`**: This is critical -- more on that in the debugging section below.

### Step 3: Compile and Test

Compile the TypeScript:

```bash
npx tsc
```

Make the entry file executable:

```bash
chmod +x dist/index.js
```

### Step 4: Test in Claude Code

This is the payoff. Register your server with Claude Code using `claude mcp add`:

```bash
claude mcp add weather-server node /absolute/path/to/your/project/dist/index.js
```

Then launch Claude Code and try it out:

```
> What's the weather like in Tokyo?

> Compare the weather in New York and London
```

Claude Code will automatically discover your `get_weather` and `compare_weather` tools and call them to return results.

To verify that your MCP Server loaded correctly:

```bash
claude mcp list
```

## Going Further: Adding Resources and Prompts

Now that you have Tools down, let's explore the other two capabilities.

### Registering a Resource

Resources let AI read your data. For example, you can expose a list of supported cities:

```typescript
server.registerResource(
  "supported-cities",
  "weather://cities",
  {
    title: "Supported Cities",
    description: "Returns all cities available for weather queries",
    mimeType: "application/json",
  },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        text: JSON.stringify(["New York", "London", "Tokyo", "Sydney", "Berlin"]),
      },
    ],
  })
);
```

### Registering a Prompt

Prompts are predefined interaction templates that help users quickly trigger common workflows:

```typescript
server.registerPrompt(
  "travel-advice",
  {
    title: "Travel Advice",
    description: "Get clothing and travel tips based on destination weather",
    argsSchema: z.object({
      destination: z.string().describe("Destination city"),
    }),
  },
  ({ destination }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Based on the current weather in ${destination}, please suggest what to wear and any travel tips.`,
        },
      },
    ],
  })
);
```

## Debugging MCP Servers

Debugging is where most developers run into trouble when building MCP Servers. Here are the essential techniques.

### Use console.error, Not console.log

This is the most common mistake beginners make. MCP communicates over the **STDIO protocol**, which means `stdout` (standard output) is the data channel. If you use `console.log`, your debug messages get mixed into the protocol stream and corrupt communication.

**The fix**: Use `console.error` for all logging. It writes to `stderr` (standard error), which stays out of the protocol channel.

```typescript
// Wrong -- breaks the STDIO protocol
console.log("debug info");

// Correct -- writes to stderr, doesn't interfere
console.error("debug info");
```

### Use the SDK's Built-in Logging

MCP SDK v2 includes structured logging that lets you send log messages from tool handlers directly to the client:

```typescript
server.registerTool(
  "fetch-data",
  {
    description: "Fetch data from a URL",
    inputSchema: z.object({ url: z.string() }),
  },
  async ({ url }, ctx) => {
    await ctx.mcpReq.log("info", `Fetching ${url}`);
    const res = await fetch(url);
    await ctx.mcpReq.log("debug", `Response status: ${res.status}`);
    const text = await res.text();
    return { content: [{ type: "text", text }] };
  }
);
```

You need to enable the logging capability when creating the server:

```typescript
const server = new McpServer(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { logging: {} } }
);
```

### Checking MCP Logs in Claude Code

If your MCP Server fails to start or behaves unexpectedly, use these commands to troubleshoot:

```bash
# Check the status of registered MCP Servers
claude mcp list

# Remove and re-add to restart the server
claude mcp remove weather-server
claude mcp add weather-server node /path/to/dist/index.js
```

### Common Error Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| Server won't start | Missing `"type": "module"` in package.json | Add `"type": "module"` |
| Tools not recognized | Invalid `inputSchema` format | Wrap schemas with `z.object()` |
| Garbled communication | Using `console.log` | Switch to `console.error` |
| Type errors | SDK version mismatch | Verify you're using `@modelcontextprotocol/server` v2 |
| Tool calls return nothing | Handler doesn't return content | Ensure handlers return `{ content: [...] }` |

## Publishing Your MCP Server

Once your MCP Server is built and tested, you can publish it to npm so others can use it.

### Prepare for Publishing

Make sure `package.json` includes these fields:

```json
{
  "name": "@your-scope/weather-mcp-server",
  "version": "1.0.0",
  "description": "An MCP Server for weather queries",
  "type": "module",
  "bin": {
    "weather-mcp-server": "./dist/index.js"
  },
  "files": ["dist"],
  "keywords": ["mcp", "mcp-server", "weather"],
  "license": "MIT"
}
```

### Publish to npm

```bash
npm run build
npm publish --access public
```

Once published, anyone can start using your server with a single command:

```bash
claude mcp add weather-server npx @your-scope/weather-mcp-server
```

### Submit to the Community

You can also submit your project to the [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) repository to help other developers discover your tool.

## Wrapping Up

By following this tutorial, you have learned the complete MCP Server development workflow:

1. **Understanding the MCP architecture**: The three-layer model of Client, Protocol, and Server
2. **Building with TypeScript and SDK v2**: `McpServer` + `registerTool` + `StdioServerTransport`
3. **Testing in Claude Code**: One `claude mcp add` command to start testing
4. **Debugging effectively**: `console.error` over `console.log`, plus structured logging
5. **Publishing and sharing**: npm publish + awesome-mcp-servers

The MCP ecosystem is growing fast. The earlier you start building, the sooner you benefit from the expanding AI tool chain.

## FAQ

### How is an MCP Server different from a traditional REST API?

MCP is a protocol designed specifically for AI clients, using JSON-RPC 2.0 for communication. The biggest difference from REST APIs is that MCP provides standardized tool discovery -- AI clients can automatically list all available tools and their parameters without reading documentation. REST APIs require developers to manually consult API docs. Additionally, MCP supports STDIO transport, meaning servers can run as local processes without spinning up an HTTP service.

### Do I have to use TypeScript to build MCP Servers?

No. MCP has official SDKs for TypeScript, Python, C#, and other languages. That said, the TypeScript SDK has the most mature ecosystem and the most thorough documentation, making it the recommended choice for getting started.

### What changed between MCP SDK v1 and v2?

The major changes in v2 include: the package was split from `@modelcontextprotocol/sdk` into separate `@modelcontextprotocol/server` and `@modelcontextprotocol/client` packages; the tool registration method changed from `server.tool()` to `server.registerTool()`; and input validation now requires wrapping schemas in `z.object()`. If a tutorial you're following still uses `server.tool()`, it's based on v1 and should be updated to v2.

### How many tools can a single MCP Server register?

The protocol itself imposes no limit. In practice, though, it's best to keep each MCP Server focused on a single domain with 3 to 10 related tools. Registering too many tools can reduce the accuracy of the AI's tool selection.

### Can clients other than Claude Code use my MCP Server?

Absolutely. Any client that supports the MCP protocol can use your server, including Cursor, VS Code Copilot (via extensions), Continue, and others. That's the beauty of an open standard -- build once, use everywhere.

## Related Articles

- [Claude Code Browser Automation in Practice](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [The Complete Guide to Claude Code](/posts/ai/2026-01-14-claude-code-guide/)
- [OpenClaw Skills Top 20 Ranking](/posts/ai/2026-01-20-claude-code-skills-top20/)
