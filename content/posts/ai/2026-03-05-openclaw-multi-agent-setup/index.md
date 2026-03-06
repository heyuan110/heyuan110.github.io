+++
date = '2026-03-04T19:00:00+08:00'
draft = false
title = 'OpenClaw Multi-Agent Setup: Build AI Teams That Work'
description = 'Step-by-step OpenClaw multi-agent setup guide. Configure agent teams, communication patterns, Tavily search, messaging bindings, and 4 collaboration patterns.'
toc = true
tags = ['OpenClaw', 'Multi-Agent', 'AI Agents', 'Tavily', 'Agent Architecture']
categories = ['AI Guides']
keywords = ['OpenClaw multi-agent', 'OpenClaw multi agent setup', 'OpenClaw agent configuration', 'OpenClaw Tavily', 'OpenClaw multi-agent architecture', 'proactive-agent', 'proactive-agent-1-2-4', 'OpenClaw agent team', 'sessions_send', 'OpenClaw bindings']

[[params.faqItems]]
question = "How do I set up multiple agents in OpenClaw?"
answer = "Use 'openclaw agents add <name>' to create each agent with its own model, workspace, and identity. Each agent gets isolated memory, sessions, and configuration under ~/.openclaw/agents/<agentId>/. Then configure bindings in openclaw.json to route messages from specific channels or groups to the correct agent."

[[params.faqItems]]
question = "What is the best OpenClaw multi-agent collaboration pattern?"
answer = "Start with the Supervisor pattern: one main agent receives all requests, delegates to specialist agents (writer, coder, researcher), and consolidates results. This covers 80% of use cases. Upgrade to Pipeline or Parallel patterns only when you need sequential processing chains or simultaneous independent tasks."

[[params.faqItems]]
question = "How do OpenClaw agents communicate with each other?"
answer = "Agents communicate via the built-in sessions_send tool, which works like an internal messaging system. You must explicitly enable agent-to-agent communication in openclaw.json under tools.agentToAgent with an allow-list of authorized agents. Communication is disabled by default for security."

[[params.faqItems]]
question = "What happened to proactive-agent-1-2-4?"
answer = "The skill proactive-agent-1-2-4 has been renamed to proactive-agent on ClawHub. Install it with 'clawdhub install proactive-agent' (current version v3.1.0). The old name proactive-agent-1-2-4 will return a 'Skill not found' error. Also note the CLI is 'clawdhub' (with a d), not 'clawhub'."

[[params.faqItems]]
question = "Can I use different AI models for different OpenClaw agents?"
answer = "Yes. Each agent can run a different model. For example, use Claude for coding tasks, DeepSeek for writing, GPT-4o for research with web browsing, and GLM for Chinese creative brainstorming. Configure models per agent in the agent's auth-profiles.json and models.json files."
+++

![OpenClaw multi-agent setup guide showing AI team architecture](cover.webp)

You built an OpenClaw personal assistant. It handles your Telegram messages, searches the web, writes drafts, reviews code. Life is good.

Then reality hits. You ask it to research a competitor, and it responds with coding suggestions from yesterday's conversation. You ask it to write an article, and it pulls in debugging context from a completely unrelated project. Your single agent is drowning in accumulated memory, and every response gets slower and more confused.

**The fix is not a better prompt. The fix is a team.**

This guide walks you through setting up multiple OpenClaw agents that work together as a coordinated team. You will learn the architecture, the configuration, the communication patterns, and the real-world collaboration models that make multi-agent systems practical -- not just theoretical.

If you are new to OpenClaw, start with the [beginner tutorial](/posts/ai/2026-02-12-openclaw-usage-tutorial/) first. For those already running a single agent, this guide picks up exactly where that leaves off.

## Why a Single Agent Is Not Enough

### Three Walls You Will Hit

Most people start with one agent doing everything. That works fine for the first week. Then three problems emerge:

| Problem | Symptom | Root Cause |
|---------|---------|------------|
| **Memory bloat** | Responses get slower over time | Memory files (USER.md, memory/) grow endlessly; every conversation loads all history |
| **Context contamination** | Answers "leak" across domains | Writing advice bleeds into code reviews; research data pollutes creative output |
| **Cost explosion** | Token usage far exceeds expectations | Every API call carries irrelevant background context, inflating input tokens |

Think of it like a browser with 50 open tabs. Each tab makes your machine slower, and you keep clicking the wrong one. The answer is not a faster computer -- it is closing the tabs you don't need.

### The Multi-Agent Principle

The core idea is simple: **specialized agents for specialized work**.

- A **writing agent** knows only writing techniques, style guides, and content templates
- A **coding agent** knows only project code, tech docs, and debugging workflows
- A **research agent** knows only search tools, data sources, and information synthesis

Each agent gets its own brain (memory), its own office (workspace), and its own journal (session history). They do not interfere with each other.

> One person can be an army -- but only if you assign the right roles.

## OpenClaw Multi-Agent Architecture Overview

### Three-Layer Isolation

In OpenClaw, each agent is not just a name. It is a **fully independent virtual worker** with physical isolation at three levels:

```
~/.openclaw/agents/<agentId>/
├── agent/                    # Identity layer
│   ├── auth-profiles.json    # API key configuration
│   └── models.json           # Model selection
└── sessions/                 # State layer
    ├── <session-id>.jsonl    # Independent chat history
    └── sessions.json         # Session index

~/.openclaw/workspace-<agentId>/
├── SOUL.md                   # Personality definition
├── AGENTS.md                 # Behavioral rules
├── USER.md                   # User context
├── PROMPT.md                 # Prompt templates
├── IDENTITY.md               # Identity definition
└── memory/                   # Memory storage
```

| Layer | Directory | Purpose | Analogy |
|-------|-----------|---------|---------|
| **Identity** | `agents/<id>/agent/` | Which model, which API key | Employee badge |
| **State** | `agents/<id>/sessions/` | Independent chat records and routing state | Work journal |
| **Workspace** | `workspace-<id>/` | Independent files, prompts, memory | Private office |

This isolation is physical, not logical. Your writing agent literally cannot see the coding agent's files. The coding agent never encounters the writing agent's style guides. No prompt engineering needed to maintain separation -- the filesystem enforces it.

### The Bindings System: Message Routing

When a message arrives, how does OpenClaw know which agent should handle it? Through **Bindings** -- a deterministic routing system with a clear priority chain:

```
Priority 1: Exact peer match (DM/group ID)
Priority 2: Parent peer match (thread inheritance)
Priority 3: guildId + role (Discord-specific)
Priority 4: guildId match
Priority 5: teamId (Slack-specific)
Priority 6: accountId match
Priority 7: Channel-level match
Priority 8: Default agent fallback
```

The rule is straightforward: **more specific rules always win**. If you bind a Telegram group to a specific agent, messages from that group will always go to that agent. No ambiguity, no surprises.

Multiple conditions within a binding use AND logic -- all conditions must match. If multiple rules match at the same priority level, the first one in the config file wins.

## Step-by-Step: Setting Up Your First Multi-Agent Team

### Step 1: Create Your Agents

Use the CLI to create isolated agents:

```bash
# Create a writing agent using DeepSeek (good cost/quality ratio)
openclaw agents add writer \
  --model deepseek/deepseek-chat \
  --workspace ~/.openclaw/workspace-writer

# Create a research agent using GPT-4o (strong at web browsing and synthesis)
openclaw agents add researcher \
  --model openai/gpt-4o \
  --workspace ~/.openclaw/workspace-researcher

# Create a coding agent using Claude (best at code understanding)
openclaw agents add coder \
  --model anthropic/claude-sonnet-4-6 \
  --workspace ~/.openclaw/workspace-coder
```

A key design advantage: **each agent can run a different model**. Match the model to the task:

| Agent | Recommended Model | Why |
|-------|-------------------|-----|
| Research | gpt-4o | Strong multimodal understanding, good at information synthesis |
| Writing | deepseek-chat | Cost-effective, stable logical output |
| Coding | claude-sonnet | Top-tier code generation and comprehension |
| Brainstorm | glm-4.7 | Strong creative ability, especially in Chinese |

### Step 2: Define Each Agent's Soul

Creating an agent gives it a body. The soul comes from its workspace files.

**SOUL.md** -- personality and expertise:

```markdown
# Writer Agent

## Role
You are a senior technical content writer. Your expertise is transforming
complex technical topics into clear, engaging articles.

## Style
- Open every piece with a relatable scenario or counterintuitive claim
- Keep paragraphs short -- mobile-friendly
- Use analogies to explain complex concepts
- End with a clear call-to-action

## Boundaries
- Never use filler phrases like "it goes without saying"
- Explain every technical term on first use
- Stay in your lane -- do not write code, do not do research
```

**AGENTS.md** -- behavioral rules:

```markdown
# Work Standards

## Output Format
- All articles in Markdown
- Heading levels: H2 > H3 > H4 maximum
- Code blocks must specify language

## Workflow
1. Outline first, get confirmation, then write
2. Each paragraph under 150 words
3. Self-check SEO elements before submitting
```

**USER.md** -- user context:

```markdown
# User Profile

## Identity
Technical blogger focused on AI tools and developer productivity.

## Preferences
- Tone: professional but approachable
- Audience: developers and product managers interested in AI
- Platforms: personal blog + social media
```

The more precisely you define these files, the more consistent the agent's output becomes. Think of it as writing a job description -- vague descriptions produce vague work.

### Step 3: Set Identity Labels

Give each agent a recognizable identity in your messaging platforms:

```bash
openclaw agents set-identity --agent writer --name "Writer" --emoji "pen"
openclaw agents set-identity --agent researcher --name "Researcher" --emoji "mag"
openclaw agents set-identity --agent coder --name "Coder" --emoji "zap"
```

### Step 4: Bind Agents to Message Channels

Now connect agents to specific groups or chats. OpenClaw supports Telegram, Feishu/Lark, Discord, WhatsApp, and more.

#### Telegram Binding

Create a Telegram group for each agent, then get the Chat ID. Add your bot to the group, then visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and find the `chat.id` field (group IDs are negative numbers).

Configure bindings in `openclaw.json`:

```json
{
  "bindings": [
    {
      "agentId": "writer",
      "match": {
        "channel": "telegram",
        "peer": {
          "kind": "group",
          "id": "-1001234567890"
        }
      }
    },
    {
      "agentId": "researcher",
      "match": {
        "channel": "telegram",
        "peer": {
          "kind": "group",
          "id": "-1009876543210"
        }
      }
    },
    {
      "agentId": "coder",
      "match": {
        "channel": "telegram",
        "peer": {
          "kind": "group",
          "id": "-1005551234567"
        }
      }
    }
  ]
}
```

Enable the Telegram channel:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    }
  }
}
```

#### Feishu/Lark Binding

For Feishu, the setup is identical except the channel is `feishu` and the peer ID uses Feishu's `oc_` format:

```json
{
  "bindings": [
    {
      "agentId": "writer",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_abc123def456"
        }
      }
    }
  ],
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a9f21xxxxx89bcd",
      "appSecret": "w6cPunaxxxxBl1HHtdF",
      "groups": {
        "oc_abc123def456": { "requireMention": false }
      }
    }
  }
}
```

Setting `requireMention: false` turns a group into a private office -- the agent responds to every message without needing an @mention. Remember to enable the `im:message.group_msg` permission in the Feishu developer console.

| Feature | Telegram | Feishu/Lark |
|---------|----------|-------------|
| **Peer ID format** | Negative number | `oc_` string |
| **Bot creation** | @BotFather | Feishu Open Platform |
| **No-mention mode** | Set bot as group admin | `requireMention: false` + permission |
| **Best for** | Personal use, global access | Enterprise teams, internal workflows |

You can absolutely **bind both platforms simultaneously** -- Feishu for work tasks, Telegram for personal use. Cross-platform operation is where multi-agent architecture truly shines.

## Agent-to-Agent Communication Patterns

Setting up isolated agents is step one. Making them collaborate is where the real value lives.

### The sessions_send Mechanism

Agents communicate through OpenClaw's built-in `sessions_send` tool -- an internal message bus between agents:

```
User sends request → Main agent receives it
                        ↓
                  Analyzes task type
                  ↙     ↓      ↘
           researcher  writer   coder
                  ↘     ↓      ↙
                  Consolidates results
                        ↓
                  Main agent responds to user
```

### Enabling Agent Communication

Agent-to-agent communication is **disabled by default** -- a security-first design. Enable it explicitly:

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "researcher", "writer", "coder"]
    }
  }
}
```

Key points:

- **Allowlist only**: Only agents in the `allow` array can communicate
- **Principle of least privilege**: Not every agent needs to talk to every other agent. A writer may never need to contact the coder directly
- **Audit trail**: All inter-agent messages are logged in session files for debugging

### Designing the Supervisor Agent

The most effective pattern is a **supervisor agent** (typically called `main`) whose job is not to do work, but to receive requests and delegate:

```markdown
# Main Agent - SOUL.md

## Role
You are the team coordinator. Your responsibilities:

1. **Receive**: Understand the user's request
2. **Route**: Identify task type and assign to the right specialist
3. **Review**: Check the specialist's output quality
4. **Report**: Consolidate results and respond to the user

## Routing Rules
- Research, fact-checking, data gathering → @researcher
- Article writing, content editing → @writer
- Code generation, debugging, technical implementation → @coder
- Simple questions, casual conversation → handle yourself

## Communication Format
When delegating, always include:
- Clear task description
- Expected output format
- Relevant context from the user's request
```

This design provides not just division of labor, but **supervision and fault tolerance**. When a specialist agent gets stuck or returns low-quality output, the supervisor can intervene, request corrections, or handle the task itself.

## Configuring Tavily Search Integration for Agents

Research agents need eyes on the internet. [Tavily](https://tavily.com/) is the most popular search integration in the OpenClaw ecosystem, purpose-built for AI agent use.

### Installing Tavily

```bash
# Install via ClawHub (note: it's clawdhub with a 'd')
clawdhub install tavily-search
```

Get your API key from [tavily.com](https://tavily.com/) and add it to your environment:

```bash
# Add to your shell profile or .env
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxx"
```

### Agent-Specific Search Configuration

Not every agent needs search. Assign Tavily selectively:

```json
{
  "agents": {
    "list": [
      {
        "id": "researcher",
        "tools": {
          "allow": ["tavily-search", "browser", "read"],
          "deny": ["exec", "write"]
        }
      },
      {
        "id": "writer",
        "tools": {
          "allow": ["read"],
          "deny": ["tavily-search", "exec"]
        }
      },
      {
        "id": "coder",
        "tools": {
          "allow": ["exec", "read", "write"],
          "deny": ["tavily-search", "browser"]
        }
      }
    ]
  }
}
```

The researcher gets search and browsing. The writer gets read-only access. The coder gets execution privileges but no web access. Each agent has exactly the tools it needs -- nothing more.

### Combining with proactive-agent

The [proactive-agent](https://clawhub.ai/halthelobster/proactive-agent) skill (formerly known as **proactive-agent-1-2-4**) gives your agents initiative -- they can report progress, ask clarifying questions, and work on multi-step tasks without constant prompting.

```bash
# Install proactive-agent (renamed from proactive-agent-1-2-4)
clawdhub install proactive-agent
```

> **Important note**: Many tutorials still reference `proactive-agent-1-2-4`, but the author renamed it to `proactive-agent` (current version v3.1.0). Also, the CLI command is `clawdhub` (with a 'd'), not `clawhub`. See our detailed breakdown in [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) for more on this.

When combined with Tavily, your research agent can autonomously search for information, synthesize findings, and proactively report results back to the supervisor -- without you having to check in at every step.

## Four Collaboration Patterns

Based on established multi-agent research from [LangChain](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) and [Google's design patterns](https://www.infoq.com/news/2026/01/multi-agent-design-patterns/), four primary collaboration models apply to OpenClaw:

### 1. Pipeline Pattern

```
User request
    ↓
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Researcher│ →  │  Writer  │ →  │ Reviewer │
└──────────┘    └──────────┘    └──────────┘
                                      ↓
                                 Final output
```

**How it works**: Tasks flow sequentially. Each agent's output becomes the next agent's input. Like a factory assembly line.

**OpenClaw implementation**: The supervisor orchestrates a chain via `sessions_send`:

```
Step 1: @researcher "Find the latest benchmarks for Claude 4.6 vs GPT-4o"
Step 2: @writer "Write a comparison article using this research: {researcher_output}"
Step 3: @reviewer "Check this draft for accuracy and readability: {writer_output}"
Step 4: Supervisor consolidates and delivers final result
```

**Best for**:
- Content production: research then write then review
- Code development: design then implement then test
- Data pipelines: collect then clean then analyze

### 2. Parallel Pattern

```
         User request
              ↓
       ┌──────────────┐
       │  Task Splitter │
       └──┬────┬────┬──┘
          ↓    ↓    ↓      ← simultaneous
       ┌───┐ ┌───┐ ┌───┐
       │ A │ │ B │ │ C │
       └─┬─┘ └─┬─┘ └─┬─┘
         ↓     ↓     ↓
       ┌──────────────┐
       │  Aggregator   │
       └──────────────┘
```

**How it works**: One task splits into independent subtasks. Multiple agents work simultaneously. Results merge at the end.

**Best for**:
- Competitive analysis: each agent researches a different competitor
- Multi-perspective review: security agent, performance agent, and maintainability agent review the same code
- Multi-language translation: same content translated into multiple languages simultaneously

### 3. Supervisor Pattern

```
         User request
              ↓
      ┌───────────────┐
      │  Supervisor    │
      │  (main agent)  │
      └──┬─────┬───┬──┘
         ↓     ↓   ↓
      ┌───┐ ┌───┐ ┌───┐
      │ A │ │ B │ │ C │
      └───┘ └───┘ └───┘
         ↓     ↓   ↓
      ┌───────────────┐
      │  Review & Output│
      └───────────────┘
```

**How it works**: A central supervisor receives all requests, breaks them into subtasks, assigns them to specialists, reviews results, and delivers consolidated output.

**OpenClaw implementation** -- complete configuration:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace-main",
        "model": "anthropic/claude-sonnet-4-6"
      },
      {
        "id": "writer",
        "workspace": "~/.openclaw/workspace-writer",
        "model": "deepseek/deepseek-chat"
      },
      {
        "id": "researcher",
        "workspace": "~/.openclaw/workspace-researcher",
        "model": "openai/gpt-4o"
      },
      {
        "id": "coder",
        "workspace": "~/.openclaw/workspace-coder",
        "model": "anthropic/claude-sonnet-4-6"
      }
    ]
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "writer", "researcher", "coder"]
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "peer": { "kind": "group", "id": "-1001234567890" }
      }
    }
  ]
}
```

**Best for**:
- Personal assistant with a single entry point
- Tasks requiring cross-domain collaboration
- Situations needing quality control and output review

### 4. Swarm Pattern

```
      ┌───┐  ←→  ┌───┐
      │ A │       │ B │
      └─┬─┘      └─┬─┘
        ↕    ←→    ↕
      ┌───┐  ←→  ┌───┐
      │ C │       │ D │
      └───┘       └───┘
```

**How it works**: No central coordinator. Agents communicate peer-to-peer, self-organize, and hand off tasks based on their own judgment. Inspired by [OpenAI's Swarm framework](https://github.com/openai/swarm).

**OpenClaw implementation**: Enable full agent-to-agent communication without a designated supervisor. Each agent's SOUL.md includes routing logic for when to hand off to other agents.

**Best for**:
- Complex, unpredictable workflows where rigid orchestration fails
- Autonomous teams handling diverse, evolving tasks
- Advanced setups after you have mastered the other three patterns

**Word of caution**: Swarm is the hardest to debug. Start with Supervisor, graduate to Pipeline or Parallel, and only consider Swarm when you have a clear need.

### Choosing the Right Pattern

You do not need a complex architecture on day one. Follow this progression:

```
Single agent + tools
    ↓ (context contamination starts)
Single agent + skills
    ↓ (memory bloat, cost explosion)
Supervisor + 2-3 specialist agents
    ↓ (need more complex collaboration)
Pipeline / Parallel hybrid
    ↓ (need autonomous coordination)
Swarm (advanced)
```

> **Core principle**: Adding tools beats adding agents. Only upgrade to multi-agent when you hit a clear wall with your current setup.

## Real-World Use Cases

### Use Case 1: Code Review + Deploy Pipeline

```
Developer pushes code → main agent receives notification
    ↓
@coder: "Review this PR for bugs, security issues, and style violations"
    ↓
@researcher: "Check if any dependencies have known vulnerabilities"
    ↓
main agent consolidates reviews → posts summary to Telegram group
    ↓
If approved → triggers deploy script via coder agent
```

### Use Case 2: Research + Write Content Pipeline

```
User: "Write an article about the latest MCP protocol updates"
    ↓
@researcher: Search Tavily for recent MCP news, read official docs
    ↓
@writer: "Write an article using this research: {research_output}"
    ↓
main agent reviews draft → requests revisions if needed → delivers final
```

### Use Case 3: Monitor + Alert System

```
Cron job triggers every 30 minutes:
    ↓
@researcher: "Check GitHub releases for OpenClaw, Claude Code, Cursor"
    ↓
If new release found → @writer: "Summarize the changelog"
    ↓
main agent posts alert to Telegram with summary
```

This uses OpenClaw's built-in Heartbeat and Cron features. For details on how these work under the hood, see our [architecture deep dive](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/).

## Performance Optimization and Cost Management

### Model Selection by Task

The biggest lever for cost control is matching models to tasks:

| Task Type | Recommended Model | Approximate Cost | Reasoning |
|-----------|-------------------|------------------|-----------|
| Simple routing/delegation | Any small model | Lowest | Supervisor just needs to classify and forward |
| Research + synthesis | gpt-4o | Medium | Strong at browsing and information fusion |
| Long-form writing | deepseek-chat | Low | Excellent quality-to-cost ratio |
| Code generation | claude-sonnet | Medium-High | Best code understanding and generation |
| Complex reasoning | claude-opus | Highest | Reserve for genuinely difficult problems |

### Reducing Inter-Agent Token Waste

Every `sessions_send` call is an API call. Minimize unnecessary communication:

1. **Supervisor pre-filtering**: Have the main agent handle simple questions itself instead of always delegating
2. **Structured handoffs**: Pass JSON-structured data between agents, not free-form text. Structured data is smaller and less ambiguous
3. **Context trimming**: Each agent should summarize its output before passing to the next agent in a pipeline, not dump the full conversation

```json
{
  "agentToAgent": {
    "maxContextTokens": 4000,
    "summaryMode": "auto"
  }
}
```

### Lightweight Models for Sub-Agents

Your supervisor agent needs to be smart (Claude Sonnet or GPT-4o). But specialist agents doing narrow, well-defined tasks can often use cheaper models:

```json
{
  "agents": {
    "list": [
      { "id": "main", "model": "anthropic/claude-sonnet-4-6" },
      { "id": "formatter", "model": "deepseek/deepseek-chat" },
      { "id": "translator", "model": "deepseek/deepseek-chat" }
    ]
  }
}
```

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Too Many Agents

**Problem**: Creating 10 agents "just in case" leads to communication overhead, management complexity, and idle resources.

**Rule of thumb**:
- **Personal use**: 3-5 agents (supervisor + 2-4 specialists)
- **Team use**: 2-3 agents per business line
- **Merge signal**: If two agents handle the same task type 80% of the time, combine them

### Pitfall 2: Missing Session Isolation

**Problem**: Agent A's research results appear in Agent B's conversation. This happens when bindings are misconfigured or when `dmScope` is not set correctly.

**Fix**: Verify each agent's binding targets the correct peer ID. Test by sending a message to each group and checking which agent responds. Also set `dmScope` to `agent` to isolate direct message contexts:

```json
{
  "agents": {
    "list": [
      {
        "id": "writer",
        "dmScope": "agent"
      }
    ]
  }
}
```

### Pitfall 3: Circular Delegation

**Problem**: Agent A delegates to Agent B, which delegates back to Agent A. Infinite loop, burning tokens.

**Fix**: Establish clear hierarchy in SOUL.md files. Only the supervisor should delegate. Specialist agents should never delegate to other specialists -- they should return results to the supervisor, which then decides the next step.

### Pitfall 4: Ignoring the proactive-agent Skill

**Problem**: Agents go silent during long tasks. You have no idea if they are working, stuck, or failed.

**Fix**: Install [proactive-agent](https://clawhub.ai/halthelobster/proactive-agent) (`clawdhub install proactive-agent`). This skill enables progress reporting, so agents proactively send status updates during multi-step tasks. Combined with the supervisor pattern, the main agent can track all sub-agent progress and alert you if something stalls.

### Pitfall 5: Unstructured Inter-Agent Communication

**Problem**: Agent A sends a lengthy, conversational response to Agent B. Agent B misinterprets the intent and produces wrong output.

**Fix**: Define communication templates in each agent's AGENTS.md:

```markdown
## Inter-Agent Communication Format

When receiving a task from another agent, expect this structure:
- **task**: What to do (one sentence)
- **context**: Relevant background (bullet points)
- **format**: Expected output format
- **deadline**: Priority level (immediate/normal/low)

When returning results, use:
- **status**: complete/partial/failed
- **result**: The actual output
- **notes**: Any caveats or follow-up needed
```

## Getting Started: Your First Multi-Agent Config

Here is a complete, minimal configuration to get a three-agent team running on Telegram:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN"
    }
  },
  "agents": {
    "defaultAgent": "main",
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace-main",
        "model": "anthropic/claude-sonnet-4-6"
      },
      {
        "id": "writer",
        "workspace": "~/.openclaw/workspace-writer",
        "model": "deepseek/deepseek-chat",
        "dmScope": "agent"
      },
      {
        "id": "coder",
        "workspace": "~/.openclaw/workspace-coder",
        "model": "anthropic/claude-sonnet-4-6",
        "dmScope": "agent"
      }
    ]
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "writer", "coder"]
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "peer": { "kind": "group", "id": "YOUR_MAIN_GROUP_ID" }
      }
    },
    {
      "agentId": "writer",
      "match": {
        "channel": "telegram",
        "peer": { "kind": "group", "id": "YOUR_WRITER_GROUP_ID" }
      }
    },
    {
      "agentId": "coder",
      "match": {
        "channel": "telegram",
        "peer": { "kind": "group", "id": "YOUR_CODER_GROUP_ID" }
      }
    }
  ]
}
```

Steps to deploy:

1. Replace `YOUR_BOT_TOKEN` with your Telegram bot token from @BotFather
2. Create three Telegram groups and replace the group IDs
3. Create workspace directories and add SOUL.md, AGENTS.md, USER.md to each
4. Install key skills: `clawdhub install tavily-search && clawdhub install proactive-agent`
5. Start OpenClaw and test by sending messages to each group

## Summary

Multi-agent architecture follows the same principles as managing a real team:

1. **Hire right** -- Create agents with the right models for the right tasks
2. **Define roles** -- Write SOUL.md and AGENTS.md with clear boundaries
3. **Build channels** -- Configure bindings and enable agent-to-agent communication
4. **Supervise** -- Set up a main agent for quality control and coordination

Start with a supervisor and two specialists. Add more agents only when you hit a specific wall. The goal is not the most agents -- it is the right agents doing the right work.

If you find yourself constantly telling your AI assistant "ignore that, focus on this" -- it is time to split into multiple agents.

## Related Reading

- [OpenClaw 2026.3.1: WebSocket Streaming, Agent Routing, and K8s Support](/posts/ai/2026-03-03-openclaw-2026-3-1-new-features/) -- Latest features including the new agent routing CLI
- [OpenClaw Automation Pitfalls: Installing 3 Skills Does Not Mean It Works](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) -- Session isolation, proactive-agent setup, and real failure cases
- [OpenClaw Architecture Deep Dive](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) -- How messages flow from Gateway to Agent to execution
- [OpenClaw Memory Strategy: Tool-Driven RAG and On-Demand Recall](/posts/ai/2026-01-31-openclaw-memory-strategy/) -- How memory works across isolated agents
- [Claude Code Agent Teams: Multi-Agent Collaborative Development](/posts/ai/2026-02-22-claude-code-agent-teams/) -- A parallel approach to multi-agent in coding workflows
- [Agentic Coding Trends in 2026](/posts/ai/2026-02-23-agentic-coding-trends-2026/) -- Where multi-agent development is heading
