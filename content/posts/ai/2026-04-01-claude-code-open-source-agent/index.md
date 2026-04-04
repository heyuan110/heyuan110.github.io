+++
date = '2026-04-01T10:00:00+08:00'
draft = false
title = 'Claude Code Open Source: The Rewrite That Hit 100K Stars in Hours'
description = 'Deep technical analysis of Claude Code Open Source — the clean-room Python and Rust rewrite of Claude Code agent harness architecture, born from the March 2026 source code leak. Architecture comparison, legal implications, and honest assessment.'
toc = true
tags = ['Claude Code Open Source', 'Open Source', 'AI Coding Tools', 'Claude Code', 'Agent Framework']
keywords = ['Claude Code Open Source review', 'Claude Code source leak', 'open source AI coding agent', 'Claude Code Open Source vs Claude Code', 'agent harness architecture', 'clean room rewrite']

[params]
  faq = [
    ['What is Claude Code Open Source?', 'Claude Code Open Source is an open-source AI coding agent framework built in Python and Rust. It is a clean-room rewrite of the Claude Code agent harness architecture, created after Anthropic accidentally leaked their source code via npm in March 2026.'],
    ['Is Claude Code Open Source legal to use?', 'Claude Code Open Source claims to be a clean-room implementation that reimplements architectural patterns without copying proprietary code. However, the legal landscape is untested. The project carries inherent risk since it was directly inspired by leaked proprietary source code.'],
    ['How does Claude Code Open Source differ from Claude Code?', 'Claude Code Open Source is written in Python and Rust instead of TypeScript, supports multiple LLM providers instead of Claude-only, and is fully open source under MIT license. Claude Code remains a proprietary, polished product with official Anthropic support.'],
    ['Should I switch from Claude Code to Claude Code Open Source?', 'For most developers, no. Claude Code offers a more polished, stable experience with official support. Claude Code Open Source is better suited for researchers, framework builders, and developers who need full control over their agent harness or want to use non-Claude models.']
  ]
+++

![Claude Code open-source agent framework visualization](cover.webp)

On March 31, 2026, a missing `.npmignore` entry shipped 512,000 lines of unobfuscated TypeScript to the public npm registry. Within hours, the entire internal architecture of Anthropic's Claude Code — the agent harness connecting LLMs to tools, file systems, and task workflows — was laid bare for the world to study.

Two days later, **Claude Code Open Source** launched as a clean-room Python and Rust rewrite. It became the fastest-growing repository in GitHub history, surpassing 100,000 stars in its first hours. This article examines what happened, what Claude Code Open Source actually is, and whether you should care.

## The Claude Code Source Leak: What Actually Happened

Security researcher **Chaofan Shou** discovered that Anthropic had accidentally published a 59.8 MB source map file in their Claude Code npm package. This single debug artifact contained the complete, unobfuscated TypeScript source across roughly 1,906 files.

The leak was not a security breach. Anthropic [confirmed it was a packaging error](https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/) — human error during a release process. But the damage was immediate and irreversible:

- **Snapshots spread within minutes.** GitHub mirrors were forked over 41,500 times before anyone could react.
- **A concurrent npm supply-chain attack** on the `axios` package happened hours before, meaning anyone who installed Claude Code between 00:21 and 03:29 UTC on March 31 may have pulled a malicious dependency containing a Remote Access Trojan.
- **The architecture was suddenly public knowledge.** One agent loop, 40+ discrete tools, on-demand skill loading, context compression, subagent spawning, task dependency graphs, and worktree isolation — all documented in source form.

The community reaction was split. Many argued the CLI should have been open source from the start, noting that Google's Gemini CLI and OpenAI's Codex were already open. Others raised serious concerns about intellectual property and the ethics of building on leaked code.

## What Is Claude Code Open Source?

Claude Code Open Source is an open-source AI coding agent framework created by **Sigrid Jin** ([@instructkr](https://github.com/instructkr)), a Korean developer who had attended Claude Code's first birthday party in San Francisco just weeks earlier. After the leak, Jin built the initial version overnight using [oh-my-codex](https://github.com/ultraworkers/claw-code), an orchestration layer on top of OpenAI's Codex, with parallel code review and persistent execution loops.

The project positions itself as a **clean-room rewrite** — reimplementing architectural patterns observed in the leaked source without copying proprietary code. Whether this distinction holds up legally remains untested.

### Language and Architecture

The codebase splits across two languages:

| Component | Language | Percentage | Purpose |
|-----------|----------|------------|---------|
| Agent orchestration | Python | 27.1% | LLM integration, command parsing, tool dispatch |
| Runtime execution | Rust | 72.9% | High-performance execution, memory safety |

The Rust layer is organized as a **6-crate workspace with 16 runtime modules**, targeting production-grade performance. A `dev/rust` branch tracks active migration work.

### Core Components

**19 permission-gated tools** covering:
- File I/O and bash execution
- Git operations
- Web scraping and HTTP requests
- LSP integration for code intelligence
- Notebook editing
- Subagent spawning

**15 slash commands** for session control, model switching, cost tracking, and session compaction.

**Multi-LLM support** — provider-agnostic design supporting Claude, OpenAI, and local models. This is the most significant architectural departure from Claude Code, which is locked to Anthropic's models.

**MCP integration** with 6 transport types, automatic name normalization, and OAuth support. If you are familiar with MCP from Claude Code, the integration model will feel familiar. For background on MCP, see my [MCP security analysis](/posts/ai/2026-03-10-mcp-security-2026/).

## Architecture Comparison: Claude Code Open Source vs Claude Code

Having worked extensively with Claude Code's [harness architecture](/posts/ai/2026-04-04-harness-engineering-guide/) and studied the leaked source, here is how the two systems compare at a structural level.

### The Agent Loop

Both systems follow the same fundamental pattern: a central loop that takes user input, constructs prompts with context, calls an LLM, parses tool-use responses, executes tools, and feeds results back into the next iteration.

Claude Code's implementation is a monolithic TypeScript bundle with tight coupling between the agent loop and Anthropic's API. Claude Code Open Source decomposes this into a Python orchestration layer backed by a Rust runtime, with explicit provider abstraction.

### Tool System

Claude Code ships roughly 40 tools. Claude Code Open Source currently implements 19 with a similar permission model — three access modes (allow, deny, ask) with per-tool policy configuration. The reduced tool count is partly by design (avoiding rarely-used tools) and partly because the project is still maturing.

### Context Management

Both systems implement context window management through **transcript compaction** — summarizing older conversation turns to stay within token limits. Claude Code's implementation is more sophisticated, with multi-layer memory and persistent knowledge graphs. Claude Code Open Source has basic session persistence but lacks the depth of Claude Code's [memory strategy](/posts/ai/2026-01-31-openclaw-memory-strategy/).

### Multi-Agent Orchestration

Claude Code Open Source calls this "swarms" — parallel subtask execution where a primary agent spawns child agents for independent work. Claude Code has a similar concept with [subagents](/posts/ai/2025-12-26-claudecode-skill%26subagent/), though the spawning model differs. Claude Code's subagent system is more battle-tested in production workflows.

### Where Claude Code Open Source Wins

1. **Full source visibility.** You can read, modify, and understand every line.
2. **Multi-LLM support.** Not locked to one provider.
3. **Rust performance layer.** Potentially faster for I/O-heavy operations.
4. **MIT license.** Use it however you want.

### Where Claude Code Wins

1. **Polish and stability.** Claude Code has been in production for over a year with a dedicated team.
2. **Deep Anthropic integration.** Optimized prompt engineering for Claude models.
3. **Ecosystem maturity.** Skills, hooks, CLAUDE.md conventions, worktrees — all battle-tested.
4. **Official support.** Bug reports get fixed. Breaking changes get migration guides.

## The Legal and Ethical Question

This is where things get uncomfortable. Claude Code Open Source claims clean-room status, but the reality is nuanced.

**The clean-room defense** requires that developers implementing the new system have never seen the proprietary source code. Given that the leaked source was publicly available and widely analyzed, and that Claude Code Open Source was built *in direct response* to seeing that architecture, the clean-room claim is on shaky ground.

**What independent audits found:** The project states that code audits confirm no Anthropic proprietary code or model weights are included. This addresses the narrowest legal question (direct copying) but not the broader one (was the architecture itself protectable trade secret information?).

**The practical reality:**
- **Copyright** protects expression, not ideas. Reimplementing an architecture pattern in a different language is generally permissible.
- **Trade secrets** lose protection once publicly disclosed, even accidentally. Anthropic's leak may have inadvertently waived trade secret claims.
- **No legal action has been taken** as of April 2026. Anthropic has not issued DMCA takedowns against Claude Code Open Source or the mirror repositories.

My honest assessment: using Claude Code Open Source for personal projects and research carries low risk. Building a commercial product on it carries higher risk until the legal landscape clarifies. Anthropic's silence is not the same as approval.

## Should You Use Claude Code Open Source?

This depends on who you are.

**Use Claude Code Open Source if you are:**
- A researcher studying agent harness architectures
- Building a custom agent framework for a specific domain
- Need multi-LLM provider support
- Want to learn how production AI coding agents work internally
- Contributing to open-source AI tooling

**Stick with Claude Code if you are:**
- A professional developer who needs reliable daily tooling
- Working in a corporate environment with legal compliance requirements
- Invested in the Claude Code ecosystem (skills, hooks, CLAUDE.md)
- Prioritizing stability over customizability

For context on how Claude Code fits into the broader landscape, see my [AI coding agents comparison](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/).

## What This Means for the AI Tooling Ecosystem

The Claude Code Open Source phenomenon reveals something important: **the agent harness layer is not the moat.** The models are.

Google's Gemini CLI is open source. OpenAI's Codex is open source. Now Claude Code's architecture has been independently reimplemented. The pattern is clear — the shell connecting an LLM to your file system and tools is becoming a commodity.

The real value lies in:
1. **Model quality** — how well the LLM reasons about code
2. **Prompt engineering** — how effectively the harness leverages the model
3. **Ecosystem integration** — skills, plugins, MCP servers, community tooling
4. **Reliability** — edge case handling, error recovery, session management

Anthropic's competitive advantage was never the TypeScript CLI wrapper. It was Claude's ability to reason about complex codebases. That has not changed.

## Getting Started with Claude Code Open Source

If you want to explore Claude Code Open Source:

```bash
git clone https://github.com/instructkr/claw-code.git
cd claw-code
pip install -r requirements.txt
python src/main.py
```

The repository includes a `tests/` directory for validation and CLI utilities for subsystem inspection and parity audits against Claude Code's feature set.

**Important caveats:**
- The project is under active development. Expect breaking changes.
- The Rust migration is ongoing. Some modules are Python-only.
- Community documentation is sparse compared to Claude Code.
- MCP server compatibility may vary from Claude Code's implementation.

## Conclusion

Claude Code Open Source is a technically impressive project born from unusual circumstances. It demonstrates that the agent harness pattern — the loop connecting LLMs to tools — is well-understood enough to be reimplemented in days. But being technically capable and being production-ready are different things.

For most developers, Claude Code remains the better choice for daily work. But Claude Code Open Source serves an important role as a reference implementation, a research platform, and a signal that the AI coding tool landscape is moving toward openness. The 100K+ stars are not just hype — they reflect genuine demand for transparency in how AI agents operate on our codebases.

The question is no longer whether agent harnesses should be open. It is how fast the industry will get there.

---

*Further reading:*
- [Harness Engineering: The Architecture Behind AI Coding Agents](/posts/ai/2026-04-04-harness-engineering-guide/)
- [Claude Code Complete Guide](/posts/ai/2026-01-14-claude-code-guide/)
- [AI Coding Agents Comparison 2026](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/)
- [MCP Security in 2026](/posts/ai/2026-03-10-mcp-security-2026/)

## Related Reading

- [OpenClaw vs CrewAI vs AutoGPT 2026: 6 AI Agent Frameworks Compared](/posts/ai/2026-03-05-openclaw-vs-ai-agents/) — How Claude Code Open Source fits in the broader agent framework landscape
- [Cursor Composer 2 Review: The Kimi K2.5 Controversy](/posts/ai/2026-04-04-cursor-composer-2-review/) — Another AI coding tool making waves the same week
- [Seedance 2.0 Deep Dive: ByteDance AI Video Model](/posts/ai/2026-04-04-seedance-2-bytedance-ai-video/) — Another open-source AI release from the same period
- [OpenCode Review: Can This Open Source AI Coding Agent Replace Claude Code?](/posts/ai/2026-03-13-opencode-ai-coding-agent-review/) — Earlier open-source Claude Code alternative
- [Claude Code vs Cursor vs Windsurf 2026: Speed, Cost & Control](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/) — The proprietary tools that Claude Code Open Source aims to replace
