+++
date = '2026-02-14T07:32:00+08:00'
draft = false
title = 'OpenClaw Automation Pitfalls: Installing 3 Skills Is Not Enough'
description = 'Installing tavily-search, find-skills, and proactive-agent on OpenClaw raises the capability ceiling, but without session isolation, task scheduling, and progress reporting, your agent will leak data, corrupt context, and silently fail.'
toc = true
tags = ['OpenClaw', 'Agent', 'Automation', 'Skills', 'Best Practices']
categories = ['AI Guides']
keywords = ['OpenClaw configuration', 'session isolation', 'task isolation', 'agent scheduling', 'AI agent team collaboration', 'dmScope', 'clawdhub', 'proactive-agent', 'OpenClaw pitfalls', 'OpenClaw best practices']
+++

![OpenClaw automation configuration and team collaboration best practices](cover.webp)

You have probably seen this recommendation floating around in every OpenClaw community:

```bash
clawdhub install tavily-search
clawdhub install find-skills
clawdhub install proactive-agent   # formerly proactive-agent-1-2-4, renamed
```

> **Important update (2026-02)**: Many tutorials still reference `clawhub install proactive-agent-1-2-4`. Two things to watch out for:
>
> 1. **CLI name**: The correct tool is **`clawdhub`** (with a "d"), not `clawhub`. Install it via `npm i -g clawdhub`. It is the official CLI for [ClawHub](https://clawhub.ai/).
> 2. **Skill rename**: `proactive-agent-1-2-4` no longer exists on ClawHub. The author [halthelobster](https://clawhub.ai/halthelobster/proactive-agent) has **renamed it to `proactive-agent`** (currently v3.1.0). Running the old install command will return a "Skill not found" error. Use `clawdhub install proactive-agent` instead.

"Give your agent eyes, a toolbox, and initiative --- experience takes off."

I followed the same advice. The first impression was genuinely impressive: the agent could search the web, pick its own tools, and proactively report progress. Within a week, things started falling apart. User A's research appeared in User B's chat. Three consecutive tasks trampled each other's context. The agent said "working on it" and then went silent for 15 minutes.

**The lesson: Skills are the engine, but without a proper chassis, a more powerful engine just means a faster crash.**

This article is not about which Skills to install --- there are plenty of those guides already. It covers the **system-level configuration** you need after installation to make these Skills reliably productive.

If you have not set up OpenClaw yet, start with the [OpenClaw setup tutorial](/posts/ai/2026-02-12-openclaw-usage-tutorial/) first.

---

## 0. Install the ClawdHub CLI First

Before installing any Skill, you need the [ClawdHub CLI](https://docs.openclaw.ai/tools/clawhub) --- the package manager for OpenClaw's Skill ecosystem. It handles searching, installing, updating, and publishing Skills.

### Installation

```bash
# Install globally via npm
npm i -g clawdhub

# Or via pnpm
pnpm add -g clawdhub
```

Verify the installation:

```bash
clawdhub --version
```

### Authentication (optional, required for publishing)

```bash
clawdhub login    # Browser-based OAuth login
clawdhub whoami   # Check current user
```

### Quick Command Reference

| Command | Description |
|---------|-------------|
| `clawdhub search "keyword"` | Search for Skills (supports natural language) |
| `clawdhub install <slug>` | Install a specific Skill |
| `clawdhub install <slug> --version <ver>` | Install a specific version |
| `clawdhub update --all` | Update all installed Skills |
| `clawdhub list` | List installed Skills |
| `clawdhub publish <path>` | Publish a Skill to ClawHub |

### Configuration

ClawdHub supports the following environment variables:

- `CLAWHUB_WORKDIR`: Override the default working directory
- `CLAWHUB_CONFIG_PATH`: Custom token storage path
- `CLAWHUB_DISABLE_TELEMETRY=1`: Disable telemetry

Installed Skills are stored in `<workspace>/skills` by default. OpenClaw automatically loads new Skills on the next session start. See the [ClawdHub documentation](https://docs.openclaw.ai/tools/clawhub) for more details.

---

## 1. What These 3 Skills Actually Do

A quick recap to make sure we are on the same page.

### tavily-search: Giving Your Agent Eyes

By default, OpenClaw cannot access the internet. An agent doing research without search capability is like writing a report blindfolded --- it will produce something perfectly formatted with entirely fabricated facts.

[tavily-search](https://github.com/openclaw/skills/blob/main/skills/arun-8687/tavily-search/SKILL.md) connects to Tavily's AI-optimized search API. Instead of returning raw webpage listings, it returns distilled summary snippets that are easy for agents to consume. It also supports `--deep` mode for in-depth research and `--topic news` for news-only searches.

### find-skills: Giving Your Agent a Tool Index

[ClawHub hosts 5,700+ community Skills](https://github.com/VoltAgent/awesome-openclaw-skills). Without find-skills, your agent can only use its built-in capabilities to tackle any task. With it, the agent can search for existing tools before starting work and install them on the fly.

Think of it this way: without find-skills, your agent is a repair technician carrying only a screwdriver. With it, there is a hardware store next door --- whatever tool is needed, the agent goes and grabs it.

### proactive-agent: Giving Your Agent Initiative

> **Note**: This Skill was previously called `proactive-agent-1-2-4`, which no longer exists on ClawHub. The author halthelobster consolidated and renamed it to **[`proactive-agent`](https://clawhub.ai/halthelobster/proactive-agent)**. Version v3.1.0 adds WAL (Write-Ahead Logging), Working Buffer, and autonomous Cron capabilities. If you installed the old version, run `clawdhub install proactive-agent` to upgrade.

Default OpenClaw is reactive --- it does nothing unless you send a message. proactive-agent enables background condition checking, autonomous task execution, and proactive result reporting.

Together, these three Skills significantly raise your agent's **capability ceiling**. The problem is that the ceiling and your day-to-day experience are separated by a layer of **system infrastructure**.

---

## 2. The Four Most Common Failure Modes

I have personally hit every one of the following scenarios. If you installed the Skills and things still feel off, one of these is almost certainly the cause.

### Failure 1: The "Research Report" Is Entirely Fabricated

**Scenario**: You ask the agent to research a competitor. Five minutes later, it delivers a detailed report complete with data, citations, and analysis. You click the citation links --- all 404s.

**Why it happens**: tavily-search is installed correctly, but the API key has expired, the free quota is exhausted, or the network is unreachable. The critical problem is that **the agent will not tell you the search failed**. It silently falls back to generating answers from training data and presents them as if they were real search results.

**Analogy**: You send an assistant to do market research. They discover the car has no fuel, but instead of telling you, they sit in a coffee shop and write an imaginary report.

**Root cause**: No health check or graceful degradation for the search capability. The agent should explicitly state "I cannot reach the internet right now; the following is based on my training data and may be inaccurate" rather than pretending everything is fine.

**Prevention**:

```json5
// Add a hard rule to the agent's system prompt:
// "If tavily-search fails or returns 0 results,
//  you MUST inform the user. Do NOT substitute training data silently."
```

Also, regularly check your [Tavily Dashboard](https://tavily.com) for API usage and key status.

### Failure 2: Chat Conversations Leak Across Users

**Scenario**: Five team members share the same OpenClaw Agent. User A asks about Client X's contract details. Suddenly, User B's chat window shows Client X's contract information.

**Why it happens**: OpenClaw's default `dmScope` is `main` --- **all DMs share a single session**. The official documentation explicitly warns:

> "If your agent can receive DMs from multiple people, you should strongly consider enabling secure DM mode."
> --- [OpenClaw Session Management](https://docs.openclaw.ai/concepts/session)

**Analogy**: A customer service hotline where every caller is connected to the same microphone in the same room. The previous caller's complaint is clearly audible to the next one.

**Root cause**: Session isolation is not configured. This is OpenClaw's default behavior, not a bug, but it becomes a ticking time bomb in multi-user scenarios.

### Failure 3: Tasks Trample Each Other

**Scenario**: You send three consecutive instructions --- "Research competitor A," "Write a weekly report," "Translate this document." The weekly report contains competitor analysis data, and the translation includes numbers from the report.

**Why it happens**: All three tasks run in the same session and share the same context. Task 2 can see all of Task 1's intermediate results, and Task 3 can see both. When the context window fills up, OpenClaw performs compaction, which further blurs the boundaries between tasks.

**Analogy**: You ask someone to write three different plans on three whiteboards, except all three are actually the same whiteboard. The previous plan's residue bleeds through into the next one.

**Root cause**: No task-level context isolation. [OpenClaw's cron system](https://docs.openclaw.ai/automation/cron-jobs) already supports isolated execution (isolated jobs run in a dedicated `cron:<jobId>` session), but unless you actively use this mechanism, all tasks default to the main session.

### Failure 4: The Agent Goes Silent

**Scenario**: You assign a 15-minute deep research task. The agent replies "Got it, working on it" and then goes quiet. After 10 minutes, you ask for an update. It responds "Still processing." Five minutes later, it dumps a wall of results --- and you have no idea what happened during those 15 minutes, what it got stuck on, or what it skipped.

**Analogy**: You hand a colleague some files to process. They take the files, close the door, and you have no idea whether they are working hard or scrolling social media until the deadline arrives.

**Root cause**: No progress reporting mechanism. From the user's perspective, "no feedback" looks identical to "something went wrong." [Real-world operational experience](https://gist.github.com/digitalknk/ec360aab27ca47cb4106a183b2c25a98) shows that tasks with no status update for over 24 hours have likely failed silently.

---

## 3. The 4 System Configurations You Should Prioritize

The root causes of all four failures above boil down to four pieces of missing system engineering. Listed in priority order --- **you must work top to bottom; skipping ahead will undo your progress**.

### Config 1: Session Isolation (Prevent Data Leaks) --- Highest Priority

This is the baseline for multi-user deployments. Skip this and nothing else matters.

OpenClaw's `dmScope` has four levels, clearly documented in the [official docs](https://docs.openclaw.ai/concepts/session):

| dmScope | Isolation Granularity | Use Case |
|---------|----------------------|----------|
| `main` | No isolation, all DMs shared | Single-user personal use only |
| `per-peer` | Isolated by sender ID | Multiple users, single channel |
| `per-channel-peer` | Isolated by channel + sender | **Recommended**: Multiple users + multiple channels (Telegram + Discord, etc.) |
| `per-account-channel-peer` | Isolated by account + channel + sender | Multiple agent accounts in parallel |

Configuration (edit `~/.openclaw/openclaw.json`):

```json5
{
  session: {
    // Recommended for multi-user, multi-channel deployments
    dmScope: "per-channel-peer",

    // Merge the same person's identities across platforms
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321"],
      bob: ["telegram:111222333", "whatsapp:44455566"]
    },

    // Auto-reset sessions daily at 4 AM to prevent unbounded context growth
    reset: {
      mode: "daily",
      atHour: 4
    }
  }
}
```

**An easy-to-miss detail**: `identityLinks` is not just a convenience feature. If Alice gives an instruction via Telegram and then asks "How's that task going?" on Discord, without identityLinks the Discord session has no knowledge of the Telegram task.

### Config 2: Task Isolation (Prevent Context Pollution)

Session isolation keeps different users separate. Task isolation keeps a single user's multiple tasks from contaminating each other.

Core principle: **The main session handles dispatch only. Heavy tasks must run in sub-sessions.**

Think of it this way: the main session is your inbox; sub-sessions are dedicated workbenches for each task. You would not pile three projects' files on the same desk --- even though you could, you will eventually grab the wrong document.

OpenClaw's cron system has built-in isolation. An isolated cron job runs in a dedicated `cron:<jobId>` session with **no prior conversation context**:

```json5
// Isolated cron job example: daily news briefing at 8 AM
{
  id: "morning-briefing",
  schedule: { cron: "0 8 * * *", tz: "Asia/Shanghai" },
  payload: {
    kind: "agentTurn",           // Independent agent turn, not the main session
    message: "Search for important AI news from the past 24 hours and generate a briefing",
    model: "claude-sonnet-4-5",  // Can specify a different model
    thinking: "medium"
  },
  delivery: {
    mode: "announce",            // Post results to a specific channel
    channel: "telegram:-1001234567890"
  }
}
```

Compare with a **main-session job** (shared context, suitable for lightweight checks):

```json5
// Main-session job example: check email every 30 minutes
{
  id: "email-check",
  schedule: { every: 1800000 },  // 30 minutes
  payload: {
    kind: "systemEvent",          // System event, uses main session
    text: "Check for new important emails"
  },
  wake: "next-heartbeat"          // Process on next heartbeat cycle
}
```

**When to isolate, when to share?** The decision is straightforward:

- **Context-dependent** lightweight tasks (quick Q&A, status checks) --- main session
- **Context-independent** heavy tasks (research, code generation, batch processing) --- isolated execution
- **Precisely timed** tasks --- isolated cron jobs
- **Loosely interval-based** batch checks --- main session heartbeat

### Config 3: Concurrency Control (Prevent Resource Stampedes)

Without concurrency limits, proactive-agent's "initiative" becomes a liability. It might kick off five deep research tasks simultaneously, each calling the Tavily API and an LLM, instantly exhausting your API quota and spiking token costs.

[An ops engineer's field notes](https://gist.github.com/digitalknk/ec360aab27ca47cb4106a183b2c25a98) provide practical guidance:

```json5
{
  // Main task concurrency limit
  maxConcurrent: 4,

  // Sub-agent concurrency limit (parallel research, batch processing, etc.)
  subagents: {
    maxConcurrent: 8
  }
}
```

**Why not set it too high**: A bad task stuck in a retry loop will consume all concurrency slots, blocking every other task from running. This is **cascading failure** --- one task exploding takes down everything.

**Why not set it too low**: Setting it to 1 makes everything serial, completely wasting proactive-agent's parallel capabilities.

Practical recommendation: 4 main tasks + 8 sub-agents works for most team scenarios. If your monthly API budget is under $50, drop main tasks to 2-3.

**The key cost-saving trick**: Use cheap models as "gatekeepers" and expensive models for actual work.

```json5
{
  // Heartbeat and status checks use a cheap model
  heartbeat: {
    model: "gpt-4o-mini"   // "Tens of thousands of tokens for heartbeat checks cost pennies"
  },
  // Real reasoning tasks use a premium model
  tasks: {
    model: "claude-sonnet-4-5"
  }
}
```

### Config 4: Progress Reporting (Prevent Information Black Holes)

No reporting equals playing dead. This is not just a UX problem --- operational experience shows that **tasks with no status update for over 24 hours have most likely failed silently**.

Minimum reporting cadence (add as hard rules in the agent's system prompt):

| Phase | Requirement | Example |
|-------|-------------|---------|
| **Acknowledgment** | Reply immediately with estimated duration | "Received. Estimated 10 minutes. I will search for the latest data first, then compile the report." |
| **In progress** | Update every 2-5 minutes | "Completed data collection for competitors A and B. Analyzing C now, approximately 5 minutes remaining." |
| **Blocked** | Report immediately with reason and next step | "Tavily search returned 0 results, keywords may be too narrow. Retrying with broader terms." |
| **Complete** | Deliver results + one-sentence summary | "Report complete. Key finding: Competitor A has a 15% price advantage but weaker feature coverage than us." |

**Going further**: If you use Todoist or a similar task manager, have the agent sync each task's status there. Open Todoist and you see Queue / Active / Blocked / Done at a glance --- far more efficient than scrolling through chat history.

---

## 4. Complete Production Template for 5-10 Person Teams

Combining all four configurations, here is a ready-to-use template for teams of 5-10 people.

### Access Layer: Control Who Can Talk to the Agent

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    dmScope: "per-channel-peer",
    identityLinks: {
      // Merge the same person's IDs across platforms
      alice: ["telegram:111", "discord:222"],
      bob: ["telegram:333", "whatsapp:444"]
    },
    reset: { mode: "daily", atHour: 4 }
  },

  // Group chat: require @mention to prevent false triggers
  groups: {
    requireMention: true
  }
}
```

### Execution Layer: Control How Tasks Run

```json5
{
  maxConcurrent: 3,           // Main task concurrency limit
  subagents: {
    maxConcurrent: 6          // Sub-agent concurrency limit
  },

  // Model routing: the key to cost efficiency
  models: {
    coordinator: "claude-sonnet-4-5",  // Mid-tier model for dispatch
    heartbeat: "gpt-4o-mini",          // Cheap model for heartbeat checks
    deepWork: "claude-opus-4"          // Top-tier model for deep tasks
  },

  // Retry strategy: exponential backoff to prevent retry storms
  retry: {
    maxAttempts: 2,
    backoff: "30s -> 1m -> 5m"   // OpenClaw built-in exponential backoff
  }
}
```

### Scheduling Layer: Control When Things Run

```json5
// ~/.openclaw/cron/jobs.json
[
  // 1. Daily 8 AM: news briefing (isolated, does not pollute main session)
  {
    id: "morning-briefing",
    schedule: { cron: "0 8 * * *", tz: "Asia/Shanghai" },
    payload: {
      kind: "agentTurn",
      message: "Search for important news from the past 24 hours and generate a briefing",
      model: "claude-sonnet-4-5"
    },
    delivery: { mode: "announce", channel: "telegram:xxx" }
  },

  // 2. Every 30 minutes: email check (main session, lightweight)
  {
    id: "email-monitor",
    schedule: { every: 1800000 },
    payload: { kind: "systemEvent", text: "Check for new emails" },
    wake: "next-heartbeat"
  },

  // 3. Every Friday 5 PM: weekly review (isolated)
  {
    id: "weekly-review",
    schedule: { cron: "0 17 * * 5", tz: "Asia/Shanghai" },
    payload: {
      kind: "agentTurn",
      message: "Summarize tasks completed this week, blockers encountered, and next week's plan",
      model: "claude-sonnet-4-5",
      thinking: "medium"
    },
    delivery: { mode: "announce", channel: "telegram:xxx" }
  }
]
```

### Reporting Layer: Control What Users See

Add these hard rules to the agent's system prompt:

```markdown
## Task Execution Rules (Mandatory)

1. Acknowledge every task immediately with an estimated completion time
2. Report progress every 3 minutes (what you are doing, what is done, what remains)
3. Report blockers immediately (cause + your next step)
4. If web search fails, you MUST inform the user explicitly. Do NOT silently substitute training data
5. On completion: provide a summary (3 sentences max) + detailed results
```

### Governance Layer: 15-Minute Weekly Review

Spend 15 minutes each week reviewing three things:

1. **Which tasks appeared 3+ times?** --- Codify them into Skills or cron jobs
2. **Which tasks timed out or failed?** --- Analyze root causes and adjust configuration
3. **What was this week's API cost?** --- Check for tasks stuck in retry loops burning money

---

## Summary

Back to the original question: "Will installing 3 Skills make OpenClaw better?"

**Yes. But that is only step one.**

tavily-search provides search capability. find-skills provides tool discovery. proactive-agent provides initiative. These three Skills raise the **capability ceiling**. But daily reliability depends on the **system floor** --- four configurations you must implement:

| Configuration | Problem Solved | Cost of Skipping |
|--------------|----------------|-----------------|
| **Session isolation** | Cross-user data leaks | Client A's data exposed to Client B |
| **Task isolation** | Cross-task context pollution | Weekly report contains competitor analysis data |
| **Concurrency control** | Resource stampedes, cost blowouts | API quota exhausted, monthly bill 5x higher |
| **Progress reporting** | Users cannot tell what the agent is doing | Tasks fail silently for 24 hours before discovery |

**First controllable, then efficient. First stable, then scalable.** Get these four things right, and your OpenClaw deployment transforms from "occasionally impressive" to "consistently deliverable."

---

## Related Reading

- [OpenClaw Complete Setup Tutorial (From Zero to Usable)](/posts/ai/2026-02-12-openclaw-usage-tutorial/)
- [OpenClaw Architecture Deep Dive: From Message to Execution](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/)
- [OpenClaw x Claude Code Workflow in Practice](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)
- [OpenClaw Memory System Strategy (MEMORY.md in Practice)](/posts/ai/2026-01-31-openclaw-memory-strategy/)
- [Skill Design Patterns for Claude Code](/posts/ai/2026-01-12-claudecode-skill-patterns/)
- [AI-Era Workflows: A Complete Guide from Idea to Delivery](/posts/ai/2026-01-30-ai-workflow-real-guide/)
