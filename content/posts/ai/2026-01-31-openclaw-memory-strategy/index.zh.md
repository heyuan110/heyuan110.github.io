+++
date = '2026-01-31T08:20:18+08:00'
draft = false
title = 'OpenClaw 记忆实施策略解析：工具驱动的 RAG 与"按需回忆"'
description = '解析 OpenClaw 的记忆实施策略：不把记忆自动注入 prompt，而是通过 memory_search/memory_get 工具按需检索；结合 BM25+向量检索、chunks 表设计与会话增量索引机制。'
toc = true
tags = ['OpenClaw', 'RAG', '向量检索', 'Agent', '记忆系统']
categories = ['AI原理']
keywords = ['OpenClaw 记忆', 'memory_search', 'RAG', 'BM25', '向量数据库', 'Agent 工具调用']
+++

![OpenClaw 记忆实施策略封面图](cover.webp)

## 一、背景：为什么"记忆"成了 Agent 的标配

这两年大家对 Agent 的期待越来越一致：

- 不仅能对话，还要能**长期记住你是谁**（用户画像、偏好、项目上下文）
- 不仅能记住，还要能**在需要时拿出来用**（而不是每轮都塞进上下文浪费 token）

很多 Character AI / Chatbot 的做法是维护一份长期 Profile，每轮把它拼进 system prompt。

但 OpenClaw 走了一条更"工具化"的路：**不自动注入记忆，而是把回忆过程交给 Agent，通过工具按需检索**。

本文聊聊 OpenClaw 的记忆实施策略，以及它对我们做 Agent 系统设计有什么启发：

## 二、核心观点：OpenClaw 的"记忆"不是 Prompt 拼接，而是 Tool 驱动

OpenClaw 的记忆检索主要通过两个工具完成：

- `memory_search`：语义搜索（通常是 BM25 + Vector Search 组合）
- `memory_get`：根据命中结果（文件路径 + 行范围）精确取回文本片段

换句话说：

> 记忆系统不是"每轮自动塞一坨"，而是"需要时才查、查到后只取必要片段"。

这会带来两个直接好处：

1) **省 token**：没有必要把一堆不相关的历史塞进每轮上下文
2) **更符合 Agent**：把"什么时候需要记忆、需要什么记忆"变成一个可决策动作

## 三、索引策略：不仅索引聊天，还索引工作区生成的文档

推文里提到一个很容易被忽略但很关键的点：

- OpenClaw 会对工作区生成的 `.md` 文件做 chunks 并进入 Memory 索引

这意味着"记忆"不仅来自对话，还来自 Agent 产出的结构化成果（笔记、文章、总结、SOP）。

这很像一个靠谱同事：

- 你问他上次怎么做的，他不是去翻聊天记录
- 而是去翻"上次写的文档/总结"

## 四、数据模型：文本与向量分离、全文检索与向量检索并存

从实现上看，这是一套很典型、也很工程友好的 RAG 数据分层：

- `chunks`：存文本（路径、行范围、text、source 等元信息）
- `chunks_vec`：存向量
- `chunks_fts`：存全文检索索引（FTS）

这类设计的优势在于：

- **可解释**：命中结果能回到具体文件与行号
- **可调优**：BM25/FTS 与向量召回可以混合、加权、做 rerank
- **可审计**：出了问题能定位"到底记了什么"

## 五、会话增量索引：把 JSONL 当成可持续增长的事实来源

推文还提到会话数据是 `.jsonl` 形式，并且会做"增量 chunks"：

- 监控 jsonl 变化
- 增量到达阈值后读取增量并索引

这里有个有意思的点：在很多系统里，"压缩历史"（例如 `/compact` 生成摘要）会导致旧消息被替换或删除。

OpenClaw 选择把"原始会话（以及摘要后的会话）"纳入可索引的事实来源，背后的取舍可能是：

- 记忆系统更像"日志检索"，而不是"完美的人设记忆"
- 摘要是一种压缩手段，但并不要求每轮都把它放进上下文

## 六、对我们做 Agent 的启发：把记忆变成"可调用能力"，而不是"默认负担"

我觉得最有启发的一句话是：

> OpenClaw 没有把记忆块自动拼进 system prompt 或每轮上下文；全部按需、Tool 驱动。这才是真正交给了 Agents。

如果用生活化的比喻：

- **自动注入**像是你每说一句话，就有人把"你一生的履历"念一遍
- **工具检索**像是你需要时去翻笔记/搜聊天/查文档

后者显然更符合现实，也更符合规模化落地。

## 七、一个实用建议：如何用好这种"按需回忆"机制

如果你也在做类似系统，可以考虑：

1) 把"长期偏好"写成明确的文件（Profile / MEMORY.md），让 Agent 有稳定锚点
2) 对产出的文档做索引（而不是只索引对话）
3) 让 Agent 学会：
   - 先判断是否需要回忆
   - 再决定搜什么关键词
   - 最后只取回需要的片段

## 总结

OpenClaw 的记忆策略整体给人的感觉是：**极简、工程化、把主动权交给 Agent**。

- 记忆不是"魔法 prompt"，而是一套可检索的知识底座
- 不追求每轮自动注入，而是追求"需要时能找回、且可解释"

如果你正在构建自己的 Agent 系统，这种思路非常值得借鉴。

---

### 参考链接

- 推文：<https://x.com/Stephen4171127/status/2017224470818160658>
- OpenClaw Docs：<https://docs.openclaw.ai/>

## 相关阅读

- [OpenClaw 超详细上手教程：小白友好 + 老鸟技巧](/zh/posts/ai/2026-02-12-openclaw-usage-tutorial/) — OpenClaw 整体上手
- [OpenClaw 多 Agent 配置实战：别让 LLM 做编排](/zh/posts/ai/2026-04-02-openclaw-multi-agent-setup-guide/) — 进阶的多 Agent 编排
- [OpenClaw vs AutoGPT vs CrewAI：2026 年最佳个人 AI Agent 全面对比](/zh/posts/ai/2026-03-05-openclaw-vs-ai-agents/) — 放回竞品里比较
- [AI Agent 记忆系统全解析：RAG 与上下文工程的对比与选择](/zh/posts/ai/2026-02-21-ai-agent-memory-systems/) — 跨产品看 Agent 记忆方案
- [QMD：本地语义搜索引擎，帮 AI Agent 省下 90% Token 开销](/zh/posts/ai/2026-03-25-qmd-local-search-ai-agent-memory/) — 本地化记忆的另一条路径
