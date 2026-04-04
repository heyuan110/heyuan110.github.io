+++
date = '2026-03-05T19:00:00+08:00'
draft = false
title = 'Claude Code Slash Commands 2026: Complete List + Custom Commands'
description = 'Every Claude Code slash command, keyboard shortcut, and CLI flag in one reference. 40+ built-in commands, custom Skills commands, and environment variables explained.'
toc = true
tags = ['Claude Code', 'Commands', 'CLI Reference', 'Productivity']
categories = ['AI Guides']
keywords = ['claude code slash commands', 'claude code commands list 2026', 'claude code commands', 'claude code keyboard shortcuts', 'claude code CLI flags', 'claude code custom commands', 'claude code environment variables', 'claude code reference 2026']

[[params.faqItems]]
question = "What are Claude Code slash commands?"
answer = "Slash commands are built-in shortcuts you type during an interactive Claude Code session. They start with / and perform actions like clearing context (/clear), checking costs (/cost), switching models (/model), or running diagnostics (/doctor). Type / in your session to see all available commands, or /help for the full list."

[[params.faqItems]]
question = "How do I create custom slash commands in Claude Code?"
answer = "Create a SKILL.md file inside .claude/skills/<skill-name>/ with YAML frontmatter (name, description) and Markdown instructions. The skill name becomes a slash command. For example, .claude/skills/deploy/SKILL.md creates /deploy. Skills can also auto-trigger based on conversation context without manual invocation."

[[params.faqItems]]
question = "What is the difference between /compact and /clear in Claude Code?"
answer = "/compact compresses your conversation history while preserving key context, reducing token usage. Use it when your context window is getting full but you want to continue the same task. /clear completely resets the conversation, removing all history. Use /clear when switching to an unrelated task."

[[params.faqItems]]
question = "How do I use Claude Code in non-interactive (print) mode?"
answer = "Use the -p or --print flag: claude -p 'your query here'. This sends a single query and exits after the response, making it ideal for scripting and CI/CD pipelines. Combine it with --output-format json for machine-readable output, --max-turns to limit agentic loops, and --allowedTools to control permissions."

[[params.faqItems]]
question = "What keyboard shortcuts work in Claude Code?"
answer = "Key shortcuts include Escape to cancel generation, Ctrl+C to exit, Ctrl+R for reverse history search, Ctrl+T to toggle the task list, Ctrl+O for verbose output, Shift+Tab to cycle permission modes, and Ctrl+B to background a running command. Press ? during a session to see all shortcuts for your terminal."
+++

![Complete reference guide for Claude Code slash commands, keyboard shortcuts, and CLI flags](cover.webp)

Claude Code has over 40 built-in slash commands, dozens of keyboard shortcuts, and a rich set of CLI flags. Most developers use about five of them. The rest sit undiscovered, which means missed opportunities to save time, reduce token costs, and automate repetitive workflows.

This is the reference you bookmark. Every slash command with what it does and when to use it. Every keyboard shortcut worth memorizing. Every CLI flag for scripting and automation. Plus how to build your own custom commands using Skills.

No fluff. Just the complete command reference for Claude Code in 2026.

## Built-in Slash Commands

Type `/` at the start of your input to see all available commands. Type any letters after `/` to filter the list. Here is every built-in command, organized by what you use them for.

### Session Management

These commands control your conversation lifecycle -- starting fresh, resuming old work, and managing context.

| Command | What It Does |
|---------|-------------|
| `/clear` | Wipe conversation history and start fresh. Aliases: `/reset`, `/new` |
| `/compact [instructions]` | Compress conversation to save context. Optionally specify what to keep: `/compact retain the API design decisions` |
| `/resume [session]` | Resume a previous session by ID or name, or open a session picker. Alias: `/continue` |
| `/fork [name]` | Branch the current conversation into a new session from this point |
| `/rename [name]` | Rename the current session. Without a name, auto-generates one from history |
| `/rewind` | Restore code and conversation to a previous point. Alias: `/checkpoint` |
| `/exit` | Exit Claude Code. Alias: `/quit` |

**When to use what:**

- **`/compact`** when context usage exceeds 80% but you are still working on the same task. Add focus instructions to control what survives: `/compact keep the database schema and error handling patterns`
- **`/clear`** when switching to a completely different task. Old context would confuse Claude
- **`/resume`** when you closed a session yesterday and want to pick up where you left off

```bash
# Check context usage first
/context

# If context is getting full, compact with focus
/compact retain the authentication flow and test results

# If switching tasks entirely, clear everything
/clear
```

### Information and Diagnostics

Commands that show you what is happening -- costs, status, context usage, and environment health.

| Command | What It Does |
|---------|-------------|
| `/cost` | Show token usage and cost for the current session |
| `/usage` | Show plan usage limits and rate limit status |
| `/context` | Visualize context window usage as a colored grid |
| `/status` | Show version, model, account, and connectivity info |
| `/doctor` | Run diagnostics on your Claude Code installation |
| `/help` | List all available commands |
| `/stats` | Visualize daily usage, session history, and streaks |
| `/diff` | Open interactive diff viewer showing uncommitted changes and per-turn diffs |
| `/export [filename]` | Export conversation as plain text to a file or clipboard |
| `/copy` | Copy last assistant response to clipboard. Shows picker for code blocks |
| `/release-notes` | View the full changelog |
| `/insights` | Generate a report analyzing your Claude Code sessions |

**Power user tip:** Run `/cost` periodically during long sessions. A single agentic loop can burn through tokens faster than you expect. If costs are climbing, use `/compact` to reduce context size or switch to a cheaper model with `/model sonnet`.

```bash
# Quick session health check
/cost          # How much have I spent?
/context       # How full is my context window?
/usage         # Am I near my rate limit?
```

### Model and Mode Control

Switch models, toggle modes, and change how Claude behaves.

| Command | What It Does |
|---------|-------------|
| `/model [model]` | Switch model. Use left/right arrows to adjust effort level |
| `/fast [on\|off]` | Toggle fast mode (same model, faster output) |
| `/plan` | Enter plan mode -- Claude proposes actions before executing |
| `/vim` | Toggle between Vim and normal editing modes |
| `/output-style [style]` | Switch output style: Default, Explanatory, or Learning |
| `/theme` | Change color theme (light, dark, colorblind-accessible options) |

**Model switching strategy:** Start with Sonnet for most tasks -- it handles 80% of work at lower cost. Switch to Opus for complex architecture decisions, subtle bugs, or tasks requiring deep reasoning. Switch back when the hard part is done.

```bash
# Start a session with Sonnet (default, cheaper)
/model sonnet

# Hit a tricky bug? Switch to Opus
/model opus

# Done with the hard part, switch back
/model sonnet
```

### Configuration and Permissions

Manage settings, permissions, authentication, and project setup.

| Command | What It Does |
|---------|-------------|
| `/config` | Open settings interface. Alias: `/settings` |
| `/permissions` | View or update tool permissions. Alias: `/allowed-tools` |
| `/init` | Initialize project with a CLAUDE.md file |
| `/memory` | Edit CLAUDE.md memory files, toggle auto-memory |
| `/login` | Sign in to your Anthropic account |
| `/logout` | Sign out from your Anthropic account |
| `/hooks` | Configure and manage lifecycle hooks |
| `/agents` | Manage subagent configurations |
| `/skills` | List available skills |
| `/mcp` | Manage MCP server connections |
| `/plugin` | Manage Claude Code plugins |
| `/terminal-setup` | Configure terminal keybindings (Shift+Enter, etc.) |
| `/keybindings` | Open or create keybindings configuration |
| `/sandbox` | Toggle sandbox mode for isolated execution |
| `/extra-usage` | Configure extra usage when rate limits hit |
| `/privacy-settings` | View and update privacy settings (Pro/Max only) |
| `/statusline` | Configure terminal status line display |

### Code Review and PR Workflow

Commands for working with pull requests and code review.

| Command | What It Does |
|---------|-------------|
| `/review` | Review a pull request for quality, correctness, and security. Pass a PR number or omit to list open PRs |
| `/pr-comments [PR]` | Fetch and display comments from a GitHub PR. Auto-detects current branch PR |
| `/security-review` | Analyze pending changes for security vulnerabilities |
| `/install-github-app` | Set up Claude GitHub Actions for automated PR review |

These commands require the `gh` CLI to be installed and authenticated. If you have not set it up:

```bash
# Install GitHub CLI
brew install gh

# Authenticate
gh auth login

# Now you can use PR commands in Claude Code
/review 42        # Review PR #42
/pr-comments      # Show comments on current branch's PR
/security-review  # Security audit of uncommitted changes
```

### Working Directories and Integration

| Command | What It Does |
|---------|-------------|
| `/add-dir <path>` | Add a new working directory to the session |
| `/ide` | Manage IDE integrations and show status |
| `/chrome` | Configure Chrome browser integration |
| `/remote-control` | Make session available for remote control from claude.ai. Alias: `/rc` |
| `/desktop` | Continue session in Claude Code Desktop app (macOS/Windows). Alias: `/app` |
| `/tasks` | List and manage background tasks |
| `/feedback [report]` | Submit feedback about Claude Code. Alias: `/bug` |

## Keyboard Shortcuts

Memorizing even a few of these shortcuts will noticeably speed up your workflow. Think of them like IDE shortcuts -- the investment pays off every session.

### Essential Shortcuts (Learn These First)

| Shortcut | What It Does | When to Use |
|----------|-------------|-------------|
| `Escape` | Cancel current generation | Claude is going down the wrong path |
| `Escape` + `Escape` | Rewind or summarize | Undo Claude's last actions |
| `Ctrl+C` | Exit session | Done working (press twice) |
| `Ctrl+R` | Reverse search history | Find a previous prompt you typed |
| `Ctrl+T` | Toggle task list | Track progress on multi-step work |
| `Shift+Tab` | Cycle permission modes | Switch between Auto-Accept, Plan, and normal mode |
| `?` | Show available shortcuts | Forgot a shortcut |

### Navigation and Editing

| Shortcut | What It Does |
|----------|-------------|
| `Up/Down` arrows | Navigate command history |
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete entire line |
| `Ctrl+Y` | Paste deleted text |
| `Alt+B` | Move cursor back one word |
| `Alt+F` | Move cursor forward one word |
| `Ctrl+L` | Clear terminal screen (keeps history) |

### Mode and Display Toggles

| Shortcut | What It Does |
|----------|-------------|
| `Ctrl+O` | Toggle verbose output (see detailed tool usage) |
| `Ctrl+B` | Background running tasks (tmux users: press twice) |
| `Ctrl+G` | Open current prompt in external text editor |
| `Option+P` / `Alt+P` | Switch model without clearing prompt |
| `Option+T` / `Alt+T` | Toggle extended thinking |

### Multiline Input

Writing multi-line prompts requires special key combinations since Enter submits the message.

| Method | Shortcut | Notes |
|--------|----------|-------|
| Backslash escape | `\` + `Enter` | Works in all terminals |
| macOS default | `Option+Enter` | Default on macOS |
| Shift+Enter | `Shift+Enter` | Works in iTerm2, WezTerm, Ghostty, Kitty out of the box |
| Line feed | `Ctrl+J` | Works everywhere |
| Paste mode | Paste directly | For code blocks and logs |

If Shift+Enter does not work in your terminal, run `/terminal-setup` to install the keybinding.

### Quick Input Prefixes

| Prefix | What It Does | Example |
|--------|-------------|---------|
| `/` | Slash command or skill | `/compact retain error patterns` |
| `!` | Direct bash command | `! git status` |
| `@` | File path autocomplete | `@src/main.ts` |

The `!` prefix is powerful -- it runs a shell command directly and adds the output to conversation context without Claude interpreting or approving it. Use it for quick checks while maintaining context:

```bash
! npm test                # Run tests, output goes into context
! git log --oneline -5    # Check recent commits
! cat .env.example        # Show file contents
```

## CLI Flags Reference

CLI flags let you customize Claude Code's behavior from the command line. They are essential for scripting, CI/CD pipelines, and automation.

### Session Control

| Flag | Description | Example |
|------|-------------|---------|
| `--continue`, `-c` | Resume most recent conversation | `claude -c` |
| `--resume`, `-r` | Resume session by ID or name | `claude -r auth-refactor` |
| `--from-pr` | Resume sessions linked to a PR | `claude --from-pr 123` |
| `--fork-session` | Fork into new session when resuming | `claude -r abc123 --fork-session` |
| `--session-id` | Use specific session UUID | `claude --session-id "550e8400-..."` |
| `--worktree`, `-w` | Start in isolated git worktree | `claude -w feature-auth` |

### Model and Behavior

| Flag | Description | Example |
|------|-------------|---------|
| `--model` | Set model (`sonnet`, `opus`, or full name) | `claude --model opus` |
| `--fallback-model` | Auto-fallback when overloaded (print mode) | `claude -p --fallback-model sonnet "query"` |
| `--permission-mode` | Start in a specific permission mode | `claude --permission-mode plan` |
| `--agent` | Specify an agent for the session | `claude --agent my-custom-agent` |
| `--agents` | Define custom subagents via JSON | See example below |

### Print Mode (Non-Interactive)

Print mode (`-p`) is the key to scripting with Claude Code. It sends a query and exits -- no interactive session.

| Flag | Description | Example |
|------|-------------|---------|
| `--print`, `-p` | Non-interactive mode | `claude -p "explain this codebase"` |
| `--output-format` | Output as `text`, `json`, or `stream-json` | `claude -p --output-format json "query"` |
| `--json-schema` | Validate output against JSON Schema | `claude -p --json-schema '{...}' "query"` |
| `--max-turns` | Limit agentic turns | `claude -p --max-turns 3 "query"` |
| `--max-budget-usd` | Cap spending for this run | `claude -p --max-budget-usd 5.00 "query"` |
| `--input-format` | Input format: `text` or `stream-json` | `claude -p --input-format stream-json` |

**Practical scripting examples:**

```bash
# Generate API docs and save to file
claude -p "Generate API documentation for src/api/" --output-format text > api-docs.md

# Get structured analysis as JSON
claude -p "Analyze the error handling in this project" --output-format json | jq '.result'

# Limit spending on expensive operations
claude -p --max-budget-usd 2.00 --max-turns 5 "Refactor the auth module"

# Pipe content for analysis
cat error.log | claude -p "What caused this crash?"

# CI/CD: Check code quality with budget cap
claude -p --max-budget-usd 1.00 --output-format json \
  "Review the last commit for security issues" | jq '.result'
```

### Permission and Tool Control

| Flag | Description | Example |
|------|-------------|---------|
| `--allowedTools` | Tools that run without permission prompts | `--allowedTools "Bash(git log:*)" "Read"` |
| `--disallowedTools` | Tools completely blocked | `--disallowedTools "Bash(rm *)" "Edit"` |
| `--tools` | Restrict which built-in tools are available | `--tools "Bash,Edit,Read"` |
| `--dangerously-skip-permissions` | Skip all permission prompts (use with extreme caution) | Not recommended for production |

**The `--allowedTools` flag is the safer alternative** to skipping permissions entirely. You get automation without giving Claude carte blanche:

```bash
# Allow only read operations and git commands
claude -p --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Read" "Grep" "Glob" \
  "Generate a code review for the last 3 commits"
```

### System Prompt Customization

| Flag | Description | Use Case |
|------|-------------|----------|
| `--system-prompt` | Replace entire system prompt | Complete control over behavior |
| `--system-prompt-file` | Replace with file contents | Version-controlled prompts |
| `--append-system-prompt` | Add to default prompt | Extra rules while keeping defaults |
| `--append-system-prompt-file` | Append file contents | Load rules from files |

For most use cases, `--append-system-prompt` is the safest option -- it keeps Claude Code's built-in capabilities while adding your custom rules:

```bash
# Add project-specific rules
claude --append-system-prompt "Always use TypeScript. Never use any. Include JSDoc comments."

# Load rules from a file for team consistency
claude --append-system-prompt-file ./team-rules.txt
```

### MCP and Extensions

| Flag | Description | Example |
|------|-------------|---------|
| `--mcp-config` | Load MCP servers from JSON file | `claude --mcp-config ./mcp.json` |
| `--strict-mcp-config` | Only use servers from `--mcp-config` | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--chrome` | Enable Chrome browser integration | `claude --chrome` |
| `--plugin-dir` | Load plugins from directory | `claude --plugin-dir ./my-plugins` |
| `--add-dir` | Add extra working directories | `claude --add-dir ../apps ../lib` |

### Other Useful Flags

| Flag | Description |
|------|-------------|
| `--verbose` | Verbose logging with full turn-by-turn output |
| `--debug` | Enable debug mode, optionally filter by category: `--debug "api,mcp"` |
| `--version`, `-v` | Show version number |
| `--ide` | Auto-connect to IDE on startup |
| `--init` | Run initialization hooks on startup |
| `--remote` | Create a web session on claude.ai |
| `--teleport` | Resume a web session in your local terminal |
| `--disable-slash-commands` | Disable all skills and commands for this session |
| `--settings` | Load additional settings from a JSON file |

## Custom Commands with Skills

Built-in commands cover general needs. But your team has specific workflows -- deployment checklists, code review processes, documentation formats. This is where custom commands come in.

Claude Code supports two approaches: legacy slash commands (files in `.claude/commands/`) and the newer Skills system (files in `.claude/skills/`). **Skills are the recommended approach** -- they do everything commands do, plus auto-triggering and supporting files.

### Creating a Custom Skill

A Skill is a folder containing a `SKILL.md` file with YAML frontmatter and Markdown instructions.

**Step 1:** Create the skill directory.

```bash
# Project-level skill (shared with team via Git)
mkdir -p .claude/skills/deploy

# Personal skill (available in all your projects)
mkdir -p ~/.claude/skills/deploy
```

**Step 2:** Write the SKILL.md file.

````yaml
---
name: deploy
description: Deploy the application to staging or production. Use when the user mentions deploying, releasing, or shipping.
---

# Deployment Workflow

## Pre-deployment Checks
1. Run the full test suite: `npm test`
2. Check for uncommitted changes: `git status`
3. Verify you're on the correct branch

## Deploy Steps
1. Build the production bundle: `npm run build`
2. Run database migrations if needed
3. Deploy using: `./scripts/deploy.sh <environment>`
4. Verify the deployment health check

## Post-deployment
1. Monitor error rates for 15 minutes
2. Run smoke tests against the deployed environment
3. Update the deployment log
````

**Step 3:** Use it.

```bash
# Manual invocation
/deploy

# Or just describe what you want -- Claude auto-detects the skill
"Deploy the latest changes to staging"
```

### Skill Frontmatter Options

The YAML frontmatter controls how and when your skill activates:

```yaml
---
name: code-review
description: Thorough code review following team standards
# Optional fields:
user_invocable: true       # Allow manual /code-review invocation (default: true)
auto_invocable: true       # Allow Claude to auto-trigger (default: true)
model: opus                # Force a specific model for this skill
tools:                     # Restrict which tools this skill can use
  - Read
  - Grep
  - Glob
---
```

### Skills vs Legacy Commands

| Feature | Legacy Commands | Skills |
|---------|----------------|--------|
| Location | `.claude/commands/name.md` | `.claude/skills/name/SKILL.md` |
| Invocation | Manual (`/name`) only | Auto-triggered + manual |
| Supporting files | No | Yes (templates, scripts, examples in same folder) |
| Frontmatter | Optional | Full control (model, tools, invocation) |
| Status | Still works | Recommended |

Legacy commands keep working. If you have existing `.claude/commands/` files, they will continue to function. Migrate when convenient -- or do not. A Skill and a command with the same name will resolve to the Skill.

For a deep dive on building advanced Skills, see our [Claude Code Skills Guide](/posts/ai/2026-02-28-claude-code-skills-guide/).

## Environment Variables

Environment variables configure Claude Code at a deeper level than settings or flags. Set them in your shell profile (`~/.zshrc`, `~/.bashrc`) or per-session.

### Authentication

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key. Leave unset to use subscription-based auth |
| `ANTHROPIC_AUTH_TOKEN` | Custom Authorization header value (prefixed with `Bearer `) |

### Cloud Provider Configuration

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_USE_BEDROCK` | Set to `1` to route through AWS Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Set to `1` to route through Google Vertex AI |
| `CLAUDE_CODE_USE_FOUNDRY` | Set to `1` to route through Microsoft Foundry |

### Model Configuration

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_MODEL` | Override the default model |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Default Sonnet-class model ID |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Default Opus-class model ID |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Default Haiku-class model ID |
| `CLAUDE_CODE_EFFORT_LEVEL` | Thinking effort: `low`, `medium`, or `high` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens (default 32,000; max 64,000) |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents |

### Bash Execution

| Variable | Purpose | Default |
|----------|---------|---------|
| `BASH_DEFAULT_TIMEOUT_MS` | Default timeout for bash commands | Varies |
| `BASH_MAX_TIMEOUT_MS` | Maximum timeout the model can set | Varies |
| `BASH_MAX_OUTPUT_LENGTH` | Max characters before truncation | Varies |
| `CLAUDE_CODE_SHELL` | Override automatic shell detection | Auto |
| `CLAUDE_CODE_SHELL_PREFIX` | Prefix to wrap all bash commands | None |

### Feature Toggles

| Variable | Set to `1` to... |
|----------|-------------------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Disable auto-memory |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable background task functionality |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | Disable fast mode |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | Remove git workflow instructions from system prompt |
| `DISABLE_AUTOUPDATER` | Disable automatic updates |
| `DISABLE_PROMPT_CACHING` | Disable prompt caching |
| `DISABLE_COST_WARNINGS` | Suppress cost warning messages |

**Setting environment variables:**

```bash
# In ~/.zshrc or ~/.bashrc
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_CODE_EFFORT_LEVEL="high"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000

# Per-session override
CLAUDE_CODE_EFFORT_LEVEL=low claude -p "Quick summary of this file"

# For AWS Bedrock users
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
```

## Power User Tips

### 1. Chain Commands for Context Efficiency

Instead of sending multiple messages, front-load context before your request:

```bash
# Bad: multiple turns, wastes tokens
"What does the auth module do?"
"Now add rate limiting to it"
"Now write tests for the rate limiting"

# Good: single prompt with full context
"Add rate limiting to the auth module in src/auth/ and write tests.
 Rate limit: 100 requests per minute per IP.
 Use the existing Redis connection for storage.
 Follow the test patterns in tests/auth/"
```

### 2. Monitor Costs with /cost

Get into the habit of checking `/cost` every 15-20 minutes during active sessions. Token usage can spike during agentic loops where Claude reads files, edits, runs tests, and iterates.

If costs are climbing faster than expected:
- Run `/compact` to reduce context size
- Switch to `/model sonnet` for less complex subtasks
- Break large tasks into smaller, focused sessions

### 3. Use /compact Strategically

`/compact` is not just a panic button when context is full. Use it proactively:

```bash
# After finishing a subtask, compact before starting the next
/compact retain the API schema and test results, discard the debugging steps

# Before a complex operation, make room
/compact keep only the project architecture and current task requirements
```

### 4. Script Repetitive Workflows

Combine `-p` mode with shell scripting for tasks you run regularly:

```bash
#!/bin/bash
# daily-review.sh -- Morning code review routine

echo "=== Reviewing yesterday's changes ==="
claude -p --max-budget-usd 1.00 --output-format text \
  "Review all commits from the last 24 hours. Flag any security issues,
   missing tests, or code quality problems. Be concise." \
  --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Bash(git show:*)" "Read" "Grep"

echo "=== Done ==="
```

### 5. Background Long-Running Commands

When Claude is running a slow command (tests, builds, deployments), press `Ctrl+B` to send it to the background. You can keep working on your prompt while the command finishes:

```bash
# Claude starts running "npm test" (takes 2 minutes)
# Press Ctrl+B to background it
# Continue typing your next instruction
# Claude retrieves the output when it's done
```

### 6. Use Vim Mode for Complex Prompts

If you write long, detailed prompts, enable Vim mode with `/vim`. You get full Vim navigation (hjkl, word motions, text objects) and editing (dd, ciw, yy) right in the Claude Code input. Toggle it off anytime with `/vim` again.

### 7. Define Subagents for Specialized Tasks

Use the `--agents` flag to create focused subagents that Claude can delegate to:

```bash
claude --agents '{
  "test-writer": {
    "description": "Writes comprehensive tests. Use after any code change.",
    "prompt": "You write thorough tests. Cover happy path, edge cases, and error conditions.",
    "tools": ["Read", "Edit", "Bash"],
    "model": "sonnet"
  },
  "security-reviewer": {
    "description": "Reviews code for security vulnerabilities.",
    "prompt": "You are a security expert. Find injection, auth, and data exposure risks.",
    "tools": ["Read", "Grep", "Glob"],
    "model": "opus"
  }
}'
```

## Quick Reference Card

Here is the cheat sheet. Print it, pin it, or keep it in a second terminal.

**Daily essentials:**

| Action | Command |
|--------|---------|
| Check costs | `/cost` |
| Check context usage | `/context` |
| Compress context | `/compact [focus]` |
| Start fresh | `/clear` |
| Switch model | `/model sonnet` or `/model opus` |
| Resume last session | `claude -c` |
| Run diagnostics | `/doctor` |

**Keyboard shortcuts:**

| Action | Shortcut |
|--------|----------|
| Cancel generation | `Escape` |
| Undo Claude's actions | `Escape` + `Escape` |
| Search history | `Ctrl+R` |
| Toggle task list | `Ctrl+T` |
| Verbose output | `Ctrl+O` |
| Cycle permission modes | `Shift+Tab` |
| Background command | `Ctrl+B` |
| Switch model | `Alt+P` |

**Scripting pattern:**

```bash
claude -p "your query" \
  --output-format json \
  --max-turns 5 \
  --max-budget-usd 2.00 \
  --allowedTools "Read" "Grep" "Glob"
```

## Related Reading

- [Claude Code Guide 2026: Everything You Need to Know](/posts/ai/2026-02-28-claude-code-complete-guide/) -- The hub page linking all Claude Code guides
- [Claude Code Hooks: Automate Your AI Workflow](/posts/ai/2026-03-05-claude-code-hooks-guide/) -- Deterministic automation with lifecycle hooks
- [Claude Code Skills Guide: Create Custom Workflows](/posts/ai/2026-02-28-claude-code-skills-guide/) -- Deep dive into building Skills
- [CLAUDE.md Best Practices: Write Files That Actually Work](/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) -- Effective project configuration
- [Install Claude Code in 5 Minutes](/posts/ai/2026-02-25-claude-code-setup-guide/) -- Getting started from zero
- [10 Claude Code Mistakes Beginners Make](/posts/ai/2026-02-25-claude-code-mistakes/) -- Common pitfalls to avoid
