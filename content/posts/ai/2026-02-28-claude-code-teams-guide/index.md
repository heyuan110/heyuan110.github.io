+++
date = '2026-02-27T10:00:00+08:00'
draft = false
title = 'Claude Code Teams Guide 2026: Multi-Agent Setup & Collaboration'
description = 'How to use Claude Code Agent Teams (teammate-mode) for multi-agent coding. Setup, tmux split-pane, collaboration patterns, worktree isolation, and cost control tips.'
toc = true
tags = ['Claude Code', 'Agent Teams', 'Multi-Agent', 'Collaboration']
categories = ['AI Guides']
keywords = ['claude code teams', 'claude code team plan 2026', 'claude code agent teams', 'claude code multi-agent', 'claude code teammate mode', 'multi-agent collaboration', 'claude code teams guide 2026', 'ai team collaboration']

[[params.faqItems]]
question = "How do I enable Claude Code Agent Teams?"
answer = "Set the environment variable CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 before launching Claude Code, or add it to your ~/.claude/settings.json under the env key. Agent Teams is still an experimental feature as of February 2026."

[[params.faqItems]]
question = "What is the difference between Agent Teams and Subagents in Claude Code?"
answer = "Subagents use one-way hierarchical communication where a parent delegates isolated tasks. Agent Teams support multi-directional messaging between a Team Lead and Teammates, enabling lateral coordination. Use Subagents for cleanly decomposable tasks and Agent Teams for complex tasks with interdependencies."

[[params.faqItems]]
question = "What display modes does Claude Code Agent Teams support?"
answer = "Agent Teams supports two display modes: in-process mode (default, works in any terminal) where agents share one window, and split-pane mode (requires tmux or iTerm2) where each Teammate gets its own pane for simultaneous viewing."

[[params.faqItems]]
question = "How much does Claude Code Agent Teams cost?"
answer = "Agent Teams runs multiple Claude agents simultaneously, each consuming tokens independently. Costs are higher than single-agent usage since multiple Opus or Sonnet instances run in parallel. The exact cost depends on the number of teammates and task complexity."

[[params.faqItems]]
question = "Can Claude Code teammates communicate with each other?"
answer = "Yes, teammates use a mailbox messaging system for lateral communication. When one agent modifies an API interface, it can notify another agent building a frontend that consumes it, enabling real-time coordination instead of discovering conflicts after both agents finish."
+++

![Claude Code Agent Teams multi-agent collaboration patterns](cover.webp)

One agent is good. A coordinated team of agents is transformative.

Since Anthropic released Agent Teams on February 5, 2026, alongside the Opus 4.6 model, [Claude Code](https://docs.anthropic.com/en/docs/claude-code) has crossed a fundamental threshold: you're no longer limited to a single agent working sequentially through your codebase. You can now spin up multiple Claude agents that communicate with each other, divide work, and execute tasks in parallel — like a small engineering team that happens to operate at machine speed.

This guide covers everything you need to know about Claude Code Agent Teams: architecture, setup, real-world collaboration patterns, cost management, and how it compares to the older Subagent and Worktree approaches.

## What Are Agent Teams?

Agent Teams let you run multiple Claude Code agents within a single session. But this isn't just "run five agents at once." The architecture is built around structured coordination.

### The Architecture: Team Lead + Teammates

When you create an Agent Team, one agent acts as the **Team Lead** and the others are **Teammates**. Here's how the pieces fit together:

- **Team Lead**: The agent you interact with directly. It breaks down your request into tasks, assigns them to Teammates, and synthesizes their work into a final result.
- **Teammates**: Independent Claude Code agents, each with their own context window, tool access, and working state. They can read and write files, run commands, and perform any action a normal Claude Code session can.
- **Shared Task List**: A structured, visible list of tasks that the Team Lead creates and Teammates pick up. You can view and modify this list at any time with `Ctrl+T`.
- **Mailbox Messaging**: Teammates communicate with each other and the Team Lead through an internal message-passing system. This is the key architectural innovation — agents don't just work in isolation, they coordinate.

The [Claude Code GitHub repository](https://github.com/anthropics/claude-code) tracks the latest features including Agent Teams.

Think of it like this: the Team Lead is a tech lead who breaks down a feature request into tickets, assigns them to developers, and reviews the output. The Teammates are the developers who do the actual work and can ask each other questions when their tasks overlap.

### How Communication Works

The messaging system is what separates Agent Teams from simply running multiple Claude instances in separate terminals. Here's how it flows:

1. **Team Lead → Teammates**: Task assignments with context and requirements
2. **Teammates → Team Lead**: Status updates, completed work, questions
3. **Teammate → Teammate**: Lateral communication — "I changed the API interface, here's the new signature" or "Which database table are you using for user preferences?"

This lateral communication is critical. When Teammate A modifies an API endpoint and Teammate B is building a frontend that consumes it, they can coordinate in real time rather than discovering conflicts after both are done.

## Agent Teams vs. Subagents: What's the Difference?

If you've used Claude Code's Subagent feature (introduced earlier in 2025), you might wonder: how are Agent Teams different?

The distinction is fundamental — it's the difference between delegation and collaboration.

| Feature | Subagents | Agent Teams |
|---------|-----------|-------------|
| **Communication** | One-way (parent → child → parent) | Multi-directional (any agent → any agent) |
| **Coordination** | Hierarchical — subagent reports back to parent | Lateral — teammates talk to each other |
| **Task visibility** | Parent sees results only | Shared task list visible to all |
| **Context sharing** | Subagent gets a scoped context window | Each teammate has full context + messaging |
| **Parallelism** | Sequential by default | Parallel by design |
| **Use case** | Isolated, well-defined subtasks | Complex tasks with interdependencies |
| **Token cost** | Lower (single subagent at a time) | Higher (multiple agents running simultaneously) |

**Subagents** are like sending an intern to research something and bring back the answer. They get a focused task, execute it, and return the result. The parent agent never loses control, and the subagent never needs to talk to anyone else.

**Agent Teams** are like assembling a project team. Each member works on their part, but they stay in communication. When the backend developer changes a data model, the frontend developer hears about it immediately instead of finding out when integration tests fail.

### When to Use Which

- **Use Subagents** when the task is cleanly decomposable — "search for all usages of this deprecated function" or "write unit tests for this module." No coordination needed.
- **Use Agent Teams** when tasks have dependencies and touch multiple parts of the system — "build this full feature across frontend, backend, and database" or "investigate this production bug from multiple angles."

For a deeper dive into Subagents, see our [Claude Code Skills Guide](/posts/ai/2026-02-28-claude-code-skills-guide/).

## Quick Start: Setting Up Agent Teams

Agent Teams is still an experimental feature as of February 2026. You need to explicitly enable it.

### Step 1: Enable Agent Teams

**Option A: Environment variable (quick)**

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

**Option B: Settings file (persistent)**

Add to your `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or add it to your project's `.claude/settings.json` for project-level configuration.

If you haven't installed Claude Code yet, follow our [Claude Code Setup Guide](/posts/ai/2026-02-25-claude-code-setup-guide/) first.

### Step 2: Create a Team with Natural Language

Once enabled, you create teams by simply describing what you want. No special syntax required:

```
> I need to add user authentication to this app. Set up a team:
  one agent handles the backend API routes,
  one builds the frontend login/signup forms,
  and one writes the integration tests.
```

Claude Code's Team Lead will:

1. Analyze your request
2. Create a task list with clear assignments
3. Spawn the appropriate number of Teammates
4. Begin parallel execution

You can also be more explicit:

```
> Create a 3-agent team:
  - Agent 1: Implement JWT auth in /src/api/auth.ts
  - Agent 2: Build React login component in /src/components/Login.tsx
  - Agent 3: Write Playwright E2E tests in /tests/auth.spec.ts
```

### Step 3: Choose a Display Mode

Agent Teams supports two display modes:

**In-Process Mode (default)**

Works in any terminal. All agents share the same terminal window, and you see output from one agent at a time. Use `Shift+Down` to cycle between teammates.

```bash
claude --teammate-mode in-process
```

**Split Pane Mode (tmux / iTerm2)**

If you're using tmux or iTerm2, each Teammate gets its own pane. You can watch all agents working simultaneously — it's impressive to see three agents coding in parallel across your screen.

```bash
claude --teammate-mode split-panes
```

> **Tip**: Split pane mode requires tmux or iTerm2. If you're using a basic terminal, stick with in-process mode.

### Step 4: Interact with the Team

While the team is working, you have several interaction options:

| Shortcut | Action |
|----------|--------|
| `Shift+Down` | Switch to next teammate's view |
| `Shift+Up` | Switch to previous teammate's view |
| `Ctrl+T` | View the shared task list |
| Type normally | Send a message to the currently visible agent |

You can redirect any agent at any time. If you notice Teammate 2 going down the wrong path, switch to it and say "Stop — use the existing auth middleware instead of creating a new one." The Team Lead can also be told to reassign tasks.

## Real-World Collaboration Patterns

Theory is nice. Let's look at how Agent Teams works in practice with patterns you can use today.

### Pattern 1: Frontend + Backend + Testing (3-Way Parallel)

This is the most natural pattern for feature development. Three agents work on different layers simultaneously.

**Prompt:**

```
Build a "Team Settings" page for our SaaS app.

Agent 1 (Backend): Create CRUD API endpoints for team settings
  at /api/teams/:id/settings. Use the existing Prisma schema
  and add any needed fields.

Agent 2 (Frontend): Build a React settings form component at
  /src/pages/TeamSettings.tsx using our existing UI component
  library in /src/components/ui/.

Agent 3 (Testing): Write comprehensive tests — unit tests for
  the API handlers, component tests for the form, and one E2E
  test for the full flow.
```

**How it plays out:**

1. Agent 1 starts implementing the API, defining request/response types
2. Agent 2 begins with the UI structure and layout
3. Agent 3 sets up test scaffolding
4. When Agent 1 defines the API contract, it messages Agent 2: "Settings endpoint accepts `{ teamName, billingEmail, notificationPrefs }` — here's the TypeScript interface"
5. Agent 2 updates its form to match the actual API shape
6. Agent 3 picks up the interface from both agents and writes tests against the real contracts

**Time savings:** What would take ~45 minutes sequentially (15 min per layer) often completes in ~18-20 minutes with three agents working in parallel. The overhead of coordination messaging adds some time, but you still get a roughly 2x speedup on well-structured tasks.

### Pattern 2: Multi-Hypothesis Debugging

This is where Agent Teams truly shines. When you have a complex production bug, you often don't know where to look. Instead of investigating one hypothesis at a time, spin up multiple agents to check different theories simultaneously.

**Prompt:**

```
Users are reporting intermittent 500 errors on the /api/checkout
endpoint. It's happening about 5% of the time, no clear pattern.

Create a team of 5 investigators:
1. Check the payment gateway integration for timeout/retry issues
2. Examine database connection pool — look for exhaustion or deadlocks
3. Review recent deployments for any changes to checkout flow
4. Analyze error logs and stack traces for patterns
5. Check for race conditions in the inventory reservation logic
```

**Why this works:** In traditional debugging, you'd try hypothesis 1, rule it out, try hypothesis 2, and so on. With five agents working in parallel, you get all five reports back roughly simultaneously. Often, one agent will find the root cause while others find contributing factors or latent bugs you didn't know about.

**Real outcome:** In a scenario like this, Agent 3 might discover that a recent deployment changed the timeout configuration, Agent 5 might find a genuine race condition that was masked by the old timeout, and Agent 2 might notice the connection pool is undersized for current traffic — all within the same investigation window.

### Pattern 3: Multi-Perspective Code Review

Instead of one agent reviewing your code, assign different review angles to different agents.

**Prompt:**

```
Review the PR in /tmp/pr-diff.patch from three perspectives:

Agent 1 (Security): Focus on authentication, authorization,
  input validation, SQL injection, XSS, secrets exposure.

Agent 2 (Performance): Analyze query efficiency, N+1 problems,
  unnecessary re-renders, memory leaks, caching opportunities.

Agent 3 (Test Coverage): Identify untested code paths, missing
  edge cases, suggest specific test scenarios.
```

Each agent brings a specialist lens. The security reviewer won't be distracted by performance concerns, and the performance reviewer can go deep on query plans without worrying about test coverage. You get three focused reviews instead of one surface-level review.

### Pattern 4: Migration and Refactoring

Large-scale migrations — TypeScript conversion, framework upgrades, API versioning — are ideal for Agent Teams because the work is parallelizable with clear boundaries.

**Prompt:**

```
Migrate our Express.js routes to the new Hono framework.

Agent 1: Migrate /src/routes/auth/* (4 files)
Agent 2: Migrate /src/routes/users/* (6 files)
Agent 3: Migrate /src/routes/billing/* (5 files)
Agent 4: Update all middleware in /src/middleware/ to Hono format
Agent 5: Update integration tests to work with Hono's test client
```

**Key principle:** Each agent works on a different directory or set of files. File isolation prevents merge conflicts and allows truly parallel work.

## Advanced Features

### Require Plan Approval Before Implementation

By default, the Team Lead creates a task plan and immediately begins execution. If you want to review and approve the plan first:

```
Create a team to refactor our database layer.
IMPORTANT: Show me the task breakdown and wait for my approval
before any agent starts working.
```

The Team Lead will present the task list and wait for your go-ahead. This is essential for large or sensitive changes where you want to verify the approach before multiple agents start modifying files.

### Use Hooks for Quality Gates

Claude Code [Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) integrate with Agent Teams through two team-specific events:

- **`TeammateIdle`**: Fires when a teammate finishes all assigned tasks
- **`TaskCompleted`**: Fires when any individual task is marked complete

You can use these to enforce quality gates:

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "command": "npm run lint -- --quiet",
        "description": "Run linter after each task completes"
      }
    ],
    "TeammateIdle": [
      {
        "command": "npm test -- --bail",
        "description": "Run test suite when a teammate finishes"
      }
    ]
  }
}
```

This ensures each agent's work passes basic quality checks before it's considered done. If the lint or test fails, the agent can fix the issue before moving on.

### Specify Models Per Teammate

Not every task needs the most powerful (and most expensive) model. You can assign different models to different teammates:

```
Create a team for this feature:
- Agent 1 (use Opus): Architect the database schema and API design
- Agent 2 (use Sonnet): Implement the CRUD endpoints following Agent 1's design
- Agent 3 (use Sonnet): Write boilerplate test files
```

Opus handles the tasks that require deep reasoning and architectural decisions. Sonnet handles the more mechanical implementation work. This can reduce your token costs by 40-60% on teams where only one or two tasks need top-tier reasoning.

### Worktree Integration

Agent Teams can work alongside Claude Code's [Worktree](/posts/ai/2026-02-28-claude-code-worktree-guide/) feature. Each teammate can operate in its own git worktree, giving it a fully isolated file system:

```
Create a team with worktree isolation:
- Each agent gets its own git worktree
- Agent 1: feature/auth-backend
- Agent 2: feature/auth-frontend
- Agent 3: feature/auth-tests
```

This eliminates any possibility of file conflicts. Each agent commits to its own branch, and you merge them together when all work is complete. This is the safest approach for large, multi-file changes.

## Best Practices

### When to Use Agent Teams

**Good fit:**
- Feature development spanning 3+ files across different layers
- Bug investigation with multiple possible causes
- Code review from multiple specialized angles
- Large migrations or refactors with parallelizable chunks
- Prototyping multiple approaches simultaneously

**Poor fit:**
- Simple, single-file changes (just use one agent)
- Tasks that are fundamentally sequential ("do A, then based on A's result, do B")
- Very small codebases where multiple agents would trip over each other
- When you're on a tight token budget

### Task Splitting Principles

The quality of your Agent Team's output depends heavily on how you split tasks. Follow these principles:

1. **Moderate granularity**: Each task should take 5-15 minutes for a single agent. Too small and the coordination overhead dominates. Too large and you lose the parallelism benefit.

2. **File isolation**: Assign different files or directories to different agents whenever possible. Two agents editing the same file creates conflicts and confusion.

3. **Clear deliverables**: Each task should have a concrete output — "create the API route that returns JSON" is better than "work on the backend."

4. **Define interfaces first**: When agents need to interact (frontend calling backend), have the Team Lead or one agent define the interface/contract first, then distribute implementation.

5. **5-6 tasks per teammate**: This is the sweet spot. Fewer than 3 tasks and you're not leveraging the agent fully. More than 8 and the agent loses focus and context quality degrades.

### Communication Hygiene

- **Be explicit about shared resources**: If two agents need the same config file, tell both of them and specify who "owns" it.
- **Name your agents by role**: "Backend Agent" and "Frontend Agent" are easier to direct than "Agent 1" and "Agent 2."
- **Check the task list regularly**: Use `Ctrl+T` to monitor progress. If an agent is stuck or heading in the wrong direction, intervene early.

## Token Cost Considerations

Let's be direct: Agent Teams costs significantly more than a single-agent session.

### The Math

A typical Agent Team session with 3 teammates costs approximately **3-4x** what a single-agent session would cost for the same total work. Here's why:

- Each teammate has its own context window, so code that's shared across agents gets loaded multiple times
- Coordination messages between agents add token overhead
- The Team Lead maintains a meta-view of all tasks, which consumes tokens for tracking state

**Example breakdown for a medium feature (3 agents, ~30 min):**

| Component | Tokens | Est. Cost (API) |
|-----------|--------|-----------------|
| Team Lead context + coordination | ~50K | ~$1.50 |
| Teammate 1 (Backend) | ~80K | ~$2.40 |
| Teammate 2 (Frontend) | ~70K | ~$2.10 |
| Teammate 3 (Tests) | ~60K | ~$1.80 |
| Inter-agent messages | ~20K | ~$0.60 |
| **Total** | **~280K** | **~$8.40** |

A single agent doing the same work might use ~120K tokens (~$3.60). So the team approach costs about 2.3x more in this case — but finishes in 18 minutes instead of 40.

### Cost Optimization Strategies

1. **Use Sonnet for mechanical tasks**: Assign Opus only to design and architecture tasks. Sonnet is ~5x cheaper per token (see [Claude model pricing](https://docs.anthropic.com/en/docs/about-claude/models)) and handles straightforward implementation well.

2. **Don't use teams for simple tasks**: If a single agent can handle it in under 10 minutes, the coordination overhead isn't worth it.

3. **Limit team size**: 3 agents is the sweet spot for most tasks. Going beyond 5 agents rarely improves speed and significantly increases cost due to coordination overhead.

4. **Reuse context**: If multiple agents need to understand the same codebase, consider having the Team Lead provide a summary context rather than having each agent independently read the same files.

5. **Max plan users**: If you're on the Max 20x plan ($200/month), Agent Teams is included in your usage limits. The per-session cost matters less when you're on a flat-rate plan. See our [Claude Code Pricing guide](/posts/ai/2026-02-25-claude-code-pricing/) for plan comparisons.

## Comparison Table: Agent Teams vs. Subagent vs. Worktree

| Feature | Agent Teams | Subagent | Worktree |
|---------|-------------|----------|----------|
| **Communication** | Multi-directional messaging | One-way (parent ↔ child) | None (isolated sessions) |
| **Coordination** | Shared task list + mailbox | Parent orchestrates | Manual (you coordinate) |
| **Parallelism** | Built-in parallel execution | Sequential by default | Manual parallel (separate terminals) |
| **File safety** | Shared filesystem (risk of conflicts) | Shared filesystem | Isolated git worktrees |
| **Context sharing** | Via messaging system | Scoped context from parent | No sharing |
| **Token cost** | 3-4x single session | 1.3-1.5x single session | 1x per session (but multiple sessions) |
| **Best for** | Complex, interdependent tasks | Simple, isolated subtasks | Large parallel changes needing git isolation |
| **Setup complexity** | Low (natural language) | Automatic (Claude decides) | Medium (worktree management) |
| **Nesting** | No (teammates cannot create sub-teams) | Yes (subagents can spawn subagents) | No |

**Choose Agent Teams** when your task has interdependencies and agents need to communicate during execution.

**Choose Subagents** when each subtask is self-contained and doesn't need to know about other subtasks.

**Choose Worktrees** when you need full git isolation — each piece of work on its own branch with no possibility of file conflicts. Read our [Worktree Guide](/posts/ai/2026-02-28-claude-code-worktree-guide/) for details.

## Command Reference

### Enabling Agent Teams

```bash
# Environment variable (session-only)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Settings file (persistent) — add to ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### Display Mode

```bash
# Force in-process mode (default, works in any terminal)
claude --teammate-mode in-process

# Force split pane mode (requires tmux or iTerm2)
claude --teammate-mode split-panes
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Down` | Switch to next teammate |
| `Shift+Up` | Switch to previous teammate |
| `Ctrl+T` | View / edit shared task list |
| `Ctrl+C` | Interrupt current agent (doesn't kill others) |

### Useful Prompts

```bash
# Check team status
"Show me the current task list and each agent's status"

# Redirect a specific agent
"Tell the backend agent to use the existing auth middleware"

# Add a new task
"Add a task: write database migration for the new settings table"

# Reassign work
"Move the caching task from Agent 2 to Agent 3"
```

## Frequently Asked Questions

### Does Agent Teams work in VS Code?

Yes. If you use the Claude Code extension for VS Code, Agent Teams works in the integrated terminal. The in-process display mode works out of the box. For split pane mode, you'll need to use VS Code's built-in terminal splitting or run Claude Code in an external tmux session.

### Can Teammates create their own sub-teams?

No. Nesting is not supported. A Teammate cannot spawn additional teams or sub-teams. This is by design — nested teams would create exponential token costs and coordination complexity. If a Teammate needs help with a subtask, it can use the standard Subagent feature instead.

### How do I troubleshoot a stuck teammate?

If a teammate seems stuck:

1. Switch to it with `Shift+Down/Up`
2. Check what it's doing — it might be waiting for user confirmation
3. Send it a message: "What's your current status? Are you blocked on anything?"
4. If truly stuck, you can tell the Team Lead: "Reassign Agent 3's remaining tasks to Agent 2"

### Is Agent Teams stable enough for production work?

As of February 2026, Agent Teams is still marked as experimental. It works reliably for most use cases, but you may encounter:

- Occasional coordination delays between agents
- Rare cases where two agents try to edit the same file simultaneously
- Display glitches in split pane mode with some terminal emulators

For critical production work, consider using Worktree mode alongside Agent Teams for file isolation. For everyday development tasks, it's stable enough to be genuinely useful.

### How do I justify the higher token cost?

The cost-benefit equation depends on your time value:

- **A 3-agent team costs ~2.5x more** in tokens but **finishes ~2x faster**
- If you bill at $100+/hour, the extra $5-10 per session pays for itself in saved time
- The real value is in **parallel investigation** — debugging 5 hypotheses at once instead of sequentially
- For Max plan users on flat-rate pricing, the token cost is already included

### Can I mix Agent Teams with other Claude Code features?

Absolutely. Agent Teams works with:

- **[Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/)**: Quality gates on task completion
- **[Skills](/posts/ai/2026-02-28-claude-code-skills-guide/)**: Each teammate can use slash commands and custom skills
- **[Worktrees](/posts/ai/2026-02-28-claude-code-worktree-guide/)**: Git isolation per teammate
- **[MCP Servers](/posts/ai/2026-02-28-claude-code-mcp-setup/)**: Each teammate can access configured MCP tools
- **CLAUDE.md**: All teammates inherit project instructions from your [CLAUDE.md configuration](/posts/ai/2026-02-28-claude-code-claudemd-guide/)

## Getting Started Today

Agent Teams changes how you think about AI-assisted development. Instead of asking "how do I get one agent to do this faster?", you start asking "how do I decompose this so multiple agents can work on it in parallel?"

Here's a practical starting point:

1. **Enable the feature** with the environment variable or settings file
2. **Start small** — try a 2-agent team on your next feature (one builds, one tests)
3. **Graduate to 3 agents** for frontend + backend + testing patterns
4. **Use multi-hypothesis debugging** for your next tricky bug
5. **Monitor token costs** for the first week to understand your usage patterns

The future of AI coding isn't a single, all-powerful agent. It's coordinated teams of specialized agents, each focused on what they do best, communicating and collaborating like human engineers — just faster.

## Related Reading

- [Claude Code Setup Guide 2026](/posts/ai/2026-02-25-claude-code-setup-guide/) — Get started with installation and configuration
- [Claude Code Pricing 2026](/posts/ai/2026-02-25-claude-code-pricing/) — Pick the right plan for your usage
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Automate your workflow with lifecycle hooks
- [Claude Code Worktree Guide](/posts/ai/2026-02-28-claude-code-worktree-guide/) — Run parallel AI tasks with Git worktree isolation
- [Claude Code Skills Guide](/posts/ai/2026-02-28-claude-code-skills-guide/) — Build reusable slash commands and workflows
- [CLAUDE.md Guide](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — Give AI perfect project context every session
