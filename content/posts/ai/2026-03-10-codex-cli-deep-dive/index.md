+++
date = '2026-03-10T10:00:00+08:00'
draft = false
title = 'Codex CLI Deep Dive: Setup, Config, and 20+ Power User Tips'
description = 'Master OpenAI Codex CLI with this complete guide. Installation, model switching, session recovery, MCP integration, security modes, and real Codex CLI vs Claude Code comparison.'
toc = true
tags = ['Codex CLI', 'OpenAI', 'AI Coding Tools', 'Terminal']
categories = ['AI Guides']
keywords = ['codex cli', 'codex cli tutorial', 'openai codex cli', 'codex cli setup', 'codex cli vs claude code', 'codex cli guide 2026', 'codex cli tips', 'codex cli mcp', 'codex cli pricing', 'ai terminal coding tool']

[[params.faqItems]]
question = "Is Codex CLI free to use?"
answer = "Codex CLI is free to install, but requires either a ChatGPT Plus/Pro subscription ($20-$200/month) or an OpenAI API key with credits. There is no free usage tier for running tasks."

[[params.faqItems]]
question = "What model does Codex CLI use?"
answer = "Codex CLI defaults to gpt-5.3-codex, a model specifically optimized for coding tasks. You can also switch to gpt-5 for complex reasoning or o4-mini for cost-sensitive simple tasks."

[[params.faqItems]]
question = "Can Codex CLI execute commands on my machine?"
answer = "Yes, but with safety controls. The default 'Auto' mode runs commands in an OS-level sandbox with file system isolation and network restrictions. You control what Codex can access through three permission modes: Auto, Read Only, and Full Access."

[[params.faqItems]]
question = "How does Codex CLI compare to Claude Code?"
answer = "Both are terminal-based AI coding agents. Codex CLI excels at sandboxed execution, session recovery, and CI/CD integration. Claude Code excels at deep reasoning, complex multi-step tasks, and interactive development. Many developers use both."

[[params.faqItems]]
question = "Does Codex CLI support MCP servers?"
answer = "Yes. Codex CLI supports both STDIO and HTTP-based MCP servers. You can add them via 'codex mcp add' command or by editing ~/.codex/config.toml. Popular integrations include Context7, Playwright, PostgreSQL, and Sentry."
+++

![Codex CLI deep dive guide with setup, configuration, and power user tips](cover.webp)

Most Codex CLI tutorials stop at "here are the commands." They translate the docs and call it a day. This guide goes deeper — covering the **configuration architecture**, **security model philosophy**, **real-world workflow patterns**, and **honest comparison with Claude Code** that you won't find in surface-level articles.

By the end, you'll have:
- A **production-ready Codex CLI configuration** you can copy and use immediately
- Deep understanding of the **sandbox security model and permission system**
- **20+ battle-tested tips** for daily development
- An **objective Claude Code comparison** to help you choose the right tool

## What Is Codex CLI?

Codex CLI is not "ChatGPT in a terminal." It's OpenAI's **local AI coding agent** that can:

- **Read your entire codebase** and understand project structure
- **Edit files directly** — not suggestions, actual changes
- **Execute shell commands** — run tests, install dependencies, manage Git
- **Connect to external tools via MCP** — Figma, Sentry, databases, and more
- **Run everything in an OS-level sandbox** — your system stays safe

Think of it as a senior developer sitting next to you. You describe what you need, and it writes the code, runs the tests, and fixes the bugs.

### Architecture Overview

```
┌─────────────────────────────────────────┐
│           Codex CLI (TUI)               │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Composer    │  │  Approval Engine │  │
│  │  (input UI)  │  │  (permissions)   │  │
│  └─────────────┘  └──────────────────┘  │
│  ┌─────────────────────────────────────┐ │
│  │         Sandbox (OS-level)          │ │
│  │  - File system isolation            │ │
│  │  - Network access control           │ │
│  │  - Process execution limits         │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  MCP Client │  │  Web Search      │  │
│  │  (tools)    │  │  (live/cached)   │  │
│  └─────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
              │
              ▼
     OpenAI API (gpt-5.3-codex)
```

The key design decision: Codex CLI uses a **local execution + cloud reasoning** hybrid. Your code stays on your machine — only necessary context goes to OpenAI's API. This differs from the cloud-based Codex Agent in ChatGPT, which runs in a remote sandbox.

## Installation and Setup

### Install Codex CLI

```bash
# macOS / Linux
npm install -g @openai/codex

# Or via Homebrew (macOS)
brew install openai-codex

# Verify installation
codex --version
```

### Authentication: Two Methods

Most tutorials skip this, but the choice matters:

**Method 1: ChatGPT Subscription (Default)**

```bash
codex login
# Opens browser for OAuth authentication
```

Best for ChatGPT Plus/Pro/Enterprise users — usage is included in your subscription.

**Method 2: API Key**

```bash
# Edit ~/.codex/config.toml
preferred_auth_method = "apikey"

# Or switch temporarily
codex --config preferred_auth_method="apikey"
```

Best for precise cost control, CI/CD pipelines, or users without a ChatGPT subscription.

**Pro tip**: You can switch between methods anytime. A practical strategy: use your ChatGPT subscription for daily work, then switch to API key when your subscription quota runs out:

```bash
# Switch back to ChatGPT auth
codex --config preferred_auth_method="chatgpt"
```

### API Pricing

If using API authentication, know the costs:

| Model | Best For | Notes |
|-------|----------|-------|
| gpt-5.3-codex | Code generation (default) | Optimized specifically for coding |
| gpt-5 | Complex reasoning, code review | General-purpose flagship |
| o4-mini | Simple tasks, cost-sensitive | Lightweight reasoning model |

> For the latest pricing, see [OpenAI API Pricing](https://openai.com/api/pricing/).

## Configuration Deep Dive

### The Five-Layer Config System

This is something most guides completely miss — Codex CLI doesn't have a single config file. It has a **five-layer priority system**:

```
CLI args & --config overrides      ← Highest priority
       │
Profile config (--profile)
       │
Project config (.codex/config.toml)
       │
User config (~/.codex/config.toml)
       │
System config (/etc/codex/config.toml)
       │
Built-in defaults                  ← Lowest priority
```

### The Complete User Config

Here's a production-ready `~/.codex/config.toml` you can use as a starting point:

```toml
# ~/.codex/config.toml

# Default model
model = "gpt-5.3-codex"

# Approval policy
approval_policy = "on-request"

# Sandbox mode
sandbox_mode = "workspace-write"

# Web search
web_search = "live"    # "cached" | "live" | "disabled"

# Reasoning effort
model_reasoning_effort = "high"

# Communication style
personality = "pragmatic"    # "friendly" | "pragmatic" | "none"

# Feature flags
[features]
shell_snapshot = true
undo = true
web_search = true

# Trusted projects (skip trust prompt)
[projects."/Users/me/work/my-project"]
trust_level = "trusted"
```

### Profiles: Better Than Aliases

Instead of shell aliases, use Codex's built-in profile system:

```toml
# ~/.codex/config.toml

# Default config (always applied)
model = "gpt-5.3-codex"
model_reasoning_effort = "high"
web_search = "live"

# Code review profile
[profiles.review]
sandbox_mode = "read-only"
approval_policy = "never"

# Quick mode profile
[profiles.quick]
model = "o4-mini"
model_reasoning_effort = "medium"
web_search = "disabled"

# Full auto profile (use with caution)
[profiles.auto]
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Switch profiles on the fly:

```bash
codex --profile review   # Read-only code review
codex --profile quick    # Fast, cheap answers
codex                    # Default high-power config
```

Why profiles beat aliases: **centralized management**. Change one file instead of editing `.zshrc`.

### Shell Aliases (If You Still Want Them)

```bash
# Add to ~/.zshrc or ~/.bashrc

# Daily development: high reasoning + web search
alias cx='codex -m gpt-5.3-codex -c model_reasoning_effort="high" --search'

# Code review: read-only, no approvals needed
alias cxr='codex -m gpt-5.3-codex --sandbox read-only --ask-for-approval never'

# Quick Q&A: lightweight model, save costs
alias cxq='codex -m o4-mini -c model_reasoning_effort="medium"'

# CI/CD script mode: non-interactive
alias cxci='codex exec'
```

### Debug Your Config

When settings don't seem to apply, use `/debug-config` to see the complete loading chain:

```
Config Layer 1: /etc/codex/config.toml (not found)
Config Layer 2: ~/.codex/config.toml (loaded)
Config Layer 3: /project/.codex/config.toml (loaded)
Config Layer 4: Profile "review" (active)
Config Layer 5: CLI overrides: model_reasoning_effort=high
```

## Security Model: Sandbox and Permissions

### Three Permission Modes

| Permission | Auto (Default) | Read Only | Full Access |
|-----------|----------------|-----------|-------------|
| Read files | Yes | Yes | Yes |
| Edit files | Yes | No | Yes |
| Run commands in workspace | Yes | No | Yes |
| Access files outside workspace | Needs approval | No | Yes |
| Network access | Needs approval | No | Yes |

### Fine-Grained Permission Control

Beyond the three presets, combine flags for precise control:

```bash
# Auto-edit, but approve untrusted commands
codex --sandbox workspace-write --ask-for-approval untrusted

# Read-only, never ask (pure analysis mode)
codex --sandbox read-only --ask-for-approval never

# Full auto with sandbox (reduced friction)
codex --full-auto

# Completely bypass everything (DANGEROUS - isolated environments only)
codex --dangerously-bypass-approvals-and-sandbox
# Alias: --yolo (yes, OpenAI really named it that)
```

### --full-auto vs --yolo: Know the Difference

Many users confuse these two options. The distinction is critical:

| Aspect | `--full-auto` | `--yolo` |
|--------|--------------|----------|
| Sandbox | **Preserved** | **Completely disabled** |
| Approvals | Reduced prompts | **All disabled** |
| Network | Still sandboxed | **Wide open** |
| Use case | Daily development (low friction) | CI/CD in isolated containers |
| Safety | Reasonably safe | **Dangerous** |

**Bottom line**: `--full-auto` is for daily work with less friction. `--yolo` is for Docker containers and CI/CD pipelines. Never use `--yolo` on your main machine.

### Approval Policy Levels

```bash
# untrusted: only untrusted commands need approval (default)
codex -a untrusted

# on-failure: approve only when a command fails
codex -a on-failure

# on-request: approve only when Codex explicitly asks
codex -a on-request

# never: never ask for approval
codex -a never
```

## All 24 Slash Commands Explained

Codex CLI has 24 slash commands — far more than most guides cover. Here's the complete reference, grouped by function:

### Session Control

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `/new` | Start fresh session | Done with current task, starting something new |
| `/resume` | Restore past session | Coming back to unfinished work |
| `/fork` | Clone current session | Want to try an alternative approach without losing progress |
| `/quit` / `/exit` | Exit CLI | Done for the day |
| `/compact` | Compress context | Running low on context window |

**`/fork` is the most underrated command.** Imagine you're implementing a feature with approach A, halfway through you want to try approach B. Without `/fork`, you lose approach A's progress or start fresh. With `/fork`, you branch off — both approaches preserved.

### Model and Style

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `/model` | Switch model and reasoning level | Need different power/cost for current task |
| `/personality` | Change communication style | Want friendlier or more direct responses |
| `/plan` | Enter planning mode | Complex task that needs a strategy before execution |

**`/plan` best practice**: For big tasks like "refactor the entire auth module," always use `/plan` first. Let Codex outline the steps, review them, then proceed. Much safer than letting it charge ahead.

### Permissions and Status

| Command | What It Does |
|---------|-------------|
| `/permissions` | Switch between Auto/Read Only/Full Access at runtime |
| `/status` | View session info, token usage, account details |
| `/statusline` | Customize the bottom status bar |
| `/debug-config` | Print complete config loading chain |

### Files and Tools

| Command | What It Does |
|---------|-------------|
| `/mention` | Add files/directories to context with fuzzy search |
| `/diff` | View Git changes including untracked files |
| `/review` | Code review with branch comparison support |
| `/mcp` | List all configured MCP tools |
| `/apps` | Browse ChatGPT app connectors |
| `/ps` | Check background task status |

### Other

| Command | What It Does |
|---------|-------------|
| `/init` | Generate AGENTS.md for your project |
| `/feedback` | Send diagnostic logs to OpenAI |
| `/logout` | Clear local credentials |

## Session Recovery: Never Lose Progress

This feature alone makes Codex CLI worth using. When you close a session, you can come back to it later with full context:

### Four Ways to Resume

```bash
# Interactive picker (recommended)
codex resume
# Shows recent sessions, select and press Enter

# Resume most recent session
codex resume --last

# Resume specific session
codex resume <SESSION_ID>

# Show sessions from all directories
codex resume --all
```

### What Gets Preserved

When you resume a session, everything comes back:
- **Full conversation history** — what you said, what Codex responded
- **Execution plans** — strategies Codex outlined
- **Approval records** — previously approved operations
- **File context** — files referenced in the conversation

You can say "continue from where we left off, but change step 3" and Codex understands the full context.

### Practical Scenarios

**Scenario 1: Save progress before leaving**

```
You: Refactor the auth module, start by analyzing the current structure
Codex: [analyzes files, outlines plan]
You: I need to go, we'll continue tomorrow
# Next day:
$ codex resume --last
You: Continue the refactor from step 2
```

**Scenario 2: Juggle multiple tasks**

```bash
# Task A: Auth refactor
codex    # Start task A, work on it...
# Ctrl+C to exit

# Task B: Fix a bug
codex    # Start task B, fix it, done

# Back to Task A
codex resume   # Select task A's session
```

This is something [Claude Code](/posts/ai/2026-01-14-claude-code-guide/) doesn't natively support — closing a Claude Code session means losing context.

## Model Switching and Reasoning Levels

### Default Model

Codex CLI defaults to `gpt-5.3-codex` — OpenAI's model specifically optimized for coding tasks, outperforming general-purpose GPT-5 on code benchmarks.

### Switch at Runtime

```bash
# At launch
codex -m gpt-5.3-codex
codex --model gpt-5

# During a session
/model    # Interactive model/reasoning picker
```

### Reasoning Effort Strategy

| Level | Best For | Token Cost |
|-------|----------|-----------|
| `high` | Architecture, complex refactors, bug hunts, code review | High |
| `medium` | Daily coding, writing tests, small changes | Medium |
| `low` | Simple Q&A, formatting, renaming | Low |

```toml
# In config.toml
model_reasoning_effort = "high"    # or "medium" / "low"
```

**Cost-saving tip**: Don't run everything on `high`. Simple tasks like renaming a variable or formatting code work perfectly on `low`, saving significant tokens over time.

## AGENTS.md: Your AI's Onboarding Document

If Codex CLI is your "AI colleague," AGENTS.md is its "onboarding handbook." It's not just documentation — it's an **instruction system designed specifically for AI agents**.

### File Discovery Order

Codex reads instruction files on startup (once per session) in this order:

```
1. ~/.codex/AGENTS.override.md   ← Global override (highest priority)
2. ~/.codex/AGENTS.md            ← Global defaults
3. <project-root>/AGENTS.override.md   ← Project override
4. <project-root>/AGENTS.md            ← Project defaults
5. <subdirectory>/AGENTS.override.md   ← Subdirectory override
6. <subdirectory>/AGENTS.md            ← Subdirectory defaults
   ... all the way to the current working directory
```

Files merge from global to local, with closer files taking higher priority.

### A Real-World AGENTS.md Example

```markdown
# Project Guidelines

## Code Standards
- Use TypeScript strict mode
- All functions must have JSDoc comments
- Test coverage must be at least 80%
- Use pnpm as package manager (no npm or yarn)

## Architecture
- Follow Clean Architecture layering
- Database operations only in the repository layer
- API routes use RESTful naming conventions

## Testing
- Unit tests: Vitest
- E2E tests: Playwright
- Run command: pnpm test

## Off-Limits
- Do NOT modify .github/workflows/ files
- Do NOT access the database directly — use the ORM
- Do NOT hardcode secrets in source code
```

### Verify Your Instructions Load

```bash
codex --sandbox read-only --ask-for-approval never "Summarize the instructions you've loaded"
```

If instructions aren't working, check:
- Is the file empty? (Empty files are ignored)
- Is an `AGENTS.override.md` overriding your file?
- Has the merged content exceeded `project_doc_max_bytes` (default 32KB)?

## MCP Integration Guide

MCP (Model Context Protocol) transforms Codex CLI from a "code editor" into an **agent that can operate your entire development toolchain**.

### Two Ways to Add MCP Servers

**Method 1: CLI command (quick)**

```bash
# Add Context7 documentation search
codex mcp add context7 -- npx -y @upstash/context7-mcp

# Add with environment variables
codex mcp add my-db --env DATABASE_URL=postgresql://... \
  -- npx -y @modelcontextprotocol/server-postgres

# List all MCP servers
codex mcp list

# Remove a server
codex mcp remove context7
```

**Method 2: Config file (full control)**

```toml
# ~/.codex/config.toml

# STDIO-based MCP server
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

# HTTP-based MCP server
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
```

### Advanced MCP Configuration

```toml
[mcp_servers.my-server]
command = "node"
args = ["my-server.js"]
cwd = "/path/to/server"
enabled = true                     # Toggle without removing
required = true                    # Abort Codex if startup fails
startup_timeout_sec = 15           # Default: 10s
tool_timeout_sec = 120             # Default: 60s
enabled_tools = ["tool_a", "tool_b"]   # Whitelist
disabled_tools = ["dangerous_tool"]     # Blacklist
```

### Recommended MCP Servers

| MCP Server | Purpose | Install Command |
|-----------|---------|----------------|
| Context7 | Dev docs search | `codex mcp add context7 -- npx -y @upstash/context7-mcp` |
| Playwright | Browser automation | `codex mcp add playwright -- npx -y @anthropic/mcp-playwright` |
| PostgreSQL | Database operations | `codex mcp add db -- npx -y @modelcontextprotocol/server-postgres` |
| Sentry | Error log queries | `codex mcp add sentry -- npx -y @sentry/mcp-server` |

For a comprehensive guide on MCP servers, see [Best MCP Servers for Claude Code](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — most servers work with Codex CLI too.

## Web Search: Three Modes

```toml
# Cached search (default): uses OpenAI's index cache
web_search = "cached"

# Live search: fetches latest web data
web_search = "live"

# Disabled
web_search = "disabled"
```

Enable at launch:

```bash
codex --search    # Enable live search
```

**Important security distinction**: `--search` only lets Codex query through OpenAI's search API — it can't access arbitrary URLs. Full Access mode allows `curl`, `wget`, and direct network access. For most cases, `--search` is sufficient and safer.

## Keyboard Shortcuts and Interaction Tips

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Option + Enter` or `Ctrl + J` | New line (don't send) |
| `Enter` | Send message |
| `Esc` or `Ctrl + C` | Interrupt current request |
| Double `Ctrl + C` | Exit Codex CLI |
| `Ctrl + G` | Open external editor for long prompts |
| Up/Down arrows | Browse draft history |

### Ctrl+G: The Underrated Long-Text Editor

When you need to write a detailed prompt, the tiny terminal input box is painful. Press `Ctrl+G` to open your configured editor (defaults to `$EDITOR`) — write your prompt in Vim, VS Code, or any editor, save and close, and it auto-sends.

### --add-dir: Cross-Directory Work

```bash
# Give Codex write access to additional directories
codex --add-dir /path/to/shared-library
```

Essential for monorepos or projects that depend on local shared libraries.

## Codex CLI vs Claude Code: Honest Comparison

As someone who uses both tools daily, here's an objective comparison:

### Feature Comparison

| Dimension | Codex CLI | Claude Code |
|-----------|-----------|-------------|
| **Model** | GPT-5.3-Codex (code-specific) | Claude Opus 4.6 (general-purpose) |
| **Sandbox** | OS-level sandbox, file + network isolation | Permission prompt system |
| **Session recovery** | Full support, cross-directory resume | Not natively supported |
| **MCP support** | STDIO and HTTP | STDIO and SSE |
| **Web search** | Built-in (cached/live) | Built-in |
| **Code review** | `/review` + GitHub App | Through conversation |
| **IDE integration** | VS Code extension | VS Code + JetBrains |
| **Instruction system** | AGENTS.md (multi-level) | [CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) (multi-level) |
| **Pricing** | ChatGPT subscription or API | Anthropic subscription or API |

### When to Use Which

**Codex CLI wins when you need:**
- Strict sandbox isolation (enterprise security)
- Session recovery for long-running tasks
- CI/CD automation (`codex exec` + JSON output)
- Cost control with precise token management

**[Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) wins when you need:**
- Deep reasoning and complex multi-step tasks
- UI development and frontend work
- Interactive development with real-time feedback
- Richer [MCP ecosystem](/posts/ai/2026-02-28-claude-code-mcp-setup/)
- [Multi-agent orchestration](/posts/ai/2026-02-22-claude-code-agent-teams/)

### The Pragmatic Approach

You don't have to choose one. Here's what works in practice:
- **Daily coding, bug fixes** → Codex CLI (fast, cost-effective)
- **Complex architecture, major refactors** → Claude Code (deeper reasoning)
- **Automated code review** → Codex CLI's GitHub App
- **Frontend development** → Claude Code (better UI understanding)
- **CI/CD integration** → Codex CLI's `codex exec`

## Scripting and CI/CD Integration

### The exec Command

`exec` is Codex CLI's non-interactive mode, built for scripts and pipelines:

```bash
# Basic usage
codex exec "Fix all ESLint errors"

# JSON output (for script parsing)
codex exec --json "Analyze this repo for security vulnerabilities"

# Pipe with other tools
codex exec "List all TODO comments" | grep "FIXME"
```

### GitHub Actions Example

```yaml
# .github/workflows/codex-review.yml
name: Codex Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Codex CLI
        run: npm install -g @openai/codex
      - name: Run Code Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex exec --json \
            --config preferred_auth_method="apikey" \
            "Review code changes in this PR for security and performance issues"
```

### Git Hook Integration

```bash
# .git/hooks/pre-commit
#!/bin/bash
codex exec "Check staged code for obvious security issues or bugs"
if [ $? -ne 0 ]; then
    echo "Codex found potential issues. Please review before committing."
    exit 1
fi
```

## Performance and Cost Optimization

### Token Optimization

1. **Match reasoning level to task complexity** — use `low` for simple tasks, `high` only when needed
2. **Use `/compact` proactively** — compress context before hitting limits
3. **Reference files with `@`** — reduces unnecessary file searching
4. **Disable search when not needed** — set `web_search = "disabled"` for offline work

### Response Speed Tips

1. **Use `--no-alt-screen`** — disables fullscreen mode, faster rendering on some terminals
2. **Minimize MCP servers** — each server adds startup time. Only configure what you actually use
3. **Set reasonable timeouts** — don't set `startup_timeout_sec` too high

## Troubleshooting

### "Re-connecting" on startup

Usually a network or auth issue:

```bash
# Re-authenticate
codex logout
codex login

# If using a proxy
export HTTPS_PROXY=http://127.0.0.1:7890

# Check API key
codex --config preferred_auth_method="apikey"
```

### MCP server won't connect

```bash
# Test the command manually
npx -y @upstash/context7-mcp

# Verify environment variables
echo $MY_ENV_VAR

# Increase startup timeout in config.toml
[mcp_servers.my-server]
startup_timeout_sec = 30
```

### Context exhaustion (Codex starts hallucinating)

```
# Option 1: Compress context
/compact

# Option 2: Start fresh with a concise summary
/new

# Option 3: Break the task into smaller pieces
# Don't cram too many tasks into one session
```

## Notifications and Hooks

Set up desktop notifications for long-running tasks:

```toml
# ~/.codex/config.toml

# macOS notification
[notification_hook]
command = "osascript"
args = ["-e", "display notification \"Task complete\" with title \"Codex CLI\""]
```

For fancier notifications on macOS with `terminal-notifier`:

```toml
[notification_hook]
command = "terminal-notifier"
args = ["-title", "Codex CLI", "-message", "Task complete", "-sound", "default"]
```

Compare this to Claude Code's [Hooks system](/posts/ai/2026-02-28-claude-code-hooks-guide/), which offers more granular event triggers but requires more setup.

## Key Takeaways

1. **Profiles over aliases** — centralized config management beats scattered shell aliases
2. **Understand the security model** — balance convenience and safety with the right sandbox + approval combo
3. **Use session recovery** — it's a killer feature that prevents context loss
4. **MCP is the force multiplier** — it transforms Codex from "code editor" to "full development agent"
5. **Write a proper AGENTS.md** — it directly determines how well Codex understands your project
6. **Don't choose between Codex CLI and Claude Code** — use each where it excels

## Related Reading

- [Claude Code Complete Guide 2026](/posts/ai/2026-02-28-claude-code-complete-guide/) — Master Claude Code's full feature set
- [Claude Code vs ChatGPT Codex: Detailed Comparison](/posts/ai/2026-02-19-claude-code-vs-codex/) — Opus 4.6 vs GPT-5.3 deep dive
- [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) — The universal standard both tools use
- [Claude Code vs Cursor: Which Wins?](/posts/ai/2026-02-28-claude-code-vs-cursor/) — Another key tool comparison
- [CLAUDE.md Guide](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — The Claude Code equivalent of AGENTS.md
- [Best MCP Servers for Claude Code](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — MCP servers that work with both tools
