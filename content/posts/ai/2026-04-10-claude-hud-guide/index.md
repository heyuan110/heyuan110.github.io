+++
date = '2026-04-10T10:00:00+08:00'
draft = false
title = "Claude HUD 2026: Claude Code's 18K-Star Status Bar in 3 Min"
description = 'Claude HUD is a free Claude Code plugin: a live status bar for context usage, rate limits, and agent activity. Install with one /plugin command in 3 minutes.'
toc = true
tags = ['Claude Code', 'Developer Tools', 'Productivity', 'AI Coding']
keywords = ['claude hud', 'claude-hud', 'claude code hud', 'claude hud install', 'claude hud setup', 'claude hud plugin', 'claude code statusline', 'claude code status bar', 'claude code context window', 'claude code plugin', 'claude code usage monitor', 'claude code rate limits']

[[params.faqItems]]
question = "What is Claude HUD?"
answer = "Claude HUD is an open-source Claude Code plugin that adds a real-time status bar showing context window usage, rate limits, tool activity, and agent status directly in your terminal."

[[params.faqItems]]
question = "How do I install Claude HUD?"
answer = "Run /plugin marketplace add jarrodwatts/claude-hud, then /plugin install claude-hud, then /reload-plugins, and finally /claude-hud:setup to configure it. Restart Claude Code afterwards and the status bar appears below your input. Total setup time is about 3 minutes."

[[params.faqItems]]
question = "Is Claude HUD free?"
answer = "Yes, Claude HUD is completely free and open-source under the MIT license. It has 18,000+ stars on GitHub."

[[params.faqItems]]
question = "Does Claude HUD work with API keys?"
answer = "Partially. Context window tracking works for all users, but rate limit tracking requires a Claude subscriber account (Pro/Max/Team). API key users have pay-per-token billing and no rate limits to display."

[[params.faqItems]]
question = "What is the difference between Claude HUD and ccstatusline?"
answer = "Claude HUD focuses on session observability with context health, agent tracking, and todo progress. ccstatusline focuses on visual customization with Powerline fonts, themes, and beautiful styling. Choose Claude HUD for functionality, ccstatusline for aesthetics."
+++

![Claude HUD adds real-time session monitoring to Claude Code terminal](cover.webp)

You know that moment when Claude Code starts repeating instructions you gave it ten minutes ago? Or when it produces code that contradicts a decision it made earlier in the same session? That is what context window saturation looks like—and without monitoring, you have zero warning before it happens.

I have been using Claude Code daily for months, and the single biggest improvement to my workflow was not a new model, not a better prompt strategy, not even a fancier CLAUDE.md file. It was installing [Claude HUD](https://github.com/jarrodwatts/claude-hud)—a plugin that shows me what is actually happening inside my session. Think of it as **htop for Claude Code**: where htop shows CPU usage, memory, and running processes, Claude HUD shows context health, active tools, subagent status, and task completion in real time.

With 18,000+ GitHub stars and 782 forks since its January 2026 launch, Claude HUD has become the most popular Claude Code plugin in existence. The community's reaction has been remarkably consistent: "Why isn't this built into Claude Code already?"

## The Problem: Flying Blind in a 200K Token Window

Claude Code's terminal interface gives you almost nothing about your session's internal state. You can type `/context` to check token usage, but that is a manual, interruptive command that tells you a number without any trend or warning. Here is what you are missing without monitoring:

**Context window degradation is gradual, then sudden.** At 85%+ context utilization, Claude's responses get noticeably "flaky"—it loses architectural decisions from earlier in the conversation, repeats itself, and makes mistakes it was getting right an hour ago. The problem is that you have no visual indicator of when you cross that threshold. You only notice when the output quality has already tanked.

**Rate limit surprises are expensive.** If you are on Claude Max ($100-200/month), your usage of claude.ai, Claude Code, and Claude Desktop all count toward the same rate limit. I have seen developers burn through their entire 5-hour allocation on a single Claude Code session without realizing it, then get throttled right when they needed to ship a fix. Without a usage bar staring you in the face, this happens more often than anyone admits.

**Agent activity is invisible.** When Claude Code spawns subagents—which it does routinely for complex tasks—you have no way to see how many are running, what they are doing, or how long they have been at it. A subagent stuck in a loop can silently eat your context and your rate limit while you wait, thinking everything is progressing.

## What Claude HUD Actually Shows You

Claude HUD renders a persistent status bar below your Claude Code input. Here is what the default two-line display looks like:

```
[Opus] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

Line 1 shows your model, project path, and git branch. Line 2 shows two critical gauges: your context window health (green → yellow → red as it fills) and your subscriber rate limit consumption.

Enable the optional lines and you get even more:

```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2        ← Tool activity
◐ explore [haiku]: Finding auth code (2m 15s)    ← Agent status
▸ Fix authentication bug (2/5)                   ← Todo progress
```

The key technical detail: Claude HUD uses **native token data from Claude Code**, not word-count estimates. It hooks into Claude Code's statusline API, which streams JSON data to the plugin on every tick (~300ms). It also parses the session transcript for tool and agent activity. No network calls, no background processes, no persistent state beyond your config file.

![Claude HUD architecture: how data flows from Claude Code through the plugin to your status bar](02-architecture-data-flow.webp)

## Installation: 3 Minutes From Zero to Running

The setup is straightforward. Inside a running Claude Code session:

**Step 1: Add the marketplace and install**

```bash
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/reload-plugins
```

**Step 2: Run the guided setup**

```bash
/claude-hud:setup
```

This writes the statusline configuration to your Claude Code settings. Restart Claude Code after this step.

**Step 3: Customize (optional)**

```bash
/claude-hud:configure
```

The guided configurator lets you choose a preset, toggle individual elements, and preview your HUD before saving.

### Platform Gotchas

**Linux users**: If installation fails with `EXDEV: cross-device link not permitted`, your `/tmp` is on a separate filesystem. Fix it:

```bash
mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude
```

Then run the install commands in that session. This is a [known Claude Code limitation](https://github.com/anthropics/claude-code/issues/14799), not a Claude HUD bug.

**Windows users**: If setup says "no JavaScript runtime found," install Node.js LTS first:

```powershell
winget install OpenJS.NodeJS.LTS
```

## My Recommended Configuration

After experimenting with all the presets, here is what I actually use daily. I started with the **Essential** preset and tweaked from there:

```json
{
  "lineLayout": "expanded",
  "pathLevels": 2,
  "display": {
    "showModel": true,
    "showContextBar": true,
    "contextValue": "both",
    "showUsage": true,
    "showTools": true,
    "showAgents": true,
    "showTodos": true,
    "showCost": true,
    "showDuration": true
  },
  "gitStatus": {
    "enabled": true,
    "showDirty": true,
    "showAheadBehind": true
  }
}
```

Why these choices specifically:

- **`contextValue: "both"`** shows both percentage and absolute tokens (`45% (45k/200k)`). The percentage alone is meaningless when you do not know whether your session has a 200K or 1M context window.
- **`showTools` and `showAgents` enabled** because I run multi-agent workflows regularly and need to see when a subagent gets stuck. Without this, I have waited 5+ minutes for an agent that was looping on a grep search.
- **`showCost: true`** gives you a session cost estimate. This matters when you are on a Pro plan and want to understand your per-session burn rate.
- **`showAheadBehind: true`** in git status. I have forgotten to push commits before ending a session more times than I want to admit. Seeing `↑3` staring at me is a useful nudge.

## How Claude HUD Compares to Alternatives

Claude HUD is not the only statusline plugin. Here is how the landscape looks as of April 2026:

![Comparison of Claude Code statusline plugins: Claude HUD vs ccstatusline vs claudeline](01-comparison-statusline-plugins.webp)

| Feature | Claude HUD (18K ★) | ccstatusline (7K ★) | claudeline (27 ★) |
|---------|-------------------|--------------------|--------------------|
| **Focus** | Session observability | Visual customization | Minimalism |
| **Language** | JavaScript/Node.js | JavaScript/Node.js | Go (single binary) |
| **Context tracking** | ✅ Native token data | ✅ Native token data | ✅ Native token data |
| **Agent tracking** | ✅ Active agents + runtime | ❌ | ❌ |
| **Todo progress** | ✅ Real-time task tracking | ❌ | ❌ |
| **Tool activity** | ✅ Live file operations | ✅ Widget-based | ❌ |
| **Powerline fonts** | ❌ | ✅ Built-in themes | ❌ |
| **Configuration** | JSON + guided wizard | TUI installer | TOML config |
| **Plugin install** | ✅ One-command | ✅ One-command | Manual setup |
| **Chinese labels** | ✅ Optional | ❌ | ❌ |

**My recommendation**: If you care primarily about *knowing what your session is doing*—context health, agent monitoring, task tracking—use Claude HUD. If you care about *making your terminal look gorgeous* with Powerline glyphs and theme presets, use ccstatusline. They solve different problems. If you want the absolute lightest footprint and like Go, claudeline is a clean single-binary option but lacks the deep session introspection that makes Claude HUD valuable.

The 18K-vs-7K star gap is not just popularity—it reflects the fact that Claude HUD's agent and todo tracking features have no equivalent in competing plugins. When you are running complex multi-agent workflows, seeing `◐ explore [haiku]: Finding auth code (2m 15s)` is the difference between productive waiting and anxious guessing.

## When You Should Not Install Claude HUD

I want to be honest about the boundaries:

**If you use Claude Code casually** (a few times a week for quick questions), the overhead of installing and configuring a plugin is not worth it. You will never hit context limits or rate limits in short sessions.

**If you are on API key billing**, the usage monitoring—arguably Claude HUD's most valuable feature—will not work. API key users have pay-per-token billing with no rate limits to display. You still get context tracking, but you lose half the value proposition.

**If you are behind a corporate proxy**, usage limit tracking can be unreliable. The plugin does not make network calls, but Claude Code's own data pipeline may be affected. You may need manual timeout configuration.

**Platform risk is real.** Claude HUD depends on Claude Code's statusline API and plugin system. If Anthropic ships a built-in monitoring dashboard (which, given the community demand, seems likely), the plugin becomes redundant. At version 0.0.9, it is still early-stage software—expect breaking changes as both Claude Code and the plugin evolve.

## The Bigger Picture: Observability as a First-Class Concern

Claude HUD's popularity reveals something important about the state of AI coding tools in 2026. We are asking these tools to manage increasingly complex tasks—multi-file refactors, agent-to-agent coordination, hours-long coding sessions—but the tooling around *understanding what the AI is doing* has not kept pace.

The context window is the most critical resource in any AI coding session, and until Claude HUD came along, managing it was a guessing game. The fact that a third-party plugin had to fill this gap, and that 18,000 developers rushed to install it, should tell Anthropic everything they need to know about prioritizing built-in observability.

If you are using Claude Code for any serious development work, install Claude HUD today. It takes 3 minutes, it is free, and it will save you from the silent session degradation that you did not even know was happening. The context bar alone—watching it creep from green to yellow—has changed how I manage my sessions. I start fresh sessions proactively now instead of waiting for quality to degrade.

## Related Reading

- [Claude Code Complete Guide: From Setup to Advanced Workflows](/posts/ai/2026-02-28-claude-code-complete-guide/) — comprehensive setup and usage guide
- [CLAUDE.md Best Practices: Configure Your AI Coding Assistant](/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) — optimize your CLAUDE.md for better results
- [Claude Code vs Cursor vs Copilot: Which AI Coding Tool Wins in 2026?](/posts/ai/2026-04-03-claude-code-vs-cursor-vs-copilot/) — how Claude Code stacks up against alternatives
- [Claude Code Hooks Guide: Automate Your Development Workflow](/posts/ai/2026-02-28-claude-code-hooks-guide/) — extend Claude Code with custom automation
- [Claude Code Rate Limits Explained](/posts/ai/2026-02-28-claude-rate-limits/) — understand and manage your usage limits
