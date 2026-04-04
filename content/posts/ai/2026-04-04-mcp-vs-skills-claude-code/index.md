+++
date = '2026-04-04T09:00:00+08:00'
draft = false
title = 'MCP vs Skills vs Hooks in Claude Code: Which Extension Do You Need?'
description = 'Deep technical comparison of Claude Code MCP, Skills, and Hooks — protocol design, context costs, trigger mechanisms, and a decision framework for choosing the right extension.'
toc = true
tags = ['Claude Code', 'MCP', 'Skills', 'Hooks', 'AI Architecture']
keywords = ['MCP vs Skills Claude Code', 'Claude Code MCP Skills difference', 'Claude Code Hooks vs Skills', 'Model Context Protocol', 'Claude Code extensions comparison', 'when to use MCP vs Skills']

[[params.faqItems]]
question = "What is the main difference between MCP and Skills in Claude Code?"
answer = "MCP (Model Context Protocol) connects Claude Code to external services through a standardized protocol — it provides tools like database queries or browser automation. Skills are reusable instruction packages that teach Claude how to perform complex workflows using those tools and built-in capabilities. MCP is the infrastructure layer; Skills are the application layer."

[[params.faqItems]]
question = "When should I use Hooks instead of Skills?"
answer = "Use Hooks when something must happen reliably every time — they execute deterministic shell commands at lifecycle events like before/after tool use. Skills are best for complex workflows where Claude needs judgment. Hooks enforce rules; Skills encode expertise."

[[params.faqItems]]
question = "Do MCP servers consume more tokens than Skills?"
answer = "Yes, typically. MCP tool definitions stay resident in the context window at all times — a server with 20 tools can consume 2,000-5,000 tokens permanently. Skills use progressive disclosure: only ~100 tokens of metadata loads initially, and full instructions load on-demand when relevant."

[[params.faqItems]]
question = "Can Skills call MCP tools internally?"
answer = "Yes, and this is the recommended pattern for complex workflows. A Skill orchestrates the high-level logic — deciding what to do, in what order, and how to handle edge cases — while MCP tools handle the actual execution of external operations like API calls or database queries."

[[params.faqItems]]
question = "How many MCP servers should I connect to Claude Code?"
answer = "Most developers need 2-4 MCP servers. Each server adds tool definitions to your context window, so connecting too many causes context bloat and slower responses. Start with essentials (filesystem, GitHub) and add domain-specific servers as needed. If you find yourself connecting 10+ servers, consider whether some tasks would be better handled by Skills."
+++

![MCP vs Skills vs Hooks comparison in Claude Code](cover.webp)

Claude Code has three distinct extension mechanisms: **MCP** (Model Context Protocol), **Skills**, and **Hooks**. They look related on the surface, but they operate at fundamentally different layers of the system. Choosing the wrong one means wasted effort, bloated context windows, or brittle automation that breaks when you need it most.

This guide provides a deep technical comparison — how each extension works internally, what it costs in terms of tokens and complexity, and a clear decision framework for when to use which.

## The Three-Layer Architecture

Before diving into details, here is how the three extensions relate to each other:

```
┌─────────────────────────────────────────────────┐
│                   Skills Layer                   │
│   Reusable workflows, domain knowledge, logic   │
│   "How to do things well"                        │
├─────────────────────────────────────────────────┤
│                   MCP Layer                      │
│   External tool connections via open protocol    │
│   "What can be done"                             │
├─────────────────────────────────────────────────┤
│                   Hooks Layer                    │
│   Lifecycle event automation, enforcement        │
│   "What must always happen"                      │
└─────────────────────────────────────────────────┘
```

Skills sit at the top, orchestrating complex workflows. MCP provides the external capabilities. Hooks enforce rules at the bottom, guaranteeing certain actions always execute regardless of what the AI decides.

## MCP: The Protocol Layer

### What It Is

MCP is an open protocol standard built on JSON-RPC 2.0 that connects AI models to external services. Anthropic released it in late 2024, and it has since become the industry standard — now governed by the Linux Foundation with backing from OpenAI, Google, and Microsoft.

Think of MCP as the **USB-C port for AI**. Just as USB-C lets any peripheral connect to any computer through a standard interface, MCP lets any external service connect to any AI application through a standard protocol.

### How It Works

An MCP server exposes three types of capabilities:

| Capability | Description | Example |
|-----------|-------------|---------|
| **Tools** | Executable actions | `browser_click`, `db_query`, `send_email` |
| **Resources** | Readable data sources | Documents, config files, live data feeds |
| **Prompts** | Pre-built prompt templates | Code review template, bug report template |

When you connect an MCP server to Claude Code, all tool definitions (names, descriptions, parameter schemas) are loaded into the context window. The AI then decides when and how to call these tools during a conversation.

```json
// Example: Adding an MCP server in .claude/settings.json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-playwright"]
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost:5432/mydb"
      }
    }
  }
}
```

### Context Cost

This is where MCP has a significant trade-off. Every connected MCP server adds its tool definitions to the context window — **permanently**. A server with 15 tools might consume 1,500-3,000 tokens just for the definitions, whether you use those tools or not.

Connect five servers and you could burn 10,000+ tokens before asking a single question. This matters because context space is finite and directly affects response quality.

### When MCP Excels

- Connecting to external services (databases, APIs, browsers, cloud platforms)
- Standardized atomic operations that multiple AI applications share
- Cross-platform compatibility — one MCP server works with Claude Code, Cursor, VS Code Copilot, and any other MCP-compatible client

## Skills: The Application Layer

### What They Are

Skills are reusable instruction packages — a folder containing a `SKILL.md` file with YAML frontmatter and Markdown content. They encode **procedural knowledge**: not just what tools to call, but when, in what order, how to handle edge cases, and what the output should look like.

If MCP tools are LEGO bricks, Skills are the instruction manuals that show you how to build specific models.

### How They Work

Skills use a **progressive disclosure architecture** that operates in three stages:

1. **Metadata stage** (~100 tokens per Skill): Claude always sees the Skill's name and description. This is used to decide whether the Skill is relevant to the current task.

2. **Loading stage**: When Claude determines a Skill is relevant — either because the user invoked it via `/skill-name` or the conversation context matches — it reads the full SKILL.md content.

3. **Execution stage**: Claude follows the Skill's instructions, potentially calling MCP tools, running shell commands, or reading additional reference files bundled with the Skill.

```yaml
# Example: .claude/skills/code-review/SKILL.md
---
name: code-review
description: "Review code changes against team standards"
---

## Instructions

1. Run `git diff --staged` to see changes
2. Check each file against these criteria:
   - No hardcoded secrets or API keys
   - All public functions have JSDoc comments
   - Error handling follows project patterns
   - Tests exist for new logic
3. Output a structured review with severity levels
```

### Two Types of Skills

| Type | Purpose | Trigger | Example |
|------|---------|---------|---------|
| **Reference** | Adds knowledge Claude applies to current work | Auto-detected by context | Style guides, conventions, domain knowledge |
| **Task** | Step-by-step instructions for specific actions | Manual via `/skill-name` | Deployments, commits, code generation |

### Context Cost

Skills are dramatically more efficient than MCP for context management. With 20 Skills installed:

- **MCP equivalent**: 20 servers x ~2,000 tokens = 40,000 tokens always in context
- **Skills**: 20 Skills x ~100 tokens metadata = 2,000 tokens normally; full content loads only when needed

This progressive disclosure model means you can have dozens of Skills installed without any meaningful context overhead.

## Hooks: The Enforcement Layer

### What They Are

Hooks are shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific lifecycle events. Unlike MCP and Skills — where the AI decides what to do — Hooks fire **deterministically**. If you configure a Hook for `PostToolUse` on the `Write` tool, it runs every single time Claude writes a file. No exceptions.

### How They Work

Hooks are configured in `settings.json` with three components:

1. **Event**: Which lifecycle point triggers the Hook (e.g., `PreToolUse`, `PostToolUse`, `Stop`)
2. **Matcher**: Optional filter for when it fires (e.g., "only for the Bash tool")
3. **Handler**: What to execute — a shell command, HTTP call, or LLM prompt

```json
// Example: Auto-format after every file write
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

### Key Lifecycle Events

| Event | When It Fires | Common Use |
|-------|---------------|------------|
| `PreToolUse` | Before a tool executes | Block dangerous commands, validate inputs |
| `PostToolUse` | After a tool completes | Auto-format code, run linters |
| `Stop` | When Claude finishes responding | Send notifications, update dashboards |
| `SessionStart` | When a session begins | Load development context, set env vars |
| `SessionEnd` | When a session ends | Cleanup, save state |
| `PreCompact` | Before context compaction | Save important context |
| `PostCompact` | After context compaction | Restore critical information |

### Context Cost

Hooks have **zero context cost**. They run entirely outside the AI's context window as external processes. This makes them the most efficient extension mechanism — but also the most limited in terms of what they can do, since they cannot reason or make judgment calls.

## Side-by-Side Comparison

| Dimension | MCP | Skills | Hooks |
|-----------|-----|--------|-------|
| **What it is** | Open protocol for external tools | Reusable instruction packages | Lifecycle event automation |
| **Layer** | Infrastructure | Application | Enforcement |
| **Trigger** | AI decides when to call | User invokes or AI auto-detects | Fires on lifecycle events |
| **Intelligence** | AI reasons about tool use | AI follows structured workflows | No AI reasoning — deterministic |
| **Context cost** | High (always resident) | Low (progressive disclosure) | Zero |
| **Scope** | Cross-platform (any MCP client) | Claude Code only | Claude Code only |
| **Configuration** | `settings.json` mcpServers | `.claude/skills/` SKILL.md | `settings.json` hooks |
| **Best for** | External service connections | Complex workflows & knowledge | Mandatory automation |
| **Examples** | Database queries, browser control | Code review, deployment | Auto-format, command blocking |

## Decision Framework: When to Use Which

### Use MCP When...

You need to **connect to something external**. If the task requires reaching outside Claude Code's built-in capabilities — querying a database, calling an API, controlling a browser, accessing a cloud service — MCP is your answer.

**Rule of thumb**: If you are writing `curl` commands or API calls repeatedly in your prompts, you need an MCP server.

### Use Skills When...

You need to **encode expertise**. If you find yourself explaining the same multi-step workflow to Claude repeatedly — your team's code review process, your deployment checklist, your documentation format — package it as a Skill.

**Rule of thumb**: If you have copy-pasted the same instructions into Claude more than three times, it should be a Skill.

### Use Hooks When...

You need **guaranteed execution**. If something must happen every single time without fail — auto-formatting code after edits, blocking dangerous shell commands, running linters before commits — use a Hook.

**Rule of thumb**: If you would describe the requirement as "must always" or "must never," it is a Hook.

### The Combined Pattern

In practice, the most powerful setups use all three together:

```
Scenario: Deploying to production

Hook (PreToolUse):  Block `rm -rf` on production paths
Skill (/deploy):    Orchestrate the full deployment workflow
  ├── MCP (GitHub):   Create a release tag
  ├── MCP (Slack):    Notify the team channel
  ├── Built-in:       Run test suite
  └── Built-in:       Build and push Docker image
Hook (Stop):        Log deployment result to audit trail
```

The Hook prevents disasters, the Skill orchestrates the workflow, and MCP servers handle external communications.

## Same Task, Three Approaches

To make the differences concrete, here is how you might handle "format code after editing" with each mechanism:

### MCP Approach

Connect a Prettier MCP server that exposes a `format_file` tool. Claude decides whether to call it after editing. **Problem**: Claude might forget, or decide formatting is not needed. Adds tool definitions to context permanently.

### Skill Approach

Create a Skill that includes "always run Prettier after editing TypeScript files" in its instructions. Claude will follow this guidance when the Skill is active. **Problem**: Only works when the Skill is loaded. Claude could still skip it if context gets crowded.

### Hook Approach

Configure a `PostToolUse` Hook on the `Write` tool that runs `prettier --write` on every written file. Runs every time, no exceptions, zero context cost. **This is the right choice** for mandatory formatting.

The point is not that one mechanism is better — it is that each solves a different class of problem. Formatting is a deterministic requirement (Hook). A multi-step deployment is a complex workflow (Skill). Querying your production database is an external connection (MCP).

## Common Mistakes

### Mistake 1: Using MCP When You Need a Skill

Connecting 15 MCP servers and expecting Claude to figure out complex workflows from raw tools. This leads to context bloat and inconsistent results. Instead, create Skills that orchestrate a focused set of MCP tools.

### Mistake 2: Using Skills When You Need a Hook

Writing a Skill that says "always run the linter after editing code." Skills are guidance, not guarantees. Claude might skip the step under context pressure. If it must happen every time, use a Hook.

### Mistake 3: Ignoring Context Costs

Every MCP server you connect burns context tokens permanently. Audit your connected servers periodically — if you have not used a server in the last week, consider disconnecting it.

### Mistake 4: Not Combining Them

The three mechanisms are designed to work together. A Hook ensures formatting always runs. A Skill knows how to do a complete code review. An MCP server provides the GitHub integration. Using only one mechanism limits what you can build.

## Practical Recommendations

For most developers, a solid setup looks like:

1. **2-4 MCP servers**: Filesystem, GitHub, and 1-2 domain-specific servers
2. **5-10 Skills**: Code review, commit, deploy, documentation, and team-specific workflows
3. **3-5 Hooks**: Auto-formatting, dangerous command blocking, and session setup

Start minimal and add extensions as you identify repeated patterns. The goal is not maximum extensions — it is maximum efficiency with minimum context overhead.

## Related Reading

- [Skills vs MCP in Claude Code: Two Ways to Extend AI](/posts/ai/2026-01-06-skill&mcp/) — Earlier overview of Skills and MCP fundamentals
- [Claude Code MCP Setup: Connect AI to Any External Service](/posts/ai/2026-02-28-claude-code-mcp-setup/) — Hands-on guide to installing and building MCP servers
- [Claude Code Skills Guide: Create Custom SKILL.md Workflows](/posts/ai/2026-02-28-claude-code-skills-guide/) — Deep dive into creating production-ready Skills
- [Claude Code Hooks 2026: Complete Event List + Ready-to-Use Configs](/posts/ai/2026-02-28-claude-code-hooks-guide/) — All Hook events explained with copy-paste configurations
- [MCP Protocol Explained: The Universal Standard for AI Integration](/posts/ai/2026-02-20-mcp-protocol-guide/) — Complete technical breakdown of the MCP protocol architecture
