+++
date = '2026-03-13T15:00:00+08:00'
draft = false
title = 'GitHub Agent HQ: Multi-Agent Development Guide for VS Code'
description = 'Set up GitHub Agent HQ to run Claude, Codex, and Copilot in VS Code. Covers setup, multi-agent workflows, practical use cases, and comparisons with CLI tools.'
toc = true
tags = ['GitHub Copilot', 'AI Coding Tools', 'VS Code', 'Claude', 'Multi-Agent']
keywords = ['GitHub Agent HQ', 'multi-agent VS Code', 'Claude Codex Copilot VS Code', 'Agent HQ setup guide', 'VS Code multi-agent development']
+++

![GitHub Agent HQ multi-agent development dashboard showing Claude, Codex, and Copilot panels in VS Code](cover.webp)

Running one AI coding agent is productive. Running three at the same time — comparing their approaches, playing to each one's strengths, and picking the best output — changes how you build software entirely.

GitHub Agent HQ makes this possible without leaving VS Code. Announced at GitHub Universe 2025 and launched in public preview in February 2026, Agent HQ lets you run [Anthropic Claude](https://www.anthropic.com/), [OpenAI Codex](https://openai.com/index/codex/), and [GitHub Copilot](https://github.com/features/copilot) from a single interface. Think of it as a mission control for AI agents: you assign tasks, monitor progress, compare results, and merge the best solution — all without switching tools.

This guide walks you through setting up Agent HQ, building effective multi-agent workflows, and understanding when this approach beats alternatives like Claude Code CLI or Cursor.

## What Is GitHub Agent HQ?

Agent HQ is GitHub's platform for orchestrating multiple AI coding agents across GitHub, VS Code, and GitHub Mobile. Instead of being locked into a single AI assistant, you get access to a fleet of agents that you can assign to tasks independently or in parallel.

The core idea: **different agents have different strengths**, and the best results come from leveraging those differences rather than relying on one model for everything.

### What You Get

| Feature | Description |
|---------|-------------|
| **Multi-agent access** | Run Claude, Codex, and Copilot from one interface |
| **Session management** | Monitor and manage multiple concurrent agent sessions |
| **Agent comparison** | Assign the same task to multiple agents and compare outputs |
| **Local + cloud modes** | Interactive local agents or autonomous cloud agents |
| **Unified governance** | Enterprise-grade access controls, audit logs, and metrics |
| **Native GitHub integration** | Agent outputs appear as PRs, comments, and issue updates |

### Supported Agents (March 2026)

- **GitHub Copilot** — GitHub's native agent, deeply integrated with the platform
- **Claude** (Anthropic) — strong at multi-file refactoring, architectural reasoning, and nuanced code review
- **Codex** (OpenAI) — excels at code generation, algorithm implementation, and rapid prototyping

Additional agents from Google, Cognition, and xAI are planned for future releases.

## Prerequisites and Subscription Requirements

Before you start, make sure you have:

1. **VS Code v1.109 or later** — the January 2026 release added multi-agent support
2. **A qualifying GitHub subscription**:
   - **Copilot Pro+** — full access to all three agents
   - **Copilot Enterprise** — full access with additional governance features
   - Copilot Individual and Business tiers do not yet include Claude and Codex access (planned for later in 2026)
3. **GitHub Copilot extension** installed in VS Code

Each agent session consumes one premium request from your subscription quota.

## Setting Up Agent HQ in VS Code

### Step 1: Update VS Code

Make sure you are on version 1.109 or newer:

```
Help → About → Version 1.109+
```

If you are behind, download the latest version from [code.visualstudio.com](https://code.visualstudio.com/).

### Step 2: Install Required Extensions

Open the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`) and install:

- **GitHub Copilot** (required for all agents)
- **GitHub Copilot Chat** (required for chat-based interactions)

For Codex support, also install the **OpenAI Codex** extension when prompted.

### Step 3: Enable Agent Support

Open VS Code settings (`Ctrl+,` / `Cmd+,`) and configure:

```json
{
  "chat.agent.enabled": true,
  "github.copilot.chat.claudeAgent.enabled": true
}
```

> **Note:** In enterprise environments, `chat.agent.enabled` may be managed at the organization level. Contact your administrator if the setting is locked.

### Step 4: Verify Your Setup

Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and search for **"Agent Sessions"**. If you see the Agent Sessions view, you are ready to go.

## Understanding Agent Types

Agent HQ supports three execution modes, and picking the right one matters more than picking the right model:

### Local Agents

Run directly on your machine with full workspace access. Best for:
- Exploratory coding where you need to steer the agent in real time
- Tasks requiring immediate feedback loops
- Debugging sessions where context changes rapidly

**How to start:** Open Chat view → click the `+` dropdown → select agent type (Copilot, Claude, or Codex) → choose "Local"

### Cloud Agents

Run on remote infrastructure and integrate with GitHub pull requests. Best for:
- Well-defined tasks you can describe upfront and walk away from
- Work that benefits from team visibility (results appear as PRs)
- Tasks that take a long time to complete

**How to start:** Same dropdown → select agent → choose "Cloud"

### Background Agents (Copilot CLI)

Run autonomously in the background using Git worktrees. Best for:
- Isolated changes that should not interfere with your current work
- Batch tasks like updating dependencies or fixing lint errors across many files
- Tasks you want to delegate while continuing other work

**How to start:** Use the `/delegate` command in a Copilot CLI session

| Agent Mode | Location | Interaction | Best For |
|-----------|----------|-------------|----------|
| Local | Your machine | Interactive, real-time | Exploratory tasks, debugging |
| Cloud | Remote infra | Async, autonomous | Well-defined tasks, team visibility |
| Background | Your machine (CLI) | Async, unattended | Isolated changes, batch work |

## Multi-Agent Workflows That Actually Work

The real power of Agent HQ is not just having three agents — it is knowing when and how to use each one. Here are workflows I have found effective:

### Workflow 1: Competitive Draft

Assign the same task to all three agents and compare their approaches.

**When to use:** Architectural decisions, complex refactoring, or any task where there is more than one reasonable solution.

**How it works:**

1. Open three agent sessions (one for each agent)
2. Give each the same prompt — for example, "Refactor the authentication module to support OAuth2 and API key authentication"
3. Let all three work in parallel
4. Compare the outputs: look at code structure, error handling approaches, and test coverage
5. Cherry-pick the best elements from each solution

This is especially valuable because Claude tends to produce well-structured, thoroughly documented solutions, Codex often generates more concise implementations, and Copilot leverages deep GitHub context about your specific codebase.

### Workflow 2: Specialist Pipeline

Use different agents for different stages of a task based on their strengths.

**Example pipeline:**

```
Claude (Planning)  →  Codex (Implementation)  →  Copilot (Integration)
```

1. **Claude** — "Design a caching layer for our API. Consider Redis vs in-memory options, define the interface, and outline edge cases." Claude excels at this kind of architectural reasoning.
2. **Codex** — "Implement the caching layer based on this design: [paste Claude's output]." Codex is fast at turning specs into code.
3. **Copilot** — "Integrate this caching module into the existing API handlers and update the tests." Copilot has the deepest context about your repository structure.

### Workflow 3: Review and Challenge

Use one agent to review another's output.

```
Agent A (writes code)  →  Agent B (reviews and critiques)
```

This catches blind spots that a single agent would miss. For example:

1. Have Codex generate a database migration
2. Ask Claude to review it for edge cases, data integrity risks, and rollback safety
3. Apply the fixes and improvements from Claude's review

### Workflow 4: Parallel Research + Implementation

Use subagents for research while the primary agent builds.

1. Start a local Claude session for your main implementation task
2. Spin up a Copilot subagent to scan your codebase for existing patterns and conventions
3. Spin up a Codex subagent to research the library documentation
4. Feed the research results back into Claude's context

VS Code's subagent feature keeps each agent's context isolated, so parallel execution does not create noise in your primary session.

## Agent HQ vs Claude Code CLI vs Cursor vs Copilot Standalone

If you are already using one of these tools, you might wonder whether Agent HQ adds value or just adds complexity. Here is an honest comparison:

### Agent HQ vs Claude Code CLI

[Claude Code CLI](/posts/ai/2026-01-14-claude-code-guide/) is Anthropic's terminal-based coding agent — no IDE required.

| Dimension | Agent HQ (Claude in VS Code) | Claude Code CLI |
|-----------|------------------------------|-----------------|
| **Interface** | VS Code GUI, visual diffs | Terminal, text-based |
| **Multi-agent** | Run Claude + Codex + Copilot | Claude only |
| **Workflow** | Click-driven, session panels | Command-driven, scriptable |
| **Context** | VS Code workspace context | Full filesystem + shell access |
| **Hooks & automation** | Limited | Extensive (pre/post hooks, [worktrees](/posts/ai/2026-02-20-claude-code-worktree/)) |
| **Best for** | Teams, visual workflows, agent comparison | Power users, automation, CI/CD integration |

**Verdict:** If you want multi-agent comparison and visual session management, Agent HQ wins. If you want maximum control, scriptability, and [deep automation](/posts/ai/2026-02-18-claude-code-hooks-guide/), Claude Code CLI is still superior.

### Agent HQ vs Cursor

[Cursor](/posts/ai/2026-03-08-cursor-setup-guide/) is an AI-native IDE fork of VS Code with its own agent mode.

| Dimension | Agent HQ | Cursor |
|-----------|----------|--------|
| **Agent choice** | Claude, Codex, Copilot | Multiple models but single-agent workflow |
| **IDE** | Standard VS Code | Forked VS Code (separate app) |
| **Extensions** | Full VS Code marketplace | Most VS Code extensions work |
| **Multi-agent** | Native, first-class | Not supported |
| **Pricing** | Copilot Pro+ ($39/mo) | Cursor Pro ($20/mo) + API costs |

**Verdict:** If multi-agent workflows matter to you, Agent HQ has no equivalent in Cursor. If you prefer a tightly integrated single-agent experience with excellent inline completions, [Cursor remains strong](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/).

### Agent HQ vs Copilot Standalone

Agent HQ is essentially Copilot upgraded. Everything Copilot did before still works — you just gain access to Claude and Codex alongside it. There is no reason to avoid the upgrade if you have a qualifying subscription.

For a detailed comparison of these tools, see our [AI Coding Agents 2026 comparison](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/).

## Practical Tips and Best Practices

### 1. Start with One Agent, Scale to Three

Do not try to run three agents on every task from day one. Start by learning each agent's personality:

- **Copilot** — fast autocomplete, good at repo-specific patterns, best inline experience
- **Claude** — thorough, good at explaining trade-offs, strong at multi-file changes
- **Codex** — fast generation, good at algorithmic tasks, concise output

Once you know their strengths, you will naturally see where multi-agent workflows add value.

### 2. Write Better Prompts for Multi-Agent Tasks

When comparing agents, give them identical, specific prompts. Vague prompts produce vague differences. Instead of:

```
# Too vague — agents will diverge for random reasons
"Improve the error handling"
```

Be specific:

```
# Specific — differences will reveal genuine approach variations
"Refactor error handling in src/api/handlers.ts to:
1. Replace generic try/catch with typed error classes
2. Add retry logic for transient network failures
3. Return structured error responses matching our ErrorResponse type
4. Add unit tests for each error path"
```

### 3. Use Cloud Agents for Overnight Work

Assign well-defined tasks to cloud agents before you leave for the day. The results appear as draft PRs, ready for your review in the morning. This works best for:

- Dependency updates with test verification
- Migration scripts
- Documentation generation
- Test coverage expansion

### 4. Monitor Session Costs

Each agent session consumes a premium request. Running three agents on every trivial task will burn through your quota quickly. Reserve multi-agent workflows for decisions that genuinely benefit from multiple perspectives.

### 5. Never Blindly Accept Agent Output

GitHub's own announcement makes this explicit: *"Agents can still make mistakes. That's exactly why their output is designed to be reviewed, compared, and challenged, not blindly accepted."*

Agent HQ's review-based workflow (draft PRs, inline comments) is designed around this principle. Use it. Every agent-generated change should go through the same code review process as human-written code.

## Enterprise Governance Features

For teams and organizations, Agent HQ includes governance tools that address the biggest concern with AI coding tools — control:

- **Access controls** — administrators define which agents and models teams can use
- **Audit logging** — full activity tracking for compliance and accountability
- **Code Quality integration** — automated security and maintainability checks on agent output (public preview)
- **Usage metrics dashboard** — track adoption and impact across the organization
- **Policy enforcement** — set rules for which tasks agents can perform autonomously vs. requiring human approval

This governance layer is a significant differentiator. Tools like Claude Code CLI and Cursor leave access control to individual developers. Agent HQ centralizes it, which matters at scale.

## Current Limitations

Agent HQ is still in public preview, and there are rough edges worth knowing about:

1. **Subscription gate** — Claude and Codex require Copilot Pro+ ($39/month) or Enterprise. This prices out many individual developers
2. **Session quota** — each agent session costs a premium request, making three-agent workflows expensive for frequent use
3. **No cross-session context** — sessions are independent with no shared memory, so you manually transfer context between agents
4. **Cloud agent latency** — cloud sessions can take minutes to start, which breaks flow for quick questions
5. **Limited agent customization** — you cannot fine-tune agent behavior beyond prompt engineering (unlike [Claude Code's CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) or [custom skills](/posts/ai/2026-02-28-claude-code-skills-guide/))

## FAQ

**Q: Do I need all three agents for Agent HQ to be useful?**

No. Even using two agents — say, Copilot for autocomplete and Claude for complex refactoring — provides clear value. The three-agent comparison workflow is a power feature, not a requirement.

**Q: Can I use Agent HQ with Copilot Free or Copilot Individual?**

Currently, Claude and Codex access requires Copilot Pro+ or Enterprise. Copilot agent mode is available on lower tiers, but without the multi-agent capability.

**Q: Does Agent HQ replace the need for Claude Code CLI?**

Not entirely. Claude Code CLI offers deeper terminal integration, [hook-based automation](/posts/ai/2026-02-18-claude-code-hooks-guide/), and [worktree workflows](/posts/ai/2026-02-28-claude-code-worktree-guide/) that Agent HQ does not replicate. They serve different workflows — Agent HQ for visual multi-agent work, CLI for automation and scripting.

**Q: How does Agent HQ handle code privacy?**

Agent outputs are processed through GitHub's infrastructure with the same privacy guarantees as Copilot. Enterprise customers get additional data residency and retention controls. Check [GitHub's Copilot privacy documentation](https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-policies-and-features-for-copilot-in-your-organization) for details.

**Q: Is Agent HQ available on github.com, or only in VS Code?**

Both. You can start agent sessions from github.com (Agents tab in repositories), GitHub Mobile, and VS Code. Cloud agent results sync across all platforms.

## Related Reading

- [AI Coding Agents 2026: The Complete Comparison (7 Tools Tested)](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/) — how Agent HQ's agents compare individually
- [Claude Code vs GitHub Copilot 2026: I Use Both — Here Is When Each Wins](/posts/ai/2026-03-05-claude-code-vs-copilot/) — detailed Copilot vs Claude comparison
- [Claude Code vs Codex CLI: 8-Dimension Head-to-Head Comparison](/posts/ai/2026-02-19-claude-code-vs-codex/) — Claude vs Codex deep dive
- [Claude Code vs Cursor vs Windsurf 2026: Speed, Cost & Control](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/) — broader AI IDE comparison
- [GitHub Copilot vs Claude Code vs Cursor: 2026 Comparison](/posts/ai/2026-02-28-copilot-vs-claude-vs-cursor/) — three-way tool comparison
