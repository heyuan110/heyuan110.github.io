+++
date = '2026-02-18T10:00:00+08:00'
lastmod = '2026-02-23T10:00:00+08:00'
draft = false
title = 'MoltBot Explained: What It Is, How It Works, and Why It Renamed to OpenClaw'
description = 'MoltBot (now OpenClaw) is an open-source personal AI agent that runs locally and executes real tasks via Telegram and WhatsApp. Learn its architecture, features, renaming history, and setup guide.'
toc = true
tags = ['MoltBot', 'AI Agent', 'OpenClaw', 'Clawdbot', 'Personal AI Assistant']
categories = ['AI Guides']
keywords = ['what is moltbot', 'moltbot ai agent', 'moltbot renamed openclaw', 'moltbot tutorial', 'moltbot vs claude code', 'openclaw setup guide', 'personal ai agent', 'moltbot architecture', 'moltbot security', 'openclaw features']
+++

If you have been seeing "MoltBot" pop up across tech communities and wondering what all the fuss is about, this article is for you.

**In one sentence: MoltBot (now renamed OpenClaw) is an open-source personal AI agent that runs on your own machine, takes commands through Telegram, WhatsApp, and other chat platforms, and actually executes tasks on your computer.**

It is not just another chatbot. It is an AI assistant that can take action. Below, we will break down exactly what MoltBot is, how it works, and whether you should use it.

---

## What Is MoltBot

### Basic Definition

MoltBot is an open-source personal AI assistant created by Austrian developer **Peter Steinberger**. Its core philosophy can be summed up in one line:

> **Turn AI from something that only talks into something that actually does things.**

Traditional AI tools like ChatGPT or Claude's web interface can only give you text-based suggestions. Ask them to "book a flight for tomorrow morning" and you get step-by-step instructions. MoltBot is different -- it can open a browser, log into your account, complete the booking, and send the confirmation back to you.

In more technical terms, MoltBot is an **Autonomous AI Agent** with these core characteristics:

- **Runs locally**: Deployed on your own computer or server, your data never leaves your device
- **Message-driven**: Interacts through Telegram, WhatsApp, Discord, iMessage, and other chat platforms
- **Autonomous execution**: Can run shell commands, control browsers, read/write files, and call APIs
- **Persistent memory**: Remembers your preferences, habits, and conversation history across sessions
- **Extensible skills**: Supports 5,700+ community skill plugins for virtually unlimited capabilities

### What Can MoltBot Actually Do

Here are concrete tasks MoltBot can handle:

| Use Case | What It Does |
|----------|-------------|
| **Email management** | Auto-classify emails, draft replies, forward important summaries |
| **Calendar** | Read your calendar, create meetings, send invitations |
| **Research** | Browse the web, read PDFs, compile research summaries |
| **File operations** | Organize folders, batch rename files, convert data formats |
| **Code assistance** | Execute scripts, deploy projects, monitor server status |
| **Daily life** | Compare prices, check in for flights, track deliveries |
| **Scheduled tasks** | Push morning news digests, run periodic backups |
| **Social media** | Post content, monitor mentions, organize comments |

One widely cited real-world example: a user claimed they "rebuilt their entire website via Telegram while watching Netflix on the couch."

### How Is It Different from ChatGPT or Claude

This is the most common source of confusion. Here is a quick comparison:

| Feature | ChatGPT / Claude Web | MoltBot |
|---------|---------------------|---------|
| **Where it runs** | Cloud (OpenAI / Anthropic servers) | Your own computer |
| **How you interact** | Browser web UI | Telegram / WhatsApp / etc. |
| **Capability boundary** | Text generation only | Can operate your computer and execute tasks |
| **Data privacy** | Data uploaded to cloud | Data stays local |
| **Persistent memory** | Limited (session-level) | Persistent (across days and weeks) |
| **Always on** | Requires you to open it | Runs in background 24/7 |
| **Cost** | Subscription ($20+/month) | Open source + API usage fees |

The core difference: **ChatGPT is a conversation tool. MoltBot is an execution engine.**

---

## Core Features

### Multi-Platform Messaging

MoltBot supports 12+ chat platforms simultaneously:

- Telegram (most popular, easiest to configure)
- WhatsApp
- Discord
- iMessage (requires macOS)
- Slack
- Signal
- Microsoft Teams
- Google Chat
- WebChat (built-in web interface)

You can send a message from any of these platforms and MoltBot will receive and act on it. This means you do not need to be sitting at your computer -- **you can command your AI assistant from anywhere**.

### Browser Automation

MoltBot controls browsers through the Chrome DevTools Protocol (CDP), handling virtually anything you would do manually:

- Open web pages, fill forms, click buttons
- Log into websites (using your stored credentials)
- Take screenshots and send them back to you
- Extract data from web pages

### Persistent Memory System

This is one of MoltBot's most valuable features. Its memory is stored as Markdown files on your local machine (`~/.clawdbot/` directory), including:

- **Conversation history**: Remembers what you said last week or last month
- **User preferences**: Knows your preferred email reply style and common workflows
- **Project context**: Understands background information about your ongoing projects
- **Learned behaviors**: Learns from mistakes and improves over time

Unlike ChatGPT's short-term memory, MoltBot's memory **persists across sessions, across days, and across weeks**. It does not forget everything when you close the chat window.

For a deeper look at the memory architecture, see [OpenClaw Memory Strategy Analysis](/posts/ai/2026-01-31-openclaw-memory-strategy/).

### Skill System

The skill system is the foundation of MoltBot's extensibility. As of February 2026, **the ClawHub marketplace has 5,700+ community-contributed skills** covering:

- Music control (Spotify integration)
- Note management (Obsidian integration)
- Email handling (Gmail integration)
- Code hosting (GitHub integration)
- Smart home control
- Financial trading and DeFi protocol integration
- Prediction market access

Each skill is essentially a **Markdown file + executable script** combination. The Markdown file describes the skill's purpose in natural language, while the script (Python, Bash, etc.) implements the actual functionality. The AI reads the Markdown description to decide when to invoke each skill.

Even more notably, MoltBot can **write new skills to extend its own capabilities** -- true agent self-evolution.

### Scheduled Tasks and Proactive Monitoring

Through cron integration and heartbeat mechanisms, MoltBot can act without waiting for your commands:

- Push morning news digests daily
- Monitor server status and alert you on anomalies
- Track stock prices and notify you at thresholds
- Periodically back up designated folders
- Check API health status

This transforms MoltBot from a passive responder into a **proactive executor**.

### Voice Interaction

MoltBot integrates with ElevenLabs voice services, supporting:

- Voice Wake
- Talk Mode (voice conversation)
- Always-on speech on macOS / iOS / Android

You can give MoltBot voice commands just like you would with Siri or Alexa.

---

## How MoltBot Works Under the Hood

### Architecture Overview

MoltBot's architecture has four distinct layers, each with a clear responsibility:

```
+--------------------------------------------------+
|              Your Device (Local)                  |
|                                                   |
|  +------------+    WebSocket     +--------------+ |
|  | Messaging  |<--------------->|   Gateway    | |
|  | Channels   |   ws://127.0.0.1|   Service    | |
|  | Telegram   |      :18789     |   :18789     | |
|  | WhatsApp   |                 +------+-------+ |
|  | Discord    |                        |         |
|  | iMessage   |                        v         |
|  | ...        |                 +--------------+  |
|  +------------+                 | AI Reasoning |  |
|                                 | Claude / GPT |  |
|                                 | / Local LLM  |  |
|                                 +------+-------+  |
|                                        |          |
|                                        v          |
|                                 +--------------+  |
|                                 | Tool Layer   |  |
|                                 | Browser Ctrl |  |
|                                 | File I/O     |  |
|                                 | Shell Exec   |  |
|                                 | Cron Jobs    |  |
|                                 | 5700+ Skills |  |
|                                 +--------------+  |
+--------------------------------------------------+
```

**Layer 1: Messaging Channels**
Receives messages from your various chat platforms and normalizes them into a unified format. Whether you send a message from Telegram or WhatsApp, it arrives at the Gateway in the same format.

**Layer 2: Gateway**
Runs at `ws://127.0.0.1:18789` and serves as the system's central nervous system. It manages all client connections, session authentication, and tool orchestration. This is what elevates MoltBot from a chatbot to an agent platform.

**Layer 3: AI Reasoning**
This is MoltBot's brain. After receiving a standardized message, it combines context (memory, available skills, system state) and uses a large language model (LLM) to decide what to do next. MoltBot uses a technique called **Mega Prompt** that dynamically fuses your instructions, available data, and system state to help the AI make optimal decisions.

MoltBot is model-agnostic and supports:
- **Cloud models**: Anthropic Claude (recommended), OpenAI GPT series, DeepSeek
- **Local models**: Open-source models like Llama via Ollama (free but less capable)

**Layer 4: Tool Execution**
Once the AI makes a decision, the tool layer handles actual execution -- browser control (CDP protocol), file operations, shell commands, HTTP requests, scheduled tasks, and more.

### Complete Request Flow

Here is what happens when you say "Check my emails today and summarize them":

```
1. You send a message on Telegram: "What important emails do I have today?"

2. Telegram Bot API pushes the message to your local Gateway

3. Gateway normalizes the message and passes it to the AI reasoning layer

4. AI reasoning layer checks memory (you use Gmail) and available skills,
   decides to invoke the "Gmail Read" skill

5. Tool layer calls the Gmail API to fetch today's emails

6. AI reasoning layer analyzes and summarizes the email content

7. Summary is returned through the Gateway to Telegram

8. You see the summary on your phone
```

The entire process typically takes 10-30 seconds, depending on email volume and API response times.

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | TypeScript |
| Package Manager | pnpm |
| Runtime | Node.js >= 22 |
| Browser Control | Chrome DevTools Protocol (CDP) |
| Communication | WebSocket |
| Memory Storage | Local Markdown files |
| Release Channels | stable / beta / dev (three-track) |

For a more detailed architecture breakdown, see [OpenClaw Architecture Deep Dive](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/).

---

## Renaming History: From Clawdbot to MoltBot to OpenClaw

The renaming story is itself a remarkable open-source community event -- **the project completed three name changes in under a week, arguably the fastest rebrand in open-source history**.

### Phase 1: Clawdbot (November 2025 - January 27, 2026)

The project originally launched as **Clawdbot**, created by Peter Steinberger in November 2025. "Clawd" is a phonetic play on "Claude" (lobster claw = Claw), since the project initially relied on Anthropic's Claude model.

The project went viral in mid-January 2026, **reaching 80,000+ GitHub stars in under a week**, making it one of the fastest-growing open-source projects at the time.

### Phase 2: MoltBot (January 27 - January 29, 2026)

On January 27, 2026, Anthropic requested a name change due to trademark similarity. "Clawd" and "Claude" were too visually and phonetically close, potentially causing confusion with official Anthropic products.

Steinberger renamed the project to **MoltBot**. "Molt" means shedding a shell -- a lobster must molt to grow. The name preserved the lobster mascot's spirit while symbolizing the project's transformation.

However, the renaming process triggered a serious security incident. When Steinberger renamed the GitHub organization and X (Twitter) handles, **a roughly 10-second window appeared between releasing the old handle and registering the new one**. Professional handle snipers immediately seized the released accounts, and cryptocurrency scammers used the hijacked "official" accounts to promote a fake token called $CLAWD. The token's market cap was pumped to $16 million within hours before crashing 90%.

### Phase 3: OpenClaw (January 29, 2026 - Present)

Just two days later on January 29, the project was renamed again to **OpenClaw**. The new name emphasizes two things:

- **Open**: The open-source spirit
- **Claw**: The lobster legacy

This rename also served as a clean break from the security incident during the previous transition.

### Latest Development: Founder Joins OpenAI

On February 15, 2026, Sam Altman announced that Peter Steinberger had joined OpenAI to lead development of "next-generation personal agents." Steinberger stated: "I want to change the world, not build a bigger company. Partnering with OpenAI is the fastest way to bring this vision to everyone."

The OpenClaw project will be transferred to an independent open-source foundation, supported by OpenAI, and remain open source.

For more analysis on this development, see [What OpenClaw's Founder Joining OpenAI Means](/posts/ai/2026-02-16-openclaw-openai-analysis/).

> **Renaming timeline**: Clawdbot (Nov 2025) -> MoltBot (Jan 27, 2026) -> OpenClaw (Jan 29, 2026). No matter which name you search for, they all refer to the same project.

---

## MoltBot vs Other AI Agents

2026 is the year of the AI agent, with numerous similar products flooding the market. Where does MoltBot (OpenClaw) fit in?

### Competitor Comparison

| Feature | MoltBot/OpenClaw | Claude Code | Manus | HyperWrite |
|---------|-----------------|-------------|-------|------------|
| **Positioning** | Personal all-in-one assistant | Developer coding assistant | General AI agent | Browser automation |
| **Open source** | Yes | No | No | No |
| **Runs where** | Self-hosted locally | Local terminal | Cloud | Browser extension |
| **Interface** | Chat platforms | Command line | Web UI | Browser |
| **Data privacy** | Data stays local | Code stays local | Data in cloud | Data in cloud |
| **Setup difficulty** | Medium (requires deployment) | Low (direct install) | Low (web access) | Low (install extension) |
| **Target audience** | Tech enthusiasts | Developers | Everyone | Everyone |
| **Persistent memory** | Yes (local files) | Yes (CLAUDE.md) | Limited | No |
| **Autonomous execution** | Strong (24/7 background) | Medium (requires terminal) | Strong | Medium |

### When Should You Choose MoltBot

**Good fit if you:**

- Value data privacy and do not want personal data uploaded to the cloud
- Have a device that can run 24/7 (Mac Mini, VPS, etc.)
- Need a unified assistant that works across email, calendar, browser, and file system
- Enjoy tinkering and customization
- Want an AI assistant that remembers your long-term preferences

**Not a good fit if you:**

- Have no technical background and do not want deployment hassles
- Only need a coding assistant ([Claude Code](/posts/ai/2026-01-14-claude-code-guide/) is a better choice)
- Have zero tolerance for security risks (MoltBot's security mechanisms are still maturing)
- Only occasionally need AI help (ChatGPT/Claude web interface is sufficient)

### The MoltBot Ecosystem

MoltBot is not just a single tool -- it has grown into an ecosystem:

- **OpenClaw**: The core agent project
- **MoltBook**: An AI agent social network with over 1.6 million registered AI agents, dubbed "the homepage of the agent internet"
- **MoltWorker**: Cloudflare's cloud-hosted version that eliminates the need for local hardware
- **ClawHub**: The skill marketplace with 5,700+ community-contributed plugins

To learn more about MoltBook, see [MoltBook: When AI Agents Get Their Own Social Network](/posts/ai/2026-02-01-moltbook-ai-agent-social-network/).

---

## Getting Started: Quick Setup Guide

### Hardware Requirements

MoltBot needs a device that runs 24/7. Recommended options:

| Option | Cost | Pros | Cons |
|--------|------|------|------|
| **Mac Mini M4** | ~$550 | Low power (6-8W), iMessage support | Higher upfront cost |
| **Cloud VPS** | ~$7-15/month | No local hardware needed | No iMessage support |
| **Old laptop/desktop** | $0 (already owned) | Zero cost | High power usage, noisy |
| **Raspberry Pi 5** | ~$70 | Ultra-low power, compact | Limited performance |

### Installation Steps

**Prerequisites**:
- Node.js >= 22
- pnpm (package manager)
- An LLM API key (Anthropic Claude recommended)

**One-line install**:

```bash
curl -sSL https://get.moltbot.org/install.sh | bash
```

The installer automatically detects your OS and handles configuration. After installation, MoltBot launches an interactive TUI (Terminal User Interface) that guides you through initial setup.

**Docker install** (recommended, more secure):

```bash
# Pull the image
docker pull openclaw/openclaw:latest

# Run the container
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  -e ANTHROPIC_API_KEY=your-api-key-here \
  openclaw/openclaw:latest
```

### Configuring Telegram

Using the most popular platform, Telegram, as an example:

```
Step 1: Search for @BotFather in Telegram, send /newbot to create a bot
Step 2: Obtain your Bot Token
Step 3: Enter the token in MoltBot's configuration
Step 4: Send your first message to your bot
```

In MoltBot's TUI, select "Messaging" -> "Telegram" and paste your Bot Token.

### Your First Conversation

Once configured, try sending this in Telegram:

```
Check my current disk usage
```

MoltBot will execute `df -h` and reply with the results in a readable format.

Try something more complex:

```
Write a Python script that checks if example.com is responding every hour,
and notify me via Telegram if it goes down
```

MoltBot will write the script, set up a cron job, and configure notifications -- all automatically.

### Security Configuration (Essential)

Before you start using MoltBot, **make sure** to complete these security steps:

```bash
# 1. Create a dedicated low-privilege user
sudo useradd -m -s /bin/bash openclaw-user
sudo su - openclaw-user

# 2. Restrict file access
chmod 700 ~/.openclaw

# 3. Configure firewall (if on a VPS)
# Only allow local access to the Gateway port
sudo ufw deny 18789
sudo ufw allow from 127.0.0.1 to any port 18789
```

For a detailed security deployment guide, see the security section in [MoltBot Deep Dive](/posts/ai/2026-01-29-moltbot-deep-dive/).

---

## Security Risks and Considerations

MoltBot is powerful, but "an AI that can operate your computer" is inherently a double-edged sword. You must understand these risks before using it:

### Known Security Concerns

1. **Plaintext credential storage**: API keys and OAuth tokens are stored as plaintext in local files
2. **Prompt injection attacks**: Malicious emails could trick MoltBot into executing unintended operations
3. **Reverse proxy authentication bypass**: Authentication may fail when running behind Nginx
4. **Info-stealer malware**: Malware specifically targeting MoltBot's local storage has been identified

Palo Alto Networks called MoltBot a security "deadly trifecta": it has access to private data, is exposed to untrusted content, and can perform external communications while retaining memory.

### Security Best Practices

| Principle | Implementation |
|-----------|---------------|
| **Least privilege** | Never run as root; create a dedicated low-privilege user |
| **Progressive authorization** | Start with read-only permissions; expand gradually after confirming safety |
| **Network isolation** | Never expose ports to the public internet; use firewalls |
| **Containerization** | Prefer running in Docker to limit access scope |
| **Regular audits** | Periodically review credential files in `~/.openclaw/` |
| **Model selection** | Claude Opus 4.5 has relatively stronger prompt injection defenses |

For more on automation security pitfalls, see [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/).

---

## Conclusion

MoltBot (now OpenClaw) represents a significant direction in AI development: **the leap from conversational AI to action-oriented AI**. It transforms AI from a tool that merely answers questions into a digital assistant that genuinely executes tasks on your behalf.

From its creation in November 2025 to its founder joining OpenAI in February 2026, this project experienced explosive growth, three name changes, a crypto scam, security controversies, and a commercial transition -- all within a few months. Its story is a microcosm of the AI agent era.

For most people, **MoltBot's significance lies not in whether you need to use it immediately, but in the new human-computer interaction paradigm it demonstrates** -- AI running continuously in the background, remembering all your preferences, always ready to work for you. This direction will very likely become the mainstream form of AI products in the coming years.

---

## Frequently Asked Questions

### Are MoltBot and OpenClaw the same thing?

Yes. MoltBot went through three name changes: Clawdbot -> MoltBot -> OpenClaw. The current official name is OpenClaw, but many people still refer to it as MoltBot. The codebase and functionality are identical -- only the brand name changed.

### Is MoltBot free?

OpenClaw (MoltBot) itself is open source and free to run on your own computer. However, it requires LLM API calls (such as Claude or GPT), which incur costs. The community edition is completely free, while the Pro edition offers additional cloud features and technical support.

### Is MoltBot safe? Will it leak my data?

MoltBot runs on your own computer, and data is not uploaded to any third-party servers by default. However, since it can execute shell commands and control browsers, improper use carries security risks. It is recommended to run it in a sandboxed environment and carefully review third-party skill plugins. For detailed security analysis, see [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/).

### What is the difference between MoltBot and Claude Code?

MoltBot (OpenClaw) is a general-purpose personal AI assistant that controls your computer through chat tools for everyday tasks. Claude Code is a professional AI coding tool focused on software development. They have different target audiences: MoltBot serves all users for life and work tasks, while Claude Code serves developers for coding scenarios. For a detailed comparison, see [Claude Code Complete Guide](/posts/ai/2026-01-14-claude-code-guide/).

---

## Related Reading

- [MoltBot Deep Dive: From Viral Hit to Renaming -- Opportunities and Risks of Personal AI Agents](/posts/ai/2026-01-29-moltbot-deep-dive/) - In-depth analysis
- [OpenClaw Architecture Deep Dive](/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) - Technical architecture breakdown
- [OpenClaw Usage Tutorial](/posts/ai/2026-02-12-openclaw-usage-tutorial/) - Hands-on tutorial
- [OpenClaw Memory Strategy Analysis](/posts/ai/2026-01-31-openclaw-memory-strategy/) - Memory system design
- [OpenClaw Automation Pitfalls](/posts/ai/2026-02-14-openclaw-automation-pitfalls/) - Common pitfalls guide
- [What OpenClaw's Founder Joining OpenAI Means](/posts/ai/2026-02-16-openclaw-openai-analysis/) - Latest developments
- [MoltBook: When AI Agents Get Their Own Social Network](/posts/ai/2026-02-01-moltbook-ai-agent-social-network/) - Ecosystem expansion
- [ClawdBot Setup Guide](/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/) - Beginner installation tutorial
- [Claude Code Complete Guide](/posts/ai/2026-01-14-claude-code-guide/) - Another AI agent experience

---

## References

- [OpenClaw Official Site](https://molt.bot)
- [OpenClaw GitHub](https://github.com/moltbot/moltbot) (145,000+ Stars)
- [OpenClaw Documentation](https://docs.openclaw.ai/start/getting-started)
- [ClawHub Skill Marketplace](https://clawdhub.com)
- [TechCrunch: Everything You Need to Know About Clawdbot (MoltBot)](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/)
- [TechCrunch: OpenClaw Creator Joins OpenAI](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)
- [CNBC: From Clawdbot to MoltBot to OpenClaw](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html)
- [Palo Alto Networks: MoltBot Security Risk Analysis](https://www.paloaltonetworks.com/blog/network-security/why-moltbot-may-signal-ai-crisis/)
- [Cloudflare: MoltWorker Cloud Solution](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/)
