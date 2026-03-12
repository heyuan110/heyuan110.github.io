+++
date = '2026-01-30T10:00:00+08:00'
draft = false
title = 'AI Workflow Playbook: From Prompts to Production Code'
description = 'A battle-tested AI workflow methodology covering prompt engineering, AI-assisted coding, tool selection, and enterprise deployment — turn AI from a chat toy into a real productivity engine.'
toc = true
tags = ['AI Workflow', 'AI Coding', 'Prompt Engineering', 'AI Tools', 'Productivity']
categories = ['AI Guides']
keywords = ['AI workflow', 'AI coding best practices', 'prompt engineering tips', 'AI tools for developers', 'enterprise AI deployment']
+++

Most people have been using AI for months, yet they're still stuck in "ask a question, get an answer" mode. They've had plenty of conversations with ChatGPT, but when it comes to real work, the results always feel lacking — answers are too generic, generated code won't run, or the output screams "written by AI."

The problem isn't that AI is bad. It's that **we're using it wrong**.

This article is a practical AI workflow methodology distilled from real-world experience — covering how to ask better questions, how to write effective prompts, how to use AI for programming, and how to deploy AI in enterprise settings. If you're still figuring out how to make AI genuinely useful, this guide is for you.

## 1. Build Your AI Tool Stack First

Before diving in, here's the AI tool combination I use daily:

| Use Case | Tool | Notes |
|----------|------|-------|
| **General chat** | ChatGPT, Gemini, Qwen | Cross-reference multiple models — each has different strengths |
| **Deep research** | NotebookLM | Google's tool for digesting long documents and videos — turns a YouTube video into an infographic in 2 minutes, generates podcast-style audio reviews |
| **Content creation** | YouMind | Writing agent with structured output |
| **Frontend coding** | Antigravity | Google's AI-native IDE with Gemini and Claude built in — and it's free |
| **Backend coding** | Codex | OpenAI's coding agent, solid for backend logic |
| **Image generation** | Nano Banana Pro | Google's image gen tool — character consistency far ahead of competitors |
| **Design** | Lovart | Design agent for rapid mockups |

**The core principle for tool selection**: Don't chase the latest hype. Use whatever solves the problem most efficiently. A "primary tool + backup" combo for each workflow step is all you need.

## 2. Make AI Actually Understand You: The Four-Quadrant Framework

Many people just throw a single sentence at AI and hope for the best. Good results feel like luck; bad results get blamed on "dumb AI."

The real issue isn't the AI — it's that you haven't figured out **what type of question you're asking**.

I use a **Four-Quadrant Framework** to decide how to communicate with AI:

### Quadrant 1: Common Ground (Clear Factual Tasks)

You know exactly what you want, and AI can deliver it directly.

**Strategy: Give direct instructions.** Don't over-explain.

```
Clean this CSV data into a standardized table. Remove duplicate rows
and normalize all dates to YYYY-MM-DD format.
```

### Quadrant 2: Blind Spots (Unfamiliar Domains)

You don't know much about the topic and need AI to build your understanding first.

**Strategy: Ask for background context first** — don't jump straight to answers.

```
I want to understand the difference between WebSocket and SSE.
Start with a background overview including use cases, pros/cons,
and performance comparison for each.
```

### Quadrant 3: Private Knowledge (Your Unique Context)

These questions involve your own business data, experience, or domain knowledge that AI can't access.

**Strategy: Feed sufficient context first.**

```
We're a cross-border e-commerce company focused on Southeast Asia,
with 5,000+ SKUs and a current return rate of 15%.
Based on this context, analyze possible reasons for the high return rate.
```

### Quadrant 4: Unknown Territory (Exploratory Questions)

You're not even sure what you want yet — you need the conversation itself to help you discover it.

**Strategy: Use Socratic questioning — let AI ask you questions.**

```
I want to start an AI-related side project, but I haven't
decided on a direction yet. Use the Socratic method to help me
clarify my thinking. Ask me one question at a time.
```

### Mental Frameworks Are AI's "Operating System"

Here's an incredibly useful technique: **ask AI to answer using a thinking framework**. The output quality jumps dramatically.

For example:
- Use the **SMART framework** to break down goals
- Use **First Principles thinking** to analyze root causes
- Use **5W2H** for comprehensive analysis
- Use **Occam's Razor** to simplify solutions
- Use the **80/20 Rule** to identify key factors

These frameworks act like an operating system for AI — without one, it produces random output; with one, its thinking gains direction and structure.

```
Use the SMART framework to break down this goal:
"I want to increase my blog's monthly traffic from 1,000 to 10,000
within 3 months"
```

## 3. Prompt Engineering Is Engineering, Not Magic

Many people think prompt writing is an art that requires natural talent. It's not — it's a **systematic engineering skill** that can be learned.

### Text Prompts: The Three-Step Iteration Method

**Step 1: Research first**

Don't start writing immediately. Use Deep Research (or any search tool) to investigate first.

For example, if you're crafting a prompt for a children's picture book, first have AI figure out "what makes a great picture book" — story structure, language style, visual pacing, age appropriateness. Only after understanding these fundamentals can you write an effective prompt.

**Step 2: Generate a meta-prompt**

Feed your research to AI:

```
I need to write a prompt for [X type of content].
Here is my research: [paste research]
Generate a structured meta-prompt for me.
```

**Step 3: Iterate and refine**

Run the initial prompt, then share the results with AI and explain what's wrong:

```
Here's the output from your prompt: [paste result]
Issues: character expressions are too stiff, background colors are too dark
Optimize the prompt to fix these two problems.
```

Repeat for 3-5 rounds, and the prompt will become increasingly precise.

### Image Prompts: The Reference Replication Method

**When you have a reference image:**

1. Find your desired style reference
2. Send it to AI and request a JSON-format meta-prompt (limited to 800 words)
3. Swap in your actual subject matter

This approach replicates roughly 90% of the target style.

**When you don't have a reference:**

Don't force a prompt from scratch. Let AI guide you instead:

```
I want to generate an image but haven't decided on the style yet.
Ask me these questions one by one to clarify my requirements:
1. What effect do I want to achieve?
2. Who is the target audience?
3. Are there any reference examples?
4. What color palette/style do I prefer?
```

**Core principle: When in doubt, don't force it. Let AI help you clarify before you start.**

## 4. AI Coding Done Right: Spec-Driven Development

Most people use AI for coding like this: paste a vague requirement, wait for a blob of code, copy-paste it, and ask again when it breaks.

This works for small scripts. It fails for real projects.

The right approach follows **spec-driven development**:

```
PRD → Technical Spec → Development Plan → Code → Test
```

### Step 1: Write the PRD (Product Requirements Document)

Discuss requirements with AI, but **don't accept the first draft**. Push back relentlessly:

```
Have you considered edge cases for this feature?
What happens if the user loses network connectivity?
Can it handle high concurrency?
This interaction flow isn't intuitive — users will get lost.
```

Force AI to refine the PRD until it's solid, rather than settling for a mediocre first attempt.

### Step 2: Rapid Prototyping

Use an AI IDE's Build mode to quickly scaffold the frontend. Get the core interaction logic running first — don't obsess over details.

### Step 3: Code Refinement

Move the initial code to a proper IDE for polish. AI-generated code typically "runs but isn't great" — naming conventions are off, error handling is missing, architecture is unclear. These all need human oversight.

For more on AI-assisted coding, check out my earlier posts on [My AI Development Workflow: From Requirements to Deployment](/posts/ai/2026-01-19-ai-dev-workflow/) and [Cursor Agent Coding Best Practices](/posts/ai/2026-01-19-cursor-agent-best-practices/).

### Step 4: Automated Testing

Have AI write test cases and run automated tests using chrome-dev-tool MCP. Many people skip this step, but it catches a huge number of edge cases.

If you're using Claude Code, see [Claude Code Browser Automation: 5 Methods Compared](/posts/ai/2026-01-28-claude-code-browser-automation/) for a comparison of different automation approaches.

### Step 5: Backend Development

Backend work needs even more context than frontend. My approach:

1. Have AI summarize the project's documentation folder to build global understanding
2. Import your private knowledge base (API docs, database schemas, business rules)
3. Then start coding

**Core principle: The clearer the context, the higher the output quality.**

Architecture decisions must be made upfront. If you let AI write code without defining the architecture first, you'll get a pile of patches — it runs, but it's impossible to modify or extend.

## 5. Enterprise AI Adoption: Where to Start

If your company wants to adopt AI, don't try to "go fully intelligent" overnight. Start with proven, low-risk scenarios for the fastest ROI:

### Q&A Systems

- **Internal knowledge base Q&A**: Import company documents, policies, and FAQs — employees can query anytime
- **Customer-facing chatbots**: Far more capable than traditional rule-based bots

### Review & Compliance

- **Contract review**: AI checks contract clauses line by line, flagging risk items
- **Process compliance**: Automated verification that approval workflows follow regulations

### Content Generation

- **PRD writing**: Double product manager productivity
- **Research reports**: Auto-generate analysis reports from data
- **Quarterly reviews**: Input key metrics, output structured presentations

### Data Queries

- **Text-to-SQL**: When someone says "Show me Q1 sales," AI automatically queries the database and returns visualized results

### A Recommended Open-Source Platform

If your team wants to experiment quickly, check out [BISHENG](https://github.com/dataelement/bisheng) — an LLM application development platform built for enterprise office scenarios. It's Apache 2.0 licensed, fully free for commercial use. Deploy one instance and you can rapidly build various office AI applications without reinventing the wheel.

## 6. Staying Up to Date: My AI Information Sources

The AI field moves incredibly fast — tools get replaced every six months, models update monthly. Staying informed matters. Here are my go-to sources:

| Source | Why It's Useful |
|--------|-----------------|
| [WaytoAGI Knowledge Base](https://waytoagi.feishu.cn/wiki) | One of the largest open AI knowledge bases (5M+ visits), covering fundamentals through real-world case studies |
| [AIBase](https://www.aibase.com/) | AI tool directory + news aggregator, great for quickly finding tools |
| Custom news scraper | AI-powered scraping of international tech communities, customized to personal needs |

**Pro tip**: Don't limit yourself to local-language content. International AI news leads by 1-2 weeks. Build an automated translate-and-summarize pipeline to maintain your information advantage.

## Key Takeaways

At the end of the day, AI is a mirror:

> **If your thinking is clear, AI accelerates you. If your thinking is muddled, AI just mass-produces garbage faster.**

Don't expect AI to think for you — but absolutely let it do the heavy lifting. The key principles:

1. **Classify your question type**: Use the Four-Quadrant Framework to match your approach
2. **Systematize prompt writing**: Research, generate, iterate — it's never a one-shot process
3. **Follow spec-driven development**: PRD, tech spec, code, test — don't skip steps
4. **Context determines quality**: The more context you feed AI, the better the output
5. **Frameworks are AI's operating system**: SMART, 5W2H, First Principles — give AI a thinking framework and output quality jumps immediately

This isn't an article to read and forget. Pick your most painful workflow bottleneck and start applying these methods today. AI's ceiling is defined by the person using it.

### Related Reading

- [My AI Development Workflow: From Requirements to Deployment](/posts/ai/2026-01-19-ai-dev-workflow/)
- [Cursor Agent Coding Best Practices: Complete Official Guide](/posts/ai/2026-01-19-cursor-agent-best-practices/)
- [Claude Code Browser Automation: 5 Methods Compared](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Why Personal Taste Matters More Than Ever in the AI Era](/posts/ai/2026-01-23-taste-matters-in-ai-era/)
