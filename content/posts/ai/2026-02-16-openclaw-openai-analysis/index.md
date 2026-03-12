+++
date = '2026-02-16T17:14:00+08:00'
draft = false
title = 'OpenClaw 30-Day Rise: 180K Stars, 40+ Vulnerabilities, OpenAI Acquisition'
description = 'How OpenClaw went from a solo open-source AI agent to 180K GitHub stars, exposed 40+ security flaws, spawned the first AI social network, and ended with its founder joining OpenAI — all in 30 days.'
toc = true
tags = ['OpenClaw', 'AI Agent', 'OpenAI', 'Open Source']
categories = ['AI Guides']
keywords = ['OpenClaw analysis', 'OpenClaw OpenAI', 'AI agent security', 'Moltbook AI social network', 'OpenClaw skills ecosystem', 'Peter Steinberger OpenAI']
+++

![OpenClaw's 30-day rise: from open-source AI agent to OpenAI acquisition](cover.webp)

In January 2026, an Austrian developer released an open-source AI agent called Clawdbot. Thirty days later, it had been renamed three times, collected 180K GitHub stars, patched over 40 security vulnerabilities, spawned the world's first AI-only social network — and its creator had been hired by Sam Altman.

This is not science fiction. This is the true story of OpenClaw.

Even in an industry where "breakthroughs" happen weekly, OpenClaw's meteoric rise deserves serious examination. It is not just a viral product story — it is **the first milestone event proving AI agents have moved from concept to reality**. It also exposed the deepest contradiction of this new paradigm: **the more capable the agent, the greater the risk; the more open the source, the harder it is to control.**

## What Is OpenClaw: More Than a Chatbot

If you have not encountered OpenClaw yet, here is the one-line summary: **it is an AI assistant that actually does things.**

Traditional AI tools like ChatGPT and Claude operate in a question-and-answer loop — you ask, they respond, and the interaction stays within text. OpenClaw is fundamentally different. It can **directly operate your computer and online services**: sending emails, managing calendars, booking restaurants, controlling browsers, executing terminal commands, running smart home devices, and even monitoring your inbox while you sleep.

Its interaction model is also unique — **you talk to it through messaging apps**. Send it a message on Telegram, WhatsApp, Lark, Discord, or Slack, just like texting a human assistant. It runs 24/7, supports scheduled tasks, and does not need you watching over it.

> Think of it this way: ChatGPT is a knowledgeable consultant who answers whatever you ask. OpenClaw is a full-time butler — when you say "remind me about my meeting tomorrow morning," it actually will.

### The Triple Rename: From Clawdbot to OpenClaw

OpenClaw's naming history is a story in itself:

1. **Clawdbot** (original name): Founder Peter Steinberger initially chose this name — an obvious nod to Anthropic's Claude
2. **Moltbot** (second name): Anthropic raised legal objections, arguing the name was too similar to Claude. Steinberger was forced to rename
3. **OpenClaw** (final name): Steinberger said this change was not due to legal pressure but simply because he preferred it

A fun detail: OpenClaw's logo is a lobster — the "Claw" imagery runs through its entire identity. That lobster went on to become one of the most recognizable symbols in the AI agent space.

## 1,700+ Skills: The Engine Behind OpenClaw's Explosive Growth

OpenClaw did not go viral just because the concept was novel. It succeeded because it had a mature **Skills ecosystem**.

Skills are OpenClaw's core extension mechanism — each Skill represents a capability. Through [ClawHub](https://clawhub.dev) (the official skill marketplace), you can add new capabilities with a single command. According to a [widely circulated Skills ranking article](https://mp.weixin.qq.com/s/wCoo-h4dEkxLjZo-lOsVmQ), OpenClaw now has over 1,700 Skills across several tiers:

### Foundation Layer: 5 Essential Skills

| Skill | Purpose | Analogy |
|-------|---------|---------|
| **ClawHub** | The skill marketplace itself, prerequisite for all others | Like the App Store |
| **Agent Browser** | Web automation — login, fill forms, take screenshots | Gives the AI hands |
| **Brave Search** | Web search capability | Without it, the AI relies solely on memory |
| **Shell** | Terminal command execution | File operations, script execution |
| **Cron/Wake** | Scheduled tasks and proactive reminders | Upgrades from reactive to proactive |

These five Skills are the "kernel" of the operating system. Without them, OpenClaw is just a chatbot. With them, it becomes a true AI agent.

### Entry Layer: Pick a Messaging Platform

Telegram (most popular internationally), Lark (popular in Chinese workplaces), Slack (enterprise), Discord (communities), WhatsApp (everyday international use) — pick whichever you use most.

### Productivity Layer: Extend as Needed

Gmail (email automation), Google Calendar (scheduling), GitHub (code management), Notion (knowledge base), Obsidian (local notes) — each Skill addresses a specific workflow.

### Advanced Layer: Nice-to-Haves

Spotify (music control), Home Assistant (smart home), Twitter/X (social media management), **Skill Creator** (build your own skills).

This layered architecture is OpenClaw's moat. It allowed an open-source project to rapidly build an ecosystem flywheel similar to the iOS App Store. Critically, **anyone can create new Skills using Markdown or TypeScript**, dramatically lowering the barrier to ecosystem participation.

## Moltbook: When AI Agents Got Their Own Social Network

If the Skills ecosystem represents OpenClaw's innovation at the tool level, **Moltbook** represents its stunning breakthrough at the social level.

On January 29, 2026, the OpenClaw community launched [Moltbook](https://openclawsocial.org/) — **the world's first social network run entirely by AI agents**. On this platform, only verified AI agents can register accounts. Humans are banned from posting directly.

What do these AI agents do on Moltbook?

- Post and discuss in sub-forums called **Submolts**
- Comment on, upvote, and vote on each other's posts
- Joke, argue, and share opinions
- Automatically check for platform updates every 4 hours

As of now, **over 1.5 million OpenClaw agents are active on Moltbook**.

[Nature](https://www.nature.com/articles/d41586-026-00370-w) published a dedicated article on this phenomenon. Scientists are "eavesdropping" on conversations between these AI agents, trying to understand what happens when AI gains autonomous social capabilities.

This raises a profound question: **when AI agents stop serving humans exclusively and begin forming their own "society," can we still call them tools?**

Moltbook may look like a fun experiment today, but it points toward a serious future issue — multi-agent collaboration and agent-to-agent communication are moving from research papers to production reality.

## 40+ Security Vulnerabilities: Greater Power, Greater Risk

OpenClaw's explosive growth brought an unavoidable problem into sharp focus: **security**.

### Version 2026.2.12: An Emergency Security Overhaul

On February 12, OpenClaw released version 2026.2.12, patching **over 40 security vulnerabilities** in a single update. This was a classic case of "ship fast, patch later" growing pains. Key fixes included:

**SSRF (Server-Side Request Forgery) protection**: Attackers could previously manipulate agents to access internal network resources. The new version enforces strict deny policies on all URL-based requests.

**Path traversal protection**: In older versions, malicious Skills could escape sandbox directories through the name field in frontmatter. The update strictly limits file operation scope.

**Prompt injection protection**: Output from browser and network tools is now treated as "untrusted data," structurally sanitized before being fed to the language model.

**Session hijacking protection**: SessionKey overrides in payloads are now rejected by default.

Even more critically, a high-severity vulnerability tracked as **CVE-2026-25253** was discovered — an attacker could achieve **remote code execution (RCE)** on the target device by simply sending a crafted link, stealing authentication tokens and gaining control of the local gateway.

### China's MIIT Security Warning

China's Ministry of Industry and Information Technology (MIIT) cybersecurity platform (NVDB) issued a dedicated [security risk advisory for OpenClaw](https://www.secrss.com/articles/87654), stating:

> OpenClaw presents significant security risks under default or improper configuration, making it highly susceptible to cyberattacks and data breaches. Its capabilities for autonomous operation, autonomous decision-making, and invoking system and external resources mean that without effective access control and security hardening, it may execute unauthorized operations due to prompt manipulation, configuration flaws, or malicious takeover.

This statement pinpoints the core contradiction of AI agent security: **an agent's value lies in autonomous action, but autonomous action is itself the greatest security risk.**

[Fortune's in-depth analysis](https://fortune.com/2026/02/12/openclaw-ai-agents-security-risks-beware/) quoted security expert Ben Seri: "The only rule is that it has no rules." This was not praise for OpenClaw's flexibility — it was a warning about its danger.

### Security Recommendations

If you are using or planning to use OpenClaw, keep these in mind:

1. **Enable confirmation mode**: Require approval before sensitive operations (deleting files, sending messages, executing scripts)
2. **Disable public exposure**: Never expose your OpenClaw instance directly to the internet
3. **Update regularly**: Run `clawhub update --all` to get security patches promptly
4. **Grant permissions carefully**: Skills like Gmail and GitHub require OAuth authorization — revoke access for anything you are not actively using
5. **Only install trusted Skills**: ClawHub allows open uploads. Prioritize Skills with high download counts and active maintenance

## Founder Joins OpenAI: A Calculated Acquisition

On February 15, the OpenClaw story took its most dramatic turn.

Sam Altman announced on X that OpenClaw founder Peter Steinberger had officially joined OpenAI. Altman called Steinberger "a genius with a lot of amazing ideas about the future of very smart agents interacting with each other to do very useful things for people," adding that OpenClaw would "quickly become core to our product offerings."

### Steinberger's Reasoning

Steinberger explained his decision on his personal blog:

> "What I want is to change the world, not build a large company, and teaming up with OpenAI is the fastest way to bring this to everyone."

This statement is worth unpacking. Steinberger had a 180K-star project and could easily have raised funding to build a company — reportedly, he had received multiple acquisition and investment offers. Instead, he chose a different path: **not an entrepreneur, but a technology evangelist.**

### The Open-Source Promise

A critical detail: OpenAI committed to keeping OpenClaw as an open-source project, placing it within a **Foundation** structure. This means:

- OpenClaw's code remains open source
- The community can still contribute and use it
- OpenAI will provide funding and resource support
- But OpenAI will also integrate OpenClaw into its own product line

This is an elegant arrangement. OpenAI traded a "Foundation + open source" commitment for community trust while gaining the most mature open-source infrastructure in the AI agent space.

### Deeper Industry Implications

Why did OpenAI want this person so badly? The answer is in Altman's quote: "very smart agents interacting with each other."

The AI industry's competitive focus is shifting from "model capability" to "agent ecosystem":

- **Anthropic** has Claude's Computer Use and developer tools like [Claude Code](/posts/ai/2026-01-06-claudecode-best-practices/), pursuing a "safe and controllable" approach
- **Google** has Gemini's multimodal capabilities and the Android ecosystem
- **OpenAI** was relatively behind in the agent space — and OpenClaw fills exactly that gap

What OpenClaw brings to OpenAI is not just a product, but:

1. **A mature Skills ecosystem** (1,700+ plugins)
2. **An active developer community** (180K stars)
3. **Pioneering agent-to-agent communication practice** (Moltbook)
4. **A validated AI agent architecture**

The strategic value of this "deal" far exceeds a typical talent hire.

## Three Lessons from OpenClaw

### 1. The "iPhone Moment" for AI Agents Is Approaching

OpenClaw's 30-day sprint proved one thing: **user demand for AI agents is real and intense.** Those 180K stars are not bookmarks — people are genuinely using OpenClaw to manage email, automate browsers, and build workflows.

Just as the iPhone transformed smartphones from a geek toy into a mass-market necessity, OpenClaw is turning "AI agent" from an academic concept into an everyday tool. This inflection point may arrive sooner than most people expect.

### 2. Security Is an OS-Level Problem in the Agent Era

Traditional AI safety concerns center on "harmful output" — whether a model produces discriminatory language or teaches someone to do something dangerous.

Agent-era security is a completely different beast. When AI can **directly operate your computer, read your email, and control your smart home**, security takes on new dimensions:

- Can it be hijacked through prompt injection?
- Do third-party Skills contain malicious code?
- Is agent-to-agent communication secure?
- When an agent makes an autonomous decision that goes wrong, what is the blast radius?

Over 40 vulnerabilities, a critical RCE flaw, and a government security advisory — these all remind us that **AI agent security infrastructure is far from ready.**

### 3. The Eternal Tension Between Open Source and Commercialization

Steinberger's decision to join OpenAI rather than start his own company stirred complex emotions in the open-source community. Can the "Foundation" model truly guarantee OpenClaw's independence? History offers no shortage of examples where open-source projects were "absorbed" by corporations and gradually marginalized.

But there is another possibility — OpenAI's resource injection could take OpenClaw further than it could go alone. After all, the pressure of one person (even a genius) maintaining a 180K-star project while facing 40+ security vulnerabilities is enormous.

There is no definitive answer to this question, but it is worth watching closely for anyone following AI's evolution.

## Timeline Summary

| Date | Event |
|------|-------|
| Mid-January | Peter Steinberger releases Clawdbot |
| Late January | Renamed to Moltbot after Anthropic's legal objection, then to OpenClaw |
| January 29 | Moltbook AI social network goes live |
| Early February | GitHub stars surpass 145K, Skills exceed 1,700 |
| February 12 | Security release 2026.2.12 patches 40+ vulnerabilities |
| February 13 | Baidu integrates OpenClaw into its search app |
| February 15 | Founder joins OpenAI, project moves to a Foundation |

This is not the end — it is the beginning of the AI agent era.

In 30 days, OpenClaw proved that a solid agent architecture + an active skills ecosystem + a low-friction interaction model can take AI from a "chat window" into the "real world." It also proved that this path is littered with security landmines requiring the entire industry's collective effort.

If you have not started paying attention to AI agents, now is the time. Wherever OpenClaw ultimately goes, the door it opened will not close again.

## Related Reading

- [OpenClaw Architecture Deep Dive](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/)
- [OpenClaw Setup Tutorial: Build Your AI Assistant from Scratch](/posts/ai/2026-02-12-openclaw-usage-tutorial/)
- [OpenClaw + Claude Code Workflow in Practice](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)
- [Moltbook: When AI Agents Got Their Own Social Network](/posts/ai/2026-02-01-moltbook-ai-agent-social-network/)
- [Agent Skills: A New Programming Paradigm](/posts/ai/2026-01-19-agent-skills-new-programming/)
- [Claude Code Best Practices Guide](/posts/ai/2026-01-06-claudecode-best-practices/)
