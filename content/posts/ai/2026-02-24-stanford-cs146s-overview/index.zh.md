+++
date = '2026-02-24T07:00:00+08:00'
draft = false
title = '斯坦福 CS146S 全解析 2026：AI 编程公开课中文笔记（免费自学路线）'
description = '斯坦福顶级 AI 编程课 CS146S The Modern Software Developer 完整拆解：10 周大纲、Boris Cherney/Karpathy 级嘉宾阵容、免费 PPT 和作业代码资源全收录，一篇看懂如何系统学 Vibe Coding。'
toc = true
tags = ['Vibe Coding', 'Stanford CS146S', 'AI 编程', '课程解读', 'Agentic Engineering']
categories = ['AI原理']
keywords = ['Stanford CS146S', '斯坦福 Vibe Coding 课程', 'The Modern Software Developer', 'AI 编程课程', 'Vibe Coding 学什么', '斯坦福 LLM 课程', 'LLM 系统设计', 'AI 编程公开课', 'Vibe Coding 教程', '斯坦福 AI 编程课']

[[params.faqItems]]
question = "斯坦福 CS146S 是什么课程？"
answer = "CS146S（The Modern Software Developer）是斯坦福大学 2025 年秋季首次开设的 3 学分课程，系统教授 AI 驱动的软件开发。覆盖从 LLM 原理、Agent 架构到安全攻防、代码审查和生产运维的完整软件工程生命周期。"

[[params.faqItems]]
question = "CS146S 的课程资料可以免费获取吗？"
answer = "可以。几乎所有课程资料都公开免费，包括完整教学大纲（themodernsoftware.dev）、课件 PPT、阅读材料和 GitHub 上的作业代码。你可以按照 10 周课程安排自学。"

[[params.faqItems]]
question = "CS146S 有哪些重量级嘉宾？"
answer = "嘉宾阵容包括 Boris Cherney（Anthropic Claude Code 创始人）、Zach Lloyd（Warp CEO）、Isaac Evans（Semgrep CEO）、Gaspar Garcia（Vercel AI 研究负责人）和 Martin Casado（a16z 合伙人）等。"

[[params.faqItems]]
question = "学 CS146S 需要什么基础？"
answer = "需要 CS111 级别的编程基础，推荐有 CS221 或 CS229（机器学习）背景。这不是编程入门课，而是教有经验的开发者如何在整个软件开发生命周期中利用 AI。"

[[params.faqItems]]
question = "Vibe Coding 和 Agentic Engineering 有什么区别？"
answer = "Vibe Coding 侧重个人生产力——向 AI 描述需求，接受生成的代码。Agentic Engineering 是 Karpathy 2026 年提出的进化概念，强调编排多个 AI Agent 覆盖整个工程流程，配合更多的监督和审查机制。"
+++

从 Andrej Karpathy 在 2025 年 2 月发推提出 [Vibe Coding](/zh/posts/ai/2026-02-22-vibe-coding-guide/)，到斯坦福大学在同年秋季正式开设 CS146S 课程，前后不到 8 个月。一个社交媒体上的热词，以这样的速度进入全球顶级高校的课程体系，在计算机科学的历史上极为罕见。

这不是一门"教你用 ChatGPT 写代码"的水课。CS146S 覆盖了从 LLM 原理到 Agent 架构、从上下文工程到安全攻防、从自动化构建到生产运维的完整软件工程生命周期。它的嘉宾名单读起来像一份 AI 编程领域的"名人堂"——Claude Code 创始人、Vercel AI 研究负责人、Semgrep CEO、a16z 合伙人……

**最关键的是，所有课程资源——PPT、阅读材料、作业代码——全部免费公开。**

这篇文章将完整拆解这门课程的每一个模块，帮你建立系统认知。后续系列文章将对其中最有价值的几个主题做深度精读。

## 课程基本信息

| 项目 | 详情 |
|------|------|
| **课程编号** | CS146S |
| **课程名称** | The Modern Software Developer |
| **开课学校** | Stanford University |
| **学期** | Fall 2025（首次开课） |
| **讲师** | Mihail Eric |
| **助教** | Febie Lin, Brent Ju |
| **学分** | 3 units |
| **前置要求** | CS111 等效编程经验，推荐 CS221/229 |
| **课程官网** | [themodernsoftware.dev](https://themodernsoftware.dev) |
| **作业代码** | [GitHub 仓库](https://github.com/mihail911/modern-software-dev-assignments) |

课程的核心论题写在简介第一段：

> In the last few years, large language models have introduced a revolutionary new paradigm in software development. The traditional software development lifecycle is being transformed by AI automation at every stage, raising the question: **how should the next generation of software engineers leverage these advances to 10x their productivity and prepare for their careers?**

注意关键词："every stage"和"10x"。这门课不是教你用某个工具，而是教你如何**用 AI 重构整个软件开发生命周期**。

## 为什么这门课的出现是个拐点

在 CS146S 之前，Vibe Coding 的学习路径基本靠自学——看博客、刷推特、试工具。各路大神各有各的最佳实践，但缺乏**系统性的知识框架**。

斯坦福这门课改变了什么？

**第一，它定义了"现代软件开发者"的知识版图。** 10 周的课程大纲，实际上是对"AI 时代的软件工程到底包含哪些维度"的一次完整回答。从 Prompt Engineering 到 Agent 架构、从 Context Engineering 到 Secure Coding、从 Code Review 到 Post-Deployment——这是一个闭环。

**第二，它拉高了 Vibe Coding 的门槛。** 很多人以为 Vibe Coding 就是"跟 AI 聊天写代码"，但 CS146S 的课程结构清楚地表明：Vibe Coding 远不止于此。你需要理解 LLM 的工作原理、Agent 的架构设计、上下文的管理策略、安全的攻防边界、代码的质量保障、系统的运维监控。这些构成了一个完整的**工程学科**。

**第三，它预判了行业的演进方向。** 就在课程开设的同时，Karpathy 提出了 Agentic Engineering 的概念——从 Vibe Coding 进化到指挥一群 AI Agent 完成整个工程流程。CS146S 的后半段（Agent 模式、安全、运维）恰好在教这件事。

## 10 周课程全拆解

### Week 1：LLM 与 AI 编程入门

**主题**：Course logistics / What is an LLM actually / How to prompt effectively

第一周从根基讲起：LLM 到底是什么？它为什么会犯错？怎么引导它稳定输出？

这不是随便聊聊"写个好 prompt"的泛泛之谈。课程的阅读材料包括 Andrej Karpathy 长达数小时的 [Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI)，Google 的 [Prompt Engineering Overview](https://cloud.google.com/discover/what-is-prompt-engineering)，以及 OpenAI 关于 [如何内部使用 Codex](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf) 的论文。

**作业**：搭建一个 [LLM Prompting Playground](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week1)——把 Prompt Engineering 从"感觉对了就行"变成可量化、可复现的实验。

**核心认知**：大多数人只把 Prompt Engineering 当"技巧"，但 CS146S 把它当"科学方法论"来教。你需要有实验思维——提出假设、设计 prompt、观察结果、迭代优化。

### Week 2：Coding Agent 解剖学

**主题**：Agent architecture and components / Tool use and function calling / [MCP (Model Context Protocol)](/zh/posts/ai/2026-02-20-mcp-protocol-guide/)

如果说第一周教你"怎么跟 LLM 对话"，第二周教你"怎么给 LLM 装上手脚"。

Agent 不是一个聪明的聊天机器人，而是一个**带工具的自主系统**。这周深入讲解 Agent 的核心组件：感知（理解任务）、规划（分解步骤）、执行（调用工具）、反馈（评估结果）。

重点是 MCP（Model Context Protocol）。阅读材料覆盖了 MCP 的方方面面：

- [MCP 入门介绍](https://stytch.com/blog/model-context-protocol-introduction/)
- [MCP Server 实现示例](https://github.com/modelcontextprotocol/servers)
- [MCP Server 认证](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication)
- [MCP Server SDK](https://github.com/modelcontextprotocol/typescript-sdk/tree/main)
- 以及一篇令人深思的 [MCP 反思文章](https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/)："API 不一定能直接变成好的 MCP 工具"

**作业**：[动手搭建一个 MCP Server](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week2)。不是看教程，是自己从零写一个。

**核心认知**：MCP 正在成为 AI 编程的"USB 接口"——标准化的工具连接协议。理解 MCP 不是可选项，而是必修项。

### Week 3：AI IDE 与上下文工程

**主题**：Context management and code understanding / PRDs for agents / IDE integrations and extensions

**这是我认为整门课最重要的一周。**

上下文工程（Context Engineering）正在取代 Prompt Engineering 成为新的核心能力。原因很简单：单条 Prompt 的优化已经触顶，真正决定 AI 代码质量的是你**给它提供什么上下文**。

阅读材料堪称豪华：

- **[Specs Are the New Source Code](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code)**——这篇文章提出一个颠覆性观点：在 AI 编程时代，代码只是规格说明的"有损投影"，真正的源代码是你的 Spec/PRD。Andrew Ng 甚至说现在组织需要的 PM 数量是工程师的两倍。
- **[How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)**——揭示了四种上下文失败模式：上下文中毒（错误信息被反复引用）、上下文分心（超过 100K token 后模型倾向于重复历史行为）、上下文混淆（过多工具定义导致性能下降）、上下文冲突（矛盾信息导致性能暴跌 39%）。
- **[Getting AI to Work In Complex Codebases](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)**——实战指南，教你如何在复杂代码库中做上下文管理。
- Anthropic 的 **[Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)**——五条工具设计原则：精选而非全包、命名空间分组、返回语义化数据、token 效率优先、工具描述即性能杠杆。

**嘉宾**：[Silas Alberti](https://www.linkedin.com/in/silasalberti/)，Cognition（Devin）Head of Research。

**作业**：[搭建自定义 MCP Server](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week3/assignment.md)，并配合 Design Doc 模板进行上下文驱动的开发。

**核心认知**：从 Prompt Engineering 到 Context Engineering，这是 AI 编程范式的第二次跃迁。好代码是好上下文的副产品。

> 关于上下文工程的深度解读，请看系列第 2 篇：[斯坦福 CS146S 精读（二）：上下文工程](/zh/posts/ai/2026-02-24-context-engineering-deep-dive/)

### Week 4：Coding Agent 模式

**主题**：Managing agent autonomy levels / Human-agent collaboration patterns

这周的核心问题是：**Agent 的自治度应该设到多高？人类应该在什么节点介入？**

阅读材料几乎是 [Claude Code](/zh/posts/ai/2026-01-14-claude-code-guide/) 生态的全景：

- **[How Anthropic Uses Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)**——Anthropic 内部如何使用自家工具的第一手材料
- **[Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)**——官方最佳实践
- **[Peeking Under the Hood of Claude Code](https://medium.com/@outsightai/peeking-under-the-hood-of-claude-code-70f5a94a9a62)**——深入 Claude Code 的内部机制
- **[Good Context Good Code](https://blog.stockapp.com/good-context-good-code/)**——StockApp 团队实现 2.5 倍生产力提升的上下文管理实践

**嘉宾**：**Boris Cherney**，Claude Code 创始人。这是整门课最重磅的嘉宾之一——直接从工具的创造者口中了解设计哲学。

**作业**：[使用 Claude Code 完成一个完整项目](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week4/assignment.md)。目标是训练你成为一个 Agent Manager——不是写代码的人，而是指挥 Agent 写代码的人。

**核心认知**：Devin 的 Agents 101 文档总结得很好：Agent 的自治度从简单任务（直接描述即可）到中等任务（预期节省 80% 时间但需要人类打磨）到复杂任务（需要多个检查点审查）。关键不在于 Agent 多强，而在于**你多会管理它**。

> 关于 Agent Manager 模式的深度解读，请看系列第 3 篇：[斯坦福 CS146S 精读（三）：Agent Manager](/zh/posts/ai/2026-02-24-agent-manager-patterns/)

### Week 5：现代终端

**主题**：AI-enhanced command line interfaces / Terminal automation and scripting

AI IDE 解决的是"写代码"的问题，AI 终端解决的是"跑代码、管系统"的问题。

这周介绍 [Warp](https://www.warp.dev/) 这类 AI 终端如何把命令行操作产品化。阅读材料包括 [Warp University](https://www.warp.dev/university)（系统学习资源）、[Warp vs Claude Code](https://www.warp.dev/university/getting-started/warp-vs-claude-code) 的定位对比，以及 [Warp 如何用 Warp 开发 Warp](https://notion.warp.dev/How-Warp-uses-Warp-to-build-Warp-21643263616d81a6b9e3e63fd8a7380c) 的 dogfooding 实践。

**嘉宾**：[Zach Lloyd](https://www.linkedin.com/in/zachlloyd/)，Warp CEO。

**作业**：[使用 Warp 完成 Agentic 开发任务](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week5)。

**核心认知**：终端不是"高级用户的玩具"，而是 AI 开发工作流的关键一环。Claude Code 本身就运行在终端中。

### Week 6：AI 测试与安全

**主题**：Secure vibe coding / History of vulnerability detection / AI-generated test suites

**这是整门课最硬核的一周。**

当 AI 帮你写代码时，谁来保证代码的安全性？这周直接上真实案例：

- **[GitHub Copilot 通过 Prompt Injection 实现远程代码执行](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)**——攻击者在源代码中植入恶意指令，操控 Copilot 修改 VS Code 配置文件，启用"YOLO 模式"（自动批准所有操作），然后执行任意终端命令。这不是理论推演，是真实的 CVE 漏洞。
- **[使用 Claude Code 和 Codex 发现 Web 应用漏洞](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/)**——Semgrep 团队在 11 个大型开源项目（800+ 万行代码）上测试，Claude Code 发现 46 个真实漏洞（14% 真正例率），但误报率高达 86%。更可怕的是"同一代码、同一 AI、不同结果"的非确定性问题。
- **[OWASP Top Ten](https://owasp.org/www-project-top-ten/)**——Web 应用安全的基础框架
- **[Context Rot 研究](https://research.trychroma.com/context-rot)**——随着输入长度增加，模型性能显著下降，即使是简单任务

**嘉宾**：[Isaac Evans](https://www.linkedin.com/in/isaacevans/)，Semgrep CEO。Semgrep 是全球最流行的静态分析安全工具之一。

**作业**：[编写安全的 AI 代码](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week6/assignment.md)。

**核心认知**：很多 AI 编程课只教你怎么写得快，这门课把**交付的底线**拉出来了：可测、可审、可防。

> 关于安全主题的深度解读，请看系列第 4 篇：[斯坦福 CS146S 精读（四）：Secure Vibe Coding](/zh/posts/ai/2026-02-24-secure-vibe-coding/)

### Week 7：代码审查与软件支持

**主题**：What AI code systems can we trust / Debugging and diagnostics / Intelligent documentation generation

第 7 周延续安全主题，聚焦一个核心问题：**AI 产出的代码，我们能信任到什么程度？**

阅读材料从经典的 [Code Reviews: Just Do It](https://blog.codinghorror.com/code-reviews-just-do-it/) 到 GitHub 工程师的 [How to Review Code Effectively](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/)，再到学术论文 [AI-Assisted Assessment of Coding Practices in Modern Code Review](https://arxiv.org/pdf/2405.13565)。

**嘉宾**：[Tomas Reimers](https://www.linkedin.com/in/tomasreimers/)，Graphite CPO。Graphite 是一个专注于代码审查和 PR 管理的开发者工具。他带来了 [百万次 AI Code Review 的经验教训](https://www.youtube.com/watch?v=TswQeKftnaw)。

**作业**：[Code Review 练习](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week7)——审查 AI 生成的代码，找出问题。

**核心认知**：AI 代码的审查不能照搬人类代码的审查方法。AI 生成的代码有独特的"味道"——表面看起来正确，但可能在边界条件、安全处理、性能优化上存在系统性盲区。

### Week 8：自动化应用构建

**主题**：Design and frontend for everyone / Rapid UI/UX prototyping and iteration

一句 Prompt 搞出一个端到端的完整应用——这是最"Vibe"的一周。

课上演示了如何用 AI 工具快速生成完整的 Web 应用，从设计到前端到后端一气呵成。

**嘉宾**：[Gaspar Garcia](https://www.linkedin.com/in/gaspargarcia/)，Vercel AI 研究负责人。Vercel 的 v0 是目前最强的 AI UI 生成工具之一。

**作业**：[多技术栈 Web 应用构建](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week8)——用 AI 生成不同技术栈的应用并对比。

**核心认知**：快速原型只是起点。课程真正想传达的是：你得能把这个原型**纳入测试、安全、Code Review 这些工程规范中**。很多人用 AI 做了 demo 就觉得大功告成，但从 demo 到 production 之间还有一道鸿沟。

> 关于从原型到生产的深度解读，请看系列第 5 篇：[斯坦福 CS146S 精读（五）：从原型到生产](/zh/posts/ai/2026-02-24-prototype-to-production/)

### Week 9：部署后运维

**主题**：Monitoring and observability for AI systems / Automated incident response / Triaging and debugging

很多人学 AI 编程只学"造"，不学"养"。这周把"养系统"补上了。

阅读材料从 Google 经典的 [SRE 入门](https://sre.google/sre-book/introduction/) 到 [可观测性基础](https://last9.io/blog/traces-spans-observability-basics/)，再到 Resolve AI 的系列文章——如何用 AI Agent 自动化 Kubernetes 故障排查、事件响应、值班工程。

**嘉宾**：[Mayank Agarwal](https://www.linkedin.com/in/mayank-ag/)（CTO）和 [Milind Ganjoo](https://www.linkedin.com/in/mganjoo/)（技术骨干），来自 [Resolve AI](https://resolve.ai/)——一个用多 Agent 系统自动化 DevOps 运维的公司。

**核心认知**：系统不是部署完就结束了。监控、告警、事件响应、自动化排查——这些在 AI 时代同样被 AI 重塑。你不仅用 AI 写代码，还要用 AI 守护代码。

### Week 10：AI 软件工程的未来

**主题**：Future of software development roles / Emerging AI coding paradigms / Industry trends and predictions

最后一周把前 9 周串起来，让你知道自己学的不是一堆零散技能，而是**一种新的工程范式**。

**嘉宾**：**[Martin Casado](https://a16z.com/author/martin-casado/)**，a16z（Andreessen Horowitz）合伙人。a16z 是全球最顶级的科技风投之一，投资了 GitHub、Databricks 等一系列开发者工具公司。Martin Casado 本人也是 VMware 联合创始人，对技术趋势有着深刻的洞察。

**核心认知**：软件开发在未来 10 年会变成什么样？当 AI 能做越来越多的实现工作时，人类开发者的核心价值在哪里？这周的讨论帮你建立长期的职业视角。

## 嘉宾阵容一览

| 周 | 嘉宾 | 身份 | 公司 |
|----|------|------|------|
| 3 | Silas Alberti | Head of Research | Cognition (Devin) |
| 4 | **Boris Cherney** | Creator of Claude Code | Anthropic |
| 5 | Zach Lloyd | CEO | Warp |
| 6 | Isaac Evans | CEO | Semgrep |
| 7 | Tomas Reimers | CPO | Graphite |
| 8 | Gaspar Garcia | Head of AI Research | Vercel |
| 9 | Mayank Agarwal & Milind Ganjoo | CTO & Technical Staff | Resolve AI |
| 10 | **Martin Casado** | General Partner | a16z |

这份名单覆盖了 AI 编程生态的各个关键层：代码生成（Anthropic）、自主开发（Cognition）、终端交互（Warp）、安全扫描（Semgrep）、代码审查（Graphite）、应用部署（Vercel）、系统运维（Resolve）、投资趋势（a16z）。

## 评分与作业体系

| 组成部分 | 占比 |
|----------|------|
| Final Project | 80% |
| Weekly Assignments | 15% |
| Class Participation | 5% |

Final Project 占 80%——这说明课程极度重视**实际动手能力**。不是考你记住了多少概念，而是你能不能真正用 AI 工具做出一个完整的项目。

## 如何免费学习这门课

虽然你不是斯坦福的学生，但这门课的几乎所有资源都是公开的：

1. **课程官网**：[themodernsoftware.dev](https://themodernsoftware.dev) — 完整大纲、每周主题和阅读材料
2. **PPT 幻灯片**：每节课都有 Google Slides 链接，可直接在线查看
3. **阅读材料**：所有推荐阅读都是公开链接，包括论文、博客、视频
4. **作业代码**：[GitHub 仓库](https://github.com/mihail911/modern-software-dev-assignments)（2.1K Stars），Python 为主，配有完整的环境搭建指南
5. **嘉宾演讲 Slides**：部分嘉宾的 PPT 也已公开

**建议学习路径**：

1. 先通读一遍课程大纲，建立全局认知
2. 按周顺序学习，每周先看 PPT，再读 Reading，最后做 Assignment
3. 重点攻克 Week 3（上下文工程）和 Week 6（安全）——这两周的信息密度最高
4. 最后尝试做一个完整的 Final Project，综合运用所学

## 全球高校跟进情况

CS146S 不是孤例。Vibe Coding 正在全球高校遍地开花：

- **Stanford Continuing Studies** 另外开设了面向非 CS 专业的 [Vibe Coding: Building Software in Conversation with AI](https://continuingstudies.stanford.edu/courses/detail/20253_TECH-36) 课程
- **Stanford IT 部门** 为内部员工开设了 [Vibe Coding for Developers: Building with Agents in Cursor](https://uit.stanford.edu/service/techtraining/class/vibe-coding-developers-building-agents-cursor) 培训
- **复旦大学** 2026 年春季开设《生成式软件开发》，面向非计算机专业学生
- **中山大学** 冬令营引入《Vibe Coding 编程入门》，教高中生用 AI 编程
- **Codecademy** 推出了 [Intro to Vibe Coding](https://www.codecademy.com/learn/intro-to-vibe-coding) 在线课程
- **Coursera** 上线了 [Vibe Coding for Beginners](https://www.coursera.org/learn/vibe-coding-for-beginners-from-zero-to-app)

## 从 Vibe Coding 到 Agentic Engineering

CS146S 的课程结构暗合了一个更大的叙事：Vibe Coding 只是起点，终点是 **[Agentic Engineering](/zh/posts/ai/2026-02-23-agentic-coding-trends-2026/)**。

课程的前半段（Week 1-5）教你如何作为个体用 AI 编程工具提效——这是 Vibe Coding 的基本形态。后半段（Week 6-10）转向工程体系：安全、审查、构建、运维、趋势——这是从个人生产力到组织级工程范式的跃迁。

正如 Karpathy 在 2026 年 2 月的新推文中所说：Agentic Engineering 是 Vibe Coding 的进化形态。以前是让 AI 帮你写代码，以后是你指挥一群 AI Agent 完成整个软件工程的全流程。

而 CS146S 恰好就是在系统性地教这件事。

## 相关阅读

如果你对 Vibe Coding 和 AI 编程工具的实战感兴趣，推荐这些文章：

- [Claude Code 从入门到精通完全指南](/zh/posts/ai/2026-01-14-claude-code-guide/) — 课程中高频提及的核心工具
- [Vibe Coding 完全指南](/zh/posts/ai/2026-02-22-vibe-coding-guide/) — Vibe Coding 的理念、工具与实战
- [MCP 协议全面解析](/zh/posts/ai/2026-02-20-mcp-protocol-guide/) — Week 2-3 核心主题的深入解读
- [CLAUDE.md 记忆术](/zh/posts/ai/2026-01-12-claudemd-memory-guide/) — 理解 AI 编程助手的项目感知机制
- [2026 Agentic Coding 趋势报告](/zh/posts/ai/2026-02-23-agentic-coding-trends-2026/) — 从 Vibe Coding 到 Agentic Engineering 的演进
- [Claude Code Hooks 实战指南](/zh/posts/ai/2026-02-18-claude-code-hooks-guide/) — Claude Code 的自动化扩展能力
- [2026 秋季 5 门免费大学 AI Agent 课怎么跟：斯坦福、CMU、MIT](/zh/posts/ai/2026-09-14-free-ai-agent-courses-fall-2026/) — CS146S 和 CMU 11-768、CS329Z、CS329A、MIT 多模态课怎么搭配着跟

## 系列文章导航

这是「斯坦福 Vibe Coding 课程精读」系列的第 1 篇。后续文章将对课程中最有价值的主题做深度解读：

1. **本文**：斯坦福 CS146S 精读（一）：Vibe Coding 如何成为正式学科
2. [斯坦福 CS146S 精读（二）：上下文工程](/zh/posts/ai/2026-02-24-context-engineering-deep-dive/)（Week 3）
3. [斯坦福 CS146S 精读（三）：Agent Manager](/zh/posts/ai/2026-02-24-agent-manager-patterns/)（Week 4）
4. [斯坦福 CS146S 精读（四）：Secure Vibe Coding](/zh/posts/ai/2026-02-24-secure-vibe-coding/)（Week 6-7）
5. [斯坦福 CS146S 精读（五）：从原型到生产](/zh/posts/ai/2026-02-24-prototype-to-production/)（Week 8-9）

课程资源全部免费公开，你需要的只是行动力。
