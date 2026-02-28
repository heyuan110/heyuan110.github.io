# SEO Optimization Plan — Based on GSC Data (2026-02-28)

> Data period: 2026-01-29 to 2026-02-27 (28 days)

---

## Current State Summary

| Metric | Chinese | English | Total |
|--------|---------|---------|-------|
| Pages with data | 101 | 3 | 104 |
| Clicks | 1,380 (99.4%) | 8 (0.6%) | 1,388 |
| Impressions | 38,554 (83.2%) | 7,789 (16.8%) | 46,343 |
| CTR | 3.58% | 0.10% | 3.0% |
| Avg Position | 7.3 | 6.2 | 7.1 |

**Core problem**: English content gets impressions but not clicks. The Pricing article alone has 7,689 impressions and 3 clicks (0.04% CTR).

---

## Priority 1: Fix Pricing Article CTR (Immediate — This Week)

### Problem Analysis

230 pricing-related queries driving 806 impressions with **0 clicks**. Query intent breakdown:

| Intent Cluster | Queries | Impressions | Avg Pos | Match to Current Title? |
|---------------|---------|-------------|---------|------------------------|
| **claude pro pricing** | 56 | 366 | 7.3 | ❌ Title says "Claude Code" |
| **claude rate limits** | 70 | 141 | 8.3 | ❌ Not mentioned in title |
| **claude max pricing** | 35 | 115 | 7.3 | ✅ Partially ("Max Plan") |
| **claude code pricing** | 33 | 105 | 5.0 | ✅ Direct match |
| **claude team pricing** | 18 | 50 | 6.9 | ❌ Not mentioned |
| **claude free tier** | 16 | 27 | 6.8 | ❌ Not mentioned |

**Root Cause**: Title targets "Claude Code Pricing" but 45% of impressions come from "Claude Pro Pricing" and "Claude AI Pricing" queries. The article covers ALL plans, but the title doesn't signal that.

### Action Items

#### 1.1 Rewrite Title and Description

**Current:**
```
title = 'Claude Code Pricing 2026: Is the Max Plan Worth $200?'
description = 'Complete Claude Code pricing breakdown for 2026. Compare Pro, Max, Team, and API plans with real cost analysis.'
```

**Proposed:**
```
title = 'Claude Pricing 2026: Pro, Max, Team & API Plans Compared'
description = 'Complete Claude pricing guide for 2026. Pro ($20), Max ($100-200), Team, and API costs compared. Includes rate limits, Claude Code access, and competitor benchmarks.'
```

**Why:**
- "Claude Pricing" matches the #1 query cluster (not "Claude Code Pricing")
- "Pro, Max, Team" in title signals coverage of all plans
- Description includes "rate limits" to capture that 70-query cluster
- Description mentions specific prices ($20, $100-200) for rich snippet potential

#### 1.2 Add Missing H2 Sections

Add these sections to capture query intent clusters the article doesn't explicitly target:

- `## Claude Pro Rate Limits 2026` — captures 70 queries, 141 impressions
- `## Is Claude AI Free?` or `## Claude Free Tier` — captures 16 queries
- `## FAQ` — add structured FAQ schema for questions like "Does Claude Pro include Claude Code?"

#### 1.3 Add Keywords

```toml
keywords = ['Claude pricing 2026', 'Claude Pro price', 'Claude Max plan cost',
            'Claude rate limits', 'Claude Code pricing', 'Claude free tier',
            'Claude Pro vs Max', 'Anthropic pricing']
```

---

## Priority 2: Accelerate Indexing (This Week)

### Problem
Only 3 of 9 English articles appear in GSC. The 6 articles published on 2026-02-28 haven't been crawled yet.

### Action Items

#### 2.1 Submit URLs for Indexing
Use GSC URL Inspection API to request indexing for:
- `/posts/ai/2026-02-28-claude-code-claudemd-guide/`
- `/posts/ai/2026-02-28-claude-code-mcp-setup/`
- `/posts/ai/2026-02-28-claude-code-hooks-guide/` (partially indexed — 92 impressions)
- `/posts/ai/2026-02-28-claude-code-skills-guide/`
- `/posts/ai/2026-02-28-claude-code-worktree-guide/`
- `/posts/ai/2026-02-28-claude-code-teams-guide/`

#### 2.2 Verify Sitemap
Ensure `sitemap.xml` includes all new English articles. Hugo should auto-generate this.

#### 2.3 Internal Links from High-Traffic Chinese Pages
Add contextual internal links from top Chinese articles to new English articles:
- From `openclaw-automation-pitfalls` (452 clicks) → link to relevant English guides
- From `openclaw-multi-agent-guide` (263 clicks) → link to Teams/MCP English guides
- From `claude-code-browser-automation` (202 clicks) → link to Hooks/Skills English guides

> ⚠️ AGENTS.md says "Don't modify existing Chinese articles." However, adding a small "Related English articles" section at the bottom is arguably not modifying the content, just adding navigation. **Confirm with user before proceeding.**

---

## Priority 3: Title/Description Optimization for All English Articles

### Hooks Guide (Already Indexed — 92 impressions, 5 clicks)

**Current:** `title = 'Claude Code Hooks: Automate Your Coding Workflow'`

This article is performing relatively well (5.43% CTR). Check if expanding the title to include more search terms helps:
- Consider: `'Claude Code Hooks Guide: 12 Automation Configs for 2026'`

### Setup Guide

**Current:** `title = 'Claude Code Setup Guide: Install and Configure'`

Target queries: "how to install claude code", "claude code setup", "claude code tutorial"
- Consider: `'How to Install Claude Code: Complete Setup Guide 2026'`
- "How to" pattern matches more informational queries

### Mistakes Article

**Current:** `title = '10 Claude Code Mistakes Beginners Make (And Fixes)'`

Target queries: "claude code tips", "claude code best practices", "claude code mistakes"
- Title is good for CTR (listicle format). Keep as-is.

---

## Priority 4: New Content — Data-Driven Priorities (Next 2 Weeks)

Based on GSC query data, reprioritize the content plan:

### 4.1 Claude Rate Limits Article (NEW — Not in Content Plan)

**Evidence:** 70 rate-limit queries with 141 impressions and 0 coverage.

Create a dedicated article: **"Claude Rate Limits 2026: Messages Per Hour for Every Plan"**

Target queries:
- "claude pro rate limits 2026"
- "claude pro messages per 5 hours"
- "claude pro usage limits"
- "claude max plan limits"

This is a **content gap** not covered by any competitor well. High informational intent, low competition.

### 4.2 Pillar Article #1 — Claude Code Complete Guide

Write the cluster pillar article to:
- Link to all 9 supporting articles (boost their authority)
- Target broad "claude code guide" and "claude code tutorial" queries
- Serve as the definitive hub page

### 4.3 Phase 3 Priority Order (Adjusted by GSC Data)

| Priority | Article | Evidence |
|----------|---------|----------|
| **1** | #42 Claude Code vs Cursor | "claude code vs cursor" not yet in data — fresh opportunity, high search volume |
| **2** | #23 Copilot vs Claude vs Cursor | Three-way comparison articles rank well for multiple queries |
| **3** | #13 MCP Protocol Explained | MCP queries exist (10 queries) but low volume — growing topic |
| **4** | #36 Vibe Coding Explained | "vibe coding" trending (seen in Chinese queries) |

---

## Priority 5: Technical SEO Checks

### 5.1 Hreflang Tags
Since the site has both Chinese and English content on the same domain, consider adding hreflang:
```html
<link rel="alternate" hreflang="en" href="https://www.heyuan110.com/posts/ai/2026-02-25-claude-code-pricing/" />
<link rel="alternate" hreflang="zh" href="https://www.heyuan110.com/posts/ai/2026-02-25-claude-code-pricing/" />
```
This tells Google which language each page targets. May not be needed if URLs are distinct.

### 5.2 Structured Data (Schema.org)
Add Article schema to all English posts for rich snippets:
- `@type: Article`
- `datePublished`, `dateModified`
- `author`, `publisher`
- FAQ schema for articles with FAQ sections

### 5.3 Page Speed
Run Lighthouse on key pages. Cover images are small (17-18 KB) which is good. Check for render-blocking resources.

---

## Priority 6: Content Refresh Strategy (Monthly)

### 6.1 Pricing Article — Monthly Updates
The pricing article targets time-sensitive queries ("february 2026", "current pricing").

**Monthly task:** Update the article with:
- Current month in content (not just in queries — Google auto-appends month)
- Any pricing changes from Anthropic
- Updated competitor pricing
- Refresh the `date` field in front matter

### 6.2 Track Position Changes
Monitor these key queries weekly:
- "claude code pricing 2026" (Pos 3.5 — push to #1)
- "claude ai pricing anthropic february 2026" (Pos 1.7 — already #1-2!)
- "claude --worktree" (Pos 5.6 — push to top 3)

---

## KPIs to Track

| Metric | Current | 30-Day Target | 90-Day Target |
|--------|---------|---------------|---------------|
| English pages indexed | 3 | 9 | 15+ |
| English clicks/day | 0.3 | 5 | 20 |
| English impressions/day | 278 | 500 | 1,500 |
| English avg CTR | 0.10% | 2% | 4% |
| Pricing article CTR | 0.04% | 3% | 5% |
| Total daily clicks | 50 | 60 | 100 |

---

## Execution Timeline

| Week | Actions |
|------|---------|
| **W1 (Now)** | Fix Pricing title/desc, submit URLs for indexing, add rate limits section |
| **W2** | Write Claude Rate Limits article, write Pillar #1 |
| **W3** | Write #42 Claude Code vs Cursor, optimize Setup/Mistakes titles |
| **W4** | Write #23 Copilot vs Claude vs Cursor, add structured data |
| **W5-6** | Write #13 MCP Protocol, #36 Vibe Coding |
| **Monthly** | Refresh Pricing article, review GSC data, adjust priorities |
