+++
date = '2026-02-18T11:00:00+08:00'
draft = false
title = 'Claude Code Hooks Guide: 12 Ready-to-Use Configs for Automation'
description = 'Master Claude Code Hooks with 12 copy-paste configurations covering auto-formatting, file protection, dangerous command blocking, Slack notifications, and more. Complete guide to all 15 lifecycle events.'
toc = true
tags = ['Claude Code', 'AI Coding', 'Hooks', 'Automation', 'Developer Tools']
categories = ['AI Guides']
keywords = ['Claude Code Hooks', 'Claude Code automation', 'Claude Code configuration', 'PreToolUse', 'PostToolUse', 'AI coding workflow', 'Claude Code hooks guide']
+++

If you use Claude Code daily, you have probably run into these problems:

- Claude edits a file and the formatting is a mess -- you have to manually run `prettier` every time
- Claude accidentally modifies `.env` or `package-lock.json`, and you only notice when it is too late
- Claude says "done!" but the tests were never run
- You step away to grab coffee and have no idea whether Claude is waiting for your input

The root cause is simple: **Claude is probabilistic, but your workflow needs deterministic guarantees**.

Hooks solve this. They are lifecycle callbacks built into Claude Code -- you define the rules, and Claude Code enforces them automatically at key moments. Instead of hoping the AI "remembers," you make the system "guarantee."

This article gives you 12 copy-paste Hook configurations that cover everything from code formatting to security protection.

## What Are Hooks? Core Concepts in 3 Minutes

### Definition

Hooks are shell commands (or AI prompts) that you define to run automatically at specific points in Claude Code's lifecycle.

Think of it this way: if Claude Code is an employee, Hooks are the sticky notes on their desk -- "format code after every edit," "don't touch .env files," "run tests before delivery." The difference is that sticky notes get ignored, but **Hooks always execute**.

### Three Hook Types

| Type | Keyword | How It Works | Best For |
|------|---------|-------------|----------|
| **Command** | `command` | Runs a shell command | Formatting, file protection, notifications |
| **Prompt** | `prompt` | Sends context to a lightweight model (Haiku by default) for a single-turn judgment | Task completion checks |
| **Agent** | `agent` | Spawns a sub-agent with multi-turn capabilities | Running tests, code quality checks |

90% of use cases only need `command` type. Use `prompt` and `agent` when you need judgment -- like checking whether a task is truly finished.

### 15 Lifecycle Events

Each event corresponds to a key moment during a Claude Code session:

```
SessionStart          ──────────────────── Session starts or resumes
    │
UserPromptSubmit      ──────────────────── User submits a prompt
    │
    ├── PreToolUse    ──────────────────── Before tool execution (can block)
    │       │
    │   PermissionRequest ───────────────── Permission confirmation popup
    │       │
    │   PostToolUse   ──────────────────── After successful tool execution
    │   PostToolUseFailure ──────────────── After failed tool execution
    │
    ├── SubagentStart ──────────────────── Sub-agent starts
    │   SubagentStop  ──────────────────── Sub-agent ends
    │
    ├── PreCompact    ──────────────────── Before context compaction
    │
    ├── Notification  ──────────────────── Notification (waiting for input, etc.)
    │
    ├── TaskCompleted ──────────────────── Task marked as complete
    │
    ├── TeammateIdle  ──────────────────── Agent team member idle
    │
Stop                  ──────────────────── Claude finishes its response
    │
SessionEnd            ──────────────────── Session ends
```

The four most commonly used events:

- **PreToolUse**: Before tool execution -- perfect for blocking dangerous operations
- **PostToolUse**: After tool execution -- ideal for auto-formatting and auto-committing
- **Notification**: When Claude is waiting for input -- great for sending alerts
- **Stop**: When Claude finishes responding -- useful for final validation

### Where Do Configuration Files Go?

| Location | Scope | Commit to Git? |
|----------|-------|----------------|
| `~/.claude/settings.json` | All projects | No (machine-specific) |
| `.claude/settings.json` | Current project | Yes (shared with team) |
| `.claude/settings.local.json` | Current project | No (gitignored) |

**Recommended strategy**:
- Personal preferences (e.g., desktop notifications) go in `~/.claude/settings.json`
- Team standards (e.g., code formatting) go in `.claude/settings.json` and get committed
- Local debugging configs go in `.claude/settings.local.json`

## Getting Started: Your First Hook in 5 Minutes

The quickest approach is the `/hooks` interactive menu. But I recommend editing the config file directly -- it enables version control, team sharing, and the format is straightforward.

### Desktop Notifications: Stop Staring at the Terminal

This is the simplest and most practical Hook. When Claude needs your input or permission, your system pops up a notification.

Edit `~/.claude/settings.json` and add:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

> Linux users: replace the `osascript` line with `notify-send 'Claude Code' 'Claude Code needs your attention'`.

Save the file, restart Claude Code (or confirm in the `/hooks` menu), ask Claude to perform an action that requires permission, then switch to another window -- you should see the notification pop up.

### Configuration Structure Explained

Every Hook configuration has three parts:

```json
{
  "hooks": {
    "EventName": [          // When to trigger
      {
        "matcher": "pattern",  // Filter condition (regex)
        "hooks": [             // List of hooks to execute
          {
            "type": "command",        // Hook type
            "command": "shell command", // Command to run
            "timeout": 30             // Timeout in seconds (optional)
          }
        ]
      }
    ]
  }
}
```

**Matcher rules**:

| Event | What matcher matches | Example |
|-------|---------------------|---------|
| PreToolUse / PostToolUse | Tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| SessionStart | Session start type | `startup`, `resume`, `compact` |
| Notification | Notification type | `permission_prompt`, `idle_prompt` |
| SessionEnd | End reason | `clear`, `logout` |

An empty string matcher matches everything.

## 12 Production-Ready Configurations (Copy and Paste)

### Config 1: Auto-Format with Prettier

Automatically run Prettier every time Claude edits or creates a file.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

**How it works**:
1. When `PostToolUse` fires, Claude Code pipes tool call info as JSON to stdin
2. `jq -r '.tool_input.file_path'` extracts the edited file path from the JSON
3. `xargs npx prettier --write` formats that file
4. `2>/dev/null; exit 0` ensures the Hook never blocks Claude, even if Prettier throws an error (e.g., unsupported file type)

**Prerequisites**: Prettier installed in your project (`npm install -D prettier`) and `jq` installed on your system (`brew install jq`).

### Config 2: Auto-Format with ESLint

If you use ESLint instead of Prettier:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); if echo \"$FILE\" | grep -qE '\\.(js|ts|jsx|tsx)$'; then npx eslint --fix \"$FILE\" 2>/dev/null; fi; exit 0"
          }
        ]
      }
    ]
  }
}
```

This adds a file type filter -- ESLint only runs on `.js`, `.ts`, `.jsx`, and `.tsx` files, avoiding errors on Markdown or JSON files.

### Config 3: Protect Sensitive Files

Prevent Claude from modifying `.env`, `package-lock.json`, `.git/`, and other critical files.

First, create the script `.claude/hooks/protect-files.sh`:

```bash
#!/bin/bash
# protect-files.sh — Block Claude from modifying sensitive files

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Protection list: customize for your project
PROTECTED_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  "package-lock.json"
  "yarn.lock"
  "pnpm-lock.yaml"
  ".git/"
  "node_modules/"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protection rule '$pattern'" >&2
    exit 2  # exit 2 = block the operation, feed stderr back to Claude
  fi
done

exit 0  # exit 0 = allow the operation
```

Make it executable and register the Hook:

```bash
chmod +x .claude/hooks/protect-files.sh
```

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

**Key details**:
- `exit 2` blocks Claude's operation and sends the stderr message back to Claude as feedback
- `exit 0` allows the operation to continue
- `$CLAUDE_PROJECT_DIR` is an environment variable automatically set by Claude Code, pointing to the project root

### Config 4: Block Dangerous Shell Commands

Prevent Claude from running `rm -rf`, `DROP TABLE`, `git push --force`, and other high-risk commands.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'CMD=$(jq -r \".tool_input.command\" <<< \"$(cat)\"); DANGEROUS=(\"rm -rf /\" \"rm -rf ~\" \"DROP TABLE\" \"git push --force\" \"git reset --hard\" \"dd if=\" \"mkfs\" \":(){ :|:& };:\"); for p in \"${DANGEROUS[@]}\"; do if echo \"$CMD\" | grep -qiF \"$p\"; then echo \"Blocked dangerous command: $CMD (matched: $p)\" >&2; exit 2; fi; done; exit 0'"
          }
        ]
      }
    ]
  }
}
```

This Hook inspects every shell command Claude is about to run. If it matches a dangerous pattern, the operation is blocked immediately. Claude receives the reason and tries to find a safe alternative.

### Config 5: Git Auto-Stage

Automatically `git add` modified files after every Claude edit, making subsequent commits easier.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path'); git add \"$FILE\" 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

### Config 6: Log All Bash Commands

Record every Bash command Claude runs to a log file for auditing and troubleshooting.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'INPUT=$(cat); CMD=$(echo \"$INPUT\" | jq -r \".tool_input.command\"); echo \"[$(date +\"%Y-%m-%d %H:%M:%S\")] $CMD\" >> \"$CLAUDE_PROJECT_DIR\"/.claude/command-log.txt'"
          }
        ]
      }
    ]
  }
}
```

Each entry includes a timestamp and the command content. The log file is saved at `.claude/command-log.txt`.

### Config 7: Re-Inject Context After Compaction

When Claude's context window fills up, automatic compaction may discard important information. Use the `SessionStart` event with the `compact` matcher to re-inject critical context after compaction.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Important reminders:\n1. This project uses pnpm, not npm\n2. Run pnpm test before committing\n3. Git commit messages should be descriptive\n4. Current sprint focus: user auth module refactor'"
          }
        ]
      }
    ]
  }
}
```

The stdout from a Hook gets injected into Claude's context. You can also replace `echo` with dynamic commands, for example:

```json
{
  "type": "command",
  "command": "echo 'Last 5 commits:' && git log --oneline -5"
}
```

### Config 8: Stop Hook -- Make Claude Actually Finish

This is one of the most powerful Hooks. Use the `prompt` type to have an AI check whether Claude truly completed all tasks:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check whether Claude has completed all tasks the user requested. If any task is incomplete, tests have not passed, or there are obvious code issues, return {\"ok\": false, \"reason\": \"Specify what still needs to be done\"}. If all tasks are complete, return {\"ok\": true}."
          }
        ]
      }
    ]
  }
}
```

**How it works**:
1. Every time Claude is about to stop, the `Stop` event fires
2. The `prompt` Hook sends the context to a lightweight model (Haiku by default) for evaluation
3. If it returns `"ok": false`, Claude continues working, using the `reason` as its next instruction
4. If it returns `"ok": true`, Claude stops normally

**Preventing infinite loops**: The Hook input includes a `stop_hook_active` field. When it is `true`, Claude is already in a continuation triggered by a Stop Hook -- your script should let it through. If implementing with the `command` type:

```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow through to prevent infinite loops
fi
# ... your validation logic here
```

### Config 9: Agent Hook -- Automated Test Verification

More powerful than `prompt`, the `agent` type can spawn a sub-agent with file reading and command execution capabilities:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test command and check the results. If any tests fail, return {\"ok\": false, \"reason\": \"Failed tests: ...\"}. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

This Hook automatically runs tests after Claude finishes. If tests fail, Claude continues fixing issues until everything passes.

### Config 10: Auto-Approve Read-Only Operations

Tired of Claude asking permission every time it reads or searches files? Use `PreToolUse` to auto-approve read-only operations:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Glob|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}'"
          }
        ]
      }
    ]
  }
}
```

**permissionDecision options**:
- `"allow"`: Approve immediately, no confirmation dialog
- `"deny"`: Reject immediately, with `permissionDecisionReason` to tell Claude why
- `"ask"`: Show the normal confirmation dialog (default behavior)

### Config 11: Replace Inefficient Commands

When Claude tries to use `grep`, automatically redirect it to `rg` (ripgrep):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'CMD=$(jq -r \".tool_input.command\" <<< \"$(cat)\"); if echo \"$CMD\" | grep -q \"^grep \"; then echo \"{\\\"hookSpecificOutput\\\":{\\\"hookEventName\\\":\\\"PreToolUse\\\",\\\"permissionDecision\\\":\\\"deny\\\",\\\"permissionDecisionReason\\\":\\\"Use rg (ripgrep) instead of grep for better performance\\\"}}\"; else exit 0; fi'"
          }
        ]
      }
    ]
  }
}
```

Claude receives the feedback "Use rg (ripgrep) instead of grep" and automatically switches to `rg`.

### Config 12: Slack Notifications

Send notifications to Slack instead of watching your desktop:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt|idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL' -H 'Content-Type: application/json' -d '{\"text\": \"Claude Code is waiting for your action\"}' > /dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

Replace `https://hooks.slack.com/services/YOUR/WEBHOOK/URL` with your actual Slack Webhook URL.

## Hook Input/Output Mechanism

Understanding how Hooks communicate with Claude Code is essential for writing more sophisticated configurations.

### Input (stdin)

When an event fires, Claude Code pipes context information to the Hook's stdin as JSON. For example, when Claude runs a Bash command, a `PreToolUse` Hook receives:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/you/project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Different events have different fields. Key field reference:

| Event | Core Fields |
|-------|------------|
| PreToolUse / PostToolUse | `tool_name`, `tool_input` |
| UserPromptSubmit | `prompt` (the user's raw input text) |
| SessionStart | `source` (startup / resume / compact) |
| Stop | `stop_hook_active` (whether in a Stop Hook continuation) |

### Output (stdout / stderr / exit code)

Hooks return results through three channels:

| Mechanism | Effect |
|-----------|--------|
| **exit 0** | Allow the operation. stdout content is injected into Claude's context (SessionStart and UserPromptSubmit events only) |
| **exit 2** | Block the operation. stderr content is sent as feedback to Claude |
| **Other exit codes** | Operation continues; stderr is written to logs but not shown to Claude |
| **JSON stdout** | With exit 0, output JSON for structured control (e.g., permissionDecision) |

### Debugging Tips

Two effective approaches for debugging Hooks:

**Method 1: Manually test Hook scripts**

```bash
# Simulate a PreToolUse event
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | bash .claude/hooks/protect-files.sh
echo $?  # Check exit code -- should be 2 (blocked)
```

**Method 2: Enable Claude Code verbose mode**

Press `Ctrl+O` in Claude Code to toggle verbose mode. Hook stderr output and execution results will appear in the transcript. Alternatively, start with the `--debug` flag:

```bash
claude --debug
```

## Complete Project Configuration: Putting It All Together

Combine the configurations above into a complete project-level Hook setup. Here is a real-world configuration for a TypeScript + React project:

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'CMD=$(jq -r \".tool_input.command\" <<< \"$(cat)\"); DANGEROUS=(\"rm -rf /\" \"rm -rf ~\" \"git push --force\" \"git reset --hard\"); for p in \"${DANGEROUS[@]}\"; do if echo \"$CMD\" | grep -qiF \"$p\"; then echo \"Blocked dangerous command: $CMD\" >&2; exit 2; fi; done; exit 0'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'INPUT=$(cat); CMD=$(echo \"$INPUT\" | jq -r \".tool_input.command\"); echo \"[$(date +\"%Y-%m-%d %H:%M:%S\")] $CMD\" >> \"$CLAUDE_PROJECT_DIR\"/.claude/command-log.txt'"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Project reminders:\n- Use pnpm (not npm)\n- Write descriptive commit messages\n- Run pnpm test before committing\n\nRecent commits:' && git log --oneline -5"
          }
        ]
      }
    ]
  }
}
```

`~/.claude/settings.json` (personal global config):

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

What this setup achieves:

| Layer | Configuration | Scope |
|-------|--------------|-------|
| Global | Desktop notifications | All projects |
| Project | File protection + dangerous command blocking | Current project |
| Project | Auto-formatting + command logging | Current project |
| Project | Context re-injection after compaction | Current project |

## Advanced Tips

### Use Script Files Instead of Inline Commands

When Hook logic gets complex, extract commands into standalone script files:

```
.claude/
├── hooks/
│   ├── protect-files.sh      # File protection
│   ├── format-code.sh        # Code formatting
│   ├── log-commands.sh       # Command logging
│   └── validate-commit.sh    # Commit validation
└── settings.json
```

Advantages of script files:
- Clearer logic, easier to maintain
- Room for comments
- Can be tested independently
- No JSON escape hell

### Matching MCP Tools

If you use MCP Servers (e.g., GitHub MCP), MCP tool names follow the format `mcp__<server>__<tool>`. Match them with regex:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__github__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"GitHub MCP tool called: $(jq -r '.tool_name')\" >&2"
          }
        ]
      }
    ]
  }
}
```

### Common Pitfalls and Solutions

**Pitfall 1: Shell profile pollutes JSON output**

If your `~/.zshrc` or `~/.bashrc` contains statements like `echo "Shell ready"`, Hook execution will mix those outputs into the JSON, causing parse failures.

**Solution**: Wrap them in an interactive shell check:

```bash
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

`$-` contains shell flags, and `i` indicates interactive mode. Hooks run in non-interactive shells, so the `echo` gets skipped.

**Pitfall 2: Stop Hook infinite loop**

If your Stop Hook always returns `"ok": false`, Claude will keep working forever. **Always check the `stop_hook_active` field** -- when it is `true`, Claude is already in a continuation from a previous Stop Hook trigger, and your Hook should let it through.

**Pitfall 3: Hook not triggering**

Troubleshooting checklist:
1. Can you see the Hook in the `/hooks` menu?
2. Is your matcher case-sensitive? (Yes -- `bash` does not match `Bash`)
3. Manually edited config files require restarting Claude Code or confirming in the `/hooks` menu to take effect
4. Is the JSON valid? (No trailing commas or comments allowed)

## Hooks vs Skills vs MCP: How to Choose

These three extension mechanisms are often confused, but they solve fundamentally different problems:

| Dimension | Hooks | Skills | MCP |
|-----------|-------|--------|-----|
| **Nature** | Lifecycle callbacks | Knowledge documents | Tool interface protocol |
| **Trigger** | Automatic, no AI judgment needed | AI matches based on context | AI chooses to call |
| **Determinism** | 100% guaranteed execution | Probabilistic (AI may not trigger) | Probabilistic |
| **Capability** | Block/allow/execute commands | Provide expertise and process guidance | Connect external tools and services |
| **Typical use** | Formatting, security, notifications | Code review standards, writing style | GitHub operations, database queries |

**Decision framework**:
- **Rules that must always execute** --> Hooks ("format files after every edit")
- **Needs domain expertise** --> Skills ("review code per our company standards")
- **Needs external tool access** --> MCP ("create a GitHub Issue for me")

All three work together. For example: use MCP to connect to GitHub, a Skill to define PR review standards, and a Hook to ensure tests pass before every commit.

## Summary

Hooks are the key to evolving Claude Code from "a helpful AI assistant" into "a reliable automation partner." The core problem they solve: **turning "things that should happen" from "hoping the AI remembers" into "the system guarantees it."**

The 12 configurations in this article cover the most common scenarios:

| # | Scenario | Event | Hook Type |
|---|----------|-------|-----------|
| 1 | Auto-format (Prettier) | PostToolUse | command |
| 2 | Auto-format (ESLint) | PostToolUse | command |
| 3 | Protect sensitive files | PreToolUse | command |
| 4 | Block dangerous commands | PreToolUse | command |
| 5 | Git auto-stage | PostToolUse | command |
| 6 | Bash command logging | PostToolUse | command |
| 7 | Context re-injection after compaction | SessionStart | command |
| 8 | Task completion check | Stop | prompt |
| 9 | Automated test verification | Stop | agent |
| 10 | Auto-approve read-only operations | PreToolUse | command |
| 11 | Replace inefficient commands | PreToolUse | command |
| 12 | Slack notifications | Notification | command |

Start with the simplest ones -- desktop notifications and auto-formatting -- then gradually add file protection and command safety checks. Once you get comfortable with this system, Claude Code becomes significantly more reliable. You are no longer "hoping" it does the right thing -- you are "guaranteeing" it.

---

**References**:

- [Claude Code Hooks Official Documentation](https://code.claude.com/docs/en/hooks-guide)
- [Hooks Reference (Event Schemas and Advanced Features)](https://code.claude.com/docs/en/hooks)
- [Claude Code Hooks Examples Collection](https://github.com/karanb192/claude-code-hooks)
- [Hooks Complete Guide (20+ Examples)](https://aiorg.dev/blog/claude-code-hooks)

## Related Reading

- [Claude Code Browser Automation Compared (2026 Update)](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Claude Code + Draw Things: Local AI Image Generation on Mac](/posts/ai/2026-02-16-claude-code-draw-things-workflow/)
- [Claude Code Skills Guide: Teach AI Your Workflow](/posts/ai/2026-01-08-claudecode-skill-guide/)
- [Skills vs MCP: Two Ways to Extend AI Capabilities](/posts/ai/2026-01-06-skill&mcp/)
- [Claude Code Memory: One File to Make AI Remember You](/posts/ai/2026-01-12-claudemd-memory-guide/)
- [OpenClaw Author's Claude Code Development Methodology](/posts/ai/2026-01-31-openclaw-claude-code-workflow/)
