+++
date = '2026-03-25T10:00:00+08:00'
draft = false
title = 'QMD：本地语义搜索引擎，帮 AI Agent 省下 90% Token 开销'
description = 'QMD 是 Shopify CEO Tobi Lütke 开源的本地语义搜索引擎：BM25 + 向量检索 + LLM 重排序三层架构，全部本地运行、模型总共不到 2GB，让 AI Agent 按需精准回忆，Token 开销直降 90%。附搜索管线拆解与安装使用指南。'
toc = true
tags = ['AI Agent', 'MCP', 'Token Optimization', 'RAG']
keywords = ['QMD 本地搜索', 'AI Agent Token 优化', '语义搜索引擎', 'MCP 记忆服务器', '减少 Token 消耗', 'AI 成本优化']
+++

![QMD 本地语义搜索引擎——AI Agent 记忆优化利器](cover.webp)

用过 AI Agent 的人都有一个共同的痛：**Token 烧得飞快**。聊不到几轮，Claude 就告诉你 hit limit 了；看看账单，OpenAI 的额度也在哗哗往下掉。

问题出在哪？绝大多数 Agent 处理记忆的方式太粗暴——不管你问什么，先把 MEMORY.md、项目文档、历史对话统统塞进上下文窗口。这就像你去图书馆找一本书，管理员把整个书架搬到你面前说"自己翻"。

**QMD** 做的事情很简单：当 Agent 需要回忆时，不再搬书架，而是直接把你要的那一页翻到面前。Token 消耗直降 90%，回答精准度反而更高。

## QMD 是什么？凭什么这么能打？

[QMD](https://github.com/tobi/qmd)（Query Markup Documents）是一个完全运行在本地的搜索引擎，开发者是 [Tobi Lütke](https://x.com/tobi)——没错，就是 Shopify 的联合创始人兼 CEO。这位大佬自己日常重度使用 AI Agent，受不了 Token 浪费的问题，于是亲手撸了这个工具。

QMD 的核心是**三层混合搜索**：

| 层级 | 技术 | 作用 |
|------|------|------|
| 第一层 | **BM25 全文检索** | 关键词精确匹配——找到包含你搜索词的文档 |
| 第二层 | **向量语义搜索** | 基于 Embedding 的相似度匹配——理解你问的"意思" |
| 第三层 | **LLM 重排序** | 用大模型对结果重新打分——挑出真正有用的 |

三层都跑在本地，通过 [node-llama-cpp](https://github.com/withcatai/node-llama-cpp) 加载 GGUF 格式的小模型。**零 API 调用，零云端成本，无限次搜索全免费。**

打个比方：BM25 是按书名找书的图书管理员，向量搜索是能听懂你描述"那本讲某个概念的书"的聪明馆员，LLM 重排序则是经验丰富的老馆长，在两人的推荐中挑出最值得看的几本。三个人配合，比任何一个人单干都强。

### 三个默认模型

QMD 内置三个精心挑选的 GGUF 模型：

| 模型 | 用途 | 大小 |
|------|------|------|
| `embeddinggemma-300M-Q8_0.gguf` | 文本向量化 | ~300MB |
| `qwen3-reranker-0.6b-q8_0.gguf` | 结果重排序 | ~600MB |
| `qmd-query-expansion-1.7B-q4_k_m.gguf` | 查询扩展 | ~1GB |

首次运行自动下载，之后完全离线。总共不到 2GB，换来的是无限免费的语义搜索能力。

## 搜索管线深度拆解

很多介绍 QMD 的文章只告诉你怎么装、怎么用，但不讲清楚它到底是怎么工作的。理解搜索管线的原理，能帮你更好地调优和排障。

### 第一步：查询扩展

当你输入 `qmd query "怎么处理用户认证"` 时，查询扩展模型会把你的问题"展开"成多个子查询：

- **词法子查询**：`"authentication" "auth" "login" "token"`（给 BM25 用）
- **语义子查询**：`"用户身份验证和会话管理的实现方式"`（给向量搜索用）
- **HyDE 子查询**：假设存在一篇完美回答你问题的文档，生成它的摘要（让 Embedding 匹配更精准）

为什么要这样做？因为同一个概念在不同文档中的表达方式千差万别。"认证"可能写成 auth、authentication、login、sign-in……单一查询根本覆盖不了所有写法。

### 第二步：双路并行检索

两个搜索后端同时开跑：

```
原始查询（×2 权重）+ 扩展查询
         ↓                    ↓
    BM25 关键词检索       向量语义检索
         ↓                    ↓
    关键词匹配结果       语义相似结果
         ↓                    ↓
         └──── RRF 融合排序 ────┘
                    ↓
            Top-30 候选文档
```

**RRF（Reciprocal Rank Fusion）** 把两路结果合并排序。同时出现在两个列表中的文档会被加分。原始查询享有 2 倍权重，防止扩展查询的结果把你真正想找的东西淹没。

这里有一个精妙的设计：**Top-Rank 加分**。如果某个文档在原始查询中排名第一，即使扩展查询的结果把它挤到了后面，它仍然会被保留在高位。这避免了"搜索越智能，精确匹配反而丢失"的经典问题。

### 第三步：LLM 重排序

Top-30 候选文档会被送给 Qwen3 Reranker——一个专门做相关性打分的小模型。它会逐一阅读每个文档片段，判断它和你的问题有多相关，然后重新排序。

最终输出使用**位置感知混合**策略：在重排序得分和检索得分之间做加权平衡。这防止了重排序模型"矫枉过正"——有时候关键词精确匹配的文档确实就是最好的结果，不应该被语义相似但不完全匹配的文档超越。

### 智能文档切片

大多数搜索工具按固定 Token 数切割文档（比如每 512 个 Token 切一刀）。这经常会把段落、代码块、甚至函数定义从中间切断，让搜索结果变得残缺不全。

QMD 用评分算法寻找 **Markdown 的自然断点**：

- 完整段落不会被拆开
- 代码块绝不会从函数中间切断
- 标题 + 正文作为整体保留

结果就是：搜索返回的每个片段都是一个完整的语义单元，Agent 可以直接使用，不需要再去读上下文。

## 10 分钟上手：从安装到跑通

### 安装 QMD

需要先装 [Bun](https://bun.sh/)（推荐）或 Node.js 20+：

```bash
# 安装 Bun
curl -fsSL https://bun.sh/install | bash

# 全局安装 QMD
bun install -g @tobilu/qmd
```

首次运行会自动下载三个 GGUF 模型（约 2GB），下载完成后完全离线运行。

### 创建记忆库

```bash
# 进入项目目录
cd ~/my-project

# 注册文档集合
qmd collection add ./docs --name project-docs --mask "**/*.md"

# 生成向量（语义搜索必需）
qmd embed

# 查看状态
qmd status
```

`--mask` 支持 glob 模式，灵活指定要索引的文件：

```bash
# 索引所有 Markdown
qmd collection add ./notes --name notes --mask "**/*.md"

# 索引 TypeScript 源码
qmd collection add ./src --name source --mask "**/*.ts"

# 索引所有文件，排除 node_modules
qmd collection add . --name all --mask "**/*" --ignore "node_modules/**"
```

### 添加上下文描述（强烈推荐）

上下文描述帮助 QMD 理解每个集合的用途，显著提升搜索精度：

```bash
qmd context add qmd://project-docs "认证服务的技术文档"
qmd context add qmd://notes "日常开发笔记和会议记录"
```

### 测试搜索

```bash
# 关键词搜索（最快）
qmd search "rate limit"

# 语义搜索（理解意图）
qmd vsearch "怎么防止 API 被滥用"

# 混合搜索（最精准）
qmd query "认证 Token 的最佳实践"
```

## 三种搜索模式该用哪个？

| 模式 | 命令 | 速度 | 精度 | 适用场景 |
|------|------|------|------|----------|
| 关键词搜索 | `qmd search` | < 10ms | 中 | 找具体的函数名、错误信息、配置项 |
| 语义搜索 | `qmd vsearch` | 50-200ms | 高 | 概念性问题，"怎么做 XX" |
| 混合搜索 | `qmd query` | 200-500ms | 最高 | Agent 记忆检索、复杂问题 |

**给 AI Agent 用，永远选 `query`。** 200-500ms 的延迟对 Agent 工作流来说可以忽略不计，但精度提升是实打实的。

## MCP 集成：让 Agent 拥有精准记忆

这是 QMD 最强大的用法。通过 [MCP 协议](/posts/ai/2026-02-20-mcp-protocol-guide/)把 QMD 暴露为工具，Agent 可以在需要时主动搜索文档，只把相关内容拉进上下文。

### 配置 MCP 服务器

**Claude Code 用户**，在 MCP 配置中添加：

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

配好之后，Agent 就多了四个工具：

| 工具 | 功能 |
|------|------|
| `query` | 混合搜索，精准找到相关内容 |
| `get` | 按路径或 ID 获取特定文档 |
| `multi_get` | 批量获取多个文档 |
| `status` | 查看索引状态 |

### HTTP 模式（多 Agent 共享）

如果你同时跑多个 Agent，可以启动 QMD 的 HTTP 守护进程：

```bash
# 启动 HTTP 服务
qmd mcp --http --port 8181

# 后台守护进程模式
qmd mcp --http --daemon

# 健康检查
curl http://localhost:8181/health

# 停止服务
qmd mcp stop
```

HTTP 模式的好处是模型常驻 VRAM，没有冷启动开销。Embedding 上下文在闲置 5 分钟后自动释放，不会一直占用显存。

## 实战对比：用了 QMD 之后到底省多少？

### 场景一：Agent 回忆用户偏好

| | 传统方式 | QMD 方式 |
|---|---------|---------|
| 做法 | 把整个 MEMORY.md（2,000 Token）塞进上下文 | 搜索"用户偏好的测试框架"，返回 3 段相关内容 |
| Token 消耗 | 2,000 | ~200 |
| 节省 | — | **90%** |

### 场景二：跨文件知识检索

| | 传统方式 | QMD 方式 |
|---|---------|---------|
| 做法 | Agent 逐个读 5 个文件，共 8,000 Token | 一条 query 命中目标段落 |
| Token 消耗 | 8,000 | ~300 |
| 节省 | — | **96%** |

### 场景三：项目上下文加载

| | 传统方式 | QMD 方式 |
|---|---------|---------|
| 做法 | 每次对话都加载 README + 架构文档 + 编码规范 | 只搜索当前任务相关的内容 |
| Token 消耗 | 5,000 | ~500 |
| 节省 | — | **90%** |

实测下来，日常使用 AI Agent 一天能省掉几万个 Token。按 Claude API 的价格算，一个月能省下不少钱。对于用 [OpenClaw](/posts/ai/2026-03-05-openclaw-multi-agent-setup/) 跑多 Agent 的同学，省得更多。

## QMD vs 其他方案

| 方案 | Token 成本 | 精度 | 延迟 | 部署复杂度 |
|------|-----------|------|------|-----------|
| 全量上下文加载 | 极高 | 低（噪音多） | 无 | 无 |
| 云端 RAG（Pinecone、Weaviate） | API 费用 | 高 | 100-500ms | 高 |
| Mem0 | API 费用 | 高 | 不稳定 | 中 |
| **QMD（本地混合搜索）** | **零** | **极高** | 200-500ms | **低** |

QMD 的杀手锏就一个字：**免费**。装好之后，每次搜索不花一分钱。对于每天用 Agent 写 8 小时代码的开发者来说，这个优势是碾压级的。

## 进阶玩法

### SDK 编程接入

如果你想在自己的工具中集成 QMD：

```typescript
import { QMDStore } from '@tobilu/qmd';

const store = new QMDStore();

// 添加文档集合
await store.addCollection("my-docs", {
  path: "/path/to/docs",
  pattern: "**/*.md",
  ignore: ["node_modules/**"]
});

// 混合搜索
const results = await store.search({
  queries: [
    { type: 'lex', query: '"连接池" 超时' },
    { type: 'vec', query: '为什么高负载下连接会超时' }
  ]
});

// 直接调用单个后端
const lexResults = await store.searchLex("精确短语");
const vecResults = await store.searchVector("语义含义");
```

### 调优建议

1. **集合要聚焦**：只索引 Agent 真正需要的文档。100 篇精选 Markdown 比 10,000 篇随机文件效果好得多。

2. **善用上下文描述**：`qmd context add` 给集合加描述，搜索引擎会根据描述调整相关性得分。

3. **Agent 场景一律用 `query`**：混合搜索 + 重排序的精度碾压纯向量搜索，200ms 的延迟完全可以接受。

4. **定期更新索引**：文档变更后执行 `qmd update && qmd embed`。

5. **切换 Embedding 模型后必须重建索引**：`qmd embed -f`，不同模型生成的向量不兼容。

## 常见问题排查

### 首次 embed 很慢

正常。首次需要下载 GGUF 模型（约 2GB）。后续只处理新增或变更的文档，通常几秒就完成。

### 语义搜索返回奇怪的结果

检查是否对新文档执行了 `qmd embed`。未生成向量的文档只会出现在关键词搜索（`search`）中。

### MCP 连接失败

确认 `qmd` 命令的路径正确：

```bash
# 查看 qmd 安装位置
which qmd

# 如果需要，在 MCP 配置中使用完整路径
{
  "mcpServers": {
    "qmd": {
      "command": "/Users/你的用户名/.bun/bin/qmd",
      "args": ["mcp"]
    }
  }
}
```

## FAQ

**Q：QMD 只能搜索 Markdown 文件吗？**
A：QMD 对 Markdown 做了特别优化（智能切片会识别标题、段落、代码块），但任何纯文本文件都可以索引。

**Q：磁盘空间要多大？**
A：三个 GGUF 模型共约 2GB。SQLite 索引很小，几千篇文档也就几 MB。

**Q：不用 AI Agent，单独用 QMD 行不行？**
A：完全可以。QMD 本身就是一个出色的本地搜索工具，用来搜笔记、文档、知识库都很好用。

**Q：支持 GPU 加速吗？**
A：支持，通过 node-llama-cpp 调用。有兼容 GPU 的话，Embedding 和重排序会更快。纯 CPU 跑也完全够用。

**Q：QMD 和传统 RAG 有什么区别？**
A：QMD 本质上就是一个开箱即用的本地 RAG 管线——但打包成了一个 CLI 工具。不需要单独搭向量数据库，不需要付 Embedding API 费用，不需要维护基础设施。

## 相关阅读

- [MCP 协议详解：让 AI Agent 连接任何工具](/posts/ai/2026-02-20-mcp-protocol-guide/) — 理解 QMD 用于 Agent 集成的底层协议
- [AI Agent 记忆系统：架构与最佳实践](/posts/ai/2026-02-21-ai-agent-memory-systems/) — 记忆管理方案的全景对比
- [Context Engineering 深度指南](/posts/ai/2026-02-24-context-engineering-deep-dive/) — 为什么上下文的内容比提示词的写法更重要
- [OpenClaw 多 Agent 配置指南](/posts/ai/2026-03-05-openclaw-multi-agent-setup/) — 在 OpenClaw 中使用 QMD 优化多 Agent 工作流
- [2026 年最佳 MCP 服务器推荐](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — QMD 与其他必备 MCP 服务器
- [RAG 管线搭建：从零到生产](/posts/ai/2026-03-01-rag-pipeline-setup/) — 对比 QMD 与传统 RAG 架构的异同
