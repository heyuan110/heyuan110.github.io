+++
date = '2026-02-01T17:00:00+08:00'
draft = false
title = 'Superpowers Deep Dive: The Skills Framework That Makes Claude Code a Senior Engineer'
description = 'Superpowers is a 40K-star agentic skills framework for Claude Code. It enforces TDD, subagent-driven development, and structured planning to transform AI coding assistants into disciplined senior developers.'
toc = true
tags = ['Claude Code', 'Superpowers', 'TDD', 'Agent Skills', 'AI Coding']
categories = ['AI Guides']
keywords = ['Superpowers Claude Code', 'agentic skills framework', 'Claude Code plugin', 'test driven development AI', 'subagent driven development', 'obra superpowers']
+++

![Superpowers Deep Dive](cover.webp)

Have you ever asked Claude Code to build a feature, only to watch it immediately start writing code with no tests, no plan, and questionable logic -- forcing you to course-correct over multiple rounds?

**The problem isn't AI capability. It's the lack of a structured workflow.**

[Superpowers](https://github.com/obra/superpowers) was built to solve exactly this. Created by Jesse Vincent (GitHub: [obra](https://github.com/obra)), it's an **agentic skills framework** that uses composable **Skills** and a strict development methodology to transform Claude Code from a "write code on demand" assistant into a "disciplined senior developer."

With over **40,000 GitHub stars**, Superpowers is the most popular Claude Code skills library available today. This article covers its core principles, complete workflow, installation, and how to use it to genuinely improve your AI-assisted development.

## What Is Superpowers?

### One-Line Definition

Superpowers is an **agentic skills framework** that uses SKILL.md files to make AI coding agents automatically follow structured software development processes -- from brainstorming to TDD, from planning to code review, with a dedicated skill governing each phase.

### What It Is Not

Superpowers is **not** a prompt template collection or a simple `.cursorrules` file. Its key innovations include:

- **Automatic activation**: Skills trigger based on context -- you don't need to remember commands
- **Enforcement, not suggestion**: If Claude tries to write implementation code without tests, the skill forces it to delete the code and start over
- **Composable**: 14 core skills combine like building blocks to cover the full development lifecycle
- **Token-efficient**: The core bootstrap is under 2,000 tokens, with skills loaded on demand

### Background on the Author

Jesse Vincent is a veteran open-source developer who shared the origin story of Superpowers on his [blog](https://blog.fsck.com/2025/10/09/superpowers/). He discovered that the key to working with AI coding agents isn't getting them to write more code -- it's making them **think and work like professional engineers**. He encoded decades of development methodology -- TDD, systematic debugging, structured planning -- into a set of skills that Claude can automatically apply in any project.

## The Seven-Stage Workflow: From Idea to Delivery

The core value of Superpowers is its **seven-stage development workflow**. When you describe what you want to build, Claude doesn't jump straight into coding. Instead, it progresses through a structured pipeline:

### Stage 1: Brainstorming

> Think before you build.

When you describe a requirement, Claude activates the `brainstorming` skill and uses Socratic questioning to **clarify the real problem**:

- What is the core problem you're solving?
- What alternative approaches exist? What are the trade-offs?
- What are the edge cases and failure modes?

It compiles the discussion into a **design document**, presenting it section by section for your approval. This process typically spans a dozen or more exchanges to ensure the approach is thoroughly vetted before any code is written.

### Stage 2: Git Worktree Isolation

> Never experiment on the main branch.

Once the design is approved, Claude activates the `using-git-worktrees` skill:

1. Creates a Git Worktree on a new branch (an isolated workspace)
2. Runs project initialization
3. Confirms all existing tests pass (establishing a clean baseline)

If the experiment fails, your main branch remains untouched.

### Stage 3: Writing Plans

> Break the elephant into bite-sized pieces.

The `writing-plans` skill decomposes the implementation into **small, discrete tasks**, each designed to be completable in minutes. Every task includes:

- Exact file paths
- Specific code changes
- Clear verification steps

This isn't a vague TODO list -- it's an **executable engineering plan**.

### Stage 4: Subagent-Driven Development

> Let focused subagents tackle tasks one by one.

This is one of Superpowers' most powerful capabilities. The `subagent-driven-development` skill **dispatches a fresh subagent** for each task:

- Each subagent focuses on a single task with a clean context
- After completion, the main agent performs a **two-phase review**: first checking compliance with the spec, then checking code quality
- Critical issues block progress and must be fixed before continuing

This pattern lets Claude **work autonomously for hours** without drifting from the plan.

### Stage 5: Test-Driven Development (TDD)

> Write the test first. No exceptions.

The `test-driven-development` skill enforces the classic **RED-GREEN-REFACTOR** cycle throughout implementation:

1. **RED**: Write a failing test
2. **GREEN**: Write the minimum code to make it pass
3. **REFACTOR**: Clean up the code while keeping tests green
4. **COMMIT**: Commit the complete cycle

**If Claude tries to skip tests and write implementation code directly, the skill forces it to delete the code and start over.** No negotiation.

### Stage 6: Code Review

> Even your own code needs a review.

Between tasks, the `requesting-code-review` skill automatically triggers to review completed work:

- Issues are classified by severity: Critical / Major / Minor
- **Critical issues block progress** and must be resolved before continuing
- It's like having a senior engineer doing continuous code review

Superpowers 4.0 further splits the review into two independent agents: a **spec compliance agent** (checking if the implementation matches the plan) and a **code quality agent** (checking code quality), each with a distinct focus.

### Stage 7: Branch Completion

> Finish what you started.

Once all tasks are done, the `finishing-a-development-branch` skill:

1. Verifies all tests pass
2. Offers options: merge to main, create a PR, continue development, or discard the branch
3. Cleans up the Worktree

A complete development cycle from start to finish.

## The Skills System: The Heart of Superpowers

### What Is a Skill?

A Skill is a `SKILL.md` file, potentially accompanied by scripts and documentation. Each Skill defines:

| Element | Description |
|---------|-------------|
| **Purpose** | What problem this skill solves |
| **Trigger conditions** | When this skill should be used |
| **Execution flow** | Step-by-step instructions |
| **Anti-patterns** | Common mistakes to avoid |
| **Verification criteria** | How to confirm the skill was executed correctly |

### The 14 Core Skills

Superpowers ships with 14 core skills organized into four categories:

**Testing**
- `test-driven-development`: RED-GREEN-REFACTOR cycle + test anti-pattern reference

**Debugging**
- `systematic-debugging`: Four-stage root cause analysis (reproduce, collect data, analyze cause, verify fix)
- `verification-before-completion`: Evidence-based verification before marking work as done

**Collaboration**
- `brainstorming`: Structured brainstorming
- `writing-plans`: Engineering plan creation
- `executing-plans`: Plan execution
- `dispatching-parallel-agents`: Parallel subagent orchestration
- `requesting-code-review`: Initiating code review
- `receiving-code-review`: Processing review feedback
- `using-git-worktrees`: Git Worktree workflow
- `finishing-a-development-branch`: Branch completion and cleanup
- `subagent-driven-development`: Subagent-driven development

**Meta-Skills**
- `writing-skills`: The skill for writing new skills (a meta-skill)
- `using-superpowers`: System bootstrap

### How Automatic Skill Activation Works

You don't need to manually tell Claude "use the TDD skill now." The Superpowers bootstrap system tells Claude at startup:

1. You have a set of skills that give you "superpowers"
2. Search for skills using a shell script
3. Read the skill content and follow its instructions
4. **If an activity has a corresponding skill, you must use it**

This mechanism is highly token-efficient -- the core bootstrap is under 2,000 tokens, with specific skills loaded on demand.

### Two-Layer Skill Architecture

Superpowers uses a two-layer architecture:

- **Core Skills**: Installed with the plugin, providing universal methodology
- **Personal Skills**: Stored in `~/.config/superpowers/skills/`, allowing you to create custom skills for your tech stack and workflow preferences

Personal skills have **override priority** -- if a path matches, your personal skill takes precedence over the core skill.

## Installation and Quick Start

### Installation (Two Commands)

Make sure your Claude Code version is >= 2.0.13, then run:

```bash
# Register the Superpowers marketplace
/plugin marketplace add obra/superpowers-marketplace

# Install the Superpowers plugin
/plugin install superpowers@superpowers-marketplace
```

Exit and restart Claude Code. Type `/help` -- if you see commands like `/superpowers:brainstorm`, `/superpowers:write-plan`, and `/superpowers:execute-plan`, the installation was successful.

### Three Ways to Use Superpowers

**Option 1: Slash Commands**

```bash
/superpowers:brainstorm I want to build a CLI tool for managing dotfiles
/superpowers:write-plan
/superpowers:execute-plan
```

**Option 2: Conversational Invocation**

Use natural language:

```
Use superpowers to brainstorm this task
```

Claude will recognize the intent and activate the appropriate skill.

**Option 3: Automatic Activation**

The recommended approach -- simply describe your requirements naturally, and Superpowers will automatically activate the appropriate skill based on context. For example, saying "I want to add user authentication to this project" will automatically trigger the brainstorming phase.

### Recommended Workflow in Practice

Based on the experience of multiple developers, this workflow produces the best results:

1. **`/superpowers:brainstorm`** -- Describe your requirements and let Claude ask thorough questions
2. **`/superpowers:write-plan`** -- Generate the plan document
3. **Manual plan review** -- This step is critical! Go back and forth with Claude to refine details
4. **`/superpowers:execute-plan`** -- Let subagents execute the plan

> Key takeaway: **Never skip the manual plan review step.** Plan quality directly determines execution quality. Time invested in planning saves hours of rework.

## Advanced: Understanding the Design Philosophy

### Why Is TDD Mandatory?

Many developers feel that having AI write tests wastes tokens. But Jesse Vincent's experience shows that mandatory TDD delivers benefits far exceeding the cost:

- **Tests are specifications**: Tests explicitly define what "correct" means, reducing AI ambiguity
- **Fast feedback**: The RED-GREEN cycle provides deterministic verification at each step
- **Regression prevention**: When subagents modify code, the test suite ensures previous functionality isn't broken
- **YAGNI enforcement**: Writing only the minimum code to pass tests prevents AI over-engineering

### Persuasion Principles

This is one of Superpowers' most fascinating design details. Jesse mentioned in his blog that he drew on Robert Cialdini's persuasion research, finding that **LLMs do respond to frameworks like Authority, Commitment, Scarcity, and Social Proof**.

He embedded these principles into the skill designs to make Claude more willing to follow skill guidance. Even the name "Superpowers" itself may play a role -- when Claude is told it possesses "superpowers," it appears more inclined to use these skills.

### GraphViz Flowchart Notation

Starting with Superpowers 4.0, internal process documentation uses GraphViz `dot` notation. The reason: Claude is particularly good at understanding and following flowcharts written in `dot` -- they produce **less ambiguity** than prose descriptions and result in more consistent execution.

### TDD for Skills Themselves

Jesse doesn't just apply TDD to code -- he applies it to **the skills themselves**. The process works like this:

1. Write a new skill
2. Have a group of subagents test the skill under stress scenarios (simulating production incidents, time pressure, sunk-cost situations, etc.)
3. Observe whether subagents correctly follow the skill
4. Iterate and improve the skill based on results

Claude now refers to this process as "RED/GREEN TDD for skills."

## Ecosystem

Superpowers is not an isolated project -- it has a complete ecosystem:

| Repository | Description |
|------------|-------------|
| [obra/superpowers](https://github.com/obra/superpowers) | Core plugin |
| [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | Claude Code plugin marketplace |
| [obra/superpowers-skills](https://github.com/obra/superpowers-skills) | Community skill library |
| [obra/superpowers-lab](https://github.com/obra/superpowers-lab) | Experimental skills |
| [obra/superpowers-chrome](https://github.com/obra/superpowers-chrome) | Chrome browser control plugin |

### Cross-Platform Support

Superpowers extends beyond Claude Code to other platforms:

- **OpenAI Codex**: Supported since Superpowers 3.3
- **OpenCode**: An open-source agentic coding tool, not locked to a specific model

### Version History

| Version | Key Changes |
|---------|-------------|
| **1.0** | Initial release with basic skills system |
| **2.0** | Skills extracted to independent Git repos, supporting forks and customization |
| **3.3** | Ported to OpenAI Codex |
| **4.0** | Code review split into dual agents, GraphViz flowcharts introduced, Opus 4.5 compatibility |
| **4.1** | Current stable release (v4.1.1) |

## Use Cases and Limitations

### Best Suited For

- Multi-file refactoring
- Production features requiring test coverage
- Projects needing team consistency
- Long-running migration tasks
- Complex features requiring architectural design

### Less Ideal For

- Quick bug fixes (one or two lines of code)
- Prototypes and demos (where engineering discipline is overkill)
- Single-file minor changes
- Simple configuration updates

### Known Limitations

- **Subagent context injection issues**: Subagent sessions may not receive the `using-superpowers` injection context, causing inconsistent skill activation. This is a [known issue](https://github.com/obra/superpowers/issues/237), and the community is exploring a `SubagentStart` hook as a solution.
- **Opus 4.5 over-inference**: Claude Opus 4.5 sometimes "guesses" skill content from descriptions instead of actually reading them. Superpowers 4.0 mitigates this by modifying skill descriptions.
- **Token consumption**: While the core bootstrap is lightweight, the full brainstorm-plan-execute pipeline does consume more tokens.

## Conclusion

Superpowers represents a fundamental shift in AI-assisted development: **instead of getting AI to write more code, teach it to write code the right way.**

Through a carefully designed skills system, it encodes decades of software engineering best practices -- TDD, systematic debugging, structured planning, code review -- into instructions that AI can understand and execute. The result is that Claude Code transforms from a chatbot that outputs code on demand into a disciplined developer capable of working autonomously for hours.

If you're using Claude Code for real-world project development, Superpowers is worth trying. Start with a small project and experience the difference between structured AI development and casual vibe coding.

## Further Reading

- [Claude Code Practical Guide: From Beginner to Advanced](/posts/ai/2026-01-14-claude-code-guide/)
- [Claude Code Skills Leaderboard: Top 20 Most Popular Skills](/posts/ai/2026-01-20-claude-code-skills-top20/)
- [Complete Guide to Claude Code Skill Development](/posts/ai/2026-01-08-claudecode-skill-guide/)
- [Claude Code Best Practices](/posts/ai/2026-01-06-claudecode-best-practices/)
- [Agent Skills: The New Programming Paradigm](/posts/ai/2026-01-19-agent-skills-new-programming/)
- [CLAUDE.md Memory Management Complete Guide](/posts/ai/2026-01-12-claudemd-memory-guide/)

## References

- [Superpowers GitHub Repository](https://github.com/obra/superpowers)
- [Jesse Vincent's Blog: The Birth of Superpowers](https://blog.fsck.com/2025/10/09/superpowers/)
- [Superpowers 4.0 Release Notes](https://blog.fsck.com/2025/12/18/superpowers-4/)
- [Practical Workflow by Stan Lo](https://st0012.dev/links/2026-01-15-a-claude-code-workflow-with-the-superpowers-plugin/)
- [Superpowers In-Depth Review by betazeta.dev](https://betazeta.dev/blog/claude-code-superpowers/)
