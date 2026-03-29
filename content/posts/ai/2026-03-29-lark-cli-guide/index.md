+++
date = '2026-03-29T09:00:00+08:00'
draft = false
title = 'Lark CLI Complete Guide: Control Feishu with Terminal and AI Agents'
description = 'Lark CLI is the official command-line tool for Feishu/Lark Open Platform, covering 11 business domains with 200+ commands and 19 AI Agent Skills. Step-by-step guide from installation to real-world usage with Claude Code integration.'
toc = true
tags = ['Lark CLI', 'Feishu', 'AI Agent', 'Claude Code', 'CLI Tools', 'Open Source', 'Productivity']
keywords = ['Lark CLI', 'lark-cli install', 'Feishu CLI', 'AI Agent Feishu', 'Claude Code Feishu', 'Lark Open Platform', 'lark-cli tutorial']
+++

![Lark CLI - Feishu Command Line Tool](cover.png)

## The Problem

You get a request from your manager: export all meetings from next week's calendar, send a notification to 50 group chats, or batch-organize documents into the wiki. You end up clicking through the UI one by one, copying and pasting until your eyes glaze over.

Now with Lark CLI, a single terminal command handles it. Even better, it integrates directly with AI Agents like Claude Code — you describe what you want in natural language, and the AI does the rest. This guide covers everything from installation to advanced usage.

---

## What Is Lark CLI?

### One-Line Definition

> **Lark CLI** is the official command-line tool for the Feishu (Lark) Open Platform, developed and open-sourced by the larksuite team under the MIT license. It covers 11 business domains, provides 200+ curated commands and 19 AI Agent Skills. As of March 2026, it has 1.7k GitHub Stars ([source](https://github.com/larksuite/cli)).

In plain terms: it's a remote control for Feishu — manage calendars, messages, documents, spreadsheets, and more without opening a browser or app.

### Lark CLI vs Direct API Calls

| Dimension | Direct Feishu API | Lark CLI |
|-----------|------------------|----------|
| Learning curve | Write code, handle auth, pagination, errors | One-line commands |
| Authentication | Manual token refresh | Built-in OAuth, auto credential management |
| AI integration | Build Function Calling yourself | 19 Skills ready out of the box |
| Coverage | 2,500+ API endpoints (full) | 200+ curated commands + raw API fallback |
| Output formats | Parse JSON yourself | JSON / Table / CSV / Pretty |

### Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 1: Shortcuts (+ prefix)              │
│  Human & AI friendly, covers common tasks   │
│  e.g., lark-cli calendar +agenda            │
├─────────────────────────────────────────────┤
│  Layer 2: API Commands                      │
│  Maps 1:1 to Feishu API endpoints, 100+     │
│  e.g., lark-cli calendar events list        │
├─────────────────────────────────────────────┤
│  Layer 3: Raw API Calls                     │
│  Covers all 2,500+ Open Platform endpoints  │
│  e.g., lark-cli api GET /open-apis/...      │
└─────────────────────────────────────────────┘
```

---

## Prerequisites

| Dependency | Version | Notes |
|-----------|---------|-------|
| Node.js | v18+ recommended | Includes npm and npx |
| Go | v1.23+ (optional) | Only for building from source |
| Python 3 | Latest (optional) | Only for building from source |

```bash
node -v   # Should output v18.x.x or higher
npm -v    # Should output 9.x.x or higher
```

macOS users without Node.js:

```bash
brew install node
```

---

## Step-by-Step Installation

### Install Lark CLI

```bash
# Global install
sudo npm install -g @larksuite/cli

# Verify
lark-cli --version
# Output: lark-cli version 1.0.0
```

### Install AI Agent Skills

```bash
# Install all 19 Skills
npx skills add larksuite/cli -y -g

# Verify
npx skills list
```

Or install specific domains:

```bash
npx skills add larksuite/cli -s lark-calendar -y
npx skills add larksuite/cli -s lark-im -y
```

### Create a Feishu App

1. Visit [Feishu Developer Console](https://open.feishu.cn/app) and log in
2. Click "Create Enterprise Custom App"
3. Note the **App ID** and **App Secret** from "Credentials & Basic Info"

### Configure and Authenticate

```bash
# Initialize with your App ID and App Secret
lark-cli config init

# Authorize (auto-selects common permission scopes)
lark-cli auth login --recommend

# Verify login
lark-cli auth status

# Health check
lark-cli doctor
```

---

## 5 Commands Every Beginner Should Try

### View Today's Calendar

```bash
lark-cli calendar +agenda
```

### Search Contacts

```bash
lark-cli contact +search-user --query "John"
```

### Find Group Chats

```bash
lark-cli im +chat-search --query "Engineering"
```

### Explore API Schema

```bash
lark-cli schema
lark-cli schema calendar.events.instance_view
```

### Dry Run (Preview Without Executing)

```bash
lark-cli im +messages-send --chat-id oc_xxx --text "Test" --dry-run
```

---

## Advanced Usage

### Claude Code Integration

With Skills installed, Claude Code understands Feishu operations natively:

```
You: Check my meetings tomorrow
Claude Code: (runs lark-cli calendar +agenda for tomorrow)

You: Send a reminder to the dev chat about the 3pm meeting
Claude Code: (runs lark-cli im +messages-send)
```

### Output Format Control

```bash
lark-cli calendar +agenda --format table
lark-cli base records list --params '...' --format csv
lark-cli calendar events list --params '...' --format pretty
```

### Pagination

```bash
lark-cli base records list --params '...' --page-all
lark-cli im +chat-messages-list --chat-id oc_xxx --page-all --page-limit 5 --page-delay 500
```

### Identity Switching

```bash
lark-cli calendar +agenda --as user
lark-cli im +messages-send --chat-id oc_xxx --text "Notice" --as bot
```

### Raw API Calls

```bash
lark-cli api GET /open-apis/calendar/v4/calendars
lark-cli api POST /open-apis/im/v1/messages \
  --params '{"receive_id_type":"chat_id"}' \
  --data '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"hello\"}"}'
```

---

## All 19 AI Agent Skills

| Category | Skill | Purpose |
|----------|-------|---------|
| Core | `lark-shared` | Auth and config management |
| Domain | `lark-calendar` | Calendar and scheduling |
| Domain | `lark-im` | Messaging and group chats |
| Domain | `lark-doc` | Cloud documents |
| Domain | `lark-drive` | File and folder management |
| Domain | `lark-sheets` | Spreadsheet operations |
| Domain | `lark-base` | Bitable (multi-dimensional tables) |
| Domain | `lark-task` | Task management |
| Domain | `lark-mail` | Email operations |
| Domain | `lark-contact` | Contact directory |
| Domain | `lark-wiki` | Knowledge base |
| Domain | `lark-event` | Event subscriptions |
| Domain | `lark-vc` | Video conferencing |
| Specialized | `lark-whiteboard` | Whiteboard |
| Specialized | `lark-minutes` | Meeting minutes |
| Specialized | `lark-openapi-explorer` | API explorer |
| Specialized | `lark-skill-maker` | Custom Skill creation |
| Workflow | `lark-workflow-meeting-summary` | Meeting summary automation |
| Workflow | `lark-workflow-standup-report` | Standup report automation |

---

## FAQ

### Permission Error (EACCES) During Install?

Add `sudo` or configure npm global directory:

```bash
mkdir ~/.npm-global && npm config set prefix '~/.npm-global'
# Add to ~/.zshrc: export PATH=~/.npm-global/bin:$PATH
```

### Browser Won't Open During Auth Login?

Use `--no-wait` and copy the URL manually:

```bash
lark-cli auth login --recommend --no-wait
```

### Scope/Permission Errors?

```bash
lark-cli auth check      # Check current permissions
lark-cli auth scopes     # List available scopes
lark-cli auth login --domain calendar,im  # Login with specific domains
```

---

## Security Notes

1. **Credential storage**: Encrypted in OS keychain (macOS Keychain / Linux Secret Service)
2. **AI Agent risk**: Model hallucination and uncontrolled execution are inherent risks — use the connected Feishu bot as a **private assistant** only
3. **Injection protection**: Built-in input sanitization, but validate parameters in automation pipelines
4. **Least privilege**: Only authorize scopes you actually need
5. **Regular audit**: Use `lark-cli auth list` to review and `lark-cli auth logout` to clean up

---

## Summary

Lark CLI solves a real pain point: **Feishu operations are fragmented, and automation has a high barrier to entry**.

Its three-layer architecture (Shortcuts → API Commands → Raw API) covers everything from simple to complex. The 19 AI Agent Skills turn Feishu into a capability module for AI tools like Claude Code and Cursor — not just a CLI wrapper, but a bridge between AI and enterprise collaboration.

---

## Links

- [Lark CLI GitHub](https://github.com/larksuite/cli) (1.7k Stars, as of March 2026)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu API Documentation](https://open.feishu.cn/document/)

---

## Further Reading

- [Claude Code Complete Guide](/posts/ai/2026-01-14-claude-code-guide/) - Get started with Claude Code
- [Claude Code Skills Top 20](/posts/ai/2026-01-20-claude-code-skills-top20/) - More useful Skills
- [Claude Code Skill Development Guide](/posts/ai/2026-01-08-claudecode-skill-guide/) - Build your own Skills
- [AI Development Workflow](/posts/ai/2026-01-19-ai-dev-workflow/) - Integrate Lark CLI into your workflow
- [Terminal Tools Guide](/posts/macos/2025-01-22-terminal-tools-guide/) - Upgrade your terminal

---

If this guide helped you, share your experience in the comments!

---

> Updated March 2026 | Written for lark-cli v1.0.0
