+++
date = '2026-03-17T10:00:00+08:00'
draft = false
title = 'Chrome DevTools MCP Setup 2026: Fix "Opens New Window" + Port 9222 (Claude Code & Cursor)'
description = 'How to connect AI to your already-logged-in Chrome browser. Fix the new-window problem in 3 steps, configure remote debugging port 9222 on macOS, enable autoConnect on Chrome 146+, and solve the user-data-dir conflict. Works with Claude Code, Cursor, Windsurf.'
toc = true
tags = ['Chrome DevTools', 'MCP', 'AI Coding Tools', 'Claude Code']
keywords = ['Chrome DevTools MCP', 'chrome devtools mcp setup', 'chrome devtools mcp setup 2026', 'chrome devtools mcp not connecting', 'chrome remote debugging port 9222', 'chrome remote debugging port 9222 mac', 'autoConnect chrome mcp', 'chrome devtools mcp autoConnect', 'chrome devtools mcp user-data-dir', 'AI browser debugging', 'AI browser session login', 'claude code chrome mcp', 'chrome devtools mcp claude code', 'cursor chrome devtools mcp', 'mcp server chrome setup', 'how to connect AI to existing chrome browser']

[[params.faqItems]]
question = "What is Chrome DevTools MCP and which AI tools support it?"
answer = "Chrome DevTools MCP is an open-source MCP server built by the Google Chrome team that exposes 29 Chrome DevTools capabilities (console logs, network requests, performance traces, Lighthouse audits, JavaScript execution, screenshots) to AI coding assistants. It works with any MCP-compatible client, including Claude Code, Cursor, Windsurf, Cline, VS Code GitHub Copilot, and Gemini CLI."

[[params.faqItems]]
question = "Why does Chrome DevTools MCP open a new window every time instead of using my existing browser?"
answer = "By default the MCP server launches a fresh Chrome instance using its own user data directory at ~/.cache/chrome-devtools-mcp/chrome-profile-stable, so it has none of your cookies or login sessions. To connect to your existing logged-in browser, either use --autoConnect (Chrome 146+ stable) or start Chrome yourself with --remote-debugging-port=9222 and point the MCP server at it via --browserUrl http://127.0.0.1:9222."

[[params.faqItems]]
question = "How do I fix the user-data-dir conflict when starting Chrome with --remote-debugging-port=9222?"
answer = "Since Chrome 136, the --remote-debugging-port flag is silently ignored when Chrome runs on the default profile directory for security reasons. The fix is to (1) kill all existing Chrome processes with `killall -9 \"Google Chrome\"` on macOS or `taskkill /F /IM chrome.exe` on Windows, then (2) relaunch Chrome with both --remote-debugging-port=9222 AND --user-data-dir pointing to a non-default path like /tmp/chrome-debug-profile. Verify with `curl http://127.0.0.1:9222/json/version`."

[[params.faqItems]]
question = "autoConnect vs --browserUrl: which connection method should I use?"
answer = "Use --autoConnect for daily debugging on Chrome 146+ stable — it is the simplest, keeps your real browser profile, and requires no manual --user-data-dir setup. Use --browserUrl when you are on Chrome 145 or below, running inside Docker or a sandboxed environment, need fine-grained control over the debug port, or want to connect a remote MCP server to a local Chrome. Default mode (new instance) is only useful for CI/CD or testing public pages."

[[params.faqItems]]
question = "Does Chrome DevTools MCP work with Claude Code, Cursor, and Windsurf?"
answer = "Yes. For Claude Code run `claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect`. For Cursor, go to Settings → MCP → Add New MCP Server and paste the npx config. For Windsurf and Cline, add chrome-devtools to the MCP config JSON the same way. VS Code GitHub Copilot uses .vscode/mcp.json. All clients use the same underlying server binary, only the registration UI differs."
+++

![Chrome DevTools MCP connecting AI agent to browser for debugging](cover.webp)

Every developer using Chrome DevTools MCP hits the same wall: the AI agent opens a **brand new Chrome window** instead of connecting to your existing browser. Your login sessions? Gone. Your debugging context? Lost. You're staring at a blank Chrome instance while your actual work sits in another window.

This guide solves that problem. You'll learn the three connection methods for Chrome DevTools MCP, why the "new window" issue happens, and how to make your AI agent work with your **actual browser session** — including the critical `--user-data-dir` fix that most tutorials skip.

## What Is Chrome DevTools MCP?

Chrome DevTools MCP is a [Model Context Protocol](https://modelcontextprotocol.io/) server built by Google's Chrome team. Think of it as a bridge between your AI coding assistant (Claude Code, Cursor, Gemini CLI, Copilot) and Chrome's built-in debugging tools.

Without it, your AI agent is debugging blind — it can only guess what's happening in the browser based on your code. With Chrome DevTools MCP, the agent can:

- **See console errors** in real time
- **Inspect network requests** — headers, payloads, timing
- **Record performance traces** and analyze bottlenecks
- **Take screenshots** and accessibility snapshots
- **Run Lighthouse audits** automatically
- **Execute JavaScript** in the page context
- **Fill forms, click buttons, navigate pages** via Puppeteer

The [official GitHub repository](https://github.com/ChromeDevTools/chrome-devtools-mcp) has 29 tools available as of v0.19.0.

## The "New Window" Problem (And Why It Happens)

Here's what happens by default when you set up Chrome DevTools MCP:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

The MCP server launches a **fresh Chrome instance** with its own user data directory at `~/.cache/chrome-devtools-mcp/chrome-profile-stable`. This means:

- No cookies, no saved passwords, no login sessions
- Websites that detect WebDriver may block you entirely
- Your real browser and its DevTools context are completely separate

This is the safest mode — but also the least useful for real debugging. If you're trying to debug a page behind authentication or inspect an issue you've already reproduced, a blank browser is worthless.

## Three Ways to Connect (Choose the Right One)

Chrome DevTools MCP offers three connection methods. Here's when to use each:

| Method | Login State | Best For | Chrome Version |
|--------|------------|----------|----------------|
| **Default** (new instance) | None | Public pages, CI/CD | Any |
| **autoConnect** | Your sessions | Daily debugging | 146+ (stable) |
| **Manual** (`--browserUrl`) | Your sessions | Docker, sandboxed envs | Any |

### Method 1: autoConnect (Recommended for Daily Use)

Since Chrome 146 stable, you can use `--autoConnect` to connect directly to your running Chrome browser. No new window, no lost sessions.

**Step 1:** Enable remote debugging in Chrome. Open `chrome://inspect/#remote-debugging` and toggle the switch on.

**Step 2:** Configure the MCP server:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--autoConnect"]
    }
  }
}
```

For Claude Code users:

```bash
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect
```

**Step 3:** When the MCP server connects, Chrome shows a permission dialog. Click "Allow." A banner appears at the top saying "Chrome is being controlled by automated test software" — this is expected.

The AI agent now sees **every tab** in your Chrome profile. It can read your authenticated pages, inspect your DevTools selections, and take over exactly where you left off.

> **Note:** autoConnect was available since Chrome 144 but only in the Beta channel. Chrome 146 is the first **stable** release with this feature — no more `--channel=beta` needed.

### Method 2: Manual Connection via `--browserUrl` (The Deep Fix)

This is the method that solves the problem when autoConnect isn't available or when you need fine-grained control. It's also the approach used in Docker containers and sandboxed environments.

The core idea: you start Chrome yourself with a debugging port, then point the MCP server at it.

**But here's where most people get stuck.** They run something like:

```bash
# This usually FAILS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222
```

Chrome opens, port 9222 seems active, but `curl http://127.0.0.1:9222/json/version` returns a 404 or connection refused. The MCP server can't connect. Why?

#### The Three Reasons Your Connection Fails

**Reason 1: Chrome wasn't started in debug mode.**

A Chrome instance launched normally (double-clicking the icon) doesn't listen on the debugging port. The `--remote-debugging-port` flag only works when Chrome is launched from the command line with that flag **from the start**.

**Reason 2: An existing Chrome process is hogging the port.**

If you have Chrome already running and try to launch a new instance with `--remote-debugging-port=9222`, Chrome detects the existing process. Instead of starting a new one with debugging enabled, it simply sends a signal to the existing instance to open a new window. The debugging flag is silently **ignored**.

**Reason 3: User data directory conflict (the real killer).**

Even if you kill all Chrome processes and restart with `--remote-debugging-port=9222`, Chrome uses your **default user data directory**. Starting from Chrome 136, [Google changed the security model](https://developer.chrome.com/blog/remote-debugging-port): `--remote-debugging-port` is **ignored** when using the default profile directory. This is a security measure to protect your saved passwords and cookies from being exposed via the debugging protocol.

#### The Fix: Kill, Isolate, Verify

Here's the complete, working solution:

```bash
# Step 1: Kill ALL Chrome processes (critical — no survivors)
killall -9 "Google Chrome"

# Step 2: Launch Chrome with debug port AND a separate user data directory
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile
```

On Windows:

```powershell
# Kill all Chrome processes
taskkill /F /IM chrome.exe

# Launch with debug port and separate profile
"C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="%TEMP%\chrome-debug-profile"
```

**Step 3: Verify the connection works:**

```bash
curl http://127.0.0.1:9222/json/version
```

You should see a JSON response like:

```json
{
  "Browser": "Chrome/146.0.6814.46",
  "Protocol-Version": "1.3",
  "User-Agent": "...",
  "V8-Version": "...",
  "WebKit-Version": "...",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/..."
}
```

If you get this response, the debugging port is working. Now configure the MCP server:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9222"]
    }
  }
}
```

For Claude Code:

```bash
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --browserUrl http://127.0.0.1:9222
```

#### Why `--user-data-dir` Is Non-Negotiable

The `--user-data-dir` flag does two things:

1. **Bypasses the Chrome 136+ security restriction** — Chrome only enables remote debugging on non-default profiles
2. **Prevents instance conflicts** — A separate data directory means Chrome won't try to merge with an existing running instance

You can use any path: `/tmp/chrome-debug-profile`, `~/chrome-debug`, or even `$(mktemp -d)` for a truly disposable session. The MCP server itself uses `~/.cache/chrome-devtools-mcp/chrome-profile-stable` by default.

> **Pro tip:** If you want to keep your bookmarks and extensions in the debug profile, copy your default Chrome profile directory to the debug location once, then reuse it.

### Method 3: Default Mode (New Instance)

The simplest setup — the MCP server handles everything:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Use `--isolated` for a temporary profile that auto-cleans after the browser closes:

```json
{
  "args": ["-y", "chrome-devtools-mcp@latest", "--isolated"]
}
```

This is fine for testing public pages, running Lighthouse audits on staging URLs, or CI/CD pipelines. But for anything requiring authentication, use Method 1 or 2.

## Real-World Workflow: Debugging a Login-Protected Page

Here's a practical example showing why connecting to your existing browser matters.

**Scenario:** Your internal admin dashboard shows a blank page after a recent deployment. The page requires SSO login.

**Without autoConnect/browserUrl:**
1. MCP opens a new Chrome → SSO login page → MCP can't authenticate → Dead end

**With autoConnect:**
1. You're already logged into the admin dashboard in your browser
2. You notice the blank page and ask Claude Code: "Check the console and network tab for errors on this page"
3. Claude Code connects to your running Chrome, inspects the page, and finds a 403 on the `/api/config` endpoint
4. It reads the request headers, notices a missing authorization header, and traces it to a recent middleware change
5. You fix the code, Claude Code verifies the fix in real time — all in your existing browser session

This "human operates, AI analyzes" workflow is the real power of Chrome DevTools MCP.

## Configuration Quick Reference

All available CLI flags for `chrome-devtools-mcp`:

| Flag | Type | Description |
|------|------|-------------|
| `--autoConnect` | boolean | Connect to running Chrome (146+) |
| `--browserUrl` / `-u` | string | Connect to Chrome at URL (e.g., `http://127.0.0.1:9222`) |
| `--wsEndpoint` / `-w` | string | WebSocket endpoint for direct CDP connection |
| `--headless` | boolean | Run Chrome without UI |
| `--isolated` | boolean | Use temporary profile, auto-cleaned on close |
| `--user-data-dir` | string | Custom Chrome profile directory |
| `--executablePath` / `-e` | string | Path to Chrome binary |
| `--channel` | string | `stable`, `canary`, `beta`, or `dev` |
| `--viewport` | string | Browser size, e.g., `1280x720` |
| `--slim` | boolean | Expose only 3 essential tools (saves tokens) |
| `--no-usage-statistics` | boolean | Opt out of anonymous telemetry |

Run `npx chrome-devtools-mcp@latest --help` to see all options.

## MCP Client Setup for Popular Tools

### Claude Code

```bash
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect
```

### Cursor

Go to **Cursor Settings → MCP → Add New MCP Server**, then paste:

```json
{
  "command": "npx",
  "args": ["chrome-devtools-mcp@latest", "--autoConnect"]
}
```

### VS Code / GitHub Copilot

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--autoConnect"]
    }
  }
}
```

### Gemini CLI

```bash
gemini mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect
```

## What's New in v0.19.0

The latest version (paired with Chrome 146) brings significant upgrades:

- **Lighthouse integration** — Run performance and quality audits directly through MCP. Your AI agent can audit, identify issues, fix code, and re-audit in one loop
- **Slim mode** (`--slim`) — Only exposes 3 core tools, dramatically reducing token usage when you have multiple MCP servers loaded
- **Memory snapshots** — `take_memory_snapshot` helps diagnose memory leaks
- **Accessibility and LCP skills** — Specialized debugging for WCAG compliance and Core Web Vitals
- **Experimental screen recording** — Capture browser interactions as video

## Security Considerations

When using autoConnect or `--browserUrl`, your AI agent can access **all tabs** in the connected Chrome profile. This includes:

- Cookies and localStorage for every domain
- Authenticated sessions (banking, email, admin panels)
- Form data and saved passwords (if auto-filled)

**Practical safety rules:**

1. **Close sensitive tabs** before connecting — bank accounts, password managers, payment pages
2. **Review AI tool calls** before approving — most MCP clients show what the agent wants to do
3. **Use a dedicated Chrome profile** for AI debugging — separate from your personal browsing
4. **Disable telemetry** if working with proprietary code: add `--no-usage-statistics` and `--no-performance-crux`

## Troubleshooting

### "Connection refused" on port 9222

```bash
# Check if anything is listening on 9222
lsof -i :9222

# If another process owns it, kill it
kill -9 <PID>

# Restart Chrome with the correct flags
killall -9 "Google Chrome"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile
```

### autoConnect permission dialog keeps popping up

This is a [known issue](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md) with many tabs open. The MCP server re-enumerates tabs on each command. Consider [chrome-cdp-skill](https://github.com/pasky/chrome-cdp-skill) as an alternative — it maintains persistent WebSocket connections and only shows the dialog once.

### Chrome opens but debugging port returns 404

You likely have `--user-data-dir` pointing to the default profile. Since Chrome 136, the default profile **blocks** remote debugging. Use a different path:

```bash
--user-data-dir=/tmp/chrome-debug-profile  # Any non-default path works
```

### Node.js version error

Chrome DevTools MCP requires **Node.js v20.19+**. Check with:

```bash
node --version
```

## FAQ

**Q: Does autoConnect work on Chrome 144/145?**
A: Yes, but only on the Beta channel. You need to add `--channel=beta` to the MCP config. Chrome 146 is the first stable version with autoConnect support.

**Q: Can I use this with Firefox or Safari?**
A: No. Chrome DevTools MCP specifically uses the Chrome DevTools Protocol (CDP). Firefox has its own remote debugging protocol, and Safari uses Web Inspector Protocol. Neither is compatible.

**Q: Will the AI agent slow down my browser?**
A: Minimally. The MCP server communicates via CDP WebSocket, which adds negligible overhead. Performance traces do add some instrumentation, but only while actively recording.

**Q: Is `--user-data-dir` needed for autoConnect too?**
A: No. autoConnect uses Chrome's built-in remote debugging request API (introduced in Chrome 144), which doesn't require a separate user data directory. The `--user-data-dir` fix is only needed for the manual `--browserUrl` method.

## Related Reading

- [MCP Protocol Explained: How AI Agents Connect to External Tools](/posts/ai/2026-02-28-mcp-protocol-explained/) — Understanding the protocol behind Chrome DevTools MCP
- [Best MCP Servers for Claude Code in 2026](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — Chrome DevTools MCP alongside other essential servers
- [How to Build an MCP Server in Python](/posts/ai/2026-03-05-build-mcp-server-python/) — Build your own MCP server from scratch
- [Claude Code Browser Automation Guide](/posts/ai/2026-01-28-claude-code-browser-automation/) — Alternative browser automation approaches
- [MCP Security Guide: Protecting Your AI Tool Integrations](/posts/ai/2026-03-10-mcp-security-2026/) — Security best practices for MCP servers

## Series Navigation

This is Part 3 of the **Browser Automation for AI Agents** series — the arc from headless drivers, to attaching to your real browser, to cutting the token bill, to sharing your logged-in session:

1. [Vercel Agent Browser](/posts/ai/2026-01-13-vercel-agent-browser/) — a snapshot-driven CLI built for agents, not test suites
2. [Browser Automation in Claude Code: 5 Tools Compared](/posts/ai/2026-01-28-claude-code-browser-automation/) — the field map: token cost, speed, stability
3. **This article**: Chrome DevTools MCP Setup 2026 — attaching to your real browser, and the port 9222 traps
4. [Playwright CLI + Skills: 0-Token Automation](/posts/ai/2026-04-18-playwright-cli-skill-zero-token-automation/) — the pattern that removes the MCP token tax
5. [Claude Code Screenshot MCP Setup](/posts/ai/2026-07-21-claude-code-screenshot-mcp-frontend-debugging/) — the frontend debugging loop, 10,220 vs 65 tokens
6. [ubrowser Review](/posts/ai/2026-07-27-ubrowser-review/) — the right design trapped in an abandoned repo
7. ego lite Review: Your Logged-In Browser, Handed to Claude Code (coming next) — handing agents your logged-in session through Spaces
