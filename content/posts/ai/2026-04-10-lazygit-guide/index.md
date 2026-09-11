+++
date = '2026-04-10T14:00:00+08:00'
draft = false
title = 'Lazygit in 2026: The Git TUI That Makes Interactive Rebase Feel Like Cheating'
description = 'Lazygit turns painful Git operations like interactive rebase and line-level staging into single-keystroke actions. With 76K stars and 8 years of development, here is why it belongs in every terminal developer workflow.'
toc = true
tags = ['Developer Tools', 'Git', 'Terminal', 'Productivity']
keywords = ['lazygit', 'lazygit tutorial', 'git TUI', 'terminal git client', 'lazygit vs gitui', 'interactive rebase tool', 'lazygit neovim']

[[params.faqItems]]
question = "What is lazygit?"
answer = "Lazygit is an open-source terminal UI for Git that replaces complex Git commands with intuitive keyboard-driven interactions. It has 76K+ GitHub stars and is written in Go."

[[params.faqItems]]
question = "How do I install lazygit?"
answer = "On macOS: brew install lazygit. On Ubuntu: sudo apt install lazygit. On Windows: winget install lazygit. Or download binaries from GitHub releases."

[[params.faqItems]]
question = "Is lazygit better than gitui?"
answer = "Lazygit has deeper functionality (interactive rebase, custom patches, worktrees) and better ecosystem integration (Neovim plugin, custom commands). Gitui is faster on startup and uses less memory. For most developers, lazygit's feature depth outweighs gitui's performance edge."

[[params.faqItems]]
question = "Can lazygit replace GUI Git clients like GitKraken?"
answer = "For terminal-native developers, yes. Lazygit handles staging, rebasing, cherry-picking, and conflict resolution without leaving the terminal. GUI clients still have advantages for large-scale visual diff review and PR management."

[[params.faqItems]]
question = "Does lazygit work with Neovim?"
answer = "Yes. The lazygit.nvim plugin embeds lazygit directly into Neovim as a floating terminal. You can open it with a keybinding, perform all Git operations, and return to your editor seamlessly."
+++

![Lazygit terminal UI for Git commands with interactive rebase and staging](cover.webp)

To perform an interactive rebase in raw Git, you run `git rebase -i HEAD~5`, which opens a temporary TODO file in your editor where you manually rearrange lines, change `pick` to `squash` or `fixup`, save, close, and pray you did not make a typo. To stage individual lines from a file, you run `git add -p`, which walks you through hunks one at a time—and if the hunk granularity is wrong, you edit a patch file by hand. To amend an old commit (not the latest, but one from three commits ago), you need to start an interactive rebase, mark the commit as `edit`, make your changes, amend, and then continue the rebase.

These are not edge cases. These are things I do multiple times a week. And every single time, the experience feels like using a 2005-era text editor to perform surgery.

[Lazygit](https://github.com/jesseduffield/lazygit) fixes this. It wraps Git's powerful-but-painful interface in a terminal UI where interactive rebase is a matter of pressing `i` and then using `s` to squash, `d` to drop, or `ctrl+k`/`ctrl+j` to reorder commits. Line-level staging is pressing `space` on a line. Amending an old commit is `shift+a`. No temporary files, no patch editing, no prayer.

With 76,000+ GitHub stars, 8 years of active development, and a latest release just days ago (v0.61.0, April 6 2026), lazygit is not a weekend project that might disappear. Its sponsors include [DHH](https://github.com/dhh) (creator of Rails) and [Tobias Lütke](https://github.com/tobi) (CEO of Shopify). In my experience, it is the single most impactful terminal tool I have adopted since tmux.

## Why Raw Git Commands Are Not Enough

There is a common misconception among experienced developers: "I know Git well enough, I do not need a TUI." This misses the point entirely. The problem is not understanding Git—it is that Git's interface actively fights you on its most powerful features.

Consider interactive rebase, arguably Git's most powerful feature for maintaining clean history. The raw workflow requires you to: (1) type the rebase command, (2) wait for an editor to open, (3) manually edit text in a TODO file, (4) save and close, (5) resolve any conflicts, (6) continue the rebase. Each step is a context switch. Each step is an opportunity for a typo that sends you into a confusing error state. And if you want to reorder commits, you are literally cutting and pasting lines of text—in 2026.

Lazygit reduces this to a visual operation. You see your commits, you move them with keyboard shortcuts, you confirm. The mental model matches the actual operation: "I want to move this commit above that one" becomes pressing `ctrl+k` instead of thinking about text line positions in a file you will never see again.

This matters because **the frequency of an operation determines whether tool friction is acceptable**. If you rebase once a month, the raw CLI is fine. If you rebase multiple times per week—which you should, if you care about clean history—the accumulated friction is enormous. I estimate lazygit saves me 15-20 minutes per day on Git operations, mostly because I no longer hesitate before doing the right thing (squashing fixup commits, reordering for logical grouping) due to the overhead of the raw CLI workflow.

## The Features That Actually Matter

Lazygit has dozens of features, but only a handful fundamentally change how you work with Git. Here are the ones I use daily and why they matter:

### Line-Level Staging

Press `space` on any line in the diff view to stage just that line. Press `v` to enter visual mode and select a range. Press `a` to select the entire hunk. This is the feature that converted me from `git add -p`—which forces you through hunks sequentially and requires manual patch editing for fine-grained control—to never wanting to go back.

The practical impact: I now commit in much more logical units. Before lazygit, I would often stage entire files because the effort of line-level staging with `git add -p` was not worth it. Now I routinely split a file's changes across 2-3 commits in under a minute, each commit telling a clear story. This is not a minor workflow improvement—it changes the quality of your Git history.

### Interactive Rebase as Direct Manipulation

Press `i` to start an interactive rebase. Then use `s` (squash), `f` (fixup), `d` (drop), `e` (edit), `ctrl+k` (move up), `ctrl+j` (move down) on any commit. When you are done, press `m` and select "continue." That is it. No editor, no TODO file, no text manipulation.

Even more powerful: you can perform any of these as one-off operations without explicitly starting a rebase. Press `s` on a commit to squash it into the previous one. Lazygit handles the interactive rebase in the background. This is the kind of design that makes you wonder why the Git CLI never worked this way.

### Amending Old Commits

Press `shift+a` on any commit to amend it with your currently staged changes. Lazygit runs an interactive rebase behind the scenes, but you never see it. This is transformative for workflows where you realize, two commits later, that you forgot to add a related change. Instead of creating a fixup commit and manually rebasing later, you do it in one keystroke.

### Custom Patches from Old Commits

This is lazygit's most underrated feature. You can enter any old commit, view its files, navigate into the diff, select specific lines to build a custom patch, and then choose what to do with that patch: remove it from the commit, split it into a new commit, apply it in reverse, or move it to another commit. Try doing that with raw Git commands—it involves `git format-patch`, manual patch editing, and `git am`, a workflow so painful that most developers simply never do it.

### Undo/Redo

Press `ctrl+z` to undo the last Git operation. This alone is worth the price of admission (which is free). Fear of irreversible mistakes is one of the biggest friction points in Git, and having a safety net makes you more willing to experiment with rebasing, resetting, and other "dangerous" operations.

## Installation and Key Bindings You Need

### Installation

```bash
# macOS
brew install lazygit

# Ubuntu/Debian
sudo apt install lazygit

# Arch Linux
pacman -S lazygit

# Windows
winget install lazygit

# From source (any platform with Go)
go install github.com/jesseduffield/lazygit@latest
```

After installing, just run `lazygit` (or `lg` if you set up the alias) inside any Git repository.

### Essential Key Bindings

Here is the cheat sheet I wish someone had given me on day one. These 20 bindings cover 90% of daily Git operations:

| Action | Key | Context |
|--------|-----|---------|
| **Stage file** | `space` | Files panel |
| **Stage line** | `space` | Staging view (line) |
| **Stage hunk** | `a` | Staging view |
| **Commit** | `c` | Files panel |
| **Commit with editor** | `C` | Files panel |
| **Amend last commit** | `A` | Files panel |
| **Amend old commit** | `shift+a` | Commits panel |
| **Squash commit** | `s` | Commits panel |
| **Fixup commit** | `f` | Commits panel |
| **Drop commit** | `d` | Commits panel |
| **Move commit up** | `ctrl+k` | Commits panel |
| **Move commit down** | `ctrl+j` | Commits panel |
| **Cherry-pick copy** | `shift+c` | Commits panel |
| **Cherry-pick paste** | `shift+v` | Commits panel |
| **Start interactive rebase** | `i` | Commits panel |
| **Checkout branch** | `space` | Branches panel |
| **New branch** | `n` | Branches panel |
| **Push** | `P` | Any panel |
| **Pull** | `p` | Any panel |
| **Undo** | `ctrl+z` | Any panel |
| **Filter/search** | `/` | Any panel |

The learning curve is real but short. I spent about two days feeling slower than my raw Git workflow, and by day three I was noticeably faster. By week two, I could not imagine going back. The key insight: **do not try to memorize everything at once**. Start with `space` (stage), `c` (commit), `s` (squash), and `ctrl+z` (undo). Add more as needed.

## Lazygit vs The Alternatives: A Decision Framework

The terminal Git TUI space has three real contenders. Here is how to choose:

![Comparison of terminal Git TUI tools: lazygit vs gitui vs tig](01-comparison-git-tui.webp)

| Feature | lazygit (76K ★) | gitui (22K ★) | tig (13K ★) |
|---------|----------------|---------------|-------------|
| **Focus** | Full Git management | Fast Git management | Read-only browsing |
| **Language** | Go | Rust | C |
| **Interactive rebase** | ✅ Full visual rebase | ❌ Limited | ❌ None |
| **Line-level staging** | ✅ Visual selection | ✅ Hunk-level | ❌ Read-only |
| **Custom patches** | ✅ Extract/move patches | ❌ | ❌ |
| **Worktrees** | ✅ Create and manage | ❌ | ❌ |
| **Undo/redo** | ✅ ctrl+z | ❌ | ❌ |
| **Neovim plugin** | ✅ lazygit.nvim | ❌ | ❌ |
| **Custom commands** | ✅ Flexible system | ❌ | ❌ |
| **Startup speed** | Fast | Faster | Fastest |
| **Memory usage** | Moderate | Low | Lowest |

**Choose lazygit if**: you want the deepest Git integration, you use Neovim, or you need interactive rebase, custom patches, and worktree support. This covers most developers.

**Choose gitui if**: you work primarily on very large repositories where startup speed and memory matter, and you do not need interactive rebase or custom patches. Gitui is written in Rust and is noticeably faster on initial load.

**Choose tig if**: you primarily need to browse history, blame, and diffs, not perform write operations. Tig is a viewer, not a manager—complementary to lazygit rather than competing with it.

**Stay with GUI clients (GitKraken/Tower/Fork) if**: you need visual PR review workflows, large-scale diff visualization with side-by-side views, or you are not a terminal-native developer. GUI clients excel at visual comprehension of complex merge situations.

## Lazygit in the AI Coding Era

![Lazygit in the AI coding workflow: AI generates code, lazygit curates commits](02-ai-coding-workflow.webp)

Here is an angle most lazygit articles miss: in 2026, the developer workflow has fundamentally shifted toward AI-assisted coding. Tools like [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), Cursor, and Copilot generate code at a pace that makes Git operations more frequent, not less. When an AI agent makes 15 file changes across a refactor, you need to review, stage selectively, and commit in logical units—fast.

Lazygit fits this workflow perfectly. After Claude Code finishes a multi-file change, I open lazygit to review every file, stage lines selectively, and create well-structured commits. The alternative—running `git diff`, `git add -p`, and `git commit` for each logical unit—takes 3-4x longer.

The [Neovim integration](https://github.com/kdheepak/lazygit.nvim) makes this even more seamless. I have lazygit bound to `<leader>gg` in my Neovim config:

```lua
-- lazy.nvim plugin spec
{
  "kdheepak/lazygit.nvim",
  keys = {
    { "<leader>gg", "<cmd>LazyGit<cr>", desc = "Open LazyGit" },
  },
}
```

One keystroke opens lazygit in a floating window inside Neovim. I review, stage, commit, push—and I am back in my editor without ever leaving the terminal. In a world where AI generates code and humans curate commits, lazygit is the curation tool.

For [Claude Code worktree workflows](/posts/ai/2026-02-28-claude-code-worktree-guide/), lazygit's worktree support (`w` in the branches panel) is particularly valuable. You can create, switch between, and manage worktrees visually—a feature I use daily when running multiple Claude Code sessions on different feature branches.

## When Lazygit Is the Wrong Choice

I want to be direct about the limitations:

**Very large repositories will suffer.** If your repo is massive enough that `git status` takes 10+ seconds (think monorepos like nixpkgs or chromium), lazygit's UI will freeze on every operation because it waits for Git commands to complete before updating panels. There is no way to limit the scope to a subdirectory. For these repos, raw Git commands with sparse checkout are still necessary.

**Git beginners should not start here.** Lazygit abstracts Git operations so well that you can use it without understanding what is happening underneath. This is dangerous. If you do not know what an interactive rebase does at the command level, you will struggle when something goes wrong—and lazygit's undo cannot fix everything. Learn the fundamentals first, then graduate to lazygit.

**Enterprise CI/CD workflows do not benefit.** If your Git interactions are primarily scripted (CI pipelines, automated releases, git hooks), lazygit adds nothing. It is a human-facing tool for human-facing Git operations.

**PR review workflows are limited.** Lazygit does not have GitHub/GitLab PR integration. You cannot review, comment on, or merge pull requests from within lazygit. For that, you still need `gh pr` commands, a GUI client, or the web interface.

## Getting Started Today

If you have read this far and are not already using lazygit, here is what I recommend:

1. **Install it** (`brew install lazygit` on macOS, or your platform's equivalent)
2. **Run it** in a real project (`lazygit` or `lg`)
3. **Learn four keys**: `space` (stage), `c` (commit), `s` (squash), `ctrl+z` (undo)
4. **Use it for one full day** before judging—the first hour will feel slower than your current workflow
5. **Add the Neovim plugin** if you use Neovim—the floating window integration is a game changer

The transition cost is about two days of mild friction. The payoff is thousands of hours of faster, more confident Git operations for the rest of your career. That is a trade I would make every time.

## Related Reading

- [gitui vs lazygit in 2026: Benchmarked on 82K Commits](/posts/ai/2026-09-02-gitui-vs-lazygit/) — startup, memory and feature receipts for the two Git TUIs, plus a decision guide
- [Claude Code Complete Guide: From Setup to Advanced Workflows](/posts/ai/2026-02-28-claude-code-complete-guide/) — the AI coding tool that pairs best with lazygit
- [Claude Code Worktree Guide](/posts/ai/2026-02-28-claude-code-worktree-guide/) — worktree workflows that lazygit makes visual
- [AI Development Workflow: A Practical Guide](/posts/ai/2026-01-19-ai-dev-workflow/) — where lazygit fits in modern development
- [High-Frequency Commits Strategy](/posts/ai/2026-03-10-high-frequency-commits/) — why frequent, clean commits matter
- [tmux Guide for AI Development](/posts/ai/2026-03-03-tmux-guide-ai-development/) — the terminal multiplexer that complements lazygit
