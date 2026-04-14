+++
date = '2026-03-06T14:00:00+08:00'
draft = false
title = 'OpenClaw Tavily Search: ClawHub Skill Integration Guide (2026)'
description = 'The clawhub tavily-search skill gives OpenClaw agents web search in minutes. Step-by-step install via clawdhub, API key setup, per-agent config, and cost control.'
toc = true
tags = ['OpenClaw', 'Tavily', 'AI Agents', 'Web Search', 'ClawHub']
categories = ['AI Guides']
keywords = ['openclaw tavily', 'openclaw clawhub skill tavily-search', 'clawhub tavily-search', 'openclaw clawhub skill', 'tavily-search skill install', 'tavily integration openclaw', 'tavily api openclaw', 'openclaw web search', 'tavily-search skill', 'openclaw tavily setup', 'openclaw ai agent framework 2026', 'tavily-extract', 'tavily-crawl']

[[params.faqItems]]
question = "What is the clawhub tavily-search skill?"
answer = "The clawhub tavily-search skill is the official OpenClaw ClawHub package that wraps Tavily's AI-optimized Search API. It lives under clawhub/skills/tavily-search/SKILL.md, exposes parameters like query, max_results, search_depth ('basic' or 'advanced'), and include_domains, and lets any OpenClaw agent perform real-time web search without writing custom code. It is the standard web-search integration for the OpenClaw AI agent framework in 2026."

[[params.faqItems]]
question = "How do I install the tavily-search skill via clawhub?"
answer = "Run 'clawdhub install tavily-search' (note the 'd' in clawdhub — the CLI is clawdhub but the registry is clawhub). This pulls the skill from ClawHub into ~/.openclaw/workspace/skills/tavily-search/. Then export TAVILY_API_KEY='tvly-...' in your shell profile (or add it to openclaw.json's skills.entries.tavily-search.env block), restart the gateway with 'openclaw restart', and verify with 'openclaw skills list' — the tavily-search SKILL.md path should appear in the output."

[[params.faqItems]]
question = "How do I add Tavily search to OpenClaw?"
answer = "Install the tavily-search skill with 'clawdhub install tavily-search', get a free API key from tavily.com, and set the TAVILY_API_KEY environment variable. Restart your OpenClaw gateway and the agent can immediately start searching the web."

[[params.faqItems]]
question = "Is Tavily free to use with OpenClaw?"
answer = "Tavily offers a free Researcher tier with 1,000 API credits per month, no credit card required. A basic search costs 1 credit, an advanced search costs 2 credits. Paid plans start at $30/month for 4,000 credits."

[[params.faqItems]]
question = "What is the difference between tavily-search, tavily-extract, and tavily-crawl?"
answer = "tavily-search performs AI-optimized web searches and returns structured snippets. tavily-extract pulls the full cleaned text from a specific URL. tavily-crawl systematically extracts content from multiple pages on a website. Most OpenClaw users only need tavily-search for general research."

[[params.faqItems]]
question = "Can I assign Tavily to specific OpenClaw agents only?"
answer = "Yes. In your openclaw.json config, use the tools.allow and tools.deny arrays per agent to control which agents can access tavily-search. This lets you give search access to a research agent while keeping it away from a coding agent that does not need it."

[[params.faqItems]]
question = "Why does my OpenClaw agent make up information instead of searching?"
answer = "The most common cause is an expired or missing Tavily API key. OpenClaw agents silently fall back to generating answers from training data when the search tool fails. Check your TAVILY_API_KEY, verify your free tier credits have not been exhausted, and add a rule in your agent's system prompt requiring it to report search failures explicitly."
+++

![OpenClaw Tavily integration guide for AI agent web search setup](cover.webp)

Your OpenClaw agent is smart, but it is blind. Without web search, it generates answers from training data alone — which means confident-sounding responses built on outdated or fabricated information. Ask it about yesterday's news and it will either admit ignorance or, worse, invent something plausible.

[Tavily](https://tavily.com/) fixes this. It is an AI-optimized search API that returns clean, structured results designed specifically for AI agents — not the noisy HTML pages a human would browse. Integrating Tavily into [OpenClaw](https://github.com/openclaw/openclaw) gives your agent real-time access to the web, turning it from a knowledge-limited chatbot into a research-capable assistant.

This guide walks you through the complete OpenClaw Tavily integration: getting your API key, installing the skill, configuring it per agent, choosing the right Tavily tool for each job, and keeping costs under control.

## Why Your OpenClaw Agent Needs Web Search

Think of an AI agent without web search like a brilliant employee locked in a windowless room. They know everything they were trained on, but they have zero visibility into what is happening right now. That means:

- **No current events**: Cannot tell you what happened today in tech, finance, or any other domain
- **No fact-checking**: Cannot verify if a claim is accurate against current sources
- **No price tracking**: Cannot check product pricing, stock prices, or competitor rates
- **No documentation lookups**: Cannot read the latest API docs, release notes, or changelogs

With Tavily connected, your OpenClaw agent can search the web, read extracted content, and synthesize results in seconds. The difference is not incremental — it is the difference between guessing and knowing.

### Why Tavily Over Other Search APIs

You could use Google Custom Search, Bing API, Brave Search, or SerpAPI. But there is a reason Tavily dominates the OpenClaw ecosystem:

| Feature | Tavily | Google/Bing APIs | Brave Search |
|---------|--------|-----------------|--------------|
| **Optimized for AI agents** | Yes — returns structured snippets | No — returns raw HTML/links | Partially |
| **AI-generated summaries** | Included in responses | Not available | Not available |
| **Relevance scoring** | 0-1 score per result | Not available | Not available |
| **Free tier** | 1,000 credits/month | Limited or paid | 2,000 queries/month |
| **OpenClaw integration** | Official ClawHub skill | Manual setup required | Community skill |
| **Domain filtering** | Built-in include/exclude | Custom implementation | Limited |

Tavily was built from the ground up for LLM consumption. Instead of dumping raw web pages on your agent, it delivers pre-processed, relevant snippets with metadata. Your agent spends fewer tokens parsing results and produces better answers.

## Getting Your Tavily API Key

Before installing anything, you need a Tavily API key. The free tier gives you 1,000 credits per month — enough for most personal use.

**Step 1**: Go to [tavily.com](https://tavily.com/) and click "Get Started" or "Sign Up"

**Step 2**: Create an account (email or GitHub login)

**Step 3**: Navigate to your dashboard and copy your API key. It starts with `tvly-`

**Step 4**: Store the key securely. You will need it in the next section.

### Tavily Pricing Overview

Understanding the credit system helps you plan usage:

| Plan | Credits/Month | Cost | Per Credit |
|------|--------------|------|------------|
| **Researcher** (free) | 1,000 | $0 | Free |
| **Project** | 4,000 | $30/month | $0.0075 |
| **Bootstrap** | 15,000 | $100/month | $0.0067 |
| **Startup** | 38,000 | $220/month | $0.0058 |
| **Growth** | 100,000 | $500/month | $0.005 |
| **Pay-as-you-go** | Per use | $0.008/credit | $0.008 |

**Credit costs by operation**:
- Basic search: **1 credit**
- Advanced/deep search: **2 credits**
- Extract (per 5 URLs): **1 credit** (basic) or **2 credits** (advanced)
- Map (per 10 pages): **1 credit**

Important: unused credits do **not** roll over. If you use 300 credits this month, the remaining 700 disappear when the month resets.

## Installing Tavily Search in OpenClaw

### Prerequisites

Make sure you have:

1. **OpenClaw installed and running** — If not, follow the [OpenClaw Setup Guide](/posts/ai/2026-03-05-openclaw-setup-guide/) first
2. **ClawdHub CLI installed** — The package manager for OpenClaw skills
3. **Node.js 20+** — Required by the tavily-search skill

If you do not have ClawdHub CLI yet:

```bash
# Install ClawdHub globally (note: it's clawdhub with a 'd')
npm i -g clawdhub

# Verify installation
clawdhub --version
```

> A common mistake: many tutorials write `clawhub` (without the 'd'). The correct command is **`clawdhub`**. See [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) for more on this naming confusion.

### Step 1: Install the Skill

```bash
# Install tavily-search from ClawHub
clawdhub install tavily-search
```

This downloads the skill to your workspace's `skills/` directory (typically `~/.openclaw/workspace/skills/tavily-search/`). OpenClaw loads new skills automatically on the next session start.

### Step 2: Set Your API Key

You have two options for providing the API key.

**Option A: Environment variable (recommended)**

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, or equivalent):

```bash
# Add your Tavily API key
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxx"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

If you run OpenClaw as a background daemon (via `launchd` or `systemd`), make sure the environment variable is available to the daemon process. On macOS with `launchd`:

```bash
# Set environment variable for launchd
launchctl setenv TAVILY_API_KEY "tvly-xxxxxxxxxxxxxxxx"
```

**Option B: OpenClaw config file**

Add the API key directly to `~/.openclaw/openclaw.json`:

```json5
{
  "skills": {
    "entries": {
      "tavily-search": {
        "enabled": true,
        "env": {
          "TAVILY_API_KEY": "tvly-xxxxxxxxxxxxxxxx"
        }
      }
    }
  }
}
```

Option A is more secure because you do not have the key in a config file that might accidentally get shared. Option B is simpler if you manage everything through the OpenClaw config.

### Step 3: Verify the Installation

Restart your OpenClaw gateway:

```bash
# If running as a daemon
openclaw restart

# If running manually
# Stop the current gateway (Ctrl+C) and start again
openclaw gateway
```

Then send your agent a test message through Telegram, WhatsApp, or the TUI:

```
Search for the latest news about AI agents today
```

If the agent returns current, dated results with source URLs, Tavily is working. If it gives you generic information without sources, check the troubleshooting section below.

## Configuring Tavily for Specific Agents

Not every agent needs web search. A coding agent that refactors your Python code has no use for Tavily. A research agent that monitors competitors cannot function without it.

OpenClaw lets you control tool access per agent through the `tools.allow` and `tools.deny` arrays in `openclaw.json`.

### Example: Research Agent Gets Search, Coding Agent Does Not

```json5
{
  "agents": {
    "list": [
      {
        "id": "researcher",
        "tools": {
          // Only give this agent search and read access
          "allow": ["tavily-search", "browser", "read"],
          "deny": ["exec", "write"]
        }
      },
      {
        "id": "coder",
        "tools": {
          // Coding agent gets execution but no search
          "allow": ["exec", "read", "write"],
          "deny": ["tavily-search", "browser"]
        }
      },
      {
        "id": "writer",
        "tools": {
          // Writer gets search for fact-checking, but no execution
          "allow": ["tavily-search", "read"],
          "deny": ["exec", "write"]
        }
      }
    ]
  }
}
```

This configuration follows the **principle of least privilege**: each agent only has access to the tools it actually needs. Your research agent can search the web but cannot execute shell commands. Your coding agent can run code but cannot waste Tavily credits on unnecessary searches.

For a deeper dive into agent-specific configurations, see the [OpenClaw Multi-Agent Setup Guide](/posts/ai/2026-03-05-openclaw-multi-agent-setup/).

### Giving All Agents Search Access

If you run a single agent or want every agent to have Tavily access, you do not need per-agent tool configuration. Simply installing the skill and setting the API key makes it available to all agents by default.

The only reason to explicitly configure tool access is when you want to **restrict** certain agents from using search.

## Using Tavily Search: Commands and Options

Once installed, your agent can use Tavily through natural language. You do not need to type commands — the agent calls the search tool internally. But understanding the available options helps you give better instructions.

### Basic Search

Just ask your agent to search for something:

```
Search for the best practices for running OpenClaw on a Mac Mini
```

The agent calls Tavily with default settings: 5 results, basic search depth, general topic.

### Deep Research Mode

For complex topics that need comprehensive coverage, tell your agent to do a deep search:

```
Do a deep search on the latest MCP protocol changes in March 2026
```

Behind the scenes, this uses the `--deep` flag, which enables Tavily's advanced search mode. It takes longer (5-10 seconds vs 1-2 seconds) but returns broader, more thorough results. Each deep search costs **2 credits** instead of 1.

### News-Focused Search

For current events, specify the news topic:

```
Search for AI news from the last 3 days
```

This triggers `--topic news` with `--days 3`, limiting results to recent news articles. Particularly useful for daily briefings — if you have [proactive-agent](https://clawhub.ai/halthelobster/proactive-agent) installed, you can schedule these automatically.

### Controlling Result Count

By default, Tavily returns 5 results. You can request more:

```
Search for "OpenClaw security best practices" and give me 15 results
```

The agent uses the `-n 15` flag. Maximum is 20 results per query. More results mean more context for the agent but also more tokens consumed.

### Domain Filtering

You can direct your agent to search only specific domains or exclude certain ones:

```
Search for Python async tutorials, only from python.org and realpython.com
```

Or exclude low-quality sources:

```
Search for AI agent frameworks, exclude Pinterest and Medium
```

Domain filtering is powerful for research tasks where you need authoritative sources. Use **include domains** for:
- Academic research (`.edu` domains)
- Official documentation sites
- Known industry authorities

Use **exclude domains** for:
- Content farms and SEO spam
- Sites with paywalls
- Irrelevant platforms (Pinterest for non-visual queries)

### Summary of Tavily Search Flags

| Flag | What It Does | Credit Cost | When to Use |
|------|-------------|-------------|-------------|
| (default) | Basic search, 5 results | 1 credit | Quick facts, simple lookups |
| `--deep` | Advanced search, more comprehensive | 2 credits | Complex research, thorough analysis |
| `--topic news` | News-only results | 1 credit | Current events, breaking news |
| `--days <n>` | Limit news to last n days | 1 credit | Recent news filtering |
| `-n <count>` | Number of results (max 20) | 1 credit | When you need more sources |

## Tavily-Search vs Tavily-Extract vs Tavily-Crawl

Tavily offers three distinct tools. The `tavily-search` skill on ClawHub includes search and extract capabilities. Understanding when to use each saves credits and improves results.

### Tavily-Search: Find Information

**What it does**: Sends a query to Tavily's search API and returns structured results with titles, URLs, content snippets, and relevance scores.

**When to use it**: Answering questions, fact-checking, market research, finding current information.

```
"What are the top AI agent frameworks in March 2026?"
→ Returns 5 structured results with snippets and source URLs
```

**Cost**: 1 credit (basic) or 2 credits (advanced)

### Tavily-Extract: Read a Specific Page

**What it does**: Takes a URL and returns the full, cleaned text content of that page. No HTML noise — just the readable text.

**When to use it**: Reading a specific article, extracting data from a known page, pulling documentation content.

```
"Extract the content from https://docs.tavily.com/documentation/api-credits"
→ Returns the complete page text, cleaned of HTML/CSS/JS
```

**Cost**: 1 credit per 5 URLs (basic) or 2 credits per 5 URLs (advanced)

### Tavily-Crawl: Scrape a Whole Site

**What it does**: Combines Tavily's Map API (to discover pages on a site) with Extract (to pull content from each page). Systematically collects content from an entire website or section.

**When to use it**: Building a knowledge base from a documentation site, competitive analysis of a company website, collecting all articles from a blog.

```
"Crawl the OpenClaw documentation site and summarize the key features"
→ Maps the site structure, extracts pages, returns combined content
```

**Cost**: Map (1 credit per 10 pages) + Extract (1 credit per 5 URLs) combined

### Which One Should You Use?

For 90% of OpenClaw use cases, **tavily-search is all you need**. Here is the decision framework:

| I want to... | Use | Example |
|--------------|-----|---------|
| Answer a question about something | `tavily-search` | "What is the latest Claude API pricing?" |
| Read a specific webpage | `tavily-extract` | "Read this blog post: [URL]" |
| Collect data from an entire site | `tavily-crawl` | "Scrape all pricing pages from competitor.com" |
| Monitor news on a topic | `tavily-search --topic news` | "AI funding news this week" |
| Deep-dive research on a complex topic | `tavily-search --deep` | "Compare all MCP server implementations" |

## Practical Use Cases

### 1. Daily News Briefing

Combine Tavily with [proactive-agent](https://clawhub.ai/halthelobster/proactive-agent) for automated daily briefings:

```
Every morning at 8:00 AM, search for the top 5 AI news stories,
summarize each in 2-3 sentences, and send me the summary here.
```

OpenClaw schedules this as a cron job. Each morning the agent runs a Tavily search, processes the results, and sends you a digest via Telegram or WhatsApp. Cost: approximately 1-2 credits per day.

### 2. Competitor Monitoring

```
Every Monday, search for mentions of [CompetitorName] in tech news
from the past 7 days. Summarize any product launches, pricing changes,
or partnerships.
```

This gives you a weekly competitive intelligence report without lifting a finger.

### 3. Research Before Writing

If you use OpenClaw to draft content (see [OpenClaw + Claude Code Workflow](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)), Tavily ensures your agent writes from current facts, not stale training data:

```
Research the current state of AI agent frameworks in 2026.
Include market leaders, open-source options, and recent developments.
Then write a 1000-word article based on your findings.
```

### 4. Price and Availability Checking

```
Search for the current price of Mac Mini M4 with 32GB RAM
on Apple.com, Amazon, and Best Buy
```

Useful for purchase decisions, product comparisons, or e-commerce monitoring.

### 5. Documentation Lookups

```
Search the Anthropic documentation for the latest Claude API
rate limits and pricing changes
```

Keeps your agent informed about the tools it uses, without you manually reading changelogs.

## Advanced Configuration

### Search Depth Options

Tavily offers multiple search depth levels with different latency and quality tradeoffs:

| Depth | Response Time | Quality | Use Case |
|-------|-------------|---------|----------|
| **ultra-fast** | < 1s | Basic snippets | Quick fact lookups, autocomplete |
| **fast** | 1-2s | Good snippets, multiple per URL | Most daily queries |
| **basic** (default) | 1-2s | Standard quality | General-purpose searching |
| **advanced** (`--deep`) | 5-10s | Comprehensive, broader coverage | Deep research, complex questions |

For latency-sensitive workflows (like real-time chat), configure your agent to default to `fast`. For research-heavy agents, `advanced` is worth the extra wait and credits.

### Adding Tavily to Agent System Prompts

For best results, add search guidelines to your agent's system prompt. Edit the agent's `SOUL.md` or `AGENTS.md` file in its workspace:

```markdown
## Web Search Guidelines

- Always use Tavily search when the user asks about current events,
  prices, or recent developments
- Start with basic search. Only use --deep for complex research topics
- If a search returns 0 results or fails, tell the user explicitly.
  Never fabricate information as a substitute for search results
- Include source URLs when citing search results
- For news queries, use --topic news and limit to relevant timeframes
- Respect domain filters when the user specifies trusted sources
```

This last rule — about explicit failure reporting — is critical. Without it, your agent will silently fall back to generating answers from training data when Tavily fails. You will get a confident-sounding response that is completely made up. For a deeper exploration of this failure mode, see [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/).

### Environment-Based Configuration for Multiple Agents

If different agents need different Tavily settings, you can configure them independently in `openclaw.json`:

```json5
{
  "agents": {
    "list": [
      {
        "id": "researcher",
        "skills": {
          "tavily-search": {
            "enabled": true,
            "env": {
              // Researcher gets a dedicated key with higher limits
              "TAVILY_API_KEY": "tvly-research-key-here"
            }
          }
        }
      },
      {
        "id": "main",
        "skills": {
          "tavily-search": {
            "enabled": true,
            "env": {
              // Main agent uses the default free-tier key
              "TAVILY_API_KEY": "tvly-free-tier-key-here"
            }
          }
        }
      }
    ]
  }
}
```

This approach lets your research agent burn through a paid Tavily plan for heavy research while your main agent stays on the free tier for occasional lookups.

## Troubleshooting Common Issues

### Problem: Agent Ignores Tavily and Generates Answers From Training Data

**Symptoms**: You ask about recent events and get answers without source URLs, or the information is clearly outdated.

**Causes and fixes**:

1. **API key not set**: Run `echo $TAVILY_API_KEY` to verify it is available. If empty, set it in your shell profile and restart the gateway
2. **API key expired or invalid**: Log in to [tavily.com](https://tavily.com/) and check your dashboard. Generate a new key if needed
3. **Free tier exhausted**: Check your usage on the Tavily dashboard. The free tier resets monthly
4. **Daemon does not see the variable**: If OpenClaw runs as a daemon, the environment variable from your shell profile may not be passed through. Use `launchctl setenv` (macOS) or add it to the systemd service file (Linux)

### Problem: "Skill Not Found" When Installing

**Symptoms**: `clawdhub install tavily-search` returns an error.

**Fixes**:

1. Make sure you are using **`clawdhub`** (with a 'd'), not `clawhub`
2. Update ClawdHub: `npm update -g clawdhub`
3. Check your internet connection

### Problem: Search Results Are Low Quality or Irrelevant

**Fixes**:

1. Be more specific in your search queries. "AI news" is too broad; "OpenClaw new features March 2026" is better
2. Use domain filtering to target authoritative sources
3. Try `--deep` mode for complex topics
4. Increase result count with `-n 10` or `-n 15` for broader coverage

### Problem: Gateway Fails to Start After Configuration Change

**Symptoms**: OpenClaw refuses to start, reporting a JSON schema error.

**Fix**: OpenClaw uses strict JSON5 schema validation. A misplaced comma, typo in a field name, or incorrect nesting will break it. Run:

```bash
# Diagnose configuration issues
openclaw doctor
```

Review the error message carefully. The most common mistake is putting skill configuration in the wrong section of the JSON hierarchy.

## Cost Management Tips

Tavily's free tier is generous (1,000 credits/month), but an aggressive agent can burn through it in days. Here is how to stay within budget.

### 1. Set a Monthly Credit Budget

Track your usage on the [Tavily dashboard](https://tavily.com/). Set up alerts if your plan supports them. A rough budget for personal use:

| Usage Pattern | Credits/Month | Tier Needed |
|--------------|--------------|-------------|
| Occasional manual queries | 100-300 | Free |
| Daily news briefing + ad-hoc searches | 300-600 | Free |
| Active research agent (daily use) | 600-1,500 | Free to Project |
| Multi-agent team with heavy research | 2,000-5,000 | Project to Bootstrap |

### 2. Default to Basic Search

Advanced (`--deep`) searches cost 2x. Reserve them for genuinely complex research. For quick fact lookups, basic search is faster and cheaper.

### 3. Restrict Agent Access

As shown in the configuration section above, only give Tavily access to agents that actually need it. A coding agent running `tavily-search` on every code review question wastes credits.

### 4. Use Cron Job Isolation

When scheduling recurring searches (daily briefings, weekly reports), use OpenClaw's isolated cron jobs. This prevents search results from bleeding into other conversations and triggering unnecessary follow-up searches:

```json5
{
  "id": "daily-news",
  "schedule": { "cron": "0 8 * * *", "tz": "Asia/Shanghai" },
  "isolated": true,  // Runs in its own session
  "message": "Search for the top 5 AI news stories and summarize them"
}
```

### 5. Cache When Possible

If your agent repeatedly searches for the same information within a short period, instruct it to reuse previous search results rather than querying Tavily again. Add this to your agent's system prompt:

```markdown
If you searched for the same topic within the last hour,
reuse the previous results instead of searching again.
```

## Related Reading

- [OpenClaw Setup Guide: Install and Configure Your AI Agent](/posts/ai/2026-03-05-openclaw-setup-guide/) — Start here if you have not set up OpenClaw yet
- [OpenClaw Multi-Agent Setup: Build AI Teams That Work](/posts/ai/2026-03-05-openclaw-multi-agent-setup/) — Configure agent teams with Tavily assigned per role
- [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) — Avoid the most common mistakes after installing Tavily and other skills
- [OpenClaw Memory Strategy](/posts/ai/2026-01-31-openclaw-memory-strategy/) — How memory works alongside tools like Tavily
- [OpenClaw 2026.3.1 New Features](/posts/ai/2026-03-03-openclaw-2026-3-1-new-features/) — Latest OpenClaw release with agent routing and WebSocket streaming
