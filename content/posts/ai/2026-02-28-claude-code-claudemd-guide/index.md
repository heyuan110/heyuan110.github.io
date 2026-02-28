+++
date = '2026-02-28T08:00:00+08:00'
draft = false
title = 'CLAUDE.md Guide: Give AI Perfect Project Context Every Time'
description = 'Master CLAUDE.md to make Claude Code understand your project, coding style, and workflow from the first prompt. Three-layer config, templates, advanced tips, and real-world examples.'
toc = true
tags = ['Claude Code', 'CLAUDE.md', 'Configuration', 'Best Practices']
categories = ['AI Guides']
keywords = ['CLAUDE.md guide', 'CLAUDE.md tutorial', 'Claude Code configuration', 'Claude Code project context', 'CLAUDE.md best practices', 'Claude Code memory', 'CLAUDE.md template']
+++

Every time you start a new Claude Code session, you repeat the same things: "We use pnpm, not npm." "Follow ESLint rules." "Commit messages in conventional format." "This is a Next.js 15 project with TypeScript."

Day after day. Session after session.

CLAUDE.md fixes this permanently. It's a plain Markdown file that Claude Code reads automatically at the start of every session. Write your project context once, and Claude follows it forever — no reminders needed.

This guide covers everything: what CLAUDE.md is, the three-layer configuration system, four ways to manage it, copy-paste templates, and advanced tips from real-world projects. If you're new to Claude Code, start with our [setup guide](/posts/ai/2026-02-25-claude-code-setup-guide/) first.

## What Is CLAUDE.md?

CLAUDE.md is Claude Code's memory file. It's a standard Markdown document placed in your project root (or other locations — more on that later) that gets loaded into context automatically every time you start a conversation.

Think of it this way: when a new developer joins your team, you hand them an onboarding doc. CLAUDE.md is that onboarding doc — except the new hire is an AI agent.

### What Goes in CLAUDE.md

- Project tech stack and architecture
- Coding conventions and style rules
- Common commands (build, test, lint, deploy)
- Directory structure overview
- Workflow instructions (Git conventions, PR process)
- Anything Claude keeps getting wrong that you're tired of correcting

### When Does It Get Loaded?

Every time you launch Claude Code or start a new conversation, it automatically searches for and loads CLAUDE.md files. You don't need to mention it, reference it, or ask Claude to read it. It just happens.

Claude Code also recursively scans parent directories for CLAUDE.md files. If you have a monorepo with `frontend/CLAUDE.md` and `backend/CLAUDE.md`, the relevant file loads when Claude works in that subdirectory.

### A Simple Example

Here's a minimal CLAUDE.md that already makes a difference:

```markdown
# E-commerce API

## Stack
- Node.js 22 + Express + TypeScript
- PostgreSQL + Prisma ORM
- Redis for caching

## Commands
- Dev: pnpm dev
- Test: pnpm test
- Lint: pnpm lint
- Build: pnpm build

## Rules
- Use functional style. No classes except Prisma models.
- All API endpoints must have input validation with Zod.
- Never use console.log in production code. Use the logger utility.
- Commit message format: type: description (e.g., feat: add user auth)
```

Fifteen lines. Takes two minutes to write. Saves hours of repeated explanations across every session.

## The Three-Layer Configuration System

CLAUDE.md isn't a single file — it's a three-layer system designed for different scopes. Each layer serves a distinct purpose, and later layers override earlier ones.

### Layer 1: Global Config — `~/.claude/CLAUDE.md`

This file lives in your home directory. It applies to **every project** you work on with Claude Code.

**What to put here:**

- Your name and role
- Universal coding preferences (language for comments, commit style)
- Personal habits that apply everywhere

**Example:**

```markdown
# About Me

I'm Alex, a full-stack engineer working primarily with TypeScript and Python.

## Universal Preferences

- Write commit messages in conventional commit format
- Prefer functional programming patterns over OOP
- Keep functions under 40 lines — split if longer
- Use descriptive variable names, never single letters
- When unsure between two approaches, pick the simpler one
```

### Layer 2: Project Config — `./CLAUDE.md`

This file sits in your project root. It gets **committed to Git** so every team member shares the same AI context.

**What to put here:**

- Project-specific tech stack
- Team coding standards
- Directory structure
- Build and test commands
- Architecture decisions

**Example:**

````markdown
# SaaS Dashboard

## Stack
- Next.js 15 (App Router) + TypeScript 5.7
- Tailwind CSS + shadcn/ui
- Zustand for state management
- Prisma + PostgreSQL

## Project Structure
```
src/
├── app/          # Next.js App Router pages
├── components/   # Reusable components
│   ├── ui/       # Base UI components (shadcn)
│   └── features/ # Business logic components
├── lib/          # Utilities and config
├── hooks/        # Custom React hooks
├── stores/       # Zustand stores
├── types/        # TypeScript type definitions
└── services/     # API client layer
```

## Commands
- Dev: pnpm dev
- Build: pnpm build
- Test: pnpm vitest
- Lint: pnpm lint

## Coding Standards
- File names: kebab-case (e.g., user-profile.tsx)
- Component names: PascalCase (e.g., UserProfile)
- Functions/variables: camelCase (e.g., getUserById)
- Constants: UPPER_SNAKE_CASE (e.g., MAX_RETRY_COUNT)
- All components must be functional with hooks
- Props must have TypeScript interfaces

## Git Rules
- Commit format: type: description
- Types: feat / fix / refactor / docs / test / chore
- Always run pnpm lint before committing
````

### Layer 3: Personal Config — `./CLAUDE.local.md`

This file also lives in the project root, but it's **not committed to Git** (add it to `.gitignore`). It's for your personal overrides on a specific project.

**What to put here:**

- Personal preferences that differ from team standards
- Local environment quirks
- Temporary debugging notes
- Experimental instructions you're testing

**Example:**

```markdown
# Personal Overrides

- I'm working on the payment module this sprint — prioritize that context
- My local PostgreSQL runs on port 5433 (not the default 5432)
- When writing tests, add verbose comments — I'm learning the testing patterns
- Draft comments in English first, I'll review before committing
```

### Priority Order

When multiple CLAUDE.md files exist, Claude Code loads them in this order:

```
Global (~/.claude/CLAUDE.md)
  → Project (./CLAUDE.md)
    → Personal (./CLAUDE.local.md)
```

**Later files override earlier ones.** If your global config says "use English comments" but the project config says "use Spanish comments," Spanish wins.

Here's a quick reference table:

| Layer | File Path | Git Committed? | Scope |
|-------|-----------|----------------|-------|
| Global | `~/.claude/CLAUDE.md` | N/A | All projects |
| Project | `./CLAUDE.md` | Yes | Current project (team-wide) |
| Personal | `./CLAUDE.local.md` | No | Current project (you only) |

> **Note:** Claude Code also supports organization-level policies at `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) and `.claude/rules/*.md` for rule-based configs. These are for enterprise setups and beyond the scope of this guide.

## Four Ways to Manage CLAUDE.md

You don't have to write CLAUDE.md manually from scratch every time. Claude Code provides four methods, each useful in different situations.

### Method 1: `/init` — Auto-Generate from Your Project

The fastest way to get started. Run Claude Code in your project directory and type:

```
/init
```

Claude analyzes your `package.json`, `tsconfig.json`, `.eslintrc`, directory structure, and other config files, then generates a CLAUDE.md draft automatically.

**Pros:** Fast, captures your actual stack accurately.

**Cons:** The output is generic. You'll need to add team-specific rules and workflow instructions manually.

**When to use:** Starting a new project or adding CLAUDE.md to an existing project for the first time.

### Method 2: `#` Syntax — Add Rules on the Fly

During any conversation, type a line starting with `#` to append a rule to CLAUDE.md:

```
# Always handle loading and error states in API calls
```

Claude adds this rule to your project's CLAUDE.md immediately.

**Pros:** Zero friction — add rules the moment you think of them.

**Cons:** Rules accumulate without organization. Clean up periodically.

**When to use:** You notice Claude keeps making the same mistake. Fix it once, remember it forever.

### Method 3: `/memory` — Visual Editor

Type `/memory` to open an interactive interface for viewing and editing your CLAUDE.md content. You can choose which layer to edit (global, project, or personal).

**Pros:** See everything at once. Easy to reorganize and clean up.

**Cons:** Requires stepping out of your coding flow.

**When to use:** Periodic maintenance — reorganizing, removing stale rules, restructuring sections.

### Method 4: `@` Imports — Modular Configuration

When your CLAUDE.md grows beyond a comfortable size, split it into multiple files and reference them with `@`:

```markdown
# Project Config

@docs/architecture.md
@docs/api-conventions.md
@docs/testing-guide.md
@AGENTS.md
```

Claude Code reads the referenced files and includes their content as context.

**Pros:** Keeps CLAUDE.md short and organized. Each referenced file can be maintained independently.

**Cons:** More files to manage. Referenced files must exist at the specified paths.

**When to use:** Large projects, monorepos, or when CLAUDE.md exceeds 200 lines.

## Copy-Paste Templates

Here are three ready-to-use templates. Copy the one that fits your situation, customize the specifics, and you're done.

### Template 1: Solo Developer (Global Config)

Place this at `~/.claude/CLAUDE.md`:

```markdown
# Developer Profile

I'm [Your Name], a [your role] working with [primary languages].

## Coding Preferences

- Prefer functional programming over OOP
- Variable names must be descriptive — no a, b, temp
- Keep functions under 40 lines
- Code should be self-documenting; minimize comments
- When adding comments, make them explain "why", not "what"

## Workflow

- Run lint before every commit
- Commit frequently in small increments
- No TypeScript errors allowed before committing
- Write tests for any non-trivial business logic

## Things I Dislike

- Over-engineering and unnecessary abstractions
- Design patterns used for the sake of patterns
- Deeply nested callbacks or promises (use async/await)
- Magic numbers — extract to named constants
```

### Template 2: Team Project (Project Config)

Place this at `./CLAUDE.md` in your project root:

`````markdown
# [Project Name]

[One-line description of what this project does]

## Stack

- Framework: Next.js 15 (App Router)
- Language: TypeScript 5.7 (strict mode)
- Styling: Tailwind CSS + shadcn/ui
- State: Zustand
- Database: PostgreSQL + Prisma
- Testing: Vitest + Testing Library
- Package manager: pnpm

## Directory Structure

```
src/
├── app/          # Pages and layouts (App Router)
├── components/   # Reusable UI components
├── lib/          # Utilities, helpers, config
├── hooks/        # Custom React hooks
├── stores/       # Zustand state stores
├── types/        # Shared TypeScript types
└── services/     # API client functions
```

## Commands

```bash
pnpm dev          # Start dev server
pnpm build        # Production build
pnpm test         # Run tests
pnpm lint         # Lint check
pnpm db:push      # Push schema to database
pnpm db:migrate   # Run database migrations
```

## Coding Rules

- Use functional components with hooks. No class components.
- Props must have TypeScript interfaces, named [Component]Props.
- File names: kebab-case. Component names: PascalCase.
- All API calls must handle loading and error states.
- No `any` type. Use `unknown` if the type is truly unknowable.
- Sensitive values in .env.local only. Never commit secrets.

## Git Conventions

- Commit format: `type: short description`
- Types: feat | fix | refactor | docs | test | chore
- Branch naming: feature/description or fix/description
- Always run `pnpm lint` before committing
- New features require unit tests

## Important Notes

- This is a multi-tenant SaaS app. All database queries MUST filter by tenantId.
- Never import from `node_modules` directly — use the re-exports in `lib/`.
- Rate limiting is handled by middleware. Do not add rate limiting in individual routes.
`````

### Template 3: Python Backend (Project Config)

Place this at `./CLAUDE.md` in your Python project root:

`````markdown
# [Project Name]

[One-line description]

## Stack

- Python 3.12 + FastAPI
- SQLAlchemy 2.0 + Alembic for migrations
- PostgreSQL 16
- Redis for caching and task queue
- Celery for background tasks
- Poetry for dependency management

## Project Structure

```
src/
├── api/           # FastAPI route handlers
│   └── v1/        # Versioned endpoints
├── core/          # App config, security, dependencies
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic request/response schemas
├── services/      # Business logic layer
├── tasks/         # Celery background tasks
└── utils/         # Helper functions
tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── conftest.py    # Shared fixtures
```

## Commands

```bash
poetry install              # Install dependencies
poetry run uvicorn src.main:app --reload  # Dev server
poetry run pytest           # Run all tests
poetry run pytest -x -v     # Run tests, stop on first failure
poetry run alembic upgrade head  # Apply migrations
poetry run black .          # Format code
poetry run ruff check .     # Lint
```

## Coding Rules

- Follow PEP 8. Use Black for formatting (line length 88).
- All functions must have type hints.
- Docstrings use Google style.
- Use Pydantic for all request/response validation.
- Service layer handles business logic. Routes are thin — validate, call service, return response.
- All database operations go through the repository pattern in services/.

## Testing Rules

- Every endpoint needs at least one happy-path and one error-path test.
- Use pytest fixtures for database setup/teardown.
- Mock external API calls. Never make real HTTP requests in tests.
`````

## CLAUDE.md vs README.md

These two files look similar but serve fundamentally different audiences. Mixing them up is one of the most common mistakes developers make.

| Dimension | README.md | CLAUDE.md |
|-----------|-----------|-----------|
| **Audience** | Human developers | AI agent (Claude Code) |
| **Purpose** | Explain what the project is | Instruct how to work on it |
| **Tone** | Descriptive, explanatory | Imperative, direct |
| **Content** | What, why, how to get started | Must do, must not do, how to do |
| **Format** | Tables, diagrams, badges, links | Compact lists, code blocks, rules |
| **Optimization** | Scannable by humans | Token-efficient for LLMs |

### The Same Topic, Two Different Treatments

Take "tech stack" as an example.

**README.md** — formatted for quick human scanning:

```markdown
| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React + TypeScript | 19.x / 5.7 |
| Backend | FastAPI + SQLAlchemy | 0.115 / 2.0 |
| Database | PostgreSQL | 16 |
| Cache | Redis | 7.x |
```

**CLAUDE.md** — compressed for token efficiency:

```markdown
- Frontend: React 19 + TypeScript 5.7 + Vite 6
- Backend: FastAPI 0.115 + SQLAlchemy 2.0 + PostgreSQL 16 + Redis 7
```

Same information, different packaging.

### Content Boundaries

| Content | README.md | CLAUDE.md |
|---------|:---------:|:---------:|
| What is this project? | Yes | No |
| Tech stack / versions | Yes (table) | Yes (compact list) |
| How to get started | Yes (step by step) | No |
| Build/test commands | Yes (detailed) | Yes (one code block) |
| Environment requirements | Yes | No |
| Git commit conventions | No | Yes |
| Coding standards | No | Yes |
| Testing rules | No | Yes |
| Development workflow | No | Yes |
| Architecture overview | Yes | Brief pointer |
| License | Yes | No |

**Rule of thumb:** README answers "What is this?" CLAUDE.md answers "How should I work on this?"

## CLAUDE.md vs AGENTS.md

There's an industry-wide movement to standardize how AI agents receive project context, and it's called AGENTS.md.

### What Is AGENTS.md?

AGENTS.md is a cross-tool standard for giving AI coding agents project instructions. Originally proposed in mid-2025, it's now managed by the Agentic AI Foundation under the Linux Foundation.

As of early 2026, AGENTS.md is supported by:

- **OpenAI Codex CLI**
- **Google Gemini CLI**
- **GitHub Copilot**
- **Cursor**
- **Windsurf**
- **Devin**
- **Claude Code** (via `@` import)
- And 20+ more tools

Over 60,000 open-source repositories have adopted AGENTS.md.

### CLAUDE.md vs AGENTS.md: When to Use Which

| Scenario | Recommendation |
|----------|---------------|
| Only your team uses Claude Code | CLAUDE.md is sufficient |
| Team uses multiple AI tools | Write AGENTS.md as the source of truth |
| Open-source project | AGENTS.md (broadest compatibility) |
| Need Claude-specific instructions | CLAUDE.md for Claude-specific rules + AGENTS.md for universal rules |

### How to Use Both Together

The most common pattern is to write your main instructions in AGENTS.md and have CLAUDE.md reference it:

```markdown
See @AGENTS.md
```

That's it. One line in CLAUDE.md, all your instructions in AGENTS.md. This way, Cursor reads AGENTS.md directly, Copilot reads AGENTS.md directly, and Claude Code reads it via the `@` import.

Alternatively, you can create a symlink:

```bash
# Write everything in AGENTS.md, symlink for Claude Code
ln -s AGENTS.md CLAUDE.md
```

If you need Claude-specific rules that don't apply to other tools (like Skill references or Claude-specific workflow instructions), keep those in CLAUDE.md and put the universal rules in AGENTS.md:

```markdown
# Claude-Specific Config

See @AGENTS.md

## Claude-Only Rules
- Use /compact when context gets long
- Prefer Sonnet for routine tasks, switch to Opus for architecture decisions
- When writing Skills, follow the pattern in .claude/skills/
```

## Writing Principles: How to Write Effective CLAUDE.md

A badly written CLAUDE.md can be worse than none at all. Here are the principles that separate effective configs from noise.

### 1. Keep It Under 300 Lines

Research shows that LLMs reliably follow roughly 150–200 discrete instructions. Claude Code's system prompt already uses about 50 of those slots. That leaves you 150 instructions at most — and most projects need far fewer.

If your CLAUDE.md exceeds 300 lines, break it up with `@` imports. Keep the main file as a concise index.

### 2. Use Imperative Sentences

Write commands, not descriptions.

| Bad (descriptive) | Good (imperative) |
|---|---|
| "The project uses TypeScript strict mode" | "Use TypeScript strict mode" |
| "We prefer functional components" | "Use functional components. No class components." |
| "It would be nice to have tests" | "Write tests for all new endpoints" |
| "The team generally follows..." | "Follow conventional commit format" |

Claude is an agent taking instructions, not a colleague reading documentation. Be direct.

### 3. Don't Duplicate What Linters Already Enforce

If your `.eslintrc` enforces 2-space indentation, don't repeat it in CLAUDE.md. Claude Code reads your project's linter configs automatically.

**Don't put in CLAUDE.md:**
- Indentation rules (handled by Prettier/ESLint)
- Import ordering (handled by eslint-plugin-import)
- Trailing commas (handled by Prettier)
- Line length (handled by Black/Prettier)

**Do put in CLAUDE.md:**
- Architectural patterns ("Use repository pattern for database access")
- Business logic rules ("All queries must filter by tenantId")
- Workflow instructions ("Run tests before committing")
- Naming conventions that linters can't enforce

### 4. Use @ Imports for Large Configs

Keep CLAUDE.md as a concise table of contents. Move detailed docs elsewhere:

```markdown
# Project Config

## Architecture
@docs/architecture.md

## API Conventions
@docs/api-conventions.md

## Testing Guide
@docs/testing-guide.md
```

Each imported file should focus on one topic and be independently maintainable.

### 5. Test Your Rules

After writing CLAUDE.md, ask Claude a question that should trigger one of your rules. If it doesn't follow the rule, the instruction might be too vague or buried too deep.

For example, if your CLAUDE.md says "All API endpoints must validate input with Zod," ask Claude to create a new endpoint. Does it include Zod validation? If not, rewrite the rule to be more prominent or specific.

### 6. Emphasize Critical Rules

For rules that absolutely must not be violated, add emphasis:

```markdown
- IMPORTANT: All database queries MUST filter by tenantId. No exceptions.
- NEVER commit .env files or API keys to Git.
- YOU MUST run the test suite before creating any pull request.
```

Words like `IMPORTANT`, `MUST`, `NEVER`, and `ALWAYS` increase compliance rates for critical instructions.

## Advanced Tips

### Modular Configs for Monorepos

In a monorepo, different directories may have different conventions. Use subdirectory CLAUDE.md files:

```
my-monorepo/
├── CLAUDE.md              # Shared rules (Git conventions, CI)
├── frontend/
│   ├── CLAUDE.md          # React/TypeScript rules
│   └── src/
├── backend/
│   ├── CLAUDE.md          # Python/FastAPI rules
│   └── src/
└── infra/
    ├── CLAUDE.md          # Terraform/AWS rules
    └── modules/
```

Claude Code loads the root CLAUDE.md plus the relevant subdirectory CLAUDE.md based on which files it's working with.

### CLAUDE.md + Skills Combo

CLAUDE.md defines the environment. [Skills](/posts/ai/2026-02-28-claude-code-skills-guide/) define task-specific workflows. They complement each other.

**CLAUDE.md** sets the standards:

```markdown
## Code Review Standards
- All new code must have unit tests
- No console.log in production code
- No hardcoded configuration values
- Functions must have JSDoc comments
```

**A Skill** defines the review process:

```markdown
---
name: code-review
description: Review code changes against project standards
---

# Code Review Skill

1. Read git diff for staged changes
2. Check each file against the Code Review Standards in CLAUDE.md
3. List violations with file, line, and suggested fix
4. Summarize: total issues found, severity breakdown
```

The Skill automatically references CLAUDE.md rules — no duplication needed. For more on combining these tools, see our [Skills guide](/posts/ai/2026-02-28-claude-code-skills-guide/).

### CLAUDE.md + Hooks Integration

[Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) let you automate actions before or after Claude Code operations. Your CLAUDE.md can reference hook behaviors:

```markdown
## Automated Checks
- Pre-commit hooks run ESLint and Prettier automatically
- Post-save hooks run the test suite for changed files
- See .claude/settings.json for hook configuration
```

This tells Claude what's already automated so it doesn't duplicate those checks manually.

### Team Best Practices

1. **Commit CLAUDE.md to Git.** It's team infrastructure, like `.eslintrc` or `tsconfig.json`. Everyone should share the same AI context.

2. **Add CLAUDE.local.md to .gitignore.** Personal preferences shouldn't be forced on teammates.

3. **Review CLAUDE.md in PRs.** When someone adds a rule, the team should agree on it — just like a linter rule change.

4. **Update regularly.** When the project evolves, update CLAUDE.md. When Claude keeps making the same mistake, add a rule. When a rule becomes irrelevant, remove it.

5. **Onboard new team members.** Your CLAUDE.md is useful for humans too. New developers can read it to quickly understand coding standards and workflows — even if they don't use Claude Code.

## Common Mistakes to Avoid

### Mistake 1: Writing a Novel

A 500-line CLAUDE.md with project history, design philosophy, and meeting notes. Claude doesn't need your backstory. It needs instructions.

**Fix:** Cut ruthlessly. For each line, ask: "If I remove this, will Claude make worse code?" If the answer is no, delete it.

### Mistake 2: Being Too Vague

Rules like "write clean code" or "follow best practices" are meaningless. Claude already tries to write clean code. Vague instructions waste context tokens without changing behavior.

**Fix:** Make rules specific and testable. Instead of "write clean code," write "Keep functions under 30 lines. Extract helper functions for repeated logic."

### Mistake 3: Mixing README Content Into CLAUDE.md

Paragraphs explaining what the project does, why it was built, or who it's for. Claude doesn't need persuading — it needs directing.

**Fix:** Project descriptions go in README.md. CLAUDE.md gets only actionable instructions.

### Mistake 4: Duplicating Linter Rules

Listing every ESLint or Prettier rule in CLAUDE.md. Claude Code already reads your linter config files.

**Fix:** Only include rules that linters can't enforce: architectural patterns, business logic constraints, and workflow instructions.

### Mistake 5: Never Updating

Writing CLAUDE.md once and forgetting about it. Six months later, the tech stack has changed, conventions have evolved, and half the instructions are obsolete.

**Fix:** Add "review CLAUDE.md" to your sprint retrospective checklist. Remove stale rules. Add rules for new patterns.

### Mistake 6: Forgetting CLAUDE.local.md

Putting personal preferences in the shared CLAUDE.md, causing conflicts when teammates have different preferences.

**Fix:** Shared standards in CLAUDE.md. Personal preferences in CLAUDE.local.md. Add `CLAUDE.local.md` to `.gitignore`.

## Quick-Start Checklist

Not sure where to begin? Follow these steps:

1. **Run `/init` in your project** — Get an auto-generated starting point
2. **Review and trim** — Remove anything Claude can figure out on its own
3. **Add team rules** — Coding standards, Git conventions, architecture constraints
4. **Add the commands** — Build, test, lint, deploy
5. **Add critical rules** — Business logic invariants that MUST be followed
6. **Test it** — Ask Claude to do a task and verify it follows your rules
7. **Commit it** — `git add CLAUDE.md && git commit -m "feat: add CLAUDE.md"`
8. **Create `.gitignore` entry** — Add `CLAUDE.local.md` for personal overrides
9. **Set up global config** — Add your universal preferences to `~/.claude/CLAUDE.md`
10. **Maintain it** — Review monthly, update when the project evolves

## Related Articles

If you're building a complete Claude Code workflow, these guides cover the other pieces:

- **[Claude Code Setup Guide 2026](/posts/ai/2026-02-25-claude-code-setup-guide/)** — Installation, authentication, and first project setup
- **[Claude Code Pricing 2026](/posts/ai/2026-02-25-claude-code-pricing/)** — Understand costs, choose the right plan, optimize token usage
- **[10 Claude Code Mistakes](/posts/ai/2026-02-25-claude-code-mistakes/)** — Common pitfalls and how to avoid them (Mistake #1 is skipping CLAUDE.md)
- **[Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/)** — Automate actions before and after Claude Code operations
- **[Claude Code Skills Guide](/posts/ai/2026-02-28-claude-code-skills-guide/)** — Build reusable task workflows that complement CLAUDE.md

---

CLAUDE.md is one of those features that takes 10 minutes to set up and pays dividends for months. The difference between a Claude Code user with a good CLAUDE.md and one without is stark: fewer corrections, more consistent code, less token waste, and a smoother workflow overall.

Write it once. Keep it updated. Let Claude handle the rest.
