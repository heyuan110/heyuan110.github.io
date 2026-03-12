+++
date = '2026-02-24T07:30:00+08:00'
draft = false
title = '斯坦福 CS146S 精读（二）：上下文工程——AI 编程最被低估的核心能力'
description = '深度解读斯坦福 CS146S 第三周课程：从 Prompt Engineering 到 Context Engineering 的范式跃迁，Spec 为何成为新的源代码，长上下文的四种失败模式与应对策略。'
toc = true
tags = ['Context Engineering', 'AI 编程', 'Stanford CS146S', 'Vibe Coding', 'Prompt Engineering']
categories = ['AI原理']
keywords = ['Context Engineering', '上下文工程', 'Specs Are the New Source Code', '长上下文失败', 'AI 编程上下文管理']
+++

> 本文是「斯坦福 Vibe Coding 课程精读」系列第 2 篇。系列导航见文末。

如果让我在 CS146S 的 10 周课程中只选一周来精读，我会毫不犹豫选 **Week 3**。

不是因为它最酷炫——那可能是 Week 8 的"一句话做 App"。也不是因为它最硬核——那可能是 Week 6 的安全攻防。而是因为 Week 3 讲的内容，直接决定了你用 AI 编程的天花板在哪里。

**上下文工程（Context Engineering）**——这个词你可能刚开始听说，但它正在取代 Prompt Engineering 成为 AI 编程的核心能力。原因很简单：单条 Prompt 的优化已经触顶，真正决定 AI 输出质量的，是你给它提供的**整体上下文**。

写一个好 prompt 是加法，做好上下文工程是乘法。

## 什么是上下文工程

Prompt Engineering 关注的是"怎么问问题"，Context Engineering 关注的是"给 AI 呈现一个什么样的世界"。

两者的区别就像：

- Prompt Engineering = 在面试中问一个好问题
- Context Engineering = 给面试官准备一整份精心组织的背景材料，让TA在回答你的问题前就已经对情况了然于胸

具体来说，上下文工程包含以下维度：

| 维度 | 说明 | 示例 |
|------|------|------|
| **信息选择** | 给 AI 看什么、不看什么 | 只加载相关的源文件，而非整个代码库 |
| **信息组织** | 以什么结构呈现信息 | 分层文档：设计文档 → 实施计划 → 具体代码 |
| **信息质量** | 确保上下文中没有错误或矛盾 | 清理过时的注释和文档 |
| **信息时机** | 什么时候提供什么信息 | 先给架构概览，再给具体实现 |
| **工具配置** | 通过 [MCP](/posts/ai/2026-02-20-mcp-protocol-guide/)/工具扩展 AI 的感知范围 | 连接数据库 schema、API 文档、项目管理工具 |

StockApp 团队在实践中总结了一个精辟的公式：**好代码是好上下文的副产品。**

他们将代码仓库视为人类与 AI 的共享工作空间，建立了分层文档结构：

```
docs/designs/    → 产品需求与高层目标
docs/plans/      → 详细实施计划
docs/guides/     → API 教程
schema.sql       → 数据结构规范
CLAUDE.md        → AI 本地化指导
README.md        → 项目概览
```

这种结构的每一层都有明确的受众和目的：designs 给决策者看，plans 给执行者（包括 AI）看，guides 给消费者看。而 [CLAUDE.md](/posts/ai/2026-01-12-claudemd-memory-guide/) 是专门给 AI Agent 看的"使用说明书"——告诉它这个项目的约定、禁忌和偏好。

## Spec 是新的源代码

Week 3 最核心的一篇阅读材料是 [Specs Are the New Source Code](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code)。这篇文章的核心论点是：

> 在 AI 编程时代，我们把优先级搞反了——精心维护生成的代码，却随手对待指导生成的规格说明。这就像"粉碎源代码，却对二进制文件做版本控制"。

想想这个类比有多精准。

在传统开发中，源代码是核心资产——它精确地定义了系统的行为。PRD 和设计文档写完就扔，代码才是真正被版本控制、Code Review、测试的对象。

但在 AI 编程时代，关系倒转了：

- **Spec（规格说明）** 包含了完整的意图和价值观
- **代码** 只是 Spec 的"有损投影"——AI 根据你的 Spec 生成代码，但这个转换过程必然丢失信息
- 如果 Spec 写得模糊，AI 会用自己的"猜测"填补空白——这些猜测可能与你的意图南辕北辙

这意味着什么？

### 1. Spec 需要被版本控制

就像代码一样，Spec 应该用 Git 管理，有 diff、有 history、有 review。因为 Spec 是你让 AI 理解意图的唯一途径——如果 Spec 丢失或过时，你就无法可靠地复现 AI 的输出。

### 2. Spec 的质量直接决定代码质量

这不是"写得好一点 prompt 效果好一点"的线性关系，而是指数级关系。一个模糊的 Spec 产生模糊的代码，模糊的代码产生模糊的 bug，模糊的 bug 产生更模糊的补丁——这是一个退化循环。反之，一个精确的 Spec 能让 AI 在第一次就生成接近生产质量的代码。

### 3. PM 的角色变得空前重要

Andrew Ng 指出了一个前所未有的趋势：现在一些组织需要的 PM 数量是工程师的两倍。当 AI 加速了工程产出速度，瓶颈从"写代码"转移到了"做决策和写清楚需求"。

Sean Grove（OpenAI）的表述更直接：

> 在不远的将来，沟通最有效的人就是最有价值的程序员。

### 4. 工作流程倒转

**旧流程**：模糊想法 → 线框图 → 设计 → MVP → 反馈 → 修改 Spec → 重建

**新流程**：模糊想法 → 快速原型 → 反馈 → 清晰 Spec → AI 实现

注意区别：在新流程中，原型不是为了交付，而是为了**快速获得反馈来完善 Spec**。原型是 Spec 的草稿，不是产品的草稿。

## 长上下文的四种失败模式

"把所有东西都塞给 AI 不就行了？"——这是最常见的上下文管理误区。

[How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) 这篇文章揭示了一个反直觉的事实：**更长的上下文并不会带来更好的结果。** 尽管现代模型支持百万级 token 的上下文窗口，盲目填充只会导致四种失败。

### 失败模式一：上下文中毒（Context Poisoning）

错误信息一旦进入上下文，就会被 AI 反复引用和放大。

Google 的 Gemini 在尝试玩精灵宝可梦时就出现了这个问题：一条虚假信息进入上下文后，Agent 开始"固执于一个无法达成的目标"，不断重复无效操作。

在 AI 编程中，这意味着：如果你的 CLAUDE.md 里有一条过时的规则（比如"使用 React 16 的 class components"），AI 会忠实地遵循这条错误指令，即使其他上下文暗示应该用 hooks。

**对策**：定期审计上下文文件，确保没有过时或矛盾的信息。把上下文文件当代码一样维护。

### 失败模式二：上下文分心（Context Distraction）

随着上下文长度增长，AI 倾向于"重复历史行为而非综合新策略"。

Databricks 的研究表明，模型在处理超过 32K token 的上下文时，正确性开始显著下降。模型不是"忘了"早期的信息，而是**被近期的信息分散了注意力**，导致决策质量退化。

在 AI 编程中，这体现为：当你在一个长对话中不断追加需求，AI 到后面可能会"忘记"你早期的约束条件，生成与之矛盾的代码。

**对策**：保持对话聚焦。一个对话做一件事。需要切换上下文时，新开一个会话。

### 失败模式三：上下文混淆（Context Confusion）

过多的工具定义或无关信息会干扰模型的判断。

Berkeley 的函数调用排行榜显示：**每个模型在获得更多工具时性能都会下降**。Llama 3.1 8B 在 19 个工具时能正常工作，到 46 个工具时就开始失败。即使是 GPT-4 级别的模型也不能免疫。

这就是为什么 Anthropic 在 [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) 中强调："少而精的工具优于面面俱到的 API 封装"。不是把所有能力都暴露给 AI，而是只给它当前任务需要的工具。关于[工具设计的实战经验](/posts/ai/2026-02-22-claude-code-mcp-server-tutorial/)，可以参考 MCP Server 开发教程。

**对策**：根据任务动态加载工具和上下文。比如在 [Claude Code](/posts/ai/2026-01-14-claude-code-guide/) 中，不要一次性加载所有可用的 MCP Server。

### 失败模式四：上下文冲突（Context Conflict）

多个来源的信息相互矛盾时，模型性能会急剧下降。

微软和 Salesforce 的联合研究发现一个惊人的数据：分阶段提供相同信息（先给出部分错误答案，再给完整正确信息）导致性能**平均下降 39%**。因为早期的错误答案留在上下文中，干扰了最终的判断。

在 AI 编程中，这意味着：如果你的项目里 README 说用 PostgreSQL，但 docker-compose.yml 里配的是 MySQL，AI 可能会生成不一致的代码，或者在两种数据库之间反复横跳。

**对策**：确保所有上下文来源的一致性。发现矛盾时立即修正，不要指望 AI 能"自动取舍"。

## Context Rot：上下文也会"腐烂"

Chroma 团队的 [Context Rot 研究](https://research.trychroma.com/context-rot) 从另一个角度补充了上下文失败的图景。

他们测试了 18 个主流模型（包括 Claude、GPT、Gemini、Qwen、Llama），发现了一个普遍规律：**随着输入长度增加，模型性能显著且持续地下降，即使是对于极其简单的任务**。

更令人意外的发现：

1. **结构化的上下文反而不如混乱的上下文**。将上下文文本打乱顺序后，所有模型的表现反而提升了。这暗示注意力机制在处理逻辑连贯的长文本时存在系统性弱点。

2. **问答相关度越低，性能下降越快**。当问题和答案的表面相似度低时（需要更多推理），模型在长上下文中的退化更严重。

3. **单个干扰项就能显著降低准确率**。即使只在上下文中加入一条无关信息，模型也会受到影响。

4. **Claude 系列模型在不确定时倾向于拒绝回答**，而 GPT 系列倾向于生成自信但错误的回答。这是一个有趣的行为差异，对实际使用有重要启示。

这些发现的实践意义是：**上下文不是越多越好，而是越精准越好**。你给 AI 的每一条信息都有成本——不仅是 token 成本，更是注意力成本。

## Anthropic 的工具设计五原则

Week 3 的另一篇重要阅读材料是 Anthropic 的 [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)。工具设计直接影响上下文质量——设计不当的工具会给 AI 带来不必要的混淆和噪音。

### 原则一：精选胜于全包

不要把 API 的每个端点都封装成工具。识别出 Agent 真正需要的核心操作，合并相关功能。比如，与其分别提供 `list_events`、`create_event`、`invite_attendees`、`book_room` 四个工具，不如提供一个 `schedule_event` 工具，内部封装多步操作。

### 原则二：一致的命名空间

当你有大量工具时，用前缀分组：`asana_projects_search`、`asana_users_search`、`slack_channels_list`。这帮助 AI 快速定位相关工具，减少混淆。

### 原则三：返回语义化数据

不要返回裸 ID，返回有意义的名称和描述。`{"user": "张三", "role": "admin"}` 比 `{"user_id": "a1b2c3", "role_id": 1}` 对 AI 更友好。AI 需要**理解**数据，而不是查表。

### 原则四：token 效率

实现分页、过滤和截断。Claude Code 默认将工具响应限制在 25,000 token。如果你的工具一次返回 10 万行数据，AI 会被淹没。给每个查询设置合理的默认限制。

### 原则五：工具描述即性能杠杆

工具的 description 字段对 AI 的行为有巨大影响。Anthropic 团队发现，仅仅优化工具描述就在 SWE-bench 评测上取得了最先进的成绩。这意味着：你的工具"说明书"和你的代码一样重要。

## 实战：如何在项目中实施上下文工程

理论讲完了，怎么落地？基于 CS146S 的材料和实践案例，这里给出一个可操作的框架。

### 第一层：项目级上下文

这是所有开发的基础，通常通过配置文件和文档来实现。

```
# CLAUDE.md 示例结构

## 项目概述
这是一个基于 FastAPI 的电商 API 服务...

## 技术栈
- 后端：FastAPI + SQLAlchemy
- 数据库：PostgreSQL 15
- 缓存：Redis
- 消息队列：RabbitMQ

## 代码规范
- 使用 pydantic v2 进行数据验证
- 所有 API 端点需要类型注解
- 错误处理统一使用自定义异常类

## 禁忌
- 不要使用 ORM 的 lazy loading
- 不要在 API handler 中直接写 SQL
- 不要使用 print 调试，使用 structlog
```

### 第二层：任务级上下文

每次给 AI 一个任务时，提供该任务特定的上下文。

```
# 任务：实现用户注册 API

## 相关文件
- src/models/user.py（User 模型定义）
- src/schemas/auth.py（认证相关 schema）
- src/services/email.py（邮件发送服务）

## 业务规则
- 邮箱需要验证唯一性
- 密码至少 8 位，包含大小写和数字
- 注册成功后发送验证邮件
- 使用已有的 EmailService，不要新建

## 参考实现
- 类似的 API 可以参考 src/api/v1/products.py 的模式
```

### 第三层：上下文卫生

最容易被忽视但最重要的一层。

**定期清理**：每周检查一次 CLAUDE.md 和其他上下文文件，移除过时的信息。

**一致性校验**：确保 README、CLAUDE.md、docker-compose.yml、CI 配置等各处的信息不矛盾。

**新开会话**：当一个对话超过 30 轮或 50K token 时，新开一个会话，在新会话中提供干净的上下文。

**动态工具加载**：不要一次性启用所有 MCP Server。根据当前任务只启用需要的。在写后端代码时不需要 Figma MCP，在做设计时不需要数据库 MCP。

### 第四层：反馈驱动的上下文优化

Anthropic 在工具设计文章中提到一个巧妙的做法：**把 AI 的评测对话反馈给 AI 自身来改进工具**。

同样的思路可以用在上下文管理上：当 AI 生成了不符合预期的代码时，分析原因——是上下文缺失？是上下文矛盾？还是上下文过载？然后针对性地调整上下文策略。

把上下文管理当作一个持续优化的系统，而不是一次性配置。

## Cognition（Devin）的视角

Week 3 的嘉宾是 Silas Alberti，Cognition（Devin 的开发公司）的 Head of Research。

Devin 的 [Agents 101](https://devin.ai/agents101) 文档为上下文管理提供了另一个视角——从 Agent 框架设计者的角度看，什么样的上下文能让 Agent 表现最好。

核心观点：

1. **明确"怎么做"，而不只是"做什么"**。与其说"实现用户认证"，不如说"使用 JWT + refresh token 模式实现用户认证，token 过期时间 15 分钟，refresh token 7 天"。

2. **给 Agent 接入反馈循环**。让 Agent 能运行测试、看到 lint 错误、访问 CI/CD 结果。这些反馈本身就是一种动态上下文——告诉 Agent 什么做对了、什么做错了。

3. **为不同复杂度设置不同的上下文策略**：
   - 简单任务：直接描述即可
   - 中等任务（1-6 小时工作量）：提供详细上下文 + 预期节省 80% 时间但保留人工打磨
   - 复杂任务：分阶段提供上下文 + 设置多个检查点

## 从"问好一个问题"到"构建一个信息系统"

CS146S Week 3 教会我们的核心认知可以浓缩为一句话：

**Prompt Engineering 是手艺，Context Engineering 是系统工程。**

手艺靠天赋和经验，能把一个问题问得精妙。系统工程靠架构和纪律，能确保 AI 在任何任务上都有一致的高质量输出。

这个转变对不同角色的影响：

| 角色 | 影响 |
|------|------|
| **个人开发者** | 需要把更多精力放在文档和上下文维护上，而不是代码本身 |
| **团队 Lead** | 需要建立团队级的上下文管理规范（CLAUDE.md 模板、文档结构、工具配置标准） |
| **PM/产品经理** | 角色价值大幅提升——写清楚 Spec 成为最关键的产出 |
| **架构师** | 从设计代码架构变为设计信息架构——不仅要让代码好维护，还要让 AI 好理解 |

当 Spec 成为新的源代码，Context 成为新的编程环境，我们其实正在见证软件工程的一次底层重构。代码的生成可以交给 AI，但上下文的管理——决定 AI 看什么、怎么看、什么时候看——这是人类不可替代的核心能力。

至少目前是这样。

## 相关阅读

- [CLAUDE.md 记忆术：一个文件让 AI 永远记住你是谁](/posts/ai/2026-01-12-claudemd-memory-guide/) — 上下文工程最直接的实践
- [MCP 协议全面解析](/posts/ai/2026-02-20-mcp-protocol-guide/) — 通过 MCP 扩展 AI 的上下文感知范围
- [Claude Code 从入门到精通完全指南](/posts/ai/2026-01-14-claude-code-guide/) — 上下文工程的最佳实践平台
- [Claude Code 最佳实践](/posts/ai/2026-01-06-claudecode-best-practices/) — Claude Code 创始人分享的实操经验
- [从零手搓一个 Claude Code](/posts/ai/2026-02-24-build-magic-code/) — 动手理解 AI 编程助手的底层架构

## 系列文章导航

本文是「斯坦福 Vibe Coding 课程精读」系列第 2 篇：

1. [斯坦福 CS146S 精读（一）：Vibe Coding 如何成为正式学科](/posts/ai/2026-02-24-stanford-cs146s-overview/)
2. **本文**：斯坦福 CS146S 精读（二）：上下文工程（Week 3）
3. [斯坦福 CS146S 精读（三）：Agent Manager](/posts/ai/2026-02-24-agent-manager-patterns/)（Week 4）
4. [斯坦福 CS146S 精读（四）：Secure Vibe Coding](/posts/ai/2026-02-24-secure-vibe-coding/)（Week 6-7）
5. [斯坦福 CS146S 精读（五）：从原型到生产](/posts/ai/2026-02-24-prototype-to-production/)（Week 8-9）
