+++
date = '2026-02-28T10:00:00+08:00'
draft = false
title = 'Claude Code Worktree: Run Multiple AI Tasks in Parallel'
description = 'Run multiple Claude Code sessions simultaneously with Git worktree mode. Parallel development, auto-cleanup, and team workflows.'
toc = true
tags = ['Claude Code', 'Git Worktree', 'Productivity', 'Parallel Development']
categories = ['AI Guides']
keywords = ['Claude Code worktree', 'Claude Code parallel development', 'git worktree', 'Claude Code -w', 'run multiple Claude sessions', 'Claude Code productivity']
+++

![Claude Code worktree mode running multiple parallel AI coding sessions](cover.webp)

You open your terminal. Claude Code is halfway through building a new authentication module. Then Slack pings: there's a production bug that needs fixing now.

What do you do? Stash your half-finished changes and hope you remember to pop them later? Force-commit a broken state just to switch branches? Tell your team to wait?

This is the fundamental constraint of single-directory development: **one working directory can only hold one task at a time**. Switching branches changes your files, but it doesn't give you isolation. If two Claude Code sessions operate on the same directory, they will step on each other's changes.

[Claude Code's](https://docs.anthropic.com/en/docs/claude-code) `--worktree` flag (short: `-w`) solves this. It combines Git worktree's isolation with Claude Code's AI workflow, letting you spin up independent coding sessions in seconds -- each with its own directory, its own branch, and zero interference with your other work.

This guide covers everything: Git worktree fundamentals, Claude Code's worktree mode, auto-cleanup behavior, practical scenarios, best practices, and a real team case study.

## Git Worktree Basics: One Repository, Multiple Directories

Before diving into Claude Code's worktree mode, let's make sure you understand the Git feature it's built on. If you already know Git worktrees, skip to the next section.

### The Problem with Branch Switching

In a standard Git workflow, one repository means one working directory. When you need to switch context:

```bash
# You're on feature-a, but need to fix a production bug
git stash                    # Save current work
git checkout hotfix-branch   # Switch to hotfix
# ... fix the bug ...
git checkout feature-a       # Switch back
git stash pop                # Restore your work
```

This works, but it has real costs:

- **Stash accidents**: Forgetting to `git stash pop` is common. Stashed changes can sit for weeks, growing stale.
- **Dependency reinstalls**: Switching branches may change `package.json` or `requirements.txt`, triggering slow reinstalls of `node_modules` or virtual environments.
- **No parallelism**: You can only work on one thing at a time. The other task is frozen until you switch back.
- **Context pollution**: If you're running Claude Code in a directory and switch branches mid-session, the AI's understanding of the codebase instantly becomes wrong.

### How Git Worktree Solves This

[Git worktree](https://git-scm.com/docs/git-worktree) lets you check out multiple branches from the same repository into separate directories. Each directory has its own independent file state, but they all share the same `.git` data underneath:

```bash
# Create a new working directory for a hotfix
git worktree add ../project-hotfix -b hotfix-branch

# Now you have two directories, each on a different branch
# /project/           -> feature-a branch (your original)
# /project-hotfix/    -> hotfix-branch (new worktree)
```

Both directories are fully functional. You can edit files, run tests, build, and commit in either one -- simultaneously, if you want. Changes in one directory don't affect the other.

### Core Git Worktree Commands

| Command | What It Does |
|---------|-------------|
| `git worktree add <path> -b <branch>` | Create a worktree with a new branch |
| `git worktree add <path> <existing-branch>` | Create a worktree from an existing branch |
| `git worktree list` | List all worktrees for the repo |
| `git worktree remove <path>` | Delete a worktree and its directory |

**Key constraint**: Git does not allow two worktrees to check out the same branch simultaneously. Each worktree must be on a unique branch.

With this foundation, Claude Code's worktree mode is straightforward -- it automates all of the above and adds session management on top.

## Claude Code --worktree Mode

### Basic Usage

The simplest way to start a worktree session is to give it a name:

```bash
# Create a worktree named "feature-auth" and start Claude Code in it
claude -w feature-auth
```

This single command does three things:

1. Creates a new working directory at `<repo-root>/.claude/worktrees/feature-auth/`
2. Creates a new branch named `worktree-feature-auth` based on the default remote branch (usually `main`)
3. Launches Claude Code inside that isolated directory

If you don't want to think of a name, let Claude generate one:

```bash
# Auto-generates a random name like "bright-running-fox"
claude -w
```

### Creating a Worktree from Inside a Session

You can also ask Claude to create a worktree mid-conversation using natural language:

```
> Start a worktree for this refactoring task
> Work on this in a new worktree called "fix-api-routes"
```

Claude Code will handle the worktree creation and switch to the isolated environment automatically.

### Directory Structure

All worktrees created by `claude -w` live in a consistent location:

```
my-project/
├── .claude/
│   └── worktrees/
│       ├── feature-auth/        # Worktree: feature-auth
│       │   ├── src/
│       │   ├── package.json
│       │   └── ...              # Full copy of project files
│       └── bugfix-memory-leak/  # Worktree: bugfix-memory-leak
│           ├── src/
│           ├── package.json
│           └── ...
├── src/                         # Main working directory
├── package.json
└── ...
```

**Important**: Add `.claude/worktrees/` to your `.gitignore` so worktree files don't show up in `git status`:

```gitignore
# Claude Code worktrees
.claude/worktrees/
```

### Branch Naming Convention

Claude Code follows a predictable pattern for worktree branches:

- Worktree name: `feature-auth`
- Branch name: `worktree-feature-auth`

This makes it easy to identify worktree branches in `git branch` output or in your CI/CD system. The `worktree-` prefix signals that the branch was auto-created and is tied to an isolated session.

## Auto-Cleanup: No Mess Left Behind

One of the best design decisions in Claude Code's worktree mode is its cleanup behavior. When you exit a worktree session, Claude Code checks whether you made any changes:

### No Changes Made

If the worktree has no uncommitted modifications and no new commits, Claude Code **automatically deletes** the worktree directory and its branch. Clean exit, zero cleanup effort.

This is ideal for exploratory sessions: "Let me check something in an isolated environment" -- if you didn't change anything, there's nothing to save.

### Changes Were Made

If the worktree contains uncommitted changes or new commits, Claude Code **prompts you** with a choice:

- **Keep**: The worktree directory and branch stay intact. You can return later using `--resume`.
- **Delete**: Everything is removed -- uncommitted changes, commits, the worktree directory, and the branch.

This two-tier approach means experimental work that didn't pan out gets cleaned up automatically, while valuable changes are preserved by default.

### Manual Cleanup

For worktrees you kept but no longer need:

```bash
# List all worktrees
git worktree list

# Remove a specific worktree
git worktree remove .claude/worktrees/old-feature

# Delete the associated branch too
git branch -d worktree-old-feature
```

## Practical Scenarios

### Scenario 1: Parallel Feature Development

The most common use case. You have two independent tasks and want Claude to work on both simultaneously:

**Terminal 1:**

```bash
claude -w feature-auth
```

```
> Implement OAuth2 login with Google and GitHub providers.
> Follow the existing auth module patterns in src/auth/.
```

**Terminal 2:**

```bash
claude -w optimize-queries
```

```
> Analyze the N+1 query problems in src/db/queries.ts
> and refactor them to use batch loading.
```

Each Claude session operates in its own directory with its own branch. They can't see each other's changes. No conflicts, no interference, no waiting.

When both tasks are done, you merge each worktree branch back into `main` through your normal workflow (pull requests, code review, CI checks).

### Scenario 2: Experimental Refactoring

You want to try a bold architectural change but aren't sure it will work:

```bash
claude -w experiment-event-driven
```

```
> Refactor the order processing module from synchronous MVC
> to an event-driven architecture. Start with the order
> creation flow and see if it simplifies the error handling.
```

If the experiment succeeds: merge the branch. If it fails: exit the session, choose "delete," and everything vanishes. Your main working directory was never touched.

This eliminates the fear of "what if I break something" that prevents developers from attempting worthwhile refactors. The worktree is your sandbox.

### Scenario 3: Code Review Without Context Switching

A pull request lands in your queue while you're deep in a feature. Instead of stashing your work:

```bash
claude -w review-pr-456
```

```
> Review PR #456. Check for security vulnerabilities,
> performance issues, and adherence to our coding standards.
> Suggest specific improvements with code examples.
```

Claude works in an isolated directory. Your current feature development continues uninterrupted in the main directory. When the review is done, exit the worktree session -- if you didn't make code changes, it auto-cleans.

### Scenario 4: Planner + Implementer Dual-Claude Pattern

Some teams use a two-Claude workflow for complex tasks:

- **Claude A** (main directory): Analyzes the codebase, designs the solution, breaks work into tasks
- **Claude B** (worktree): Implements the plan, writes the actual code

```bash
# Terminal 1: Planner in main directory
claude
```

```
> Analyze the payment processing system. I need to add
> support for recurring subscriptions. Design a plan
> with specific files to modify and code changes needed.
```

```bash
# Terminal 2: Implementer in worktree
claude -w implement-subscriptions
```

```
> Implement the recurring subscription feature based on
> the plan in this project. Start with the database schema
> changes, then the API endpoints, then the webhook handlers.
```

The planner has read-only context of the full codebase. The implementer writes code in isolation. Neither session's context is polluted by the other's work. For more on multi-agent collaboration patterns, see our [Claude Code for Teams guide](/posts/ai/2026-02-28-claude-code-teams-guide/).

### Scenario 5: Bug Fix While Feature Is In Progress

The classic interrupt scenario:

```bash
# You're working on a feature in the main directory
# A P0 bug report comes in

# Don't stash. Don't panic. Just:
claude -w hotfix-payment-timeout
```

```
> There's a production bug: payment webhooks are timing out
> after 30 seconds. Investigate the webhook handler in
> src/payments/webhooks.ts and fix the timeout issue.
```

Fix, test, commit, push, create PR -- all without touching your feature branch. When the hotfix is merged and deployed, exit the worktree session and get back to your feature with zero context loss.

## Tips and Best Practices

### Naming Conventions

Use descriptive names that tell you at a glance what each worktree is doing. This matters when you have multiple sessions and need to find the right one in `--resume`:

```bash
# Good: clear purpose at a glance
claude -w feat-oauth-login
claude -w fix-memory-leak
claude -w refactor-db-layer
claude -w spike-graphql-migration

# Bad: meaningless names
claude -w test1
claude -w tmp
claude -w stuff
```

Recommended prefixes:

| Prefix | Use Case |
|--------|----------|
| `feat-` | New feature development |
| `fix-` | Bug fixes |
| `refactor-` | Code restructuring |
| `spike-` | Exploratory investigation |
| `review-` | Code review sessions |
| `test-` | Writing or fixing tests |

### Installing Dependencies in New Worktrees

A new worktree contains all Git-tracked files but not ignored directories like `node_modules/`, `venv/`, or `vendor/`. You need to install dependencies before the code will run:

```bash
# After starting the worktree session, tell Claude to install first
> Run npm install before starting any development work.
```

Or add a rule to your [CLAUDE.md](/posts/ai/2026-02-28-claude-code-claudemd-guide/) so Claude always remembers:

```markdown
## Worktree Rules
- Always run `npm install` (or `pip install -r requirements.txt`)
  before starting work in a new worktree.
```

You can also automate this with [Claude Code hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) -- set up a post-session hook that detects a fresh worktree and runs the install command automatically.

### Handling .env Files

Environment variable files (`.env`, `.env.local`) are typically in `.gitignore`, so they won't exist in a new worktree. Two approaches:

**Option A: Manual copy**

```bash
cp .env .claude/worktrees/feature-auth/.env
```

**Option B: Ask Claude to copy it**

```
> Copy the .env file from the project root to this worktree directory,
> then start working on the feature.
```

**Option C: Symlink** (one-time setup)

```bash
# In the worktree directory
ln -s ../../.env .env
```

For teams, consider keeping a `.env.example` in version control with placeholder values. Claude can copy and populate it in each new worktree.

### Regular Cleanup

Worktrees accumulate over time if you always choose "keep" when exiting. Build a habit of periodic cleanup:

```bash
# See all worktrees
git worktree list

# Remove ones you no longer need
git worktree remove .claude/worktrees/old-experiment

# Prune stale references (worktrees whose directories were manually deleted)
git worktree prune
```

A good rule of thumb: if a worktree hasn't been touched in a week, either merge its changes or delete it.

### Combining with --resume

Worktree sessions work seamlessly with Claude Code's session resume feature. If you kept a worktree and want to continue where you left off:

```bash
claude --resume
```

The session picker shows all sessions from every worktree in the same repository, clearly labeled with their worktree names. Select the one you want, and Claude Code resumes in the correct worktree directory with full conversation history.

This is powerful for multi-day tasks: start a feature in a worktree on Monday, resume it Tuesday with full context, and merge it Wednesday.

## Worktree vs Branch Switching: A Comparison

When should you use a worktree versus just switching branches? Here's how they compare:

| Dimension | Worktree Mode | Branch Switching |
|-----------|--------------|-----------------|
| **File isolation** | Each task has its own directory | All tasks share one directory |
| **Parallel sessions** | Multiple Claude instances simultaneously | One task at a time |
| **Dependency install** | Required per worktree | May be needed if deps differ between branches |
| **Disk usage** | Each worktree copies source files (not `.git`) | Only one copy of files |
| **Context isolation** | Claude sessions are fully independent | Sessions may read other tasks' changes |
| **Cleanup effort** | Auto-cleanup on exit or one command | Manual stash/commit management |
| **Best for** | Multi-task parallelism, experiments, AI workflows | Simple sequential development |
| **Learning curve** | Must understand worktree concept | Basic Git knowledge |

**The decision is simple**: If you work on one task at a time, branch switching is fine. If you want multiple Claude sessions running in parallel, or you want a risk-free sandbox for experiments, use worktree mode.

## Real Team Case Study: incident.io

The team at incident.io shared their experience using Claude Code with Git worktrees, and the results illustrate what parallel AI development looks like in practice.

### The Setup

Team members routinely run **4-5 parallel Claude Code instances**, each operating in its own worktree. The workflow looks like this:

1. Identify the tasks for the session (features, bug fixes, refactors)
2. Spin up a worktree for each task
3. Give each Claude instance clear instructions
4. Monitor progress across terminals
5. Review and merge results

### The Results

One specific example: a JavaScript editor enhancement that was estimated to take **2 hours** of manual development was completed in **10 minutes** using parallel worktrees. The task was decomposed into independent sub-tasks, each assigned to a separate Claude instance, and all ran simultaneously.

### Their Workflow Wrapper

To reduce the friction of creating worktrees and launching Claude, the team built a simple bash wrapper function:

```bash
# Usage: w <project> <task-name> <command>
w myproject new-feature claude
```

This single command creates the worktree, changes to the directory, and launches Claude Code -- reducing the workflow to one line.

### Key Takeaways from Their Experience

- **Plan Mode first**: Before each parallel session, they use Claude's plan mode to review the approach. This prevents wasted effort from Claude going in the wrong direction.
- **Gradual adoption**: The team took about four months to go from experimental use to full adoption. Start small -- try one worktree session alongside your main work -- before going all-in with 4-5 parallel instances.
- **Task decomposition matters**: Parallel worktrees only help when tasks are genuinely independent. If two tasks modify the same files, you'll hit merge conflicts regardless.
- **Code review is essential**: More parallel output means more code to review. The team maintains strict review standards even though the code is AI-generated.

## Frequently Asked Questions

### What's the difference between a worktree and `git clone`?

A worktree shares the same `.git` repository data as your main directory. Creation is nearly instant because it doesn't download anything -- it just checks out files. A clone creates a completely independent repository copy, which takes longer and doesn't share branch or commit data.

Use worktrees for parallel development within the same project. Use clone only when you need fully independent repository configurations (different remotes, different hooks).

### Can I commit and push from a worktree?

Yes. Commits made in a worktree are part of the same repository. You can commit, push, create pull requests, and do everything you would in the main directory. The commits show up in `git log` from any worktree.

### Can two worktrees be on the same branch?

No. Git enforces a rule that each branch can only be checked out in one worktree at a time. This prevents conflicting edits to the same branch from different directories. Claude Code handles this automatically by creating a unique `worktree-<name>` branch for each worktree.

### How do I merge worktree changes back?

The same way you merge any branch:

```bash
# Option 1: Direct merge from your main directory
git merge worktree-feature-auth

# Option 2: Create a pull request (recommended for team workflows)
cd .claude/worktrees/feature-auth
git push -u origin worktree-feature-auth
# Then create a PR through GitHub/GitLab
```

Most teams prefer pull requests because they get the benefit of CI checks and code review.

### How much disk space do worktrees use?

A worktree copies your tracked source files but **not** the `.git` directory (which is shared across all worktrees). So the disk cost is roughly equal to your source code size.

The real space concern is dependencies. If each worktree runs `npm install`, you'll have a separate `node_modules` in each one. For a typical Node.js project, that's 200-500 MB per worktree. Keep this in mind if you're running many parallel sessions.

**Tip**: Tools like [pnpm](https://pnpm.io/) use a content-addressable store that deduplicates packages across projects, significantly reducing disk usage when you have multiple worktrees.

### Do Git hooks work in worktrees?

Yes. Git hooks (pre-commit, pre-push, etc.) work identically in worktrees because they're defined in the shared `.git/hooks` directory. If you use [Claude Code hooks](/posts/ai/2026-02-28-claude-code-hooks-guide/) for automation (auto-formatting, linting, file protection), those also apply in worktree sessions -- the `.claude/` configuration is read from the repository root.

### What happens if I delete a worktree directory manually?

Git will notice the directory is gone. Run `git worktree prune` to clean up the stale reference. The branch associated with the worktree will still exist and can be deleted separately with `git branch -d <branch-name>`.

### Can I use worktrees with monorepos?

Yes, and they work well. Each worktree gets a copy of the entire monorepo, so you can work on different packages simultaneously. The tradeoff is disk space -- large monorepos mean larger worktrees. Consider using sparse checkout if you only need specific packages in a worktree.

## Summary

Claude Code's `--worktree` mode turns Git's worktree feature into a seamless parallel development tool. The core value is simple: **run multiple AI coding sessions simultaneously in the same repository without conflicts**.

Here's what to remember:

1. **`claude -w <name>`** creates an isolated worktree and starts Claude Code in one command
2. Worktrees live in `.claude/worktrees/` -- add this to your `.gitignore`
3. Branches are auto-named `worktree-<name>` for easy identification
4. Auto-cleanup removes empty worktrees; changed worktrees prompt you to keep or delete
5. Install dependencies separately in each worktree (`node_modules`, `venv`, etc.)
6. Combine with `--resume` for multi-day tasks that span sessions
7. Works with Git hooks and Claude Code hooks out of the box

If you're still running a single Claude session in a single directory, working on one task at a time, try this: open two terminals, create two worktrees, and assign two independent tasks. When you see both sessions making progress simultaneously, you'll understand why teams like incident.io run 4-5 parallel instances as their default workflow.

The bottleneck in AI-assisted development is no longer how fast the model thinks. It's how many tasks you can feed it at once. Worktrees remove that bottleneck.

## Related Reading

- [Claude Code Setup Guide 2026](/posts/ai/2026-02-25-claude-code-setup-guide/) -- Install and configure Claude Code from scratch
- [Claude Code for Teams: Multi-Agent Collaboration](/posts/ai/2026-02-28-claude-code-teams-guide/) -- Advanced patterns for running multiple Claude instances
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) -- Automate formatting, linting, and safety checks
- [10 Claude Code Mistakes Beginners Make](/posts/ai/2026-02-25-claude-code-mistakes/) -- Common pitfalls and how to avoid them
