+++
date = '2026-04-09T10:00:00+08:00'
draft = false
title = 'Claude Code + OpenSpec + Superpowers: When to Use All Three (and When Not To)'
description = 'A deep dive into combining Claude Code, OpenSpec, and Superpowers for AI-assisted development. Includes a decision matrix, hands-on walkthrough, and command cheat sheet to help you decide when the full stack is worth it.'
toc = true
tags = ['Claude Code', 'OpenSpec', 'Superpowers', 'AI Development', 'Spec-Driven Development']
keywords = ['Claude Code OpenSpec Superpowers', 'OpenSpec tutorial', 'Superpowers Claude Code', 'spec-driven development', 'AI coding workflow 2026', 'OpenSpec vs Superpowers', 'AI engineering best practices']

[[params.faqItems]]
question = "What is the difference between OpenSpec and Superpowers?"
answer = "OpenSpec manages 'what to build' — it converts requirements into traceable spec documents (proposal, spec, design, tasks). Superpowers manages 'how to build it' — it enforces TDD, code review, subagent-driven development, and other engineering disciplines. They solve fundamentally different problems and are complementary, not competing."

[[params.faqItems]]
question = "Is using all three tools together overkill?"
answer = "For tasks under 4 hours, yes. OpenSpec's propose→apply→archive cycle alone takes 30-60 minutes. For quick prototypes, use Claude Code alone. For medium tasks, add Superpowers. Reserve the full stack for team projects or production code that needs decision traceability."

[[params.faqItems]]
question = "How do I install OpenSpec?"
answer = "Run npm install -g @fission-ai/openspec@latest, then openspec init in your project directory. Requires Node.js 20.19.0+. During init, select your AI tool (Claude Code, Cursor, etc.)."

[[params.faqItems]]
question = "Can OpenSpec and Superpowers be used separately?"
answer = "Yes. Superpowers alone works well for personal projects that don't need decision auditing. OpenSpec alone suits teams that need specs but aren't using Claude Code's subagent capabilities. But the combination delivers significantly more value than either tool in isolation."

[[params.faqItems]]
question = "What does Superpowers actually enforce on Claude Code?"
answer = "Superpowers enforces a 7-stage workflow: Brainstorming (Socratic questioning), Git Worktrees (isolated branches), Planning (2-5 min tasks), Subagent Development (parallel execution with two-stage review), TDD (RED-GREEN-REFACTOR with code deletion if tests aren't written first), Code Review, and Branch Completion."
+++

![Claude Code + OpenSpec + Superpowers AI development workflow](cover.webp)

## You've Probably Hit These Three Walls

If you've used Claude Code or any AI coding tool seriously, these scenarios will be familiar.

**Wall 1: The AI builds something different from what you wanted.** You say "add user login," it gives you session-based auth when you wanted JWT. You say "payment scanning," it integrates a real payment SDK when you just wanted a demo. You only discover the mismatch after reviewing the generated code — by then, you've already burned tokens and time.

**Wall 2: The AI skips engineering discipline.** Claude Code's default behavior is "receive request, start coding." No Git branches, no tests, no code review. It ships fast, but when something breaks, you don't know where the problem is. And rolling back is painful because it modified your main branch directly.

**Wall 3: Decisions disappear when you close the chat.** Why bcrypt over argon2? Why `/api` prefix instead of `/v1`? Last week's design decisions vanish with the conversation. Three months later, nobody remembers the reasoning. A new team member has zero context.

These problems can't be solved with better prompts — they require **different tools operating at different layers.** That's what this article is about: Claude Code + OpenSpec + Superpowers.

![AI coding three common problems: requirement drift, missing discipline, decision amnesia](03-comparison-three-problems.webp)

## Layer 1: Meet the Three Tools

### Claude Code: An AI Programmer in Your Terminal

[Claude Code](https://code.claude.com/docs/) is Anthropic's official CLI tool for AI-assisted development. Unlike chat-based tools, it lives in your terminal — reading project files, running shell commands, writing code, managing Git. It can autonomously complete an entire "create project → write code → run tests → commit" workflow.

It's powerful, but has the three problems above: potential requirement mismatches, no enforced engineering discipline, and ephemeral decisions. It needs partners.

**Prerequisite**: Claude Pro ($20/month), Team, or Enterprise subscription required.

### OpenSpec: Turns One-Sentence Requirements into Four Structured Documents

[OpenSpec](https://openspec.dev/) is an open-source framework by Fission AI for Spec-Driven Development, specifically solving **Wall 1**. It expands "I want user login" into:

- **proposal.md**: Why, what's in scope, and critically — **what's out of scope** (preventing AI from adding unrequested features)
- **specs/**: Behavioral specifications using GIVEN/WHEN/THEN scenarios
- **design.md**: Technical decisions with reasoning
- **tasks.md**: Implementation checklist, each task completable in 2-5 minutes

OpenSpec supports 20+ AI coding assistants, but works best with Claude Code thanks to its subagent capabilities for parallel task execution.

### Superpowers: Engineering Discipline as Enforceable Rules

[Superpowers](https://github.com/obra/superpowers) is an open-source skills framework by Jesse Vincent and Prime Radiant (140K+ GitHub stars), solving **Wall 2**. It's not a standalone tool — it's skills installed into Claude Code that enforce professional engineering practices.

With Superpowers installed, Claude Code stops jumping straight to coding. It has a set of core skills. **When using Superpowers alone** (without OpenSpec), brainstorming and writing-plans trigger automatically. However, TDD, code-review and other coding disciplines **require explicit configuration in CLAUDE.md** to take effect:

| Skill | When It Activates | Trigger |
|-------|------------------|---------|
| brainstorming | Before creating features or components | Automatic when used alone |
| writing-plans | When requirements need multi-step decomposition | Automatic when used alone |
| test-driven-development | Before implementing features or fixing bugs | Requires explicit rule in CLAUDE.md |
| systematic-debugging | When encountering bugs, test failures, unexpected behavior | Requires explicit rule in CLAUDE.md |
| code-reviewer | After completing a major implementation step | Requires explicit rule in CLAUDE.md |
| dispatching-parallel-agents | When multiple independent tasks can run concurrently | When 2+ tasks have no dependencies |
| verification-before-completion | Before claiming work is done | Requires explicit rule in CLAUDE.md |

> **Important correction**: OpenSpec and Superpowers are two independent systems — they **do not automatically chain together**. When using `/opsx:apply`, Superpowers' TDD, code-review, etc. will **not automatically kick in**. To enforce engineering disciplines during apply, you must explicitly add rules to your project's CLAUDE.md, e.g.: `When using /opsx:apply, always follow TDD: write failing tests first, then implement code.`

When combined, **OpenSpec leads the planning phase, Superpowers leads the coding phase** — each owns its stage:

```
OpenSpec handles:            Superpowers handles:
  Thinking through WHAT        Ensuring HOW it's built well
┌──────────┐               ┌──────────────┐
│ explore  │               │ brainstorming │ ← replaced by propose
│ propose  │               │ writing-plans │ ← replaced by tasks.md
│ apply ───┼─────────────→ │ TDD          │ ← requires CLAUDE.md config
│          │               │ debugging    │ ← requires CLAUDE.md config
│          │               │ verification │ ← requires CLAUDE.md config
│ archive  │               │ code-review  │ ← requires CLAUDE.md config
└──────────┘               └──────────────┘
```

OpenSpec's propose covers requirements exploration and design decisions (proposal.md + design.md + specs + tasks.md), naturally replacing Superpowers' brainstorming and writing-plans. However, when apply enters the coding phase, Superpowers' TDD, debugging, verification, and code-review **do not automatically kick in** — you need to configure these requirements in your project's CLAUDE.md for them to take effect during the apply phase.

Without OpenSpec, Superpowers handles everything — brainstorming first explores requirements, writing-plans breaks down tasks, then TDD enforces test-first coding.

**One-line summary**: OpenSpec handles planning, Superpowers handles coding discipline, Claude Code executes. They don't conflict — each owns its stage.

![Three-layer architecture: OpenSpec requirements, Superpowers discipline, Claude Code execution](04-framework-three-layers.webp)

## Layer 2: Installation — Get All Three Running

### Step 1: Install Claude Code

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash

# Verify
claude --version
```

### Step 2: Install OpenSpec

Requires Node.js 20.19.0+.

```bash
npm install -g @fission-ai/openspec@latest
cd your-project
openspec init    # Select Claude Code when prompted
```

Creates an `openspec/` directory with `specs/`, `changes/archive/`, and `AGENTS.md`.

### Step 3: Install Superpowers

```bash
# Inside a Claude Code session:
/plugin install superpowers@claude-plugins-official
```

You'll see "You have Superpowers" on next launch — that confirms it's working.

### Step 4: Configure Collaboration

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "openspec": {
      "command": "npx",
      "args": ["-y", "@fission-ai/openspec-mcp"]
    }
  },
  "permissions": {
    "allow": ["Bash:openspec:*", "Bash:npm:*", "Bash:git:*"]
  }
}
```

## Layer 3: Run It Once — Feel the Full Workflow

Don't try to understand the theory first — **run it and feel what each tool does.** We'll build a user auth API (Express + MongoDB + JWT).

### 3.1 OpenSpec: Requirements → Spec

```bash
claude
> /opsx:propose User auth API with Express + MongoDB + JWT.
> Features: registration (username+email+password), login (return JWT),
> get current user (requires auth).
> Security: bcrypt password encryption, JWT auth for private endpoints.
```

OpenSpec generates four documents. **Your action**: open `proposal.md`, check the Out of Scope section — confirm the AI didn't add OAuth or password reset on its own.

Refine if needed by editing the files directly — there's no separate refine command in the core profile.

**What you gained**: A structured blueprint. All subsequent AI work is based on this document, not your one-sentence description.

![OpenSpec generates four structured documents from one requirement: proposal, specs, design, tasks](05-infographic-openspec-docs.webp)

### 3.2 Planning Done, Coding Discipline Takes Over

Remember the division of labor? **OpenSpec leads planning, Superpowers leads coding discipline.**

The previous `/opsx:propose` step already completed requirements exploration and design decisions — password algorithm, JWT expiration, ORM choice — all recorded in `design.md`. OpenSpec's propose has covered what Superpowers' brainstorming and writing-plans would normally do.

So when `/opsx:apply` begins, if you've configured TDD and other requirements in CLAUDE.md, Superpowers' coding disciplines take effect: TDD (tests before code), debugging (systematic troubleshooting), verification (pre-completion checks), and code-review (quality gate before commit). **Note: these do not activate automatically — they require explicit configuration in CLAUDE.md.**

**What you gained**: All design decisions are recorded in `design.md`. Three months later, you can see exactly why you chose bcrypt over argon2 — **Wall 3 solved.**

### 3.3 Confirm Plan, Let AI Execute

Superpowers generates `tasks.md` with 6 tasks. Spend 5 minutes reviewing task order and acceptance criteria. Then:

```bash
> Plan confirmed, start execution
```

With TDD configured in CLAUDE.md, subagent mode activates — parallel execution with TDD:

```
[Task 1/6] Project Init ✓
[Task 2/6] Database Connection
  ├─ Write test → Fails (RED) ✓
  ├─ Write implementation → Passes (GREEN) ✓
  ├─ Code Review → Pass ✓
  └─ Git commit ✓
...
```

**What you gained**: AI working on an isolated Git branch, following specs, with TDD enforcement (when configured in CLAUDE.md). If it goes wrong, discard the branch — your main code is untouched. **Wall 2 solved.**

![TDD cycle enforced by Superpowers: RED (write failing test) → GREEN (write implementation) → REFACTOR](06-flowchart-tdd-cycle.webp)

### 3.4 Verify + Archive

```bash
> /opsx:archive   # Don't skip this! Syncs delta specs and archives the change
```

### 3.5 Run and Test

```bash
npm install && node src/app.js
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"123456"}'
# {"success":true,"data":{"id":"...","username":"testuser"}}
```

Requirements to running API — your work was: confirm requirements → answer design questions → review plan → verify results.

![Three-layer workflow pipeline: specification, discipline enforcement, and code execution](02-workflow-pipeline.webp)

## Layer 4: Why All Three Are Necessary

Now that you've felt the workflow, let's understand why removing any tool creates problems. First, a table showing exactly where OpenSpec and Superpowers overlap vs complement each other:

| Capability | OpenSpec | Superpowers |
|------------|:---:|:---:|
| Requirements exploration | ✅ propose | ✅ brainstorming |
| Task decomposition | ✅ tasks.md | ✅ writing-plans |
| **Spec persistence** | ✅ specs/ + archive/ | ❌ Gone when chat closes |
| **Decision traceability** | ✅ design.md | ❌ Buried in chat history |
| **TDD enforcement** | ❌ | ✅ Tests before code |
| **Code review** | ❌ | ✅ Automatic code-review |
| **Git branch isolation** | ❌ | ✅ Worktree |
| **Systematic debugging** | ❌ | ✅ systematic-debugging |
| **Pre-completion verification** | ❌ | ✅ verification |

Only the first two rows overlap. Everything else is **purely complementary.** People who say "they're redundant, just pick one" have either never used Superpowers' TDD and Code Review (thinking it's just a brainstorming tool), or never used OpenSpec's archive (thinking it's just a doc generator).

With this table in mind, it's clear what breaks when you remove each tool.

![Four combinations compared: Claude Code only, two-tool combos, and full triple stack](07-comparison-combinations.webp)

### Claude Code Only: Fast but Chaotic

No specification constraints. Different developers get different code styles, inconsistent return formats (`{code: 200}` vs `{success: true}`), missing security constraints. A real team found passwords stored in plaintext and private endpoints without auth — issues that only surfaced in production.

### OpenSpec + Claude Code (No Superpowers): Blueprint Without a Foreman

Great specs, but no enforcement during execution. Claude may "freestyle" away from the spec. Without TDD and code review rules in CLAUDE.md, there's no branch isolation — like having perfect architectural drawings but no construction supervisor.

### Superpowers + Claude Code (No OpenSpec): Discipline Without Direction

TDD and code review ensure quality, but plans are based on the current chat's understanding. Close the conversation and all requirement context and design rationale is lost. Next iteration starts from scratch. No reusable spec documents for team sharing.

### All Three: Blueprint + Foreman + Construction Crew

```
OpenSpec (Requirements) → Superpowers (Discipline) → Claude Code (Execution)
   │                        │                          │
   ├─ proposal.md           ├─ Brainstorming           ├─ Write code
   ├─ specs/                ├─ TDD enforcement         ├─ Run tests
   ├─ design.md             ├─ Code Review             ├─ Git operations
   └─ tasks.md              └─ Subagent parallelism    └─ Install deps
```

A key design detail: **OpenSpec's spec output is ~250 lines vs ~800 from Spec Kit.** Intentionally concise — specs that are too long don't get read, and AI loses context. Specs describe behavior (GIVEN/WHEN/THEN), not implementation steps.

Another counterintuitive design: **Superpowers' TDD skill deletes code written before tests.** Not warns — deletes. This prevents AI from writing implementation first and then retrofitting tests that only verify "code does what it does" rather than "code does what it should."

## Layer 5: Bigger Cases — Where the Ceiling Is

### Case 1: Blog System in One Day

Next.js + PostgreSQL blog with auth, article CRUD, Markdown rendering, and comments. Four independent OpenSpec changes running in parallel, completed in 8 hours.

Output: ~2,500 lines, 87% test coverage, 23 commits, zero bugs in the first week. Time breakdown: **requirements 19%, planning 13%, execution 56%, verification 12%.** One-third of the time spent before writing code — but that's exactly why the other two-thirds had virtually zero rework.

### Case 2: Payment Checkout — 11 Issues Found Before Any Code

A developer used the full stack for a payment checkout demo (React + FastAPI + MySQL). After OpenSpec generated specs, Superpowers' brainstorming reviewed them from three perspectives (architect, QA, developer) and found **11 issues before writing a single line of code**:

- **Critical**: Missing order lookup endpoint, no API parameter validation
- **Medium**: Incomplete dependencies, missing database indexes
- **Low**: Unclear demo mode scope, missing test data steps

Catching these before coding reduced fix costs by an estimated 5-10x. Tasks expanded from 50+ to 74, and core functionality reached 100% completion.

**Key insight**: The value isn't just "AI writes code for you" — it's "AI finds problems you hadn't thought of before you start coding." Pure Claude Code can't do this because it starts coding immediately without multi-perspective requirement review.

## Layer 6: Knowing When NOT to Use It

![Decision matrix for choosing the right tool combination](01-decision-matrix.webp)

**Not every project needs the full stack.** Over-engineering is just as harmful as under-engineering.

| Scenario | Recommended Combo | Reasoning |
|----------|------------------|-----------|
| Quick prototype (<2h) | Claude Code only | Requirements aren't settled; specs waste time |
| Individual medium feature (2-8h) | Claude Code + Superpowers | TDD and Worktree prevent disasters; no decision auditing needed |
| Team medium feature (4-16h) | Full stack | Team needs spec alignment and decision trails |
| Large project / parallel features | Full stack + parallel Worktrees | OpenSpec supports concurrent changes |
| One-off scripts | Claude Code only | No maintenance needs |
| Learning / teaching | Full stack | The workflow itself is the curriculum |

**Start with Claude Code + Superpowers, not the full triple.** Superpowers' TDD and Code Review add value to any project. Add OpenSpec when "decision traceability" becomes a real bottleneck — you'll naturally understand its value at that point.

### Five Common Pitfalls

**Pitfall 1: Specs that are actually pseudocode.** Specs describe behavior (GIVEN/WHEN/THEN), not implementation. Over-detailed specs constrain AI's choices and are expensive to maintain.

**Pitfall 2: Forgetting to archive.** I've done this. Finished a feature, skipped `/opsx:archive`. Next session, AI read the old spec and reimplemented existing functionality. **Rule: archive is always the last action.**

**Pitfall 3: Skipping brainstorming.** Not small talk — it aligns you and AI on technical decisions. Skip it and AI guesses your tech choices. You discover the mismatch during code review, when change costs are high.

**Pitfall 4: Confirming plans without reading them.** 5 minutes reading `tasks.md` saves 1-2 hours of rework. Check task ordering, missing tasks, acceptance criteria clarity.

**Pitfall 5: Full pipeline for 30-minute tasks.** The complete propose→archive cycle can take 2 hours. Tools serve goals, not the other way around.

## Quick Reference

### Command Cheat Sheet

**Core Profile (default)**:

| Stage | Command | Purpose |
|-------|---------|---------|
| Explore | `/opsx:explore` | Enter explore mode — think through ideas with AI |
| Requirements | `/opsx:propose <feature>` | Generate proposal + spec + design + tasks |
| Implement | `/opsx:apply` | Implement code task-by-task from spec |
| Archive | `/opsx:archive` | Merge Delta Spec, archive change |

Simplest flow: **propose → apply → archive**. Use explore as needed.

> **Note**: Commands like `/opsx:ff`, `/opsx:refine`, `/opsx:validate`, `/opsx:verify`, `/opsx:continue`, `/opsx:sync` are **not in the default core profile**. To enable them, run `openspec config profile` to switch to the expanded profile, then `openspec update` to install the additional skill files. For most workflows, the four core commands are sufficient. To modify generated artifacts (proposal.md, design.md, tasks.md), simply edit the files directly.

### Beginner Roadmap

```
Week 1: Claude Code only
  → Get comfortable with AI collaboration in the terminal

Week 2: Add Superpowers
  → Experience TDD, Code Review, Worktree isolation
  → Feel the difference between disciplined and undisciplined AI

Week 3+: Add OpenSpec when needed
  → When "I keep re-explaining requirements" or "teammates can't follow my logic"
  → That's when OpenSpec earns its overhead
```

## Final Take

The essence of this combination is **encoding human engineering best practices (requirements alignment, TDD, code review, decision recording) into rules AI must follow.** Not letting AI freestyle — making AI create within constraints.

Three things to remember:

1. **Start small.** Claude Code → add Superpowers → add OpenSpec when needed. Don't go all-in on day one.
2. **Tools don't replace judgment.** You still need to read, review, and evaluate AI-generated code. Tools amplify efficiency, not capability.
3. **Don't let process become a cage.** 30-minute tasks don't need the full pipeline. Quick prototypes don't need specs. Choosing the right combination — that's real engineering maturity.

The ultimate goal isn't "get AI to write more code" — it's **making AI-generated code as reliable, maintainable, and traceable as code written by a disciplined human engineer.** Whether that's worth the tooling investment depends on your project scale and team needs. Now you have both the decision framework and the hands-on path to get started.

---

**Related Reading:**

- [Superpowers Deep Dive: The Skills Framework That Turns Claude Code into a Senior Engineer](/posts/ai/2026-02-01-superpowers-deep-dive/)
- [The Ultimate CLAUDE.md Guide: Training Your AI Assistant to Be Your Ideal Colleague](/posts/ai/2026-02-28-claude-code-claudemd-guide/)
- [Harness Engineering: Dramatically Improve AI Agent Performance Without Changing the Model](/posts/ai/2026-03-30-harness-engineering-guide/)
- [Claude Code Complete Guide: From Beginner to Expert](/posts/ai/2026-02-28-claude-code-complete-guide/)
