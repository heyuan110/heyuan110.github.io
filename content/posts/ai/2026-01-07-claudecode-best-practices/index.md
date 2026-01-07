---
title: "Claude Code 创始人的几个最佳实践"
date: 2026-01-07T18:00:00+08:00
author: "bruce"
description: "来自 Anthropic 工程团队的 Claude Code 官方最佳实践，包括配置技巧、思考模式、工作流程和高级用法"
toc: true
images:
tags:
  - AI
  - Claude Code
  - 最佳实践
  - Anthropic
categories:
  - AI工具与工程实战
---

![Claude Code Best Practices](claude-code-best-practices.png)

Anthropic 工程团队发布了一份 [Claude Code 最佳实践指南](https://www.anthropic.com/engineering/claude-code-best-practices)，作者是 Boris Cherny，以及 Daisy Hollman、Ashwin Bhat、Cat Wu、Sid Bidasaria 等工程师。

这些实践来自他们在各种代码库、语言和环境中使用 Claude Code 的真实经验。下面是其中最实用的几条。

## 1. 用好 CLAUDE.md 文件

CLAUDE.md 是 Claude Code 的"记忆文件"。把它放在项目根目录，Claude 每次启动时都会自动读取。

应该写什么：

- 常用的 bash 命令和用法
- 代码风格规范
- 测试和部署流程
- 项目特有的坑和注意事项
- 开发环境配置说明

```markdown
# CLAUDE.md 示例

## 构建命令
- `npm run dev` - 启动开发服务器
- `npm run test` - 运行测试
- `npm run build` - 生产构建

## 代码规范
- 使用 TypeScript
- 组件放在 src/components/
- 工具函数放在 src/utils/

## 注意事项
- API 密钥在 .env.local 中配置
- 数据库迁移前先备份
```

文件可以放在多个位置：

- 项目根目录（推荐，可以提交到 git）
- 父级目录（适合 monorepo）
- 用户主目录 `~/.claude/CLAUDE.md`（全局配置）

## 2. 触发"深度思考"模式

Claude Code 有不同级别的思考模式，用特定的词可以触发：

| 触发词 | 思考深度 |
|--------|----------|
| think | 基础思考 |
| think hard | 加深思考 |
| think harder | 更深入思考 |
| ultrathink | 最大思考预算 |

什么时候用：

- 复杂的架构决策 → `ultrathink`
- 代码审查和优化 → `think hard`
- 简单的修改 → 不需要特别触发

示例：

```
帮我分析这个模块的依赖关系，ultrathink
```

## 3. 遵循"探索→计划→编码→提交"流程

Anthropic 团队推荐的标准工作流程：

**第一步：探索**
```
先读一下 src/auth/ 目录下的代码，不要做任何修改
```

**第二步：计划**
```
基于你看到的代码，think hard，给我一个添加 OAuth 支持的方案
```

**第三步：编码**
```
按照计划实现，完成后运行测试确认
```

**第四步：提交**
```
/commit
```

为什么这样做有效：让 Claude 先理解上下文再动手，减少返工。

## 4. 指令要具体

模糊指令：
```
给 foo.py 加点测试
```

具体指令：
```
为 foo.py 的 calculate_total 函数写测试，覆盖以下场景：
1. 空列表输入
2. 包含负数的列表
3. 超过 100 个元素的列表
不要用 mock
```

具体的指令能显著提高一次成功率。

## 5. 善用 /clear 命令

每完成一个任务，用 `/clear` 清空上下文。

原因：
- 避免旧对话消耗 token
- 防止 Claude 被无关上下文干扰
- 每个任务保持聚焦

经验法则：一个功能、一个 chat。做完就清。

## 6. 提供视觉上下文

Claude Code 能理解图片。可以：

- 直接粘贴截图（macOS: `Cmd+Ctrl+Shift+4` 截图到剪贴板，然后 `Ctrl+V` 粘贴）
- 拖入设计稿
- 粘贴错误截图

视觉迭代工作流：

1. 给 Claude 一张设计稿截图
2. 让它实现
3. 截图实际效果，指出差异
4. 重复 2-3 次直到满意

## 7. 中途纠偏

发现 Claude 跑偏了？

- **按一次 Escape**：中断当前操作
- **按两次 Escape**：返回编辑上一条指令
- **直接说**："停，换个方向..."

早纠正比做完再改成本低得多。

## 8. 多 Claude 并行工作

高级玩法：同时开多个 Claude 实例。

**方式一：多终端**

开两个终端窗口，各跑一个 Claude，分别做不同任务。

**方式二：Git Worktree**

```bash
# 创建独立的工作目录
git worktree add ../feature-a feature-a
git worktree add ../feature-b feature-b

# 在不同目录启动 Claude
cd ../feature-a && claude
cd ../feature-b && claude
```

**方式三：写代码 + 审代码分离**

一个 Claude 写代码，另一个 Claude（独立 session）专门审查。互相独立，不受彼此上下文影响。

## 9. Headless 模式自动化

用 `claude -p` 可以在无交互模式下运行，适合集成到 CI/CD：

```bash
# 自动给 GitHub issue 打标签
claude -p "分析这个 issue 内容，返回合适的标签" --json

# 代码审查
claude -p "审查这个 PR 的改动，给出建议" < diff.txt

# 管道处理
cat data.json | claude -p "提取所有邮箱地址" --json | jq '.emails'
```

## 10. 用检查清单处理复杂任务

大型迁移或重构，让 Claude 先列个清单：

```
我要把项目从 JavaScript 迁移到 TypeScript。
先列一个 markdown 检查清单，包括所有需要改的地方，不要开始动手。
```

Claude 会生成一个任务清单，然后你可以逐项推进，确保不遗漏。

---

## 总结

这些实践的核心思想：

1. **配置先行**：用 CLAUDE.md 让 Claude 了解你的项目
2. **先想后做**：探索→计划→执行，减少返工
3. **保持聚焦**：勤用 /clear，每次对话一个目标
4. **具体明确**：指令越具体，结果越好
5. **善用工具**：截图、多实例、headless 模式

Claude Code 的设计理念是"低层级、不强加观点"——它是一个灵活的工具，怎么用取决于你。掌握这些实践，能让你用得更顺手。

---

**参考资料**：
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic 官方博客
