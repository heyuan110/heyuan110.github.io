+++
date = '2026-04-01T14:00:00+08:00'
draft = false
title = 'Cursor Composer 2 深度评测：Kimi K2.5 风波背后的真相与启示'
description = 'Cursor Composer 2 深度评测：2026 年 3 月 19 日发布，三天后被发现底座是月之暗面 Kimi K2.5，75% 算力做 RL 的说法站得住吗？Terminal-Bench 61.7 对 Claude Opus 4.6 的 58.0，跑分、争议与实战体验全拆解。'
toc = true
tags = ['Cursor', 'Composer 2', 'AI Coding Tools', 'Kimi K2.5', 'Claude Code']
keywords = ['Cursor Composer 2 评测', 'Kimi K2.5 争议', 'Composer 2 对比 Claude Code', 'AI 编程工具 2026', '月之暗面']
+++

![Cursor Composer 2 — 当西方产品遇上东方底座模型](cover.webp)

2026 年 3 月 19 日，Cursor 高调发布了 Composer 2。更快、更聪明、更便宜——发布稿用了所有你能想到的溢美之词。三天后，一位叫 Fynn 的开发者在 API 配置中发现了一个有趣的模型标识符：`kimi-k2p5-rl-0317-s515-fast`。

这串字符把 Cursor 推到了风口浪尖。一个估值 500 亿美元的公司，用了中国公司的开源模型做底座，却在发布时只字不提——这事搁谁身上都说不过去。

## Composer 2 到底是什么

先抛开争议谈技术。Composer 2 是 Cursor 自研的编程模型，旨在取代 IDE 中调用的第三方模型（Claude、GPT），提供原生的代码编辑体验。[技术报告](https://cursor.com/blog/composer-2-technical-report)描述了两阶段训练：

**第一阶段：继续预训练。** 在底座模型上用代码密集的数据做进一步预训练，夯实模型的编码能力。报告写道："降低预训练损失能改善下游 RL 表现，更好的底座知识能可靠地转化为更好的 Agent。"

**第二阶段：大规模强化学习。** 使用 Anyrun（Cursor 内部管理的沙盒编码环境平台，规模达数十万个）在真实的 Cursor 会话中做 RL 训练。训练用的工具、执行环境和线上部署完全一致，问题分布覆盖了开发者日常使用 Composer 的全部场景。

基础设施层面，训练需要针对 MoE（混合专家）架构定制的低精度算子，在 NVIDIA Blackwell GPU 上运行；还有跨多个区域的全异步 RL 流水线。

技术上确实有干货。问题是那个"底座模型"——是月之暗面的 **Kimi K2.5**，而原始发布稿对此只字未提。

## 月之暗面与 Kimi K2.5

对国内读者来说，[月之暗面](https://www.moonshot.cn/)不需要过多介绍。阿里和红杉中国（HongShan）投资的明星公司，Kimi 大模型在国内用户量巨大。2026 年初发布的 Kimi K2.5 是一个开源 MoE 模型，编码能力强，推理效率高，商业许可也比较宽松。

但许可证有一个关键条款：**月活超过 100 万或月收入超过 2000 万美元的产品，必须在显著位置标注来源。**

Cursor 的年化收入约 20 亿美元。远超门槛。他们不仅应该标注，而且是有法律义务标注。

## 穿帮经过

- **3 月 19 日**：Cursor 发布 Composer 2，博客通篇不提 Kimi。
- **3 月 21 日**：开发者 Fynn 在 API 配置中发现 `kimi-k2p5-rl-0317-s515-fast`，发到 X 上。
- **3 月 22 日**：[TechCrunch 报道](https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/)，Cursor 联合创始人 Aman Sanger 回应："没在博客里提到 Kimi 底座是我们的疏忽。"
- **3 月 22-23 日**：Cursor 补充更新了博客和技术报告，加上了 Kimi K2.5 的署名。

Cursor 产品副总裁 Lee Robinson 的说法是：大约 **75% 的算力** 花在了 Cursor 自己的继续预训练和 RL 上，只有 25% 来自底座模型。言下之意：Composer 2 主要是我们自己的成果。

这个说法经不起推敲。

## 75/25 的说法站不住脚

花了 75% 的算力做微调，不代表底座模型不重要。打个比方：你花了 75% 的装修预算翻新一栋房子，难道就不需要告诉买家谁打的地基？

底座模型提供的是：

- **核心的语言理解与生成能力**
- **MoE 架构**——Composer 2 高效推理的根基
- **基础编码知识**——RL 在此之上做专项优化

Cursor 的 RL 训练确实有价值，它让模型学会在 Cursor 的工具链中高效工作。但 RL 不能凭空造出能力，它只能精炼和引导底座模型已有的知识。技术报告自己也承认了这一点。

## 跑分：真实但需要语境

| 基准测试 | Composer 2 | Composer 1.5 | Claude Opus 4.6 |
|---------|-----------|--------------|-----------------|
| CursorBench | 61.3 | 44.7 | — |
| SWE-bench Multilingual | 73.7 | — | — |
| Terminal-Bench 2.0 | 61.7 | — | 58.0 |

几个注意点：

**CursorBench 是 Cursor 自己的基准测试。** 在 Cursor 环境中，用 Cursor 的工具，测 Cursor 专门训练过的模型——这成绩好看不奇怪。

**Terminal-Bench 相对中立**，61.7 对 Claude Opus 4.6 的 58.0，领先 3.7 个百分点。统计意义上有效，单次使用中几乎感受不到差异。

**SWE-bench Multilingual 73.7** 是扎实的成绩，这个基准测试跨语言、测真实 bug 修复，比较难刷。

**20 万 token 上下文窗口** 够用，但跟 Claude Code 的 100 万 token 比起来，处理大型项目时会捉襟见肘。

## Composer 2 对比 Claude Code：实战体验

两个工具我都深度使用过。如果你看过我之前写的 [AI 编程工具对比](/posts/ai/2026-02-18-claude-code-vs-cursor-vs-windsurf-2026/)，你知道我更看重实际体验而非跑分。

### Cursor Composer 2 赢在哪里

- **日常编码速度快。** 补全、小改动、行内建议——在 Cursor IDE 里 Composer 2 响应飞快，上下文切换少。
- **成本低。** 标准模式 $0.50/M 输入 token，快速模式 $1.50/M，比前沿模型便宜一个数量级。团队日常高频使用省钱明显。
- **IDE 原生体验。** 多文件编辑、行内 diff、Agent 循环——都是为这个模型量身定制的。

### Claude Code 赢在哪里

- **深度代码理解。** [100 万 token 上下文窗口](/posts/ai/2026-01-14-claude-code-guide/)意味着能把整个代码库装进记忆。大型重构、架构调整、跨文件 debug——这不是锦上添花，是刚需。
- **复杂推理。** [Claude Code + Opus 4.6](/posts/ai/2026-03-13-gpt-5-4-vs-claude-opus-comparison/) 处理多步推理链的能力是 Composer 2 做不到的。安全审计、架构决策、细致的权衡分析。
- **终端原生。** Claude Code 跑在终端里，不绑定编辑器，跟 git 深度集成，支持 [Agent Teams](/posts/ai/2026-02-22-claude-code-agent-teams/) 并行执行。
- **透明度。** 你清楚知道自己在用什么模型，没有任何遮掩。

### 2026 年的最佳组合

我认识的高效开发者大多两个都用：

- **Cursor + Composer 2** 负责 80% 的日常工作——快速编辑、常规实现
- **Claude Code** 负责 20% 的硬骨头——复杂调试、大型重构、[安全分析](/posts/ai/2026-02-22-claude-code-security/)、架构决策

这不是非此即彼的竞争。两个工具解决不同层次的问题。

## 定价：Composer 2 的最大优势

| 模型 | 输入（标准） | 输入（快速） | 输出（标准） | 输出（快速） |
|------|------------|------------|------------|------------|
| Composer 2 | $0.50/M | $1.50/M | $2.50/M | $7.50/M |
| Claude Opus 4.6 | $15/M | — | $75/M | — |
| Claude Sonnet 4.5 | $3/M | — | $15/M | — |

Composer 2 输入 token 价格只有 Opus 4.6 的 1/30。高频使用场景下省钱效果显著。但便宜不等于更好——该用前沿模型做深度推理的场景，省这点钱反而亏时间。

## 更大的图景：中国模型驱动西方产品

Composer 2 事件是一个趋势的缩影。月之暗面、DeepSeek、阿里通义千问——中国 AI 实验室正在产出越来越有竞争力的开源模型。西方公司基于这些模型构建产品，面临三重张力：

1. **经济上合理**：用最好的底座模型，不问出处，能做出更好、更便宜的产品。
2. **政治上敏感**：在 AI 出口管制和地缘博弈的背景下，承认用了中国模型做底座，市场团队压力不小。
3. **伦理上必须**：开源许可证的存在是有原因的。署名不是可选项。

Cursor 选了经济上合理的路，却在伦理上栽了跟头。更讽刺的是，他们其实跟 Fireworks AI 有正式的商业合作来使用 Kimi K2.5——明明有合法渠道，偏偏不愿意公开说。

这不会是最后一次。随着中国开源模型持续进步，会有更多西方 AI 公司在此基础上构建产品。主动透明的公司会赢得信任，遮遮掩掩的公司迟早被揭穿。

## 该不该用 Composer 2

**该用，但要心里有数。** 模型本身确实好用，争议不改变它的技术能力。

但你需要清楚自己买的是什么：

- 一个底座来自中国开源项目的模型（这本身没问题，知道就好）
- 一家被抓住才承认的公司（这值得记住）
- 一个绑定 IDE 的封闭体验
- 好看的跑分里有"主场优势"的成分

2026 年最好的 AI 编程体验，不是选边站，而是搭建适合自己的[工具组合](/posts/ai/2026-01-19-ai-dev-workflow/)。Composer 2 在这个组合里有一席之地。只是它没有资格假装一切都是自己从零做起的。

## 核心要点

1. **Composer 2 确实好用。** 跑分虽有语境限制，但改进是真实的，定价很有竞争力。
2. **署名遗漏是选择，不是疏忽。** Cursor 这个体量的公司不会"不小心"忘记标注底座模型。
3. **75/25 算力比是误导性框架。** 算力占比不等于贡献占比，底座模型是根基。
4. **Cursor 和 Claude Code 都该用。** 前者拼速度，后者拼深度。
5. **趋势值得关注。** 中国开源模型驱动西方产品，这个趋势会加速，透明度将成为竞争分水岭。

---

*更多 AI 编程工具的深度内容，请阅读 [Claude Code 完全指南](/posts/ai/2026-01-14-claude-code-guide/) 和 [AI 编程代理横评](/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/)。*

## 相关阅读

- [Cursor 完全指南 2026：从安装到高级 Agent 模式实战](/zh/posts/ai/2026-03-08-cursor-setup-guide/) — Cursor 的完整上手路径
- [Cursor Agent 编码最佳实践：官方指南完整解读](/zh/posts/ai/2026-01-19-cursor-agent-best-practices/) — Cursor Agent 的使用范式
- [Claude Code vs Cursor 2026：哪个 AI 编程工具更强？](/zh/posts/ai/2026-02-28-claude-code-vs-cursor/) — Composer 2 的直接对手
- [2026 年 AI 编程工具全面对比：7 款主流工具实测评析](/zh/posts/ai/2026-03-10-ai-coding-agents-comparison-2026/) — Composer 2 在横评中的位置
- [GPT-5.4 vs Claude Opus 4.6 终极对比 2026](/zh/posts/ai/2026-03-13-gpt-5-4-vs-claude-opus-comparison/) — 底座模型层面的对比参考
