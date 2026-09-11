+++
date = '2026-04-01T14:00:00+08:00'
draft = false
title = 'Cursor Composer 2 Review: The Kimi K2.5 Controversy and What It Means for AI Coding'
description = 'Deep technical analysis of Cursor Composer 2, built on Moonshot AI Kimi K2.5. Benchmarks, pricing, the attribution scandal, and honest comparison with Claude Code.'
toc = true
tags = ['Cursor', 'Composer 2', 'AI Coding Tools', 'Kimi K2.5', 'Claude Code']
keywords = ['Cursor Composer 2 review', 'Kimi K2.5 controversy', 'Composer 2 vs Claude Code', 'AI coding tools 2026', 'Cursor benchmarks']
+++

![Cursor Composer 2 — where Western product meets Eastern foundation model](cover.webp)

On March 19, 2026, Cursor shipped Composer 2 with a triumphant blog post. Faster, smarter, cheaper — the usual superlatives. Three days later, a developer on X noticed something peculiar in Cursor's API configuration: a model identifier reading `kimi-k2p5-rl-0317-s515-fast`. That single string unraveled a story about transparency, open-source ethics, and the increasingly global nature of AI infrastructure.

This is not just a product review. It is an examination of what happens when a $50 billion startup forgets — or chooses not — to credit the open-source model powering its flagship feature.

## What Is Composer 2, Actually?

Composer 2 is Cursor's custom coding model, designed to replace third-party models (Claude, GPT) for the core agentic coding experience inside the Cursor IDE. Cursor positions it as an in-house breakthrough. The [technical report](https://cursor.com/blog/composer-2-technical-report) describes a two-phase training process:

**Phase 1: Continued Pretraining.** Starting from a base model, Cursor performed extended pretraining on a code-heavy data mix. The report states that "reducing pretraining loss improves downstream RL performance, with better base knowledge reliably translating into a better agent."

**Phase 2: Large-Scale Reinforcement Learning.** Using Anyrun — Cursor's internal platform managing hundreds of thousands of sandboxed coding environments — they ran RL training in realistic Cursor sessions. The RL used "the same tools and harness the deployed model uses, applied to a problem distribution that reflects the full range of what developers ask Composer to do."

The infrastructure required custom low-precision kernels for efficient Mixture of Experts (MoE) training on NVIDIA Blackwell GPUs, plus a fully asynchronous RL pipeline spanning multiple regions.

What the original blog post conspicuously did not mention: that "base model" was **Kimi K2.5** from Moonshot AI.

## The Kimi K2.5 Foundation

[Moonshot AI](https://www.moonshot.cn/) is a Beijing-based company backed by Alibaba and HongShan (formerly Sequoia China). Kimi K2.5 is their open-weight MoE model released in early 2026, and it is genuinely impressive — strong coding capabilities, efficient inference characteristics, and a permissive license for commercial use.

The license, however, has one notable requirement: **prominent attribution** for products exceeding 1 million monthly active users or $20 million in monthly revenue.

Cursor's annualized revenue sits around $2 billion. They were far above the threshold. Yet their launch blog mentioned neither Kimi nor Moonshot AI.

## How the Cover-Up Unraveled

The timeline tells the story:

- **March 19**: Cursor publishes Composer 2 blog post. No mention of Kimi K2.5.
- **March 21**: Developer "Fynn" discovers `kimi-k2p5-rl-0317-s515-fast` in API configs and posts on X.
- **March 22**: [TechCrunch reports](https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/) on the discovery. Cursor co-founder Aman Sanger responds: "It was a miss to not mention the Kimi base in our blog from the start."
- **March 22-23**: Cursor updates the blog post and technical report to acknowledge Kimi K2.5.

Lee Robinson, Cursor's VP of Product, offered a defense: approximately **75% of total compute** went into Cursor's own continued pretraining and RL, while only 25% came from the base model. The implication: Composer 2 is more Cursor than Kimi.

This framing deserves scrutiny.

## The 75/25 Argument Does Not Hold Up

Spending 75% of compute on fine-tuning does not make the base model unimportant. Consider an analogy: if you spend 75% of your construction budget on renovating a house, you still need to disclose who built the foundation — especially if that foundation determines the structural integrity of everything above it.

The base model provides:

- **Core language understanding and generation capabilities**
- **The MoE architecture** that makes Composer 2 efficient
- **Foundational coding knowledge** that RL then specializes

Cursor's RL training is genuinely valuable — it teaches the model to operate within Cursor's specific tool harness, handle real developer workflows, and manage long-horizon coding tasks. But RL cannot conjure capabilities from nothing. It refines and directs what already exists in the base model.

The technical report itself acknowledges this: better base knowledge reliably translates into a better agent. You cannot separate the student from the school.

## Benchmarks: Impressive but Contextualized

The numbers are real and worth examining:

| Benchmark | Composer 2 | Composer 1.5 | Claude Opus 4.6 |
|-----------|-----------|--------------|-----------------|
| CursorBench | 61.3 | 44.7 | — |
| SWE-bench Multilingual | 73.7 | — | — |
| Terminal-Bench 2.0 | 61.7 | — | 58.0 |

A few caveats:

**CursorBench is Cursor's own benchmark.** It measures performance within Cursor's environment, with Cursor's tools. Composer 2 was trained specifically for this environment. Comparing other models on CursorBench is like testing a fish on tree-climbing — the benchmark inherently favors the home team.

**Terminal-Bench is more neutral**, and the 61.7 vs 58.0 gap over Claude Opus 4.6 is real but modest. A 3.7-point difference is meaningful in aggregate but unlikely to be noticeable on any individual coding task.

**SWE-bench Multilingual at 73.7** is genuinely strong. This benchmark tests real-world bug fixing across multiple languages and is harder to game.

**The 200,000-token context window** is serviceable for most tasks but falls short of Claude Code's 1M-token context, which matters for large codebase understanding.

## Composer 2 vs Claude Code: An Honest Comparison

Having used both extensively, here is when each wins. If you have read my [comparison of AI coding tools](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/), you know I value practical experience over benchmarks.

### When Cursor Composer 2 Wins

- **Speed for routine tasks.** Tab completions, small edits, inline suggestions — Composer 2 is snappy inside the Cursor IDE. The tight integration means less context-switching.
- **Cost efficiency.** At $0.50/M input tokens (standard) and $1.50/M (fast), Composer 2 is dramatically cheaper than frontier models. For teams burning through tokens on daily coding, this matters.
- **IDE-native experience.** If you live in Cursor, Composer 2 feels seamless. Multi-file edits, inline diffs, the agent loop — all designed for this specific model.

### When Claude Code Wins

- **Deep codebase understanding.** Claude Code's [1M-token context window](/posts/ai/2026-01-14-claude-code-guide/) means it can hold entire codebases in memory. For large refactors, architecture changes, or debugging cross-file issues, this is not a nice-to-have — it is essential.
- **Complex reasoning.** [Claude Code with Opus 4.6](/posts/ai/2026-03-13-gpt-5-4-vs-claude-opus-comparison/) handles multi-step reasoning chains that Composer 2 struggles with. Security audits, architectural decisions, nuanced trade-off analysis.
- **Terminal-native workflows.** Claude Code runs in your terminal, works with any editor, integrates with git, and supports [Agent Teams](/posts/ai/2026-02-22-claude-code-agent-teams/) for parallel task execution. It is editor-agnostic.
- **Transparency.** You know exactly what model you are running. There is no obfuscation about the underlying technology.

### The Realistic Stack for 2026

Most productive developers I know use both:

- **Cursor + Composer 2** for the 80% — daily editing, quick implementations, routine code generation
- **Claude Code** for the 20% — complex debugging, large refactors, [security analysis](/posts/ai/2026-02-22-claude-code-security/), architectural decisions

This is not a zero-sum competition. The tools complement each other.

## Pricing: The Real Advantage

| Model | Input (Standard) | Input (Fast) | Output (Standard) | Output (Fast) |
|-------|------------------|--------------|-------------------|---------------|
| Composer 2 | $0.50/M | $1.50/M | $2.50/M | $7.50/M |
| Claude Opus 4.6 | $15/M | — | $75/M | — |
| Claude Sonnet 4.5 | $3/M | — | $15/M | — |

Composer 2's pricing is its strongest argument. At roughly 1/30th the cost of Opus 4.6 for input tokens, teams doing high-volume coding can save significantly. But cheaper does not mean better — it means cheaper. You get what the model can deliver, and for tasks requiring deep reasoning, you will still reach for a frontier model.

## The Bigger Picture: Chinese Models Powering Western Tools

The Composer 2 controversy is a preview of a larger trend. Chinese AI labs — Moonshot AI, DeepSeek, Alibaba's Qwen — are producing increasingly competitive open-weight models. Western companies building on these models face a tension:

1. **Economically rational**: Using the best available base model, regardless of origin, produces better products at lower cost.
2. **Politically fraught**: In an era of AI export controls and geopolitical competition, acknowledging Chinese AI foundations can be uncomfortable for marketing teams.
3. **Ethically required**: Open-source licenses exist for a reason. Attribution is not optional.

Cursor chose the economically rational path but stumbled on the ethical requirement. The fact that they had a legitimate commercial partnership with Fireworks AI for Kimi K2.5 access makes the attribution omission worse, not better — they had every opportunity to be upfront.

This will happen again. As open-weight models from Chinese labs continue improving, more Western AI companies will build on them. The ones that are transparent about it will earn trust. The ones that hide it will eventually get caught.

## Should You Use Composer 2?

**Yes, with clear eyes.** The model is genuinely good for its intended purpose: fast, efficient coding assistance inside the Cursor IDE. The controversy does not change the model's capabilities.

But consider what you are buying:

- A model whose foundations come from a Chinese open-source project (nothing wrong with that — just know it)
- A company that chose not to disclose this until caught (that is worth remembering)
- An IDE-locked experience that does not transfer to other environments
- Benchmarks that look impressive partly because the benchmark was designed for this model

If you want the best AI coding experience in 2026, the answer is not picking one tool — it is building a [workflow that combines the right tools](/posts/ai/2026-01-19-ai-dev-workflow/) for the right tasks. Composer 2 has earned a place in that workflow. It just has not earned the right to pretend it built everything from scratch.

## Key Takeaways

1. **Composer 2 is real and useful.** The benchmarks, while context-dependent, show genuine improvement. The pricing is excellent.
2. **The attribution failure was a choice, not an oversight.** A company at Cursor's scale does not accidentally forget to credit its base model.
3. **The 75/25 compute split is misleading framing.** Compute percentage does not equal contribution percentage. The base model is foundational.
4. **Use both Cursor and Claude Code.** They solve different problems. Composer 2 for speed, Claude Code for depth.
5. **Watch this space.** Chinese open-weight models powering Western products is a trend that will accelerate, and transparency about it will become a competitive differentiator.

---

*For a deeper look at AI coding tools and workflows, see my [complete Claude Code guide](/posts/ai/2026-01-14-claude-code-guide/) and [AI coding agents comparison](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/).*

## Related Reading

- [Cursor Agent Best Practices: The Complete Guide to AI Coding](/posts/ai/2026-01-19-cursor-agent-best-practices/) — Get the most out of Cursor's agent capabilities
- [Cursor Setup Guide 2026: From Install to Advanced Agent Mode](/posts/ai/2026-03-08-cursor-setup-guide/) — Complete Cursor installation and configuration
- [Claude Code vs Cursor vs Windsurf 2026: Speed, Cost & Control](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/) — Side-by-side comparison of the top three tools
- [Claw Code: The Open-Source Claude Code Rewrite That Hit 100K Stars in Hours](/posts/ai/2026-04-01-claude-code-open-source-agent/) — Open-source alternative gaining traction
- [GPT-5.4 vs Claude Opus 4.6: Complete Comparison for Developers](/posts/ai/2026-03-13-gpt-5-4-vs-claude-opus-comparison/) — The models powering these AI coding tools
