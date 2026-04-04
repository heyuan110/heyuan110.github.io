+++
date = '2026-04-04T15:00:00+08:00'
draft = false
title = 'Harness Engineering #2: How to Write CLAUDE.md Files That Actually Work'
description = 'Research-backed guide to writing effective CLAUDE.md files. The ETH Zurich study found human-written files under 60 lines beat LLM-generated verbose ones. Learn the principles, anti-patterns, templates, and measurement strategies.'
toc = true
tags = ['Harness Engineering', 'Claude Code', 'CLAUDE.md', 'AI Agents', 'AI Engineering']
keywords = ['CLAUDE.md best practices', 'how to write CLAUDE.md', 'CLAUDE.md guide 2026', 'harness engineering CLAUDE.md', 'CLAUDE.md vs AGENTS.md', 'CLAUDE.md anti-patterns', 'CLAUDE.md template', 'ETH Zurich CLAUDE.md study']

[[params.faqItems]]
question = "How long should a CLAUDE.md file be?"
answer = "Research from ETH Zurich shows that human-written files under 60 lines outperform longer alternatives. LLM-generated verbose files (200+ lines) actually degraded agent performance by 20% while increasing token costs. The key principle is: every line must prevent a real mistake. If removing a line would not cause Claude to do something wrong, cut it."

[[params.faqItems]]
question = "What is the difference between CLAUDE.md and AGENTS.md?"
answer = "CLAUDE.md is Anthropic's native configuration for Claude Code with features like hierarchical scoping, @import syntax, and user-level overrides. AGENTS.md is an open standard adopted by the Linux Foundation's Agentic AI Foundation, supported by 60,000+ repositories across tools like Codex, Cursor, and Copilot. If you use multiple AI tools, put shared instructions in AGENTS.md and Claude-specific features in CLAUDE.md."

[[params.faqItems]]
question = "Should I use an LLM to generate my CLAUDE.md file?"
answer = "No. The ETH Zurich study tested 138 agentfiles and found that LLM-generated context files decreased success rates while increasing costs by approximately 20%. Agents spent 14-22% more reasoning tokens processing verbose LLM-generated instructions without improving resolution rates. Write your CLAUDE.md by hand, based on real mistakes the agent has made."

[[params.faqItems]]
question = "What should I NOT put in CLAUDE.md?"
answer = "Do not include: code style rules (use linters instead), directory listings (the agent can read the filesystem), standard language conventions Claude already knows, full API documentation (link to it), codebase overviews, or tool-steering instructions. The most common mistake is treating CLAUDE.md like documentation. It is not — it is a constraint injection file."

[[params.faqItems]]
question = "How do I know if my CLAUDE.md is working?"
answer = "Track three metrics: First-attempt success rate (does the agent get it right on the first try?), unnecessary tool calls (is the agent exploring the codebase for information that should be in CLAUDE.md?), and repeated corrections (are you telling the agent the same thing across multiple sessions?). A working CLAUDE.md eliminates repeated corrections and reduces exploratory tool calls."
+++

![A minimalist code editor showing a concise CLAUDE.md file with harness engineering guide rails and feedback loops](cover.webp)

This is **Part 2** of the [Harness Engineering series](/posts/ai/2026-04-04-harness-engineering-guide/). Part 1 covered the full framework — what harness engineering is, why it matters, and the core concepts of Guides and Sensors. This article goes deep on the single most important Guide in your harness: the `CLAUDE.md` file.

If you have not read Part 1, the key concept you need is this: **Agent = Model + Harness**. The harness is everything around the model — tools, constraints, feedback loops, and configuration files. `CLAUDE.md` is the primary feedforward control that steers agent behavior before generation begins.

Most `CLAUDE.md` files are bad. Not because people do not try, but because they optimize for the wrong thing. They write documentation when they should write constraints. They add information the agent already knows. They generate files with AI instead of writing them from observed failures.

This guide shows you what actually works, backed by research and real-world evidence.

## The ETH Zurich Study: What the Data Says

In early 2026, researchers at ETH Zurich published [a study](https://www.infoq.com/news/2026/03/agents-context-file-value-review/) that tested 138 agentfiles across multiple AI coding agents (Claude Code, Codex, Qwen Code) on 300 SWE-bench Lite tasks and a new 138-task benchmark called AGENTbench.

The results were surprising:

| File Type | Performance Impact | Cost Impact |
|-----------|-------------------|-------------|
| Human-written, concise (<60 lines) | +4% success rate | Neutral |
| LLM-generated, verbose (200+ lines) | -3% success rate | +20% token cost |
| No agentfile at all | Baseline | Baseline |

**LLM-generated files made agents worse.** Agents spent 14-22% more reasoning tokens processing verbose instructions, took more steps to complete tasks, and ran more tools — all without improving resolution rates.

The researchers' conclusion was stark: **omit LLM-generated context files entirely, and limit human-written instructions to non-inferable details.**

This aligns with what the [harness engineering framework](/posts/ai/2026-04-04-harness-engineering-guide/) predicts. Guides work by narrowing the solution space. A verbose file does not narrow — it floods. An agent receiving 300 lines of instructions must spend reasoning capacity deciding which instructions are relevant, leaving less capacity for the actual task.

## The 60-Line Principle

The convergence point from ETH Zurich's research, Anthropic's internal usage data, and community benchmarks is clear: **keep your CLAUDE.md under 60 lines**.

This is not arbitrary. It follows from how LLMs process context:

1. **Attention is finite.** Every line in CLAUDE.md competes with task-relevant context for attention weight.
2. **Specificity beats volume.** One precise constraint prevents more errors than ten vague guidelines.
3. **Constraints compound.** Each unnecessary line dilutes the attention given to every other line.

### The Litmus Test

For every line in your CLAUDE.md, ask: **"Would removing this line cause Claude to make a specific, observable mistake?"**

If the answer is no, cut it. Be ruthless.

Lines that pass the test:
- `Use pnpm, not npm` (Claude defaults to npm)
- `All API responses use shared Result<T> type` (Claude cannot infer this)
- `Tests live next to source: foo.ts → foo.test.ts` (project-specific convention)

Lines that fail the test:
- `Write clean, well-documented code` (Claude already does this)
- `Follow best practices` (too vague to constrain anything)
- `This is a TypeScript project using React` (Claude infers this from the codebase)

## What Belongs in CLAUDE.md (and What Does Not)

### Include: Non-Inferable Specifics

These are things Claude **cannot** determine by reading your codebase:

```markdown
## Commands
- `pnpm test` — run tests (not npm test)
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — strict TypeScript

## Conventions
- All API handlers return Result<T, AppError> type
- Database migrations use reversible format (up + down)
- Commit messages follow Conventional Commits
- Feature branches: feat/description, bug fixes: fix/description

## Architecture Decisions
- No circular imports between modules (enforced by eslint-plugin-import)
- Frontend never imports from backend directly — use shared types package
- All external API calls go through src/lib/api-client.ts
```

### Exclude: Things Claude Already Knows

| Category | Example | Why to exclude |
|----------|---------|----------------|
| Language basics | "Use TypeScript strict mode" | Claude reads `tsconfig.json` |
| Framework conventions | "Use React hooks, not class components" | Claude knows modern React |
| General best practices | "Write unit tests for critical code" | Too vague, no actionable constraint |
| Directory listings | "src/ contains source code" | Claude can read the filesystem |
| Codebase overview | "This app has a frontend and backend" | Claude infers this from files |
| Tool steering | "Use grep to search" | Claude picks the right tool itself |

### The Anti-Pattern Gallery

Here are real anti-patterns from production CLAUDE.md files, and why they fail:

**Anti-pattern 1: The Documentation Dump**

```markdown
# BAD: 247 lines of project documentation
## Project Overview
This is a full-stack e-commerce application built with Next.js 14,
using the App Router pattern with React Server Components...
[200+ more lines describing the architecture]
```

Why it fails: This is a README, not an instruction file. Claude can infer architecture from code. You have consumed 247 lines of context budget to convey zero actionable constraints.

**Anti-pattern 2: The LLM-Generated Manifesto**

```markdown
# BAD: Generated by asking "write me a CLAUDE.md"
## Code Quality Standards
- Write clean, maintainable code following industry best practices
- Use meaningful variable names that clearly convey purpose
- Add comprehensive comments for complex logic
- Ensure proper error handling throughout the codebase
- Follow the DRY principle to avoid code duplication
```

Why it fails: Every line is something Claude already does by default. This file adds zero signal while consuming attention budget. The ETH Zurich study found files like this **decreased** performance by 3%.

**Anti-pattern 3: The Everything File**

```markdown
# BAD: 500+ lines covering every possible scenario
## Database
[40 lines about database conventions]
## Authentication
[30 lines about auth patterns]
## Deployment
[25 lines about deploy procedures]
## API Design
[35 lines about REST conventions]
## Testing
[50 lines about testing strategies]
...
```

Why it fails: When everything is important, nothing is. The agent cannot distinguish critical constraints from nice-to-have preferences. Use [progressive disclosure with Skills](/posts/ai/2026-01-08-claudecode-skill-guide/) instead.

## Progressive Disclosure: The Skills Solution

The answer to "my CLAUDE.md is too long" is not "write a shorter CLAUDE.md." It is **move domain-specific knowledge into Skills that load on demand**.

This is the progressive disclosure pattern from [harness engineering](/posts/ai/2026-04-04-harness-engineering-guide/):

```
CLAUDE.md (always loaded, <60 lines)
  → Universal constraints
  → Build/test commands  
  → Critical architecture decisions

Skills (loaded on demand)
  → Database migration rules
  → API design patterns
  → Deployment procedures
  → Testing conventions
```

### How It Works in Practice

Your CLAUDE.md stays lean:

```markdown
# CLAUDE.md

## Project
- TypeScript monorepo, pnpm workspaces
- React frontend (packages/web), Express backend (packages/api)

## Commands
- `pnpm test` — run all tests
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — TypeScript strict mode

## Critical Rules
- All API responses use Result<T, AppError>
- No direct database queries outside packages/db
- Never modify shared types without running full test suite
```

Domain knowledge lives in Skills:

```markdown
# .claude/skills/database-migration.md
---
name: database-migration
description: Rules for creating or modifying database migrations
---

## Migration Rules
- Always create reversible migrations (up + down)
- Use transactions for DDL changes
- Never modify an existing migration file — create a new one
- Test against production schema copy before merging
- Migration files: YYYYMMDDHHMMSS_description.ts
```

When Claude works on a database migration, the skill loads automatically. When it works on frontend components, it does not waste context on database rules. The agent's context window stays clean, and each piece of guidance gets full attention when it is relevant.

For a deep dive on Skills, see the [Claude Code Skills Guide](/posts/ai/2026-01-08-claudecode-skill-guide/) and [Skill Patterns](/posts/ai/2026-01-12-claudecode-skill-patterns/).

## CLAUDE.md vs AGENTS.md: When to Use Which

Since 2025, the ecosystem has two standards for agent instruction files:

| Feature | CLAUDE.md | AGENTS.md |
|---------|-----------|-----------|
| **Scope** | Claude Code only | Any AI coding tool |
| **Standard body** | Anthropic | Linux Foundation (Agentic AI Foundation) |
| **Adoption** | Native to Claude Code | 60,000+ GitHub repos |
| **Hierarchical scoping** | Yes (root, subdirectory, user-level) | Partial (subdirectory only) |
| **Import system** | `@import` syntax with recursive resolution | No |
| **User-level overrides** | `~/.claude/CLAUDE.md` | No |
| **Local files (untracked)** | `.claude/CLAUDE.local.md` | No |

### The Practical Rule

If your team uses **only Claude Code**: Use CLAUDE.md for everything.

If your team uses **multiple AI tools** (Cursor, Copilot, Codex, etc.): Put shared instructions in AGENTS.md, and keep CLAUDE.md for Claude-specific features:

```markdown
# CLAUDE.md
See @AGENTS.md for shared project conventions.

## Claude-Specific
- Use sub-agents for codebase exploration tasks
- Prefer Sonnet for test generation, Opus for architecture decisions
- Run typecheck hook after every file edit
```

```markdown
# AGENTS.md
## Project
- TypeScript monorepo, pnpm workspaces

## Conventions
- All API responses use Result<T, AppError>
- Tests next to source: foo.ts → foo.test.ts

## Commands
- `pnpm test` — run tests
- `pnpm lint` — lint check
```

This blog itself uses this pattern — [our AGENTS.md](https://github.com/heyuan110/heyuan110.github.io/blob/code/AGENTS.md) contains shared conventions for all AI tools, while CLAUDE.md simply points to it with Claude-specific additions.

For a deeper comparison of these files, see [CLAUDE.md vs README.md](/posts/ai/2026-01-31-claudemd-vs-readme/).

## Templates for Common Project Types

### Monorepo (TypeScript)

```markdown
# CLAUDE.md — 28 lines

## Project
- TypeScript monorepo, pnpm workspaces
- Packages: web (React), api (Express), shared (types + utils), db (Prisma)

## Commands
- `pnpm test` — all tests
- `pnpm test --filter=web` — frontend tests only
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — TypeScript strict

## Rules
- Cross-package imports only through package.json exports
- Shared types in packages/shared — never duplicate
- API handlers return Result<T, AppError>
- No circular dependencies (enforced by eslint-plugin-import)

## Testing
- Unit tests next to source: foo.ts → foo.test.ts
- Integration tests in __tests__/ at package root
- Mock external services, never real API calls in tests

## Git
- Conventional commits (feat:, fix:, refactor:, test:, docs:)
- One PR per feature, squash merge to main
```

### API Service (Python)

```markdown
# CLAUDE.md — 24 lines

## Project
- Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic migrations
- Package manager: uv (not pip)

## Commands
- `uv run pytest` — run tests
- `uv run ruff check .` — linting
- `uv run mypy .` — type checking
- `uv run alembic upgrade head` — apply migrations

## Rules
- All endpoints return ResponseModel[T] wrapper
- Database access only through repository pattern (src/repos/)
- Environment variables via pydantic-settings, never os.getenv
- New endpoints need: handler, schema, test, OpenAPI docstring

## Migrations
- Always reversible (upgrade + downgrade)
- One migration per PR
- Never edit existing migrations
```

### Frontend App (React)

```markdown
# CLAUDE.md — 22 lines

## Project
- React 19, TypeScript, Vite, Tailwind CSS 4
- State: Zustand for global, React Query for server state

## Commands
- `npm run dev` — dev server (port 3000)
- `npm test` — Vitest
- `npm run lint` — ESLint + Prettier
- `npm run typecheck` — tsc --noEmit

## Rules
- Components in src/components/, one component per file
- Custom hooks in src/hooks/, prefixed with use*
- No inline styles — Tailwind classes only
- Server state through React Query, never useEffect + fetch
- All user-facing text through i18n (src/i18n/)

## Testing
- Component tests with Testing Library
- Mock API calls with MSW, never fetch mocking
```

Notice the pattern: each template is **under 30 lines**, contains **only non-inferable specifics**, and focuses on **constraints that prevent real mistakes**.

## The Hierarchy: How Claude Loads Configuration

Claude Code loads CLAUDE.md files from multiple locations, and they merge in a specific order:

```
~/.claude/CLAUDE.md          (user-level, all projects)
  ↓ merged with
./CLAUDE.md                   (project root)
  ↓ merged with
./packages/web/CLAUDE.md      (subdirectory, closest to edited file)
  ↓ merged with
./.claude/CLAUDE.local.md     (local overrides, not committed)
```

Use this hierarchy strategically:

| Level | What goes here | Example |
|-------|---------------|---------|
| **User-level** (`~/.claude/`) | Personal preferences, global tooling | "Use vim keybindings in diffs" |
| **Project root** (`./`) | Team conventions, build commands | "pnpm, not npm" |
| **Subdirectory** (`./packages/web/`) | Package-specific rules | "React components use .tsx extension" |
| **Local** (`.claude/CLAUDE.local.md`) | Machine-specific overrides | "Database runs on port 5433 locally" |

The key insight: **rules closer to the edited file take priority**. If your root CLAUDE.md says "use Jest" but `packages/web/CLAUDE.md` says "use Vitest," the agent uses Vitest when editing files in that package.

## Measuring Effectiveness

A CLAUDE.md file is a harness component. Like any engineering artifact, it should be measured. Track these three metrics:

### 1. First-Attempt Success Rate

**What:** The percentage of tasks where Claude produces correct output on the first attempt, without requiring corrections.

**How to measure:** Review your last 20 Claude Code sessions. Count how many required zero corrections vs. how many needed "no, do it this way" interventions.

**Target:** 70%+ for well-harnessed projects. Below 50% means your CLAUDE.md is missing critical constraints.

### 2. Repeated Correction Rate

**What:** How often you tell Claude the same thing across multiple sessions.

**How to measure:** Keep a tally for one week. Every time you correct Claude, note what you said. If the same correction appears 3+ times, it belongs in CLAUDE.md.

**Target:** Zero repeated corrections. Every repeated correction is a missing CLAUDE.md line.

### 3. Exploratory Tool Calls

**What:** How many tool calls Claude makes to understand the project before starting work.

**How to measure:** Check Claude's tool usage in a typical session. If it runs `find`, `grep`, or reads multiple files just to understand project structure, your CLAUDE.md is missing orientation information.

**Target:** Claude should start working on the actual task within 2-3 tool calls.

### The Feedback Loop

These metrics feed back into your CLAUDE.md:

```
Repeated correction detected
  → Add constraint to CLAUDE.md
  → Verify it reduces corrections
  → If CLAUDE.md exceeds 60 lines
    → Move least-critical rules to Skills
```

This is the [Guide + Sensor pattern](/posts/ai/2026-04-04-harness-engineering-guide/) in action: your observations (sensor) improve your CLAUDE.md (guide), which reduces future errors, which changes what you observe.

## Real Example: This Blog's Configuration

This blog uses the hierarchical pattern in production. Here is the actual structure:

**`CLAUDE.md`** (2 lines):
```markdown
see @AGENTS.md
```

**`AGENTS.md`** (79 lines of active rules):
- Interaction language (Chinese for conversation, English for content)
- Git branch conventions (`code` branch, auto-deploy)
- Hugo build commands
- Multilingual setup (English default, Chinese optional)
- Front matter template with required fields
- Image format rules (WebP only, 1200x630 covers)
- Content strategy constraints (no personal journal entries)

The AGENTS.md is at the upper limit of what research recommends. But it works because every line prevents a specific mistake — wrong branch, wrong language, missing front matter field, incorrect image format.

Domain-specific knowledge (like deployment procedures or theme customization rules) lives in separate documentation files that Claude reads on demand, not in the always-loaded configuration.

## The Checklist

Before committing your CLAUDE.md, verify:

- [ ] **Under 60 lines** — count them
- [ ] **Every line prevents a specific mistake** — apply the litmus test
- [ ] **No inferable information** — nothing Claude can determine from code
- [ ] **No generic advice** — no "write clean code" or "follow best practices"
- [ ] **Commands are exact** — `pnpm test`, not "run the tests"
- [ ] **Domain knowledge in Skills** — not stuffed into the main file
- [ ] **Written by a human** — not generated by an LLM
- [ ] **Tested against real tasks** — not theoretical

## Related Reading

- [Harness Engineering: Why the System Around Your AI Agent Matters More Than the Model](/posts/ai/2026-04-04-harness-engineering-guide/) — Part 1 of this series
- [CLAUDE.md Guide: Give Claude Code Persistent Memory](/posts/ai/2026-01-12-claudemd-memory-guide/) — Getting started with CLAUDE.md
- [CLAUDE.md vs README.md](/posts/ai/2026-01-31-claudemd-vs-readme/) — Understanding the different purposes of each file
- [Claude Code Skills Guide](/posts/ai/2026-01-08-claudecode-skill-guide/) — Progressive disclosure with Skills
- [Claude Code Best Practices](/posts/ai/2026-01-06-claudecode-best-practices/) — Foundational Claude Code workflow tips
- [Superpowers Deep Dive](/posts/ai/2026-02-01-superpowers-deep-dive/) — A real-world Skills harness in action
