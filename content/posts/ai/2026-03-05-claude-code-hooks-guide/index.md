+++
date = '2026-03-04T09:00:00+08:00'
draft = false
title = 'How Claude Code Hooks Work: 17 Lifecycle Events Explained'
description = 'What Claude Code hooks are and how they work: all 17 lifecycle events explained, hook types, matcher rules, and exit codes — a beginner-friendly reference.'
toc = true
tags = ['Claude Code', 'Hooks', 'Automation', 'Developer Tools']
categories = ['AI Guides']
keywords = ['what are claude code hooks', 'how do claude code hooks work', 'claude code lifecycle events', 'claude code hook events list', 'claude code hooks explained', 'claude code hooks for beginners', 'claude code hook types']

[[params.faqItems]]
question = "What are Claude Code hooks and how do they work?"
answer = "Claude Code hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. They are configured in settings.json and can run before or after tool calls, on session start/end, or when Claude finishes responding. Hooks receive JSON context via stdin and use exit codes or JSON output to control behavior."

[[params.faqItems]]
question = "How many lifecycle events do Claude Code hooks support?"
answer = "Claude Code supports 17 lifecycle events, grouped into session events (SessionStart, InstructionsLoaded, SessionEnd), user input (UserPromptSubmit), the tool loop (PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure), completion events (Stop, SubagentStart, SubagentStop, Notification, TeammateIdle, TaskCompleted), and context/config events (PreCompact, ConfigChange, WorktreeCreate). Beginners should focus on five: PreToolUse, PostToolUse, Notification, Stop, and SessionStart."

[[params.faqItems]]
question = "Can Claude Code hooks block dangerous commands?"
answer = "Yes. PreToolUse hooks run before a tool executes and can block the operation. Your hook script inspects the command via stdin JSON, and if it matches a dangerous pattern (like rm -rf / or DROP TABLE), the hook returns exit code 2 or a JSON deny decision to prevent execution. The blocked command never reaches your shell."

[[params.faqItems]]
question = "What is the difference between Claude Code hooks, CLAUDE.md, and Skills?"
answer = "Hooks are automatic lifecycle scripts for enforcement, formatting, and logging that run every time without prompting. CLAUDE.md provides persistent project context and instructions loaded at session start. Skills are reusable prompt workflows triggered manually by the user with slash commands. Use hooks for deterministic automation, CLAUDE.md for project knowledge, and skills for on-demand workflows."

[[params.faqItems]]
question = "How do I debug Claude Code hooks that are not working?"
answer = "Check these common issues: matcher values are case-sensitive (use Bash not bash), hooks must read stdin with cat or jq (unread stdin is lost), shell profile output can corrupt JSON parsing, and hooks have a default timeout (600 seconds for commands). Use verbose mode (Ctrl+O) to see hook output. Test your hook script manually by piping sample JSON to it."
+++

![Claude Code Hooks guide for automating AI coding workflows](cover.webp)

Claude Code is probabilistic by nature. Ask it to format your code, and it might. Ask it to never touch `.env` files, and it usually respects that -- until it doesn't.

Claude Code hooks solve this. They are shell commands, HTTP endpoints, or LLM prompts that run automatically at specific points during Claude's operation. Before a file edit happens, after a command runs, when a session starts, when Claude finishes a task. Hooks give you deterministic control over the parts of your workflow that cannot be left to chance.

This guide explains how hooks work from the ground up: what they are, all 17 lifecycle events, the configuration format, matcher rules, 8 starter examples, and when to choose hooks over [CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) or [Skills](/posts/ai/2026-02-28-claude-code-skills-guide/).

## What Are Claude Code Hooks?

Hooks are user-defined automation that Claude Code executes at specific lifecycle points. Think of them like [Git hooks](https://git-scm.com/docs/githooks), but for your AI coding assistant instead of your version control system.

Here is the key difference between hooks and natural language instructions: when you tell Claude "always run Prettier after editing files," Claude *might* forget, *might* decide it is unnecessary, or *might* interpret it differently across sessions. A `PostToolUse` hook that runs Prettier will fire every single time, on every file edit, with zero exceptions.

### Four Hook Types

Every hook handler has a `type` field that determines how it operates:

| Type | What It Does | Best For |
|------|-------------|----------|
| `command` | Runs a shell command | Formatting, logging, file protection, notifications |
| `http` | Sends a POST request to a URL | Remote validation services, webhook integrations |
| `prompt` | Sends a prompt to a Claude model for single-turn evaluation | Context re-injection, yes/no validation |
| `agent` | Spawns a subagent with tool access | Complex multi-step verification, test suite analysis |

The `command` type handles 90% of use cases. Start there.

### 17 Lifecycle Events

Hooks attach to specific events during Claude's operation. Here are all 17 events, grouped by when they fire:

**Session lifecycle:**

| Event | When It Fires | Can Block? |
|-------|--------------|------------|
| `SessionStart` | Session begins or resumes | No |
| `InstructionsLoaded` | A CLAUDE.md or rules file loads into context | No |
| `SessionEnd` | Session terminates | No |

**User input:**

| Event | When It Fires | Can Block? |
|-------|--------------|------------|
| `UserPromptSubmit` | User submits a prompt, before Claude processes it | Yes |

**Tool lifecycle (the agentic loop):**

| Event | When It Fires | Can Block? |
|-------|--------------|------------|
| `PreToolUse` | Before a tool call executes | Yes |
| `PermissionRequest` | When a permission dialog appears | Yes |
| `PostToolUse` | After a tool call succeeds | No |
| `PostToolUseFailure` | After a tool call fails | No |

**Completion:**

| Event | When It Fires | Can Block? |
|-------|--------------|------------|
| `Stop` | Claude finishes responding | Yes |
| `SubagentStart` | A subagent is spawned | No |
| `SubagentStop` | A subagent finishes | Yes |
| `Notification` | Claude sends a notification | No |
| `TeammateIdle` | An agent team teammate is about to go idle | Yes |
| `TaskCompleted` | A task is being marked as completed | Yes |

**Context and config:**

| Event | When It Fires | Can Block? |
|-------|--------------|------------|
| `PreCompact` | Before context compaction | No |
| `ConfigChange` | A config file changes during a session | Yes |
| `WorktreeCreate` | A worktree is being created | Yes |

For everyday automation, focus on these five: `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, and `SessionStart`.

## Configuration Format

### Where Hooks Live

Hooks are defined in JSON settings files. Where you put them determines their scope:

| Scope | File Path | Who It Affects |
|-------|-----------|---------------|
| **Project** | `.claude/settings.json` | Everyone on the team (commit to Git) |
| **User** | `~/.claude/settings.json` | All your projects, just you |
| **Local** | `.claude/settings.local.json` | This project, just you (gitignored) |
| **Plugin** | `hooks/hooks.json` in a plugin | When the plugin is enabled |
| **Managed** | Organization policy settings | All users in the org |

**Recommendation**: Put shared automation in `.claude/settings.json` so your whole team benefits. Put personal preferences (like desktop notifications) in `~/.claude/settings.json`.

### Configuration Structure

The configuration has three levels of nesting: event, matcher group, and hook handlers.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-shell-command-here",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Breaking this down:

1. **Event** (`PostToolUse`): Choose which lifecycle event triggers this hook
2. **Matcher group** (`"matcher": "Edit|Write"`): Filter which tool calls trigger it
3. **Hook handlers** (the `hooks` array): One or more commands to run when matched

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `type` | Yes | -- | `"command"`, `"http"`, `"prompt"`, or `"agent"` |
| `command` | Yes (for command type) | -- | Shell command to execute |
| `matcher` | No | Match all | Regex pattern to filter which tools trigger this hook |
| `timeout` | No | 600s (command), 30s (prompt) | Max execution time in seconds |
| `async` | No | false | Run in background without blocking (command type only) |
| `statusMessage` | No | -- | Custom spinner message while the hook runs |

### Matcher Rules

The `matcher` field uses regex and is case-sensitive. This is the most common source of bugs.

| Matcher Value | What It Matches |
|--------------|----------------|
| `"Bash"` | The Bash tool only |
| `"Edit"` | The Edit tool only |
| `"Write"` | The Write tool only |
| `"Edit\|Write"` | Edit OR Write |
| `"mcp__.*"` | All MCP tools |
| `"mcp__github__.*"` | All tools from the GitHub MCP server |
| `"mcp__memory__create_entities"` | One specific MCP tool |
| Not specified or `"*"` | Every occurrence of the event |

**Critical**: `"Bash"` works, `"bash"` does not. Tool names are PascalCase. Double-check your matchers.

Different events match on different fields. For `PreToolUse`/`PostToolUse`, the matcher checks the tool name. For `SessionStart`, it checks the session source (`startup`, `resume`, `clear`, `compact`). For `Notification`, it checks the notification type. Some events like `Stop` and `UserPromptSubmit` do not support matchers at all and always fire on every occurrence.

### Input/Output Mechanism

Hook commands receive JSON context via **stdin**. The exact fields depend on the event, but all events include these common fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

For `PreToolUse` and `PostToolUse`, you also get `tool_name` and `tool_input`:

```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Use `jq` to extract specific fields:

```bash
# Extract the bash command
jq -r '.tool_input.command'

# Extract the file path from an Edit operation
jq -r '.tool_input.file_path'
```

### Exit Codes and Decision Control

For `PreToolUse` hooks, your exit code controls what happens next:

| Exit Code | Effect |
|-----------|--------|
| `0` | Allow the operation (check stdout for JSON decisions) |
| `2` | **Block** the operation -- stderr is fed back to Claude |
| Other | Non-blocking error -- operation proceeds, error is logged |

For richer control on exit 0, return structured JSON to stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Safe read-only command"
  }
}
```

Valid values for `permissionDecision`:
- `"allow"` -- Skip the permission prompt, auto-approve
- `"deny"` -- Block the operation (equivalent to exit code 2)
- `"ask"` -- Show the normal permission prompt to the user

For `Stop` and `PostToolUse` hooks, use a top-level `decision` field instead:

```json
{
  "decision": "block",
  "reason": "Tests must pass before stopping"
}
```

## 8 Practical Hook Examples

Here are 8 production-ready configurations. Each one is a complete JSON snippet for your `.claude/settings.json`.

### 1. Auto-Format Code After File Edits

Automatically run Prettier on every file Claude edits or creates. No more "can you format that?" follow-ups.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path // empty') && [ -n \"$FILE\" ] && npx prettier --write \"$FILE\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**How it works**: After every `Edit` or `Write` operation, the hook reads the JSON from stdin with `jq`, extracts the file path, and runs Prettier. The `2>/dev/null || true` ensures the hook does not fail on files Prettier cannot handle.

**Prerequisite**: `npm install --save-dev prettier` in your project.

### 2. Block Dangerous Shell Commands

Prevent destructive commands from ever reaching your shell, no matter what Claude generates:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "CMD=$(jq -r '.tool_input.command // empty') && if echo \"$CMD\" | grep -qEi '(rm\\s+-rf\\s+/|DROP\\s+TABLE|DROP\\s+DATABASE|mkfs\\.|chmod\\s+-R\\s+777\\s+/)'; then jq -n '{hookSpecificOutput: {hookEventName: \"PreToolUse\", permissionDecision: \"deny\", permissionDecisionReason: \"Dangerous command blocked by hook\"}}'; fi"
          }
        ]
      }
    ]
  }
}
```

**Blocked patterns**: `rm -rf /`, `DROP TABLE`, `DROP DATABASE`, `mkfs.` (format filesystem), `chmod -R 777 /`.

**How it works**: The hook inspects the command Claude wants to run. If it matches a dangerous pattern, the hook outputs a JSON deny decision. The command never executes. Customize the grep pattern to add project-specific dangerous commands.

### 3. Protect Sensitive Files From Modification

Block Claude from editing `.env` files, lockfiles, credentials, and other files that should never be AI-modified:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path // empty') && if echo \"$FILE\" | grep -qE '(\\.env|\\.lock$|secrets\\.yaml|credentials|id_rsa|\\.pem$)'; then echo \"BLOCKED: Cannot modify protected file: $FILE\" >&2; exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

**How it works**: Before any `Edit` or `Write` operation, the hook checks the target file against a list of protected patterns. If matched, it exits with code 2 and sends an error message via stderr. Claude sees the message and understands why the operation was blocked.

### 4. Lint Check Before Commits

Run ESLint auto-fix on JavaScript/TypeScript files after every edit, catching issues before they make it into a commit:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path // empty') && [ -n \"$FILE\" ] && [[ \"$FILE\" =~ \\.(js|ts|jsx|tsx)$ ]] && npx eslint --fix \"$FILE\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**How it works**: Same pattern as the Prettier hook, but with a file extension check so ESLint only runs on JavaScript/TypeScript files. Pair this with the Prettier hook for complete code quality automation.

### 5. Desktop Notification on Task Completion

Get a system notification when Claude needs your attention. Essential for long-running tasks where you switch to another window.

**macOS:**

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "MSG=$(jq -r '.message // \"Needs attention\"') && osascript -e \"display notification \\\"$MSG\\\" with title \\\"Claude Code\\\"\""
          }
        ]
      }
    ]
  }
}
```

**Linux:**

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "MSG=$(jq -r '.message // \"Needs attention\"') && notify-send 'Claude Code' \"$MSG\""
          }
        ]
      }
    ]
  }
}
```

**Tip**: Put this in `~/.claude/settings.json` (user-level) so it works across all your projects.

### 6. Auto-Run Tests When Claude Stops

Use a `Stop` hook to verify Claude's work by running your test suite before accepting the result:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm test 2>&1 | tail -20; if [ ${PIPESTATUS[0]} -ne 0 ]; then echo '{\"decision\": \"block\", \"reason\": \"Tests failed. Please fix the failing tests before finishing.\"}'; fi"
          }
        ]
      }
    ]
  }
}
```

**How it works**: When Claude tries to stop, the hook runs `npm test`. If tests fail, it outputs a JSON `decision: "block"` which prevents Claude from stopping and feeds the failure reason back to Claude. Claude then continues working to fix the failing tests.

**Warning**: This hook makes Claude do more work (and use more tokens) on every task. Use it selectively on projects where correctness matters more than speed.

### 7. Log All Commands for Auditing

Keep a timestamped log of every shell command Claude runs. Useful for debugging, security audits, and understanding what Claude did in a session:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\" + (now | strftime(\"%Y-%m-%d %H:%M:%S\")) + \"] \" + .tool_input.command' >> \"${CLAUDE_PROJECT_DIR:-.}/.claude/command_log.txt\"",
            "async": true
          }
        ]
      }
    ]
  }
}
```

**Output example:**

```
[2026-03-05 14:32:15] npm test
[2026-03-05 14:32:48] git status
[2026-03-05 14:33:02] cat src/index.ts
```

The `"async": true` flag runs the logging in the background so it does not slow down Claude's workflow. Add `.claude/command_log.txt` to your `.gitignore`.

### 8. Auto-Allow Safe Read-Only Commands

Skip permission prompts for commands that only read data, while still prompting for writes:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "CMD=$(jq -r '.tool_input.command // empty') && if echo \"$CMD\" | grep -qE '^(ls|cat|head|tail|wc|find|grep|rg|git\\s+(status|log|diff|show|branch)|echo|pwd|which|file|stat)\\b'; then echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PreToolUse\", \"permissionDecision\": \"allow\", \"permissionDecisionReason\": \"Safe read-only command\"}}'; fi"
          }
        ]
      }
    ]
  }
}
```

**How it works**: The hook checks if the command starts with a known safe command. If it does, it returns a `permissionDecision: "allow"` to skip the permission prompt. For any other command, the hook produces no output, falling through to the default permission behavior.

**Security note**: Review the allow-listed commands for your environment. Remove anything you consider potentially risky.

## Complete Project Configuration

Here is a real-world `.claude/settings.json` that combines several hooks into a production setup:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path // empty') && if echo \"$FILE\" | grep -qE '(\\.env|\\.lock$|secrets\\.yaml|credentials)'; then echo \"BLOCKED: Protected file: $FILE\" >&2; exit 2; fi"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "CMD=$(jq -r '.tool_input.command // empty') && if echo \"$CMD\" | grep -qEi '(rm\\s+-rf\\s+/|DROP\\s+TABLE)'; then echo \"BLOCKED: Dangerous command\" >&2; exit 2; fi"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "CMD=$(jq -r '.tool_input.command // empty') && if echo \"$CMD\" | grep -qE '^(ls|cat|head|tail|grep|rg|git\\s+(status|log|diff)|pwd|which)\\b'; then echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}'; fi"
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
            "command": "FILE=$(jq -r '.tool_input.file_path // empty') && [ -n \"$FILE\" ] && npx prettier --write \"$FILE\" 2>/dev/null; git add \"$FILE\" 2>/dev/null || true"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\" + (now | strftime(\"%Y-%m-%d %H:%M:%S\")) + \"] \" + .tool_input.command' >> \"${CLAUDE_PROJECT_DIR:-.}/.claude/command_log.txt\"",
            "async": true
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

This configuration:

1. **Blocks** modifications to `.env`, lockfiles, and secrets
2. **Blocks** destructive shell commands like `rm -rf /`
3. **Auto-allows** safe read-only commands without permission prompts
4. **Auto-formats** edited files with Prettier
5. **Auto-stages** edited files with `git add`
6. **Logs** all Bash commands with timestamps (async, non-blocking)
7. **Sends** macOS desktop notifications

**Matcher group order matters**: `PreToolUse` matcher groups are evaluated in array order. The file protection group runs before the auto-allow group, so protected files are always blocked even if the command itself would be auto-allowed.

## Advanced Techniques

### Use Script Files for Complex Logic

Inline commands get unreadable fast. For anything beyond a one-liner, use a script file:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-command.sh"
          }
        ]
      }
    ]
  }
}
```

Then create `.claude/hooks/validate-command.sh`:

```bash
#!/bin/bash
# .claude/hooks/validate-command.sh
# Validates Bash commands before execution

# Read the full JSON input from stdin
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Define blocked patterns
DANGEROUS_PATTERNS=(
  'rm\s+-rf\s+/'
  'DROP\s+TABLE'
  'DROP\s+DATABASE'
  'mkfs\.'
  'chmod\s+-R\s+777\s+/'
  'dd\s+if=.*of=/dev/'
)

# Check each pattern
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$CMD" | grep -qEi "$pattern"; then
    # Output structured deny decision
    jq -n --arg reason "Blocked pattern: $pattern" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: $reason
      }
    }'
    exit 0
  fi
done

# If nothing matched, allow the command
exit 0
```

Make it executable: `chmod +x .claude/hooks/validate-command.sh`

### Re-Inject Context After Compaction

When Claude compacts its context window, it can lose important project details. Use a `PostToolUse` hook on compaction or a `SessionStart` hook on compact to re-inject critical context. Alternatively, the simplest approach is a `prompt` type hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat \"${CLAUDE_PROJECT_DIR}/.claude/compaction-context.md\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

Create `.claude/compaction-context.md` with your critical project rules. The file contents are sent to stdout, which `SessionStart` adds as context for Claude.

### Persist Environment Variables with SessionStart

`SessionStart` hooks have access to `CLAUDE_ENV_FILE`, which lets you persist environment variables for all subsequent Bash commands in the session:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "[ -n \"$CLAUDE_ENV_FILE\" ] && echo 'export NODE_ENV=development' >> \"$CLAUDE_ENV_FILE\" && echo 'export DEBUG=true' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

This is useful for setting up project-specific environment variables without modifying shell profiles.

### HTTP Hooks for Remote Validation

For teams with centralized validation services, HTTP hooks send the event JSON as a POST request:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/validate-command",
            "timeout": 10,
            "headers": {
              "Authorization": "Bearer $API_TOKEN"
            },
            "allowedEnvVars": ["API_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

The endpoint receives the same JSON that command hooks get on stdin, but as the POST request body. Return the same JSON output format in the response body.

## Common Pitfalls

**1. Case sensitivity in matchers**

`"Bash"` matches. `"bash"` does not. `"Edit"` matches. `"edit"` does not. Tool names in Claude Code are PascalCase.

**2. Not reading stdin**

Your hook receives JSON via stdin. If your command does not read it, the data is lost:

```bash
# Wrong -- stdin is never consumed
echo "hook ran"

# Right -- read stdin, then process
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command')
```

**3. Shell profile pollution**

Hooks run in a shell that may source your profile. If `~/.bashrc` or `~/.zshrc` prints output (welcome messages, echo statements), that output mixes with the hook's stdout and corrupts JSON parsing. Keep your shell profile clean.

**4. Infinite loops with Stop hooks**

A Stop hook that tells Claude to "keep working" triggers another Stop event when Claude finishes, which fires the hook again. Always include a guard condition. With `command` type Stop hooks, check your JSON decision carefully. With `prompt` type Stop hooks, include an instruction like: "If stop_hook_active is already true in context, do NOT trigger this check again."

**5. Timeout kills**

Hooks have a default timeout of 600 seconds for commands. If your hook calls a slow external API, set a custom timeout. If the timeout is hit, the hook is killed.

**6. Missing jq**

All command hooks that parse stdin need `jq` installed. On macOS: `brew install jq`. On Ubuntu/Debian: `sudo apt install jq`. This is a hard dependency for most hook scripts.

**7. Hooks are snapshotted at startup**

Direct edits to hooks in settings files do not take effect immediately. Claude Code captures a snapshot of hooks when it starts and uses that snapshot for the entire session. If you modify hooks mid-session, Claude Code warns you and requires review in the `/hooks` menu before changes apply.

## Hooks vs CLAUDE.md vs Skills: When to Use Each

Claude Code has three extension mechanisms. They serve different purposes:

| Feature | [Hooks](https://code.claude.com/docs/en/hooks) | [CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) | [Skills](/posts/ai/2026-02-28-claude-code-skills-guide/) |
|---------|-------|-----------|--------|
| **What they do** | Run code at lifecycle events | Provide persistent project context | Define reusable prompt workflows |
| **When they run** | Automatically, every time the event fires | Loaded at session start, always in context | Manually, when the user invokes a slash command |
| **Can block operations?** | Yes (PreToolUse exits with code 2 or deny) | No -- advisory only | No -- advisory only |
| **Token cost** | Zero for command type | Proportional to file size | Depends on prompt length |
| **Best for** | Enforcement, automation, formatting, logging, security | Tech stack, coding conventions, project structure | Reusable workflows, deployment scripts, templates |
| **Where defined** | `settings.json` | `CLAUDE.md` files | `.claude/skills/` Markdown files |

**Decision framework:**

- Something must happen **automatically and reliably** every time? Use **hooks** (formatting, protection, logging, notifications).
- Claude needs to **know** something about your project? Use **[CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/)** (tech stack, conventions, commands, architecture).
- You want a **reusable workflow** triggered on demand? Use **[Skills](/posts/ai/2026-02-28-claude-code-skills-guide/)** (deployment, code review, scaffolding).

## Getting Started

If you are new to hooks, start with these three and expand from there:

1. **Desktop notification** (Example #5) -- Immediate quality-of-life improvement. Put it in `~/.claude/settings.json`.
2. **Protect sensitive files** (Example #3) -- A safety net you will be glad you have. Put it in `.claude/settings.json`.
3. **Auto-format with Prettier** (Example #1) -- Eliminates the most common follow-up request. Put it in `.claude/settings.json`.

You can also use the interactive `/hooks` menu inside Claude Code to add, view, and manage hooks without editing JSON files directly. Type `/hooks` in any session to open it.

From there, layer on more hooks as your workflow demands. The combined configuration above is a solid target to build toward.

## Related Reading

- [Claude Code Hooks: PreToolUse, PostToolUse & settings.json](/posts/ai/2026-02-28-claude-code-hooks-guide/) -- Deep reference for the two most-used events and their config format
- [Claude Code Hooks Examples: 12 Copy-Paste Automation Configs](/posts/ai/2026-02-18-claude-code-hooks-guide/) -- A recipe-style config library you can paste as-is
- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) -- Full overview of Claude Code features and setup
- [Claude Code Setup Guide](/posts/ai/2026-02-25-claude-code-setup-guide/) -- Installation and initial configuration
- [CLAUDE.md Guide](/posts/ai/2026-02-28-claude-code-claudemd-guide/) -- Project context and memory configuration
- [Claude Code Skills Guide](/posts/ai/2026-02-28-claude-code-skills-guide/) -- Slash commands and reusable workflows
- [Claude Code MCP Setup](/posts/ai/2026-02-28-claude-code-mcp-setup/) -- External service integration with MCP
- [Official Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) -- Anthropic's complete reference documentation
