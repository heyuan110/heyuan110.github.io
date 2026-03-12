+++
date = '2026-01-12T00:00:00+08:00'
draft = false
title = 'CLAUDE.md Guide: Give Claude Code Persistent Memory'
description = 'Learn how to configure CLAUDE.md so Claude Code remembers your tech stack, coding standards, and workflow preferences across every conversation.'
toc = true
tags = ['AI', 'Claude Code', 'CLAUDE.md', 'Developer Tools']
categories = ['AI Guides']
keywords = ['CLAUDE.md configuration', 'Claude Code memory', 'CLAUDE.md setup guide', 'Claude Code project config', 'AI coding standards']
+++
![Memory Guide](memory-guide.webp)

## The Problem: Repeating Yourself Every Single Time

Claude Code is a fantastic coding assistant. But it has one glaring weakness: **it forgets everything between conversations.**

Every new session, you find yourself saying the same things:

- "We use pnpm, not npm"
- "Follow ESLint + Prettier for code style"
- "Git commit messages should use conventional commits"
- "This project runs React 18 + TypeScript + Tailwind"

Once is fine. Doing it every day? Exhausting.

It gets worse with teams. You set things up perfectly on your end, but your colleague starts fresh with a blank slate. Claude generates completely different code styles for each of you.

**CLAUDE.md solves this problem.**

> **CLAUDE.md is Claude's onboarding handbook — write it once, and it takes effect forever.**

Just like a new hire reads the company handbook on day one, Claude reads this file every time it starts up and follows its instructions.

## What CLAUDE.md Actually Is

### A Plain Markdown File

No magic involved. CLAUDE.md is a regular Markdown file placed in your project root or home directory.

Whatever you write in it, Claude remembers:

- Project context and tech stack
- Code conventions and style rules
- Common commands and workflows
- Your personal preferences

Here is a minimal example:

```markdown
# Project Overview

An e-commerce admin dashboard built with Next.js 14.

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Prisma + PostgreSQL

## Code Standards

- Use functional components, no class components
- State management: Zustand
- All functions must have TypeScript type annotations
- Variables: camelCase, Components: PascalCase

## Common Commands

- Dev server: pnpm dev
- Build: pnpm build
- Test: pnpm test
```

That is it. Claude reads this file and "knows" your project. Every piece of code it generates will follow your conventions automatically.

### When Does Claude Read It?

Every time you launch Claude Code or start a new conversation, it **automatically loads** CLAUDE.md.

No need to manually reference it. No need to say "please read my config file first." Claude finds and reads it on its own.

The loading order is:

1. Global config: `~/.claude/CLAUDE.md`
2. Project config: `./CLAUDE.md`
3. Personal config: `./CLAUDE.local.md`

Later files override earlier ones. This design is intentional: global settings for universal rules, project settings for team standards, personal settings for individual preferences.

### CLAUDE.md vs Skills: What Is the Difference?

These two features confuse many users. Here is a quick comparison:

| Feature | CLAUDE.md | Skill |
|---------|-----------|-------|
| Purpose | Defines "who you are" | Defines "how to do a task" |
| Content | Project context, code standards, preferences | Step-by-step task execution |
| Trigger | Auto-loaded every conversation | Activated when a matching task arises |
| Analogy | Employee handbook | Standard operating procedure |

**In short:**

- CLAUDE.md tells Claude "what environment you work in"
- Skills tell Claude "how to handle specific tasks"

They are complementary, not competing.

## The Three-Layer Configuration System

CLAUDE.md supports three configuration layers, each serving a different purpose.

### Project Level: CLAUDE.md

Lives in your project root. **Committed to Git.** Shared by the entire team.

```
your-project/
├── CLAUDE.md        ← this one
├── package.json
├── src/
└── ...
```

**What to put here:**

- Tech stack documentation
- Team coding standards
- Directory structure overview
- Common commands

**Core principle:** Everything here represents team consensus. Everyone follows it.

### Personal Level: CLAUDE.local.md

Lives in your project root. **Not committed to Git** (add it to .gitignore).

```
your-project/
├── CLAUDE.md
├── CLAUDE.local.md  ← this one
├── .gitignore       ← add CLAUDE.local.md here
└── ...
```

**What to put here:**

- Your personal coding habits
- Local environment-specific settings
- Temporary debugging instructions

**Example:** The team standard says comments must be in English, but you prefer drafting in your native language first and translating later. That kind of personal quirk belongs here.

### Global Level: ~/.claude/CLAUDE.md

Lives in your home directory. **Works across all projects.**

```
~/.claude/
└── CLAUDE.md        ← this one
```

**What to put here:**

- Your personal info (name, role)
- Universal coding preferences
- Rules that apply to every project

**Example:**

```markdown
# About Me

I'm Bruce, a full-stack engineer working primarily with TypeScript and Go.

## Universal Preferences

- Prefer functional programming style
- Keep things simple, avoid over-engineering
- Small, focused commits over large changesets
```

### Layer Priority

When all three files exist, the loading order is:

```
Global → Project → Personal
```

**Later files override earlier ones.**

For example:
- Global sets "comments in English"
- Project does not specify
- Personal sets "comments in Chinese"

The final result: "comments in Chinese."

| Layer | File Path | Git Tracked | Scope |
|-------|-----------|-------------|-------|
| Global | ~/.claude/CLAUDE.md | — | All projects |
| Project | ./CLAUDE.md | Yes | Current project (team-wide) |
| Personal | ./CLAUDE.local.md | No | Current project (you only) |

## Four Ways to Manage CLAUDE.md

### /init — One-Command Setup

The simplest approach. Run Claude Code in your project directory and type:

```
/init
```

Claude analyzes your project structure and generates a CLAUDE.md draft. It reads package.json, tsconfig.json, .eslintrc, and other config files to identify your tech stack and conventions.

**Pros:** Quick start, minimal effort.

**Cons:** Output is generic. You will need to add project-specific details manually.

### # Syntax — Quick Append

During any conversation, prefix a line with `#` to add a rule to CLAUDE.md:

```
# All API requests must include loading state handling
```

Claude appends this rule to the config file.

**Best for:** Capturing rules on the fly as you discover them during coding sessions.

### /memory — Visual Editor

Type:

```
/memory
```

This opens an interactive interface for viewing and editing your CLAUDE.md content. You can choose which layer to edit (global, project, or personal).

### @ References — Modular Composition

When your config grows large, split it into multiple files and reference them with `@` syntax:

```markdown
# Project Config

@docs/architecture.md
@docs/api-conventions.md
@docs/testing-guide.md
```

Claude automatically reads all referenced files.

**Best for:** Large projects where the config exceeds a few hundred lines. Modular files are easier to maintain.

## Three Ready-to-Use Templates

### Solo Developer Template

For individual developers. Place in `~/.claude/CLAUDE.md`:

```markdown
# About Me

I'm [Your Name], [Your Role].

## Coding Preferences

- Meaningful variable names, no single-letter throwaway names
- Prefer functional programming patterns
- Code should be self-documenting, minimal comments
- Git commits: conventional commit format

## Work Habits

- Run lint after every change
- Ensure zero TypeScript errors before committing
- Small, focused commits — avoid changing too many files at once

## Things I Dislike

- Over-abstraction
- Unnecessary design patterns
- Functions longer than 50 lines (break them up)
```

### Team Collaboration Template

For team projects. Place in your project root `CLAUDE.md` and commit to Git.

````markdown
# Project Name

[One-line project description]

## Tech Stack

- Framework: Next.js 14 (App Router)
- Language: TypeScript 5.x (strict mode)
- Styling: Tailwind CSS
- State: Zustand
- Database: PostgreSQL + Prisma
- Testing: Vitest + Testing Library

## Directory Structure

```
src/
├── app/          # Next.js App Router pages
├── components/   # Reusable components
│   ├── ui/       # Base UI components
│   └── features/ # Feature-specific components
├── lib/          # Utility functions and config
├── hooks/        # Custom hooks
├── stores/       # Zustand stores
├── types/        # TypeScript type definitions
└── services/     # API call layer
```

## Code Standards

### Naming Conventions
- Files: kebab-case (e.g., `user-profile.tsx`)
- Components: PascalCase (e.g., `UserProfile`)
- Functions/variables: camelCase (e.g., `getUserById`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

### Component Rules
- Functional components + Hooks only
- Props must have a TypeScript interface
- Break complex components into smaller ones

### Git Conventions
- Commit format: `type: description`
- Types: feat / fix / refactor / docs / test / chore
- Example: `feat: add user authentication flow`

## Common Commands

```bash
pnpm dev          # Start dev server
pnpm build        # Production build
pnpm test         # Run tests
pnpm lint         # Lint check
pnpm db:migrate   # Run database migrations
```

## Important Notes

- All API requests must handle loading and error states
- Sensitive data goes in .env.local, never commit it
- New features require unit tests
````

### Tech Stack-Specific Templates

#### React + TypeScript Project

```markdown
# React Project Standards

## Component Rules

- Functional components only
- State: useState for simple, Zustand for complex
- useEffect dependencies must be exhaustive
- Avoid creating new objects/functions in render (use useMemo/useCallback)

## Type Definitions

- Component Props: use interface, name as `XxxProps`
- API response types: place in `types/api.ts`
- Never use any — use unknown if the type is truly uncertain

## File Organization

- One component per folder: `ComponentName/index.tsx`
- Component-specific styles: `ComponentName/styles.ts`
- Component-specific types: `ComponentName/types.ts`
```

#### Python Project

````markdown
# Python Project Standards

## Code Style

- Follow PEP 8
- Use Black formatter, line width 88
- Use type hints throughout
- Docstrings: Google style

## Project Structure

- Entry point: main.py
- Config management: pydantic-settings
- Dependency management: Poetry

## Common Commands

```bash
poetry install     # Install dependencies
poetry run pytest  # Run tests
poetry run black . # Format code
```
````

## Advanced Techniques

### Modularize Large Configurations

When CLAUDE.md exceeds 500 lines, maintenance becomes painful.

Use `@` references to split it into focused files:

```markdown
# Project Config

## Overview
@docs/overview.md

## Architecture
@docs/architecture.md

## API Conventions
@docs/api-conventions.md

## Testing Guide
@docs/testing-guide.md
```

Each referenced file covers a single topic — clean and maintainable.

### Combining CLAUDE.md with Skills

CLAUDE.md defines the environment. Skills define the tasks. Together, they are powerful.

**In CLAUDE.md**, write:

```markdown
## Code Review Standards

- Must have unit tests
- No console.log statements
- No hardcoded configuration values
```

**In a Skill**, write the review workflow:

```markdown
---
name: code-review
description: Review code changes for standards compliance and potential issues
---

# Code Review Skill

## Steps

1. Read git diff
2. Check against code review standards in CLAUDE.md
3. Output issue list with fix suggestions
```

The Skill automatically references the standards from CLAUDE.md. No duplication needed.

### Team Collaboration Best Practices

1. **Always commit CLAUDE.md to Git**
   - It represents team consensus
   - Check CLAUDE.md compliance during code reviews

2. **Add CLAUDE.local.md to .gitignore**
   - Personal preferences should not be forced on others
   - Avoids merge conflicts

3. **Update regularly**
   - As the project evolves, the config should too
   - When Claude keeps making the same mistake, add a rule

4. **First thing for new team members**
   - Have them read CLAUDE.md on day one
   - It is not just for Claude — it is documentation for humans too

## Final Thoughts

At its core, CLAUDE.md turns volatile context into persistent configuration.

All those things you tell Claude every day — project background, code standards, personal preferences — instead of repeating them endlessly, you write them down once and they last forever.

This is not just about "making AI work better." It is about turning your knowledge into a reusable asset.

A well-written CLAUDE.md is like an onboarding handbook. Claude follows it. New teammates learn from it. Your standards propagate automatically.

**AI has no memory, but you can give it one.**

CLAUDE.md is that memory.
