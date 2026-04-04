# 自动选择规则

维度未指定时，根据文章内容信号自动选择。

## 类型自动选择

| 内容信号 | 类型 |
|---------|------|
| 产品发布、公告、新版本、评测 | `hero` |
| 架构、框架、系统、API、技术原理 | `conceptual` |
| 观点、洞察、对比分析、方法论 | `typography` |
| 哲学、成长、抽象、反思 | `metaphor` |
| 教程、实战、步骤指南、工作流 | `scene` |
| 极简、核心概念、纯粹 | `minimal` |

## 色板自动选择

| 内容信号 | 色板 |
|---------|------|
| AI、编程、技术架构、代码 | `cool` |
| 娱乐、高端、暗色系、开发工具 | `dark` |
| 个人经历、社区、人文 | `warm` |
| 产品发布、游戏、推广 | `vivid` |
| 极简、专注、纯粹 | `mono` |
| 历史、复古、经典 | `retro` |

## 渲染自动选择

| 内容信号 | 渲染 |
|---------|------|
| 干净、现代、技术、信息图 | `flat-vector` |
| 草图、笔记、个人、随性 | `hand-drawn` |
| 数据、仪表盘、企业、精致 | `digital` |
| 艺术、水彩、柔和、梦幻 | `painterly` |
| 游戏、复古、怀旧 | `pixel` |
| 教育、教程、课堂 | `chalk` |

## 情绪自动选择

| 内容信号 | 情绪 |
|---------|------|
| 专业、企业、学术 | `subtle` |
| 通用、教育、博客 | `balanced` |
| 发布、公告、推广、争议 | `bold` |

默认：`balanced`

## 兼容性矩阵（高推荐组合）

| 场景 | 类型 | 色板 | 渲染 |
|------|------|------|------|
| AI 工具评测 | hero | dark | digital |
| 编程教程 | conceptual | cool | flat-vector |
| 架构设计 | conceptual | dark | digital |
| 工具对比 | hero | cool | flat-vector |
| 方法论/趋势 | typography | mono | digital |
| 开源项目 | hero | vivid | flat-vector |
| 安全/隐私 | conceptual | dark | digital |
| 网络/基础设施 | conceptual | cool | digital |
