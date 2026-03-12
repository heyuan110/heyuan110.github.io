+++
date = '2026-01-13T19:00:00+08:00'
draft = false
title = 'Claude Cowork: Anthropic Desktop AI Agent That Controls Your Files'
description = 'Claude Cowork is a research preview desktop AI agent that directly accesses local files, runs code in sandboxed environments, and integrates with Notion, Linear, and GitHub via MCP. Currently macOS only.'
toc = true
tags = ['Claude Cowork', 'Claude Desktop', 'Anthropic', 'AI Agent', 'MCP']
categories = ['AI Guides']
keywords = ['Claude Cowork', 'Claude desktop agent', 'AI file access', 'Claude MCP integration', 'Anthropic Cowork setup']
+++

![Claude Cowork](cover.webp)

Anthropic has launched **Claude Cowork** as a research preview — arguably the most ambitious desktop AI agent to date. Unlike traditional chatbots that rely on copy-paste workflows, Claude Cowork directly accesses files on your computer, runs code, executes terminal commands, and integrates with third-party apps like Notion, Linear, and Figma.

## What Is Claude Cowork?

Claude Cowork is a new capability inside the Claude desktop app that transforms Claude from a conversation partner into a hands-on work assistant.

Instead of manually feeding file contents into a chat window, Cowork can:

- **Read and edit local files** on your machine
- **Run code** in a sandboxed environment
- **Execute terminal commands** directly
- **Connect to third-party apps** for richer context

You describe what you need done. Claude handles the rest.

## Core Features

### Local File Access

Cowork reads files directly from your filesystem — no manual uploads required. Common use cases include:

- Analyzing project code structure
- Organizing documents and notes
- Processing CSV, JSON, and other data files
- Batch-editing file contents

**How it works**: Type `@` in the conversation to select files or folders you want Claude to access.

### Sandboxed Code Execution

Cowork includes a secure sandbox for running Python, JavaScript, and other languages:

- Data analysis and visualization
- Automation script development
- Code testing and debugging
- File format conversion

All code runs in an isolated environment, keeping your system safe.

### Third-Party App Integration

Through MCP (Model Context Protocol), Cowork connects with a growing ecosystem of apps:

| App | What Claude Can Do |
|-----|-------------------|
| Notion | Read and create pages, query databases |
| Linear | Manage tasks and track projects |
| Figma | Retrieve design file details |
| GitHub | Browse repos, issues, and pull requests |
| Slack | Search messages and channels |

This gives Claude the full context of your work environment, enabling more accurate and relevant assistance.

### Background Task Execution

Cowork supports **background mode**. Launch a complex task, minimize the window, and continue with other work. Claude processes the job silently and notifies you when it finishes.

## Security Architecture

Giving an AI agent access to local files and code execution raises obvious security concerns. Anthropic has built multiple layers of protection:

### Permission Prompts

Before executing any sensitive operation, Claude displays a confirmation dialog showing:
- Which files will be accessed
- What commands will run
- Potential impact of the action

### Sandbox Isolation

Code execution happens inside an isolated sandbox with no direct access to critical system areas.

### Activity Audit Log

Every action is logged in detail. You can review exactly what Claude did at any time.

### Scoped Access

You control precisely which folders Claude can access — it never has free rein over your entire filesystem.

## Real-World Use Cases

### Project Architecture Analysis

```
You: Analyze the architecture of this project and identify performance bottlenecks.

Claude: Let me examine the project structure...
[Reads files in src/ directory]
[Analyzes dependency graph]
[Generates architecture diagram and optimization recommendations]
```

### Data Processing

```
You: Merge all CSVs in my Downloads folder and sort by date.

Claude: On it...
[Reads all CSV files]
[Runs Python script in sandbox]
[Produces merged output file]
```

### Document Organization

```
You: Organize my notes folder by topic and create an index.

Claude: I'll sort through your notes...
[Scans note files]
[Classifies content by topic]
[Creates categorized directory structure and index file]
```

## Getting Started

### Requirements

- **OS**: macOS (Mac only at this time)
- **Subscription**: Claude Max ($100/month)
- **App version**: Latest Claude desktop app

### Setup Steps

1. Open the Claude desktop app
2. Go to Settings → Features
3. Enable the "Cowork" toggle
4. Restart the app

### Configuring Integrations

To connect third-party apps, you need to set up MCP servers. Anthropic provides detailed configuration guides in their official documentation.

## Current Limitations

As a research preview, Cowork comes with notable constraints:

- **macOS only** — Windows and Linux support has not been announced
- **Max subscription required** — $100/month price point
- **Feature stability** — some capabilities may be unreliable during the preview period
- **Restricted network access** — certain network operations are limited for security reasons

## Bottom Line

Claude Cowork marks a significant shift in how AI assistants work — moving from conversation to genuine collaboration. Rather than just answering questions, Claude now participates directly in your workflow.

The research preview is limited to Mac power users for now, but this direction signals where AI products are heading. If you work on a Mac and want a capable AI that goes beyond chat, Claude Cowork is worth trying.

**Links**:
- [Official blog announcement](https://claude.com/blog/cowork-research-preview)
- [Download Claude Desktop](https://claude.ai/download)

## Further Reading

- [Claude Code Browser Automation: Agent Browser vs Playwright vs DevTools](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Claude Code Best Practices Guide](/posts/ai/2026-01-06-claudecode-best-practices/)
- [Agent Skills: A New Programming Paradigm](/posts/ai/2026-01-19-agent-skills-new-programming/)
- [Claude Code Skills Complete Guide](/posts/ai/2026-01-08-claudecode-skill-guide/)
