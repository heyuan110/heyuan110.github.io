+++
date = '2026-03-25T10:00:00+08:00'
draft = false
title = 'QMD: Local Semantic Search That Cuts AI Agent Token Costs by 90%'
description = 'Learn how QMD, a local hybrid search engine by Shopify founder Tobi Lütke, dramatically reduces AI agent token consumption through intelligent memory retrieval with BM25, vector search, and LLM reranking.'
toc = true
tags = ['AI Agent', 'MCP', 'Token Optimization', 'RAG']
keywords = ['qmd search engine', 'AI agent token optimization', 'local semantic search', 'MCP server memory', 'reduce AI token costs']
+++

![QMD local semantic search engine for AI agent memory optimization](cover.webp)

Every AI agent developer hits the same wall: **token costs spiral out of control** as conversations grow longer. You feed your agent a 2,000-token memory file, a 3,000-token project context, and a 1,500-token conversation history — suddenly you're burning through your API budget just to answer a simple question.

The root cause? Agents treat memory like a firehose. They dump everything into the context window and hope the LLM figures out what matters. This is like reading an entire encyclopedia to answer "What's the capital of France?"

**QMD** solves this by acting as a precision scalpel for agent memory. Instead of feeding everything into context, QMD searches your local documents and returns only the relevant paragraphs — cutting token usage by 90% while actually improving accuracy.

## What Is QMD and Why Should You Care?

[QMD](https://github.com/tobi/qmd) (Query Markup Documents) is a local search engine built by [Tobi Lütke](https://x.com/tobi), co-founder and CEO of Shopify. It's written in TypeScript, runs entirely on your machine, and combines three search techniques into one pipeline:

| Layer | Technique | What It Does |
|-------|-----------|--------------|
| 1 | **BM25 Full-Text Search** | Fast keyword matching — finds exact terms |
| 2 | **Vector Semantic Search** | Embedding-based similarity — understands meaning |
| 3 | **LLM Reranking** | Context-aware ordering — picks the best results |

All three layers run locally via [node-llama-cpp](https://github.com/withcatai/node-llama-cpp) with GGUF models. No API calls. No cloud. No cost per query.

Think of it like this: BM25 is a librarian who finds books by title. Vector search is a librarian who understands your question and finds related books even if the titles don't match. LLM reranking is a senior librarian who reviews both lists and puts the most helpful books on top.

### The Three Default Models

QMD ships with three carefully chosen GGUF models:

| Model | Purpose | Size |
|-------|---------|------|
| `embeddinggemma-300M-Q8_0.gguf` | Embedding generation | ~300MB |
| `qwen3-reranker-0.6b-q8_0.gguf` | Result reranking | ~600MB |
| `qmd-query-expansion-1.7B-q4_k_m.gguf` | Query expansion | ~1GB |

These models are downloaded automatically on first run and cached at `~/.cache/qmd/models/`. Total disk footprint is under 2GB — a small price for unlimited, free semantic search.

## How the Hybrid Search Pipeline Works

Understanding QMD's search pipeline helps you tune it for better results. Here's what happens when you run `qmd query "how to handle authentication"`:

### Step 1: Query Expansion

The query expansion model generates multiple sub-queries from your original question:

- **Lexical sub-query**: `"authentication" "auth" "login" "token"` (for BM25)
- **Semantic sub-query**: `"user identity verification and session management"` (for vector search)
- **HyDE sub-query**: A hypothetical document that would answer the question (for better embedding matching)

This is critical because a single query rarely captures all the ways a concept might be expressed in your documents.

### Step 2: Parallel Retrieval

Both search backends run simultaneously:

```
Original Query (×2 weight) + Expanded Queries
         ↓                        ↓
    BM25 Search              Vector Search
         ↓                        ↓
    Keyword Matches         Semantic Matches
         ↓                        ↓
         └──────── RRF Fusion ────┘
                      ↓
              Top-30 Candidates
```

**Reciprocal Rank Fusion (RRF)** merges the two result lists. Documents that appear in both lists get boosted. The original query receives 2× weight to prevent expanded queries from drowning out exact matches.

### Step 3: LLM Reranking

The top 30 candidates go through the Qwen3 reranker, which reads each document chunk and scores how relevant it is to your question. This catches cases where keyword matching found a document that mentions your terms but isn't actually relevant.

The final output uses **position-aware blending** — it balances the reranker's judgment against the retrieval scores to prevent the reranker from destroying high-confidence keyword matches.

### Smart Document Chunking

Most search tools split documents at fixed token boundaries (every 512 tokens, for example). This often cuts paragraphs, code blocks, or sections in half — destroying context.

QMD uses a scoring algorithm to find **natural markdown break points**. It keeps semantic units together:

- Complete paragraphs stay intact
- Code blocks are never split mid-function
- Heading + body sections remain as units

This means search results are immediately useful without needing surrounding context.

## Installation and Setup

### Prerequisites

You need [Bun](https://bun.sh/) (or Node.js 20+). Bun is recommended for faster installation and runtime:

```bash
# Install Bun (if not already installed)
curl -fsSL https://bun.sh/install | bash

# Install QMD globally
bun install -g @tobilu/qmd
```

On first run, QMD downloads the three GGUF models (~2GB total). After that, everything runs offline.

### Creating Your First Collection

A "collection" is a directory of documents that QMD indexes. Let's say you have a project with markdown notes:

```bash
# Navigate to your project
cd ~/my-project

# Register a collection
qmd collection add ./docs --name project-docs --mask "**/*.md"

# Generate embeddings (required for semantic search)
qmd embed

# Check status
qmd status
```

The `--mask` flag supports glob patterns. Common examples:

```bash
# Index all markdown files
qmd collection add ./notes --name notes --mask "**/*.md"

# Index TypeScript source code
qmd collection add ./src --name source --mask "**/*.ts"

# Index everything except node_modules
qmd collection add . --name all --mask "**/*" --ignore "node_modules/**"
```

### Adding Context (Optional but Powerful)

Context is metadata that helps QMD understand what each collection contains. This improves search relevance significantly:

```bash
# Add descriptions to collections
qmd context add qmd://project-docs "Technical documentation for the authentication service"
qmd context add qmd://notes "Daily development notes and meeting minutes"
```

Context forms a hierarchical tree and is returned alongside search results — giving your AI agent extra signal about where information came from.

## Three Search Modes Compared

QMD offers three search modes, each with different speed/accuracy tradeoffs:

### 1. Lexical Search (`qmd search`)

Fast BM25 keyword matching. Best for finding specific terms:

```bash
# Find documents mentioning "rate limit"
qmd search "rate limit"

# Search within a specific collection
qmd search "rate limit" -c project-docs

# Output as JSON (for scripts)
qmd search "rate limit" --json
```

**Speed**: < 10ms
**Best for**: Known terms, error messages, function names

### 2. Semantic Search (`qmd vsearch`)

Vector embedding similarity. Finds related documents even when exact keywords don't match:

```bash
# Find documents about throttling (even if they don't say "rate limit")
qmd vsearch "how to prevent API abuse"
```

**Speed**: 50-200ms
**Best for**: Conceptual queries, "how to" questions

### 3. Hybrid Search (`qmd query`)

The full pipeline — lexical + semantic + query expansion + reranking:

```bash
# Maximum accuracy search
qmd query "best practices for handling authentication tokens"

# Show all results with scores
qmd query "auth tokens" --all --min-score 0.4
```

**Speed**: 200-500ms
**Best for**: Complex questions, agent memory retrieval

### Output Formats for Agent Integration

QMD supports machine-readable output for seamless agent integration:

```bash
# JSON output with scores and metadata
qmd query "deployment process" --json -n 5

# File paths only (for piping to other tools)
qmd query "deployment" --files
```

## MCP Integration: Give Your Agent a Memory Brain

This is where QMD transforms from a CLI tool into an agent superpower. By exposing QMD as an [MCP server](/posts/ai/2026-02-20-mcp-protocol-guide/), your AI agent can search your documents on demand — pulling only what's relevant into context.

### Setting Up the MCP Server

**For Claude Code** (recommended):

Add to your `.claude/settings.json` or project MCP config:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

**For other MCP-compatible agents**, the same configuration pattern applies — just adapt the config file format.

### What Tools Does the MCP Server Expose?

| Tool | Description |
|------|-------------|
| `query` | Hybrid search with full pipeline |
| `get` | Retrieve a specific document by path or ID |
| `multi_get` | Batch retrieve multiple documents |
| `status` | Check index health and collection info |

### HTTP Transport (Shared Daemon)

For setups where multiple agents need simultaneous access:

```bash
# Start QMD as a long-lived HTTP server
qmd mcp --http --port 8181

# Run as a background daemon
qmd mcp --http --daemon

# Check health
curl http://localhost:8181/health

# Stop the daemon
qmd mcp stop
```

The HTTP server keeps models loaded in VRAM across requests — eliminating cold-start latency. Embedding contexts are disposed after 5 minutes of inactivity to free memory.

## Real-World Impact: Before vs. After

### Scenario 1: Agent Memory Recall

**Before QMD**: Agent loads entire `MEMORY.md` (2,000 tokens) + `CLAUDE.md` (1,500 tokens) + recent conversation logs (3,000 tokens) = **6,500 tokens** per request, regardless of relevance.

**After QMD**: Agent queries "user's preferred testing framework" → QMD returns the 3 most relevant paragraphs = **~200 tokens**. That's a **97% reduction**.

### Scenario 2: Cross-File Knowledge Retrieval

**Before QMD**: Agent reads 5 files trying to find where authentication is configured = **~8,000 tokens** of file reading.

**After QMD**: `qmd query "authentication configuration"` → returns the exact section from the right file = **~300 tokens**. Plus the agent now has a confidence score for the result.

### Scenario 3: Project Context Loading

**Before QMD**: Agent loads project README, architecture docs, and coding standards every conversation = **~5,000 tokens** of boilerplate context.

**After QMD**: Agent only queries for context relevant to the current task. Writing a database migration? QMD returns only the database-related sections = **~500 tokens**.

## Advanced Configuration

### Re-indexing After Changes

When your documents change, update the index:

```bash
# Rescan all collections and update
qmd update

# Force re-embed all documents (needed when switching models)
qmd embed -f
```

### SDK Integration (Programmatic Access)

For building custom tools or integrations:

```typescript
import { QMDStore } from '@tobilu/qmd';

const store = new QMDStore();

// Add a collection programmatically
await store.addCollection("my-docs", {
  path: "/path/to/docs",
  pattern: "**/*.md",
  ignore: ["node_modules/**"]
});

// Hybrid search
const results = await store.search({
  queries: [
    { type: 'lex', query: '"connection pool" timeout' },
    { type: 'vec', query: 'why connections timeout under load' }
  ]
});

// Direct backend access
const lexResults = await store.searchLex("exact phrase");
const vecResults = await store.searchVector("semantic meaning");
```

### Performance Tuning Tips

1. **Keep collections focused**: Index only what your agent needs. A collection of 100 targeted markdown files outperforms 10,000 random files.

2. **Use context descriptions**: They give the search pipeline hints about collection purpose, improving relevance scoring.

3. **Prefer `query` over `vsearch` for agents**: The full hybrid pipeline with reranking consistently outperforms pure vector search.

4. **Monitor with `qmd status`**: Check document counts, embedding coverage, and collection health regularly.

## QMD vs. Other Approaches

| Approach | Token Cost | Accuracy | Latency | Setup Complexity |
|----------|-----------|----------|---------|-----------------|
| **Full context loading** | Very High | Low (noise) | None | None |
| **Cloud RAG (Pinecone, Weaviate)** | API costs | High | 100-500ms | High |
| **Mem0** | API costs | High | Variable | Medium |
| **QMD (local hybrid)** | **Zero** | **Very High** | 200-500ms | **Low** |

QMD's killer advantage: **zero ongoing cost**. Once installed, every query is free. For developers running AI agents 8+ hours per day, the savings compound fast.

## Common Pitfalls and Troubleshooting

### "qmd embed" is slow on first run

First-time embedding downloads GGUF models (~2GB). Subsequent runs only embed new or changed documents — typically completing in seconds.

### Vector search returns unexpected results

Make sure you've run `qmd embed` after adding new documents. Unembedded documents only appear in lexical (`search`) results.

### Switching embedding models

If you change the embedding model, you **must** re-embed with `qmd embed -f`. Vectors from different models are not compatible.

### MCP connection issues with Claude Code

Verify the `command` path resolves correctly:

```bash
# Check where qmd is installed
which qmd

# Use the full path in MCP config if needed
{
  "mcpServers": {
    "qmd": {
      "command": "/Users/yourname/.bun/bin/qmd",
      "args": ["mcp"]
    }
  }
}
```

## FAQ

**Q: Does QMD work with non-Markdown files?**
A: QMD is optimized for Markdown but can index any text file. Its smart chunking works best with structured Markdown (headings, paragraphs, code blocks).

**Q: How much disk space does QMD need?**
A: The three GGUF models total ~2GB. The SQLite index is typically tiny — a few MB even for thousands of documents.

**Q: Can I use QMD without an AI agent?**
A: Absolutely. QMD works great as a standalone CLI search tool for your notes, docs, and knowledge base.

**Q: Does QMD support GPU acceleration?**
A: Yes, through node-llama-cpp. If you have a compatible GPU, embedding and reranking will be faster. CPU-only works fine for most use cases.

**Q: How does QMD compare to RAG pipelines?**
A: QMD essentially _is_ a local RAG pipeline — but packaged as a single CLI tool. No vector database setup, no embedding API costs, no infrastructure to maintain.

## Related Reading

- [MCP Protocol Explained: Connect AI Agents to Any Tool](/posts/ai/2026-02-20-mcp-protocol-guide/) — Understanding the protocol QMD uses for agent integration
- [AI Agent Memory Systems: Architecture and Best Practices](/posts/ai/2026-02-21-ai-agent-memory-systems/) — Broader context on memory management approaches
- [Context Engineering Deep Dive: Beyond Prompt Engineering](/posts/ai/2026-02-24-context-engineering-deep-dive/) — Why what goes into context matters more than how you ask
- [OpenClaw Multi-Agent Setup Guide](/posts/ai/2026-03-05-openclaw-multi-agent-setup/) — Using QMD with OpenClaw for multi-agent workflows
- [Best MCP Servers for Claude Code in 2026](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — QMD alongside other essential MCP servers
- [RAG Pipeline Setup: From Zero to Production](/posts/ai/2026-03-01-rag-pipeline-setup/) — Compare QMD's approach with traditional RAG architectures
