---
name: blog-diagram
description: "架构图/信息图生成器。根据内容生成专业的架构图、流程图、对比表、层级图等。支持 12 种布局和 8 种风格。使用此 skill 当用户需要：(1) 生成架构图 (2) 生成流程图 (3) 生成对比表/信息图 (4) 可视化数据或概念"
---

# 架构图/信息图生成器

将文字内容转化为专业的可视化图表。布局 × 风格二维度自由组合。

## 使用方式

```bash
# 从文章内容生成
/blog-diagram content/posts/ai/2026-04-04-article-slug/ --layout hub-spoke

# 从粘贴内容生成
/blog-diagram --layout comparison-matrix --style blueprint
[粘贴内容]

# 指定输出位置
/blog-diagram --layout flowchart --output content/posts/ai/2026-04-04-article-slug/architecture.webp

# 快速模式
/blog-diagram content.md --quick
```

## 二维度系统：布局 × 风格

### 布局（12 种信息结构）

| 布局 | 适合场景 | 视觉描述 |
|------|---------|---------|
| `linear-progression` | 时间线、流程、教程步骤 | 水平/垂直线性排列，箭头连接 |
| `binary-comparison` | A vs B 对比、优缺点 | 左右分屏，中间分隔 |
| `comparison-matrix` | 多维度对比表格 | 网格矩阵，行列交叉 |
| `hierarchical-layers` | 金字塔、优先级、技术栈 | 上窄下宽的层级结构 |
| `hub-spoke` | 中心概念+关联要素 | 中心节点辐射分支 |
| `tree-branching` | 分类、决策树、目录结构 | 树状分支展开 |
| `bento-grid` | 多主题概览、功能模块 | 模块化方格布局（默认） |
| `funnel` | 转化漏斗、筛选过程 | 上宽下窄的漏斗形 |
| `circular-flow` | 循环过程、生命周期 | 环形闭合流程 |
| `venn-diagram` | 重叠概念、交集关系 | 重叠圆形区域 |
| `bridge` | 问题→解决方案 | 两端+桥梁连接 |
| `dashboard` | 指标、KPI、数据概览 | 仪表盘风格多区块 |

### 风格（8 种视觉美学）

| 风格 | 描述 | 适合场景 |
|------|------|---------|
| `craft` | 手工质感，纸艺风（默认） | 通用、教育类 |
| `blueprint` | 技术蓝图，工程制图 | 架构设计、系统设计 |
| `corporate` | 扁平矢量，鲜艳色块 | 产品介绍、商业分析 |
| `schematic` | 原理图，精确线条 | 技术深度文、工程 |
| `wireframe` | 灰度线框，界面模型 | UI/UX、产品设计 |
| `chalkboard` | 粉笔黑板风 | 教学、概念解释 |
| `pixel` | 像素复古风 | 游戏、复古技术 |
| `minimal` | 极简线条图 | 概念、核心思想 |

### 推荐组合

| 内容场景 | 推荐布局 + 风格 |
|---------|----------------|
| AI 工具技术栈 | `hierarchical-layers` + `blueprint` |
| 工具 A vs B 对比 | `binary-comparison` + `corporate` |
| 多工具横评 | `comparison-matrix` + `corporate` |
| 开发工作流 | `linear-progression` + `schematic` |
| 架构组件关系 | `hub-spoke` + `blueprint` |
| 技术演进史 | `linear-progression` + `craft` |
| 功能模块概览 | `bento-grid` + `corporate` |
| 决策选型指南 | `tree-branching` + `minimal` |
| 数据监控面板 | `dashboard` + `wireframe` |

## 工作流

### 步骤 1：分析内容

读取内容，提取：
- 核心概念和关系
- 数据点（具体数字、指标）
- 结构类型（对比/层级/流程/网络）
- 推荐的布局×风格组合

### 步骤 2：确认配置

除非 `--quick`，用 `AskUserQuestion` 确认：
- 推荐的布局×风格组合（提供 2-3 个选项和理由）
- 画幅（默认 16:9，可选 1:1、9:16 竖版）
- 内容语言

### 步骤 3：构造提示词

用以下结构构造生图提示词：

```
[标题] - [布局类型]可视化

布局: [布局描述，参考上表]

内容区域:
- 区域 1: [具体内容，用真实数据]
- 区域 2: [具体内容，用真实数据]
...

标签: [文章中的具体数字、术语、指标]
配色: [语义化配色]
风格: [风格修饰词]
画幅: [16:9/1:1/9:16]

干净构图，充足留白。简洁背景。
No watermarks, no logos.
```

### 步骤 4：生成图片

1. 调用 Rube MCP + Gemini 生成
2. 下载并转换为 WebP（质量 85）
3. 验证生成结果

### 步骤 5：输出

```
图表生成完成！

主题: [主题]
布局: [layout] | 风格: [style]
画幅: [ratio]
文件: [路径]
```

## 输出规范

| 项目 | 标准 |
|------|------|
| 格式 | WebP |
| 质量 | 85 |
| 画幅 | 16:9（默认）、1:1、9:16 |
| 最大尺寸 | 宽 1200px |
| 命名 | 用户指定 `--output`，或自动命名 `diagram-{slug}.webp` |

## 与其他 skill 的关系

- **blog-illustrator** 在生成 framework/flowchart/comparison 类型插图时可以调用本 skill
- **blog-writer** 写技术架构文章时可以调用本 skill 生成架构图
- 也可以**独立使用**——为任何内容生成可视化图表
