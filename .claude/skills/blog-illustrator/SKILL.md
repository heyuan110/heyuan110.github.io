---
name: blog-illustrator
description: "文章配图生成器。分析文章结构，识别需要配图的位置，用 AI 生成匹配的插图并自动插入。使用此 skill 当用户需要：(1) 为文章添加配图 (2) 为某个章节生成插图 (3) 批量为文章配图"
---

# 文章配图生成器

分析文章结构，识别需要视觉辅助的位置，生成匹配的插图并自动插入。

## 使用方式

```bash
# 为整篇文章自动配图
/blog-illustrator content/posts/ai/2026-04-04-article-slug/

# 只为特定章节配图
/blog-illustrator content/posts/ai/2026-04-04-article-slug/ --section "## Core Concepts"

# 指定类型和风格
/blog-illustrator article/ --type comparison --style blueprint

# 快速模式
/blog-illustrator article/ --quick

# 指定配图密度
/blog-illustrator article/ --density balanced
```

## 二维度系统：类型 × 风格

类型控制信息结构，风格控制视觉美学。两个维度自由组合。

### 类型（信息结构）

| 类型 | 适合场景 | 提示词要点 |
|------|---------|-----------|
| `infographic` | 数据、指标、技术参数 | 网格/放射/层级布局，标签用文章中的真实数据 |
| `scene` | 叙事、情感、氛围 | 焦点主体、氛围灯光、情绪色温 |
| `flowchart` | 流程、工作流、步骤 | 左右/上下/环形布局，步骤+箭头+决策点 |
| `comparison` | 并排对比、AB测试 | 左右分屏，视觉分隔符，对称结构 |
| `framework` | 架构、模型、层级 | 节点+连接线，层级/网络/矩阵结构 |
| `timeline` | 历史、版本演进 | 水平/垂直时间轴，里程碑标记 |

### 风格（视觉美学）

| 风格 | 描述 | 适合内容 |
|------|------|---------|
| `flat-vector` | 干净扁平矢量，几何图标 | 技术文章、教程 |
| `blueprint` | 技术蓝图，工程制图风 | 架构设计、系统设计 |
| `minimal` | 极简线条，大量留白 | 概念解释、核心思想 |
| `warm` | 温暖手绘，友好亲和 | 个人经验、社区故事 |
| `editorial` | 杂志信息图风格 | 数据解析、对比评测 |
| `digital` | 精致数字风，渐变抛光 | 产品评测、SaaS 工具 |

### 兼容性矩阵

| | flat-vector | blueprint | minimal | warm | editorial | digital |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| infographic | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓ |
| scene | ✓ | ✗ | ✓ | ✓✓ | ✓ | ✓ |
| flowchart | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓ |
| comparison | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ |
| framework | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ |
| timeline | ✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓ |

## 工作流

### 步骤 1：分析文章

读取文章内容，分析：
- 内容类型（技术/教程/方法论/叙事）
- 核心论点（2-5 个主要观点）
- **识别配图位置**：哪些段落/章节需要视觉辅助

配图位置判断标准：
- 复杂概念需要可视化解释
- 对比/表格数据适合用图表
- 流程/步骤适合用流程图
- 架构/层级关系适合用架构图
- 情绪/故事转折适合用场景图

**关键原则**：视觉隐喻要表达底层概念，不要做字面插图。

### 步骤 2：确认配置

除非 `--quick`，用 `AskUserQuestion` 确认（一次性问完，不要分多次）：
- 配图密度：minimal（1-2张）、balanced（3-5张）、rich（6+张）
- 类型偏好：自动推断还是指定
- 风格偏好：自动推断还是指定

### 步骤 3：生成大纲

为每个配图位置生成大纲：

```markdown
## 插图 1
**位置**: [对应章节/段落]
**类型**: [infographic/scene/flowchart/comparison/framework/timeline]
**目的**: [为什么这里需要配图]
**内容**: [具体画面描述]
**文件名**: 01-{type}-{slug}.webp
```

### 步骤 4：生成图片

对每个插图：

1. 根据类型构造提示词（参考 [references/prompt-templates.md](references/prompt-templates.md)）
2. 调用 Rube MCP + Gemini 生成
3. 下载并转换为 WebP（质量 85，宽度不超过 1200px）
4. 保存到文章目录

**提示词构造核心规则**：
- **先描述布局结构**，再描述内容
- **用文章中的真实数据**做标签（具体数字、术语、指标）
- **语义化配色**（红=警告、绿=高效、蓝=技术）
- 结尾加画幅和复杂度级别
- 加 `No text, no watermarks, no logos.`（除非是 infographic 类型需要标签）

### 步骤 5：插入文章

在文章对应位置插入图片引用：

```markdown
![插图描述](01-{type}-{slug}.webp)
```

插入在对应段落之后，不要打断段落。

### 步骤 6：完成报告

```
文章配图完成！

文章: [路径]
类型: [type] | 风格: [style]
生成: X/N 张插图

插图列表：
✓ 01-infographic-xxx.webp — [描述]
✓ 02-comparison-xxx.webp — [描述]
...
```

## 输出规范

| 项目 | 标准 |
|------|------|
| 格式 | WebP |
| 质量 | 85 |
| 最大宽度 | 1200px（高度按比例） |
| 画幅 | 16:9（默认）或根据类型调整 |
| 位置 | 文章目录下（与 index.md 同级） |
| 命名 | `NN-{type}-{slug}.webp`（如 `01-comparison-tool-matrix.webp`） |

## 参考文件

- [references/prompt-templates.md](references/prompt-templates.md) — 各类型的提示词模板
