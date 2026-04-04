+++
date = '2026-03-06T22:00:00+08:00'
draft = false
title = 'OpenAI Symphony: From Issue Ticket to Pull Request Without a Developer'
description = 'OpenAI Symphony monitors your issue tracker, spawns Codex agents, and delivers verified PRs automatically. Architecture breakdown, WORKFLOW.md setup, and real-world limitations.'
toc = true
tags = ['OpenAI', 'Symphony', 'AI Agents', 'Autonomous Coding', 'Codex']
categories = ['AI Guides']
keywords = ['OpenAI Symphony', 'Symphony AI coding', 'autonomous coding agent', 'Symphony framework', 'harness engineering', 'Codex orchestration']

[[params.faqItems]]
question = "What is OpenAI Symphony and how does it work?"
answer = "OpenAI Symphony is an open-source automation service that monitors your issue tracker (like Linear), spawns autonomous Codex coding agents for each task, and delivers verified pull requests with passing CI checks. It operates through a WORKFLOW.md configuration file that lives in your repository."

[[params.faqItems]]
question = "Does Symphony replace developers?"
answer = "No. Symphony automates the implementation step but still requires human review before merging pull requests. It handles routine coding tasks so developers can focus on architecture, design decisions, and complex problems that require human judgment."

[[params.faqItems]]
question = "What issue trackers does Symphony support?"
answer = "Symphony currently ships with a Linear integration using GraphQL. The architecture is pluggable, and the community is working on a GitHub Issues adapter. Adding support for Jira or other trackers requires implementing a standard interface."

[[params.faqItems]]
question = "What is harness engineering in the context of Symphony?"
answer = "Harness engineering is OpenAI's term for designing infrastructure, constraints, and feedback loops that make AI agents reliably productive. It encompasses context engineering, architectural constraints like sandboxed execution, and entropy management through retry queues and proof-of-work verification."

[[params.faqItems]]
question = "How does Symphony handle agent failures?"
answer = "Symphony uses exponential backoff retry logic starting at 10 seconds and capping at 5 minutes. After exhausting all retries (default 3 attempts), the issue is released back to the tracker for human attention. It also supports state reconciliation if issues change in the tracker."
+++

![OpenAI Symphony — autonomous coding agent orchestration framework](cover.webp)

What if your issue tracker could fix its own tickets?

OpenAI just open-sourced **Symphony**, an automation service that monitors your project's issue tracker (like Linear), spawns autonomous coding agents (like Codex) for each task, and delivers verified pull requests — complete with CI status, code reviews, and walkthrough videos — before a human even looks at the code.

This isn't another AI code assistant that waits for your prompt. Symphony represents a fundamental shift in how software gets built: from **developer-driven coding** to **project-driven orchestration**. In this guide, we'll break down Symphony's architecture, explain how it works under the hood, and show you how to set it up for your own projects.

---

## Why Symphony Matters: The Paradigm Shift

Most AI coding tools today follow the same pattern:

```
Developer → Prompt AI → Review output → Fix mistakes → Repeat
```

You're still the driver. The AI is a copilot — helpful, but fundamentally reactive. You decide what to work on, when to start, and how to iterate.

Symphony flips this model entirely:

```
Project task → Symphony run → Agents implement → Proof generated → Human review → Merge
```

The difference is profound. Instead of a developer manually picking up a ticket and asking an AI for help, Symphony:

1. **Watches** your issue tracker continuously
2. **Claims** eligible tasks automatically
3. **Spawns** isolated coding agents for each task
4. **Monitors** agent progress with timeouts and retries
5. **Delivers** proof of work (passing CI, PR diffs, complexity analysis)
6. **Releases** failed tasks back to the queue for retry or human pickup

Think of it like a **factory floor for code** — where issues go in one end and verified pull requests come out the other.

This concept is what OpenAI internally calls **"harness engineering"** — the discipline of designing infrastructure, constraints, and feedback loops that make AI agents reliably productive. Symphony is the reference implementation of that discipline, and it's now [open-source on GitHub](https://github.com/openai/symphony) under the Apache 2.0 license.

---

## Architecture: The 8 Components

Symphony isn't a single monolithic tool. It's a modular system with 8 distinct components, each with a clear responsibility. Let's walk through them.

### 1. Workflow Loader

The Workflow Loader reads your `WORKFLOW.md` file — a single, in-repo configuration file that defines everything about how Symphony operates on your project.

`WORKFLOW.md` has two parts:
- **YAML front matter**: Configuration for the tracker, polling, workspace, hooks, and agent settings
- **Liquid-compatible template body**: The prompt template that gets rendered for each issue

```markdown
---
tracker:
  type: linear
  team_key: ENG
  candidate_label: "symphony"
polling:
  interval_ms: 30000
workspace:
  base_dir: /tmp/symphony-workspaces
agent:
  type: codex
  model: o4-mini
  timeout_ms: 600000
codex:
  approval_mode: auto-edit
---

You are working on issue {{ issue.identifier }}: {{ issue.title }}

{{ issue.description }}

## Requirements
- Write clean, well-tested code
- Follow existing code conventions
- Ensure all CI checks pass
```

The key insight here: **WORKFLOW.md lives in your repo**, right next to your code. This means your orchestration rules are version-controlled, reviewable, and project-specific. Different repos can have entirely different Symphony configurations.

Even better, Symphony supports **dynamic reload** — if you update `WORKFLOW.md`, the changes apply on the next polling cycle without restarting the service.

### 2. Config Layer

The Config Layer provides typed getters with sensible defaults and environment variable resolution. It handles configuration precedence:

```
WORKFLOW.md values → Environment variables → Default values
```

For example, `SYMPHONY_MAX_CONCURRENT_AGENTS=5` would override the default of 10 concurrent agents. This makes it easy to tune Symphony differently in development vs. production.

### 3. Issue Tracker Client

Currently, Symphony ships with a **Linear** integration that uses GraphQL to fetch issue candidates. The client:

- Queries for issues matching configurable labels (e.g., `symphony`)
- Extracts issue metadata (identifier, title, description, labels, assignee)
- Supports filtering by team, project, or custom fields

The design is pluggable — adding support for GitHub Issues, Jira, or other trackers means implementing a standard interface. The SPEC mentions that the community is already working on a GitHub Issues adapter.

### 4. Orchestrator

The Orchestrator is the brain of Symphony. It owns the polling tick, runtime state, dispatch logic, and retry queue.

Every polling interval (default: 30 seconds), the Orchestrator:

1. Fetches candidate issues from the tracker
2. Evaluates which ones are eligible (not already claimed, not rate-limited)
3. Dispatches eligible issues to the Agent Runner
4. Monitors running agents for timeouts or failures
5. Manages the retry queue with exponential backoff

The Orchestrator enforces concurrency limits — by default, no more than 10 agents run simultaneously. It also tracks per-state limits to prevent resource exhaustion.

### 5. Workspace Manager

Each issue gets its own **isolated workspace** — a dedicated directory with its own git clone, dependencies, and environment. The Workspace Manager handles:

- **Creation**: Cloning the repo, checking out the right branch, installing dependencies
- **Lifecycle hooks**: `after_create`, `before_run`, `after_run`, `before_remove`
- **Cleanup**: Removing workspaces after completion or failure
- **Safety**: Sanitized paths, prefix validation, and agent cwd restriction

The hooks are particularly powerful. For example, you could use `after_create` to install project-specific tools, or `after_run` to upload test coverage reports.

```yaml
workspace:
  base_dir: /tmp/symphony-workspaces
  hooks:
    after_create: "npm install && npm run build"
    before_run: "git checkout -b symphony/{{ issue.identifier }}"
    after_run: "npm test && npm run lint"
```

### 6. Agent Runner

The Agent Runner is where the magic happens. For each dispatched issue, it:

1. Creates an isolated workspace
2. Renders the prompt template with issue context
3. Launches a Codex subprocess using the **App-Server Protocol**
4. Monitors the subprocess until completion or timeout

The App-Server Protocol is a **line-delimited JSON protocol over stdout**, with a simple handshake:

```
→ initialize (client sends config)
← initialized (server confirms)
← thread/start (agent begins work)
← turn/start (new reasoning turn)
← turn/completed | turn/failed (turn result)
```

This protocol is intentionally simple — it's designed to be implementable by any agent runtime, not just Codex. You could theoretically plug in Claude Code, Cursor, or any other agent that speaks this protocol.

### 7. Status Surface

Symphony includes an optional **human-readable dashboard** built with Phoenix LiveView. The dashboard shows:

- Active runs and their current state
- Historical run results (succeeded/failed/timed out)
- Agent logs and output
- System metrics (queue depth, concurrency usage)

The dashboard exposes an HTTP API at `/api/v1/*` for programmatic access — useful for integrating with your existing monitoring stack or building custom alerting.

### 8. Logging

Structured logs flow to configurable sinks (stdout, file, or external services). Each log entry includes:

- Timestamp
- Run ID and issue identifier
- Component name
- Severity level
- Structured metadata (agent model, workspace path, duration)

This makes it straightforward to pipe Symphony logs into your existing observability stack (Datadog, Grafana, ELK, etc.).

---

## The State Machine: How a Task Flows Through Symphony

Every issue in Symphony follows a 5-state lifecycle:

```
┌───────────┐     ┌─────────┐     ┌─────────┐
│ Unclaimed │────→│ Claimed │────→│ Running │
└───────────┘     └─────────┘     └─────────┘
                                    │     │
                              ┌─────┘     └─────┐
                              ▼                   ▼
                    ┌──────────────┐      Terminal States:
                    │ RetryQueued  │      - Succeeded
                    └──────────────┘      - Failed
                           │              - TimedOut
                           │              - Stalled
                           └──→ Released   - CanceledByReconciliation
```

### State Transitions

| From | To | Trigger |
|------|----|---------|
| **Unclaimed** | Claimed | Orchestrator picks up the issue |
| **Claimed** | Running | Workspace ready, agent launched |
| **Running** | Succeeded | Agent completes successfully, CI passes |
| **Running** | Failed | Agent errors out or CI fails |
| **Running** | TimedOut | Agent exceeds `timeout_ms` |
| **Running** | Stalled | No progress detected for configurable period |
| **Running** | CanceledByReconciliation | Issue was modified/deleted in tracker |
| **Failed/TimedOut** | RetryQueued | Retry policy allows another attempt |
| **RetryQueued** | Claimed | Backoff period elapsed |
| **RetryQueued** | Released | Max retries exceeded |

### Run Phases

Within the "Running" state, each agent goes through 5 distinct phases:

1. **Workspace Prep** — Clone repo, install deps, run `after_create` hook
2. **Prompt Render** — Fill Liquid template with issue context
3. **Agent Launch** — Start Codex subprocess via App-Server Protocol
4. **Monitoring** — Track progress, enforce timeout, handle signals
5. **Terminal State** — Evaluate result, trigger `after_run` hook, clean up

### Retry Logic

When an agent fails, Symphony doesn't just give up. It uses **exponential backoff** with the formula:

```
delay = min(10000 × 2^(attempt-1), max_backoff_ms)
```

With the default `max_backoff_ms` of 300,000 (5 minutes), the retry schedule looks like:

| Attempt | Delay |
|---------|-------|
| 1 | 10 seconds |
| 2 | 20 seconds |
| 3 | 40 seconds |
| 4 | 80 seconds |
| 5 | 160 seconds |
| 6+ | 300 seconds (cap) |

After exhausting all retries, the issue is **Released** back to the tracker for human attention.

---

## WORKFLOW.md: The Single Source of Truth

The `WORKFLOW.md` file is Symphony's killer feature. Instead of scattering configuration across environment variables, YAML files, and dashboard settings, everything lives in one place.

Here's a complete example:

```yaml
---
# Tracker configuration
tracker:
  type: linear
  team_key: ENG
  candidate_label: "symphony-ready"
  api_key_env: LINEAR_API_KEY

# Polling settings
polling:
  interval_ms: 30000
  max_concurrent_agents: 10

# Workspace settings
workspace:
  base_dir: /tmp/symphony
  hooks:
    after_create: |
      npm install
      npm run build
    before_run: |
      git checkout -b symphony/{{ issue.identifier }}
    after_run: |
      npm test
      npm run lint
      gh pr create --title "{{ issue.identifier }}: {{ issue.title }}" --body "Automated by Symphony"

# Agent settings
agent:
  type: codex
  model: o4-mini
  timeout_ms: 600000
  max_retries: 3

# Codex-specific settings
codex:
  approval_mode: auto-edit
  sandbox: network-none
---

You are an expert software engineer working on issue {{ issue.identifier }}.

## Task
{{ issue.title }}

## Description
{{ issue.description }}

## Guidelines
- Follow existing code patterns and conventions
- Write comprehensive tests for all new functionality
- Ensure all existing tests still pass
- Keep changes minimal and focused on the issue
- Add comments for complex logic

## Context
This is a {{ issue.labels | join: ", " }} issue in the {{ issue.team }} team.
```

Key things to notice:

- **Liquid templating**: The prompt body supports full Liquid syntax — variables, filters, conditionals, loops
- **Hook scripts**: Multi-line shell scripts run at each lifecycle phase
- **Environment variable references**: Secrets like API keys can reference env vars
- **Agent-agnostic**: While Codex is the default, the `agent.type` field is designed for extensibility

---

## Harness Engineering: The Philosophy Behind Symphony

Symphony isn't just a tool — it embodies a new engineering discipline that OpenAI calls **"harness engineering."**

Traditional software engineering focuses on writing code. Prompt engineering focuses on crafting instructions for AI. Harness engineering focuses on something different: **designing the infrastructure, constraints, and feedback loops that make AI agents reliably productive.**

The three pillars of harness engineering, as demonstrated by Symphony:

### 1. Context Engineering

Instead of dumping an entire codebase into an AI's context window, Symphony carefully constructs the right context for each task:

- Issue title and description from the tracker
- Rendered prompt template with project-specific guidelines
- Isolated workspace with only the relevant repository
- Lifecycle hooks that set up the exact environment needed

### 2. Architectural Constraints

Symphony limits what agents can do to prevent chaos:

- **Isolated workspaces**: Each agent operates in its own directory — no cross-contamination
- **Sandboxed execution**: Codex runs with `network-none` by default — agents can't access the internet
- **Path sanitization**: Agents are restricted to their workspace directory
- **Concurrency limits**: No more than N agents running simultaneously
- **Timeouts**: Hard time limits prevent runaway processes

### 3. Entropy Management

In any autonomous system, things go wrong. Symphony manages entropy through:

- **Retry queues**: Failed tasks get another chance with exponential backoff
- **State reconciliation**: If an issue changes in the tracker, the corresponding run is canceled
- **Proof of work**: Agents must demonstrate success through CI, not just claim it
- **Graceful degradation**: When max retries are exceeded, tasks are released back for human attention

This philosophy of **"constrain the agent, not the ambition"** is what makes Symphony different from simply pointing an AI at a codebase and hoping for the best.

---

## Reference Implementation: Why Elixir/OTP?

Symphony's reference implementation is built in **Elixir** on the **OTP** (Open Telecom Platform) framework. This choice might seem unusual, but it's actually perfect for the problem:

| Requirement | OTP Feature |
|-------------|-------------|
| Concurrent agent management | Lightweight processes (millions per node) |
| Fault tolerance | Supervisor trees auto-restart crashed processes |
| State management | GenServer for predictable state machines |
| Hot code reload | Built-in hot swap for `WORKFLOW.md` changes |
| Real-time dashboard | Phoenix LiveView for zero-JS reactivity |
| Structured logging | Elixir Logger with metadata propagation |

The Elixir codebase is structured as an umbrella project:

```
symphony/
├── elixir/
│   ├── apps/
│   │   ├── symphony_core/      # Business logic, state machine, orchestrator
│   │   ├── symphony_linear/    # Linear issue tracker integration
│   │   ├── symphony_codex/     # Codex agent runner
│   │   └── symphony_web/       # Phoenix LiveView dashboard
│   ├── config/                 # Environment-specific configs
│   └── mix.exs                 # Umbrella project definition
├── SPEC.md                     # Detailed specification
├── WORKFLOW.md                 # Example workflow config
└── LICENSE                     # Apache 2.0
```

You don't *have* to use the Elixir implementation. The SPEC.md (3,500+ words) provides enough detail to implement Symphony in any language. The state machine, protocol, and configuration format are all language-agnostic.

---

## How to Get Started

### Prerequisites

- Elixir 1.15+ and Erlang/OTP 26+
- A Linear account with API access
- OpenAI API key (for Codex)
- A git repository with your project

### Quick Setup

```bash
# Clone Symphony
git clone https://github.com/openai/symphony.git
cd symphony/elixir

# Install dependencies
mix deps.get

# Set environment variables
export LINEAR_API_KEY="lin_api_xxxxx"
export OPENAI_API_KEY="sk-xxxxx"

# Create WORKFLOW.md in your project repo
# (see the example above)

# Start Symphony
mix phx.server
```

### Creating Your First WORKFLOW.md

1. **Start simple**: Use the minimal configuration with default settings
2. **Label your issues**: Add a `symphony` label to issues you want automated
3. **Watch the dashboard**: Open `http://localhost:4000` to see Symphony in action
4. **Iterate**: Refine your prompt template based on agent results

### Tips for Success

- **Start with small, well-defined issues**: "Fix typo in README" is better than "Refactor authentication system"
- **Write detailed issue descriptions**: The more context in the issue, the better the agent performs
- **Use lifecycle hooks**: `after_run` hooks for CI/linting catch many issues before you see them
- **Monitor and tune**: Watch the dashboard, adjust timeouts and retry limits based on your project's needs
- **Keep WORKFLOW.md updated**: As you learn what works, refine your prompt template

---

## Symphony vs. Other AI Coding Tools

How does Symphony compare to the alternatives?

| Feature | Symphony | GitHub Copilot Coding Agent | Devin | Claude Code Agent Teams |
|---------|----------|---------------------------|-------|------------------------|
| **Scope** | Project-level orchestration | Issue → PR automation | Full autonomous agent | Session-level multi-agent |
| **Open Source** | Yes (Apache 2.0) | No | No | No (CLI is open-source) |
| **Self-hosted** | Yes | No (GitHub-hosted) | No (cloud) | Local execution |
| **Issue Tracker** | Linear (extensible) | GitHub Issues only | Custom | N/A |
| **Agent Runtime** | Codex (extensible) | Copilot | Proprietary | Claude |
| **Customization** | Full (WORKFLOW.md) | Limited | Limited | CLAUDE.md + skills |
| **Concurrency** | Up to N parallel agents | 1 per repo | 1 session | Configurable subagents |
| **Retry Logic** | Built-in exponential backoff | Basic | Unknown | Manual |
| **Dashboard** | Phoenix LiveView | GitHub UI | Web UI | Terminal output |

### Key Differentiators

**vs. GitHub Copilot Coding Agent**: Both convert issues into PRs, but Symphony is open-source, self-hosted, and works with any issue tracker. Copilot's agent is locked into the GitHub ecosystem.

**vs. Devin**: Devin is a closed, commercial product. Symphony is an open framework you can customize, extend, and self-host. Devin is more "turnkey" but less flexible.

**vs. Claude Code Agent Teams**: [Claude Code's multi-agent system](/posts/ai/2026-02-28-claude-code-teams-guide/) operates at the session level — you manually start agent teams for specific tasks. Symphony operates at the project level — it continuously monitors and processes issues without human initiation.

**vs. CrewAI / LangGraph**: These are general-purpose agent frameworks. Symphony is purpose-built for code task orchestration with specific features like workspace isolation, issue tracker integration, and CI verification.

---

## Limitations and Considerations

Symphony is powerful, but it's not magic. Here are the current limitations:

### Technical Limitations

- **Linear only**: The issue tracker integration currently only supports Linear. GitHub Issues and Jira adapters are in development
- **Codex only**: The agent runtime currently only supports OpenAI Codex. Support for other agents would require implementing the App-Server Protocol
- **Elixir dependency**: The reference implementation requires Elixir/OTP, which may not be in your team's toolbox
- **Early stage**: As a newly open-sourced project, expect rough edges and breaking changes

### Practical Considerations

- **Issue quality matters**: Symphony is only as good as your issue descriptions. Vague tickets produce vague code
- **Not for complex refactors**: Symphony excels at well-scoped, clearly defined tasks. Multi-file architectural changes still need human guidance
- **Cost awareness**: Each agent run consumes API tokens. At scale, this adds up
- **Security posture**: Running autonomous agents that modify your codebase requires careful security consideration. Use sandboxing, restrict network access, and review all PRs before merging

---

## The Future of Autonomous Coding

Symphony represents an important milestone in the evolution of AI-assisted development. We're moving from:

1. **Code completion** (2021-2023): AI suggests the next line → GitHub Copilot
2. **Code conversation** (2023-2025): AI discusses and modifies code → [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), Cursor
3. **Code orchestration** (2025+): AI autonomously processes project work → Symphony

The "harness engineering" paradigm that Symphony embodies — designing constraints and feedback loops for AI agents — will likely become a distinct engineering discipline. Just as DevOps bridged development and operations, harness engineering bridges human project management and AI execution.

For now, Symphony is best suited for:
- **Bug fixes** with clear reproduction steps
- **Feature additions** with detailed specifications
- **Test writing** for existing code
- **Documentation updates** and maintenance tasks
- **Dependency updates** and routine maintenance

As agent capabilities improve, expect the scope of automatable tasks to expand rapidly.

---

## FAQ

**Is Symphony free to use?**
Yes, Symphony itself is free and open-source under the Apache 2.0 license. However, you'll need API keys for OpenAI (Codex) and Linear, which have their own pricing.

**Can I use Symphony with GitHub Issues instead of Linear?**
Not yet out of the box, but the architecture is pluggable. A GitHub Issues adapter is being developed by the community.

**Does Symphony work with models other than Codex?**
The agent runtime is designed to be extensible. Any agent that implements the App-Server Protocol (line-delimited JSON over stdout) can be plugged in. Community implementations for other models are expected.

**How do I prevent Symphony from making dangerous changes?**
Use sandboxed execution (`network-none`), restrict agent workspace paths, require CI to pass before merge, and always review PRs manually before merging.

**What happens when an agent fails?**
Failed tasks enter the retry queue with exponential backoff. After exceeding the maximum retry count, the task is released back to the issue tracker for human attention.

---

## Related Reading

- [Claude Code Agent Teams: How to Run Multiple AI Agents in Parallel](/posts/ai/2026-02-28-claude-code-teams-guide/) — Compare Symphony's project-level orchestration with Claude Code's session-level multi-agent approach
- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — If you prefer hands-on AI coding over full automation
- [Claude Code vs GitHub Copilot 2026](/posts/ai/2026-03-05-claude-code-vs-copilot/) — How Copilot's coding agent compares to Symphony
- [Building MCP Servers with Python](/posts/ai/2026-03-05-build-mcp-server-python/) — Learn about the protocol layer that powers AI tool integrations
- [Best MCP Servers for Claude Code 2026](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — Explore the tool ecosystem that autonomous agents rely on
- [OpenClaw vs Other AI Agents 2026](/posts/ai/2026-03-05-openclaw-vs-ai-agents/) — How Symphony fits into the broader AI agent landscape

---

*Symphony is available now on [GitHub](https://github.com/openai/symphony) under the Apache 2.0 license. Star the repo, try it on a small project, and join the conversation about the future of autonomous coding.*
