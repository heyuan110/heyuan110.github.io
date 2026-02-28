+++
date = '2026-02-28T09:00:00+08:00'
draft = false
title = 'Claude Code MCP Setup: Connect AI to Any External Service'
description = 'Complete guide to setting up MCP servers with Claude Code — from installing community servers to building your own TypeScript MCP server. Includes debugging tips, real examples, and production patterns.'
toc = true
tags = ['Claude Code', 'MCP', 'TypeScript', 'Tutorial']
categories = ['AI Guides']
keywords = ['Claude Code MCP', 'MCP setup guide', 'MCP server tutorial', 'Model Context Protocol', 'Claude Code MCP server', 'build MCP server', 'MCP TypeScript tutorial']
+++

Out of the box, Claude Code can read files, run shell commands, and search code. But what if you need it to query your Postgres database, send a Slack message, or hit your company's internal API?

That's exactly what MCP solves. The **Model Context Protocol** is an open standard that lets you plug any external service into Claude Code — no prompt hacking, no copy-pasting data, no brittle workarounds. Think of it as **USB-C for AI**: a single, universal connector between your AI assistant and every tool you care about.

This guide covers everything from installing your first community MCP server to building a custom one from scratch in TypeScript. By the end, you'll know how to make Claude Code talk to anything.

> **Prerequisites**: You should have Claude Code installed and working. If you haven't set that up yet, follow our [Claude Code setup guide](/posts/ai/2026-02-25-claude-code-setup-guide/) first.

## What Is MCP? The Architecture in 60 Seconds

MCP stands for **Model Context Protocol**. Anthropic released it as an open specification in late 2024, and it has since become the standard way to extend AI coding tools.

Here's the architecture:

```
┌─────────────────────────────────────────────────────┐
│              MCP Client (Host)                      │
│     Claude Code / Cursor / VS Code Copilot          │
├─────────────────────────────────────────────────────┤
│              MCP Protocol Layer                     │
│           JSON-RPC 2.0 over STDIO or HTTP           │
├─────────────────────────────────────────────────────┤
│              MCP Server                             │
│   Your custom tools, data sources, prompt templates │
└─────────────────────────────────────────────────────┘
```

**The client** (Claude Code) sends requests. **The server** (your code or a community package) handles them. **The protocol** defines the message format between them.

An MCP server can expose three types of capabilities:

| Capability | What It Does | Example |
|-----------|-------------|---------|
| **Tools** | Let AI perform actions | Query a database, send a notification, create a GitHub issue |
| **Resources** | Let AI read data | Configuration files, user profiles, API documentation |
| **Prompts** | Predefined interaction templates | Code review checklist, bug report format, deployment summary |

**Tools** are by far the most commonly used capability. When Claude Code asks "Can I call the `query_database` tool?", that tool is provided by an MCP server.

### Why Not Just Use Shell Commands?

You might wonder: Claude Code can already run shell commands. Why bother with MCP?

Three reasons:

1. **Safety**. MCP tools have explicit schemas. Claude knows exactly what parameters a tool accepts, instead of constructing arbitrary shell commands.
2. **Discoverability**. Claude automatically sees all available MCP tools and knows when to use them. No need to explain in your prompt that "you can use `curl` to call our API."
3. **Reusability**. An MCP server works across every MCP-compatible client — Claude Code, Cursor, Windsurf, and more. Write once, use everywhere.

## Installing Community MCP Servers

The fastest way to start is by installing servers that other people have already built. The community has created MCP servers for GitHub, Slack, PostgreSQL, filesystem operations, and dozens of other services.

### The `claude mcp add` Command

Adding an MCP server to Claude Code takes one command:

```bash
claude mcp add <name> <command> [args...]
```

For example, to add the official filesystem MCP server:

```bash
claude mcp add filesystem npx @anthropic/mcp-filesystem /path/to/allowed/directory
```

This tells Claude Code: "There's an MCP server called `filesystem`. Start it by running `npx @anthropic/mcp-filesystem /path/to/allowed/directory`."

### Popular Community MCP Servers

Here are the most useful MCP servers you can install right now:

#### GitHub (Official)

```bash
claude mcp add github npx @anthropic/mcp-github
```

Gives Claude Code the ability to create issues, open pull requests, search repositories, and manage branches — all without you switching to the browser.

**Required**: Set the `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Or pass it inline:

```bash
claude mcp add github -e GITHUB_TOKEN=ghp_your_token_here npx @anthropic/mcp-github
```

#### Slack

```bash
claude mcp add slack npx @anthropic/mcp-slack
```

Lets Claude Code read and send Slack messages, search channels, and post updates. Useful for automated notifications when long-running tasks complete. (This pairs well with [Claude Code Hooks](/posts/ai/2026-02-18-claude-code-hooks-guide/) for full automation.)

**Required**: Set `SLACK_BOT_TOKEN` and `SLACK_TEAM_ID`.

#### PostgreSQL

```bash
claude mcp add postgres npx @anthropic/mcp-postgres "postgresql://user:pass@localhost:5432/mydb"
```

Claude can now query your database directly. It sees your schema, writes SQL, and returns results. Extremely useful for debugging data issues or generating reports.

#### Filesystem (Extended)

```bash
claude mcp add filesystem npx @anthropic/mcp-filesystem /Users/you/projects
```

While Claude Code already has built-in file access, the filesystem MCP server provides additional operations like directory tree visualization, file watching, and advanced search.

#### Context7 (Documentation Lookup)

```bash
claude mcp add context7 npx @anthropic/mcp-context7
```

Fetches up-to-date library documentation at query time. When Claude needs to use a library API it's unsure about, Context7 pulls the latest docs instead of relying on training data.

### Scope Options: Project vs User

By default, `claude mcp add` adds the server to your **project** scope — it's only available when you're working in the current directory.

You can change the scope:

```bash
# Available in all your projects (user scope)
claude mcp add --scope user github npx @anthropic/mcp-github

# Available only in this project (project scope — default)
claude mcp add --scope project postgres npx @anthropic/mcp-postgres "postgresql://..."
```

**Best practice**: Use **project scope** for project-specific servers (databases, project APIs) and **user scope** for universal tools (GitHub, Slack, filesystem).

## Managing MCP Servers

### List All Configured Servers

```bash
claude mcp list
```

Output looks like this:

```
Project servers:
  postgres: npx @anthropic/mcp-postgres postgresql://user:pass@localhost:5432/mydb

User servers:
  github: npx @anthropic/mcp-github
  slack: npx @anthropic/mcp-slack
```

### Remove a Server

```bash
claude mcp remove <name>
```

For example:

```bash
claude mcp remove postgres
```

### Check Server Status Inside Claude Code

Once you're in a Claude Code session, you can verify that MCP servers are connected:

```
/mcp
```

This slash command shows the status of all configured MCP servers, including whether they're running and what tools they expose.

### Updating Servers

Community MCP servers distributed via npm are updated automatically when you run them with `npx` (it always fetches the latest version). If you need a specific version:

```bash
claude mcp add github npx @anthropic/mcp-github@2.1.0
```

## Build Your Own MCP Server (TypeScript)

Community servers cover common use cases. But the real power of MCP is building servers tailored to your specific workflow. Let's build one step by step.

We'll create a **weather service** MCP server — simple enough to understand quickly, but it demonstrates all the patterns you need for real-world servers.

### Step 1: Initialize the Project

```bash
mkdir mcp-weather-server
cd mcp-weather-server
npm init -y
```

Install the MCP SDK and Zod (for input validation):

```bash
npm install @modelcontextprotocol/server zod
npm install -D typescript @types/node
```

### Step 2: Configure TypeScript and package.json

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
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

Update `package.json` — the critical parts are:

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

**Important**: You must set `"type": "module"`. The MCP SDK uses ES modules, and without this setting you'll get cryptic import errors.

### Step 3: Write the Server

Create `src/index.ts`:

```typescript
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio.js";
import { z } from "zod";

// Create the MCP server
const server = new McpServer({
  name: "weather-server",
  version: "1.0.0",
});

// Define a tool: get current weather
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
    // In a real server, you'd call a weather API here
    // For this example, we return mock data
    const temperature = units === "celsius" ? 22 : 72;
    const unitLabel = units === "celsius" ? "C" : "F";

    // IMPORTANT: Always use console.error for logging, never console.log
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

// Start the server using STDIO transport
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

Let's break down the key parts:

- **`McpServer`**: The main server class from the SDK.
- **`registerTool()`**: Registers a tool with a name, schema, and handler function.
- **`inputSchema` with Zod**: Defines what parameters the tool accepts, with types and descriptions. Claude reads these descriptions to understand how to use the tool.
- **`StdioServerTransport`**: Communicates over stdin/stdout. This is what Claude Code expects for local MCP servers.
- **`console.error` for logging**: This is critical. Stdout is the MCP protocol channel. If you use `console.log`, your log messages will corrupt the JSON-RPC messages and crash the server.

### Step 4: Build and Test

Build the TypeScript:

```bash
npm run build
```

Make the entry point executable:

```bash
chmod +x dist/index.js
```

Register the server with Claude Code:

```bash
claude mcp add weather node /absolute/path/to/mcp-weather-server/dist/index.js
```

**Important**: Use the absolute path to `dist/index.js`, not a relative path.

Now start Claude Code and try it:

```
What's the weather in Tokyo?
```

Claude Code should recognize that the `get_weather` tool is available and call it automatically.

### Step 5: Add Resources

Resources let Claude read data from your server without calling a tool. They're useful for configuration, documentation, or any data that Claude might need as context.

Add this to your `src/index.ts`, before the `main()` function:

```typescript
// Define a resource: list of supported cities
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

After rebuilding (`npm run build`), Claude Code can read the list of supported cities as context before making weather queries.

### Step 6: Add Prompts

Prompts are predefined interaction templates. They're useful when you want Claude to follow a specific format.

```typescript
// Define a prompt: weather briefing template
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

Now when a user invokes `/mcp` and selects the `daily-briefing` prompt, Claude Code will generate a weather briefing in the specified format.

## Debugging MCP Servers

MCP servers communicate over stdio, which makes debugging different from typical web servers. Here are the techniques that work.

### The Golden Rule: console.error, Not console.log

This is the single most common MCP server bug. It deserves repeating:

```typescript
// WRONG - This corrupts the JSON-RPC protocol channel
console.log("Processing request...");

// CORRECT - This goes to stderr, which is safe
console.error("Processing request...");
```

When you use `console.log`, your message gets mixed into the JSON-RPC messages on stdout. The MCP client receives garbage data and the server crashes with an unhelpful error.

### Enable SDK Debug Logging

Set the `MCP_DEBUG` environment variable to see protocol-level messages:

```bash
MCP_DEBUG=1 node dist/index.js
```

Or when registering with Claude Code:

```bash
claude mcp add weather -e MCP_DEBUG=1 node /path/to/dist/index.js
```

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `SyntaxError: Cannot use import statement` | Missing `"type": "module"` in package.json | Add `"type": "module"` to package.json |
| `ERR_MODULE_NOT_FOUND` | Wrong import path | Use `.js` extension in imports even for TypeScript files |
| Server starts but no tools appear | `registerTool()` not called before `connect()` | Register all tools before calling `server.connect()` |
| `Unexpected token` in client | Using `console.log` instead of `console.error` | Replace all `console.log` with `console.error` |
| Server times out | Long-running operation without progress | Add timeouts and progress callbacks |
| `ENOENT` when starting server | Wrong path in `claude mcp add` | Use absolute path to the built JS file |
| Tools appear but fail silently | Handler throws uncaught error | Wrap handler in try/catch with `console.error` |

### Testing Without Claude Code

You can test your MCP server manually using the MCP inspector:

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

This opens a web UI where you can browse tools, call them with test inputs, and see the raw JSON-RPC messages. It's invaluable for debugging before connecting to Claude Code.

### Checking Server Logs in Claude Code

While Claude Code is running, MCP server stderr output goes to Claude Code's log directory:

```bash
# macOS
ls ~/Library/Logs/Claude\ Code/mcp*.log

# Linux
ls ~/.local/share/claude-code/logs/mcp*.log
```

## Publishing Your MCP Server

Once your server works, you might want to share it with others.

### Publish to npm

1. Make sure `package.json` has the correct `name`, `version`, `bin`, and `description` fields:

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

2. Build and publish:

```bash
npm run build
npm publish
```

3. Now anyone can use your server:

```bash
claude mcp add weather npx mcp-weather-server
```

### List on awesome-mcp-servers

The [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) repository is the community index of MCP servers. Submit a pull request to add yours.

### Private Distribution

For company-internal servers, publish to a private npm registry or distribute via Git:

```bash
# Install from a private Git repo
claude mcp add internal-tools npx github:your-org/internal-mcp-tools
```

## Real-World MCP Patterns

The weather example teaches the basics. Here are patterns for production MCP servers.

### Pattern 1: Database Query Server

A server that lets Claude query your database safely:

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
    // Safety: only allow SELECT queries
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

// Expose schema as a resource so Claude understands the database
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

**Key insight**: Exposing the database schema as a Resource means Claude automatically understands your tables without you explaining them every session. This dramatically improves query accuracy.

### Pattern 2: API Wrapper Server

Wrapping your company's internal API as an MCP server:

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

**Pro tip**: Add the `-e` flag when registering to inject API credentials:

```bash
claude mcp add customer-api \
  -e API_BASE_URL=https://api.internal.company.com \
  -e API_TOKEN=your_token_here \
  node /path/to/dist/index.js
```

### Pattern 3: Multi-Tool Server

Real servers typically expose multiple related tools. Group related functionality into a single server:

```typescript
const server = new McpServer({
  name: "project-management",
  version: "1.0.0",
});

// Tool 1: List tasks
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
    // Implementation here
  }
);

// Tool 2: Create task
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
    // Implementation here
  }
);

// Tool 3: Update task status
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
    // Implementation here
  }
);
```

**Design principle**: Group tools that share the same authentication, data source, or domain. Don't create one server per tool — that wastes resources. Don't put unrelated tools together either — that makes maintenance harder.

## Combining MCP with CLAUDE.md and Hooks

MCP servers become even more powerful when combined with other Claude Code features.

### MCP + CLAUDE.md

In your [CLAUDE.md file](/posts/ai/2026-02-28-claude-code-claudemd-guide/), you can tell Claude when and how to use specific MCP tools:

```markdown
## MCP Tools

- Use the `query_database` tool to check data before making schema changes
- Always use `get_customer` to verify customer data instead of guessing
- After completing a task, use `send_slack_message` to notify #dev-updates
```

This gives Claude explicit guidance on which tools to reach for in different situations.

### MCP + Hooks

[Claude Code Hooks](/posts/ai/2026-02-18-claude-code-hooks-guide/) can automate actions around MCP tool usage. For example, you could set up a hook that logs every MCP tool call for auditing:

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

## Tips for Avoiding Common MCP Mistakes

If you're new to Claude Code, you might find our list of [10 common Claude Code mistakes](/posts/ai/2026-02-25-claude-code-mistakes/) helpful. Here are the MCP-specific pitfalls:

1. **Using `console.log` instead of `console.error`**. This is the #1 cause of MCP server crashes. Stdout is reserved for JSON-RPC protocol messages. All your debug output must go to stderr via `console.error`.

2. **Forgetting `"type": "module"` in package.json**. The MCP SDK uses ES module imports. Without this setting, Node.js tries CommonJS resolution and fails with confusing error messages.

3. **Using relative paths in `claude mcp add`**. Always use absolute paths. Claude Code resolves MCP commands from its own working directory, not yours.

4. **Not adding `.describe()` to Zod schemas**. Claude reads the descriptions to understand what each parameter means. Without descriptions, it has to guess — and it often guesses wrong.

5. **Putting too many unrelated tools in one server**. If your server has 20+ tools spanning different domains, Claude gets confused about which to use. Keep servers focused.

6. **Not handling errors in tool handlers**. An uncaught exception in your handler crashes the entire MCP server. Always wrap your handler logic in try/catch.

7. **Forgetting to rebuild after changes**. TypeScript changes require `npm run build` before they take effect. The server runs from `dist/`, not `src/`.

## FAQ

### MCP vs REST API: What's the Difference?

REST APIs are designed for application-to-application communication. MCP is designed for AI-to-tool communication. Key differences:

- **Discovery**: MCP servers advertise their capabilities (tools, resources, prompts). REST APIs require external documentation.
- **Schema**: MCP uses Zod schemas with human-readable descriptions. REST uses OpenAPI/Swagger.
- **Transport**: MCP typically runs over stdio for local servers (no port conflicts, no HTTP overhead). REST requires a running HTTP server.
- **Lifecycle**: Claude Code manages MCP server processes automatically — starts them when needed, stops them when done.

You can absolutely wrap a REST API as an MCP server (see Pattern 2 above). That's often the best approach.

### TypeScript vs Python SDK: Which Should I Choose?

Both are officially supported. Choose based on your team:

| Factor | TypeScript | Python |
|--------|-----------|--------|
| Package | `@modelcontextprotocol/server` | `mcp[cli]` |
| Best for | Web/Node.js teams | Data science, ML teams |
| Type safety | Zod schemas | Pydantic models |
| Ecosystem | npm, larger MCP community | pip, better for data tools |
| Claude Code integration | Excellent (native Node.js) | Excellent (via uvx or python) |

For Claude Code users, TypeScript has a slight edge because Claude Code itself runs on Node.js and has stronger TypeScript understanding.

### Can I Use MCP Servers with Other AI Tools?

Yes. MCP is an open standard. The same server works with:

- **Claude Code** (CLI)
- **Claude Desktop App**
- **Cursor** (IDE)
- **Windsurf** (IDE)
- **VS Code** with Copilot MCP extension
- **Cline** (VS Code extension)

Configuration differs per client, but the server code is identical. That's the whole point of having a protocol.

### How Many MCP Servers Can I Run Simultaneously?

There's no hard limit, but each server is a separate process consuming memory. Practical guidelines:

- **3-5 servers**: No noticeable performance impact
- **5-10 servers**: Slightly longer startup time
- **10+ servers**: Consider merging related servers or using on-demand activation

### Do MCP Servers Have Access to My Files?

Only if you give them access. An MCP server runs as a regular process with whatever permissions you grant. It cannot access your filesystem unless you explicitly pass directory paths as arguments or your server code reads files.

Claude Code will always ask for your permission before calling an MCP tool, unless you've pre-approved it in your [settings or CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/).

## Quick Reference

### Essential Commands

```bash
# Add an MCP server (project scope)
claude mcp add <name> <command> [args...]

# Add with environment variables
claude mcp add <name> -e KEY=value <command> [args...]

# Add to user scope (available in all projects)
claude mcp add --scope user <name> <command> [args...]

# List all configured servers
claude mcp list

# Remove a server
claude mcp remove <name>

# Check server status (inside Claude Code)
/mcp
```

### Minimal MCP Server Template

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
    console.error(`Processing: ${param}`); // stderr only!
    return {
      content: [{ type: "text" as const, text: `Result: ${param}` }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### package.json Essentials

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

## What to Build Next

Now that you understand MCP, here are some project ideas to try:

1. **Jira/Linear MCP server** — Create and update tickets without leaving the terminal
2. **Monitoring dashboard server** — Let Claude query your Datadog/Grafana metrics
3. **Code review server** — Expose your team's review checklist as an MCP prompt
4. **Deployment server** — Let Claude trigger deploys with safety checks built in
5. **Documentation server** — Search your internal docs and wikis from Claude Code

Each of these follows the same patterns we covered in this guide: initialize a project, define tools with Zod schemas, handle errors properly, and register with `claude mcp add`.

## Related Articles

- [Claude Code Setup Guide 2026](/posts/ai/2026-02-25-claude-code-setup-guide/) — Get Claude Code installed and configured
- [10 Claude Code Mistakes Beginners Make](/posts/ai/2026-02-25-claude-code-mistakes/) — Avoid the most common pitfalls
- [Claude Code Hooks Guide](/posts/ai/2026-02-18-claude-code-hooks-guide/) — Automate your Claude Code workflow
- [CLAUDE.md Guide](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — Configure project context for better AI results
