+++
date = '2026-03-30T10:00:00+08:00'
draft = false
title = 'Harness Engineering 完全指南：为什么 AI Agent 的「外围系统」比模型本身更重要'
description = '深入浅出讲透 Harness Engineering：从提示词工程到上下文工程再到线束工程的三次进化，核心公式 Agent = Model + Harness，实操组件拆解（引导器+传感器），以及 Claude Code、Codex 等工具的落地案例。'
toc = true
tags = ['Harness Engineering', 'AI Agents', 'AI Engineering', 'Claude Code', 'AI Coding Tools']
keywords = ['harness engineering', '线束工程', 'AI Agent 外围系统', 'harness engineering 是什么', 'harness engineering 入门', '提示词工程 vs 线束工程', 'AI 编程工具', 'Claude Code 配置']

[[params.faqItems]]
question = "Harness Engineering 是什么？"
answer = "Harness Engineering（线束工程）是设计 AI Agent 外围系统的学科。核心公式：Agent = 模型 + 线束。线束包括模型之外的一切：工具接口、护栏约束、反馈循环、记忆系统和可观测层。目标是让 Agent 在生产环境中稳定可靠地工作。"

[[params.faqItems]]
question = "Harness Engineering 和 Prompt Engineering 有什么区别？"
answer = "Prompt Engineering 优化你发给模型的指令；Context Engineering 优化模型看到的信息；Harness Engineering 设计整个运行环境：工作流编排、工具权限、验证系统、生命周期管理。三者是层层包含的关系，Harness Engineering 范围最大。"

[[params.faqItems]]
question = "为什么说模型选择不如 Harness 重要？"
answer = "因为模型已经同质化了——Claude、GPT、Gemini 的能力在一个很窄的区间内。LangChain 在不换模型的情况下，仅优化 Harness 就让编程 Agent 在 TerminalBench 2.0 上从第 30 名升到第 5 名（52.8%→66.5%）。决定 Agent 成败的是外围系统，不是模型。"

[[params.faqItems]]
question = "Harness 的核心组件是什么？"
answer = "两大类：引导器（Guides，前馈控制）和传感器（Sensors，反馈控制）。引导器在生成前引导行为，如 CLAUDE.md、lint 规则、架构文档；传感器在生成后纠错，如测试、类型检查、AI 代码审查。只有引导器会导致错误不被发现，只有传感器会导致重复犯错——两者必须组合使用。"
+++

![Harness Engineering 架构——层层包裹 AI Agent 核心的护栏、反馈循环和监控系统](cover.webp)

2026 年，AI 工程圈发现了一个反直觉的事实：**模型是 AI Agent 中最不重要的部分。** 决定一个 Agent 能不能在生产环境跑起来的，是模型「外面」的一切——它能调用的工具、约束它行为的护栏、帮助它自我纠错的反馈循环、让你能观察它工作的监控系统。

这个「模型外面的一切」，现在有了一个名字：**Harness（线束）**。构建它的学科叫做 **Harness Engineering（线束工程）**。

这不是一个空洞的概念。OpenAI 的 Codex 团队用 Harness Engineering 的原则，让 AI Agent **写了超过 100 万行生产代码**。LangChain 在不换模型的前提下，仅优化 Harness 就在 TerminalBench 2.0 上从第 30 名跃升到第 5 名。斯坦福 HAI 的研究发现，Harness 层面的优化让 Agent 输出质量提升了 28-47%，而提示词微调的提升不到 3%。

这篇文章用最通俗的方式讲透 Harness Engineering：它是什么、为什么出现、怎么运作、怎么落地。

## 三次进化：我们是怎么走到这一步的

AI 工程经历了三个阶段，每一步都在扩大工程师「设计什么」的范围。

### 第一阶段：Prompt Engineering（2022-2024）

**关注点：** 写出完美的指令。

```
"你是一个资深 Python 开发者。写干净、有注释的代码。
使用类型提示。遵循 PEP 8。逐步思考。"
```

这在 AI 是无状态工具的时代管用——发一条指令，得到一个回复。全部的工程挑战都在你选的词上。

**类比：** 给承包商写一封措辞完美的邮件。

### 第二阶段：Context Engineering（2025）

**关注点：** 构建正确的信息环境。

一条指令远远不够。模型需要一个动态构建的上下文窗口：相关文档、对话历史、工具定义、RAG 检索结果、当前文件内容。

```
系统提示 + 检索文档 + 对话历史 + 工具定义 + 
当前文件内容 + git diff → 上下文窗口 → 模型 → 响应
```

这是 RAG 管道、向量数据库和精细上下文管理的时代。

**类比：** 不只是邮件本身，而是整个简报包——组织架构、项目文档、过往沟通记录。

### 第三阶段：Harness Engineering（2026）

**关注点：** 设计整个运行环境。

Context Engineering 假设 Agent 做一次决策，你评估输出。但现代 Agent 是自主运行的——发起几百次工具调用、编辑几十个文件、跑测试、反复迭代。Harness 就是管理这整个生命周期的系统。

```
Harness = {
  工作流编排,
  工具访问策略,
  验证系统,
  反馈循环,
  记忆持久化,
  护栏约束,
  可观测性与监控,
  升级规则
}
```

**类比：** 不只是邮件或简报包——而是在设计整个办公室：文件归档系统、审批流程、安全制度、绩效考核。

### 三者的包含关系

```
┌─────────────────────────────────────────┐
│         Harness Engineering             │
│  ┌───────────────────────────────────┐  │
│  │       Context Engineering         │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │    Prompt Engineering       │  │  │
│  │  │   "写干净的 Python 代码"     │  │  │
│  │  └─────────────────────────────┘  │  │
│  │  + 文档、历史、工具、RAG           │  │
│  └───────────────────────────────────┘  │
│  + 工作流、护栏、反馈、生命周期管理       │
└─────────────────────────────────────────┘
```

每层扩大范围，但不替代前一层。你依然需要写好提示词、管好上下文。但现在你还要工程化设计围绕两者的系统。

## 核心公式：Agent = Model + Harness

**Model** 提供原始推理能力。**Harness** 提供其他一切。

| 维度 | Model | Harness |
|------|-------|---------|
| 类比 | CPU | 操作系统 |
| 做什么 | 思考、生成、推理 | 管理、约束、验证 |
| 怎么提升 | 等下一代模型 | **今天**就能工程化优化 |
| 差异化 | 同质化（性能差距很小） | 独特的（你的竞争优势） |

打个比方：CPU 没有操作系统就是废铁；操作系统没有 CPU 无法运行。但买电脑的时候，操作系统对你的体验影响远大于具体的 CPU 型号。

AI Agent 同理。Claude Opus 4.6、GPT-5、Gemini 3 Pro 推理能力都不差。你围绕它们构建的 Harness 决定了 Agent 是稳定交付代码还是制造混乱。

## 核心组件：引导器与传感器

Martin Fowler 的[经典文章](https://martinfowler.com/articles/harness-engineering.html)把 Harness 组件分成两大类：

### 引导器（Guides）—— 前馈控制

引导器在**生成之前**引导 Agent 行为，提高一次性做对的概率。

| 引导器 | 类型 | 举例 |
|--------|------|------|
| 架构文档 | 推理型 | `CLAUDE.md` 描述仓库结构和约定 |
| 编码规范 | 计算型 | ESLint/Prettier 配置约束输出格式 |
| 启动脚本 | 计算型 | 项目初始化脚本创建正确的文件结构 |
| 类型定义 | 计算型 | TypeScript 类型收窄解题空间 |
| 示例模式 | 推理型 | 展示"正确做法"的代码片段 |

**在 Claude Code 里，你的引导器包括：**
- `CLAUDE.md` 和 `AGENTS.md` 文件（约定、约束、模式）
- MCP Server 配置（可用工具）
- Skills（按需加载的能力包）

**苏黎世联邦理工的一项关键研究发现：** `CLAUDE.md` 控制在 60 行以内效果最好。人写的简洁文件提升约 4%，但 LLM 自动生成的冗长文件反而**降低了 20%** 的表现。少即是多。

### 传感器（Sensors）—— 反馈控制

传感器在**生成之后**帮助 Agent 自我纠错。

| 传感器 | 类型 | 能发现什么 |
|--------|------|-----------|
| 单元测试 | 计算型 | 行为正确性 |
| 类型检查 | 计算型 | 类型错误、接口不匹配 |
| 代码检查 | 计算型 | 风格违规、常见 bug |
| AI 代码审查 | 推理型 | 语义问题、设计缺陷 |
| 集成测试 | 计算型 | 跨组件故障 |

**在 Claude Code 里，你的传感器包括：**
- Hooks（`PreToolUse`、`PostToolUse`）自动化验证
- 代码修改后自动跑的测试套件
- 类型检查（TypeScript `tsc`、Python `mypy`）

**关键经验：** 传感器的输出要为 LLM 优化。比如 lint 错误信息写成 `Error: unused variable 'x' on line 42` 就比一个错误码有用得多。格式化成纠错指令效果最好。

### 为什么两者缺一不可

```
只有引导器 → Agent 按模式做但从不验证 → 静默失败
只有传感器 → Agent 犯错→发现→修复→再犯同样的错 → 缓慢低效
引导器 + 传感器 → Agent 通常一次做对，偶尔出错能自动修复 → 可靠
```

## 真实案例

### OpenAI Codex：100 万行代码，零行人写

OpenAI Codex 团队在**五个月内生产了超过 100 万行代码和 1,500 个 PR**，没有一行是人类工程师写的。

怎么做到的？七名工程师全力投入 Harness Engineering：
- 分层架构通过**自定义 lint 规则**（不是提示词）强制执行
- 结构性测试验证模块边界
- 定期"垃圾回收"扫描架构漂移
- 仓库作为唯一真相源——约束写在代码里，不是指令里

核心原则：**把约束编码进系统，而不是写进提示词。** 一条拦截循环引用的 lint 规则比一句"不要创建循环引用"的提示词可靠一万倍。

### LangChain：不换模型，从第 30 名升到第 5 名

LangChain 的编程 Agent 在 TerminalBench 2.0 上从 52.8% 跳到 66.5%——从第 30 名升到第 5 名——**模型一点没换**。只改了 Harness：更好的工具定义、更聪明的上下文管理、更完善的错误恢复循环。

这是"模型选择不如 Harness 质量重要"最有力的证据。

### Stripe Minions：每周 1,300 个 PR

Stripe 的自主 Agent 系统每周合并 1,300+ 个 PR：
- "Blueprint" 编排，确定性节点和 Agent 节点分离
- Push 前的 Hook 自动选择相关 lint 规则
- **两次失败升级规则**：同一个问题失败两次就转交人类，不再无限重试

### Epsilla 实验：42% → 78%

一个团队在同一个 benchmark 上，用**完全相同的模型和提示词**，仅修改运行环境（工具接口、验证循环、约束执行），就把 Agent 表现从 42% 提升到 78%。

## 实操指南：从零搭建 Harness

### 第一层：基础配置（从这里开始）

```markdown
# CLAUDE.md（控制在 60 行以内）

## 项目
- TypeScript monorepo，pnpm workspaces
- React 前端，Express 后端

## 约定
- 优先组合而非继承
- 所有 API 响应使用共享的 Result<T> 类型
- 测试文件与源码同目录：foo.ts → foo.test.ts

## 命令
- `pnpm test` — 跑全部测试
- `pnpm lint` — ESLint + Prettier
- `pnpm typecheck` — TypeScript 严格模式
```

这是最小可行 Harness。告诉 Agent 项目是什么、遵循什么约定、怎么验证。

### 第二层：加上反馈循环（Hooks）

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "pnpm typecheck --quiet",
        "description": "文件修改后自动类型检查"
      }
    ]
  }
}
```

Agent 每次修改文件后自动跑类型检查。错误立即暴露，不会在改了 50 个文件后才发现。

### 第三层：按需加载（Skills）

别把所有东西塞进 CLAUDE.md，用 Skills 按需加载：

```markdown
# .claude/skills/database-migration.md
---
name: database-migration
description: 创建或修改数据库迁移时使用
---

## 迁移规则
- 必须创建可逆迁移（up + down）
- DDL 变更使用事务
- 迁移前在生产 schema 副本上测试
- 永远不要修改已有迁移，创建新的
```

只在做数据库迁移时才加载这段上下文，其他时候不占用上下文窗口。

### 第四层：子 Agent 隔离

复杂任务用子 Agent 隔离上下文：

- 父 Agent（Opus）负责编排和关键决策
- 子 Agent（Sonnet/Haiku）负责具体子任务
- 每个子 Agent 返回精简结果 + 文件:行号引用

防止上下文污染——父 Agent 的上下文窗口保持干净。

### 第五层：架构约束

把架构规则写成可自动验证的适应度函数（Fitness Functions）：

```typescript
// architecture.test.ts
describe('架构适应度', () => {
  it('后端模块不引用前端', () => {
    const violations = findImports('src/backend/**', 'src/frontend/**');
    expect(violations).toHaveLength(0);
  });

  it('API 处理器使用共享 Result 类型', () => {
    const handlers = findFiles('src/api/handlers/**/*.ts');
    handlers.forEach(file => {
      expect(file.content).toContain('Result<');
    });
  });
});
```

这些测试作为传感器，捕捉架构漂移——不管漂移来自人类还是 Agent。

## 常见错误

| 错误 | 为什么不行 | 应该怎么做 |
|------|-----------|-----------|
| 一开始就设计完美 Harness | 你猜不到 Agent 会犯什么错 | 从最小配置开始，出问题再加 |
| 装一堆 MCP Server "以防万一" | 每个工具都消耗上下文预算 | 需要时再加 |
| CLAUDE.md 写 500 行 | Agent 在冗长指令下表现更差 | 控制在 60 行，用 Skills 按需加载 |
| 每次改文件都跑完整测试 | 5 分钟的循环毁掉迭代速度 | 跑相关子集，完整套件放 CI |
| 只靠测试（传感器） | Agent 反复犯同样的错 | 加引导器（架构文档、lint 规则）预防 |
| 把约束写在提示词里 | 提示词是建议，lint 是强制执行 | 用计算型约束（lint、类型系统、Hooks） |

## Ashby 定律：为什么约束反而提升产出

看似矛盾：给 Agent 更**少**的选项让它更**高效**。但这直接来自 Ashby 必要多样性定律：调节器的复杂度必须不低于被调节系统。

LLM 能生成几乎任何东西——解题空间是无限的。为无限空间构建完备的 Harness 是不可能的。但如果你承诺固定的模式——"所有 API 端点遵循这个结构"、"所有数据访问走这一层"——你就把解题空间缩小到 Harness 能全面覆盖的范围。

**约束不是限制。约束是可靠自主运行的前提条件。**

## 接下来会怎样

1. **Harness 模板**：针对常见模式（CRUD 服务、数据管道、事件处理器）的预制引导器+传感器包
2. **Harness 评估**：类似代码覆盖率的 Harness 质量指标
3. **AI 辅助 Harness 开发**：用 AI 写结构测试、lint 规则和适应度函数来管理其他 AI Agent
4. **Harness 感知训练**：模型根据 Harness 运行时的失败轨迹数据来改进自身

工程师的角色正在从"写代码"转向"设计写代码的系统"。Harness Engineering 是让这个转变真正落地的实操学科。

## 延伸阅读

- [Claude Code Hooks 完全指南](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Harness 实操：用 Hooks 构建反馈循环
- [Claude Code CLAUDE.md 最佳实践](/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) — 写好引导器文件
- [Context Engineering 指南](/posts/ai/2026-03-10-context-engineering-guide/) — Harness Engineering 的前身
- [2026 AI 开发方法论对比](/posts/ai/2026-03-11-ai-development-methodologies-compared/) — Harness Engineering 在更大图景中的位置
- [Claude Code 安全指南](/posts/ai/2026-02-22-claude-code-security/) — Harness 设计中的安全考量
- [Superpowers 深度解析](/posts/ai/2026-02-01-superpowers-deep-dive/) — 一个真实的 Harness（Skills 系统）实战
