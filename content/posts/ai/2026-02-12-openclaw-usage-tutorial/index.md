+++
date = '2026-02-12T07:36:00+08:00'
draft = false
title = 'OpenClaw Tutorial: Complete Setup Guide for Beginners and Power Users'
description = 'Step-by-step OpenClaw tutorial covering installation, Gateway setup, TUI terminal, multi-agent configuration, session isolation, and troubleshooting for your personal AI assistant.'
toc = true
tags = ['OpenClaw', 'AI Agent', 'Telegram', 'Personal Assistant', 'Open Source']
categories = ['AI Guides']
keywords = ['OpenClaw tutorial', 'OpenClaw setup guide', 'AI agent gateway', 'Telegram AI bot', 'OpenClaw TUI', 'Moltbot tutorial', 'Clawdbot tutorial', 'OpenClaw multi-agent']

[[params.faqItems]]
question = "What is OpenClaw and what can it do?"
answer = "OpenClaw is an open-source AI Agent gateway that runs 24/7 and connects to messaging platforms like Telegram, WhatsApp, and Discord. It manages multiple AI agents, each with their own workspace, model, and tool permissions, enabling personal AI assistant workflows."

[[params.faqItems]]
question = "Is OpenClaw the same as Moltbot and Clawdbot?"
answer = "Yes, they are the same project at different stages. Clawdbot was the original name, Moltbot was a brief transitional name, and OpenClaw is the current official name with a unified repository and ecosystem."

[[params.faqItems]]
question = "How do I install OpenClaw on Mac?"
answer = "Install OpenClaw via npm with 'npm install -g openclaw', then run 'openclaw init' to create the configuration. You need Node.js 18+, an API key for your preferred AI model (Claude, GPT-4, etc.), and optionally a Telegram bot token for messaging integration."

[[params.faqItems]]
question = "Can OpenClaw use different AI models for different tasks?"
answer = "Yes. Each OpenClaw agent can be configured with a different AI model. For example, you can use Claude for coding tasks, GPT-4o for web research, and DeepSeek for writing — all managed through separate agent configurations in openclaw.json."

[[params.faqItems]]
question = "What is the OpenClaw TUI terminal?"
answer = "The TUI (Terminal User Interface) is OpenClaw's built-in interactive terminal that lets you chat with agents, switch between sessions, manage configurations, and monitor agent activity — all from a single terminal window without needing Telegram or other messaging apps."
+++

![OpenClaw complete tutorial cover](cover.webp)

Want a personal AI assistant that runs 24/7 and responds instantly on Telegram, WhatsApp, or Discord? [OpenClaw](https://github.com/openclaw/openclaw) is an open-source AI Agent gateway built exactly for this. This guide takes you from zero to proficient — whether you are a complete beginner or a power user looking to unlock multi-agent workflows.

## OpenClaw / Moltbot / Clawdbot — Same Project, Different Names

If you have seen three different names floating around, here is the short version: they are all the same project at different stages.

- **Clawdbot**: the original name (early viral phase)
- **Moltbot**: transitional name (used briefly after the rename)
- **OpenClaw**: current official name (unified repo and ecosystem)

**Rule of thumb**: use `OpenClaw` for current docs; expect `Moltbot` or `Clawdbot` in older resources.

> This guide targets macOS, Linux, and WSL2. Commands assume you are on the machine that will run the Gateway (e.g., a Mac mini or a VPS).
>
> Goal: go from zero to a working setup (web chat, Telegram, WhatsApp), learn the TUI, troubleshoot common issues, and explore multi-agent and security isolation.

---

## 0. Three Core Concepts You Need First

OpenClaw's mental model fits in one sentence:

- **Gateway**: a long-running background process that connects to Telegram, WhatsApp, web UI, manages sessions, and routes messages to agents.
- **Agent**: a conversational "persona" that handles dialogue and tool calls (`main`, `work`, `research`...). Each agent can have its own workspace, model, and tool permissions.
- **Session**: a conversation thread under a specific agent (e.g., `main`, `global`, or a channel-specific session key).

Everything you do revolves around: **start the Gateway, pick an agent/session, send messages through a channel**.

If you have followed the evolution from [ClawdBot](/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/) to [Moltbot](/posts/ai/2026-01-29-moltbot-deep-dive/) to OpenClaw, these concepts should be familiar.

---

## 1. Directory Layout: Where OpenClaw Stores Everything

### 1.1 Workspace

Default workspace path:

- `~/.openclaw/workspace`

This directory typically contains:

- `SOUL.md / USER.md / MEMORY.md`: your preferences, conventions, and long-term memory
- `memory/YYYY-MM-DD.md`: daily logs
- `skills/`: custom skills (e.g., a blog-writer skill)
- `tmp/`: temporary files

> The workspace serves a dual purpose: it is where OpenClaw reads your preferences **and** where it writes outputs like drafts, scripts, and documents.

For a deeper dive into how OpenClaw handles memory, see [OpenClaw Memory Implementation Strategy](/posts/ai/2026-01-31-openclaw-memory-strategy/).

### 1.2 Configuration File (openclaw.json)

Default location:

- `~/.openclaw/openclaw.json`

The file uses **JSON5** (comments and trailing commas allowed), with **strict schema validation** — a single typo in a field name will prevent the Gateway from starting.

### 1.3 State Directory

Default location:

- `~/.openclaw/`

This holds agent authentication and runtime state (e.g., `~/.openclaw/agents/main/...`).

---

## 2. Installation and Setup (Fastest Path)

> Already installed? Skip to Section 3.

### 2.1 Install the CLI

```bash
npm install -g openclaw@latest
# or
pnpm add -g openclaw@latest
```

Verify:

```bash
openclaw --version
openclaw help
```

For more installation details, see the [OpenClaw official documentation](https://docs.openclaw.ai/).

### 2.2 Run the Onboarding Wizard (Highly Recommended for Beginners)

```bash
openclaw onboard --install-daemon
```

The wizard walks you through:

- Model authentication (OAuth or API key)
- Basic Gateway configuration
- Channel setup (Telegram, WhatsApp, Discord...)
- Pairing and allowlist (secure defaults)
- Optional: install a background service (launchd on macOS)

If you have used the Moltbot Wizard before, this experience is similar but more polished. See [Moltbot Wizard Complete Guide](/posts/ai/2026-01-28-moltbot-wizard-guide/) for reference.

---

## 3. Gateway: Start, Monitor, and Manage

### 3.1 Start the Gateway (Foreground)

```bash
openclaw gateway --port 18789
```

Default console UI:

- http://127.0.0.1:18789/

> Power user note: if you are using Telegram or WhatsApp, **run with Node, not Bun** — there are known compatibility issues with Bun.

### 3.2 Check Gateway Status (Background Service)

```bash
openclaw gateway status
```

### 3.3 Quick Health Check

```bash
openclaw status
openclaw health
```

For deeper diagnostics:

```bash
openclaw status --all
openclaw status --deep
```

### 3.4 Follow Logs (First Thing to Check When Something Breaks)

```bash
openclaw logs --follow
```

### 3.5 Doctor: Auto-diagnose, Migrate, and Repair

```bash
openclaw doctor
# Use --fix only when auto-repair is needed (modifies config/state)
openclaw doctor --fix
```

---

## 4. Three Ways to Interact with OpenClaw

This is where beginners often get confused. There are three distinct interfaces.

### 4.1 Web Console (Dashboard)

The fastest way to start chatting:

```bash
openclaw dashboard
```

Or open directly:

- http://127.0.0.1:18789/

Best for:

- First-time verification that everything works
- Quick conversations without configuring any channel
- Visual configuration and session inspection

### 4.2 Terminal UI (TUI)

As long as the Gateway is running:

```bash
openclaw tui
```

Connect to a remote Gateway:

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

#### 4.2.1 Key TUI Concept: Session and Delivery

- By default, TUI sends messages to the Gateway **but does not deliver them to chat platforms**.
- To have replies actually sent back to Telegram or WhatsApp:
  - In the TUI: `/deliver on`
  - Or at startup: `openclaw tui --deliver`

This is a deliberate safety feature — **accidentally sending test messages to a group chat is a common beginner mistake**.

#### 4.2.2 TUI Keyboard Shortcuts (Worth Memorizing)

- `Enter`: send message
- `Esc`: abort current run
- `Ctrl+C`: clear input (press twice to exit)
- `Ctrl+D`: exit
- `Ctrl+L`: model selector
- `Ctrl+G`: agent selector
- `Ctrl+P`: session selector
- `Ctrl+O`: toggle tool output collapse
- `Ctrl+T`: toggle thinking visibility (reloads history)

#### 4.2.3 TUI Slash Commands (Most Used)

- `/help`: help
- `/status`: current connection, session, and model info
- `/agent <id>`, `/agents`
- `/session <key>`, `/sessions`
- `/model <provider/model>`, `/models`
- `/think off|minimal|low|medium|high`
- `/verbose on|full|off`
- `/reasoning on|off|stream`
- `/deliver on|off`
- `/new` or `/reset`

#### 4.2.4 Power User Trick: Run Local Shell Commands from TUI

Inside the TUI, prefix any command with `!`:

```text
! pwd
! ls -la
! openclaw status
```

Notes:

- First use prompts for authorization (once per session)
- Each `!` command runs in an **independent non-interactive shell** (no state carried between commands)

This is incredibly useful for troubleshooting — you can chat with the AI and run diagnostics in the same interface.

### 4.3 CLI Message Sending (Script-Friendly)

```bash
openclaw message send --channel telegram --target @your_chat --message "hello"
```

Best for:

- Automation and scripting
- CI/CD pipelines
- Verifying outbound channel connectivity

---

## 5. Configuration: What Beginners Should Change and Power User Tricks

### 5.1 Three Things Beginners Should Configure First

1. **Who can trigger the bot via DM** (`allowFrom` / `pairing`)
2. **Whether group messages require an @mention** (`requireMention`)
3. **Workspace path** (`workspace`)

### 5.2 Power User Trick 1: Isolated Environments with `--profile`

OpenClaw supports profiles that isolate state and config into:

- `~/.openclaw-<name>`

For example, create a lab environment that does not affect production:

```bash
openclaw --profile lab gateway --port 19001
openclaw --profile lab tui --url ws://127.0.0.1:19001
```

You can also use:

- `--dev`: development isolation mode (port offsets automatically)

### 5.3 Power User Trick 2: Configuration Splitting with `$include`

When your config grows large (multiple agents, channels, allowlists), split it up.

`~/.openclaw/openclaw.json`:

```json5
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  channels: { $include: "./channels.json5" },
}
```

Benefits:

- Cleaner structure
- Easier auditing
- Git-friendly

### 5.4 Power User Trick 3: Multi-Agent Routing

Run multiple "personas" under a single Gateway:

- `work`: only triggered from work groups, stricter tool permissions
- `personal`: full permissions for private chats
- `research`: dedicated to search and summarization

The key config sections:

- `agents.list[]`: define multiple agents
- `bindings[]`: route specific channels, accounts, groups, or DMs to different agents

> Decide on your division of labor first, then build the routing config around your actual channels (Telegram groups, DMs, etc.).

For more on the author's own development philosophy and workflow, see [OpenClaw Author's Claude Code Development Methodology](/posts/ai/2026-01-31-openclaw-claude-code-workflow/).

### 5.5 Power User Trick 4: DM Session Isolation (Prevent Context Leakage)

A common security warning from `openclaw status`:

- "Multiple Telegram DMs may share the main session, potentially leaking context"

Solution: set DM scope to per-user isolation (typically in the `session` / `messages` / `channels` section — exact field names vary by version).

---

## 6. Daily Usage Patterns: From "Working" to "Working Well"

### 6.1 Recommended Beginner Workflow

1. Start with the Dashboard (fastest verification):
   - `openclaw dashboard`
2. Move to TUI to build command-line muscle memory:
   - `openclaw tui`
3. Then connect Telegram or WhatsApp — avoid permission and pairing issues on day one.

This progressive approach also applies to other AI tools. For more workflow tips, see [AI Workflow Practical Guide](/posts/ai/2026-01-30-ai-workflow-real-guide/).

### 6.2 Three Settings to Reduce Noise

- Group chats: `requireMention: true`
- Keyword-only triggers: configure `mentionPatterns`
- Inbound debounce: merge rapid consecutive messages (`messages.inbound.debounceMs`)

### 6.3 Three Settings to Make the Bot Feel Like a Teammate

- `messages.ackReaction`: acknowledge receipt with an emoji reaction
- `messages.responsePrefix`: auto-prepend context (e.g., model name or thinking level)
- Multi-agent setup: one agent for writing, one for research, one for ops

---

## 7. Automation and Reminders (Advanced but Practical)

OpenClaw supports cron-based scheduling for reminders and recurring tasks:

- One-time: e.g., remind me in 20 minutes
- Recurring: e.g., every day at 9 AM

You can set these up conversationally — just tell the AI the time, content, and destination channel.

---

## 8. Troubleshooting Checklist (Covers 90% of Issues)

### 8.1 Bot Is Not Responding

1. Check if the Gateway is running:

```bash
openclaw gateway status
openclaw status
```

2. Check the logs:

```bash
openclaw logs --follow
```

3. Check channel status:

```bash
openclaw status --deep
```

4. If you are using the TUI, make sure delivery is enabled:

- In TUI: `/deliver on`

### 8.2 Bad Config Prevents Gateway from Starting

- Run `openclaw doctor` to identify schema errors
- Restore from backup: `~/.openclaw/openclaw.json`
- After fixing: `openclaw gateway restart`

### 8.3 Tool Process Killed by SIGKILL

This usually is not an OpenClaw bug. Common causes:

- Command ran too long and was killed externally
- You closed the terminal or session
- The OS reclaimed the process

What to do:

- Check `openclaw logs --follow` for the real reason
- Run long tasks in the background or break them into smaller steps

### 8.4 FAQ: Are Moltbot and OpenClaw the Same Project?

Yes. They represent different naming stages of the same codebase and ecosystem:

- Early resources use **Clawdbot**
- Transitional period uses **Moltbot**
- Current official name is **OpenClaw**

Seeing all three names in search results is normal. Always defer to the official OpenClaw repository and docs.

---

## 9. Quick Reference Card (Bookmark This)

### 9.1 Daily Essentials

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw tui
openclaw dashboard
```

### 9.2 Troubleshooting Essentials

```bash
openclaw status --all
openclaw status --deep
openclaw doctor
openclaw health
openclaw security audit --deep
```

### 9.3 Multi-Environment Commands

```bash
openclaw --profile lab status
openclaw --profile lab gateway --port 19001
openclaw --profile lab tui --url ws://127.0.0.1:19001
```

---

## 10. Ready-to-Use openclaw.json Template (Telegram DM Only)

> Scenario: **Telegram private chats only**, no groups, single `main` agent.
>
> Goals:
> - **Per-user DM session isolation** (prevent context leakage between different conversations)
> - **Groups disabled** (simplest setup)
> - **Single `main` agent** (keep it simple)

Save the following to `~/.openclaw/openclaw.json` (JSON5 format — comments and trailing commas are valid):

```json5
{
  gateway: {
    port: 18789,
    // auth: { token: "Optional: add if you need console/remote auth" },
  },

  // Key: DM session isolation (per channel + per peer user)
  session: {
    dmScope: "per-channel-peer",
  },

  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      sandbox: { mode: "off" },
    },
    list: [{ id: "main", default: true }],
  },

  channels: {
    telegram: {
      enabled: true,
      // botToken: "Should already be set via wizard or env var; can also be placed here",

      // Safest: strangers must pair first before messages are processed
      dmPolicy: "pairing",

      // Groups disabled for now
      groupPolicy: "disabled",

      // Optional: disable link previews if preferred
      linkPreview: true,
    },
  },

  messages: {
    responsePrefix: "[openclaw]",
    // Optional: react on message receipt (Telegram supports this)
    // ackReaction: "👀",
  },
}
```

### Apply the Configuration

Restart the Gateway after making changes:

```bash
openclaw gateway restart
```

To verify session isolation works: use two different Telegram accounts to DM the bot, then ask each one "Who am I?" or "What did we just talk about?" — they should not share context.

> When you are ready to enable groups or split into a `work` agent, define your goals first, then add `groups` and `bindings[]` sections.

---

## 11. Configuration Verification and Rollback (Your Safety Net)

This section answers three common beginner questions:

1. **Which config file is actually in use?**
2. **How do I confirm my changes took effect?**
3. **How do I roll back a broken config?**

### 11.1 Where Is the Config File?

Default path:

- `~/.openclaw/openclaw.json`

(On macOS, this expands to `/Users/<your-username>/.openclaw/openclaw.json`)

> Tip: if you use `--profile lab`, the config directory becomes `~/.openclaw-lab/` — do not edit the wrong one.

### 11.2 Confirm the Gateway Is Running with Your Latest Config

Three essential commands:

```bash
openclaw gateway status
openclaw status
openclaw logs --follow
```

- `openclaw gateway status`: confirms the service is alive
- `openclaw status`: overall health, channels, update notices
- `openclaw logs --follow`: shows **config validation errors** immediately after restart

### 11.3 How to Apply Config Changes

Config is loaded at startup, so you must restart:

```bash
openclaw gateway restart
```

If you are running in the foreground (not as a daemon):

- `Ctrl+C` to stop
- `openclaw gateway --port 18789` to start again

### 11.4 Use `openclaw config get/set/unset` for Safe Incremental Changes

OpenClaw provides config helper commands for small adjustments without editing the file directly:

Read values:

```bash
openclaw config get session.dmScope
openclaw config get channels.telegram.groupPolicy
```

Set values (use `--json` for non-string values):

```bash
# Disable Telegram groups
openclaw config set channels.telegram.groupPolicy disabled

# Set DM scope
openclaw config set session.dmScope per-channel-peer
```

Delete values:

```bash
openclaw config unset messages.responsePrefix
```

> Remember: changes still require `openclaw gateway restart` to take effect.

### 11.5 Backup and One-Command Rollback (Do This Now)

After your first successful run, back up the working config:

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
```

If you break the config (Gateway will not start, schema errors everywhere):

```bash
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
openclaw gateway restart
```

### 11.6 How to Diagnose Config Errors

OpenClaw uses **strict schema validation** — a single misspelled field will be rejected.

Debugging sequence:

1. Run the doctor:

```bash
openclaw doctor
```

2. Follow the logs to see exactly which field is wrong:

```bash
openclaw logs --follow
```

3. Collect full diagnostics if needed:

```bash
openclaw status --all
```

### 11.7 Common Beginner Config Mistakes

- **Treating JSON as JSON5**: JSON5 allows comments and trailing commas, but some editors auto-format to strict JSON, stripping comments and potentially breaking the structure.
- **Profile confusion**: `openclaw --profile lab ...` uses `~/.openclaw-lab/` — edits to `~/.openclaw/` will have no effect.
- **Forgetting to restart**: changes to the file do not take effect until you restart the Gateway.
- **Assuming TUI delivers to Telegram by default**: TUI does not deliver unless you explicitly run `/deliver on` or start with `--deliver`.

---

## Conclusion

OpenClaw's core value proposition is simple: **one local gateway connecting all your chat platforms to AI models**. Once you understand Gateway, Agent, and Session, combined with the TUI and Dashboard, you have everything you need.

For beginners, follow the **Dashboard, then TUI, then Telegram** progression. For power users, explore `--profile` isolation, `$include` config splitting, and multi-agent routing.

And remember the troubleshooting trifecta: `openclaw status`, `openclaw logs --follow`, and `openclaw doctor`. These three commands solve 90% of issues.

## Related Reading

- [ClawdBot: Build Your Personal AI Assistant in 30 Minutes](/posts/ai/2026-01-25-clawdbot-personal-ai-assistant/)
- [Moltbot Deep Dive: From Viral Hit to Rebrand — Opportunities and Pitfalls](/posts/ai/2026-01-29-moltbot-deep-dive/)
- [What Is Moltbot? Understand Its Purpose, Capabilities, and Risks in 3 Minutes](/posts/ai/2026-02-18-what-is-moltbot/)
- [Moltbot Wizard Complete Guide: Build Your Personal AI Assistant](/posts/ai/2026-01-28-moltbot-wizard-guide/)
- [OpenClaw Author's Claude Code Development Methodology](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)
- [OpenClaw Memory Implementation Strategy: Tool-Driven RAG and On-Demand Recall](/posts/ai/2026-01-31-openclaw-memory-strategy/)
- [Moltbook Deep Dive: The Bold Experiment of an AI Agent Social Network](/posts/ai/2026-02-01-moltbook-ai-agent-social-network/)
- [AI Workflow Practical Guide: From Prompts to Programming](/posts/ai/2026-01-30-ai-workflow-real-guide/)
