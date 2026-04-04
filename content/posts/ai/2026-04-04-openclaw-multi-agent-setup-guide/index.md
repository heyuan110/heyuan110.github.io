+++
date = '2026-04-04T10:00:00+08:00'
draft = false
title = 'OpenClaw Multi-Agent Configuration: Architecture, Routing, and Production Patterns'
description = 'Complete guide to OpenClaw multi-agent configuration. Covers agent creation, workspace isolation, binding-based routing, sessions_send communication, Feishu/Lark integration, and four production-ready collaboration patterns.'
toc = true
tags = ['OpenClaw', 'Multi-Agent', 'AI Architecture', 'Feishu', 'Agent Orchestration']
keywords = ['OpenClaw multi-agent configuration', 'OpenClaw multi-agent setup', 'openclaw agents add', 'openclaw bindings', 'sessions_send', 'OpenClaw Feishu integration', 'multi-agent routing', 'agent orchestration patterns']

[[params.faqItems]]
question = "How do I create multiple agents in OpenClaw?"
answer = "Use 'openclaw agents add <name>' for each agent. Each agent gets an isolated workspace with its own SOUL.md, AGENTS.md, memory, model config, and session store under ~/.openclaw/agents/<agentId>/. Agent names must be lowercase letters, digits, and hyphens only, starting with a letter."

[[params.faqItems]]
question = "What are OpenClaw bindings and how do they route messages?"
answer = "Bindings are deterministic routing rules in openclaw.json that map incoming messages to specific agents. They use a most-specific-wins priority: exact peer match (highest) > group match > channel-level default > fallback default agent (lowest). If multiple bindings match at the same tier, the first in config order wins."

[[params.faqItems]]
question = "How does sessions_send work for agent-to-agent communication?"
answer = "sessions_send is a built-in tool that enables direct messaging between agents. Configure it in openclaw.json under tools.agentToAgent with an allow-list. It supports reply-back loops controlled by maxPingPongTurns (0-5, default 5). Agents can exit the loop by replying REPLY_SKIP. Communication is disabled by default for security."

[[params.faqItems]]
question = "Can I connect OpenClaw multi-agent to Feishu/Lark?"
answer = "Yes. Since OpenClaw 2026.2.26, Feishu is bundled as a built-in channel. Create multiple Feishu bot applications in the same enterprise, each acting as an independent channel account. Use bindings to route each bot to a different agent. Feishu uses WebSocket event subscription — no public webhook URL required."

[[params.faqItems]]
question = "Which multi-agent collaboration pattern should I start with?"
answer = "Start with the Supervisor pattern: one coordinator agent receives all requests and delegates to specialists via sessions_send. This covers 80% of use cases. Graduate to Router (parallel channel dispatch), Pipeline (sequential processing chain), or Parallel (simultaneous task splitting) only when the Supervisor becomes a bottleneck."
+++

![OpenClaw multi-agent configuration guide covering architecture, routing, and collaboration patterns](cover.webp)

Your single OpenClaw agent worked great for two weeks. Then it started hallucinating project context into unrelated conversations, confusing your coding tasks with your writing tasks, and taking 15 seconds to respond because its memory index had grown to 200MB.

The problem is not the model. The problem is architectural: **one agent cannot hold unlimited context domains without degradation**. The solution is not a bigger context window — it is multiple specialized agents with isolated workspaces, deterministic routing, and explicit communication channels.

This guide covers the complete multi-agent configuration for OpenClaw in 2026, from workspace isolation to binding-based routing to production collaboration patterns. If you have not installed OpenClaw yet, start with the [OpenClaw Setup Guide](/posts/ai/2026-03-05-openclaw-setup-guide/) first.

---

## Why Multi-Agent? The Single-Agent Ceiling

A single OpenClaw agent accumulates context from every domain it touches: coding, writing, research, personal messaging, calendar management. After a few weeks of heavy use, three things happen:

1. **Memory pollution** — The agent retrieves irrelevant context from other domains when answering questions. Ask about a blog draft and it pulls in debugging notes from last week.
2. **Persona confusion** — One SOUL.md cannot define both "formal technical writer" and "casual friend" without contradictions that leak across conversations.
3. **Model mismatch** — A coding agent needs Claude Sonnet or GPT-4.1; a brainstorming agent works better with GLM-4.7 or DeepSeek. One agent means one model for everything.

Multi-agent architecture solves all three by giving each agent its own workspace, memory, persona, and model configuration. The [OpenClaw Architecture Deep Dive](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) explains the underlying Gateway-Agent-Skill model that makes this possible.

---

## Core Concepts: What Makes an Agent

In OpenClaw, each agent is three things:

| Component | Path | Purpose |
|-----------|------|---------|
| **Workspace** | `~/openclaw-agents/<name>/` | SOUL.md, AGENTS.md, USER.md, TOOLS.md, MEMORY.md |
| **Agent Directory** | `~/.openclaw/agents/<agentId>/` | Auth profiles, model registry, per-agent config |
| **Session Store** | `~/.openclaw/agents/<agentId>/sessions/` | Chat history, routing state |

**Critical rule**: Never share an agentDir between agents. Shared directories cause auth collisions, session bleed, and memory cross-contamination.

---

## Step 1: Create Agent Workspaces

### Add Agents via CLI

```bash
# Create a supervisor agent (coordinator)
openclaw agents add supervisor

# Create specialist agents
openclaw agents add writer
openclaw agents add coder
openclaw agents add researcher
```

Each command creates a workspace directory with starter files:

```
~/openclaw-agents/writer/
├── AGENTS.md      # Agent capabilities and rules
├── SOUL.md        # Personality, tone, values
├── USER.md        # User preferences and context
├── TOOLS.md       # Available tools and restrictions
├── MEMORY.md      # Persistent memory notes
├── HEARTBEAT.md   # Proactive check-in rules
└── IDENTITY.md    # Name, avatar, metadata
```

### Naming Rules

- Lowercase letters, digits, and hyphens only (`a-z`, `0-9`, `-`)
- Must start with a letter
- Cannot end with a hyphen
- Examples: `writer`, `code-reviewer`, `research-v2`

### Configure SOUL.md Per Agent

Each agent needs a distinct SOUL.md. Here is a minimal example for a writer agent:

```markdown
# Writer Agent

You are a technical content writer specializing in AI engineering topics.

## Rules
- Always write in clear, direct English
- Use concrete examples over abstract explanations
- Target 1500-2500 words per article
- Include code snippets when relevant
- Never generate placeholder content — every section must be substantive

## Tone
Professional but conversational. No corporate speak. No filler phrases.

## Tools You Can Use
- tavily-search (web research)
- memory_search (recall past articles)
- read/write (file operations)

## Tools You Cannot Use
- exec (no shell commands)
- browser (no browser automation)
```

---

## Step 2: Configure Model Routing Per Agent

Each agent can run a different AI model. Configure this in each agent's model settings:

```bash
# Supervisor: fast, cheap model for routing decisions
openclaw agents config set supervisor model claude-3.5-haiku

# Writer: strong reasoning for content creation
openclaw agents config set writer model deepseek-r1

# Coder: best coding model available
openclaw agents config set coder model claude-sonnet-4

# Researcher: model with strong web browsing
openclaw agents config set researcher model gpt-4.1
```

### Model Selection Strategy

| Agent Type | Recommended Model | Reasoning |
|-----------|-------------------|-----------|
| Supervisor | Claude Haiku / GPT-4.1-mini | Fast routing, low cost |
| Writer | DeepSeek-R1 / Claude Sonnet | Strong long-form generation |
| Coder | Claude Sonnet / Codex | Best code quality |
| Researcher | GPT-4.1 / Claude Sonnet | Strong tool use and synthesis |
| Brainstormer | GLM-4.7 / DeepSeek | Creative, divergent thinking |

The key insight: **the supervisor agent does not need the best model**. It only makes routing decisions. Save your expensive API calls for the specialist agents that do the actual work.

---

## Step 3: Configure Bindings (Message Routing)

Bindings are the deterministic routing rules that map incoming messages to the correct agent. This is configured in `openclaw.json`:

```json
{
  "agents": {
    "list": [
      {
        "id": "supervisor",
        "workspace": "~/openclaw-agents/supervisor",
        "default": true
      },
      {
        "id": "writer",
        "workspace": "~/openclaw-agents/writer"
      },
      {
        "id": "coder",
        "workspace": "~/openclaw-agents/coder"
      },
      {
        "id": "researcher",
        "workspace": "~/openclaw-agents/researcher"
      }
    ]
  },
  "bindings": [
    {
      "channel": "telegram",
      "peer": "writing_group_id",
      "agent": "writer"
    },
    {
      "channel": "telegram",
      "peer": "coding_group_id",
      "agent": "coder"
    },
    {
      "channel": "telegram",
      "agent": "supervisor"
    }
  ]
}
```

### Binding Priority (Most-Specific Wins)

1. **Exact peer match** (highest) — A specific chat/group ID routes to a specific agent
2. **Channel + account match** — A channel type with a specific account
3. **Channel-level default** — All messages on a channel type
4. **Fallback default** — The agent marked `"default": true` (or the first in the list)

If multiple bindings match at the same tier, **the first one in config order wins**.

### Verify Your Bindings

After configuring, verify the routing:

```bash
# Show all active bindings
openclaw gateway --bindings

# Probe a specific channel to confirm routing
openclaw gateway --probe telegram
```

---

## Step 4: Agent-to-Agent Communication (sessions_send)

For agents to talk to each other (not just receive routed messages), you need to configure `sessions_send`. This is OpenClaw's internal messaging system between agents.

### Enable Agent-to-Agent Communication

Add this to your `openclaw.json`:

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["supervisor", "writer", "coder", "researcher"],
      "maxPingPongTurns": 3
    }
  }
}
```

### How sessions_send Works

1. **Supervisor** receives a user request: "Write a blog post about OpenClaw security"
2. **Supervisor** calls `sessions_send` to the **researcher** agent: "Find the latest OpenClaw security features and vulnerabilities"
3. **Researcher** completes the research and replies back
4. **Supervisor** calls `sessions_send` to the **writer** agent: "Write a 2000-word article using this research: [research results]"
5. **Writer** produces the article and replies back
6. **Supervisor** consolidates and delivers the final result to the user

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enabled` | `false` | Master switch for agent-to-agent communication |
| `allow` | `[]` | Allowlist of agent IDs that can communicate |
| `maxPingPongTurns` | `5` | Maximum back-and-forth turns (0-5) |

### Stopping the Loop

An agent can exit a conversation loop by replying exactly `REPLY_SKIP`. This prevents infinite loops and wasted tokens.

### Anti-Recursion Rule

**Critical**: Configure your supervisor's SOUL.md with a strict no-recursion rule:

```markdown
## Coordination Rules
- NEVER accept tasks routed back from specialists
- If you receive output from a specialist, aggregate and close — do not re-delegate
- If a specialist cannot complete a task, report failure to the user — do not retry with a different framing
```

Without this rule, you get circular delegation loops that burn tokens rapidly.

---

## Step 5: Per-Agent Sandbox and Tool Permissions

Each agent should have only the tools it needs. Over-permissioning creates security risks and confuses the model with too many tool options.

```json
{
  "agents": {
    "list": [
      {
        "id": "writer",
        "workspace": "~/openclaw-agents/writer",
        "sandbox": {
          "enabled": true,
          "allowedPaths": ["~/writing/", "~/drafts/"]
        },
        "tools": {
          "allow": ["tavily-search", "memory_search", "read", "write"],
          "deny": ["exec", "browser", "shell"]
        }
      },
      {
        "id": "coder",
        "workspace": "~/openclaw-agents/coder",
        "sandbox": {
          "enabled": true,
          "allowedPaths": ["~/projects/"]
        },
        "tools": {
          "allow": ["exec", "read", "write", "browser", "memory_search"],
          "deny": ["tavily-search"]
        }
      }
    ]
  }
}
```

### Sandbox Best Practices

- **Writer agents**: Read/write access to content directories only, no shell execution
- **Coder agents**: Full shell access but restricted to project directories
- **Researcher agents**: Web search tools only, no file write permissions
- **Family/shared agents**: Read-only sandbox — can answer questions but cannot modify anything

For more on tool permissions, see the [OpenClaw Automation Pitfalls](/posts/ai/2026-03-05-openclaw-automation-pitfalls/) guide.

---

## Feishu/Lark Integration for Multi-Agent

Feishu (Lark) is bundled as a built-in channel since OpenClaw 2026.2.26. Multi-agent routing is fully supported since 2026.3.13.

### Architecture: One Bot Per Agent

The recommended pattern for Feishu multi-agent:

1. Create multiple **robot applications** in the same Feishu enterprise
2. Each robot acts as an independent channel account in OpenClaw
3. Use bindings to route each robot to a different agent

```json
{
  "channels": {
    "feishu": [
      {
        "account": "work-bot",
        "appId": "cli_xxxwork",
        "appSecret": "secret1"
      },
      {
        "account": "writing-bot",
        "appId": "cli_xxxwrite",
        "appSecret": "secret2"
      }
    ]
  },
  "bindings": [
    {
      "channel": "feishu",
      "account": "work-bot",
      "agent": "supervisor"
    },
    {
      "channel": "feishu",
      "account": "writing-bot",
      "agent": "writer"
    }
  ]
}
```

### Feishu Connection Details

- **No public URL required** — Feishu uses WebSocket event subscription, so your OpenClaw gateway does not need to be publicly accessible
- **Real-time status** — The plugin shows Thinking/Generating/Complete status in message cards
- **Rich capabilities** — Agents can access Feishu docs, calendars, tasks, bases, and group messages through the bundled Feishu tools

### Feishu Permissions Setup

Each Feishu bot application needs these scopes:

- `im:message` — Send and receive messages
- `im:message.group_at_msg` — Receive @mentions in groups
- `contact:user.base:readonly` — Read user information
- Additional scopes based on tools: `docs:doc`, `calendar:calendar`, `task:task`

---

## Four Production Collaboration Patterns

### Pattern 1: Supervisor (Start Here)

```
User → Supervisor → Writer
                  → Coder
                  → Researcher
```

One coordinator agent receives all requests and delegates to specialists via `sessions_send`. The supervisor decides which specialist handles each task, collects results, and delivers the final response.

**Best for**: Personal assistants, small teams, mixed-domain workflows.

**Config complexity**: Low — one supervisor, 2-4 specialists.

### Pattern 2: Router (Channel-Based Dispatch)

```
Telegram Writing Group → Writer
Telegram Coding Group  → Coder
Feishu Work Bot        → Supervisor
WhatsApp Personal      → Personal Agent
```

Messages are routed directly to specialist agents based on channel and group bindings. No supervisor needed — each channel goes to the right agent automatically.

**Best for**: Teams where each channel has a clear purpose.

**Config complexity**: Low — just bindings, no inter-agent communication needed.

### Pattern 3: Pipeline (Sequential Processing)

```
User → Researcher → Writer → Editor → User
```

Each agent's output feeds the next agent's input. The research agent gathers data, the writer creates content from it, the editor polishes the result.

**Best for**: Content creation, code review chains, data processing workflows.

**Config complexity**: Medium — requires `sessions_send` with clear handoff protocols.

### Pattern 4: Parallel (Simultaneous Execution)

```
           → Researcher A (topic 1)
User → Supervisor → Researcher B (topic 2) → Supervisor → User
           → Researcher C (topic 3)
```

The supervisor splits a task across multiple agents running simultaneously. Results are aggregated when all agents complete.

**Best for**: Large research tasks, multi-file code generation, batch processing.

**Config complexity**: High — requires careful result aggregation and error handling.

### Choosing the Right Pattern

| Scenario | Pattern | Why |
|----------|---------|-----|
| Personal assistant with mixed tasks | Supervisor | Flexible routing, easy to add specialists |
| Team with dedicated channels | Router | Zero overhead, direct routing |
| Blog content production | Pipeline | Research → Write → Edit flow |
| Competitive analysis across 10 companies | Parallel | Speed through simultaneous execution |

---

## Monitoring and Debugging

### Check Agent Status

```bash
# List all configured agents
openclaw agents list

# Show detailed config for a specific agent
openclaw agents config show writer

# Check gateway routing status
openclaw gateway --bindings
```

### Common Issues

**Agent not receiving messages**: Check binding priority. A more general binding might be catching messages before your specific one. Remember: most-specific wins, and within the same tier, first in config order wins.

**sessions_send failing silently**: Verify the target agent is in the `agentToAgent.allow` list. Communication is disabled by default.

**Memory cross-contamination**: Ensure each agent has its own `agentDir`. Shared directories cause session bleed. Run `openclaw agents list` and verify each agent has a unique path.

**High token costs**: The supervisor agent should handle simple routing decisions with a cheap model. If your supervisor is using Claude Sonnet for every routing decision, switch it to Haiku or GPT-4.1-mini.

---

## Cost Optimization

Multi-agent setups multiply API costs because each `sessions_send` call is a separate API request. Here are strategies to manage this:

1. **Let the supervisor handle simple tasks directly** — Do not delegate one-line answers to specialist agents
2. **Use cheap models for routing** — Haiku for supervisor, expensive models only for specialists
3. **Limit `maxPingPongTurns`** — Set to 2-3 instead of the default 5
4. **Consolidate similar agents** — If two agents handle 80%+ the same tasks, merge them
5. **Use the Router pattern when possible** — Channel-based routing has zero token overhead compared to supervisor-based delegation

For detailed memory optimization, see the [OpenClaw Memory Strategy](/posts/ai/2026-01-31-openclaw-memory-strategy/) guide.

---

## Recommended Starting Configuration

For most personal users, start with this 3-agent setup:

| Agent | Model | Role | Channels |
|-------|-------|------|----------|
| supervisor | claude-3.5-haiku | Route tasks, handle simple queries | Default for all channels |
| writer | deepseek-r1 | Blog posts, documentation, emails | Writing-specific groups |
| coder | claude-sonnet-4 | Code generation, debugging, reviews | Coding-specific groups |

Add a researcher agent when you find the supervisor frequently needing web search for complex queries. Add more specialists only when you have clear, distinct workloads that justify the overhead.

For the development workflow behind OpenClaw itself, see how the creator runs [parallel agents with Claude Code](/posts/ai/2026-01-31-openclaw-claude-code-workflow/).

---

## What's Next

Multi-agent configuration is the foundation. Once your agents are running, explore:

- **[OpenClaw Tavily Integration](/posts/ai/2026-03-05-openclaw-tavily-integration/)** — Give your researcher agent real-time web search
- **[OpenClaw Usage Tutorial](/posts/ai/2026-02-12-openclaw-usage-tutorial/)** — Complete beginner guide if you are just getting started
- **Lobster Workflows** — Deterministic multi-agent pipelines using YAML orchestration (coming in OpenClaw 2026.4)
- **ACP (Agent Communication Protocol)** — Bridge your IDE to OpenClaw agents for coding workflows

The key principle: **start simple, add complexity only when the current setup becomes a bottleneck**. A well-configured 3-agent team beats a poorly-configured 10-agent mess every time.
