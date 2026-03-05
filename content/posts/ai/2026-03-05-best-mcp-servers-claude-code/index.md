+++
date = '2026-03-05T10:00:00+08:00'
draft = false
title = 'Best MCP Servers for Claude Code: 18 Tools You Need in 2026'
description = 'Curated list of the best MCP servers for Claude Code in 2026. Install commands, key features, and practical use cases for 18 top MCP servers across databases, browsers, productivity, and more.'
toc = true
tags = ['Claude Code', 'MCP', 'AI Tools', 'Developer Tools']
categories = ['AI Guides']
keywords = ['best MCP servers', 'top MCP servers Claude Code', 'MCP servers list 2026', 'MCP server install', 'Claude Code MCP', 'Model Context Protocol servers']

[[params.faqItems]]
question = "How many MCP servers can I run in Claude Code at once?"
answer = "There is no hard limit, but each MCP server runs as a separate process. Running 3-5 servers has no noticeable performance impact. With 5-10 servers, startup takes slightly longer. Beyond 10, consider merging related servers or only enabling what you actively need."

[[params.faqItems]]
question = "What is the difference between project scope and user scope for MCP servers?"
answer = "Project scope (the default) makes an MCP server available only in the current project directory. User scope (--scope user) makes it available across all your projects. Use project scope for database connections and project-specific APIs. Use user scope for universal tools like GitHub, Context7, or browser automation."

[[params.faqItems]]
question = "Do MCP servers work with AI tools other than Claude Code?"
answer = "Yes. MCP is an open protocol supported by Claude Code, Claude Desktop, Cursor, Windsurf, VS Code Copilot, Cline, and many others. The same MCP server works across all compatible clients — configuration syntax differs per client, but the server code is identical."

[[params.faqItems]]
question = "Are MCP servers safe to use? Can they access my files or data?"
answer = "MCP servers only have the permissions you explicitly grant. Claude Code always asks for your permission before calling an MCP tool unless you have pre-approved it. Each server runs as a standard process — it cannot access your filesystem unless you pass directory paths as arguments."

[[params.faqItems]]
question = "How do I update an MCP server to the latest version?"
answer = "Servers installed via npx automatically fetch the latest version each time they start. To pin a specific version, append the version number: claude mcp add servername npx @package/name@2.1.0. For Docker-based servers, pull the latest image with docker pull."
+++

The MCP ecosystem has exploded. Since Anthropic open-sourced the Model Context Protocol in late 2024, the community has built over 10,000 public MCP servers, and the official SDKs have surpassed 97 million downloads across TypeScript and Python. Every major AI tool vendor now supports MCP — Anthropic, OpenAI, Google, and Microsoft have all adopted it as the standard for connecting AI agents to external tools.

But with thousands of servers available, finding the ones that actually matter is the hard part.

This guide cuts through the noise. Here are the 18 MCP servers that deliver the most value for Claude Code users in 2026, organized by category, with install commands you can copy-paste right now.

## Quick Start: How to Install MCP Servers in Claude Code

Before diving into the list, here is how MCP server installation works in Claude Code.

### The Basic Command

```bash
claude mcp add <name> <command> [args...]
```

### Adding with Environment Variables

```bash
claude mcp add <name> -e KEY=value <command> [args...]
```

### Scope Options

```bash
# Available only in the current project (default)
claude mcp add <name> npx @package/server

# Available across all your projects
claude mcp add --scope user <name> npx @package/server
```

### Managing Servers

```bash
# List all configured servers
claude mcp list

# Remove a server
claude mcp remove <name>

# Check server status inside Claude Code
/mcp
```

**Rule of thumb**: Use `--scope user` for general-purpose tools you want everywhere (GitHub, Context7, browser). Use project scope for project-specific connections (databases, internal APIs).

For a deeper walkthrough of MCP setup, configuration, and building your own servers, see our [Claude Code MCP Setup Guide](/posts/ai/2026-02-28-claude-code-mcp-setup/).

---

## Database Servers

### 1. PostgreSQL

**What it does**: Connects Claude Code directly to your PostgreSQL database. Claude can inspect schemas, write SQL queries, and return results — all without you switching to a database client.

**Install**:

```bash
claude mcp add postgres \
  npx @anthropic/mcp-postgres \
  "postgresql://user:pass@localhost:5432/mydb"
```

**Key features**:
- Read-only query execution by default (safe for production databases)
- Automatic schema introspection — Claude understands your tables and columns
- Support for parameterized queries
- Connection string passed as argument, not stored in plain text config

**When to use it**: Debugging data issues, generating reports, exploring unfamiliar databases, verifying migrations. Pair it with a read-only database user for production safety.

### 2. SQLite

**What it does**: Provides SQLite database management — querying, schema inspection, and data manipulation for local SQLite files.

**Install**:

```bash
claude mcp add sqlite \
  npx @anthropic/mcp-sqlite \
  /path/to/database.db
```

**Key features**:
- Full read/write access to SQLite databases
- Schema exploration and table management
- Works with any local `.db` file
- Lightweight — no database server required

**When to use it**: Working with mobile app databases, local development databases, embedded systems data, or any project using SQLite as its storage layer.

### 3. MySQL

**What it does**: Connects Claude Code to MySQL and MariaDB databases with the same query and schema inspection capabilities as the PostgreSQL server.

**Install**:

```bash
claude mcp add mysql \
  npx @anthropic/mcp-mysql \
  "mysql://user:pass@localhost:3306/mydb"
```

**Key features**:
- Schema introspection for MySQL-specific types
- Support for stored procedures and views
- Read-only mode available for production safety

**When to use it**: Any project backed by MySQL or MariaDB. Essential for legacy application maintenance where MySQL is the primary data store.

---

## Browser Automation

### 4. Playwright (Microsoft Official)

**What it does**: Gives Claude Code full browser automation capabilities through Microsoft's Playwright engine. Claude can navigate pages, click elements, fill forms, take screenshots, and run end-to-end test flows.

**Install**:

```bash
claude mcp add playwright \
  npx @anthropic/mcp-playwright
```

**Key features**:
- Cross-browser support: Chromium, Firefox, WebKit
- Uses accessibility tree snapshots for element interaction (more reliable than CSS selectors)
- Screenshot capture for visual verification
- Network request interception and monitoring
- Runs entirely on your local machine — no data leaves your environment

**When to use it**: Writing and debugging E2E tests, scraping web data, automating repetitive browser workflows, verifying UI changes after code modifications. This is the go-to choice for serious browser automation.

For a deeper look at browser automation options, see our [browser automation guide](/posts/ai/2026-01-28-claude-code-browser-automation/).

### 5. Fetch

**What it does**: A simpler alternative to Playwright for basic web content retrieval. Fetches URLs and converts HTML to markdown that Claude can process.

**Install**:

```bash
claude mcp add fetch \
  npx @anthropic/mcp-fetch
```

**Key features**:
- HTML to markdown conversion for clean text extraction
- Handles redirects and authentication headers
- Lightweight — no browser engine required
- Supports custom headers for authenticated endpoints

**When to use it**: When you need to read web content without full browser interaction. API documentation lookups, checking deployment status pages, or pulling content from URLs shared in conversations.

---

## Code & Version Control

### 6. GitHub (Official by GitHub)

**What it does**: Full GitHub integration — issues, pull requests, repository search, branch management, CI/CD workflows, and code review. This is GitHub's own official MCP server, not a third-party wrapper.

**Install**:

```bash
claude mcp add github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token \
  npx @anthropic/mcp-github
```

**Key features**:
- Create, read, and update issues and pull requests
- Search across repositories and code
- Trigger and monitor GitHub Actions workflows
- Branch and tag management
- Review and merge pull requests with comments

**When to use it**: Any project hosted on GitHub. This eliminates context-switching to the browser for issue tracking, PR reviews, and CI monitoring. Use `--scope user` since you likely want this everywhere.

### 7. Git

**What it does**: Provides Git operations beyond what Claude Code's built-in shell access offers — structured access to repository history, diffs, blame, and branch operations with proper error handling.

**Install**:

```bash
claude mcp add git \
  npx @anthropic/mcp-git \
  /path/to/repository
```

**Key features**:
- Structured log and diff output (easier for Claude to parse than raw git output)
- Blame analysis for tracking down code authorship
- Branch comparison and merge-base detection
- Commit history search by message, author, or date range

**When to use it**: When you need Claude to do deep repository archaeology — understanding code evolution, finding when bugs were introduced, or analyzing contribution patterns across a large codebase.

---

## Documentation & Knowledge

### 8. Context7

**What it does**: Fetches up-to-date library documentation at query time. When Claude needs to use an API it is unsure about, Context7 pulls the latest official docs instead of relying on training data that may be months or years old.

**Install**:

```bash
claude mcp add context7 \
  --scope user \
  npx @upstash/context7-mcp
```

**Key features**:
- Version-specific documentation retrieval
- Covers thousands of popular libraries and frameworks
- Two tools: `resolve-library-id` (finds the correct library) and `query-docs` (fetches documentation)
- Eliminates hallucinated APIs — Claude works from real documentation

**When to use it**: Always. This should be one of your default `--scope user` servers. It prevents Claude from inventing API calls that do not exist, especially for fast-moving libraries like Next.js, React, or LangChain where APIs change frequently.

**Pro tip**: When asking Claude about a library, add "use context7" to your prompt. Claude will automatically look up the latest docs before writing code.

### 9. Memory (Knowledge Graph)

**What it does**: Gives Claude persistent memory across conversations using a local knowledge graph. Claude can store and retrieve entities, relationships, and observations — remembering context about your project, preferences, and decisions.

**Install**:

```bash
claude mcp add memory \
  npx @anthropic/mcp-memory
```

**Key features**:
- Local knowledge graph stored as JSON
- Entities with typed relationships (person, project, concept)
- Observations attached to entities
- Persists across Claude Code sessions
- Fully local — no data sent to external services

**When to use it**: Long-running projects where you want Claude to remember architectural decisions, team member roles, coding conventions, or domain-specific terminology without re-explaining every session.

---

## AI Reasoning

### 10. Sequential Thinking

**What it does**: Introduces a structured, multi-step reasoning process for Claude. Instead of jumping to a solution, Claude breaks problems into sequential thought steps with the ability to branch, revise, and verify along the way.

**Install**:

```bash
claude mcp add sequential-thinking \
  npx @modelcontextprotocol/server-sequential-thinking
```

**Key features**:
- Step-by-step thought decomposition
- Ability to revise previous reasoning steps
- Branching for exploring alternative approaches
- Configurable depth — set minimum and maximum thought steps
- Thought logging can be disabled for cleaner output (set `DISABLE_THOUGHT_LOGGING=true`)

**When to use it**: Complex architectural decisions, debugging multi-system issues, planning large refactors, or any problem where the first intuition might be wrong. This server makes Claude's reasoning visible and auditable.

---

## Productivity & Communication

### 11. Notion

**What it does**: Connects Claude Code to your Notion workspace. Claude can search pages, read content, create new pages, update existing ones, and manage databases.

**Install**:

```bash
claude mcp add notion \
  -e NOTION_API_KEY=ntn_your_key \
  npx @anthropic/mcp-notion
```

**Key features**:
- Search across your entire Notion workspace
- Read and write page content (including rich text blocks)
- Create pages in specific databases
- Query database entries with filters and sorts
- Comment on pages for team collaboration

**When to use it**: Teams that use Notion for documentation, project management, or knowledge bases. Claude can pull requirements from Notion, update status pages after deployments, or create documentation pages from code analysis.

### 12. Slack

**What it does**: Lets Claude Code interact with your Slack workspace — read messages, post updates, search conversations, and manage channels.

**Install**:

```bash
claude mcp add slack \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e SLACK_TEAM_ID=T01234567 \
  npx @anthropic/mcp-slack
```

**Key features**:
- Read and send messages in channels and DMs
- Search message history across your workspace
- Post formatted messages with attachments
- Channel management (list, join, create)
- Thread support for organized discussions

**When to use it**: Automated notifications when Claude completes long tasks, pulling context from team discussions, or posting deployment summaries. Pairs well with [Claude Code Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) for fully automated workflows.

### 13. Linear

**What it does**: Integrates with Linear for issue tracking and project management. Claude can create issues, update statuses, search for existing tickets, and manage project workflows.

**Install**:

```bash
claude mcp add linear \
  -e LINEAR_API_KEY=lin_api_your_key \
  npx @anthropic/mcp-linear
```

**Key features**:
- Create and update issues with labels, priorities, and assignees
- Search issues by text, status, or assignee
- Project and cycle management
- Team and member lookups
- Workflow state transitions

**When to use it**: Engineering teams using Linear for project management. Claude can automatically create bug tickets from code analysis, update issue status after completing work, or search for related tickets before starting a new feature.

---

## File System & Infrastructure

### 14. Filesystem

**What it does**: The official MCP server for secure local file operations. While Claude Code has built-in file access, this server adds granular permission controls, directory tree visualization, and advanced search capabilities.

**Install**:

```bash
claude mcp add filesystem \
  npx @anthropic/mcp-filesystem \
  /path/to/allowed/directory
```

**Key features**:
- Read, write, and edit files within allowed directories
- Directory tree visualization
- File search by name or content patterns
- Granular permission boundaries — only the directories you specify
- Symlink-aware operations

**When to use it**: When you need strict filesystem sandboxing or when working across multiple project directories. The directory argument acts as a security boundary — Claude cannot access files outside the specified paths.

### 15. Docker

**What it does**: Manages Docker containers, images, volumes, and networks directly from Claude Code. Claude can build images, start containers, inspect logs, and manage Docker Compose stacks.

**Install**:

```bash
claude mcp add docker \
  npx @anthropic/mcp-docker
```

**Key features**:
- Container lifecycle management (create, start, stop, remove)
- Image building and management
- Log inspection and container exec
- Docker Compose stack operations
- Volume and network management

**When to use it**: Microservice development, debugging container issues, managing local development environments, or automating Docker workflows. Especially useful when you need to inspect running containers while debugging application issues.

---

## Cloud & Infrastructure

### 16. AWS Documentation

**What it does**: Provides Claude Code with access to official AWS documentation. Claude can search and read AWS service docs, getting accurate configuration details, API references, and best practices.

**Install**:

```bash
claude mcp add aws-docs \
  npx @awslabs/aws-documentation-mcp-server
```

**Key features**:
- Search across all AWS service documentation
- Read specific documentation pages
- Service-specific recommendations
- Always up-to-date — pulls from live AWS docs

**When to use it**: Any project using AWS services. Eliminates guesswork about IAM policies, CloudFormation templates, Lambda configurations, and other AWS-specific details where getting the syntax exactly right matters.

### 17. Cloudflare

**What it does**: Manages Cloudflare Workers, KV stores, R2 buckets, and DNS records. Claude can deploy edge functions, configure caching rules, and manage your Cloudflare infrastructure.

**Install**:

```bash
claude mcp add cloudflare \
  -e CLOUDFLARE_API_TOKEN=your_token \
  npx @anthropic/mcp-cloudflare
```

**Key features**:
- Workers deployment and management
- KV namespace operations (read, write, list, delete)
- R2 object storage management
- DNS record configuration
- Zone and domain management

**When to use it**: Projects deployed on Cloudflare's edge platform. Claude can deploy Workers, update KV stores, manage R2 buckets, and configure DNS — all without leaving the terminal.

---

## Monitoring & Observability

### 18. Sentry

**What it does**: Connects Claude Code to your Sentry error tracking. Claude can search for errors, inspect stack traces, analyze error trends, and help debug production issues with full context.

**Install**:

```bash
claude mcp add sentry \
  -e SENTRY_AUTH_TOKEN=your_token \
  -e SENTRY_ORG=your-org \
  npx @anthropic/mcp-sentry
```

**Key features**:
- Search and filter error events
- Inspect detailed stack traces with source context
- Analyze error frequency and trends
- Link errors to specific releases and commits
- Issue assignment and status management

**When to use it**: Debugging production errors. Instead of switching to the Sentry dashboard, Claude can pull error details, analyze the stack trace alongside your codebase, and suggest fixes with full context of both the error and the code.

---

## My Recommended Setup

Here is the MCP configuration I use daily across all projects. These five servers cover 90% of typical development needs:

```bash
# Universal tools (user scope — available everywhere)
claude mcp add --scope user github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx \
  npx @anthropic/mcp-github

claude mcp add --scope user context7 \
  npx @upstash/context7-mcp

claude mcp add --scope user playwright \
  npx @anthropic/mcp-playwright

claude mcp add --scope user sequential-thinking \
  npx @modelcontextprotocol/server-sequential-thinking

claude mcp add --scope user fetch \
  npx @anthropic/mcp-fetch
```

Then per-project, I add whatever the project needs:

```bash
# Project-specific database
claude mcp add postgres \
  npx @anthropic/mcp-postgres \
  "postgresql://dev:password@localhost:5432/myapp"

# Project-specific integrations
claude mcp add slack \
  -e SLACK_BOT_TOKEN=xoxb-xxx \
  -e SLACK_TEAM_ID=T01234567 \
  npx @anthropic/mcp-slack
```

Verify everything is connected:

```bash
claude mcp list
```

Inside Claude Code, run `/mcp` to confirm all servers are running and their tools are available.

## How to Choose the Right MCP Servers

Not every project needs all 18 servers. Here is a decision framework:

| If you... | Install these |
|-----------|--------------|
| Work with any GitHub repo | GitHub |
| Use any database | PostgreSQL, MySQL, or SQLite |
| Need accurate library docs | Context7 |
| Write or debug E2E tests | Playwright |
| Use Slack for team communication | Slack |
| Manage issues in Linear | Linear |
| Work with AWS infrastructure | AWS Documentation |
| Debug production errors in Sentry | Sentry |
| Need Claude to remember context | Memory |
| Tackle complex architectural decisions | Sequential Thinking |

**Start small.** Install two or three servers that match your daily workflow, learn how they work, and add more as you identify gaps. Running too many servers that you rarely use just adds startup overhead.

## Where to Find More MCP Servers

The 18 servers in this guide are the ones I have personally used and found valuable. But the ecosystem is vast and growing fast:

- **[Official MCP Servers](https://github.com/modelcontextprotocol/servers)** — Reference implementations maintained by Anthropic
- **[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — Community-curated list with 1,800+ servers
- **[MCP Registry](https://www.claudemcp.com/servers)** — Searchable directory of published servers
- **[Smithery](https://smithery.ai)** — MCP server marketplace with one-click install
- **[PulseMCP](https://www.pulsemcp.com)** — Server discovery with reviews and ratings

New servers are being published daily. The categories growing fastest in 2026 are AI agent orchestration, enterprise SaaS integrations (Salesforce, HubSpot, Zendesk), and infrastructure-as-code tools.

## Related Reading

- [Claude Code MCP Setup Guide](/posts/ai/2026-02-28-claude-code-mcp-setup/) — Complete walkthrough of installing, configuring, and building MCP servers
- [Building MCP Servers with TypeScript](/posts/ai/2026-03-02-building-mcp-servers-typescript/) — Create your own MCP server from scratch
- [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) — Technical deep dive into how MCP works under the hood
- [MCP Security Guide](/posts/ai/2026-02-23-mcp-security-guide/) — Best practices for running MCP servers safely
- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — Everything you need to know about Claude Code
