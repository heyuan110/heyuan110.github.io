+++
date = '2026-02-03T00:23:00+08:00'
draft = false
title = 'Claude-Mem Deep Dive: Persistent Memory Plugin for Claude Code'
description = 'Claude-Mem gives Claude Code cross-session persistent memory via hooks, AI compression, hybrid search, and Endless Mode. Full architecture breakdown and comparison with native CLAUDE.md.'
toc = true
tags = ['Claude Code', 'Claude-Mem', 'AI Memory', 'Plugin Architecture', 'MCP']
categories = ['AI Guides']
keywords = ['Claude-Mem', 'Claude Code memory', 'AI persistent memory', 'Claude Code plugin', 'cross-session context']
+++

![Claude-Mem architecture diagram showing the persistent memory plugin for Claude Code](cover.webp)

The most frustrating thing about Claude Code is not when it writes bad code. It is when **every new session starts with a blank slate**. The architecture discussion from yesterday, the bug you spent two hours tracking down, the coding conventions you agreed on — all gone. You end up repeating context over and over, like introducing yourself every morning to someone with amnesia.

[Claude-Mem](https://github.com/thedotmack/claude-mem) was built to fix this. It is a Claude Code plugin that **automatically captures every interaction, compresses it into structured memory using AI, and intelligently injects relevant context into future sessions**. In short, it gives Claude Code a long-term memory system.

By the end of this article, you will understand:

- How Claude-Mem's core architecture is designed
- How its Hook system captures context transparently
- How three-tier progressive search saves 10x on tokens
- How Endless Mode breaks through context window limits
- How it compares to the native CLAUDE.md memory system

## Why You Need Claude-Mem

### The Amnesia Problem

Claude Code has a 200K token context window (Claude Sonnet 4). That sounds large, but in practice each tool call consumes 1,000 to 10,000 tokens. A moderately complex development task with 50 tool calls can fill the entire window. More critically, **once a session ends, all context vanishes**.

This means:
- Architecture decisions discussed yesterday need to be explained again today
- A bug you spent hours debugging requires a fresh investigation in a new session
- Team coding conventions must be manually restated every time

### Limitations of Existing Solutions

Claude Code natively provides the `CLAUDE.md` memory mechanism — you place a Markdown file in your project root, and Claude reads it automatically at startup. This works, but has clear limitations:

| Pain Point | Description |
|------------|-------------|
| **Manual maintenance** | You decide what to remember and what to forget |
| **Static content** | Does not automatically record discoveries and decisions |
| **No search** | Finding specific information becomes harder as the file grows |
| **Context overhead** | Larger files leave fewer tokens for actual work |

Claude-Mem takes a fundamentally different approach: **let AI decide what to remember, how to compress it, and when to inject it**.

## Core Architecture: Five Layers Working Together

Think of Claude-Mem's architecture as a smart archive. Hooks are the archivists (they collect information), the Worker is the librarian (it classifies and compresses), databases are the filing cabinets (they store everything), the search system is the index desk (it retrieves), and SessionStart injection is your daily briefing.

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│                Claude Code IDE               │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
│  │Session  │ │UserPrompt│ │ PostToolUse  │  │
│  │Start    │ │Submit    │ │              │  │
│  │Hook     │ │Hook      │ │ Hook         │  │
│  └────┬────┘ └────┬─────┘ └──────┬───────┘  │
│       │           │              │           │
└───────┼───────────┼──────────────┼───────────┘
        │           │              │
        ▼           ▼              ▼
┌─────────────────────────────────────────────┐
│          Worker Service (Port 37777)         │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ Context     │  │ Session Manager      │  │
│  │ Builder     │  │ (AI Agent Generator) │  │
│  └─────────────┘  └──────────────────────┘  │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ Search      │  │ SSE Broadcaster      │  │
│  │ Manager     │  │ (Real-time Events)   │  │
│  └─────────────┘  └──────────────────────┘  │
└────────┬──────────────────┬─────────────────┘
         │                  │
         ▼                  ▼
┌────────────────┐  ┌────────────────┐
│  SQLite + FTS5 │  │ ChromaDB       │
│  (Structured)  │  │ (Embeddings)   │
└────────────────┘  └────────────────┘
```

The system consists of six Hook scripts, an HTTP Worker service, dual-database storage, and 4 MCP tools. Let us break down each layer.

### The Hook System: Transparent Capture

Claude-Mem leverages Claude Code's [Hook lifecycle](https://code.claude.com/docs/en/plugins) to inject logic at five critical moments:

| Hook | Trigger | Purpose |
|------|---------|---------|
| **Smart Install** | Before session start | Checks dependencies (Bun, uv, etc.), installs what is missing |
| **SessionStart** | Session begins | Retrieves relevant context from the last 10 sessions and injects it |
| **UserPromptSubmit** | User sends a message | Records user input and session metadata |
| **PostToolUse** | After each tool call | Captures observation from tool operations (file reads, code changes, etc.) |
| **Stop/SessionEnd** | Session ends | Uses AI to generate a semantic summary for the next session |

A key design choice: all Hooks are lightweight HTTP clients (each roughly 75 lines of code after the v7.0 refactor). They only send requests to the Worker Service and **perform no heavy computation**. This ensures Hooks never slow down Claude Code's response time.

```javascript
// PostToolUse Hook core logic (simplified)
// After capturing a tool call, immediately send it async to Worker
const response = await fetch(`http://127.0.0.1:37777/api/sessions/observations`, {
  method: 'POST',
  body: JSON.stringify({
    session_id: currentSessionId,
    tool_name: toolResult.name,
    tool_input: toolResult.input,
    tool_output: toolResult.output
  })
});
// Returns 202 Accepted, does not wait for processing
```

### Worker Service: The Central Orchestrator

The Worker Service is the brain of the entire system, running on Bun and listening on `127.0.0.1:37777` by default. It uses a **two-phase startup**:

- **Phase 1 (fast)**: HTTP server binds the port immediately and returns control to the Hook (prevents timeout)
- **Phase 2 (background)**: Initializes databases, crash recovery, SearchManager, and MCP connections

Core responsibilities include:

1. **Session management**: Tracks active development sessions with dual ID mapping (IDE session ID to memory agent session ID)
2. **AI agent dispatch**: Generates observations and summaries in the background
3. **Search orchestration**: Coordinates hybrid search across SQLite FTS5 and ChromaDB
4. **Real-time broadcasting**: Pushes events to the Web UI via SSE (Server-Sent Events)
5. **Crash recovery**: Scans the `pending_messages` table on startup and retries incomplete tasks

### Three-Layer Storage Architecture

Claude-Mem uses triple-redundant storage:

**SQLite (structured data)**:
- Database location: `~/.claude-mem/claude-mem.db`
- Core tables: `sdk_sessions`, `observations`, `session_summaries`, `user_prompts`, `pending_messages`
- Uses FTS5 virtual tables for keyword full-text search
- The `pending_messages` table ensures crash recovery — any unprocessed work is persisted

**ChromaDB (vector embeddings)**:
- Location: `~/.claude-mem/vector-db/`
- Each observation field (title, narrative, facts) is stored as an independent vector
- `ChromaSync` handles asynchronous syncing with smart backfill strategies

**File system**:
- `~/.claude-mem/settings.json`: Configuration file
- `~/.claude-mem/logs/`: Runtime logs
- Optional `CLAUDE.md` activity timeline file

## AI Compression Engine: 10:1 to 100:1 Ratios

### What Is an Observation?

Every time you use Claude Code to read a file, write code, or run a command, the PostToolUse Hook captures the raw tool input and output. But raw data is too large — a single file read can be thousands of tokens.

Claude-Mem's AI agent **compresses this raw data into structured observations of roughly 500 tokens**, containing:

```json
{
  "id": "obs_20260203_001",
  "type": "discovery",
  "title": "Found race condition in API auth middleware",
  "narrative": "While investigating intermittent 401 errors on /api/users...",
  "facts": [
    "Auth middleware does not lock during token expiry",
    "Concurrent requests can trigger simultaneous token refreshes",
    "Fix: use mutex to ensure single refresh"
  ],
  "concepts": ["problem-solution", "gotcha"],
  "session_id": "sess_abc123",
  "timestamp": "2026-02-03T00:00:00Z"
}
```

Think of it as compressing a book into high-quality reading notes — preserving core insights while discarding redundant details.

### Three AI Engine Options

Claude-Mem supports three AI providers with hot-swapping at runtime (shared conversation history, no context loss):

| Engine | Advantage | Best For |
|--------|-----------|----------|
| **SDKAgent** (default) | Uses Claude Agent SDK, highest observation quality | Best results, included in Claude Code subscription |
| **GeminiAgent** | Free tier with 1,500 requests/day, rate limiting | Budget-conscious, lightweight usage |
| **OpenRouterAgent** | 100+ models available, some free | Flexible model selection, experimentation |

All engines automatically fall back to SDKAgent when encountering errors (429/5xx).

## Three-Tier Progressive Search: 10x Token Savings

Traditional RAG (Retrieval-Augmented Generation) typically dumps everything retrieved into the context. In a token-scarce environment, this is extremely wasteful. Claude-Mem implements a **progressive disclosure** search pattern:

### The Three-Tier Workflow

```
Tier 1: Index Search (~50-100 tokens per entry)
    │  Returns observation ID, title, date, type
    │  Quick filtering to find entries of interest
    ▼
Tier 2: Timeline Context
    │  Shows timeline around an anchor observation
    │  Understand causal relationships and decision chains
    ▼
Tier 3: Full Details (~500-1000 tokens per entry)
    │  Retrieves full text only for selected observations
    │  Final confirmation of needed information
    ▼
  Result: ~10x token savings compared to traditional RAG
```

The elegance of this design is **filter first, fetch later**. It is like visiting a library: you would not carry every book off the shelf before choosing. You check the catalog, find the chapter, then turn to the specific page.

### Hybrid Search Strategy

SearchManager invokes three search strategies simultaneously and fuses the results:

- **ChromaStrategy**: Vector similarity search via ChromaDB, excels at semantic matching ("that auth bug I fixed yesterday")
- **SQLiteStrategy**: Keyword search via FTS5, excels at exact matching ("401 error")
- **HybridStrategy**: Relevance fusion ranking, combining the strengths of both

### MCP Tool Interface

Claude-Mem exposes search capabilities through 4 MCP tools:

| Tool | Function | Token Cost |
|------|----------|------------|
| `search` | Returns compact index | ~50-100/entry |
| `timeline` | Timeline context | Medium |
| `get_observations` | Full observation details | ~500-1000/entry |
| `__IMPORTANT` | Workflow documentation | One-time |

A major optimization in v7.0 was **consolidating 9 MCP tools (~2,500 tokens) into 1 Skill (~250 tokens preamble + on-demand instructions)**, dramatically reducing token overhead during tool registration.

## Context Injection: Your Session Briefing

### The Injection Flow

When you start a new Claude Code session, the SessionStart Hook triggers context injection:

1. Sends a `GET /api/context/inject` request to the Worker
2. ContextBuilder retrieves up to 50 relevant observations from the last 10 sessions (both configurable)
3. Ranks by relevance using hybrid search
4. Formats as Markdown and injects into the new session

### Fine-Grained Configuration

You can tune injection parameters in the Web UI at `http://localhost:37777`:

```json
{
  "CLAUDE_MEM_CONTEXT_OBSERVATIONS": 50,
  "CLAUDE_MEM_CONTEXT_SHOW_LAST_SUMMARY": false,
  "CLAUDE_MEM_CONTEXT_SHOW_LAST_MESSAGE": false,
  "CLAUDE_MEM_SKIP_TOOLS": [
    "ListMcpResourcesTool",
    "SlashCommand",
    "Skill"
  ]
}
```

Filtering by type (bugfix, feature, refactor, etc.) and concept (how-it-works, problem-solution, gotcha, etc.) is also supported, giving you precise control over what information enters the new session.

### Token Economics

From v3 to v7, context injection token consumption went through a massive improvement:

| Version | Context Injection | Notes |
|---------|-------------------|-------|
| v3 | ~25,000 tokens | Full dump, brute force |
| v7 | ~1,500 tokens | Compression + progressive loading |

**A 94% reduction in tokens**, meaning far more of the context window is available for actual coding work.

## Endless Mode: Breaking the Context Window Barrier

### The Problem: O(N squared) Token Consumption

Standard Claude Code sessions have **quadratic token growth**. Each tool call not only adds new content but also retains all previous tool outputs in the context. After roughly 50 tool calls, the 200K context window is full.

### The Solution: Bionic Memory Architecture

Endless Mode (currently in Beta) implements a two-tier memory system inspired by human cognition:

```
┌───────────────────────────────┐
│  Working Memory               │  ← In context window
│  Compressed observations,     │
│  ~500 tokens each             │
│  (like short-term memory)     │
└───────────────┬───────────────┘
                │ Compression
                ▼
┌───────────────────────────────┐
│  Archive Memory               │  ← On disk
│  Full tool outputs,           │
│  retrieved on demand          │
│  (like long-term memory)      │
└───────────────────────────────┘
```

**How it works**: The PostToolUse Hook **blocks after each tool call** (up to 110 seconds), allowing the AI agent to compress the full tool output into a ~500 token observation. The compressed observation then **replaces** the original output in the context. The full output is archived to disk.

**Results**:
- Token consumption drops from O(N squared) to O(N)
- ~95% reduction in tokens within the context window
- Tool call capacity increases roughly 20x

### Trade-offs

Endless Mode is not a free lunch:

| Benefit | Cost |
|---------|------|
| Massively extends single-session capacity | Adds 60-90 seconds latency per tool call |
| Context never overflows | Compression may lose details |
| Great for extended development tasks | Still experimental, may have bugs |

Best suited for scenarios where you need to **work continuously in a single session for a long time** — large refactors, complex bug investigations, multi-module development.

## Comparison with Native CLAUDE.md

A common question: Claude Code already has a `CLAUDE.md` memory system. Why would you need Claude-Mem?

### The Fundamental Differences

| Dimension | CLAUDE.md (Native) | Claude-Mem |
|-----------|---------------------|------------|
| **Memory method** | Manually written and maintained | AI auto-captures and compresses |
| **Content type** | Static rules, preferences, conventions | Dynamic work history and decision records |
| **Search** | None (full file loaded into context) | Semantic search + keyword search |
| **Token efficiency** | Wastes more as file grows | Progressive loading, on-demand retrieval |
| **Privacy control** | .local.md excluded from repo | `<private>` tag for fine-grained control |
| **Version control** | Git-friendly | Independent database storage |
| **Team collaboration** | Can be committed and shared | Personal memory, does not sync across devices |

### They Are Complementary, Not Competing

The best practice is to **use both together**:

- **CLAUDE.md**: Store project-level static knowledge — tech stack, coding conventions, architecture principles, common commands
- **Claude-Mem**: Automatically record dynamic work processes — bug investigation trails, architecture decision rationale, approaches you have tried

Think of it like a company's employee handbook (CLAUDE.md) versus work journal (Claude-Mem) — one tells you the rules, the other records what you did.

Some developers have proposed a [two-tier memory architecture](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d):

- **Tier 1 (CLAUDE.md, ~150 lines)**: Auto-generated concise briefing with the most important project knowledge
- **Tier 2 (full database)**: Complete storage of all facts, decisions, and observations, queried on demand via MCP tools

80% of sessions only need Tier 1, with the remaining 20% fetching from Tier 2 as needed.

## Installation and Configuration

### Quick Install

Run these commands in Claude Code:

```bash
# Add from plugin marketplace
> /plugin marketplace add thedotmack/claude-mem

# Install the plugin
> /plugin install claude-mem
```

After restarting Claude Code, context from previous sessions will automatically appear in new sessions.

### Key Configuration Options

After installation, the configuration file is at `~/.claude-mem/settings.json`. Here are the most commonly adjusted parameters:

| Setting | Default | Description |
|---------|---------|-------------|
| `CLAUDE_MEM_PROVIDER` | `claude` | AI engine: claude / gemini / openrouter |
| `CLAUDE_MEM_MODEL` | `claude-sonnet-4-5` | Specific model |
| `CLAUDE_MEM_CONTEXT_OBSERVATIONS` | `50` | Number of observations to inject (1-200) |
| `CLAUDE_MEM_WORKER_PORT` | `37777` | Worker service port |
| `CLAUDE_MEM_LOG_LEVEL` | `INFO` | Log level: DEBUG/INFO/WARN/ERROR/SILENT |
| `CLAUDE_MEM_SKIP_TOOLS` | Multiple system tools | Tools excluded from observation capture |

### Web Dashboard

Visit `http://localhost:37777` to view in real time:

- Current session's observation stream
- Historical session list and summaries
- Memory database search
- Context injection parameter tuning (with live preview)
- Stable / Beta version switching

### Privacy Protection

If you want certain content excluded from memory, use the privacy tag in your conversation with Claude:

```
<private>
This content contains sensitive information. Do not record it to memory.
API Key: sk-xxx...
</private>
```

You can also exclude specific tools from observation capture in the configuration.

## FAQ and Troubleshooting

### Does Claude-Mem slow down Claude Code?

**Not in normal mode**. All Hooks are asynchronous — they send HTTP requests to the Worker and return immediately without waiting for processing. However, Endless Mode does add noticeable latency (60-90 seconds per tool call).

### Is the data secure?

All data is stored locally (`~/.claude-mem/`), nothing is uploaded to any cloud service. The Worker only listens on `127.0.0.1`, so it is inaccessible from outside. AI compression uses your own Claude subscription (or a configured third-party API key).

### How much disk space does it use?

The SQLite database typically stays in the tens of MB range. ChromaDB vector embeddings may be slightly larger, but negligible for modern drives. If it grows too large over time, you can manually clean up historical sessions.

### Is it compatible with Git Worktrees?

Yes. Claude-Mem supports unified Git Worktree context, so multiple worktrees can share the same memory database.

### What does the AGPL-3.0 license mean?

For **personal use**, there are no restrictions. But if you modify Claude-Mem's code and deploy it as a network service (SaaS), you must open-source your modifications. Note that the `ragtime/` directory uses the PolyForm Noncommercial License, which is limited to non-commercial use.

## Conclusion

Claude-Mem addresses one of the most fundamental pain points with AI coding assistants — **memory continuity**. Its core value lies in:

1. **Transparent operation**: No manual effort after installation; Hooks capture everything automatically
2. **Smart compression**: AI-driven observation generation with 10:1 to 100:1 compression ratios
3. **Precise retrieval**: Three-tier progressive search that fetches only what is needed
4. **Token efficiency**: From 25K tokens in v3 down to 1.5K tokens in v7

Of course, it has limitations: dependency on a background Worker service, noticeable Endless Mode latency, and unsuitability for team-shared memory. For most individual developers, the **CLAUDE.md + Claude-Mem combination** is currently the most practical memory solution for Claude Code.

If you use Claude Code daily and are tired of repeating context every session, Claude-Mem is worth trying. After all, an AI assistant that actually remembers things is the one you will want to keep using.

## Related Reading

- [CLAUDE.md Memory Management Guide](/posts/ai/2026-01-12-claudemd-memory-guide/)
- [Claude Code Best Practices: Complete Guide](/posts/ai/2026-01-06-claudecode-best-practices/)
- [Claude Code Skills Deep Dive: Custom Skill System](/posts/ai/2026-01-08-claudecode-skill-guide/)
- [Claude Code Browser Automation in Practice](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Superpowers Skills Deep Dive](/posts/ai/2026-02-01-superpowers-deep-dive/)
