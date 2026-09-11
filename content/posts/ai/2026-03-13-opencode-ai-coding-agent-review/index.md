+++
date = '2026-03-13T10:00:00+08:00'
draft = false
title = 'OpenCode Review: Can This Open Source AI Coding Agent Replace Claude Code?'
description = 'Hands-on review of OpenCode, the 121K-star open source AI coding agent with LSP integration, multi-model support, and client-server architecture. Honest comparison with Claude Code, Cursor, and Aider.'
toc = true
tags = ['OpenCode', 'AI Agent', 'Coding Tools', 'CLI', 'Developer Tools']
keywords = ['OpenCode review', 'open source coding agent', 'OpenCode vs Claude Code', 'AI coding tool comparison', 'terminal AI assistant', 'LSP AI integration']
+++

![OpenCode open source AI coding agent terminal interface and architecture overview](cover.webp)

Every developer building with AI coding agents eventually hits the same wall: vendor lock-in. Claude Code only works with Anthropic models. Cursor ties you to their subscription. GitHub Copilot lives inside VS Code. [OpenCode](https://github.com/anomalyco/opencode) takes a different path — it's MIT-licensed, supports 75+ model providers, and runs anywhere from your terminal to a desktop app. With 121K GitHub stars and a release cadence measured in days, it's the fastest-growing open source AI coding agent in 2026.

But does open source actually mean better? I spent two weeks using OpenCode as my primary coding agent to find out. Here's what I learned — the genuine strengths, the rough edges, and who should actually switch.

## Who Built OpenCode (and Why It Matters)

OpenCode is built by [Anomaly](https://github.com/anomalyco), the same team behind [SST](https://github.com/sst/sst) (Serverless Stack, 25K+ stars). The lead developer is Dax (thdxr), who is also behind terminal.shop and OpenAuth.

The README describes the creators as "neovim users and the creators of terminal.shop." This is worth clarifying: they are Neovim **users and sponsors**, not core Neovim developers. Terminal.shop is a fun novelty project — ordering coffee via SSH terminal. The SST pedigree, however, is real and significant: they've shipped production infrastructure tooling used by thousands of companies.

### The Naming Controversy

There's an awkward backstory. The name "OpenCode" was originally used by [Kujtim Hoxha's Go-based TUI tool](https://github.com/opencode-ai/opencode), which had 11K+ stars. When Anomaly launched their own project under the same name, the original was archived and continued as "Crush" under Charm. This caused friction in the community. Whether this matters to you depends on your views about open source etiquette, but it's context worth knowing.

## Architecture: The Client-Server Difference

Most AI coding agents are monolithic — the UI and the agent runtime are tightly coupled. OpenCode separates them with a client-server architecture:

```
┌─────────────────┐          ┌──────────────────┐          ┌─────────────────┐
│   Client Layer   │  HTTP   │   Agent Server    │          │  External Tools │
│                  │◄───────►│   (port 4096)     │◄────────►│                 │
│ • Terminal TUI   │         │ • Agent runtime   │          │ • LSP servers   │
│ • Desktop (Tauri)│         │ • Tool execution  │          │ • MCP servers   │
│ • IDE extensions │         │ • Session mgmt    │          │ • Git, Docker   │
│ • Web interface  │         │ • Context mgmt    │          │ • 75+ LLMs      │
└─────────────────┘          └──────────────────┘          └─────────────────┘
```

**What this enables in practice:**

- Run the server on a beefy workstation, connect from a lightweight laptop
- Multiple team members can potentially connect to the same agent session
- The desktop app (built with Tauri, not Electron) and TUI share the same backend
- mDNS support for automatic local network discovery

Here's what the server configuration looks like in `opencode.json`:

```json
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "cors": {
      "origins": ["http://localhost:*"]
    }
  }
}
```

**The trade-off nobody talks about:** This architecture introduced a [critical unauthenticated RCE vulnerability](https://github.com/anomalyco/opencode/issues/6355) (CVSS ~10). Any website could execute arbitrary code as the current user if OpenCode was installed, because the local server was accessible without authentication. This has reportedly been patched, but it's a reminder that client-server architecture in local dev tools creates an attack surface that monolithic tools simply don't have.

## LSP Integration: The Genuine Differentiator

This is where OpenCode genuinely outshines every other terminal-based AI coding agent. Most tools (including [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/)) rely on reading files and running grep to understand your code. OpenCode connects directly to Language Server Protocol servers — the same protocol your IDE uses for autocomplete, go-to-definition, and error checking.

### How It Actually Works

When you run `/init` in a project, OpenCode:

1. Detects your project's languages and frameworks
2. Downloads and starts the appropriate LSP servers (supports ~40 languages)
3. Feeds real-time diagnostics back to the LLM

Here's the real magic — the **self-correction loop**:

```
Agent writes code
       ↓
LSP analyzes the change instantly
       ↓
LSP reports: "Type 'string' is not assignable to type 'number' on line 42"
       ↓
Agent sees the diagnostic, fixes the error automatically
       ↓
LSP confirms: no more errors
       ↓
Agent moves on to the next task
```

This is fundamentally different from Claude Code's approach, where you'd need to run `tsc` or your linter manually to catch type errors. With OpenCode, the feedback loop is automatic and continuous.

**Real example**: Say you're refactoring a TypeScript function signature:

```typescript
// Before: function getUser(id: string): Promise<User>
// After:  function getUser(id: number): Promise<User>
```

Without LSP, the agent has no idea that 15 call sites now pass strings where numbers are expected. With OpenCode's LSP integration, the agent immediately sees 15 type errors and fixes them all — without you running `tsc` or pointing them out.

### LSP Configuration

The LSP setup is configured in `opencode.json`:

```json
{
  "lsp": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "filetypes": ["typescript", "typescriptreact", "javascript"],
      "root_markers": ["tsconfig.json", "package.json"]
    },
    "python": {
      "command": "pyright-langserver",
      "args": ["--stdio"],
      "filetypes": ["python"],
      "root_markers": ["pyproject.toml", "setup.py"]
    }
  }
}
```

**Caveat**: LSP support is still marked as experimental. Users report that it works well for TypeScript and Python but can be flaky with less common languages. It also adds memory overhead — expect an extra 200-500MB of RAM depending on the language server.

## Multi-Agent System: Specialized Workflows

OpenCode's agent system is similar in concept to [Claude Code's sub-agents](/posts/ai/2025-12-26-claudecode-skillsubagent/) but with a different design philosophy.

### Built-in Agents

| Agent | Type | Access Level | Use Case |
|-------|------|-------------|----------|
| **Build** | Primary | Full (read + write + execute) | Default development agent |
| **Plan** | Primary | Read-only | Code analysis, architecture review |
| **@general** | Subagent | Full | Complex multi-step research |
| **@explore** | Subagent | Read-only | Fast codebase search |

Switch between Build and Plan with `Tab`. Invoke subagents with `@general` or `@explore` in your prompt.

### Custom Agent Example

Create a file at `~/.config/opencode/agents/security-audit.md`:

```markdown
---
description: Security vulnerability scanner
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
permission:
  bash:
    "npm audit": allow
    "grep -r": allow
    "*": deny
---

You are a security auditor. Analyze the codebase for:
- SQL injection and XSS vulnerabilities
- Hardcoded secrets and credentials
- Insecure dependency versions
- Authentication/authorization flaws

Report findings with severity levels and remediation steps.
Never modify any files.
```

Then invoke it: `@security-audit Review the authentication module`

This is genuinely powerful. The granular permission model means you can create a security auditor that can read code and run `npm audit` but can never write files or execute arbitrary commands. Claude Code has [similar capabilities with custom sub-agents](/posts/ai/2026-02-28-claude-code-skills-guide/), but OpenCode's per-agent permission model is more explicit.

## Permission System: How It Compares

```json
{
  "permission": {
    "edit": "allow",
    "write": "allow",
    "bash": {
      "*": "ask",
      "git status": "allow",
      "git diff": "allow",
      "git log *": "allow",
      "git add *": "allow",
      "git commit *": "ask",
      "git push *": "ask",
      "npm test": "allow",
      "npm run build": "allow",
      "rm -rf *": "deny"
    },
    "webfetch": "deny"
  }
}
```

Three permission levels:
- **`allow`** — Execute without asking
- **`ask`** — Prompt for user confirmation
- **`deny`** — Block completely

This is more granular than Claude Code's permission system, which uses broader categories (allow all bash, ask all bash, or deny all bash). OpenCode lets you allow `git status` while requiring confirmation for `git push` — a practical distinction for day-to-day use.

## Model Support: The BYO Keys Advantage

OpenCode integrates with [Models.dev](https://models.dev) to support 75+ LLM providers. This means you can:

```json
{
  "provider": {
    "anthropic": {
      "api_key": "sk-ant-..."
    },
    "openai": {
      "api_key": "sk-..."
    },
    "ollama": {
      "base_url": "http://localhost:11434"
    }
  },
  "model": {
    "default": "anthropic/claude-sonnet-4-20250514",
    "plan": "openai/gpt-4o-mini",
    "general": "anthropic/claude-sonnet-4-20250514"
  }
}
```

**Practical benefit**: Use Claude Sonnet for complex coding, GPT-4o Mini for quick exploration, and a local Llama model for sensitive code that can't leave your machine — all within the same tool.

**GitHub Copilot trick**: If you have a GitHub Copilot subscription, you can route OpenCode through it — effectively getting a Claude Code-like experience using your existing subscription.

### OpenCode Zen

Zen is OpenCode's curated model service — a proxy that provides pre-tested model configurations optimized for coding agents. It starts at $20 (pay-as-you-go, auto-tops up when balance drops below $5). The claim is "zero markup pricing," meaning you pay exactly what the model providers charge. Whether this is strictly true is hard to verify, but the convenience of a single API key for all models is genuine.

## Honest Comparison: OpenCode vs Claude Code vs Cursor vs Aider

Having used all four tools extensively, here's my honest assessment:

| Aspect | OpenCode | Claude Code | Cursor | Aider |
|--------|----------|-------------|--------|-------|
| **Open source** | Yes (MIT) | No | No | Yes (Apache 2.0) |
| **Model flexibility** | 75+ providers | Anthropic only | Multi-model | Multi-model |
| **Interface** | TUI + Desktop + IDE | Terminal | IDE | Terminal |
| **LSP integration** | Native (~40 servers) | No native LSP | Via IDE | No |
| **Multi-agent** | Built-in | Built-in | Limited | No |
| **MCP support** | Yes | Yes (extensive) | No | No |
| **Context management** | Auto-compaction | Good manual + auto | Good | Best (explicit) |
| **Permission granularity** | Per-command | Per-category | Basic | Confirm each edit |
| **Maturity** | Young, fast-moving | Mature | Mature | Mature |
| **Security track record** | Had critical RCE | No major issues | No major issues | No major issues |
| **Desktop app** | Yes (Tauri) | No | Yes (Electron) | No |
| **Price** | Free + API keys | Max plan ~$100/mo | $20/mo | Free + API keys |

### Where OpenCode Wins

1. **LSP self-correction loop** — Genuinely produces fewer type errors and catches issues Claude Code would miss until you manually run the compiler
2. **Model freedom** — Use any model, switch between them per-task, avoid vendor lock-in
3. **Permission granularity** — Per-command permissions vs Claude Code's broader categories
4. **Desktop app** — Tauri-based (lighter than Electron), looks polished

### Where Claude Code Wins

1. **Maturity and reliability** — Fewer crashes, better error handling, more predictable behavior
2. **Context management** — Better at staying coherent in long sessions
3. **MCP ecosystem** — More extensive [MCP server support](/posts/ai/2026-02-28-claude-code-mcp-setup/) and community
4. **Security** — No history of critical vulnerabilities
5. **[Hooks system](/posts/ai/2026-02-28-claude-code-hooks-guide/)** — Powerful automation that OpenCode lacks
6. **Documentation** — Comprehensive and well-maintained

### Where Aider Wins

1. **Context control** — You explicitly decide what files the agent sees, leading to more predictable results
2. **Lightweight** — Minimal resource usage, fastest startup
3. **Git integration** — Auto-commits each change, making rollback trivial

## Real-World Usage: What 2 Weeks Taught Me

### What Worked Well

**TypeScript refactoring**: The LSP integration shined here. I renamed a core interface, and OpenCode's LSP caught every downstream type error across 40+ files. With Claude Code, I would have needed to run `tsc` after the change and feed the errors back manually.

**Quick model switching**: Debugging a tricky async issue, I started with GPT-4o Mini for fast exploration, then switched to Claude Sonnet for the actual fix. Seamless.

**Custom security agent**: The per-agent permission system made it easy to create a read-only security scanner that couldn't accidentally modify production code.

### What Didn't Work

**Long sessions degraded**: After ~100K tokens of context, responses became slower and less coherent. The auto-compaction exists but isn't as smooth as Claude Code's.

**Patch failures**: On 3 occasions in 2 weeks, OpenCode generated patches that didn't apply cleanly. It would then retry, sometimes making things worse. Claude Code's edit system is more reliable.

**Documentation gaps**: Many configuration options are undocumented or only documented in GitHub issues. I spent 30 minutes figuring out LSP configuration that should have been a 2-minute docs lookup.

**Memory usage**: With TypeScript LSP running, OpenCode consumed ~1.2GB of RAM compared to Claude Code's ~400MB.

## Getting Started

```bash
# Install (pick one)
curl -fsSL https://opencode.ai/install | bash
npm i -g opencode
brew install opencode

# Start in your project
cd my-project
opencode

# First-time setup
/connect anthropic    # or openai, ollama, etc.
/init                 # Detect project, start LSP servers
```

Essential keyboard shortcuts:
- `Tab` — Switch between Build and Plan agents
- `@` — Mention a subagent or file
- `Ctrl+Z` — Undo last change
- `/share` — Share session link

## Should You Switch?

**Switch to OpenCode if:**
- You want to use multiple model providers (especially local models for sensitive code)
- You're a TypeScript/Python developer who'd benefit from LSP self-correction
- You want maximum customization over agent behavior and permissions
- You philosophically prefer open source tools

**Stay with [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) if:**
- You value stability and maturity over cutting-edge features
- You're heavily invested in the [MCP ecosystem](/posts/ai/2026-02-28-claude-code-mcp-setup/)
- Security is a top priority (Claude Code's track record is cleaner)
- You prefer comprehensive documentation

**Consider [Aider](https://aider.chat) if:**
- You want explicit control over context and token usage
- You prefer lightweight tools with minimal overhead
- Git-native workflow matters to you

OpenCode is the most ambitious open source AI coding agent available today. Its LSP integration and model flexibility are genuine differentiators. But ambition comes with rough edges — the security history, documentation gaps, and stability issues in long sessions mean it's not yet a drop-in replacement for mature tools. It's one to watch closely, and for many workflows, it's already good enough to be your primary tool.

## Related Reading

- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — Deep dive into Anthropic's terminal-based AI coding agent
- [AI Coding Agents Comparison 2026](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/) — Side-by-side comparison of all major AI coding tools
- [Claude Code vs Cursor vs Windsurf](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/) — IDE-based vs terminal-based AI coding approaches
- [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) — Understanding the Model Context Protocol powering modern AI agents
- [Claude Code Skills and Sub-Agents](/posts/ai/2025-12-26-claudecode-skillsubagent/) — How Claude Code handles multi-agent workflows
