+++
date = '2026-03-03T10:00:00+08:00'
draft = false
title = 'Tmux 完全指南：从入门到 AI 多智能体并行开发工作流'
description = '从零开始掌握 tmux，学会会话管理、窗格分屏、自定义配置，以及如何使用 tmux 运行多个并行 Claude Code 智能体，实现 10 倍开发效率提升。'
toc = true
tags = ['tmux', 'Claude Code', 'AI Workflow', 'Terminal', 'Developer Tools']
categories = ['AI Guides']
keywords = ['tmux 教程', 'tmux 入门指南', 'tmux Claude Code', 'tmux AI 开发', 'tmux 多智能体工作流', 'tmux 并行编码', 'tmux 配置', '终端复用器教程']

[[params.faqItems]]
question = "什么是 tmux，为什么要使用它？"
answer = "Tmux（终端复用器）可以创建持久化的终端会话，即使断开连接也不会丢失。你可以将屏幕分成多个窗格、管理多个窗口，并随时断开/重新连接会话。对于 AI 开发者来说，tmux 是并行运行多个 Claude Code 实例、维持长时间 AI 编程会话的必备工具。"

[[params.faqItems]]
question = "如何将 tmux 与 Claude Code 配合使用？"
answer = "启动一个 tmux 会话，为不同任务分割窗格（Claude Code、日志、测试），利用会话持久化来保持 AI 对话运行。要运行并行智能体，可以创建独立的 tmux 窗口，或使用 Claude Code 内置的 Agent Teams 功能配合分屏显示。这种配置可以同时运行 4-8 个编码智能体。"

[[params.faqItems]]
question = "最重要的 tmux 快捷键有哪些？"
answer = "默认前缀键是 Ctrl+b。必备快捷键：Ctrl+b d（断开）、Ctrl+b %（垂直分屏）、Ctrl+b \"（水平分屏）、Ctrl+b 方向键（切换窗格）、Ctrl+b c（新建窗口）、Ctrl+b n/p（下一个/上一个窗口）、Ctrl+b z（切换窗格全屏）、Ctrl+b [（复制模式）。"

[[params.faqItems]]
question = "可以用 tmux 并行运行多个 AI 编码智能体吗？"
answer = "可以。将 tmux 与 git worktree 结合，可以运行 4-8 个并行 Claude Code 智能体，每个在独立的 tmux 窗口中拥有隔离的代码副本。dmux 和 ntm 等工具可以自动化这个工作流。Claude Code 的实验性 Agent Teams 功能也原生使用 tmux 分屏来实现多智能体协调。"
+++

![用于 AI 开发工作流的 tmux 终端复用器](cover.webp)

如果你在终端工作，大概遇到过这些情况：SSH 连接在长时间运行的任务中断开、在多个终端窗口之间手忙脚乱地调试、或者眼睁睁看着 Claude Code 的对话在笔记本休眠时消失。

**Tmux 能解决所有这些问题** —— 在 AI 驱动的开发时代，它可以说是你最值得学习的终端工具。

本指南将带你从零 tmux 基础到熟练运行并行 AI 编码智能体。无论你是完全的新手，还是希望提升 AI 工作流的资深开发者，都能在这里找到有价值的内容。

## 什么是 Tmux？

Tmux 是 **terminal multiplexer**（终端复用器）的缩写。它的核心功能有三个：

1. **会话持久化** —— 终端会话在断开连接、SSH 掉线、笔记本休眠后依然存活
2. **窗口管理** —— 在单个连接中管理多个终端窗口
3. **窗格分屏** —— 将一个窗口分割成多个区域

可以把它理解为终端的窗口管理器。就像桌面操作系统可以有多个应用窗口一样，tmux 让你在一个连接中拥有多个终端会话。

### 为什么 Tmux 对 AI 开发如此重要

传统的 tmux 优势（会话持久化、多任务处理）与 AI 编码工具结合后会变成**超能力**：

| 传统用途 | AI 驱动用途 |
|---------|-----------|
| 保持 SSH 会话不断 | 保持 Claude Code 对话在断开后不丢失 |
| 分屏看代码和日志 | 一个窗格 Claude Code，一个跑测试，一个看日志 |
| 运行后台进程 | 并行运行多个 AI 智能体 |
| 远程开发 | 随时随地（甚至用手机）访问完整的 AI 开发环境 |

tmux + Claude Code 的组合已经成为认真对待 AI 辅助开发的标准配置。让我们从基础开始。

### 如何检查是否在 Tmux 中

不确定自己是否已经在 tmux 会话中？检查 `$TMUX` 环境变量：

```bash
echo $TMUX
# 如果有输出 → 你在 tmux 中
# 如果输出为空 → 你在普通终端中
```

## 安装

**macOS**（推荐使用 Homebrew）：

```bash
brew install tmux
```

**Ubuntu / Debian**：

```bash
sudo apt-get install tmux
```

**CentOS / Fedora**：

```bash
sudo yum install tmux
```

**验证安装**：

```bash
tmux -V
# tmux 3.5a
```

## 核心概念：会话、窗口和窗格

在学习命令之前，先理解三层层级结构：

```
tmux server（服务器）
└── Session（会话：一个命名的工作空间）
    ├── Window 0（窗口：类似浏览器标签页）
    │   ├── Pane 0（窗格：上半部分）
    │   └── Pane 1（窗格：下半部分）
    ├── Window 1
    │   └── Pane 0（完整窗口）
    └── Window 2
        ├── Pane 0（左侧）
        ├── Pane 1（右上）
        └── Pane 2（右下）
```

- **会话（Session）**：窗口的集合。你可以从会话中断开，稍后重新连接——一切继续运行。
- **窗口（Window）**：会话中的一个全屏终端。类似浏览器标签页。
- **窗格（Pane）**：窗口的子分区。类似 IDE 中的分屏视图。

### 前缀键

所有 tmux 快捷键都以**前缀键**开头——默认是 `Ctrl+b`。操作流程是：

1. 按下 `Ctrl+b`
2. 松开两个键
3. 按下命令键

例如，要断开：按 `Ctrl+b`，松开，然后按 `d`。

> 很多用户会把前缀键重映射为 `Ctrl+a`（更靠近主键区）。我们会在配置部分介绍这个。

## 会话管理

会话是 tmux 的基础。先掌握这些。

### 创建和命名会话

```bash
# 启动一个未命名的会话
tmux

# 启动一个命名会话（推荐）
tmux new -s dev

# 在指定目录启动命名会话
tmux new -s myproject -c ~/projects/myproject
```

务必给会话命名。当你有 5 个以上的会话时，`tmux ls` 显示 `0:`、`1:`、`2:` 毫无用处。而 `dev`、`claude`、`deploy` 这样的命名让一切一目了然。

### 断开和重新连接

这是 tmux 的杀手级功能。断开会话后，**一切继续运行**。

```bash
# 从当前会话断开
# 快捷键：Ctrl+b d
tmux detach

# 列出所有会话
tmux ls

# 重新连接到命名会话
tmux attach -t dev
tmux a -t dev  # 简写

# 重新连接到最近的会话
tmux attach
```

**实际场景**：你启动了 Claude Code 会话，正在深入讨论重构认证系统，然后需要合上笔记本去开会。只需 `Ctrl+b d` 断开。会后 `tmux attach -t claude` 就能回到之前的状态——对话历史、运行中的进程，一切完好。

### 会话快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+b d` | 断开会话 |
| `Ctrl+b s` | 列出并切换会话 |
| `Ctrl+b $` | 重命名当前会话 |
| `Ctrl+b (` | 切换到上一个会话 |
| `Ctrl+b )` | 切换到下一个会话 |

### 其他会话命令

```bash
# 终止指定会话
tmux kill-session -t dev

# 终止除当前外的所有会话
tmux kill-session -a

# 终止整个 tmux 服务器（所有会话）
tmux kill-server

# 重命名会话
tmux rename-session -t old-name new-name

# 切换到另一个会话（在 tmux 内部）
tmux switch -t other-session
```

## 窗口管理

窗口就像会话中的标签页。

### 创建和导航窗口

```bash
# 创建新窗口
# 快捷键：Ctrl+b c
tmux new-window

# 创建命名窗口
tmux new-window -n tests

# 重命名当前窗口
# 快捷键：Ctrl+b ,
tmux rename-window editor
```

### 窗口快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+b c` | 创建新窗口 |
| `Ctrl+b ,` | 重命名当前窗口 |
| `Ctrl+b n` | 下一个窗口 |
| `Ctrl+b p` | 上一个窗口 |
| `Ctrl+b 0-9` | 按编号切换窗口 |
| `Ctrl+b w` | 列出所有窗口（交互式选择器） |
| `Ctrl+b &` | 关闭当前窗口（需确认） |

底部状态栏显示所有窗口，当前活动窗口用 `*` 标记。

## 窗格管理

窗格让你同时看到多个终端——这是 tmux 真正闪光的地方。

### 分割窗格

```bash
# 垂直分割（左 | 右）
# 快捷键：Ctrl+b %
tmux split-window -h

# 水平分割（上 / 下）
# 快捷键：Ctrl+b "
tmux split-window -v
```

### 导航窗格

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+b ←↑↓→` | 向该方向移动到窗格 |
| `Ctrl+b o` | 循环切换窗格 |
| `Ctrl+b q` | 显示窗格编号（按数字切换） |
| `Ctrl+b z` | 切换全屏（当前窗格最大化） |
| `Ctrl+b x` | 关闭当前窗格（或直接输入 `exit`） |
| `Ctrl+b {` | 与上一个窗格交换 |
| `Ctrl+b }` | 与下一个窗格交换 |
| `Ctrl+b Space` | 循环切换窗格布局 |

### 调整窗格大小

按下前缀 `Ctrl+b`，松开，然后按住 `Ctrl` 并按方向键：

```
Ctrl+b Ctrl+←  # 向左缩小
Ctrl+b Ctrl+→  # 向右扩大
Ctrl+b Ctrl+↑  # 向上缩小
Ctrl+b Ctrl+↓  # 向下扩大
```

或者使用命令行精确控制：

```bash
# 调整当前窗格大小（单位为单元格）
tmux resize-pane -D 10  # 向下 10 行
tmux resize-pane -U 5   # 向上 5 行
tmux resize-pane -L 20  # 向左 20 列
tmux resize-pane -R 20  # 向右 20 列
```

## 复制模式和滚动

默认情况下你无法在 tmux 中向上滚动。需要进入**复制模式**：

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+b [` | 进入复制模式 |
| `q` | 退出复制模式 |
| `↑↓` 或 `PgUp/PgDn` | 滚动 |
| `Space` | 开始选择（复制模式中） |
| `Enter` | 复制选择内容并退出（复制模式中） |
| `Ctrl+b ]` | 粘贴已复制的文本 |

在复制模式中，如果设置了 `setw -g mode-keys vi`，可以使用 vim 风格的导航（`h`、`j`、`k`、`l`、`Ctrl+u`、`Ctrl+d`）。

## 配置：~/.tmux.conf 文件

tmux 的默认设置可用但不够优化。创建 `~/.tmux.conf` 来自定义你的体验。

### 入门配置

```bash
# ~/.tmux.conf — 为 AI 开发优化

# ============================================
# 通用设置
# ============================================

# 将前缀键从 Ctrl+b 改为 Ctrl+a（更方便按到）
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# 窗口编号从 1 开始（而不是 0）
set -g base-index 1
setw -g pane-base-index 1

# 关闭窗口时重新编号
set -g renumber-windows on

# 增大滚动缓冲区（对 Claude Code 输出很重要）
set -g history-limit 50000

# 启用鼠标支持
set -g mouse on

# 减少转义时间（更快的按键响应）
set -sg escape-time 10

# 启用焦点事件（用于 vim/neovim 集成）
set -g focus-events on

# ============================================
# 显示设置
# ============================================

# 启用 256 色和真彩色支持
set -g default-terminal "screen-256color"
set-option -ga terminal-overrides ",xterm-256color:Tc"

# 设置状态栏更新间隔
set -g status-interval 5

# ============================================
# 键位绑定
# ============================================

# 直观的分屏快捷键
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# 新窗口继承当前路径
bind c new-window -c "#{pane_current_path}"

# Vim 风格的窗格导航
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Shift+方向键调整窗格大小
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# 快速重载配置
bind r source-file ~/.tmux.conf \; display "配置已重载！"

# 启用 vi 模式复制
setw -g mode-keys vi

# Vi 风格的复制绑定
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-selection-and-cancel
```

保存后重载：

```bash
tmux source-file ~/.tmux.conf
```

或者在 tmux 中：按 `Ctrl+a r`（使用上述配置时）。

### 键位绑定说明

使用上述配置后，你的操作流程变为：

| 操作 | 默认 | 自定义 |
|------|------|--------|
| 前缀键 | `Ctrl+b` | `Ctrl+a` |
| 垂直分屏 | `Ctrl+b %` | `Ctrl+a |` |
| 水平分屏 | `Ctrl+b "` | `Ctrl+a -` |
| 切换窗格 | `Ctrl+b 方向键` | `Ctrl+a h/j/k/l` |
| 调整窗格 | `Ctrl+b Ctrl+方向键` | `Ctrl+a H/J/K/L` |

## 必备插件

[TPM（Tmux Plugin Manager）](https://github.com/tmux-plugins/tpm) 让插件管理变得简单。

### 安装 TPM

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

添加到你的 `~/.tmux.conf`：

```bash
# 插件管理器
set -g @plugin 'tmux-plugins/tpm'

# 推荐插件
set -g @plugin 'tmux-plugins/tmux-sensible'      # 合理的默认设置
set -g @plugin 'tmux-plugins/tmux-resurrect'      # 保存/恢复会话
set -g @plugin 'tmux-plugins/tmux-continuum'      # 自动保存会话
set -g @plugin 'tmux-plugins/tmux-yank'           # 系统剪贴板集成

# 每 15 分钟自动保存
set -g @continuum-save-interval '15'

# tmux 启动时自动恢复
set -g @continuum-restore 'on'

# 初始化 TPM（保持在底部）
run '~/.tmux/plugins/tpm/tpm'
```

安装插件：在 tmux 中按 `Ctrl+a I`（大写 I）。

### AI 开发必备插件

| 插件 | 用途 |
|------|------|
| **tmux-resurrect** | 保存和恢复完整的 tmux 环境（会话、窗口、窗格，甚至运行中的程序） |
| **tmux-continuum** | 自动保存。你的 AI 会话能在系统重启后存活 |
| **tmux-yank** | 复制到系统剪贴板。复制 Claude Code 输出时必不可少 |
| **tmux-sensible** | 每个 tmux 用户都应该有的通用默认设置 |

## Tmux + Claude Code：AI 开发者的标配

现在来看真正改变游戏规则的部分。以下是 tmux 如何变革 AI 驱动的开发。

### 基础工作流：持久化 Claude Code 会话

最简单也是最有影响力的用法：

```bash
# 创建一个专用的 Claude Code 会话
tmux new -s claude

# 启动 Claude Code
claude

# ... 与 Claude 进行关于你项目的深入对话 ...
# 需要离开？Ctrl+a d 断开

# 随时回来
tmux attach -t claude
# 你的整个对话都保留着
```

如果你还没设置 Claude Code，可以先看我们的[完整安装指南](/zh/posts/ai/2026-02-25-claude-code-setup-guide/)。仅凭这一点就值得学习 tmux。你的 Claude Code 会话变成了**持久化工作空间**，能够在以下情况中存活：

- 笔记本休眠/唤醒
- SSH 断开
- 终端崩溃
- 网络中断

### 开发仪表盘布局

设置多窗格布局以获得最大可视性：

```bash
#!/bin/bash
# 保存为 ~/scripts/ai-dev.sh

SESSION="ai-dev"

# 创建会话，第一个窗口用于 Claude Code
tmux new-session -d -s $SESSION -n claude

# 右侧分出窗格用于测试
tmux split-window -h -t $SESSION:claude

# 右下角分出窗格用于日志
tmux split-window -v -t $SESSION:claude.1

# 设置窗格大小（Claude 占 60% 宽度）
tmux resize-pane -t $SESSION:claude.0 -x '60%'

# 创建第二个窗口用于 git 操作
tmux new-window -t $SESSION -n git

# 选择 Claude 窗格并连接
tmux select-window -t $SESSION:claude
tmux select-pane -t 0

tmux attach -t $SESSION
```

这会创建：

```
┌──────────────────────┬───────────────┐
│                      │               │
│    Claude Code       │    测试       │
│    （主工作区）       │  (npm test)   │
│                      │               │
│                      ├───────────────┤
│                      │               │
│                      │    日志       │
│                      │ (tail -f ...) │
└──────────────────────┴───────────────┘
```

### Claude Code 弹出窗口（进阶）

如果你想让 Claude Code 作为**弹出覆盖层**，不用离开当前工作，可以使用这个 tmux 绑定：

```bash
# 添加到 ~/.tmux.conf
bind -r y run-shell '\
  SESSION="claude-$(echo #{pane_current_path} | md5 | cut -c1-8)"; \ # macOS 用 md5；Linux 用 md5sum
  tmux has-session -t "$SESSION" 2>/dev/null || \
  tmux new-session -d -s "$SESSION" -c "#{pane_current_path}" "claude"; \
  tmux display-popup -w80% -h80% -E "tmux attach-session -t $SESSION"'
```

工作原理：

1. 基于当前目录生成唯一的会话名（通过 MD5 哈希）
2. 如果不存在，创建一个运行 Claude Code 的后台 tmux 会话
3. 打开一个 80% 大小的弹出窗口连接到该会话

按 `Ctrl+a y` 切换弹出窗口。关闭它，Claude Code 在后台继续运行。再打开——对话完好无损。

> 这个技巧来自 [Takuya Matsuyama 的工作流](https://www.devas.life/how-to-run-claude-code-in-a-tmux-popup-window-with-persistent-sessions/)。本质上是一个嵌套的 tmux 会话以弹出窗口形式显示。

## 使用 Tmux 并行运行 AI 智能体

这是 tmux 真正具有变革性的地方。不用等一个 AI 智能体完成，而是**并行运行 4-8 个智能体**，各自处理不同任务。

### 为什么要并行？

算一下就知道。如果单个 AI 智能体一次产出完美方案的概率约为 25%，运行四个智能体的成功率为：

```
P(至少一个成功) = 1 - (0.75)^4 ≈ 68%
```

代价是大约 4 倍的 token 消耗。但时间节省是巨大的——不再是串行试错，而是并行探索。

### 方法一：手动 Tmux + Git Worktree

Git worktree 为每个智能体提供**隔离的仓库副本**，防止文件冲突。关于 Claude Code 原生 worktree 支持的深入介绍，请参阅我们的 [Claude Code Worktree 指南](/zh/posts/ai/2026-02-28-claude-code-worktree-guide/)。

```bash
# 为并行智能体创建 worktree
git worktree add -b feature-auth ../project-auth
git worktree add -b feature-api ../project-api
git worktree add -b feature-ui ../project-ui

# 创建 tmux 会话，每个智能体一个窗口
tmux new-session -d -s agents -n auth -c ../project-auth
tmux new-window -t agents -n api -c ../project-api
tmux new-window -t agents -n ui -c ../project-ui

# 在每个窗口中启动 Claude Code
tmux send-keys -t agents:auth "claude" Enter
tmux send-keys -t agents:api "claude" Enter
tmux send-keys -t agents:ui "claude" Enter

# 连接并监控
tmux attach -t agents
```

现在用 `Ctrl+a n`（下一个窗口）或 `Ctrl+a 1/2/3` 在智能体之间切换。

### 方法二：Claude Code Agent Teams（内置功能）

Claude Code 有实验性的原生多智能体团队支持，使用 tmux 来显示。我们在 [Agent Teams 协作指南](/zh/posts/ai/2026-02-28-claude-code-teams-guide/)中详细介绍了这个功能。

**启用 Agent Teams**：

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**启动团队**：

```
创建一个智能体团队来完成这个功能：
- 一个队友负责后端 API 实现
- 一个队友负责前端组件
- 一个队友负责编写测试
```

Claude 会自动：
- 创建 tmux 分屏窗格（每个队友一个）
- 通过共享任务列表分配工作
- 协调智能体之间的工作
- 汇总结果

每个队友都是一个完整、独立的 Claude Code 实例，拥有自己的上下文窗口。你可以点击任意窗格直接与该智能体交互。

> Agent Teams 在 macOS 的 tmux 中效果最好。对于 iTerm2，使用 `tmux -CC` 获得最佳体验。

### 方法三：Feature Design (FD) 系统

对于较大的项目，[Manuel Schipper 的方法](https://schipper.ai/posts/parallel-coding-agents/)提供了一个结构化框架：

**角色分配**：
- **规划智能体** —— 探索问题并编写规格说明
- **执行智能体** —— 按照完成的规格说明实现
- **PM 智能体** —— 管理待办事项并记录想法

**工作流程**：

```bash
# 终端 1：规划智能体
tmux new-session -s planner -c ~/project
# "探索认证系统重新设计，编写 Feature Design 规格说明"

# 终端 2-4：执行智能体（各自有 worktree）
tmux new-session -s worker1 -c ~/project-wt1
# "按照 docs/fd/042-auth-redesign.md 中的规格说明实现 FD-042"

tmux new-session -s worker2 -c ~/project-wt2
# "按照 docs/fd/043-api-routes.md 中的规格说明实现 FD-043"

tmux new-session -s worker3 -c ~/project-wt3
# "为 FD-042 和 FD-043 编写测试"
```

**实际上限**：认知负荷在 **8 个智能体**时达到峰值。超过这个数量你会失去态势感知。从 3-5 个开始，按需扩展。

### 方法四：自动化工具

几个工具可以自动化 tmux + AI 智能体工作流：

| 工具 | 描述 |
|------|------|
| [**dmux**](https://dmux.ai/) | AI 智能体的 tmux 窗格管理器，带自动 git worktree 隔离 |
| [**ntm**](https://github.com/Dicklesworthstone/ntm) | Named Tmux Manager：生成、排列和协调多个 AI 智能体 |
| [**Codeman**](https://github.com/Ark0N/Codeman) | 通过 Web UI 管理 20+ 个并行 Claude Code 会话 |

dmux 示例：

```bash
# 启动 3 个带有隔离 worktree 的并行智能体
dmux start --agents 3 --prompt "实现用户仪表盘功能"

# 监控所有智能体
dmux status

# 合并结果
dmux merge
```

## 使用 Tmux 进行远程 AI 开发

最强大的模式之一：在远程服务器上运行 Claude Code，随时随地访问。

### 设置

```bash
# 在你的服务器上
tmux new -s remote-claude
claude

# 从任何设备（笔记本、手机、平板）
ssh user@your-server
tmux attach -t remote-claude
```

这意味着你可以：
- 在台式机上开始复杂的重构
- 在沙发上用笔记本继续
- 通勤时用手机检查进度
- 永远不丢失上下文

### SSH 配置建议

在 `~/.ssh/config` 中添加以下内容，让远程 tmux 更顺畅：

```
Host devserver
    HostName your-server.com
    User your-username
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
```

`ServerAliveInterval` 可以防止长时间 Claude Code 会话中 SSH 超时。

## 高级 Tmux 技巧

### 同步窗格

同时向所有窗格发送相同的命令：

```bash
# 切换同步输入
Ctrl+a :setw synchronize-panes on

# 现在每次按键都会发送到所有窗格
# 在多个 worktree 中运行相同的设置命令时很有用

# 完成后关闭
Ctrl+a :setw synchronize-panes off
```

### 程序化发送按键

通过脚本自动化智能体交互：

```bash
# 向指定窗格发送命令
tmux send-keys -t agents:auth.0 "npm test" Enter

# 向会话中的所有窗口发送
for window in $(tmux list-windows -t agents -F '#W'); do
  tmux send-keys -t "agents:$window" "git pull" Enter
done
```

### 会话分组

在多个终端之间共享会话（与 AI 结对编程）：

```bash
# 终端 1
tmux new -s shared

# 终端 2（加入相同会话，独立的窗口选择）
tmux new -t shared -s paired
```

两个终端共享同一个会话，但可以独立查看不同窗口。非常适合一个人看 Claude Code 输出，另一个人监控测试。

### 钩子和通知

当 AI 智能体完成时收到通知。关于更高级的自动化，请参阅我们的 [Claude Code Hooks 指南](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/)——钩子可以在各种生命周期事件中触发脚本。

```bash
# 添加到 ~/.tmux.conf
# 当窗格在静默后产生输出时发出 bell 通知
set -g visual-activity on
setw -g monitor-activity on

# 或在智能体脚本中使用 bell 字符
# 当 Claude Code 完成任务时：
echo -e '\a'  # 触发 tmux bell 通知
```

## 完整速查表

### 会话

| 命令 | 描述 |
|------|------|
| `tmux new -s name` | 新建命名会话 |
| `tmux ls` | 列出会话 |
| `tmux attach -t name` | 连接到会话 |
| `tmux kill-session -t name` | 终止会话 |
| `Ctrl+a d` | 断开 |
| `Ctrl+a s` | 切换会话 |
| `Ctrl+a $` | 重命名会话 |

### 窗口

| 命令 | 描述 |
|------|------|
| `Ctrl+a c` | 新建窗口 |
| `Ctrl+a ,` | 重命名窗口 |
| `Ctrl+a n / p` | 下一个 / 上一个窗口 |
| `Ctrl+a 0-9` | 跳转到第 N 个窗口 |
| `Ctrl+a w` | 窗口选择器 |
| `Ctrl+a &` | 关闭窗口 |

### 窗格

| 命令 | 描述 |
|------|------|
| `Ctrl+a |` | 垂直分屏 |
| `Ctrl+a -` | 水平分屏 |
| `Ctrl+a h/j/k/l` | 导航（vim 风格） |
| `Ctrl+a z` | 切换全屏 |
| `Ctrl+a x` | 关闭窗格 |
| `Ctrl+a Space` | 循环布局 |
| `Ctrl+a q` | 显示窗格编号 |

### 其他

| 命令 | 描述 |
|------|------|
| `Ctrl+a [` | 复制模式（滚动） |
| `Ctrl+a ]` | 粘贴 |
| `Ctrl+a :` | 命令提示符 |
| `Ctrl+a r` | 重载配置 |
| `Ctrl+a ?` | 列出所有快捷键 |
| `Ctrl+a t` | 显示时钟 |

> 注意：以上快捷键基于本文的自定义 `~/.tmux.conf`（前缀 = `Ctrl+a`，vim 绑定）。

## 最佳实践

### 通用使用

1. **始终命名你的会话** —— 用 `tmux new -s 项目名`，而不是只输 `tmux`
2. **使用鼠标** —— `set -g mouse on` 让 tmux 更容易上手
3. **增大滚动缓冲区** —— AI 输出至少需要 50,000 行
4. **安装 tmux-resurrect** —— 你的会话能在系统重启后存活
5. **学会复制模式** —— `Ctrl+a [` 对于审查长输出至关重要

### AI 开发专用

1. **每个项目一个会话** —— 按项目组织 AI 对话
2. **专用 Claude 窗格** —— 给 Claude Code 最大的窗格（60%+ 宽度）
3. **保持测试可见** —— 在 Claude 编码时实时观察测试通过/失败
4. **用 worktree 隔离并行智能体** —— 防止智能体之间的文件冲突
5. **从小处开始** —— 先用 2-3 个智能体，熟练后扩展到 4-8 个
6. **设置通知铃声** —— 不用持续监控就能知道智能体何时完成
7. **经常保存检查点** —— AI 智能体在长会话中可能丢失上下文；保存进度

### 应避免的事项

- 不要运行超过 8 个并行智能体（认知超载）
- 不要让多个智能体编辑同一个文件（合并冲突）
- 不要忘记清理无用会话（定期 `tmux ls` 并清理）
- 不要跳过会话命名（你会后悔的）

## 总结

Tmux 是那种用得越多回报越大的工具。单独使用它已经是一个强大的终端管理器。与 Claude Code 等 AI 编码工具结合后，它成为现代开发工作流的基石：

- **持久化** —— 永远不会丢失对话或运行中的进程
- **并行化** —— 同时运行多个 AI 智能体
- **便携性** —— 随时随地访问完整的开发环境
- **高效性** —— 一次看到所有内容，无需切换窗口

从基础开始：安装 tmux，创建命名会话，学会断开和重连。然后逐渐加入窗格分屏、自定义配置，最终实现并行 AI 智能体。一周之内，你就会想不明白以前没有它是怎么开发的。

终端没有死。有了 tmux 和 AI，它比以往任何时候都更加生机勃勃。

## 相关阅读

- [Claude Code Worktree：并行运行多个 AI 任务](/zh/posts/ai/2026-02-28-claude-code-worktree-guide/) — 深入了解 Git worktree 模式实现并行 Claude Code 会话
- [Claude Code 团队协作：多智能体协作模式](/zh/posts/ai/2026-02-28-claude-code-teams-guide/) — 掌握 Agent Teams 实现协调的多智能体开发
- [Claude Code Hooks 指南：12 种自动化配置](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/) — 通过生命周期钩子自动化格式化、文件保护和通知
- [如何安装 Claude Code：完整安装指南](/zh/posts/ai/2026-02-25-claude-code-setup-guide/) — 从零开始使用 Claude Code
- [Claude Code 指南 2026：你需要知道的一切](/zh/posts/ai/2026-02-28-claude-code-complete-guide/) — 涵盖所有 Claude Code 功能的综合参考
