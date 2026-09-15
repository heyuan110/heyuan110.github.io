+++
date = '2026-01-31T08:20:18+08:00'
draft = false
title = 'OpenClaw Memory Strategy: Tool-Driven RAG and On-Demand'
description = 'How OpenClaw implements agent memory using tool-driven RAG instead of prompt injection — combining BM25 and vector search, chunk-based indexing, and...'
toc = true
tags = ['OpenClaw', 'RAG', 'Vector Search', 'AI Agent', 'Memory System']
categories = ['AI Guides']
keywords = ['OpenClaw memory', 'agent memory architecture', 'RAG memory system', 'BM25 vector search', 'tool-driven recall', 'AI agent memory design']

[[params.faqItems]]
question = "How does OpenClaw's memory system actually work?"
answer = "Through two tools rather than prompt injection. `memory_search` runs a hybrid query that combines BM25 full-text scoring with vector similarity, and `memory_get` pulls an exact text chunk by file path and line range. Nothing is concatenated into the system prompt automatically — the agent decides whether recall is needed, what to search for, and how much to retrieve. That keeps irrelevant history out of the context window and makes recall part of the agent's own reasoning."

[[params.faqItems]]
question = "Is OpenClaw memory a RAG system?"
answer = "Yes — it is a production-shaped RAG layer with three separated stores: `chunks` holds text plus metadata (file path, line range, source), `chunks_vec` holds embedding vectors, and `chunks_fts` holds the full-text index. Splitting them buys three properties: explainability, because every result traces back to a file and line numbers; tunability, because BM25 and vector recall can be weighted and reranked independently; and auditability, because you can inspect exactly what was indexed."

[[params.faqItems]]
question = "Why not just inject a user profile into the system prompt every turn?"
answer = "It works, but it burns tokens and scales badly — every request pays for context that is usually irrelevant. The article's analogy: auto-injection is like having someone read your entire resume aloud before every sentence you speak, while tool-driven retrieval is reaching for your notebook when you actually need it. The second matches how people work and is what handing control to the agent really means."

[[params.faqItems]]
question = "What does OpenClaw index besides chat history?"
answer = "Workspace documents. Any `.md` file the agent produces — notes, summaries, SOPs, articles — is chunked and added to the memory index alongside raw conversation data. The reasoning is that a competent colleague asked how something was handled last time does not scroll back through old chat messages, they open the document they wrote. Agent-generated structured output is often more valuable for recall than the transcript that produced it."

[[params.faqItems]]
question = "How does OpenClaw index new sessions, and what happens to compacted history?"
answer = "Sessions are stored as `.jsonl` files and indexed incrementally: the files are watched for changes, and once new content crosses a threshold the delta is read and chunked. Compression is treated as an addition, not a replacement — unlike systems where a `/compact` summary overwrites or deletes old messages, OpenClaw keeps both the original session data and the summary as indexable sources. Memory behaves like log retrieval rather than a curated persona."

[[params.faqItems]]
question = "What should I copy if I am building my own agent memory?"
answer = "Three patterns. Anchor long-term preferences in an explicit file such as a Profile or `MEMORY.md` that the agent can reference reliably. Index what the agent writes, not only what it said. And teach it an actual retrieval workflow — first decide whether this task needs recall at all, then pick the keywords or concepts to search, then fetch only the fragments needed. Minimal, engineered, agent-controlled, with retrievability valued over automatic injection."
+++

![OpenClaw memory strategy overview](cover.webp)

## Why Memory Matters for AI Agents

Modern AI agents need more than conversation ability. Users expect agents to:

- **Remember who you are** — your preferences, project context, and past interactions
- **Use that knowledge when it matters** — without stuffing everything into the context window every turn

Many chatbot platforms solve this by maintaining a long-term user profile and injecting it into the system prompt on every request. It works, but it wastes tokens and scales poorly.

OpenClaw takes a fundamentally different approach: **memory is not automatically injected — it is retrieved on demand through tool calls**. The agent decides when to recall, what to search for, and how much to retrieve.

This article breaks down how OpenClaw's memory strategy works and what it means for anyone building agent systems.

## Core Design: Memory as Tool Calls, Not Prompt Injection

OpenClaw's memory retrieval relies on two primary tools:

- `memory_search` — semantic search combining BM25 and vector similarity
- `memory_get` — precise retrieval of text chunks by file path and line range

The key insight:

> Memory is not "auto-injected every turn." It is searched only when needed, and only the relevant fragments are retrieved.

This delivers two immediate benefits:

1. **Token efficiency** — irrelevant history never enters the context window
2. **Agent autonomy** — the decision of when and what to recall becomes part of the agent's reasoning process

## Indexing Strategy: Beyond Chat History

One easily overlooked but critical detail: OpenClaw indexes not just conversation history, but also **workspace-generated documents**.

Any `.md` files the agent produces — notes, summaries, SOPs, articles — are chunked and added to the memory index.

Think of it like a competent colleague. When you ask "how did we handle this last time?", they don't scroll through old chat messages. They open the document they wrote about it.

This means the memory system captures:
- Raw conversation data
- Agent-generated structured outputs
- Any markdown artifacts in the workspace

## Data Model: Separated Text, Vectors, and Full-Text Search

The implementation follows a clean, production-friendly RAG data layer:

- `chunks` — stores text content with metadata (file path, line range, source)
- `chunks_vec` — stores embedding vectors
- `chunks_fts` — stores full-text search (FTS) indexes

This separation provides three critical properties:

- **Explainability** — search results trace back to specific files and line numbers
- **Tunability** — BM25/FTS and vector recall can be mixed, weighted, and reranked independently
- **Auditability** — when something goes wrong, you can inspect exactly what was indexed

## Incremental Session Indexing

OpenClaw stores session data as `.jsonl` files and performs incremental chunking:

- Monitor JSONL files for changes
- When new content crosses a threshold, read the delta and index it

An interesting design choice here: many systems use history compression (like `/compact` to generate summaries) that replaces or deletes old messages. OpenClaw keeps both the original session data and any compressed summaries as indexable sources.

The philosophy behind this:

- Memory works more like **log retrieval** than a curated persona
- Summaries are a compression tool, but they don't need to be injected into every context window

## What This Means for Agent System Design

The most important takeaway from OpenClaw's approach:

> Memory chunks are never automatically concatenated into the system prompt or per-turn context. Everything is on-demand and tool-driven. This is what it truly means to hand control to the agent.

Consider the analogy:

- **Auto-injection** is like someone reading your entire resume aloud before every sentence you speak
- **Tool-driven retrieval** is like reaching for your notebook, searching your notes, or checking a document when you actually need it

The second approach mirrors how humans work and scales far better in production.

## Practical Recommendations for Your Own Agent

If you are building a similar system, consider these patterns:

1. **Anchor long-term preferences in explicit files** — use a Profile or `MEMORY.md` that the agent can reliably reference
2. **Index agent outputs, not just conversations** — documents the agent produces are often more valuable than raw chat logs
3. **Teach the agent a retrieval workflow**:
   - First, decide whether recall is needed for this task
   - Then, determine what keywords or concepts to search
   - Finally, retrieve only the necessary fragments

## Summary

OpenClaw's memory strategy is defined by three principles: **minimal, engineered, and agent-controlled**.

- Memory is not a magic prompt — it is a searchable knowledge base
- The system does not chase automatic injection — it prioritizes retrievability and explainability

If you are building your own agent system, this tool-driven approach to memory is well worth adopting.

---

### References

- Thread: <https://x.com/Stephen4171127/status/2017224470818160658>
- OpenClaw Docs: <https://docs.openclaw.ai/>

## Related Reading

- [OpenClaw Architecture Deep Dive: How Automation Actually Works](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) — Complete pipeline from message to execution
- [OpenClaw Multi-Agent Guide: Architecture, Configuration, and Collaboration Patterns](/posts/ai/2026-02-23-openclaw-multi-agent-guide/) — Multi-agent collaboration in OpenClaw
- [AI Agent Memory Systems: RAG vs Context Engineering](/posts/ai/2026-02-21-ai-agent-memory-systems/) — Broader comparison of memory approaches
- [OpenClaw Claude Code Workflow: How One Dev Built a 100K-Star Project](/posts/ai/2026-01-31-openclaw-claude-code-workflow/) — Real workflow patterns with OpenClaw
- [RAG Pipeline Setup: Vector Database + LLM Integration Guide](/posts/ai/2026-03-01-rag-pipeline-setup/) — Build the RAG infrastructure that powers agent memory
- [QMD Local Search: Cut AI Agent Token Costs by 90%](/posts/ai/2026-03-25-qmd-local-search-ai-agent-memory/) — the local search engine behind on-demand recall, measured in tokens saved
- [Claude-Mem Deep Dive: Persistent Memory Plugin for Claude Code](/posts/ai/2026-02-03-claude-mem-deep-dive/) — the same on-demand recall idea, implemented as a Claude Code plugin
