+++
date = '2026-03-02T10:00:00+08:00'
draft = false
title = 'Building MCP Servers with TypeScript: Zero to Deploy Tutorial'
description = 'Step-by-step guide to building MCP servers with TypeScript. Learn to create tools, resources, and prompts using the MCP SDK v2, test with Claude Code, debug common issues, and publish to npm.'
toc = true
tags = ['MCP', 'TypeScript', 'Claude Code', 'AI Agent', 'Tutorial']
categories = ['AI Guides']
keywords = ['build MCP server', 'MCP TypeScript tutorial', 'Model Context Protocol server', 'MCP SDK v2', 'Claude Code MCP', 'create MCP tools', 'MCP server development']

[[params.faqItems]]
question = "What programming languages can I use to build MCP servers?"
answer = "The MCP protocol has official SDKs for TypeScript, Python, and C#. TypeScript is the most mature with the best documentation. Python is a strong alternative. You can also build servers in any language that supports JSON-RPC 2.0 over STDIO or HTTP."

[[params.faqItems]]
question = "How is an MCP server different from a REST API?"
answer = "MCP servers use JSON-RPC 2.0 instead of HTTP REST. The key difference is standardized tool discovery — AI clients can automatically list all available tools and their parameters without reading documentation. MCP also supports STDIO transport, running as a local process without an HTTP server."

[[params.faqItems]]
question = "Can MCP servers work with clients other than Claude Code?"
answer = "Yes. Any MCP-compatible client can use your server, including Cursor, VS Code with Copilot extensions, Continue, and other AI tools. This is the core benefit of building on an open protocol — build once, use everywhere."

[[params.faqItems]]
question = "What is the difference between MCP SDK v1 and v2?"
answer = "SDK v2 split the package into @modelcontextprotocol/server and @modelcontextprotocol/client. Tool registration changed from server.tool() to server.registerTool(). Input validation now requires z.object() wrapping. If a tutorial uses server.tool(), it's using v1 syntax."
+++

![Building MCP servers with TypeScript from zero to deploy](cover.webp)

MCP (Model Context Protocol) is the standard way to give AI models access to external tools, data, and services in 2026. If you've used [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) or Cursor, you've already used MCP servers — they power everything from database queries to API integrations.

This tutorial walks you through building your own MCP server from scratch with TypeScript, from project setup to npm publishing. By the end, you'll have a working server that any MCP-compatible AI client can use.

## What Is MCP? The 30-Second Version

**MCP is USB-C for AI.** Just as USB-C lets your laptop connect to monitors, drives, and keyboards through one standard port, MCP lets AI models connect to databases, APIs, and file systems through one standard protocol. The [official MCP specification](https://spec.modelcontextprotocol.io/) defines the full protocol details.

```
┌─────────────────────────────────────────────┐
│           MCP Client (Host)                 │
│   Claude Code / Cursor / VS Code Copilot    │
├─────────────────────────────────────────────┤
│           MCP Protocol Layer                │
│         JSON-RPC 2.0 + STDIO/HTTP           │
├─────────────────────────────────────────────┤
│           MCP Server (Your Code)            │
│   Tools / Resources / Prompt Templates      │
└─────────────────────────────────────────────┘
```

An MCP server exposes three types of capabilities:

| Capability | What It Does | Examples |
|-----------|-------------|---------|
| **Tools** | Let AI perform actions | Query a database, send a message, call an API |
| **Resources** | Let AI read data | Configuration files, user profiles, logs |
| **Prompts** | Pre-built interaction templates | Code review template, summary template |

**Tools** are the most common — and the focus of this tutorial.

For a broader overview of the MCP protocol, see my [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) guide.

## Why Build MCP Servers with Claude Code

You can build MCP servers with any editor, but [Claude Code](/posts/ai/2026-02-25-claude-code-setup-guide/) is uniquely suited for this:

1. **Claude Code is an MCP client.** Run `claude mcp add` and test your server instantly — no separate client setup needed.
2. **Live testing loop.** Write a tool, register it, and ask Claude to call it. Debug in real-time.
3. **AI building AI tools.** Using Claude Code to write MCP server code is AI developing its own plugins. The efficiency is remarkable.

## Prerequisites

| Dependency | Minimum Version | Check Command |
|-----------|----------------|---------------|
| Node.js | >= 18 | `node -v` |
| npm | >= 9 | `npm -v` |
| TypeScript | >= 5.0 | `npx tsc --version` |
| Claude Code | Latest | `claude --version` |

## Tutorial: Build a Weather MCP Server

We'll start with a classic example — a weather query tool. It covers the complete MCP server development workflow: project init, tool registration, testing, and debugging.

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

Two core packages:
- **[@modelcontextprotocol/server](https://github.com/modelcontextprotocol/typescript-sdk)** — MCP Server SDK providing `McpServer`, `StdioServerTransport`, and related classes
- **[zod](https://zod.dev/)** — Schema validation library used by SDK v2 to define tool input/output formats

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

Update `package.json` with required fields:

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

**Critical**: `"type": "module"` is required. The MCP SDK uses ESM modules.

### Step 2: Write the MCP Server

Create `src/index.ts` — the entry point for your server:

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

// 2. Simulated weather data (replace with real API in production)
function getWeatherData(city: string) {
  const weatherMap: Record<
    string,
    { temperature: number; condition: string; humidity: number }
  > = {
    "New York": { temperature: 2, condition: "Cloudy", humidity: 65 },
    "San Francisco": { temperature: 14, condition: "Sunny", humidity: 70 },
    London: { temperature: 8, condition: "Rainy", humidity: 85 },
    Tokyo: { temperature: 10, condition: "Clear", humidity: 55 },
    Sydney: { temperature: 25, condition: "Sunny", humidity: 60 },
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
    description:
      "Get current weather for a city including temperature, condition, and humidity",
    inputSchema: z.object({
      city: z
        .string()
        .describe("City name, e.g. New York, London, Tokyo"),
    }),
  },
  async ({ city }) => {
    const weather = getWeatherData(city);
    const text = `Weather in ${weather.city}: ${weather.condition}, ${weather.temperature}°C, humidity ${weather.humidity}%`;
    return {
      content: [{ type: "text", text }],
    };
  }
);

// 4. Register tool: compare two cities
server.registerTool(
  "compare_weather",
  {
    title: "Compare Weather",
    description: "Compare weather between two cities",
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

// 5. Start STDIO transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server started"); // Use stderr, not stdout!
}

main().catch(console.error);
```

Key concepts in this code:

- **`McpServer`** — Core class where all tools, resources, and prompts are registered
- **`registerTool`** — SDK v2 method taking three arguments: tool name, config object, handler function
- **`inputSchema`** — Zod schema that defines parameter types and descriptions. AI clients use this schema to construct correct tool calls
- **`StdioServerTransport`** — Communicates via stdin/stdout, the standard transport for local MCP servers
- **`console.error` not `console.log`** — Critical detail explained in the debugging section below

### Step 3: Build and Test

Compile TypeScript:

```bash
npx tsc
chmod +x dist/index.js
```

Register with Claude Code:

```bash
claude mcp add weather-server node /absolute/path/to/dist/index.js
```

Now open Claude Code and test:

```
> What's the weather in Tokyo?

> Compare the weather in New York and London
```

Claude Code automatically discovers your `get_weather` and `compare_weather` tools and calls them.

To verify your server is loaded:

```bash
claude mcp list
```

For more on Claude Code's MCP integration, see my [Claude Code MCP Setup guide](/posts/ai/2026-02-28-claude-code-mcp-setup/).

## Adding Resources and Prompts

Beyond tools, MCP servers can expose data and interaction templates.

### Registering a Resource

Resources let AI clients read your data. Here's a resource that exposes a list of supported cities:

```typescript
server.registerResource(
  "supported-cities",
  "weather://cities",
  {
    title: "Supported Cities",
    description: "Returns all cities with weather data available",
    mimeType: "application/json",
  },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        text: JSON.stringify([
          "New York",
          "San Francisco",
          "London",
          "Tokyo",
          "Sydney",
        ]),
      },
    ],
  })
);
```

### Registering a Prompt

Prompts are pre-built interaction templates:

```typescript
server.registerPrompt(
  "travel-advice",
  {
    title: "Travel Advice",
    description: "Get outfit and travel tips based on destination weather",
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
          text: `Based on the current weather in ${destination}, suggest appropriate clothing and travel tips.`,
        },
      },
    ],
  })
);
```

## Building a Real-World MCP Server: GitHub Issues

Let's build something more practical — a server that reads GitHub issues. This demonstrates real API integration.

```typescript
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/server";
import { StdioServerTransport } from "@modelcontextprotocol/server";
import * as z from "zod";

const server = new McpServer({
  name: "github-issues-server",
  version: "1.0.0",
});

// Tool: List recent issues
server.registerTool(
  "list_issues",
  {
    title: "List GitHub Issues",
    description: "List recent issues from a GitHub repository",
    inputSchema: z.object({
      owner: z.string().describe("Repository owner (e.g. 'anthropics')"),
      repo: z.string().describe("Repository name (e.g. 'claude-code')"),
      state: z
        .enum(["open", "closed", "all"])
        .default("open")
        .describe("Issue state filter"),
      limit: z
        .number()
        .min(1)
        .max(30)
        .default(10)
        .describe("Number of issues to return"),
    }),
  },
  async ({ owner, repo, state, limit }) => {
    const url = `https://api.github.com/repos/${owner}/${repo}/issues?state=${state}&per_page=${limit}`;

    const response = await fetch(url, {
      headers: {
        Accept: "application/vnd.github.v3+json",
        "User-Agent": "mcp-github-issues",
      },
    });

    if (!response.ok) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching issues: ${response.status} ${response.statusText}`,
          },
        ],
        isError: true,
      };
    }

    const issues = await response.json();
    const formatted = issues
      .map(
        (issue: any) =>
          `#${issue.number} [${issue.state}] ${issue.title}\n  Labels: ${issue.labels.map((l: any) => l.name).join(", ") || "none"}\n  Created: ${issue.created_at}\n  URL: ${issue.html_url}`
      )
      .join("\n\n");

    return {
      content: [
        {
          type: "text",
          text: `Issues for ${owner}/${repo} (${state}):\n\n${formatted}`,
        },
      ],
    };
  }
);

// Tool: Get issue details
server.registerTool(
  "get_issue",
  {
    title: "Get Issue Details",
    description: "Get detailed information about a specific GitHub issue",
    inputSchema: z.object({
      owner: z.string().describe("Repository owner"),
      repo: z.string().describe("Repository name"),
      issue_number: z.number().describe("Issue number"),
    }),
  },
  async ({ owner, repo, issue_number }) => {
    const url = `https://api.github.com/repos/${owner}/${repo}/issues/${issue_number}`;

    const response = await fetch(url, {
      headers: {
        Accept: "application/vnd.github.v3+json",
        "User-Agent": "mcp-github-issues",
      },
    });

    if (!response.ok) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${response.status} ${response.statusText}`,
          },
        ],
        isError: true,
      };
    }

    const issue = await response.json();
    const text = [
      `# #${issue.number}: ${issue.title}`,
      `State: ${issue.state}`,
      `Author: ${issue.user.login}`,
      `Created: ${issue.created_at}`,
      `Labels: ${issue.labels.map((l: any) => l.name).join(", ") || "none"}`,
      `Comments: ${issue.comments}`,
      `---`,
      issue.body || "(no description)",
    ].join("\n");

    return {
      content: [{ type: "text", text }],
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("GitHub Issues MCP Server started");
}

main().catch(console.error);
```

After building and registering this server, you can ask Claude Code:

```
> List open issues in anthropics/claude-code
> Show me the details of issue #42 in that repo
```

## Debugging MCP Servers

Debugging is the trickiest part of MCP server development. Here are the essential techniques.

### Use console.error, Not console.log

This is the #1 mistake new MCP developers make, as noted in the [MCP debugging guide](https://modelcontextprotocol.io/docs/tools/debugging). MCP uses **STDIO protocol** for communication — `stdout` is the data channel. Any `console.log` output gets interpreted as protocol messages, breaking communication.

```typescript
// WRONG — breaks STDIO protocol
console.log("Debug info");

// CORRECT — uses stderr, doesn't interfere
console.error("Debug info");
```

### Use SDK Built-in Logging

MCP SDK v2 provides structured logging that sends messages to the client:

```typescript
server.registerTool(
  "fetch-data",
  {
    description: "Fetch data from URL",
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

Enable logging when creating the server:

```typescript
const server = new McpServer(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { logging: {} } }
);
```

### Common Errors and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Server won't start | Missing `"type": "module"` in package.json | Add `"type": "module"` |
| Tools not recognized | Invalid `inputSchema` format | Wrap with `z.object()` |
| Communication errors | Using `console.log` | Switch to `console.error` |
| Type errors | SDK version mismatch | Verify `@modelcontextprotocol/server` v2 |
| Tool calls return nothing | Missing content in response | Ensure handler returns `{ content: [...] }` |
| Server crashes on startup | Unhandled async error | Add `.catch(console.error)` to main() |
| Parameters not validated | Using raw object instead of Zod | Always use `z.object()` with `.describe()` |

### Restart and Verify

```bash
# Check registered servers
claude mcp list

# Remove and re-add (restart the server)
claude mcp remove weather-server
claude mcp add weather-server node /path/to/dist/index.js
```

## Publishing Your MCP Server

When your server is ready, publish it to npm so others can use it.

### Prepare package.json

```json
{
  "name": "@your-scope/weather-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for weather data queries",
  "type": "module",
  "bin": {
    "weather-mcp-server": "./dist/index.js"
  },
  "files": ["dist"],
  "keywords": ["mcp", "mcp-server", "weather"],
  "license": "MIT"
}
```

### Build and Publish

```bash
npm run build
npm publish --access public
```

After publishing, anyone can use your server with one command:

```bash
claude mcp add weather-server npx @your-scope/weather-mcp-server
```

### Share with the Community

Submit your project to the [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) repository to increase visibility. You can also list it on the [MCP official server registry](https://modelcontextprotocol.io/examples).

## Project Structure Best Practices

For larger MCP server projects, organize your code like this:

```
my-mcp-server/
├── src/
│   ├── index.ts          # Entry point, server setup
│   ├── tools/            # Tool handlers
│   │   ├── query.ts
│   │   └── mutate.ts
│   ├── resources/        # Resource handlers
│   │   └── config.ts
│   └── utils/            # Shared utilities
│       └── api-client.ts
├── dist/                 # Compiled output
├── package.json
├── tsconfig.json
└── README.md
```

Key principles:
- **One domain per server** — Don't build a mega-server with 50 tools. Create focused servers (3-10 tools each)
- **Separate tool handlers** — Keep each tool's logic in its own file for testability
- **Type your responses** — Use TypeScript interfaces for API responses to catch errors at compile time
- **Handle errors gracefully** — Return `isError: true` in content rather than throwing exceptions

## FAQ

### What programming languages can I use to build MCP servers?

The MCP protocol has official SDKs for TypeScript, Python, and C#. TypeScript is the most mature with the best documentation. Python is a strong alternative. You can also build servers in any language that supports JSON-RPC 2.0 over STDIO or HTTP.

### How is an MCP server different from a REST API?

MCP servers use JSON-RPC 2.0 instead of HTTP REST. The key difference is standardized tool discovery — AI clients can automatically list all available tools and their parameters without reading documentation. MCP also supports STDIO transport, running as a local process without an HTTP server.

### Can MCP servers work with clients other than Claude Code?

Yes. Any MCP-compatible client can use your server, including Cursor, VS Code with Copilot extensions, Continue, and other AI tools. This is the core benefit of building on an open protocol — build once, use everywhere.

### What is the difference between MCP SDK v1 and v2?

SDK v2 split the package into `@modelcontextprotocol/server` and `@modelcontextprotocol/client`. Tool registration changed from `server.tool()` to `server.registerTool()`. Input validation now requires `z.object()` wrapping. If a tutorial uses `server.tool()`, it's using v1 syntax.

### How many tools should one MCP server have?

The protocol has no limit, but practically, 3-10 tools per server works best. Too many tools reduces the AI's accuracy in selecting the right one. Group related tools in a single server, and create separate servers for different domains.

### Can MCP servers access the internet?

Yes. Your server runs as a Node.js process with full network access. You can call external APIs, query databases, read files — anything Node.js can do. Just be mindful of latency, as the AI client waits for your tool to respond.

## Summary

Building MCP servers follows a straightforward workflow:

1. **Initialize** — Set up a TypeScript project with `@modelcontextprotocol/server` and `zod`
2. **Register tools** — Use `server.registerTool()` with Zod schemas for input validation
3. **Test locally** — `claude mcp add` for instant testing in Claude Code
4. **Debug** — Use `console.error` (never `console.log`), check common errors table
5. **Publish** — `npm publish` and share via `npx`

The MCP ecosystem is growing fast. Every MCP server you build becomes instantly usable by Claude Code, Cursor, Copilot, and any future MCP-compatible tool. Start building today.

## Related Articles

- [MCP Protocol Explained: The Universal Standard for AI Tools](/posts/ai/2026-02-28-mcp-protocol-explained/)
- [Claude Code MCP Setup: Connect AI to Any External Service](/posts/ai/2026-02-28-claude-code-mcp-setup/)
- [Claude Code Complete Guide 2026](/posts/ai/2026-02-28-claude-code-complete-guide/)
- [Claude Code Hooks: Automation Configs](/posts/ai/2026-02-28-claude-code-hooks-guide/)

## Related Reading

- [Build MCP Servers in Python: Complete Step-by-Step Tutorial](/posts/ai/2026-03-05-build-mcp-server-python/) — The Python alternative to this tutorial
- [MCP Protocol Explained: The Universal Standard for AI Integration](/posts/ai/2026-02-20-mcp-protocol-guide/) — Deep dive into MCP protocol architecture
- [Build an MCP Server with Claude Code: TypeScript Tutorial](/posts/ai/2026-02-22-claude-code-mcp-server-tutorial/) — Build MCP servers using Claude Code as your development tool
- [MCP Security Guide: Attack Patterns, Real CVEs, and Defense Strategies](/posts/ai/2026-02-23-mcp-security-guide/) — Secure your MCP servers before deploying
- [Best MCP Servers for Claude Code: 18 Tools You Need in 2026](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — Discover what others have built with MCP
