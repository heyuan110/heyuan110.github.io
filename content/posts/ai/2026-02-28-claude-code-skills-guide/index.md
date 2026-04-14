+++
date = '2026-02-26T14:00:00+08:00'
draft = false
title = 'Claude Code Skills: 20 I Use Daily + 3 That Saved Me 10 Hours/Week'
description = 'The 20 Claude Code Skills I actually load every day, plus the 3 SKILL.md files that cut 10 hours/week off my workflow — with the exact frontmatter, triggers, and why they beat slash commands.'
toc = true
tags = ['Claude Code', 'Skills', 'Automation', 'Workflow']
categories = ['AI Guides']
keywords = ['claude code skills', 'claude code custom skills 2026', 'SKILL.md guide', 'claude code skill tutorial', 'claude code automation', 'claude code plugins', 'agent skills', 'claude code slash commands skills']

[[params.faqItems]]
question = "What is a Claude Code Skill and how do I create one?"
answer = "A Skill is a reusable set of instructions packaged as a SKILL.md file with YAML frontmatter and Markdown content. Create a directory at ~/.claude/skills/your-skill-name/ (personal) or .claude/skills/your-skill-name/ (project), then write a SKILL.md file with a name, description, and step-by-step instructions."

[[params.faqItems]]
question = "What is the difference between Claude Code Skills and slash commands?"
answer = "Slash commands (in .claude/commands/) require manual invocation every time. Skills (in .claude/skills/) can be triggered automatically when Claude detects a relevant conversation context, and also support manual invocation. Skills additionally support frontmatter for invocation control, supporting files, and model overrides."

[[params.faqItems]]
question = "How do Claude Code Skills compare to CLAUDE.md and Hooks?"
answer = "CLAUDE.md provides static project context like tech stack and conventions. Skills define reusable workflows that Claude decides when to apply. Hooks guarantee execution of specific actions (like linting after file edits). Use CLAUDE.md for context, Skills for repeatable workflows, and Hooks for mandatory steps."

[[params.faqItems]]
question = "Do Claude Code Skills increase token usage?"
answer = "No, Skills use a progressive disclosure pattern. At startup, only the frontmatter (about 100 tokens per Skill) loads into context. The full Skill content only loads when Claude determines it is relevant, so you can have dozens of Skills installed without bloating your context window."

[[params.faqItems]]
question = "Can Claude Code Skills run shell commands automatically?"
answer = "Yes, Skills support dynamic context injection using the !`command` syntax. Shell commands inside this syntax execute immediately when the Skill activates, and their output replaces the placeholder before Claude sees the content. This is useful for injecting live data like PR diffs or git logs."
+++

![Claude Code Skills guide for teaching AI custom workflows](cover.webp)

Claude Code is one of the most powerful AI coding tools available. But out of the box, it's generic. It doesn't know your team's code review checklist. It doesn't know your API documentation format. It doesn't know your commit message conventions.

Every time you explain the same workflow from scratch, you're wasting tokens and time.

Claude Code Skills fix this. A Skill is a reusable set of instructions — packaged as a simple Markdown file — that teaches Claude exactly how to perform a specific task your way. Once created, Claude auto-detects when a Skill is relevant and applies it without you lifting a finger.

This guide covers everything: what Skills are, how to create them, three practical examples you can copy today, the growing Skills ecosystem, and how Skills fit alongside CLAUDE.md and Hooks in the broader Claude Code configuration system.

## What Are Claude Code Skills?

A Skill is a folder containing a `SKILL.md` file with two parts:

1. **YAML frontmatter** (between `---` markers) that tells Claude when to use the Skill
2. **Markdown content** with instructions Claude follows when the Skill is invoked

Here's the simplest possible Skill:

```yaml
---
name: daily-standup
description: Generate a daily standup summary from git activity
---

Summarize today's git commits into a standup format:
1. What I did yesterday
2. What I'm doing today
3. Any blockers
```

That's it. No code. No configuration files. No build steps. Just a Markdown file that teaches Claude a new capability.

Skills follow the [Agent Skills](https://agentskills.io) open standard, which means they work across multiple AI tools — not just Claude Code. But Claude Code extends the standard with additional features like invocation control, subagent execution, and dynamic context injection.

### How Skills Get Triggered

Claude Code uses a progressive disclosure pattern for Skills:

1. **At startup**: Only the frontmatter (name + description) loads into context — roughly 100 tokens per Skill
2. **During conversation**: Claude reads the descriptions to decide which Skills are relevant
3. **On activation**: The full Skill content loads when Claude determines it's needed

This means you can have dozens of Skills installed without bloating your context window. Claude only loads what it needs, when it needs it.

You can also trigger any Skill manually using its name as a slash command:

```
/daily-standup
```

Both approaches work. Claude can auto-detect relevance from your conversation, or you can invoke a Skill directly when you know exactly what you want.

## Skills vs. Slash Commands

If you've been using Claude Code for a while, you might be familiar with custom slash commands (files in `.claude/commands/`). Here's how they relate to Skills:

| Feature | Slash Commands (Legacy) | Skills |
|---------|------------------------|--------|
| Location | `.claude/commands/review.md` | `.claude/skills/review/SKILL.md` |
| Invocation | Manual (`/review`) | Auto-triggered + manual (`/review`) |
| Supporting files | No | Yes (templates, scripts, examples) |
| Frontmatter | Optional | Supported (invocation control, tools, model) |
| Status | Still works | Recommended |

**The key difference**: Slash Commands require you to type `/command-name` every time. Skills can be triggered automatically by Claude when it detects a relevant conversation context — no manual invocation needed.

Custom slash commands still work. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and behave the same way. But Skills add optional features: supporting file directories, frontmatter for invocation control, and automatic triggering. If a Skill and a command share the same name, the Skill takes precedence.

> If you're starting fresh, use Skills. If you have existing commands, they'll keep working — migrate them when convenient.

## When to Use Skills

Skills shine in specific scenarios. Here's when to reach for them versus other Claude Code features:

**Use Skills when you have:**

- **Repetitive workflows** — Code reviews, PR creation, documentation generation, deployment checklists. Any task you do the same way every time.
- **Domain expertise** — Industry-specific knowledge, company conventions, framework-specific patterns. Things Claude doesn't know by default.
- **Fixed output formats** — Standup reports, changelog entries, API documentation, test plans. Any task where the output structure matters.
- **Team standards** — Coding conventions, architectural patterns, naming rules. Things every team member should follow consistently.

**Don't use Skills for:**

- **Static project context** — Use [CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) instead. Your tech stack, project structure, and general conventions belong in CLAUDE.md, not in a Skill.
- **Guaranteed execution** — Use [Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) instead. If a step must always run (like linting after file edits), a Hook guarantees it. Skills are suggestions — Claude decides whether to use them.
- **One-off tasks** — Just describe them in your prompt. Skills are for patterns you'll reuse.

## Creating Your First Skill

Let's build a Skill step by step. We'll create a code review Skill that enforces your team's review checklist.

### Step 1: Create the Skill Directory

Skills can live in two places:

| Level | Path | Scope |
|-------|------|-------|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |

For a code review Skill that applies to all your projects:

```bash
mkdir -p ~/.claude/skills/code-review
```

For a project-specific Skill:

```bash
mkdir -p .claude/skills/code-review
```

### Step 2: Write SKILL.md

Create `~/.claude/skills/code-review/SKILL.md`:

```yaml
---
name: code-review
description: Perform a thorough code review following the team checklist. Use when reviewing code changes, pull requests, or when the user asks for a code review.
---

# Code Review Checklist

When reviewing code, evaluate every item in this checklist and provide a structured report.

## Review Process

1. **Read the diff** — Understand what changed and why
2. **Check each category** — Go through every section below
3. **Rate severity** — Flag issues as Critical, Warning, or Suggestion
4. **Summarize** — Provide an overall assessment

## Checklist Categories

### Correctness
- Does the logic handle edge cases?
- Are error paths handled properly?
- Could any input cause unexpected behavior?

### Security
- Is user input validated and sanitized?
- Are there any SQL injection, XSS, or CSRF risks?
- Are secrets hardcoded anywhere?

### Performance
- Are there unnecessary database queries or API calls?
- Could any loop cause O(n^2) or worse performance?
- Are large datasets paginated?

### Maintainability
- Are functions and variables named clearly?
- Is the code DRY (Don't Repeat Yourself)?
- Would a new team member understand this code?

### Testing
- Are there tests for the new code?
- Do tests cover edge cases and error paths?
- Are tests deterministic (no flaky tests)?

## Output Format

Structure your review as:

### Summary
[One-paragraph overall assessment]

### Critical Issues
[Must fix before merging]

### Warnings
[Should fix, but not blocking]

### Suggestions
[Nice to have improvements]

### Approved?
[YES / NO / YES WITH CONDITIONS]
```

### Step 3: Test the Skill

Open Claude Code and test it both ways:

**Auto-triggered** — Ask something that matches the description:

```
Review the changes in src/auth/login.ts
```

Claude should recognize this as a code review request and automatically apply the Skill's checklist.

**Manually invoked** — Use the slash command:

```
/code-review src/auth/login.ts
```

Both approaches should produce a structured review following your checklist format.

### Step 4: Iterate

Your first version won't be perfect. Watch how Claude uses the Skill, then refine:

- If Claude misses checklist items, make them more explicit
- If the output format isn't quite right, add an example
- If the Skill triggers when it shouldn't, narrow the description
- If it doesn't trigger when it should, broaden the description

## SKILL.md Anatomy

Every `SKILL.md` file has the same structure: YAML frontmatter for metadata, followed by Markdown content for instructions.

### Frontmatter Reference

```yaml
---
name: my-skill
description: What this skill does and when to use it
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Grep, Glob
argument-hint: [filename] [format]
model: opus
context: fork
agent: Explore
---
```

Here's what each field does:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name and slash command. Defaults to directory name. Lowercase, hyphens, max 64 chars. |
| `description` | Recommended | What the Skill does. Claude uses this to decide when to load it. |
| `disable-model-invocation` | No | Set `true` to prevent auto-triggering. User must type `/name`. |
| `user-invocable` | No | Set `false` to hide from the `/` menu. Background knowledge only. |
| `allowed-tools` | No | Tools Claude can use without permission prompts when Skill is active. |
| `argument-hint` | No | Autocomplete hint (e.g., `[issue-number]`). |
| `model` | No | Override the model when this Skill is active. |
| `context` | No | Set `fork` to run in a subagent. |
| `agent` | No | Subagent type when `context: fork` is set. |

### Content Structure

The Markdown content after the frontmatter is entirely freeform, but effective Skills typically include these sections:

1. **Overview** — What the Skill does (1-2 sentences)
2. **Input Requirements** — What Claude needs from the user
3. **Step-by-Step Instructions** — The actual workflow
4. **Output Format** — How to structure the result
5. **Constraints** — What to avoid, edge cases, guardrails

### Variable Substitution

Skills support dynamic variables in the content:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking |
| `$ARGUMENTS[0]`, `$0` | First argument |
| `$ARGUMENTS[1]`, `$1` | Second argument |
| `${CLAUDE_SESSION_ID}` | Current session ID |

Example using arguments:

```yaml
---
name: fix-issue
description: Fix a GitHub issue by number
disable-model-invocation: true
---

Fix GitHub issue #$ARGUMENTS following our coding standards:

1. Read the issue description with `gh issue view $0`
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit referencing the issue
```

Running `/fix-issue 423` replaces `$ARGUMENTS` with `423` and `$0` with `423`.

### Dynamic Context Injection

The `` !`command` `` syntax runs shell commands before the Skill content is sent to Claude. The command output replaces the placeholder:

```yaml
---
name: pr-summary
description: Summarize the current pull request
context: fork
agent: Explore
---

## Current PR Context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Task
Provide a concise summary of this pull request highlighting:
1. What changed and why
2. Potential risks
3. Suggested reviewers
```

When this Skill runs, each `` !`command` `` executes immediately. Claude only sees the final rendered content with actual PR data.

## Three Practical Skills (Copy-Paste Ready)

Here are three production-ready Skills you can start using today.

### Skill 1: Code Review with Checklist

Already covered above in the tutorial. Here's the file path for quick reference:

```
~/.claude/skills/code-review/SKILL.md
```

### Skill 2: API Documentation Generator

This Skill generates consistent API documentation from your source code. It reads endpoint handlers and produces standardized docs.

Create `~/.claude/skills/api-docs/SKILL.md`:

```yaml
---
name: api-docs
description: Generate API documentation from source code. Use when the user asks to document an API endpoint, route handler, or controller. Also triggers when creating or updating API reference documentation.
allowed-tools: Read, Grep, Glob
---

# API Documentation Generator

Generate comprehensive API documentation for the specified endpoint(s).

## Process

1. **Find the endpoint** — Locate the route handler, controller, or API function
2. **Analyze the code** — Read the implementation to understand:
   - HTTP method and path
   - Request parameters (path, query, body)
   - Authentication requirements
   - Response format and status codes
   - Error handling
3. **Check for existing docs** — Look for JSDoc, docstrings, or OpenAPI annotations
4. **Generate documentation** — Follow the output format below

## Output Format

For each endpoint, generate:

### `METHOD /path/to/endpoint`

**Description**: One-sentence description of what this endpoint does.

**Authentication**: Required / Optional / None

**Parameters**:

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| id | path | string | Yes | Resource identifier |
| limit | query | integer | No | Max results (default: 20) |

**Request Body** (if applicable):

```json
{
  "field": "type — description"
}
```

**Response** `200 OK`:

```json
{
  "data": "example response"
}
```

**Error Responses**:

| Status | Description |
|--------|-------------|
| 400 | Invalid request parameters |
| 401 | Authentication required |
| 404 | Resource not found |

**Example**:

```bash
curl -X METHOD https://api.example.com/path \
  -H "Authorization: Bearer TOKEN" \
  -d '{"field": "value"}'
```

## Constraints

- Always include real field names and types from the source code
- Document all possible error responses, not just the happy path
- If authentication middleware is present, always note it
- Use the project's actual base URL if found in configuration
- Flag any undocumented endpoints as needing attention
```

### Skill 3: Git Commit Message Standardizer

This Skill enforces [Conventional Commits](https://www.conventionalcommits.org/) format with your team's specific rules.

Create `~/.claude/skills/commit-msg/SKILL.md`:

```yaml
---
name: commit-msg
description: Generate a standardized git commit message following Conventional Commits format. Use when the user asks to commit, create a commit message, or after completing a task that should be committed.
disable-model-invocation: true
---

# Commit Message Generator

Generate a git commit message following our team's Conventional Commits standard.

## Process

1. Run `git diff --staged` to see what's being committed
2. If nothing is staged, run `git diff` and ask the user what to stage
3. Analyze the changes to determine the commit type and scope
4. Generate the commit message following the format below

## Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (required)

| Type | When to use |
|------|------------|
| `feat` | New feature for the user |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, missing semicolons, no code change |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `chore` | Build process, dependencies, CI changes |

### Scope (optional)

The module or component affected. Use the directory name or feature name:
- `auth`, `api`, `ui`, `db`, `config`, `ci`

### Subject (required)

- Imperative mood: "add feature" not "added feature"
- No period at the end
- Max 50 characters
- Lowercase first letter

### Body (optional, but recommended for non-trivial changes)

- Explain **what** and **why**, not how
- Wrap at 72 characters
- Separate from subject with a blank line

### Footer (when applicable)

- Breaking changes: `BREAKING CHANGE: description`
- Issue references: `Closes #123` or `Fixes #456`

## Examples

**Simple bug fix:**
```
fix(auth): prevent token refresh race condition
```

**Feature with body:**
```
feat(api): add pagination to user search endpoint

The /users/search endpoint now supports cursor-based pagination
with configurable page sizes. This replaces the previous offset-based
approach which had performance issues with large datasets.

Closes #234
```

**Breaking change:**
```
refactor(db): migrate from MongoDB to PostgreSQL

BREAKING CHANGE: All database queries now use SQL syntax.
The MongoDB query builders have been removed. See migration
guide in docs/migration-v3.md.
```

## Constraints

- Never generate a message without reading the actual diff first
- If the diff contains multiple unrelated changes, suggest splitting into separate commits
- Always ask the user before committing — show the proposed message first
- Include Co-Authored-By if pair programming or AI-assisted
```

## The Skills Ecosystem

Claude Code Skills aren't just a personal productivity tool. A thriving ecosystem of community-created Skills has emerged, with thousands of developers sharing their workflows.

### Official Repository

Anthropic maintains the [anthropics/skills](https://github.com/anthropics/skills) repository with **78.9k+ stars**. It includes production-quality Skills for:

- **docx** — Word document creation, editing, and change tracking
- **pdf** — PDF extraction (text, tables, metadata, merging)
- **pptx** — PowerPoint generation and adjustment
- **xlsx** — Excel operations (formulas, charts, data transformation)
- **web-artifacts-builder** — Build complex interactive web components
- **skill-creator** — Interactive Skill creation wizard (Claude asks about your workflow, generates the folder structure and SKILL.md)

### Top Community Skills

The community Skills ecosystem has grown rapidly. Here are the most popular ones:

| Skill | Stars/Popularity | What It Does |
|-------|-----------------|-------------|
| **create-pr** | 170k+ | Auto-creates GitHub PRs with formatted titles, descriptions, CI validation |
| **skill-lookup** | 143k+ | Finds and installs Skills — ask "what Skills exist for X?" |
| **frontend-code-review** | 126k+ | Frontend-specific code review (tsx/ts/js checklist) |
| **component-refactoring** | 126k+ | React component refactoring with safety checks |
| **github-code-review** | 48k+ | Multi-agent collaborative code review |

### Superpowers Framework

The [Superpowers](https://github.com/obra/superpowers) project (**42k+ stars**, now in the official Anthropic plugin marketplace) is a comprehensive Skills framework that implements an entire software development methodology:

- **TDD Skill** — Enforces red-green-refactor cycles where tests must fail before implementation
- **Debugging Skill** — Four-phase debugging methodology requiring root cause investigation before fixes
- **Brainstorming Skill** — Socratic sessions that refine requirements before coding begins
- **Code Review Skill** — Structured review with subagent-driven analysis
- **Execute Plan Skill** — Batched implementation with review checkpoints

Superpowers transforms Claude Code from a code generator into something closer to a senior developer who follows disciplined practices.

### Awesome Lists

For a curated directory of community Skills:

- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) — Categorized list of Skills and resources
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — Skills, hooks, plugins, and agent orchestrators

## Installing Skills

There are several ways to add Skills to your Claude Code setup.

### Plugin Marketplace (Recommended)

The easiest way to install curated Skill packs:

```bash
# Browse the marketplace
/plugin marketplace add anthropics/skills

# Install specific plugin packs
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

For the Superpowers framework:

```bash
/plugin marketplace add obra/superpowers
```

### Manual Installation

For individual Skills from GitHub or other sources, copy the Skill folder to your skills directory:

**Personal level** (available across all projects):

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/my-new-skill

# Copy or create the SKILL.md
cp downloaded-skill/SKILL.md ~/.claude/skills/my-new-skill/SKILL.md
```

**Project level** (committed to version control, shared with team):

```bash
# Create in your project
mkdir -p .claude/skills/my-new-skill

# Copy the SKILL.md
cp downloaded-skill/SKILL.md .claude/skills/my-new-skill/SKILL.md

# Commit to share with team
git add .claude/skills/
git commit -m "feat: add code review skill for team"
```

### Project vs. Personal: How to Choose

| Scenario | Use Project-Level | Use Personal-Level |
|----------|------------------|--------------------|
| Team coding standards | Yes | No |
| Personal productivity shortcuts | No | Yes |
| Project-specific documentation format | Yes | No |
| Your preferred commit message style | No | Yes |
| Company-wide API conventions | Yes (or Enterprise) | No |
| General-purpose utilities | No | Yes |

**Rule of thumb**: If your teammates need the Skill, put it in the project. If it's your personal preference, put it in `~/.claude/skills/`.

### Priority Order

When Skills share the same name across levels, higher-priority locations win:

```
Enterprise > Personal > Project
```

Plugin Skills use a `plugin-name:skill-name` namespace, so they never conflict with other levels.

### Monorepo Support

Claude Code automatically discovers Skills from nested directories. If you're editing a file in `packages/frontend/`, Claude also looks for Skills in `packages/frontend/.claude/skills/`. This lets different packages in a monorepo have their own specialized Skills.

## Skills + CLAUDE.md + Hooks: The Complete System

Claude Code has three configuration systems that complement each other. Understanding how they fit together is the key to getting maximum value.

### CLAUDE.md: Who You Are

[CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) defines your project's identity and conventions. It's always loaded at the start of every session.

**Use it for**:
- Tech stack and architecture
- Coding conventions and style rules
- Common commands (`npm test`, `npm run lint`)
- Project structure overview
- General rules ("never use console.log in production")

### Skills: How to Do Tasks

Skills define step-by-step workflows for specific tasks. They load on demand when relevant.

**Use them for**:
- Code review checklists
- Documentation generation
- Commit message formatting
- Deployment procedures
- Any repeatable, structured workflow

### Hooks: Guaranteed Execution

[Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) run shell commands at specific lifecycle points. They always execute — no AI judgment involved.

**Use them for**:
- Auto-linting after file edits
- Running tests after changes
- Formatting code on save
- Validating commits before they're created
- Anything that must happen every single time

### How They Work Together

Here's a real-world example showing all three systems:

**CLAUDE.md** (project context):
```markdown
## Project: E-commerce API
- Stack: Node.js 22 + Express + PostgreSQL
- Testing: Jest, files in __tests__/
- Style: ESLint + Prettier, functional style
- Never use console.log — use the logger utility
```

**Skill** (code review workflow):
```yaml
---
name: review
description: Review code changes using our team checklist
---
Follow the team review checklist: correctness, security,
performance, maintainability, testing...
```

**Hook** (guaranteed linting):
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "command": "npx eslint --fix $FILE_PATH",
      "silent": true
    }]
  }
}
```

The result: CLAUDE.md ensures Claude understands your project. The Skill ensures code reviews follow your checklist. The Hook ensures every file edit gets auto-linted — even if Claude forgets.

| System | Loads When | AI Decides? | Guaranteed? |
|--------|-----------|-------------|-------------|
| CLAUDE.md | Every session | No (always loaded) | Yes |
| Skills | On demand / auto-detected | Yes (can be overridden) | No |
| Hooks | On matching tool events | No (always runs) | Yes |

**The key insight**: Don't put workflow instructions in CLAUDE.md and don't put project context in Skills. Keep each system focused on what it does best.

## Best Practices for Writing Skills

After studying hundreds of community Skills and building dozens of my own, here are the patterns that work.

### 1. Keep Skills Focused

**Good**: One Skill that does code reviews.
**Bad**: One Skill that does code reviews, generates docs, and formats commit messages.

Each Skill should do one thing well. If you need multiple workflows, create multiple Skills.

### 2. Optimal Length: 500–2000 Words

Skills under 500 words tend to be too vague — Claude has to guess too much. Skills over 2000 words waste context tokens and often contain redundant information.

The sweet spot: enough detail to remove ambiguity, not so much that you're writing a novel.

If your Skill needs extensive reference material (API specs, large checklists), use **supporting files**:

```
my-skill/
├── SKILL.md           # Core instructions (500-1500 words)
├── reference.md       # Detailed API docs (loaded on demand)
├── examples/
│   └── sample.md      # Example outputs
└── scripts/
    └── validate.sh    # Helper scripts
```

Reference them from SKILL.md:

```markdown
For complete API reference, see [reference.md](reference.md).
For example outputs, see [examples/sample.md](examples/sample.md).
```

Claude loads supporting files only when needed, keeping initial context lean.

### 3. Write Clear Descriptions

The `description` field is the single most important part of your Skill. Claude uses it to decide when to activate the Skill. Write it like you're explaining to a colleague when to use this workflow.

**Bad description**:
```yaml
description: Review code
```

**Good description**:
```yaml
description: Perform a thorough code review following the team checklist. Use when reviewing code changes, pull requests, diffs, or when the user asks for a code review, feedback on code, or quality assessment.
```

Include keywords users would naturally say. If they'd say "review my PR", make sure "PR" and "review" appear in the description.

### 4. Define the Output Format Explicitly

The number one complaint about AI-generated output is inconsistency. Skills solve this by defining exactly what the output should look like.

Always include an "Output Format" section with:
- Structure (headers, sections, lists)
- Required fields
- Examples of expected output

### 5. Don't Duplicate CLAUDE.md Content

CLAUDE.md is always in context. Skills load on demand. If you put the same information in both, you waste tokens when the Skill activates (the info loads twice).

**Wrong**: Repeating your tech stack in every Skill.
**Right**: Reference it — "Follow the coding conventions defined in CLAUDE.md."

### 6. Use `disable-model-invocation` for Dangerous Actions

Any Skill that has side effects — deploying, sending messages, deleting resources — should be manual-only:

```yaml
---
name: deploy
description: Deploy to production
disable-model-invocation: true
---
```

You don't want Claude deciding to deploy because your code "looks ready."

### 7. Test with Both Invocation Methods

Always test your Skill two ways:
1. **Auto-triggered**: Ask something that should match the description
2. **Manual**: Type `/skill-name` directly

If auto-triggering works but manual doesn't (or vice versa), there's a configuration issue to fix.

### 8. Use Supporting Files for Complex Skills

Keep `SKILL.md` under 500 lines. Move detailed reference material, large checklists, and example collections to separate files. This keeps the main Skill focused and reduces context usage.

## Troubleshooting

### Skill Not Triggering Automatically

1. **Check the description** — Does it include keywords from your prompt?
2. **Verify discovery** — Ask Claude: "What skills are available?"
3. **Check the budget** — If you have many Skills, they may exceed the description budget. Run `/context` to check for warnings.
4. **Try manual invocation** — Type `/skill-name` to confirm the Skill loads correctly.

### Skill Triggers Too Often

1. **Narrow the description** — Be more specific about when to use it
2. **Add `disable-model-invocation: true`** — Switch to manual-only

### Skill Description Shows as ">-" Instead of Text

Claude Code's skill indexer doesn't parse YAML multiline indicators (`>-`, `|`, `|-`) correctly. Write your description on a single line:

```yaml
# Bad — may not parse correctly
description: >-
  This is a multi-line
  description

# Good — always works
description: This is a single-line description that works correctly
```

### Too Many Skills Exceeding Context Budget

The description budget scales at 2% of the context window (fallback: 16,000 characters). If you see a warning about excluded Skills:

- Remove Skills you don't use
- Shorten descriptions (keep the keywords, cut the filler)
- Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable to override the limit

## Related Reading

- [Claude Code Setup Guide: Installation to First Project](/posts/ai/2026-02-25-claude-code-setup-guide/) — Get Claude Code installed and configured
- [CLAUDE.md Guide: Give AI Perfect Project Context](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — Master the project context system that Skills complement
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Automate workflows with guaranteed execution
- [Claude Code MCP Setup](/posts/ai/2026-02-28-claude-code-mcp-setup/) — Extend Claude with external tool integrations
- [10 Claude Code Mistakes Beginners Make](/posts/ai/2026-02-25-claude-code-mistakes/) — Avoid common pitfalls
- [Official Skills Documentation](https://code.claude.com/docs/en/skills) — Anthropic's reference docs
- [anthropics/skills Repository](https://github.com/anthropics/skills) — Official Skills collection (78k+ stars)
- [Superpowers Framework](https://github.com/obra/superpowers) — Comprehensive development methodology Skills (42k+ stars)
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Anthropic's 32-page deep dive
