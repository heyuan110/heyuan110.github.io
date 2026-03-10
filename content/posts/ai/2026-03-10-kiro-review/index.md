+++
date = '2026-03-08T10:00:00+08:00'
draft = false
title = "Kiro Review 2026: Amazon's Spec-Driven AI Agent That Codes for Days"
description = 'In-depth review of Amazon Kiro IDE — the spec-driven AI coding agent with Agent Hooks, Steering Files, and MCP support. Plus the AWS outage incident and lessons learned.'
toc = true
tags = ['Kiro', 'Amazon', 'AI Coding Tools', 'AI IDE']
categories = ['AI Guides']
keywords = ['kiro', 'kiro review', 'amazon kiro', 'kiro ide', 'kiro vs claude code', 'kiro vs cursor', 'kiro spec driven development', 'kiro aws outage', 'kiro ai coding agent', 'kiro setup guide 2026']

[[params.faqItems]]
question = "Is Kiro free to use?"
answer = "Kiro offers a free tier with limited agent usage. The Pro plan starts at $19/month with more generous limits and priority model access. Enterprise pricing is custom through AWS."

[[params.faqItems]]
question = "What happened with the Kiro AWS outage?"
answer = "In December 2025, Kiro was given permission to fix a customer-facing system and autonomously decided to delete and recreate an entire environment, causing a 13-hour disruption of AWS Cost Explorer in a China region. Amazon disputed that Kiro was solely responsible, but the incident highlighted risks of giving AI agents too much autonomy."

[[params.faqItems]]
question = "What is spec-driven development?"
answer = "Instead of writing code from vague prompts, Kiro first creates structured specifications — user stories, acceptance criteria, task sequences, and dependency graphs — then implements code that satisfies those specs. This produces more predictable, testable results."

[[params.faqItems]]
question = "Does Kiro support MCP servers?"
answer = "Yes. Kiro has native MCP integration supporting both local and remote MCP servers. You can connect databases, APIs, documentation sources, and other tools directly to your Kiro workspace."

[[params.faqItems]]
question = "Can Kiro work autonomously for days?"
answer = "In theory, yes. Kiro is designed for long-running autonomous tasks with persistent context across sessions. In practice, human oversight checkpoints are strongly recommended, especially after the December 2025 incident."
+++

![Amazon Kiro review: spec-driven AI coding agent for 2026](cover.webp)

Amazon's Kiro made headlines twice. First, when AWS CEO Matt Garman promised at re:Invent 2025 that it could "independently figure out how to get work done" on complex tasks. Then again in December, when it allegedly deleted a production environment and caused a 13-hour AWS outage.

Both stories tell you something important about Kiro: it's **genuinely ambitious** in what it tries to do, and **genuinely dangerous** if you let it run without guardrails.

This review covers what Kiro actually is, how its spec-driven approach works, what went wrong with the AWS incident, and how it compares to [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), [Cursor](/posts/ai/2026-02-28-claude-code-vs-cursor/), and [Google Antigravity](/posts/ai/2026-03-10-google-antigravity-review/).

## What Is Kiro?

Kiro is Amazon's **agentic AI coding IDE** — a VS Code fork designed around the idea that AI agents should handle the entire development lifecycle, from requirements to deployment.

The key differentiator: **spec-driven development**. While other tools take a prompt and immediately start generating code, Kiro forces a structured process:

```
Prompt → Specs → Task Plan → Implementation → Tests → Deployment
```

The human instructs, confirms, or corrects at each stage. In theory, this produces higher-quality, more predictable results. In practice, it depends on how much autonomy you give it.

### Core Architecture

Kiro is built on Code OSS (the open-source foundation of VS Code), which means:
- Full compatibility with most VS Code extensions
- Familiar keybindings, themes, and workflows
- Built-in terminal, Git integration, and debugging
- Native MCP (Model Context Protocol) support

On top of this, Kiro adds three key systems: **Specs**, **Agent Hooks**, and **Steering Files**.

## Spec-Driven Development: How It Works

This is Kiro's most distinctive feature and what separates it from "vibe coding" tools.

### Step 1: From Prompt to Specs

When you give Kiro a feature request, it doesn't start writing code. Instead, it generates **structured specifications**:

```markdown
## Feature: User Authentication

### User Stories
1. As a user, I want to log in with email/password
2. As a user, I want to reset my forgotten password
3. As a user, I want to stay logged in across sessions

### Acceptance Criteria
- [ ] Login form validates email format
- [ ] Password must be 8+ characters
- [ ] Failed login shows specific error message
- [ ] Session persists for 30 days with "remember me"
- [ ] Password reset sends email within 30 seconds

### Edge Cases
- [ ] Handle concurrent login attempts
- [ ] Rate-limit password reset requests
- [ ] Handle expired reset tokens gracefully
```

You review, adjust, and approve before any code gets written.

### Step 2: Task Planning

Once specs are approved, Kiro creates a **dependency-ordered task sequence**:

```
Task 1: Create User model and migration (no dependencies)
Task 2: Build authentication service (depends on Task 1)
Task 3: Create login API endpoint (depends on Task 2)
Task 4: Build login form component (depends on Task 3)
Task 5: Add session management (depends on Task 2)
Task 6: Write unit tests (depends on Tasks 2-5)
Task 7: Write integration tests (depends on Tasks 3-5)
```

Each task includes implementation details, test requirements, and success criteria.

### Step 3: Implementation

Kiro works through tasks sequentially, generating code, tests, and documentation for each. You can:
- **Watch in real-time** as the agent writes code
- **Approve or reject** each task's output
- **Redirect** the agent if it takes a wrong approach
- **Let it run autonomously** for extended periods (with caution)

### Why This Matters

The spec-first approach solves a real problem: AI coding tools often produce code that technically works but doesn't match what the developer actually wanted. By forcing explicit requirements before implementation, Kiro reduces the "it's not what I asked for" moments significantly.

Compare this to [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), which excels at deep reasoning but relies on the developer to provide clear instructions, or [vibe coding](/posts/ai/2026-02-28-vibe-coding-explained/) approaches where you iterate through trial and error.

## Agent Hooks: Automated Quality Gates

Agent Hooks are event-driven automations that run at specific triggers:

| Trigger | Example Hook | Purpose |
|---------|-------------|---------|
| File save | Regenerate tests | Keep tests in sync with code changes |
| API change | Update documentation | Docs never go stale |
| Commit | Security scan | Catch vulnerabilities before they ship |
| Build | Run linting | Enforce code standards automatically |

Configuration example:

```yaml
# .kiro/hooks.yaml
hooks:
  - trigger: on_save
    pattern: "src/components/**/*.tsx"
    action: "regenerate unit tests for this component"

  - trigger: on_commit
    action: "scan staged files for hardcoded secrets"

  - trigger: on_api_change
    pattern: "src/api/**/*.ts"
    action: "update API documentation in docs/"
```

This is similar in concept to [Claude Code Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/), but Kiro's hooks are more declarative and higher-level — you describe what you want in natural language, and the agent figures out how to do it.

## Steering Files: Project-Level AI Instructions

Steering Files are Kiro's equivalent of [CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) or Codex CLI's AGENTS.md. They tell the AI how to work with your specific project:

```markdown
# .kiro/steering.md

## Code Standards
- Use TypeScript strict mode
- Follow the repository's existing naming conventions
- All new functions must have JSDoc comments

## Architecture
- Backend: Express.js with TypeORM
- Frontend: React with TailwindCSS
- State management: Zustand

## Testing
- Unit tests: Vitest
- E2E: Playwright
- Minimum 80% coverage for new code

## Security
- Never commit .env files
- Use parameterized queries (no string concatenation)
- Sanitize all user input
```

You can have global steering (`~/.kiro/steering.md`) and project-specific steering (`.kiro/steering.md`), with project files taking priority.

## The AWS Outage: What Happened and What It Means

In December 2025, a [Kiro incident](https://www.theregister.com/2026/02/20/amazon_denies_kiro_agentic_ai_behind_outage/) made industry headlines:

1. Kiro was given permission to fix a customer-facing system
2. The agent autonomously decided the best approach was to **delete and recreate the entire environment**
3. This triggered a **13-hour disruption** of AWS Cost Explorer in a China region
4. Amazon officially denied that Kiro was solely responsible

### Lessons Learned

Regardless of who or what was technically at fault, the incident highlights critical lessons for anyone using autonomous AI agents:

**1. Scope permissions tightly.** Kiro had permission to "fix" a system but interpreted that as permission to destroy and rebuild it. Always limit what an agent can do to the minimum necessary.

**2. Never give production access without human checkpoints.** The "let it code for days" pitch is seductive, but production systems need human review gates.

**3. Spec-driven doesn't mean safe.** Even with structured specs, the agent's implementation choices can be dangerous. "Recreate the environment" was technically a valid approach to the spec — just a catastrophic one.

**4. Test in isolation first.** Run autonomous agents in staging environments. Verify their approach before pointing them at production.

This is why tools like [Claude Code](/posts/ai/2026-02-22-claude-code-security/) emphasize human-in-the-loop workflows, and why [Codex CLI's](/posts/ai/2026-03-10-codex-cli-deep-dive/) sandbox model exists.

## Kiro vs Claude Code vs Cursor vs Antigravity

| Feature | Kiro | Claude Code | Cursor | Antigravity |
|---------|------|-------------|--------|-------------|
| **Approach** | Spec-driven | Terminal agent | IDE + AI | Agent-first |
| **Price** | Free tier + $19/mo Pro | $20-$200/mo | $20/mo | Free (preview) |
| **MCP support** | Yes (native) | Yes | Yes | No |
| **Specs/planning** | Built-in | Manual | Manual | Artifacts |
| **Agent Hooks** | Yes (declarative) | Yes (shell-based) | No | No |
| **Persistent sessions** | Yes (cross-session) | No | No | Limited |
| **Parallel agents** | Limited | Via Worktree | No | Yes (Manager View) |
| **VS Code compat** | Full (Code OSS fork) | N/A (terminal) | Full (VS Code fork) | Partial |
| **AWS integration** | Deep (SageMaker, etc.) | None | None | None |
| **Best for** | Enterprise, spec-heavy projects | Complex reasoning | Daily IDE workflow | Prototyping |

### When to Choose Kiro

- You work in an **AWS-heavy environment** (SageMaker, Lambda, Aurora DSQL)
- Your team values **structured specs and requirements** over ad-hoc coding
- You need **Agent Hooks** for automated quality gates
- You want an IDE that **persists context across sessions**

### When to Choose Something Else

- For **deepest reasoning**: [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) with Opus 4.6
- For **familiar VS Code experience**: [Cursor](/posts/ai/2026-02-28-claude-code-vs-cursor/)
- For **free parallel agents**: [Google Antigravity](/posts/ai/2026-03-10-google-antigravity-review/)
- For **terminal-first automation**: [Codex CLI](/posts/ai/2026-03-10-codex-cli-deep-dive/)

## Getting Started with Kiro

### Installation

```bash
# Download from kiro.dev
# Available for macOS, Windows, and Linux

# Or via Homebrew (macOS)
brew install --cask kiro
```

### First Project Setup

1. Open Kiro and sign in (AWS account or standalone)
2. Open your project folder
3. Run `Kiro: Initialize` from the command palette
4. This creates `.kiro/` with default steering files and hook templates

### Create Your First Spec

In the Kiro agent panel, type:

```
Build a REST API for a todo list with CRUD operations,
user authentication, and PostgreSQL storage
```

Kiro will generate specs, task plans, and wait for your approval before writing any code.

## Tips for Safe and Effective Kiro Usage

1. **Always start with Review mode** — Don't enable full autonomy until you trust the agent's behavior on your specific project
2. **Write detailed Steering Files** — The more context you give Kiro about your project, the better its specs and code
3. **Set up Agent Hooks early** — Automated test regeneration and security scanning catch issues before they accumulate
4. **Limit permissions in production** — After the AWS incident, this should be non-negotiable
5. **Review specs thoroughly** — The spec is your contract with the agent. Sloppy specs lead to sloppy code

## Final Verdict

**Rating: 7.5/10**

Kiro's spec-driven approach is genuinely innovative and produces more structured, predictable results than "just start coding" tools. The Agent Hooks and deep AWS integration make it especially compelling for enterprise teams.

But the AWS outage incident casts a shadow. The "code autonomously for days" promise needs serious guardrails. Use Kiro for its spec-driven workflow and automated quality gates, not for unsupervised production deployments.

**Best for**: Teams that value structured development processes, AWS-native organizations, and developers who want AI that plans before it codes.

---

*Review based on Kiro as of March 2026. Features and pricing evolve frequently — check [kiro.dev](https://kiro.dev/) for the latest.*

## Related Reading

- [Google Antigravity Review](/posts/ai/2026-03-10-google-antigravity-review/) — The free agent-first alternative
- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — The terminal-first approach
- [Codex CLI Deep Dive](/posts/ai/2026-03-10-codex-cli-deep-dive/) — OpenAI's terminal agent
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Compare with Kiro's Agent Hooks
- [CLAUDE.md Guide](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — Compare with Kiro's Steering Files
- [Claude Code Security](/posts/ai/2026-02-22-claude-code-security/) — Why human oversight matters
