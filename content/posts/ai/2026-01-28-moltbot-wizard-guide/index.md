+++
date = '2026-01-28T23:30:00+08:00'
draft = false
title = 'Moltbot Wizard Setup Guide: Build Your Own Private AI Assistant'
description = 'Step-by-step guide to configuring Moltbot using the Wizard CLI. Set up Gateway, connect Telegram and WhatsApp, install Skills, and deploy your personal AI assistant.'
toc = true
tags = ['Moltbot', 'AI Assistant', 'Personal AI', 'Open Source', 'Clawdbot']
categories = ['AI Guides']
keywords = ['Moltbot setup guide', 'Moltbot Wizard configuration', 'personal AI assistant', 'Clawdbot tutorial', 'self-hosted AI bot']
+++

Imagine mentioning your AI in a group chat and having it book flights, check the weather, write code, and manage your schedule — all while remembering every conversation from last week. That is exactly what **Moltbot** delivers: a fully self-hosted, private AI assistant you actually own.

This guide walks you through the Moltbot Wizard — the interactive CLI that turns a complex multi-step setup into a few simple prompts.

## Why Moltbot?

### The Problem with Existing AI Assistants

We all use AI assistants daily — ChatGPT, Claude, Gemini. But they share a fundamental limitation: **you are a tenant, not the owner**.

- **No data ownership**: Your conversations and preferences live on someone else's servers
- **Limited integrations**: Want AI in your WeChat group? Not happening
- **Platform fragmentation**: Slack for work, Telegram for personal — each needs separate setup
- **No customization**: The AI's personality and capabilities are entirely platform-controlled

### How Moltbot Solves This

Moltbot (formerly Clawdbot, renamed due to trademark issues) is an open-source project created by PSPDFKit founder Peter Steinberger, with over 68,000 stars on GitHub.

Its core philosophy: **give you full control over your AI assistant**.

```
┌─────────────────────────────────────────────────────────────┐
│                       Your Device                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Moltbot Gateway                    │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │ Claude  │  │ GPT-5   │  │ Gemini  │  ...more    │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘            │   │
│  │       └────────────┼────────────┘                  │   │
│  │                    ▼                                │   │
│  │            ┌──────────────┐                        │   │
│  │            │   AI Agent   │ ← Your custom persona   │   │
│  │            └──────┬───────┘                        │   │
│  └───────────────────┼─────────────────────────────────┘   │
│                      ▼                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ WhatsApp│  │Telegram │  │ Discord │  │ iMessage│ ...   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
└─────────────────────────────────────────────────────────────┘
```

In short, Moltbot acts as an AI relay hub:
- **Upstream**: Connects to AI models (Claude, GPT, Gemini, etc.)
- **Downstream**: Connects to your messaging apps (WhatsApp, Telegram, Discord, etc.)
- **Core**: Your custom AI Agent with its own memory, skills, and personality

## What Is the Wizard?

### One-Command Configuration

Setting up Moltbot manually requires writing JSON configs, configuring API tokens for each platform, setting up daemons, debugging network connections, and installing dependencies. For non-technical users, that is a nightmare.

The **Wizard** is an interactive CLI tool that asks you questions step by step and handles all configuration automatically. Think of it as the "Next, Next, Finish" installer experience.

```bash
moltbot onboard
```

One command to start the magic.

### What Does the Wizard Configure?

| Component | Purpose | Why It Matters |
|-----------|---------|----------------|
| **Model Auth** | Configure API keys for Claude, GPT, etc. | Gives the AI its "brain" |
| **Workspace** | Set up the Agent's working directory | The Agent's "home" |
| **Gateway** | Configure port and authentication | The message routing hub |
| **Channels** | Connect WhatsApp, Telegram, etc. | Conversation entry points |
| **Daemon** | Background service installation | 24/7 availability |
| **Skills** | Install capability plugins | Extend what the AI can do |

## Prerequisites

### System Requirements

- **OS**: macOS, Linux, or Windows (WSL2 required)
- **Node.js**: Version 22 or higher
- **Network**: Access to your chosen AI provider's API

### Getting an API Key

You need at least one AI model API key. **Anthropic** (Claude) is recommended:

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account and generate an API key
3. Save the key — you will need it shortly

> **Tip**: If you already use the Claude Code CLI, the Wizard can automatically reuse its authentication credentials.

### Installing Moltbot

**Linux/macOS**:
```bash
curl -fsSL https://molt.bot/install.sh | bash
```

**Windows (PowerShell)**:
```powershell
iwr -useb https://molt.bot/install.ps1 | iex
```

Verify the installation:
```bash
moltbot --version
```

## Step-by-Step Wizard Walkthrough

### Launch the Wizard

```bash
moltbot onboard
```

You will see a mode selection screen:

```
? How would you like to proceed?
> QuickStart (recommended defaults)
  Advanced (full control)
```

### QuickStart vs Advanced

| Mode | Best For | What It Does |
|------|----------|--------------|
| **QuickStart** | Beginners, quick evaluation | Uses recommended defaults, minimal prompts |
| **Advanced** | Power users, custom setups | Full control over every setting |

For first-time users, choose **QuickStart**. The Wizard will automatically configure:
- Local Gateway on port 18789
- Token authentication (auto-generated)
- Allowlist mode for Telegram/WhatsApp

### Step 1: Choose Your AI Model

```
? Which model provider would you like to use?
> Anthropic API key (recommended)
  Anthropic OAuth (Claude Code CLI)
  OpenAI API key
  OpenAI Code (Codex) subscription
  Vercel AI Gateway (multi-model proxy)
  MiniMax M2.1
  Moonshot (Kimi K2)
  Skip
```

**Provider comparison**:

| Provider | Description | Best For |
|----------|-------------|----------|
| **Anthropic API key** | Direct Claude API access | Recommended for most users |
| **Anthropic OAuth** | Reuse Claude Code CLI auth | Existing Claude Code users |
| **OpenAI API key** | GPT model family | GPT users |
| **Vercel AI Gateway** | Multi-model proxy | Users wanting model flexibility |
| **Moonshot** | Kimi K2 model | Users in China |

After selecting "Anthropic API key", paste your key:

```
? Enter your Anthropic API key: sk-ant-api03-xxxxx
```

The Wizard automatically validates the key.

### Step 2: Set Up the Workspace

```
? Where should the agent workspace be?
> ~/clawd (default)
  Custom location
```

The workspace stores Agent configurations, memory, and sessions. The default `~/clawd` works well for most users.

Workspace structure:
```
~/clawd/
├── IDENTITY.md      # Agent persona definition
├── BOOT.md          # Startup instructions
├── TOOLS.md         # Available tool descriptions
├── SOUL.md          # Core behavior guidelines
└── sessions/        # Conversation history
```

### Step 3: Configure the Gateway

The Gateway is Moltbot's core — all messages pass through it.

```
? Gateway port: 18789
? Gateway bind address:
> loopback (127.0.0.1, recommended for single user)
  all interfaces (0.0.0.0, for remote access)
? Enable authentication?
> Yes (recommended)
  No
```

**Key concepts**:

The **Gateway** works like a home router — just as all internet traffic flows through the router, all messages flow through the Gateway.

**Loopback vs All Interfaces**:
- `loopback`: Only accessible from your machine — most secure
- `all interfaces`: Allows access from other devices — must be combined with authentication

**Why enable authentication?** Even on localhost, other programs running on your machine could potentially interact with the Gateway. Token authentication prevents unauthorized access.

### Step 4: Connect Messaging Channels

This is where Moltbot comes alive — bringing AI into your chat apps.

```
? Which channels would you like to set up?
  ◉ WhatsApp
  ◉ Telegram
  ◯ Discord
  ◯ Google Chat
  ◯ Signal
  ◯ iMessage
```

#### Configuring Telegram

If you selected Telegram, the Wizard will prompt:

```
? Enter your Telegram bot token:
```

How to get a Bot Token:
1. Search for `@BotFather` on Telegram
2. Send `/newbot`
3. Follow the prompts to name your bot
4. BotFather returns a token like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Paste the token into the Wizard

#### Configuring WhatsApp

WhatsApp requires QR code authentication:

```
? Set up WhatsApp now?
> Yes
  Skip for now
```

Select Yes and the terminal displays a QR code. Scan it with WhatsApp (Settings > Linked Devices).

> **Note**: WhatsApp pairing data is stored in `~/.clawdbot/credentials/whatsapp/`.

### Step 5: Install the Daemon

```
? Install as background service?
> Yes (recommended)
  No
? Runtime:
> Node (recommended)
  Bun
```

The daemon keeps Moltbot running in the background and starts it automatically on boot.

- **macOS**: Creates a LaunchAgent
- **Linux**: Creates a systemd user service

Choose Node as the runtime (Bun support is still maturing).

### Step 6: Install Skills

Skills are capability plugins that extend what your AI can do.

```
? Install recommended skills?
> Yes
  No
? Node package manager:
> npm
  pnpm
```

Recommended Skills include:
- **web_search**: Search the web
- **web_fetch**: Fetch and parse web pages
- **exec**: Execute system commands
- **browser**: Browser automation

### Setup Complete

After configuration, the Wizard shows a summary:

```
Configuration complete!

Gateway:     ws://127.0.0.1:18789
Workspace:   ~/clawd
Channels:    Telegram, WhatsApp
Model:       claude-sonnet-4-20250514

Next steps:
1. Run 'moltbot dashboard' to open the web UI
2. Send a message to your bot on Telegram or WhatsApp
3. Run 'moltbot status' to check system health
```

## Verifying Your Installation

### Check Status

```bash
moltbot status
```

Example output:
```
Gateway:     Running (ws://127.0.0.1:18789)
Agent:       Ready
Channels:
  Telegram:  Connected (@your_bot)
  WhatsApp:  Connected (+1 555xxxx)
Model:       claude-sonnet-4-20250514
```

### Open the Dashboard

```bash
moltbot dashboard
```

This opens `http://127.0.0.1:18789/` in your browser — the Moltbot web console where you can:
- Monitor conversations in real time
- Manage sessions
- Adjust Agent settings

### Send Your First Message

Open Telegram, find your bot, and send:

```
Hello! Tell me about yourself.
```

If everything is working, you will receive an AI response. Congratulations — your private AI assistant is live.

## Advanced Configuration

### Non-Interactive Installation

For automated server deployments, use `--non-interactive` mode:

```bash
moltbot onboard --non-interactive \
  --mode local \
  --auth-choice anthropic-api-key \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node
```

### Running Multiple Agents

A single Moltbot instance can run multiple Agents, each with its own workspace and sessions. For example, create separate work and personal Agents:

```bash
# Add a work Agent
moltbot agents add work --workspace ~/clawd-work

# Add a personal Agent
moltbot agents add life --workspace ~/clawd-life
```

Then use routing rules to direct messages from different channels to different Agents.

### Remote Mode

To run the Gateway on a VPS and connect locally:

```bash
# Run on your local machine
moltbot onboard --mode remote
```

Then enter the remote Gateway's WebSocket address:
```
? Remote Gateway URL: ws://your-vps-ip:18789
? Authentication token: your-token
```

### Modifying Configuration

After initial setup, use the `configure` command to change settings:

```bash
# Reconfigure everything
moltbot configure

# Reconfigure specific sections
moltbot configure --section gateway
moltbot configure --section channels
moltbot configure --section skills
```

## Troubleshooting

### Gateway fails to start — port already in use

```bash
# Check what is using the port
lsof -i :18789

# Change the port
moltbot configure --section gateway
```

### WhatsApp won't connect after scanning the QR code

1. Ensure your phone and computer are on the same network
2. Check firewall settings
3. Try re-pairing:
   ```bash
   moltbot channels login whatsapp
   ```

### Slow AI responses

1. Check network latency to your AI provider
2. Consider using a closer model provider
3. Configure a proxy if needed:
   ```bash
   export HTTPS_PROXY=http://your-proxy:port
   moltbot gateway
   ```

### How to customize the AI persona

Edit `IDENTITY.md` in your workspace:

```bash
cd ~/clawd
nano IDENTITY.md
```

Example persona:
```markdown
You are Alex's personal assistant, named "Jarvis".

Personality:
- Concise and well-organized responses
- Professional but friendly tone
- Remembers user preferences

Responsibilities:
- Schedule management
- Technical Q&A
- Writing and translation assistance
```

### Where are the configuration files?

| File | Location | Purpose |
|------|----------|---------|
| Main config | `~/.clawdbot/moltbot.json` | All settings |
| OAuth credentials | `~/.clawdbot/credentials/oauth.json` | OAuth auth data |
| WhatsApp data | `~/.clawdbot/credentials/whatsapp/` | WhatsApp sessions |
| Agent sessions | `~/.clawdbot/agents/<id>/sessions/` | Conversation history |

## Security Best Practices

Moltbot runs on your device with significant permissions. Follow these guidelines:

1. **Always enable Gateway authentication**, even in loopback mode
2. **Never expose the Gateway to the public internet** unless you fully understand the risks
3. **Keep Moltbot updated** to the latest version
4. **Be cautious with exec permissions** — this allows the AI to run system commands
5. **Audit Skill sources** — only install plugins from trusted providers

For group chat scenarios, enable sandbox mode:

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```

This isolates non-primary Agent sessions inside Docker containers.

## Summary

The Moltbot Wizard transforms a complex multi-step configuration into answering a few simple prompts. After following this guide, you should have:

- A clear understanding of Moltbot's architecture
- A fully configured instance via the Wizard
- Connected messaging channels (Telegram, WhatsApp, etc.)
- Knowledge of advanced configuration and troubleshooting

You now own a truly private AI assistant — one that knows you, remembers you, and works exclusively for you.

### Further Reading

- [Clawdbot (Moltbot): Build Your Own Private AI Assistant](/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/)
- [Claude Code Complete Guide](/posts/ai/2026-01-14-claude-code-guide/)

---

**References**:
- [Moltbot Official Documentation](https://docs.molt.bot/)
- [Moltbot Wizard Configuration Page](https://docs.molt.bot/start/wizard)
- [Moltbot GitHub Repository](https://github.com/moltbot/moltbot)
- [TechCrunch: Everything you need to know about Moltbot](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/)

## Related Reading

- [Moltbot Explained: 80K Stars, Renaming Drama & Security Guide](/posts/ai/2026-01-29-moltbot-deep-dive/) — Deep dive into Moltbot's architecture and security
- [MoltBot Explained: What It Is, How It Works, and Why It Renamed to OpenClaw](/posts/ai/2026-02-18-what-is-moltbot/) — The full story of the Moltbot-to-OpenClaw transition
- [OpenClaw Setup Guide: Install and Configure Your AI Agent](/posts/ai/2026-03-05-openclaw-setup-guide/) — Getting started with OpenClaw (the successor to Moltbot)
- [OpenClaw vs CrewAI vs AutoGPT 2026: 6 AI Agent Frameworks Compared](/posts/ai/2026-03-05-openclaw-vs-ai-agents/) — How OpenClaw compares to other agent frameworks
