+++
date = '2026-02-20T12:00:00+08:00'
draft = false
title = 'Claude Code Worktree: Run Multiple AI Tasks in One Repo'
description = 'Learn how to use Claude Code --worktree (-w) mode to run parallel AI coding sessions in isolated directories. Covers setup, auto-cleanup, best practices, and real-world workflows.'
toc = true
tags = ['Claude Code', 'Git Worktree', 'AI Coding', 'Developer Productivity']
categories = ['AI Guides']
keywords = ['Claude Code worktree', 'Claude Code parallel development', 'git worktree AI coding', 'claude code -w flag', 'parallel AI coding sessions']

[[params.faqItems]]
question = "What does Claude Code --worktree (-w) mode do?"
answer = "It creates an isolated Git worktree directory and launches a new Claude Code session inside it with a single command (claude -w <name>). This lets you run multiple AI coding tasks in parallel within the same repository without file conflicts."

[[params.faqItems]]
question = "Where are Claude Code worktrees stored?"
answer = "All worktrees created via claude -w are stored under <repo-root>/.claude/worktrees/<name>/. You should add .claude/worktrees/ to your .gitignore to keep them out of version control."

[[params.faqItems]]
question = "Does Claude Code automatically clean up worktrees?"
answer = "Yes. If no changes were made during the session, the worktree and its branch are automatically deleted on exit. If uncommitted changes or new commits exist, Claude prompts you to keep or delete the worktree."

[[params.faqItems]]
question = "Can two Git worktrees use the same branch?"
answer = "No. Git does not allow two worktrees to check out the same branch simultaneously. That is why claude -w <name> automatically creates a new branch named worktree-<name>."

[[params.faqItems]]
question = "What is the difference between Git worktree and git clone?"
answer = "Worktrees share the same .git repository, so creation is faster and there is no re-downloading of code. A clone creates a fully independent repository copy, which is better when you need complete isolation such as different remote configurations."
+++

Have you ever run into these situations?

- Claude is halfway through a feature when an urgent production bug comes in. You have to `git stash` your half-done work or force-commit a messy WIP.
- You want Claude to work on two things at once -- one building a new feature, the other writing tests -- but both sessions edit the same files and create conflicts.
- You want to try a risky refactor but worry about messing up your working directory beyond recovery.

The root cause is simple: **one working directory can only support one in-progress task**. Switching branches isolates Git history, but the file system is shared. Two Claude sessions operating on the same directory will inevitably step on each other.

Claude Code's `--worktree` (shorthand `-w`) mode solves this problem. It integrates Git worktree functionality directly into Claude Code, letting you spin up an isolated working directory and a new Claude session with a single command.

## Git Worktree Basics: One Repo, Multiple Working Directories

Before diving into Claude Code's worktree mode, let's quickly cover how Git worktree works. If you're already familiar, skip to the next section.

### The Problem with Traditional Workflows

Normally, one Git repo maps to one working directory. When you need to switch between branches:

```bash
# Working on feature-a, suddenly need to fix a bug
git stash                    # Save current work
git checkout hotfix-branch   # Switch to hotfix
# ... fix the bug ...
git checkout feature-a       # Switch back
git stash pop                # Restore saved work
```

This workflow has several problems: you might forget to `git stash pop`, switching branches can invalidate `node_modules` and require reinstalling dependencies, and you can only work on one thing at a time.

### How Git Worktree Solves It

Git worktree lets you check out multiple working directories from the same repository. Each directory has its own branch, but they all share the underlying `.git` repository data:

```bash
# Create a new working directory alongside the current repo
git worktree add ../project-hotfix -b hotfix-branch

# Now you have two directories, each independent
# /project/           -> feature-a branch
# /project-hotfix/    -> hotfix-branch branch
```

Each directory has its own independent file state. You can write code in one while running tests in the other -- no stashing, no branch switching.

### Quick Reference

| Command | Purpose |
|---------|---------|
| `git worktree add <path> -b <branch>` | Create worktree with a new branch |
| `git worktree add <path> <existing-branch>` | Create worktree from existing branch |
| `git worktree list` | List all worktrees |
| `git worktree remove <path>` | Remove a worktree |

With this foundation, Claude Code's worktree mode is straightforward -- it automates these operations and adds session management on top.

## Claude Code --worktree Mode Explained

### Basic Usage

The simplest approach is to give your worktree a name:

```bash
# Create a worktree named "feature-auth" and launch Claude
claude -w feature-auth
```

This command does three things:

1. Creates a new working directory at `<repo-root>/.claude/worktrees/feature-auth/`
2. Creates a new branch called `worktree-feature-auth` from the default remote branch (usually `main`)
3. Launches a Claude Code session inside this isolated directory

If you don't want to choose a name, let Claude generate one automatically:

```bash
# Auto-generates a random name like "bright-running-fox"
claude -w
```

### Creating a Worktree from Within a Session

You can also ask Claude to create a worktree from an active session using natural language:

```
> Start a worktree for this task
> Work on this feature in a new worktree
```

Claude handles the worktree creation and switches to the isolated environment automatically.

### Directory Structure

All worktrees created via `claude -w` are stored in a consistent location:

```
my-project/
├── .claude/
│   └── worktrees/
│       ├── feature-auth/      # worktree: feature-auth
│       │   ├── src/
│       │   ├── package.json
│       │   └── ...            # Full copy of project files
│       └── bugfix-123/        # worktree: bugfix-123
│           ├── src/
│           ├── package.json
│           └── ...
├── src/                       # Main working directory
├── package.json
└── ...
```

Add this rule to your `.gitignore` to keep worktree contents out of `git status`:

```gitignore
.claude/worktrees/
```

### Automatic Cleanup

When you exit a worktree session, Claude Code decides what to do based on whether changes exist:

- **No changes made**: Automatically deletes the worktree and its branch. Clean and simple.
- **Uncommitted changes or new commits exist**: Claude prompts you to keep or delete. Keeping preserves the directory and branch for later `--resume`. Deleting removes everything, including uncommitted changes and commits.

This design is sensible -- throwaway experiments get automatically recycled, while meaningful work is never accidentally lost.

### Manual Worktree Management

For finer control -- such as placing worktrees outside the repo or checking out an existing remote branch -- use native Git commands:

```bash
# Create worktree outside the repo
git worktree add ../project-feature-a -b feature-a

# Check out an existing remote branch
git worktree add ../project-bugfix bugfix-123

# Enter the worktree and launch Claude
cd ../project-feature-a && claude

# Clean up when done
git worktree remove ../project-feature-a
```

## Real-World Scenarios

### Scenario 1: Parallel Feature Development

This is the most common use case. You have two independent tasks and want Claude working on both simultaneously:

```bash
# Terminal 1: Claude builds the auth module
claude -w feature-auth
> Implement OAuth2 login, referencing the existing auth module

# Terminal 2: Claude optimizes database queries
claude -w optimize-queries
> Analyze and fix N+1 query issues in src/db/queries.ts
```

Both Claude sessions work in isolated file systems. They cannot see each other's changes, eliminating code conflicts entirely.

### Scenario 2: Experimental Refactoring

Want to try an aggressive architectural change without risking your main codebase?

```bash
# Experiment boldly in a worktree
claude -w experiment-new-arch
> Refactor the current MVC architecture to event-driven, starting with the order module
```

If the experiment succeeds, merge the changes back. If it fails, choose to delete on exit and everything reverts. Your main working directory stays untouched throughout.

### Scenario 3: Code Review and Fixes

Need to review a PR without interrupting your current work?

```bash
# Review and fix in a worktree
claude -w review-pr-456
> Review PR #456 changes, check for security issues and performance concerns

# Continue your current development in the main directory
```

### Scenario 4: Multi-Instance Collaboration

Some teams use a "planner + executor" dual-Claude pattern:

- **Claude A** (main directory): Analyzes code, designs solutions, breaks down tasks
- **Claude B** (worktree): Implements the actual code changes

The planner reads code and produces plans in the main directory while the executor writes code in the worktree. Their contexts are completely isolated, preventing any cross-contamination. For more on multi-agent patterns, see [Claude Multi-Agent Collaboration](/posts/ai/2026-01-13-claude-cowork/).

## Tips and Best Practices

### Use Descriptive Names

Give worktrees meaningful names so they're easy to identify in the `/resume` session list:

```bash
# Good names: immediately clear what the task is
claude -w feat-oauth-login
claude -w fix-memory-leak
claude -w refactor-db-layer

# Bad names
claude -w test1
claude -w tmp
```

### Install Dependencies

New worktrees contain all Git-tracked project files, but untracked items like `node_modules` or virtual environments need to be reinstalled:

```bash
# After launching a worktree, have Claude install dependencies first
> Run npm install before starting development
```

Or add a rule in your CLAUDE.md:

```markdown
## Worktree Rules
- Run `npm install` before starting work in a new worktree
```

### Handle Environment Variables

`.env` files are typically in `.gitignore`, so new worktrees won't include them. Two solutions:

**Option A**: Copy manually

```bash
cp .env .claude/worktrees/feature-auth/.env
```

**Option B**: Tell Claude at session start

```
> Copy the .env file from the root directory to the current directory, then start working
```

### Clean Up Regularly

Make it a habit to clean up finished worktrees. Accumulated worktrees waste disk space and clutter `git worktree list` output:

```bash
# View all current worktrees
git worktree list

# Manually remove unused worktrees
git worktree remove .claude/worktrees/old-feature
```

### Combine with --resume

Worktree Claude sessions support `/resume` and `--resume` just like regular sessions. The session selector shows all sessions across worktrees in the same Git repo, making it easy to switch between tasks.

## Worktree Mode vs Branch Switching

| Dimension | Worktree Mode | Branch Switching |
|-----------|--------------|-----------------|
| **File isolation** | Each task has its own file system | Shared files, overwritten on switch |
| **Parallelism** | Multiple Claude sessions simultaneously | One branch at a time |
| **Dependency install** | Each worktree needs its own install | May need reinstall if deps differ |
| **Disk usage** | Each worktree uses file space | Single copy |
| **Context isolation** | Claude sessions fully independent | Sessions may read other task's changes |
| **Cleanup cost** | Auto-cleanup or one-click delete | Manual stash / commit management |
| **Best for** | Parallel tasks, experiments, AI-assisted dev | Simple sequential development |
| **Learning curve** | Need to understand worktree concept | Basic Git, nearly zero |

**Bottom line**: If you process tasks sequentially (finish one, start the next), branch switching is fine. If you want multiple Claude sessions working simultaneously or need risk-free experimentation, worktree mode is the better choice.

## Case Study: How Teams Use Worktree to Ship Faster

The incident.io team shared their experience using Claude Code with Git worktrees:

- **Dramatic efficiency gains**: A JavaScript editor enhancement estimated at 2 hours took just 10 minutes with parallel worktree development
- **4-5 parallel Claude instances**: Team members routinely run 4-5 Claude sessions, each in its own worktree
- **Combined with Plan Mode**: Reviewing plans before execution makes parallel development safer and more predictable
- **Gradual adoption**: The team went from experimental usage to full adoption over about four months

They wrapped the workflow in a simple bash function `w` to lower the barrier even further:

```bash
# One command: create worktree + launch Claude
w myproject new-feature claude
```

This case demonstrates that worktree mode works well not just for solo developers but also in team settings.

## FAQ

### Q1: What's the difference between worktree and git clone?

Worktrees share the same `.git` repository, so there's no re-downloading of code. Creation is faster and branch operations are more direct. A clone creates a fully independent repository copy, which is better when you need complete isolation (e.g., different remote configurations).

### Q2: Can I commit from inside a worktree?

Yes. Commits in a worktree work exactly like commits in the main directory -- they appear in the same repository's Git history. You can commit, push, and create PRs from a worktree.

### Q3: Can two worktrees be on the same branch?

No. Git does not allow two worktrees to check out the same branch simultaneously. This is why `claude -w feature-auth` automatically creates a new branch named `worktree-feature-auth`.

### Q4: How do I merge worktree changes back to main?

The same way as any branch -- via merge or rebase:

```bash
# From the main directory
git merge worktree-feature-auth
# Or create a PR
```

### Q5: How much disk space do worktrees use?

Worktrees copy only working files, not the `.git` directory (all worktrees share the same one). Actual usage roughly equals the size of your source code. However, running `npm install` in each worktree adds dependency directory space on top.

### Q6: Does the worktree persist after exiting Claude?

It depends on whether changes were made. No changes means automatic cleanup; with changes, Claude asks whether to keep or delete. For manual cleanup, use `git worktree remove <path>`.

### Q7: Does it work with Hooks?

Yes. Hook configurations apply to worktree Claude sessions as well. For example, if you configured auto-formatting or file protection rules in your [Hooks setup](/posts/ai/2026-02-18-claude-code-hooks-guide/), those rules execute automatically in worktree sessions too.

## Summary

Claude Code's `--worktree` mode seamlessly combines Git worktree isolation with AI-powered coding workflows. The core value in one sentence: **safely run multiple parallel AI tasks within a single repository**.

Key takeaways:

1. **`claude -w <name>`** -- one command to create a worktree and launch Claude
2. Worktrees live under `.claude/worktrees/` -- add this to `.gitignore`
3. Unchanged worktrees are automatically cleaned up on exit; changed ones prompt you to decide
4. Ideal for parallel development, experimental changes, code review, and any scenario requiring isolation
5. Use `git worktree add/remove` for manual control when you need finer-grained management

If you're still working with a single terminal, a single directory, and a single Claude session in sequence, give worktree mode a try. Once you see two or three Claude instances making progress on different tasks simultaneously, there's no going back.

---

**Related reading**:

- [Claude Code Hooks Guide](/posts/ai/2026-02-18-claude-code-hooks-guide/) -- Automate guardrails with Hooks
- [Claude Code vs Codex CLI](/posts/ai/2026-02-19-claude-code-vs-codex/) -- In-depth comparison of two AI coding tools
- [Claude Multi-Agent Collaboration](/posts/ai/2026-01-13-claude-cowork/) -- Patterns for running multiple Claude instances
- [Claude Code Browser Automation](/posts/ai/2026-01-28-claude-code-browser-automation/) -- Drive browser testing with Claude Code
