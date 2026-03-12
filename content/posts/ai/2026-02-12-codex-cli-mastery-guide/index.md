+++
date = '2026-02-12T16:02:00+08:00'
draft = false
title = 'Codex CLI Mastery Guide: 20+ Power Tips for Real-World Development'
description = 'Complete Codex CLI guide covering installation, model switching, session recovery, MCP integration, security modes, and an honest Codex CLI vs Claude Code comparison.'
toc = true
tags = ['Codex CLI', 'AI Coding', 'OpenAI', 'Terminal Tools', 'AI Agent']
categories = ['AI Guides']
keywords = ['Codex CLI guide', 'Codex CLI tips', 'OpenAI Codex', 'AI coding tools', 'Codex CLI vs Claude Code']
+++

![Codex CLI mastery guide: 20+ power tips cover image](cover.webp)

Most Codex CLI tutorials out there simply restate the official docs — listing commands without explaining when to use them, how to combine them, or what pitfalls to avoid.

This guide is different. It starts from real development scenarios and goes beyond the basics, covering the configuration hierarchy, the philosophy behind Codex's security model, an honest comparison with Claude Code, and advanced techniques the docs barely mention.

By the end, you will have:
- A **production-ready Codex CLI configuration** you can copy and adapt
- Deep understanding of the **security model and permission system**
- **20+ battle-tested tips** for daily workflows
- An **objective Codex CLI vs Claude Code comparison** to help you choose

---

## 1. What Is Codex CLI — and Why Should You Care?

### 1.1 More Than "ChatGPT in a Terminal"

Many people hear "Codex CLI" and think it is just a chat interface for the terminal. That misses the point entirely.

Codex CLI is OpenAI's **local AI coding agent**. It can:

- **Read your entire codebase**, understanding project structure and context
- **Edit files directly** — not just suggest changes, but apply them
- **Run shell commands** — tests, dependency installs, Git operations
- **Connect to external tools via MCP** — Figma, Sentry, databases, and more
- **Execute inside an OS-level sandbox** so AI commands cannot break your system

In short, Codex CLI acts like a **senior developer sitting next to you** — you describe what you need, and it writes code, runs tests, and fixes bugs.

### 1.2 Architecture Overview

Several aspects of Codex CLI's architecture deserve attention:

```
┌─────────────────────────────────────────┐
│           Codex CLI (TUI)               │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Composer    │  │  Approval Engine │  │
│  │  (Input UI)  │  │  (Permissions)   │  │
│  └─────────────┘  └──────────────────┘  │
│  ┌─────────────────────────────────────┐ │
│  │         Sandbox (OS-level)          │ │
│  │  - Filesystem isolation             │ │
│  │  - Network access control           │ │
│  │  - Process execution limits         │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  MCP Client │  │  Web Search      │  │
│  │  (Tools)    │  │  (Internet)      │  │
│  └─────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
              │
              ▼
     OpenAI API (gpt-5.3-codex)
```

**Key design decision**: Codex CLI uses a **local execution + cloud inference** hybrid architecture. Your code stays on your machine; only the necessary context is sent to OpenAI's API. This differs from OpenAI's cloud Codex Agent (available in ChatGPT), which runs inside a remote sandbox.

---

## 2. Installation and Basic Configuration

### 2.1 Installation

```bash
# macOS / Linux
npm install -g @openai/codex

# Or via Homebrew (macOS)
brew install openai-codex

# Verify installation
codex --version
```

### 2.2 Authentication Methods

Codex CLI supports two authentication methods — an important choice most tutorials skip:

**Option 1: ChatGPT Subscription Auth (Default)**

```bash
codex login
# Opens a browser for OAuth authentication
```

Best for: ChatGPT Plus/Pro/Enterprise subscribers — usage is included in the subscription.

**Option 2: API Key Auth**

```bash
# Edit ~/.codex/config.toml
preferred_auth_method = "apikey"

# Or switch temporarily
codex --config preferred_auth_method="apikey"
```

Best for: Users without a ChatGPT subscription, teams that need precise cost control, or CI/CD pipelines.

**Pro tip**: You can switch between the two at any time. A practical strategy is to use your ChatGPT subscription by default, then fall back to an API key when the subscription quota runs out:

```bash
# Switch back to ChatGPT auth
codex --config preferred_auth_method="chatgpt"
```

### 2.3 GPT-5 Series API Pricing

If you use API key authentication, understanding the pricing matters:

| Model | Input ($/1M tokens) | Output ($/1M tokens) | Best For |
|-------|---------------------|----------------------|----------|
| gpt-5.3-codex | Latest code model | Latest code model | Default Codex CLI model — strongest at code generation |
| gpt-5 | General flagship | General flagship | Complex reasoning, code review |
| o4-mini | Lightweight reasoning | Lightweight reasoning | Simple tasks, cost-sensitive use |

> Check the latest pricing at [OpenAI API Pricing](https://openai.com/api/pricing/)

---

## 3. Shell Aliases: One-Command Launch Configurations

### 3.1 Basic Alias

Tired of typing long parameter strings every time you start Codex? Create an alias:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias cx='codex -m gpt-5.3-codex -c model_reasoning_effort="high" --search'
```

This alias does three things:
1. Selects the most capable code model `gpt-5.3-codex`
2. Sets reasoning effort to `high`
3. Enables live web search with `--search`

### 3.2 Multi-Scenario Alias Setup

A single alias is rarely enough. Different scenarios call for different configurations:

```bash
# Daily development: high reasoning + web search + auto mode
alias cx='codex -m gpt-5.3-codex -c model_reasoning_effort="high" --search'

# Code review: read-only to prevent accidental edits
alias cxr='codex -m gpt-5.3-codex --sandbox read-only --ask-for-approval never'

# Quick questions: lightweight model, lower cost
alias cxq='codex -m o4-mini -c model_reasoning_effort="medium"'

# Full auto: for trusted projects only (use with caution)
alias cxa='codex -m gpt-5.3-codex --full-auto --search'

# CI/CD script mode: non-interactive
alias cxci='codex exec'
```

**Why separate these?** Token consumption scales directly with reasoning effort. `high` uses more tokens but produces more accurate results; `medium` suits everyday tasks; `low` handles simple requests. Choosing the right level for each task can save significant costs over a month.

### 3.3 Profiles: A More Elegant Alternative to Aliases

Codex CLI supports a `--profile` parameter that lets you predefine configuration groups in your config file:

```toml
# ~/.codex/config.toml

# Default configuration
model = "gpt-5.3-codex"
model_reasoning_effort = "high"
web_search = "live"

# Code review profile
[profiles.review]
sandbox_mode = "read-only"
approval_policy = "never"

# Lightweight profile
[profiles.quick]
model = "o4-mini"
model_reasoning_effort = "medium"
web_search = "disabled"
```

Usage:

```bash
codex --profile review   # Code review mode
codex --profile quick    # Lightweight mode
codex                    # Uses default config
```

Profiles are better than aliases because **configuration is centralized** — update one file instead of editing your `.zshrc`.

---

## 4. All 24 Slash Commands Explained

Codex CLI currently supports 24 slash commands — far more than the 8 most tutorials cover. Here they are, grouped by function:

### 4.1 Session Control

| Command | Purpose | Details |
|---------|---------|---------|
| `/new` | Start new session | Clears context while staying in the same CLI process |
| `/resume` | Restore a past session | Opens a selector showing recent sessions |
| `/fork` | Clone current session | Copies the conversation to a new thread — great for trying alternative approaches without losing progress |
| `/quit` / `/exit` | Exit CLI | Fully exits Codex CLI |
| `/compact` | Compress context | Summarizes the conversation to free up token space |

**`/fork` is seriously underrated.** Imagine you are implementing a feature using Approach A and want to try Approach B halfway through. Without `/fork`, you either lose Approach A's progress or start a brand-new session from scratch. With `/fork`, you branch off to try Approach B while keeping both conversation contexts intact.

### 4.2 Model and Style

| Command | Purpose | Details |
|---------|---------|---------|
| `/model` | Switch model and reasoning level | Interactive selection, works mid-session |
| `/personality` | Change communication style | `friendly` / `pragmatic` / `none` |
| `/plan` | Enter planning mode | Codex drafts a plan before executing — ideal for complex tasks |

**Using `/plan` correctly**: For complex tasks like "refactor the entire auth module," use `/plan` first to have Codex outline its steps. Review and approve the plan before execution. This is far safer than letting it jump straight in, and prevents wasted effort if the approach is wrong.

### 4.3 Permissions and Status

| Command | Purpose | Details |
|---------|---------|---------|
| `/permissions` | Adjust authorization mode | Switch between Auto/Read Only/Full Access at runtime |
| `/status` | View session info | Shows model, token usage, and account details |
| `/statusline` | Customize status bar | Interactively adjust what the bottom status bar displays |
| `/debug-config` | Debug configuration | Prints the full config loading chain and policy diagnostics |

**`/debug-config` is invaluable for troubleshooting.** When a config setting seems to have no effect, this command reveals exactly which files Codex loaded and which values override which.

### 4.4 Files and Tools

| Command | Purpose | Details |
|---------|---------|---------|
| `/mention` | Reference files or directories | Adds specific files to the conversation context |
| `/diff` | View Git changes | Includes untracked files |
| `/review` | Code review | Supports branch comparisons, uncommitted changes, and specific commits |
| `/mcp` | View MCP tools | Lists all configured MCP tools |
| `/apps` | Browse app connectors | View and insert ChatGPT connectors |
| `/ps` | View background tasks | Check status and output of background terminals |

### 4.5 Other Commands

| Command | Purpose | Details |
|---------|---------|---------|
| `/init` | Initialize AGENTS.md | Generates a project guidance file |
| `/feedback` | Submit feedback | Sends logs and diagnostics to OpenAI |
| `/logout` | Log out | Clears local credentials |

---

## 5. Session Recovery: Never Lose Your Work

This is a critical feature that many guides completely overlook. In real-world development, you frequently need to interrupt work to handle something else, then return to the previous conversation.

### 5.1 Four Recovery Methods

```bash
# Method 1: Interactive selector (recommended)
codex resume
# Shows recent sessions — highlight one and press Enter

# Method 2: Resume the most recent session
codex resume --last

# Method 3: Resume a specific session
codex resume <SESSION_ID>
# Get the ID from the selector, /status, or ~/.codex/sessions/

# Method 4: Cross-directory recovery
codex resume --all
# By default, only sessions from the current directory are shown
```

### 5.2 What Gets Preserved?

When you resume a session, the following are fully restored:

- **Conversation history**: Everything you and Codex discussed
- **Plan history**: Execution plans Codex created
- **Approval records**: Previously approved operations
- **File context**: Files referenced earlier

This means you can resume and say "continue from step 3 of the last plan," and Codex will understand the full context.

### 5.3 Practical Scenarios

**Scenario 1: Saving progress before leaving**

```
You: Refactor the auth module. Start by analyzing the code structure.
Codex: [Analyzes multiple files]
You: OK, I'm done for today. Will continue tomorrow.
# Next day:
$ codex resume --last
You: Continue yesterday's refactor, starting from step 2.
```

**Scenario 2: Juggling multiple tasks**

```bash
# Task A: Refactor auth
codex    # Start Task A
# ... working ...
# Ctrl+C to exit

# Task B: Fix a bug
codex    # Start Task B
# ... done ...

# Back to Task A
codex resume   # Select Task A's session
```

---

## 6. Authorization Modes In Depth

### 6.1 Three Basic Modes

| Permission | Auto (Default) | Read Only | Full Access |
|------------|---------------|-----------|-------------|
| Read files | Yes | Yes | Yes |
| Edit files | Yes | No | Yes |
| Run commands in workspace | Yes | No | Yes |
| Access files outside workspace | Requires approval | No | Yes |
| Network access | Requires approval | No | Yes |

### 6.2 Fine-Grained Permission Control (Flags)

Beyond the three presets, you can combine flags for precise permissions:

```bash
# Mode 1: Auto-edit, but require approval for untrusted commands
codex --sandbox workspace-write --ask-for-approval untrusted

# Mode 2: Read-only, never ask for approval (pure analysis)
codex --sandbox read-only --ask-for-approval never

# Mode 3: Fully automatic (use only in isolated environments!)
codex --dangerously-bypass-approvals-and-sandbox
# Alias: --yolo (yes, OpenAI actually named it that)
```

### 6.3 `--full-auto` vs `--yolo` — Know the Difference

These two options are commonly confused:

| Aspect | `--full-auto` | `--yolo` |
|--------|-------------|----------|
| Full name | `--full-auto` | `--dangerously-bypass-approvals-and-sandbox` |
| Sandbox | **Retained** | **Completely disabled** |
| Approvals | Reduced prompts | **Completely disabled** |
| Network access | Still sandbox-controlled | **Fully open** |
| Use case | Daily development (low friction) | CI/CD isolated environments |
| Safety | Reasonably safe | **Dangerous** |

**Bottom line**: `--full-auto` is "trust mode" for daily work. `--yolo` is for CI/CD pipelines or Docker containers. Never use `--yolo` on your personal machine.

### 6.4 Approval Policies (`--ask-for-approval`) Explained

The `--ask-for-approval` parameter has four levels:

```bash
# untrusted: Only untrusted commands need approval (default)
codex -a untrusted

# on-failure: Ask for approval only when a command fails
codex -a on-failure

# on-request: Approve only when Codex explicitly asks
codex -a on-request

# never: Never ask for approval
codex -a never
```

**Practical advice**: The default `untrusted` works for most situations. For code reviews where no commands need to run, combine `never` with a `read-only` sandbox.

---

## 7. Model Switching and Reasoning Levels

### 7.1 Default Model

Codex CLI defaults to `gpt-5.3-codex` — OpenAI's latest model specifically optimized for coding tasks, outperforming the general-purpose GPT-5 on code.

### 7.2 Switching at Runtime

```bash
# Option 1: Specify at launch
codex -m gpt-5.3-codex
codex --model gpt-5

# Option 2: Switch during a session
/model    # Interactive model and reasoning level selection
```

### 7.3 Choosing the Right Reasoning Level

```bash
# Config file setting
model_reasoning_effort = "high"    # Complex tasks, higher token cost
model_reasoning_effort = "medium"  # Everyday development (default)
model_reasoning_effort = "low"     # Simple tasks, saves tokens
```

**When to use which level:**

| Level | Best For | Token Cost |
|-------|----------|------------|
| `high` | Architecture design, complex refactors, bug hunting, code review | High |
| `medium` | Daily coding, writing tests, small changes | Medium |
| `low` | Quick questions, formatting, renaming | Low |

### 7.4 Reasoning Summary Format

```bash
# Standard format
codex -c model_reasoning_summary_format="none"

# Experimental format (more detailed reasoning trace)
codex -c model_reasoning_summary_format="experimental"
```

The `experimental` format shows the model's detailed thought process, which is valuable for understanding why Codex made a particular decision. Worth enabling for complex tasks.

---

## 8. AGENTS.md Deep Dive

### 8.1 More Than a README

If Codex CLI is your "AI coworker," then `AGENTS.md` is the **onboarding document** you write for it. It is not an ordinary file — it is an **instruction system designed specifically for AI agents**.

> Full specification: [agents.md](https://agents.md/)

### 8.2 File Discovery Mechanism

At startup (read once per session), Codex searches for instruction files in this order:

```
1. ~/.codex/AGENTS.override.md   ← Global override (highest priority)
2. ~/.codex/AGENTS.md            ← Global default
3. <project-root>/AGENTS.override.md   ← Project override
4. <project-root>/AGENTS.md            ← Project default
5. <subdirectory>/AGENTS.override.md   ← Subdirectory override
6. <subdirectory>/AGENTS.md            ← Subdirectory default
   ... all the way to the current working directory
```

**Merge rule**: Files are merged from global to current directory, with files closer to the working directory taking higher priority.

### 8.3 Configuration Options

```toml
# ~/.codex/config.toml

# Custom fallback filenames (tried in order)
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]

# Maximum byte size after merging
project_doc_max_bytes = 65536    # Default: 32KB
```

This means you can use `TEAM_GUIDE.md` or `.agents.md` instead of `AGENTS.md` — useful for teams that prefer not to have "AGENTS" in their repo.

### 8.4 A Practical AGENTS.md Example

```markdown
# Project Guidelines

## Code Standards
- Use TypeScript strict mode
- All functions must have JSDoc comments
- Test coverage must be at least 80%
- Use pnpm — npm and yarn are not allowed

## Architecture Constraints
- Follow Clean Architecture layers
- Database operations only in the repository layer
- API routes use RESTful naming conventions

## Testing
- Unit tests: Vitest
- E2E tests: Playwright
- Run command: pnpm test

## Deployment
- Main branch: main
- Deploy command: pnpm deploy
- Environment variable template in .env.example

## Prohibited Actions
- Do not modify files under .github/workflows/
- Do not run raw SQL — use the ORM
- Do not hardcode secrets in source code
```

### 8.5 Global vs Project-Level Strategy

**Global `~/.codex/AGENTS.md`** — write preferences that apply to all projects:

```markdown
# Global Preferences
- Communicate in English
- Write code comments in English
- Analyze before acting — do not jump straight to implementation
- Explain the reason before every modification
```

**Project-level `AGENTS.md`** — write project-specific standards and constraints (like the example above).

**Subdirectory `AGENTS.override.md`** — write rules specific to a submodule:

```markdown
# Rules for tests/ directory
- Test file naming: *.test.ts
- Use describe/it structure
- Put mock data in __fixtures__ directory
```

### 8.6 Verifying That Instructions Are Loaded

```bash
codex --sandbox read-only --ask-for-approval never "Summarize the instructions currently loaded"
```

If instructions are not taking effect, check these common issues:
- Is the file empty? (Empty files are ignored.)
- Is there an `AGENTS.override.md` overriding your file?
- Does the merged content exceed the `project_doc_max_bytes` limit?

---

## 9. The Configuration Hierarchy: Five Priority Levels

Many users do not realize that Codex CLI's configuration is not a single file — it is a **five-level priority system**:

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

### 9.1 User Config File In Detail

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

# Shell environment variable policy
[shell_environment_policy]
include_only = ["PATH", "HOME", "LANG"]

# Log directory
log_dir = "/path/to/codex-logs"

# Feature flags
[features]
shell_snapshot = true
undo = true
web_search = true

# Project trust levels
[projects."/Users/me/work/my-project"]
trust_level = "trusted"

[projects."/Users/me/work/another-project"]
trust_level = "trusted"
```

### 9.2 Project-Level Config

Create `.codex/config.toml` in the project root for project-specific settings:

```toml
# .codex/config.toml (project-level)
model = "gpt-5.3-codex"
model_reasoning_effort = "high"

# Project-specific MCP servers
[mcp_servers.my-db]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-postgres"]
env = { "DATABASE_URL" = "postgresql://..." }
```

### 9.3 Using `/debug-config` to Troubleshoot

When a setting does not seem to take effect, run `/debug-config` to see the full config loading chain:

```
Config Layer 1: /etc/codex/config.toml (not found)
Config Layer 2: ~/.codex/config.toml (loaded)
Config Layer 3: /project/.codex/config.toml (loaded)
Config Layer 4: Profile "review" (active)
Config Layer 5: CLI overrides: model_reasoning_effort=high
```

---

## 10. Web Search

### 10.1 Three Search Modes

```toml
# Cached search (default): uses OpenAI's maintained index cache
web_search = "cached"

# Live search: fetches the latest web data
web_search = "live"

# Disabled
web_search = "disabled"
```

### 10.2 Enabling at Launch

```bash
# Command-line flag
codex --search    # Enables live search

# Config file (permanent)
# ~/.codex/config.toml
web_search = "live"
```

### 10.3 Search vs Full Network Access

This is an **important security distinction**:

- `--search`: Allows Codex to access the web only through OpenAI's search API — it **cannot hit arbitrary URLs**
- Full Access network: Codex can execute `curl`, `wget`, and other commands to access any network resource

**Recommendation**: `--search` is sufficient for most workflows. It lets Codex look up the latest documentation and solutions without granting full network access.

---

## 11. File References and Image Input

### 11.1 @ File References

```
# Reference a file in conversation
@src/auth/login.ts There's a bug in the login logic — fix it

# Reference an entire directory
@src/components/ Add unit tests for all components in this directory
```

**Why explicitly reference files?** While Codex can search your codebase automatically, explicit references:
1. **Save time** by skipping the search step
2. **Prevent edits to wrong files** by clearly specifying the target
3. **Reduce token usage** by avoiding unnecessary file reads

### 11.2 Image Input

```bash
# CLI flags
codex -i screenshot.png "The layout on this page is broken — fix it"
codex --image wireframe.png,design.png "Implement this page based on the design"

# Interactive: paste images directly
# Use Cmd+V in the Codex input field to paste a screenshot
```

**Practical use cases**:
- Paste an error screenshot for Codex to analyze
- Paste a UI mockup for Codex to implement
- Paste a data chart for Codex to interpret

### 11.3 Using the `/mention` Command

```
/mention src/auth/     # Add the entire auth directory to context
/mention package.json  # Reference a specific file
```

The difference between `/mention` and `@`: `/mention` opens a file picker with fuzzy search; `@` is used inline in your input.

---

## 12. Scripting and Automation

### 12.1 The `exec` Command

`exec` is Codex CLI's **non-interactive mode**, designed for scripts and CI/CD:

```bash
# Basic usage
codex exec "Fix all ESLint errors"

# JSON output (for script parsing)
codex exec --json "Analyze this repository for security vulnerabilities"

# Combine with pipes
codex exec "List all TODO comments" | grep "FIXME"
```

### 12.2 CI/CD Integration Example

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
            "Review this PR's code changes, focusing on security and performance"
```

### 12.3 Git Hook Integration

```bash
# .git/hooks/pre-commit
#!/bin/bash
codex exec "Check the staged code for obvious security issues or bugs"
if [ $? -ne 0 ]; then
    echo "Codex found potential issues — please review before committing"
    exit 1
fi
```

---

## 13. MCP Integration Guide

MCP (Model Context Protocol) is the standard protocol that lets Codex CLI connect to external tools. It transforms Codex from a "code editor" into an **agent that can operate your entire development toolchain**.

### 13.1 Two Ways to Add MCP Servers

**Option 1: CLI Commands (beginner-friendly)**

```bash
# Add Context7 for documentation search
codex mcp add context7 -- npx -y @upstash/context7-mcp

# Add a server with environment variables
codex mcp add my-db --env DATABASE_URL=postgresql://... -- npx -y @modelcontextprotocol/server-postgres

# List all MCP servers
codex mcp list

# Remove an MCP server
codex mcp remove context7
```

**Option 2: Edit the Config File (for power users)**

```toml
# ~/.codex/config.toml

# STDIO-type MCP server
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.context7.env]
MY_VAR = "my_value"

# HTTP-type MCP server
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"

[mcp_servers.figma.http_headers]
X-Figma-Region = "us-east-1"
```

### 13.2 STDIO vs HTTP Configuration

| Aspect | STDIO | HTTP |
|--------|-------|------|
| Config params | `command` + `args` | `url` |
| How it runs | Codex spawns a subprocess | Connects to a remote service |
| Best for | Local tools (filesystem, databases) | Remote services (Figma, Sentry) |
| Authentication | `env` variables | `bearer_token_env_var` / `http_headers` |

### 13.3 Advanced Configuration Options

```toml
[mcp_servers.my-server]
command = "node"
args = ["my-server.js"]
cwd = "/path/to/server"           # Working directory
enabled = true                     # Set false to disable without deleting
required = true                    # Abort Codex if startup fails
startup_timeout_sec = 15           # Startup timeout (default: 10s)
tool_timeout_sec = 120             # Tool execution timeout (default: 60s)
enabled_tools = ["tool_a", "tool_b"]   # Whitelist: only allow these tools
disabled_tools = ["dangerous_tool"]     # Blacklist: block these tools
```

### 13.4 Recommended MCP Servers

| MCP Server | Purpose | Install Command |
|-----------|---------|-----------------|
| Context7 | Documentation search | `codex mcp add context7 -- npx -y @upstash/context7-mcp` |
| Playwright | Browser automation | `codex mcp add playwright -- npx -y @anthropic/mcp-playwright` |
| PostgreSQL | Database operations | `codex mcp add db -- npx -y @modelcontextprotocol/server-postgres` |
| Sentry | Error log queries | `codex mcp add sentry -- npx -y @sentry/mcp-server` |

### 13.5 Verifying MCP Connections

Codex does not have a dedicated MCP verification command (unlike Claude Code's `/mcp` with detailed status). Two ways to check:

1. **Watch at startup**: If an MCP connection fails, Codex displays an error on launch
2. **Check at runtime**: Use the `/mcp` command to list loaded MCP tools

```
/mcp
# If you see your configured tool names, the connection succeeded
```

---

## 14. Keyboard Shortcuts and Interaction Tips

### 14.1 Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Option + Enter` or `Ctrl + J` | New line (without sending) |
| `Enter` | Send message |
| `Esc` or `Ctrl + C` | Interrupt current request |
| Press `Ctrl + C` again | Exit Codex CLI |
| `Ctrl + G` | Open external editor (e.g., Vim) for long prompts |
| Up/Down arrows | Browse draft history |

### 14.2 `Ctrl+G`: The Underrated Long-Text Editor

When you need to write a lengthy prompt — say, a detailed feature spec — typing in the narrow terminal input is painful. Press `Ctrl+G` to open your configured editor (defaults to `$EDITOR`). Write comfortably in Vim or VS Code, save and close, and it is sent automatically.

### 14.3 `--add-dir`: Working Across Directories

```bash
# Let Codex access additional directories
codex --add-dir /path/to/shared-library
```

Essential when your project depends on a local shared library or when working across packages in a monorepo.

---

## 15. Context Management Strategies

### 15.1 Understanding the Context Window

Codex CLI has a context window limit. As a conversation grows longer, you will see the remaining context length displayed below the input. Once you approach the limit, Codex's performance degrades — it starts "forgetting" earlier parts of the conversation.

### 15.2 Using `/compact` Correctly

```
/compact
# Codex summarizes the conversation so far to free up context space
```

**When to use `/compact`:**
- When remaining context drops below 30%
- When finishing one phase and starting the next
- When Codex starts forgetting details discussed earlier

### 15.3 Proactive Context Management Tips

1. **Break large tasks into smaller ones**: Do not ask Codex to do everything at once — work in stages
2. **Use `/new` promptly**: Once a task is complete, start a fresh session instead of cramming more into the same one
3. **Use `/mention` proactively**: Tell Codex which files to read rather than letting it search (search results also consume context)
4. **Plan first with `/plan`**: For complex tasks, draft a plan and confirm it before execution to avoid repeated revisions that waste context

---

## 16. Code Review

### 16.1 The `/review` Command

```
# Review current workspace changes
/review

# Review differences against a specific branch
/review Compare changes against main branch

# Review a specific commit
/review Analyze commit abc1234

# Custom review focus
/review Focus on security vulnerabilities and performance issues
```

### 16.2 Automated CI/CD Reviews

Codex's [GitHub App](https://developers.openai.com/codex/integrations/github/) can automatically review PRs:

- Install and enable auto-review per repository
- It inspects code changes in PRs and leaves inline comments
- It catches real bugs — not the "you should add a comment here" kind of noise

---

## 17. Codex CLI vs Claude Code: An Honest Comparison

Having used both tools extensively, here is my attempt at an objective comparison:

### 17.1 Core Capability Comparison

| Dimension | Codex CLI | Claude Code |
|-----------|-----------|-------------|
| **Underlying model** | GPT-5.3-Codex (code-specialized) | Claude Opus 4.6 (strong generalist) |
| **Sandbox security** | OS-level sandbox with filesystem/network isolation | Permission prompt system with per-action approval |
| **Session recovery** | Full support, cross-directory resume | Not supported (context lost on close) |
| **MCP support** | STDIO and HTTP | STDIO and SSE |
| **Web search** | Built-in (cached/live) | Built-in search |
| **Code review** | `/review` + GitHub App | Via conversation |
| **IDE integration** | VS Code extension | VS Code + JetBrains extensions |
| **Instruction system** | AGENTS.md (multi-level) | CLAUDE.md (multi-level) |
| **Pricing** | ChatGPT subscription or API | Anthropic subscription or API |

### 17.2 Where Each Excels

**Codex CLI is better for:**
- Environments requiring **strict sandbox isolation** (enterprise security requirements)
- **Large file handling** (Claude Code struggles with files exceeding 25K tokens)
- **Session recovery** for long-running tasks
- **CI/CD automation** (exec command + JSON output)
- Teams focused on **cost control**

**Claude Code is better for:**
- **Complex reasoning and multi-step tasks** (Claude models have an edge in reasoning depth)
- **UI development and frontend work**
- **Interactive development** with real-time feedback
- Richer **MCP ecosystem**
- **Test-driven development** (TDD workflows)

### 17.3 My Actual Approach

You do not have to pick one. Here is my strategy:
- **Daily coding, bug fixes**: Codex CLI (fast, cost-effective)
- **Complex architecture, refactoring**: Claude Code (deeper reasoning)
- **Code review**: Codex CLI's GitHub App (automated)
- **Frontend development**: Claude Code (better UI understanding)

---

## 18. Performance and Cost Optimization

### 18.1 Token Consumption Optimization

1. **Match reasoning level to task complexity**: Use `low` for simple tasks, `medium` for everyday work, `high` for complex problems
2. **Use `/compact` regularly**: Avoid token waste from excessively long contexts
3. **Reference files explicitly**: Use `@` to specify files and reduce unnecessary searches
4. **Disable unused search**: If you do not need web search, set `web_search = "disabled"`

### 18.2 Response Speed Optimization

1. **Use `--no-alt-screen`**: Disabling full-screen mode can improve rendering speed in some terminals
2. **Limit MCP servers**: Each server adds startup time — only configure the ones you actually use
3. **Set reasonable timeouts**: Keep `startup_timeout_sec` and `tool_timeout_sec` realistic

---

## 19. Notifications and Hooks

```toml
# ~/.codex/config.toml

# Run a notification when the agent finishes a round of work
[notification_hook]
command = "osascript"
args = ["-e", "display notification \"Codex has finished the task\" with title \"Codex CLI\""]
```

This is invaluable for time-consuming tasks — switch to another window and get a system notification when Codex finishes.

macOS users can pair this with `terminal-notifier` for richer notifications:

```toml
[notification_hook]
command = "terminal-notifier"
args = ["-title", "Codex CLI", "-message", "Task completed", "-sound", "default"]
```

---

## 20. Feature Flags (Experimental)

Codex CLI includes a feature flag system for trying experimental capabilities early:

```bash
# Enable a feature
codex features enable shell_snapshot

# Disable a feature
codex features disable shell_snapshot

# Temporarily enable/disable at launch
codex --enable shell_snapshot
codex --disable web_search
```

Known feature flags:

| Flag | Capability |
|------|-----------|
| `shell_snapshot` | Shell state snapshot |
| `undo` | Operation undo |
| `apps` | App connectors |
| `personality` | Communication style |
| `collaboration_modes` | Collaboration modes |
| `apply_patch_freeform` | Freeform patch application |

---

## 21. Extra Directory Write Permissions

```bash
# Grant Codex write access to additional directories
codex --add-dir /path/to/shared-lib --add-dir /path/to/configs
```

By default, Codex can only write to the current working directory. If your project uses a monorepo structure or requires edits across multiple related projects, `--add-dir` grants write permissions to additional directories.

---

## 22. Shell Completions

```bash
# Generate completion script for bash
codex completions bash >> ~/.bashrc

# Generate completion script for zsh
codex completions zsh >> ~/.zshrc

# Generate completion script for fish
codex completions fish >> ~/.config/fish/completions/codex.fish
```

After installation, press Tab when typing `codex` commands to auto-complete parameters and options.

---

## Troubleshooting Guide

### Q1: Codex Keeps Showing "Re-connecting"

This is usually a network issue or expired authentication. Solutions:

```bash
# 1. Re-authenticate
codex logout
codex login

# 2. If using a proxy, verify the configuration
export HTTPS_PROXY=http://127.0.0.1:7890

# 3. Check if your API key has expired
codex --config preferred_auth_method="apikey"
```

### Q2: MCP Server Connection Fails

```bash
# 1. Test the command manually
npx -y @upstash/context7-mcp  # Run it directly to see errors

# 2. Verify environment variables
echo $MY_ENV_VAR  # Confirm the variable is set

# 3. Increase the startup timeout
# In config.toml:
[mcp_servers.my-server]
startup_timeout_sec = 30
```

### Q3: Context Exhausted — Codex Starts Hallucinating

```
# Option 1: Compress the context
/compact

# Option 2: Start a new session with a concise prompt
/new

# Option 3: Decompose the task
# Avoid cramming too much into a single session
```

### Q4: Codex Keeps Editing the Wrong File

```
# Explicitly reference the target file
@src/auth/login.ts Only modify line 42 in this file

# Use Read Only mode to analyze first
/permissions -> Read Only
You: Analyze the code structure in @src/auth/
# Confirm understanding is correct, then switch back to Auto mode
```

---

## Summary

Codex CLI is a tool **far richer than it first appears**. From the five-level configuration hierarchy to OS-level sandboxing, from 24 slash commands to full MCP integration, it is not just a "terminal chat tool" — it is a **complete AI coding agent platform**.

Key takeaways:

1. **Combine aliases and profiles** to prepare configurations for different scenarios
2. **Understand the security model** to balance convenience and safety
3. **Use session recovery** so closing a terminal never means losing context
4. **MCP is the killer feature** — it transforms Codex from "writing code" to "operating your entire dev toolchain"
5. **Write AGENTS.md carefully** — it directly determines how deeply Codex understands your project
6. **You do not have to choose between Codex CLI and Claude Code** — pick the right tool for each task

## Related Reading

- [Claude Code Complete Guide: From Beginner to Power User](/posts/ai/2026-01-14-claude-code-guide/)
- [CLAUDE.md Writing Guide: Help AI Truly Understand Your Project](/posts/ai/2026-01-12-claudemd-memory-guide/)
- [AI-Powered Development Workflows](/posts/ai/2026-01-19-ai-dev-workflow/)
- [Cursor Agent Best Practices](/posts/ai/2026-01-19-cursor-agent-best-practices/)
- [Claude Code Best Practices Guide](/posts/ai/2026-01-06-claudecode-best-practices/)
