+++
date = '2026-03-05T10:00:00+08:00'
draft = false
title = 'CLAUDE.md Best Practices: Write Files That Actually Work'
description = 'How to write effective CLAUDE.md files for Claude Code. Practical patterns, examples for 7 project types, and CLAUDE.md vs .cursorrules vs AGENTS.md compared.'
toc = true
tags = ['Claude Code', 'CLAUDE.md', 'Best Practices', 'AI Development', 'AGENTS.md']
categories = ['AI Guides']
keywords = ['CLAUDE.md guide', 'claude code claude.md', 'how to write CLAUDE.md', 'CLAUDE.md best practices', 'CLAUDE.md examples', 'CLAUDE.md vs cursorrules', 'CLAUDE.md vs AGENTS.md', 'claude code configuration']

[[params.faqItems]]
question = "What is CLAUDE.md and how does it work?"
answer = "CLAUDE.md is a Markdown file that Claude Code automatically loads into context at the start of every session. It acts as persistent memory — you write project rules, coding standards, and workflow instructions once, and Claude follows them in every conversation without reminders."

[[params.faqItems]]
question = "Where should I put my CLAUDE.md file?"
answer = "Claude Code supports multiple locations: ~/.claude/CLAUDE.md for global preferences across all projects, ./CLAUDE.md in the project root for team-shared rules (committed to Git), ./CLAUDE.local.md for personal overrides (not committed), and .claude/rules/*.md for modular rule files. Later files override earlier ones."

[[params.faqItems]]
question = "How long should CLAUDE.md be?"
answer = "Keep the main CLAUDE.md under 200 lines. LLMs reliably follow roughly 150-200 discrete instructions, and Claude Code's system prompt uses about 50 of those slots. If you need more, use @ imports to reference separate files for architecture docs, testing guides, or API conventions."

[[params.faqItems]]
question = "What is the difference between CLAUDE.md, AGENTS.md, and .cursorrules?"
answer = "CLAUDE.md is Claude Code-specific and auto-loaded by Claude Code. AGENTS.md is a cross-tool standard supported by 30+ AI coding tools including Codex CLI, Gemini CLI, Cursor, and Claude Code. .cursorrules is Cursor-specific. For multi-tool teams, write AGENTS.md as the source of truth and have CLAUDE.md reference it with 'See @AGENTS.md'."

[[params.faqItems]]
question = "Can I use CLAUDE.md and AGENTS.md together?"
answer = "Yes, and it's the recommended approach for teams using multiple AI tools. Put universal rules in AGENTS.md, then create a CLAUDE.md with one line: 'See @AGENTS.md'. Add any Claude-specific instructions (like Skill references or model preferences) below that line in CLAUDE.md."
+++

![CLAUDE.md best practices guide for writing effective Claude Code configuration files](cover.webp)

Most CLAUDE.md files are bad. They're either empty, stuffed with 500 lines of auto-generated boilerplate, or full of vague instructions like "write clean code" that Claude already tries to do by default.

A well-written CLAUDE.md transforms Claude Code from a generic assistant into a team member who knows your stack, follows your conventions, and avoids your project's specific pitfalls. A bad one wastes context tokens and gives you a false sense of control.

This guide focuses on the **how** — practical patterns for writing CLAUDE.md files that actually change Claude's behavior. You'll get real examples for different project types, the specific mistakes that make CLAUDE.md files useless, and a clear comparison of CLAUDE.md vs AGENTS.md vs .cursorrules. If you need the basics first (what CLAUDE.md is, how it loads, the three-layer system), read our [CLAUDE.md introduction](/posts/ai/2026-02-28-claude-code-claudemd-guide/) before continuing.

## How CLAUDE.md Gets Loaded

Before writing effective rules, you need to understand the loading mechanism. [Claude Code](https://docs.anthropic.com/en/docs/claude-code/memory) auto-loads CLAUDE.md files from multiple locations in a specific priority order:

| Priority | Location | Scope | Git Tracked? |
|----------|----------|-------|:------------:|
| 1 (lowest) | `~/.claude/CLAUDE.md` | All projects (global) | N/A |
| 2 | `./CLAUDE.md` | Current project (team) | Yes |
| 3 | `./.claude/rules/*.md` | Current project (modular) | Yes |
| 4 (highest) | `./CLAUDE.local.md` | Current project (personal) | No |

Key behaviors:

- **Auto-loaded**: You never need to tell Claude to read CLAUDE.md. It happens automatically at session start.
- **Recursive scanning**: Claude Code walks up from the current directory, loading every CLAUDE.md it finds. In a monorepo, `frontend/CLAUDE.md` loads when Claude works on frontend files.
- **Override order**: Later (higher priority) files override earlier ones. Your personal `CLAUDE.local.md` overrides the team's `CLAUDE.md`.
- **@ imports**: Any CLAUDE.md can reference other files with `@path/to/file.md`, and Claude loads those too.

This means you can layer your configuration: global preferences that apply everywhere, project rules shared with the team, and personal overrides that stay local.

## The 6 Principles of Effective CLAUDE.md

### Principle 1: Write Commands, Not Descriptions

CLAUDE.md is an instruction set, not documentation. Every line should tell Claude what to **do**.

**Bad — descriptive:**

```markdown
## About This Project
This project is an e-commerce platform built with Next.js 15 and TypeScript.
We generally prefer functional programming patterns and try to keep our
code clean and maintainable. The team values readability and...
```

**Good — imperative:**

```markdown
## Stack
- Next.js 15 (App Router) + TypeScript 5.7 (strict mode)
- Tailwind CSS + shadcn/ui + Zustand
- PostgreSQL + Prisma

## Rules
- Use functional components only. No class components.
- All functions must have TypeScript type annotations.
- Keep functions under 30 lines. Extract helpers for repeated logic.
```

The first version reads like a README introduction. Claude doesn't need to be sold on your project — it needs instructions. The second version is 40% fewer tokens and 100% more actionable.

### Principle 2: Only Include Rules That Change Behavior

Every rule in CLAUDE.md should pass this test: **"If I remove this rule, will Claude's output be worse?"**

Rules that fail this test:

- "Write clean, maintainable code" — Claude already tries to do this
- "Follow best practices" — too vague to change behavior
- "Use meaningful variable names" — Claude does this by default
- "Handle errors properly" — not specific enough

Rules that pass this test:

- "All database queries MUST filter by `tenantId`" — project-specific invariant
- "Use Zustand for state management, not Redux or Context API" — explicit choice
- "Test files go in `__tests__/` next to the source file, not in a separate `tests/` directory" — structural decision
- "Never use `console.log`. Use the `logger` utility from `src/lib/logger`" — specific override

If Claude would already do something without the rule, the rule is wasting context tokens.

### Principle 3: Keep It Under 200 Lines

Research on LLM instruction following shows diminishing returns after roughly 150-200 discrete instructions. Claude Code's system prompt uses about 50 of those slots, leaving you around 150 effective instructions.

A 500-line CLAUDE.md doesn't give you 3x more control — it gives you **less** control because important rules get buried in noise.

**When your CLAUDE.md outgrows 200 lines:**

```markdown
# Project Config

## Architecture
@docs/architecture.md

## API Conventions
@docs/api-conventions.md

## Testing Standards
@docs/testing-guide.md

## Deployment
@docs/deploy-runbook.md
```

Keep the main CLAUDE.md as a concise index. Move detailed documentation into separate files referenced with `@` imports.

### Principle 4: Emphasize Critical Rules

Not all rules are equal. Some are preferences ("prefer `const` over `let`"). Others are invariants that must never be violated ("all queries must filter by tenant ID").

For critical rules, use strong language:

```markdown
## Critical Rules

- IMPORTANT: All database queries MUST filter by `tenantId`. No exceptions.
  Multi-tenant data leakage is a security incident.
- NEVER commit `.env` files or API keys to Git.
- NEVER delete or modify database migration files. Create new migrations instead.
- YOU MUST run `pnpm test` before creating any commit.
```

Words like `IMPORTANT`, `MUST`, `NEVER`, and `ALWAYS` measurably increase compliance for critical instructions. Use them sparingly — if everything is "IMPORTANT," nothing is.

### Principle 5: Don't Duplicate Linter Rules

Claude Code reads your project's config files — `eslintrc`, `prettier.config`, `tsconfig.json`, `.editorconfig`, `pyproject.toml`. If a rule is already enforced by a tool, repeating it in CLAUDE.md wastes tokens.

**Don't put in CLAUDE.md** (already handled by tooling):

- Indentation style (Prettier/EditorConfig)
- Import ordering (eslint-plugin-import)
- Line length limits (Black/Prettier)
- Trailing commas (Prettier)
- Type checking strictness (tsconfig.json)

**Do put in CLAUDE.md** (can't be enforced by linters):

- Architectural patterns ("Service layer handles business logic. Routes are thin.")
- Business logic constraints ("All prices stored in cents, not dollars.")
- Naming conventions beyond syntax ("Feature flags use `isEnabled` prefix.")
- Workflow instructions ("Run tests before committing.")
- Technology choices ("Use Zustand, not Redux.")

### Principle 6: Test and Iterate

After writing your CLAUDE.md, test it:

1. Start a new Claude Code session
2. Ask Claude to do a task that should trigger one of your rules
3. Check whether it follows the rule
4. If not, the rule is either too vague, buried too deep, or contradicted by another instruction

For example, if your CLAUDE.md says "Use Zod for all API input validation," ask Claude to create a new API endpoint. Does it include Zod schemas? If not, rewrite the rule to be more prominent or add emphasis with `MUST`.

Treat CLAUDE.md like code — it needs testing, iteration, and maintenance.

## Real-World Examples by Project Type

### Example 1: React/Next.js Frontend

````markdown
# SaaS Dashboard

## Stack
- Next.js 15 (App Router) + TypeScript 5.7 (strict)
- Tailwind CSS + shadcn/ui
- Zustand for client state
- TanStack Query for server state
- Vitest + Testing Library

## Commands
```bash
pnpm dev           # Dev server at localhost:3000
pnpm build         # Production build
pnpm test          # Run tests
pnpm lint          # ESLint check
pnpm db:push       # Push Prisma schema
```

## Rules
- Use functional components only. No class components.
- Props interfaces named `[Component]Props` (e.g., `UserCardProps`).
- File names: kebab-case. Component names: PascalCase.
- Use `useQuery`/`useMutation` from TanStack Query for all API calls.
- No `any` type. Use `unknown` if truly unknowable.
- All user-facing text must use the i18n system (`t()` function).

## Critical
- NEVER import from `node_modules` directly. Use re-exports in `src/lib/`.
- All database queries MUST filter by `organizationId` (multi-tenant).
- NEVER commit `.env.local` or expose API keys in client-side code.
````

### Example 2: Python FastAPI Backend

````markdown
# Payment Service API

## Stack
- Python 3.12 + FastAPI 0.115
- SQLAlchemy 2.0 + Alembic
- PostgreSQL 16 + Redis 7
- Poetry for dependencies
- pytest for testing

## Commands
```bash
poetry run uvicorn src.main:app --reload    # Dev server
poetry run pytest -x -v                     # Tests (stop on first failure)
poetry run alembic upgrade head             # Apply migrations
poetry run ruff check . && ruff format .    # Lint + format
```

## Architecture
- Routes are thin. Validate input → call service → return response.
- Business logic lives in `src/services/`.
- Database operations go through repository classes in `src/repositories/`.
- Background tasks use Celery. Define in `src/tasks/`.

## Rules
- All functions must have type hints. No exceptions.
- Use Pydantic models for all request/response validation.
- Docstrings use Google style.
- NEVER make raw SQL queries. Use SQLAlchemy ORM.
- All money amounts stored as integers (cents). Convert at API boundary.
- New endpoints MUST have at least one happy-path and one error-path test.
````

### Example 3: Monorepo

````markdown
# Acme Platform Monorepo

## Structure
```
apps/
├── web/           # Next.js customer portal (see apps/web/CLAUDE.md)
├── admin/         # Next.js admin dashboard (see apps/admin/CLAUDE.md)
└── api/           # FastAPI backend (see apps/api/CLAUDE.md)
packages/
├── ui/            # Shared component library
├── config/        # Shared configs (ESLint, TypeScript, Tailwind)
└── types/         # Shared TypeScript types
```

## Global Rules (apply to all apps)
- Package manager: pnpm. NEVER use npm or yarn.
- Commit format: `type(scope): description` (e.g., `feat(web): add login page`)
- Scopes: web, admin, api, ui, config, types, infra
- All PRs require passing CI before merge.
- Shared types go in `packages/types/`. NEVER duplicate type definitions.

## Commands
```bash
pnpm install              # Install all dependencies
pnpm --filter web dev     # Run web app
pnpm --filter api dev     # Run API
pnpm -r test              # Run all tests
pnpm -r build             # Build all packages
```

## Cross-App Rules
- Frontend apps fetch data from API only. No direct database access.
- Shared components in `packages/ui/` must be framework-agnostic.
- API changes must be backward-compatible. Version breaking changes.
````

### Example 4: Mobile App (React Native)

````markdown
# HealthTrack Mobile App

## Stack
- React Native 0.76 + Expo SDK 52
- TypeScript 5.7 (strict)
- Zustand + MMKV for local storage
- React Navigation v7

## Commands
```bash
npx expo start        # Dev server
npx expo run:ios      # Run on iOS simulator
npx expo run:android  # Run on Android emulator
pnpm test             # Jest tests
```

## Rules
- Use Expo APIs when available. Don't install bare RN modules for things Expo covers.
- Screens go in `src/screens/`, components in `src/components/`.
- Navigation types MUST be defined in `src/navigation/types.ts`.
- Use `StyleSheet.create()` for styles. No inline style objects.
- All network requests go through `src/api/client.ts`. No direct fetch calls.
- IMPORTANT: Test on both iOS and Android. Platform-specific code uses `.ios.tsx` / `.android.tsx` suffixes.
- NEVER store sensitive data (tokens, passwords) in AsyncStorage. Use expo-secure-store.
````

### Example 5: Go Microservice

````markdown
# Notification Service

## Stack
- Go 1.23
- Chi router + sqlc for database queries
- PostgreSQL 16 + Redis 7
- Docker for local development

## Commands
```bash
go run ./cmd/server              # Run server
go test ./...                    # Run all tests
make migrate-up                  # Apply migrations
make generate                    # Regenerate sqlc + protobuf
docker compose up -d             # Start local deps
```

## Rules
- Follow standard Go project layout. Entrypoints in `cmd/`, packages in `internal/`.
- Error handling: wrap errors with `fmt.Errorf("context: %w", err)`. Never discard errors.
- Interfaces defined by the consumer, not the implementer.
- Database queries in `internal/db/` generated by sqlc. Edit `.sql` files, then run `make generate`.
- NEVER modify generated code directly. Modify the source (SQL, proto) and regenerate.
- Logging: use structured logging via `slog`. No `fmt.Println` or `log.Println`.
- Context must be the first parameter of any function that does I/O.
````

### Example 6: Hugo Blog (Like This Site)

This is the actual pattern used for this blog:

````markdown
# AI Engineering Blog

## Stack
- Hugo v0.153.2+ (Extended)
- Theme: hermit-V2 (git submodule)

## Commands
```bash
hugo server -D         # Preview with drafts
hugo server            # Preview without drafts
hugo --minify          # Production build
```

## Content Rules
- All new articles MUST be in English.
- NEVER modify existing Chinese articles.
- Front matter uses TOML format (+++).
- Categories: only 'AI Guides' or 'Comparisons'. No custom categories.

## Article Structure
- Directory: content/posts/ai/YYYY-MM-DD-english-slug/index.md
- Cover image: MUST be named cover.webp (1200x630px, <200KB)
- Cover image MUST be referenced on the first line after front matter
- Tags: 3-5 English tags
- Description: 120-160 characters with primary keyword

## Git
- Working branch: code
- Commit messages: Chinese
- Push to code triggers auto-deployment
````

### Example 7: Global User Config

Place at `~/.claude/CLAUDE.md` — applies to every project:

```markdown
# Developer Profile

I'm a senior full-stack engineer. Primary languages: TypeScript, Python, Go.

## Preferences
- Respond in Chinese for all conversations
- Commit messages in Chinese
- Code comments in English
- Prefer functional patterns over OOP
- Keep functions under 30 lines
- Descriptive variable names — never single letters except loop counters

## Workflow
- Conventional commit format: type: description
- Run linter before every commit
- Small, focused commits over large batches
- When unsure between two approaches, pick the simpler one
```

## CLAUDE.md vs .cursorrules vs AGENTS.md

If your team uses multiple AI coding tools, you need to understand how these three configuration files relate to each other.

### Quick Comparison

| Feature | CLAUDE.md | .cursorrules | AGENTS.md |
|---------|-----------|--------------|-----------|
| **Tool** | Claude Code only | Cursor only | 30+ tools (cross-platform) |
| **Auto-loaded** | Yes | Yes (in Cursor) | Yes (by supporting tools) |
| **File location** | Root, subdirs, `~/.claude/` | Root only | Root, subdirs |
| **Multi-layer** | Yes (global + project + personal) | No (single file) | Yes (directory hierarchy) |
| **@ imports** | Yes | No | Depends on tool |
| **Standard body** | [Anthropic](https://docs.anthropic.com/en/docs/claude-code/memory) | Cursor-specific | [Linux Foundation](https://github.com/anthropics/agents-md) |
| **Adoption** | Claude Code users | Cursor users | 60,000+ repos |

### When to Use What

**Solo developer using only Claude Code**: Use CLAUDE.md. It's all you need.

**Team using only Cursor**: Use `.cursorrules` (or Cursor's newer `.cursor/rules/` system).

**Team using multiple AI tools** (Claude Code + Cursor + Copilot + Codex CLI): Write your universal rules in AGENTS.md. Then:

- CLAUDE.md → one line: `See @AGENTS.md`
- .cursorrules → copy relevant rules (Cursor doesn't support `@` imports the same way)

**Open-source project**: Use AGENTS.md. It has the broadest tool compatibility. Over 60,000 repositories have adopted it, and it's backed by the [Agentic AI Foundation](https://github.com/anthropics/agents-md) under the Linux Foundation.

### The Recommended Multi-Tool Setup

Here's the pattern that works for teams using Claude Code alongside other tools:

**Step 1**: Write `AGENTS.md` with all universal rules:

```markdown
# Repository Guidelines

## Stack
- Next.js 15 + TypeScript 5.7
- Tailwind CSS + shadcn/ui
- PostgreSQL + Prisma

## Coding Standards
- Functional components only
- Props interfaces named [Component]Props
- All API calls must handle loading and error states

## Testing
- Vitest + Testing Library
- New features require tests
- Run pnpm test before committing
```

**Step 2**: Create a minimal `CLAUDE.md`:

```markdown
See @AGENTS.md

## Claude-Specific
- Use /compact when context gets long
- Prefer Sonnet for routine tasks, Opus for architecture decisions
- When writing Skills, follow patterns in .claude/skills/
```

**Step 3**: Optionally create `.cursorrules` with the same universal rules (since Cursor reads `.cursorrules` natively).

This way, every AI tool reads the same core instructions. Claude-specific features like [Skills](/posts/ai/2026-02-28-claude-code-skills-guide/) and [Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) stay in CLAUDE.md where they belong.

## 10 Common Mistakes (and How to Fix Them)

### 1. Writing a Novel

**Symptom**: A 500-line CLAUDE.md with project history, design philosophy, team bios, and meeting notes.

**Fix**: Cut ruthlessly. For each line, ask: "If I remove this, will Claude produce worse output?" If no, delete it. Claude needs instructions, not backstory.

### 2. Being Too Vague

**Symptom**: Rules like "write clean code" or "follow best practices."

**Fix**: Make rules specific and testable. Not "handle errors properly" but "All async functions must have try/catch blocks. Log errors with the logger utility. Return appropriate HTTP status codes."

### 3. Duplicating Linter Rules

**Symptom**: Listing every ESLint or Prettier rule. Specifying 2-space indentation when `.editorconfig` already says so.

**Fix**: Only include rules that automated tools can't enforce — architectural patterns, business logic constraints, workflow instructions.

### 4. Never Updating

**Symptom**: CLAUDE.md written 6 months ago. Tech stack has changed, conventions evolved, half the instructions are obsolete.

**Fix**: Review CLAUDE.md monthly. Add rules when Claude makes repeated mistakes. Remove rules when they become irrelevant. Treat it like living documentation.

### 5. Mixing README and CLAUDE.md Content

**Symptom**: Paragraphs explaining what the project does, why it was built, badges, screenshots.

**Fix**: README answers "What is this?" CLAUDE.md answers "How should I work on this?" Keep them separate. For a detailed breakdown, see our [CLAUDE.md vs README.md comparison](/posts/ai/2026-01-31-claudemd-vs-readme/).

### 6. Putting Personal Preferences in the Shared File

**Symptom**: Your CLAUDE.md says "respond in Chinese" but your teammate wants English. Merge conflicts on preferences.

**Fix**: Shared standards go in `./CLAUDE.md`. Personal preferences go in `./CLAUDE.local.md` (add to `.gitignore`). Universal personal preferences go in `~/.claude/CLAUDE.md`.

### 7. Ignoring Subdirectory CLAUDE.md Files

**Symptom**: A monorepo with one giant root CLAUDE.md trying to cover frontend React rules and backend Python rules simultaneously.

**Fix**: Split by directory. Root CLAUDE.md for shared rules (Git conventions, CI process). `frontend/CLAUDE.md` for React/TypeScript rules. `backend/CLAUDE.md` for Python/FastAPI rules. Claude loads the right one based on context.

### 8. Not Using @ Imports

**Symptom**: A 400-line CLAUDE.md that's hard to navigate and maintain.

**Fix**: Break it into focused files. Main CLAUDE.md becomes a table of contents with `@` imports pointing to detailed docs. Each imported file covers one topic.

### 9. Contradictory Rules

**Symptom**: Line 15 says "Use Redux for state management." Line 87 says "Prefer Zustand for client state." Claude gets confused and does neither consistently.

**Fix**: Audit for contradictions. Use a single source of truth for each decision. When migrating from one approach to another, be explicit: "Legacy code uses Redux. All new code MUST use Zustand."

### 10. Treating CLAUDE.md as Set-and-Forget

**Symptom**: You run `/init` once, accept the generated file, and never touch it again.

**Fix**: `/init` is a starting point, not the finish line. Review the output, add your team's specific rules, remove generic content, and add rules over time as you discover what Claude gets wrong in your project.

## Advanced Patterns

### The "Lessons Learned" Section

One of the highest-value sections you can add is a record of mistakes Claude has made in your project. This was [recommended by Claude Code's creator](https://x.com/amanrsanger/status/1917312117418262599):

```markdown
## Lessons Learned (Do Not Repeat These Mistakes)
- This project uses ESM modules. NEVER use require() or module.exports.
- The `user` table has a soft-delete column `deleted_at`. All queries must
  add `WHERE deleted_at IS NULL` unless explicitly querying deleted users.
- Tests must not use the production database. Use the test fixtures in conftest.py.
- The /api/v1/upload endpoint has a 10MB limit enforced by nginx, not the app.
  Do not add app-level size validation — it's already handled.
```

Every time Claude makes a mistake, add it here. Over time, this section becomes your project's institutional memory for AI — the equivalent of onboarding notes saying "by the way, watch out for this gotcha."

### Conditional Rules with Context

For projects that have different rules in different situations:

```markdown
## API Development
- When creating new endpoints: follow the pattern in src/api/v1/users.py as reference
- When modifying existing endpoints: maintain backward compatibility. Add new fields,
  don't rename or remove existing ones.
- When writing migrations: NEVER modify or delete existing migration files. Create new ones.

## Frontend Development
- When creating new pages: use the template in src/app/(dashboard)/template/page.tsx
- When adding forms: use react-hook-form + Zod. See src/components/forms/ for patterns.
- When adding new API calls: add the query/mutation in src/hooks/api/ using TanStack Query.
```

This pattern gives Claude context-specific instructions without bloating the file with rules that only apply some of the time.

### Rules Files for Modular Organization

Claude Code supports `.claude/rules/*.md` for organizing rules into separate files that all get auto-loaded:

```
.claude/
└── rules/
    ├── coding-standards.md
    ├── git-conventions.md
    ├── testing-requirements.md
    └── security-policies.md
```

Each file is loaded automatically. This is cleaner than `@` imports for projects that want modular organization without maintaining an index in CLAUDE.md.

### CLAUDE.md + Hooks: Automated Enforcement

Your CLAUDE.md can reference automated checks via [Claude Code Hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/):

```markdown
## Automated Checks (Do NOT duplicate these manually)
- Pre-commit: ESLint + Prettier run automatically via hooks
- Pre-push: Full test suite runs automatically
- See .claude/settings.json for hook configuration

## You MUST Still Do
- Write meaningful commit messages
- Add tests for new business logic
- Update API documentation when endpoints change
```

This prevents Claude from manually running checks that hooks already handle, avoiding double work.

## Quick-Start Checklist

Starting from scratch? Follow these steps:

1. **Run `/init`** in your project — Get an auto-generated starting point
2. **Cut the fluff** — Remove anything Claude would do anyway without the instruction
3. **Add your stack** — Framework, language, database, package manager (one line each)
4. **Add commands** — build, test, lint, deploy (one code block)
5. **Add team rules** — naming conventions, architectural patterns, Git workflow
6. **Add critical rules** — business invariants with MUST/NEVER emphasis
7. **Add lessons learned** — mistakes Claude has made that you don't want repeated
8. **Test it** — Start a new session, give Claude a task, verify rule compliance
9. **Commit to Git** — `git add CLAUDE.md`
10. **Add `.gitignore` entry** — `CLAUDE.local.md` for personal overrides
11. **Set up global config** — `~/.claude/CLAUDE.md` for universal preferences
12. **Maintain monthly** — Remove stale rules, add new ones, keep it lean

## Related Reading

- [CLAUDE.md Guide: Give AI Perfect Context](/posts/ai/2026-02-28-claude-code-claudemd-guide/) — The fundamentals of CLAUDE.md and the three-layer system
- [CLAUDE.md vs README.md](/posts/ai/2026-01-31-claudemd-vs-readme/) — Why these two files serve different audiences
- [Claude Code Setup Guide 2026](/posts/ai/2026-02-25-claude-code-setup-guide/) — Installation, authentication, and first project setup
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Automate actions before and after Claude Code operations
- [Claude Code Skills Guide](/posts/ai/2026-02-28-claude-code-skills-guide/) — Build reusable task workflows that complement CLAUDE.md
- [10 Claude Code Mistakes](/posts/ai/2026-02-25-claude-code-mistakes/) — Common pitfalls including skipping CLAUDE.md
- [Claude Code Pricing 2026](/posts/ai/2026-02-25-claude-code-pricing/) — Choose the right plan for your usage

---

CLAUDE.md isn't magic. It's a plain text file with instructions. But the difference between a developer who maintains a good CLAUDE.md and one who doesn't is the difference between an AI that knows your project and one that's guessing. Write tight rules, test them, keep them updated, and let Claude handle the rest.
