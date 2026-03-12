+++
date = '2026-02-22T10:00:00+08:00'
draft = false
title = 'Claude Code February 2026 Updates: Worktree, Background Agents, Simple Mode'
description = 'Claude Code shipped major features in February 2026 including Git Worktree parallel development, background agent tasks, and a leaner Simple Mode. Full breakdown with commands and use cases.'
toc = true
tags = ['Claude Code', 'Git Worktree', 'AI Coding', 'Release Notes', 'Anthropic']
categories = ['AI Guides']
keywords = ['Claude Code update', 'Claude Code new features 2026', 'Claude Code worktree', 'Claude Code background tasks', 'Claude Code simple mode', 'Claude Code February update']
+++

Claude Code released over a dozen versions in February 2026 (v2.1.39 through v2.1.50), introducing several features that fundamentally change how you work. This article covers the most important updates, explains how to use each one, and highlights the practical scenarios where they shine.

## Git Worktree Support: The Biggest Workflow Upgrade

This is the headline feature of February, shipped in v2.1.49. It brings Git's worktree capability directly into Claude Code, making parallel development remarkably simple.

### What Is Git Worktree?

Git Worktree lets you check out multiple working directories from the same repository, each tied to a different branch. Unlike `git stash` or cloning the repo multiple times, worktrees share the same `.git` database — no extra disk space, no overhead when switching contexts.

### Basic Usage

A single command spins up Claude in an isolated worktree:

```bash
# Start a new worktree session
claude --worktree

# Short form
claude -w

# Name the worktree for easy identification
claude -w --name fix-login-bug
```

When you run this, Claude Code creates an independent working directory under `.claude/worktrees/`, branches off from your current HEAD, and does all file operations inside that isolated environment.

### True Parallelism with Tmux

The real power shows up when you combine worktrees with `--tmux` to run multiple sessions in the background:

```bash
# Run a worktree task in its own tmux session
claude -w --tmux --name feature-auth "Implement the user authentication module"

# Kick off a second task at the same time
claude -w --tmux --name fix-bug-123 "Fix the login error from issue #123"

# Check running tmux sessions
tmux ls
```

Each Claude session operates in its own file system — no conflicts, no interference.

### Declaring Worktree Isolation in Agent Definitions

Beyond CLI flags, v2.1.49 also supports declaring worktree isolation directly in agent definition files:

```yaml
# .claude/agents/refactor.md
---
name: refactor-agent
isolation: worktree
---
You are a refactoring specialist responsible for code restructuring tasks.
```

Subagents support `isolation: "worktree"` too, so each agent in a multi-agent setup works in its own sandbox.

### Hook Events

v2.1.50 added `WorktreeCreate` and `WorktreeRemove` hook events. These let you run custom actions automatically when a worktree is created or removed — installing dependencies, setting environment variables, whatever you need:

```json
{
  "hooks": {
    "WorktreeCreate": [{
      "command": "npm install",
      "description": "Auto-install dependencies"
    }],
    "WorktreeRemove": [{
      "command": "echo 'Worktree cleaned up'",
      "description": "Cleanup notification"
    }]
  }
}
```

There's a lot more to worktrees than what's covered here. For the full tutorial, best practices, and troubleshooting, see the [Claude Code Worktree Practical Guide](/posts/ai/2026-02-20-claude-code-worktree/).

## Background Task Management

v2.1.49 introduced background agents, letting you offload long-running tasks while continuing to work in your main session.

### Enabling Background Mode in Agent Definitions

Set `background: true` in your agent definition file:

```yaml
# .claude/agents/test-runner.md
---
name: test-runner
background: true
---
You are responsible for running the full test suite and reporting results.
```

Once launched, this agent runs in the background without blocking your main session.

### Stopping Background Agents

Press `Ctrl+F` to terminate background agents. To prevent accidental kills, you need to press it twice within 3 seconds:

```
First Ctrl+F  → Confirmation prompt
Second Ctrl+F → Terminates all background agents
```

A related change in v2.1.47: the `ESC` key now only cancels main-thread operations and no longer affects background agents. You can freely interrupt your current conversation without accidentally killing background tasks.

### Viewing Background Task Results

v2.1.47 improved how background task results are displayed. When an agent finishes, its final response appears inline in your main session — no need to dig through transcript files. If multiple tasks complete at the same time, notifications are collapsed with up to 3 lines shown plus an overflow summary.

## Simple Mode Enhancements

Claude Code's Simple Mode (enabled with the `CLAUDE_CODE_SIMPLE=true` environment variable) is a stripped-down mode designed for non-developers or quick one-off tasks.

### File Editing Capability

Before v2.1.49, Simple Mode only had access to the Bash tool. Now it includes **file editing tools**, allowing you to read and modify files directly — a significant usability improvement:

```bash
# Launch Simple Mode
CLAUDE_CODE_SIMPLE=true claude
```

### A Truly Minimal Experience

v2.1.50 went further by disabling several components in Simple Mode:

- MCP tools
- Attachments
- Hooks
- CLAUDE.md file loading
- Skills and Session Memory
- Custom Agents
- Token counting

This makes Simple Mode a genuinely lightweight terminal AI assistant — faster startup, lower resource usage.

## Performance Improvements

Multiple February releases included substantial performance work. Here are the changes you'll actually feel:

### Faster @ File Mentions

v2.1.47 specifically optimized the `@` file mention experience:

- **Index pre-warming at startup**: The file index now builds when Claude starts, not when you first type `@`
- **Session-level caching with background refresh**: File suggestion lists are cached for the duration of your session and silently updated in the background when files change

### Major Memory Leak Fixes

This was a quiet but significant theme across February. From v2.1.47 to v2.1.50, multiple memory leaks were identified and fixed:

| Issue | Version |
|-------|---------|
| Completed task state objects not released | v2.1.50 |
| LSP diagnostic data not cleaned up | v2.1.50 |
| Tree-sitter WASM memory growing unbounded | v2.1.49 |
| Yoga WASM linear memory never reclaimed | v2.1.49 |
| Large shell command output causing RSS to grow indefinitely | v2.1.45 |
| Agent task messages accumulating at O(n^2) | v2.1.47 |

Long-running sessions are noticeably more stable now.

### Startup Performance Gains

- Headless mode (`-p` flag) now lazy-loads Yoga WASM and UI components
- MCP authentication failures are cached to prevent repeated connection attempts
- MCP tool token counting is batched into a single API call
- SessionStart hook execution is deferred, saving roughly 500ms on startup

## Model Updates

### Sonnet 4.6 Replaces Sonnet 4.5

v2.1.45 introduced support for Claude Sonnet 4.6. Then in v2.1.49, Sonnet 4.5 (with 1M context) on the Max plan was replaced by Sonnet 4.6, which also supports the full 1M context window.

In v2.1.50, Opus 4.6's Fast Mode gained full 1M context support as well. If you're still on an older model, switch via the `/model` command.

### Disabling 1M Context

If you don't need the 1M context window (for example, to reduce token costs), v2.1.50 added an environment variable for that:

```bash
export CLAUDE_CODE_DISABLE_1M_CONTEXT=1
```

## Other Notable Updates

- **claude.ai MCP Connectors** (v2.1.46): Use MCP connectors configured on claude.ai directly from Claude Code
- **Agent List Command** (v2.1.50): `claude agents` lists all configured agents
- **Session Resume Fixes** (v2.1.47/v2.1.50): Multiple fixes for session resume failures and data loss
- **ConfigChange Hook** (v2.1.49): Triggers when config files change, useful for enterprise security auditing
- **Windows ARM64 Support** (v2.1.41): Native ARM64 binary support
- **CLI Auth Commands** (v2.1.41): New `claude auth login`, `claude auth status`, and `claude auth logout` commands

## Quick Reference

| Feature | Command / Config |
|---------|------------------|
| Start worktree | `claude --worktree` or `claude -w` |
| Named worktree | `claude -w --name my-feature` |
| Worktree + Tmux | `claude -w --tmux --name my-feature "task description"` |
| Agent worktree isolation | Set `isolation: worktree` in agent file |
| Background agent | Set `background: true` in agent file |
| Kill background agents | `Ctrl+F` (press twice within 3 seconds) |
| Simple Mode | `CLAUDE_CODE_SIMPLE=true claude` |
| Switch model | `/model` |
| Disable 1M context | `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` |
| List all agents | `claude agents` |

## What to Try First

If you only have time for one or two new features, here's the priority order:

1. **Worktree parallel development** (`claude -w`): If you regularly juggle multiple tasks, this will immediately change how you work. One command gives you an isolated environment — no more stashing, no more branch-switching headaches.

2. **Background agents**: Send test runs, builds, and deployments to the background while you keep coding in your main session.

3. **Upgrade to Sonnet 4.6**: If you're still on Sonnet 4.5, make the switch. Same 1M context window, better performance.

## FAQ

### How is a worktree different from a regular branch?

A regular branch only isolates Git history — the file system still shares the same working directory. A worktree creates a completely independent working directory tied to its own branch. This means two Claude sessions can modify files in different worktrees simultaneously without any conflicts. See the [Worktree Practical Guide](/posts/ai/2026-02-20-claude-code-worktree/) for a deep dive.

### How do I see background task output?

When a background agent finishes, a notification pops up in your main session with the final response displayed inline. You can also use the `/tasks` command to check the status and details of all background tasks.

### When should I use Simple Mode?

Simple Mode serves two audiences: non-developers who just need Claude to handle files and run commands, and developers in lightweight scenarios — quickly looking something up, editing a config file, or running a one-off task without loading the full MCP toolkit and Skills. It starts faster and uses fewer tokens.

## Further Reading

- [Claude Code Worktree Practical Guide](/posts/ai/2026-02-20-claude-code-worktree/) — Full tutorial and best practices for worktrees
- [Claude Code Browser Automation Compared](/posts/ai/2026-01-28-claude-code-browser-automation/) — Choosing the right testing and debugging approach
- [The Complete Claude Code Guide](/posts/ai/2026-01-14-claude-code-guide/) — From beginner to advanced
- [Claude Code Skills Top 20](/posts/ai/2026-01-20-claude-code-skills-top20/) — The most useful skills ranked
