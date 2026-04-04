+++
date = '2025-12-26T12:40:02+08:00'
title = 'Claude Code Skills vs SubAgents: Context Management Guide'
description = 'Learn the key differences between Skills and SubAgents in Claude Code. Understand when to internalize capabilities vs delegate to child agents for optimal context management.'
toc = true
tags = ['AI', 'Claude Code', 'Skills', 'SubAgent']
categories = ['AI Guides']
keywords = ['Claude Code Skills vs SubAgents', 'AI agent context management', 'Claude Code SubAgent', 'agent architecture patterns', 'AI agent delegation']
+++
![ClaudeCode Skill](cc-skill-agent.webp)

There are two fundamentally different ways to make an AI agent more capable.

The first is **Skills** — loading new abilities directly into the agent's own brain.

The second is **SubAgents** — delegating work to a separate agent and only reviewing the results.

Both approaches sound like they get the job done, but they suit very different scenarios. Pick the wrong one and your agent may actually get slower and less reliable over time.

## Skills: Installing Plugins Into the Main Agent

Imagine your agent can only chat, but you want it to create slide decks. With the Skills approach, you inject the slide-creation instructions, tool-calling patterns, and best practices straight into the main agent's context. The agent learns the skill on the spot and handles everything itself.

## SubAgents: Delegating to a Specialist

Same scenario — creating slides — but this time the main agent hands the task off to a dedicated SubAgent that specializes in slide creation. The SubAgent works independently, then returns the finished result. The main agent never touches the details; it only assigns the task and reviews the output.

One path internalizes the capability. The other outsources it. Both can complete the task — so what's the real difference?

## The Core Difference: Context Management

Context is an AI's working memory, and it is the deciding factor.

Think of an AI's context window as a desk. The desk has a fixed size. The more documents you pile on it, the harder it becomes to find the one you actually need.

**Under the Skills model**, every capability's instructions sit on the same desk. The upside: information flows freely, the main agent sees all intermediate results, and reasoning stays coherent. The downside: the desk gets cluttered fast. Prompts grow longer, capabilities can conflict with each other, and the AI starts making mistakes.

**Under the SubAgent model**, the SubAgent works at a separate desk. When it finishes, it passes back only the result. All the drafts and intermediate artifacts stay on its own desk. The main agent's workspace remains clean. The trade-off: you need to design the handoff carefully, or critical information can get lost in transit.

This is the **context pollution** problem — not a dramatic metaphor, but a real engineering bottleneck.

## When to Use Which

The decision comes down to two questions: How complex is the subtask? And do you need access to the intermediate results?

### Use Skills When...

The task is relatively simple, or you need the main agent to stay in full control.

A great example is using the agent as a **router**. Based on the user's request, it loads different "modes" — a YouTube summarizer mode, a report-writing mode, and so on. Skills shine here because of **lazy loading**: you start by loading only the skill name and a brief description. The full instructions load only when the skill is actually invoked. Unlike MCP, which dumps every tool's detailed documentation into context all at once.

### Use SubAgents When...

The subtask is heavy, time-consuming, or generates a lot of verbose intermediate output.

The classic example is **browser debugging tools**. Chrome DevTools MCP is powerful, but its tool descriptions are massive. Loading them into the main agent's context eats up significant capacity. Wrap it as a SubAgent instead. You just say "go check the logs, take screenshots, and analyze." The SubAgent runs its investigation and returns a concise analysis. All those screenshots, DOM trees, and network request details stay on the SubAgent's side — never polluting the main agent's context.

## Advanced Patterns: Combining Both

The interesting part is that Skills and SubAgents aren't mutually exclusive. You can combine them in creative ways.

### Pattern 1: Expand Then Compress

Picture a two-hour brainstorming session. The whiteboard is covered with rough ideas, debates, and rejected proposals. But the meeting notes capture just three conclusions. The messy process was essential to reaching those conclusions, but it's pure noise for whoever executes the plan next.

Agents can work the same way. The main agent loads a Skill, runs through a complex operation, and gets a result. Then it **collapses** the entire sequence — from "load Skill" to "got result" — into a compact summary. For all subsequent reasoning, it's as if a meeting happened but only the minutes survived.

### Pattern 2: Use the File System as a Relay

Imagine managing an outsourced team. You wouldn't cram every requirement detail into a single chat message. Instead you'd say: "The spec is at this link — go read it." When the team delivers, they don't paste source code into a message either. They say: "Code is in this repo, deployment docs are here."

Agents can collaborate the same way. When delegating a task, the main agent saves lengthy background material to a file and passes only the file path. The SubAgent returns a brief status summary — "done / blocked / need your decision" — plus a path to the detailed log. The main agent decides whether to dig into the details or move on. Both sides keep their context lean.

### Pattern 3: The Context Rewind Trick in Claude Code

When context is running low, have Claude summarize all completed work into a document. Then use the **rewind** feature to roll back to the state before the task started. Tell it: "This task is already done. The record is in this file."

What does this achieve? It's like running a marathon, hitting the wall near the finish line, then drawing a map of the route you've already covered, teleporting back to the start with full energy, and saying "I know the way — here's the map." The context is cleared, but the results are preserved. This technique lets you rescue progress before context runs out.

## The Bigger Picture

The competition among AI agents is shifting from "how many tools can you call" to "how elegantly can you manage those tools."

Many developers chase the latest agent frameworks and flashiest capability extensions, while overlooking the most fundamental constraint: **AI working memory is finite**. How you organize it determines how complex a task the agent can handle. Skills and SubAgents aren't an either-or choice — they're two tools in your toolkit, and each delivers value only when applied to the right scenario.

At the end of the day, agent architecture design shares a lot of DNA with traditional software architecture:
- Do you write everything in one monolithic function, or break it into modular services?
- Do you share global state for convenience, or strictly isolate it for cleanliness?

These old questions have put on new clothes — but they're very much back.

## Related Reading

- [Skills vs MCP in Claude Code: Two Ways to Extend AI Capabilities](/posts/ai/2026-01-06-skill-mcp/) — How Skills and MCP servers complement each other
- [Claude Code Skills Guide: Teach AI Your Exact Workflow](/posts/ai/2026-01-08-claudecode-skill-guide/) — Hands-on guide to creating custom Skills
- [Claude Code Skills: Create Custom AI Abilities in 30 Seconds](/posts/ai/2026-01-12-claudecode-skill-patterns/) — Advanced patterns for Skill development
- [Claude Code Agent Teams 2026: Parallel Multi-Agent Development](/posts/ai/2026-02-22-claude-code-agent-teams/) — How multi-agent collaboration works in practice
- [Agent Skills: Why Markdown Files Are the New Programs](/posts/ai/2026-01-19-agent-skills-new-programming/) — The paradigm shift from code to natural language instructions
- [CLAUDE.md Guide: Give Claude Code Persistent Memory](/posts/ai/2026-01-12-claudemd-memory-guide/) — Configure the context that Skills and SubAgents inherit
