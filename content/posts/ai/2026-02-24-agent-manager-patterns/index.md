+++
date = '2026-02-24T08:00:00+08:00'
draft = false
title = 'Stanford CS146S Deep Dive (3): Agent Manager — Best Practices for Human-AI Collaboration'
description = "A deep dive into Stanford CS146S Week 4: from Claude Code creator Boris Cherney's talk to Anthropic's official best practices, learn how to manage Coding Agents and design human-AI collaboration patterns."
toc = true
tags = ['Agent Manager', 'Claude Code', 'AI Coding', 'Stanford CS146S', 'Human-AI Collaboration']
categories = ['AI Guides']
keywords = ['Agent Manager', 'Claude Code best practices', 'Coding Agent patterns', 'human-AI collaboration coding', 'Agent autonomy']
+++

> This is Part 3 of the "Stanford Vibe Coding Course Deep Dive" series. See the series navigation at the end of this article.

The title of CS146S Week 4 is "Coding Agent Patterns," but what it really teaches is an entirely new professional skill: **Agent Manager**.

What is an Agent Manager? Someone who doesn't write code directly but directs AI Agents to write code. It might sound like being a "hands-off boss," but in reality, this may be one of the hardest and most valuable skills of the AI coding era.

Why is it hard? Because you need three capabilities simultaneously:

1. **Technical judgment**: The ability to evaluate AI-generated code quality and know what passes and what doesn't
2. **Task decomposition**: The ability to break complex requirements into subtasks an Agent can complete independently
3. **Communication precision**: The ability to convey the most accurate intent with the least amount of information

This week's guest was **Boris Cherney** — the creator of [Claude Code](/posts/ai/2026-01-14-claude-code-guide/). Learning how to use a tool directly from its creator — the value speaks for itself.

## The Autonomy Spectrum of Agents

AI coding Agents are not a binary switch — "fully automatic" or "fully manual." They exist on an **autonomy spectrum**, and you need to dynamically adjust based on task type.

Devin (Cognition)'s [Agents 101](https://devin.ai/agents101) documentation divides this spectrum into three zones:

### Low Autonomy: Simple Tasks

- **Characteristics**: Clear input/output, limited decision space
- **Examples**: Renaming variables, adding type annotations, writing unit tests, fixing lint errors
- **Management approach**: Describe the requirement directly, almost no intervention needed
- **Time saved**: Close to 100%

In this zone, the Agent is like a skilled typist — you tell it what to do, and it does it. Your role is more like "the person giving orders."

### Medium Autonomy: Moderate Tasks

- **Characteristics**: Requires some design decisions, involves multiple files, has some ambiguity
- **Examples**: Implementing a new API endpoint, refactoring a module, adding a new feature
- **Management approach**: Provide detailed context + intermediate checks + manual polishing
- **Time saved**: About 80%

This is the zone where most daily development work falls. The Agent can complete 80% of the work, but the remaining 20% needs human polishing — handling edge cases, optimizing performance, ensuring consistency with existing code style.

Your role shifts from "giving orders" to "collaborative partner" — you work with the Agent like pair programming.

### High Autonomy: Complex Tasks

- **Characteristics**: Spans multiple systems, requires architectural decisions, has significant uncertainty
- **Examples**: Designing database schemas, implementing microservice communication, performance optimization, security hardening
- **Management approach**: Phased progression + multiple checkpoints + deep review
- **Time saved**: 30-60%

In this zone, the Agent is more like a junior engineer — capable of doing a lot of execution work, but needs a senior engineer to make calls at critical decision points. Your role becomes that of a true "Manager" — planning, decomposing, reviewing, and correcting.

Key mindset shift: **Don't expect the Agent to perfectly complete complex tasks in one shot.** Break complex tasks into multiple moderate tasks, progress in phases, and have clear acceptance criteria for each phase.

## Anthropic's Official Best Practices

One of the required readings for CS146S this week was [How Anthropic Uses Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) — first-hand experience from Anthropic's internal engineering team using Claude Code.

Combined with [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) ([Chinese analysis](/posts/ai/2026-01-06-claudecode-best-practices/)), we can distill the following core patterns:

### Pattern 1: Start with Planning, Not Coding

The most common mistake is jumping straight into having the Agent write code. A better approach is to have the Agent plan first:

```
# Bad approach
"Implement the user authentication system"

# Better approach
"Analyze the current project's authentication approach, list the files
that need modification and the steps involved.
Give me an implementation plan first, don't start writing code."
```

Get the plan first, review its feasibility, then have the Agent execute according to the plan. This is far more efficient than letting the Agent charge ahead only to discover the direction was wrong.

### Pattern 2: Use CLAUDE.md to Establish Project Standards

[CLAUDE.md](/posts/ai/2026-01-12-claudemd-memory-guide/) is the project-level configuration file that Claude Code reads. It functions like an "onboarding handbook for new employees" — telling the Agent about the project's conventions, tech stack, coding style, and taboos.

A good CLAUDE.md should include at minimum:

- Project overview and tech stack
- Coding standards and style guide
- Common commands (build, test, deploy)
- File structure description
- An explicit "do not do" list

The ROI of CLAUDE.md is extremely high — write it once, and it takes effect automatically in every conversation. This is the most direct application of "context engineering" discussed in Part 2 of the series.

### Pattern 3: Give the Agent Feedback Loops

An Agent shouldn't work in a vacuum. Let it see:

- **Test results**: Run the test suite and let the Agent see what passes and what fails
- **Lint/Type Check output**: Let the Agent know if the code meets standards
- **Build logs**: Compilation errors, dependency issues
- **CI/CD results**: Let the Agent see CI feedback in the PR workflow

These feedback loops act as "automated Code Review" — the Agent can self-correct based on feedback, reducing the number of human interventions needed.

### Pattern 4: Divide and Conquer

Break big tasks into small ones. Each subtask has clear input, output, and acceptance criteria.

```
# Bad approach
"Migrate the entire frontend from Vue 2 to Vue 3"

# Better approach
"We need to migrate the frontend from Vue 2 to Vue 3, step by step:
Step 1: First migrate src/components/Button.vue,
rewrite it using Composition API while keeping the same props interface.
After completion, run npm test -- --grep Button to confirm tests pass."
```

Small steps forward, verified at each step. This not only reduces the probability of errors but also makes it easier to spot and locate problems.

### Pattern 5: Keep Sessions Focused

One conversation, one task. When the context gets too long or drifts off topic, start a new session.

This directly relates to the "context distraction" discussed in Part 2 of the series — beyond a certain length, the AI's attention gets scattered and output quality drops. Timely "refreshing" of sessions is an effective way to maintain output quality.

## What We Learn from the Claude Code Creator

Boris Cherney is the creator of Claude Code. In his Week 4 guest lecture, he shared Claude Code's design philosophy and usage wisdom.

Combined with the publicly available [Slides](https://docs.google.com/presentation/d/1bv7Zozn6z45CAh-IyX99dMPMyXCHC7zj95UfwErBYQ8/edit?usp=sharing), the core ideas can be summarized as:

### Terminal-First Design Philosophy

Claude Code chose to run in the terminal rather than embed in an IDE. This isn't a step backward — it's a deliberate choice:

- **The terminal is the most universal development environment**: Not tied to any specific editor
- **The terminal naturally supports automation**: Can be called by scripts, run in parallel, embedded in CI/CD
- **The terminal gives the Agent full system access**: Not just reading and writing code, but also running tests, viewing logs, operating Git

The deeper implication of this design philosophy: Claude Code is not a "smarter code completion tool" — it's an **Agent capable of doing everything a software engineer does**.

### Trust but Verify

Claude Code's permission model is "trust but verify" — it proactively tells you what operation it's about to execute, and you can choose to approve or reject. For high-risk operations (deleting files, executing shell commands), explicit authorization is required.

The takeaway from this model: **Good Agent management isn't about distrusting the Agent, but about setting up checkpoints at critical junctures.** Like managing a junior engineer — you trust their daily work, but you review before merging to the main branch.

### Context Is Everything

A recurring theme Boris emphasized: Claude Code's output quality depends entirely on the context it receives. The same prompt, under different contexts (different CLAUDE.md, different codebase states, different conversation histories), produces completely different results.

This echoes the entire Week 3 theme and explains why "the same question works great for someone else with Claude Code but not for me" — **the difference isn't in the prompt, it's in the context**.

## Good Context Good Code: The Secret to 2.5x Productivity

Among Week 4's reading materials, [Good Context Good Code](https://blog.stockapp.com/good-context-good-code/) is the most practically valuable piece. The StockApp team claimed to have achieved **approximately 2.5x productivity improvement** (compared to purely manual development), far exceeding the commonly reported 30-50% improvement.

Their secret? A complete context management system.

### Layered Development Workflow

```
Design → Plan → Implement → Test → Review → Update
```

Each phase has corresponding documentation and AI interaction patterns:

- **Design phase**: Use AI for requirements analysis and technical solution design, output to `docs/designs/`
- **Plan phase**: Use AI to break designs into specific implementation steps, output to `docs/plans/`
- **Implementation phase**: AI writes code following the plan, referencing `schema.sql` and `docs/guides/`
- **Test phase**: AI generates test cases based on designs and plans
- **Review phase**: Multiple AI models cross-review code (ensemble method)
- **Update phase**: Update documentation and code based on feedback

### MCP Server Matrix

StockApp deployed multiple [MCP Servers](/posts/ai/2026-02-20-mcp-protocol-guide/) to extend AI's perception:

| MCP Server | Purpose |
|-----------|---------|
| Notion | Access product docs and knowledge base |
| Linear | Read tasks and issues |
| AWS | View infrastructure status |
| GitHub | Manage code repositories and PRs |
| Database | Query schema and data samples |

Each MCP Server acts as a pair of "eyes" for the AI — allowing it to see not just the code, but the entire business context surrounding the code.

### Ensemble Method

The most interesting practice is using multiple AI models for cross-review. Code written by one AI is reviewed by another AI (or even a different model). Different models have different blind spots and strengths — diversity brings more comprehensive review coverage.

This is like Code Review in human teams — not because the person who wrote the code is incompetent, but because a second pair of eyes always catches what the first pair missed.

## The Core Competency Model for Agent Managers

Synthesizing all materials from CS146S Week 4, I believe an excellent Agent Manager needs the following capabilities:

### 1. Task Decomposition

**Core question**: How do you break a complex requirement into subtasks an Agent can complete independently?

**Methodology**:
- Each subtask has clear input and output
- Dependencies between subtasks are explicit
- Each subtask can be tested independently
- Subtask granularity doesn't exceed "the amount one PR can review"

**Anti-patterns**:
- Having the Agent do an entire feature in one go
- Implicit dependencies between subtasks (unclear but assumed)
- Unable to verify whether a single subtask was completed correctly

### 2. Context Curation

**Core question**: What information do you provide to the Agent, and in what form?

**Methodology**:
- Follow the "minimum sufficiency principle" — only provide information needed for the current task
- Use a layered structure — from global to local, from abstract to concrete
- Ensure information consistency — no contradictions in the context
- Update timely — after completing a subtask, update the context for subsequent tasks

**Anti-patterns**:
- Dumping the entire codebase on the Agent (information overload)
- Providing a README that's outdated (context poisoning)
- Giving contradictory information (context conflict)

### 3. Quality Control

**Core question**: How do you evaluate the Agent's output quality?

**Methodology**:
- Have clear acceptance criteria (tests pass, lint passes, meets standards)
- Focus review on the Agent's "blind spots" — edge cases, security handling, performance impact
- For critical code paths, manually walk through the logic
- Use the ensemble method — have another AI or human cross-review

**Anti-patterns**:
- Glancing at it and thinking "it runs, good enough"
- Only looking at the happy path, ignoring error handling
- Relying entirely on test passage as a quality standard (AI may generate "passing but meaningless" tests)

### 4. Autonomy Calibration

**Core question**: When do you let the Agent work autonomously, and when do you intervene?

**Decision framework**:

| Dimension | Low Risk (Let Go) | High Risk (Intervene) |
|-----------|-------------------|----------------------|
| **Impact scope** | Single file change | Across multiple systems |
| **Reversibility** | Easy to rollback | Hard to undo |
| **Security** | Internal logic | Involves user data/auth |
| **Certainty** | Clear standards exist | Requires subjective judgment |
| **Precedent** | Similar successful cases | Entirely new scenario |

### 5. Continuous Learning

**Core question**: How do you continuously improve Agent performance?

**Methodology**:
- Record the Agent's common error patterns and add corresponding rules to CLAUDE.md
- Summarize successful task description templates to build a reusable prompt library
- Track time savings ratios across different task types to optimize resource allocation
- Follow tool updates and adjust usage strategies accordingly

## From "Writing Code" to "Managing Agents"

CS146S Week 4 outlines a clear career evolution path:

```
Traditional developer: Write code → Review code → Deploy code
AI-assisted developer: Guide AI to write code → Review AI code → Deploy code
Agent Manager: Plan tasks → Configure context → Manage multiple Agents → Review results → Continuously optimize
```

With each step in this evolution, the human role **moves upward** — from execution layer to management layer to strategy layer.

This isn't "replacement" — it's "liberation." When Agents handle 80% of execution work, you have more energy for what only humans can do: understanding business requirements, making architectural decisions, safeguarding quality baselines, and anticipating technical directions.

Boris Cherney's original vision for Claude Code was exactly this — not to build a faster code editor, but to build an **Agent capable of independently completing software engineering tasks**, enabling human engineers to level up into Agent Managers.

Are you ready to level up?

## Related Reading

- [The Complete Guide to Claude Code](/posts/ai/2026-01-14-claude-code-guide/) — The tool Boris Cherney created, worth a deep dive
- [Claude Code Best Practices](/posts/ai/2026-01-06-claudecode-best-practices/) — Usage wisdom shared by the creator himself
- [Complete Guide to Claude Code Agent Teams](/posts/ai/2026-02-22-claude-code-agent-teams/) — From single Agent to multi-Agent collaboration
- [CLAUDE.md Memory Guide](/posts/ai/2026-01-12-claudemd-memory-guide/) — Core practices for project-level context management
- [Build a Claude Code from Scratch](/posts/ai/2026-02-24-build-magic-code/) — The best way to understand Agent architecture under the hood

## Series Navigation

This is Part 3 of the "Stanford Vibe Coding Course Deep Dive" series:

1. [Stanford CS146S Deep Dive (1): How Vibe Coding Became an Academic Discipline](/posts/ai/2026-02-24-stanford-cs146s-overview/)
2. [Stanford CS146S Deep Dive (2): Context Engineering](/posts/ai/2026-02-24-context-engineering-deep-dive/) (Week 3)
3. **This article**: Stanford CS146S Deep Dive (3): Agent Manager (Week 4)
4. [Stanford CS146S Deep Dive (4): Secure Vibe Coding](/posts/ai/2026-02-24-secure-vibe-coding/) (Week 6-7)
5. [Stanford CS146S Deep Dive (5): From Prototype to Production](/posts/ai/2026-02-24-prototype-to-production/) (Week 8-9)
