# AGENTS.md

本文档为所有 AI 代理（Claude Code、Cursor、Windsurf、Copilot、Cline 等）提供项目上下文和协作指南。

## 交互指南

- **语言**：代理用户交互默认使用中文；所有**新增内容**必须使用英文撰写
- **Git 分支**：工作分支为 `code`。推送到 `code` 会触发自动部署
- **提交信息**：使用中文提交信息

## 项目概述

一个基于 Hugo 的 AI 工程博客，托管在 GitHub Pages 上，目前正在从中文向英文过渡。

- **网址**：https://www.heyuan110.com/
- **Hugo 版本**：v0.153.2+（需要 Extended 版本）
- **主题**：hermit-V2

## 多语言设置

博客通过 Hugo 的内置 i18n 系统支持**英文（默认）**和**中文**。

### URL 结构

| 语言 | URL 模式 | 示例 |
|------|----------|------|
| 英文（默认） | `/posts/ai/slug/` | `/posts/ai/2026-03-11-ai-development-methodologies-compared/` |
| 中文 | `/zh/posts/ai/slug/` | `/zh/posts/ai/2026-03-11-ai-development-methodologies-compared/` |

### 文件命名

```
content/posts/ai/2026-03-11-article-slug/
├── index.md       # 英文文章（必须）
├── index.zh.md    # 中文文章（默认创建）
└── cover.webp     # 共享封面图片（英文生成，中英文共用）
```

### 关键配置文件

| 文件 | 用途 |
|------|------|
| `hugo.toml` | 语言定义（`[languages.en]`、`[languages.zh]`）、语言特定菜单 |
| `i18n/en.toml` | 英文 UI 翻译（TOC、Newer、Older 等） |
| `i18n/zh.toml` | 中文 UI 翻译 |
| `layouts/_partials/lang-switcher.html` | 语言切换下拉菜单（固定右上角） |
| `content/about.zh.md` | 中文 About 页面 |
| `content/posts/_index.zh.md` | 中文文章列表页面 |

### 写作规则

- **默认中英文都写**：每篇新文章必须同时创建 `index.md`（英文）和 `index.zh.md`（中文）
- **中英文角度可以不同**：中文偏实操/国内生态，英文偏原理/国际视角
- **中文版本不是机器翻译**：必须是自然、高质量的重写，符合中文阅读习惯。Google 会惩罚低质量翻译
- **关键词策略独立**：中文 `keywords` 用中文搜索词，英文用英文搜索词
- **写文章必须用 `/blog-writer` skill**

### 添加中文版本时（`index.zh.md`）

1. 前置元数据的 `title` 和 `description` 必须是中文，自然表达（非逐字翻译）
2. 前置元数据的 `tags` 保持英文（与英文版本相同）
3. 前置元数据的 `keywords` 应使用中文搜索词
4. 内容必须符合中文阅读习惯——使用本土表达方式，避免翻译腔
5. 封面图片共享（相同的 `cover.webp`），引用方式相同
6. 内部链接使用相同路径（Hugo 会自动解析语言）

### 语言切换器行为

- **首页**：始终显示语言切换按钮（右上角下拉菜单）
- **有翻译的文章**：显示语言切换 → 链接到翻译版本
- **无翻译的文章**：不显示语言切换按钮（避免重定向到首页）

### 多语言 SEO

Hugo 会自动生成：
- `<link rel="alternate" hreflang="en">` 和 `<link rel="alternate" hreflang="zh">` 标签
- 按语言分隔的网站地图
- `<html>` 标签上的正确 `lang` 属性

这告诉 Google 两个版本是相关的，不是重复内容。

## 双语内容规则（必须遵守）

### 目标：所有文章都应该有英文和中文两个版本

### 禁止：
- 更改已索引的 URL（中文或英文）
- 创建低质量机器翻译——两种语言都必须自然
- 添加另一种语言版本时覆盖现有内容

### 必须做：
- **新文章**：先写英文（`index.md`），然后添加中文（`index.zh.md`）
- 两个版本都必须是**高质量的本土写作**，不是逐字翻译
- 所有站点级文本使用英文（菜单、页脚、关于、元数据）；中文 UI 通过 i18n 文件实现
- `tags` 在两个语言版本中保持英文
- 新文章默认不添加 `categories`
- 旧文章如果已经有 `categories`，不为此单独修改 URL 或历史内容

## 常用命令

```bash
# 本地预览（含草稿）
hugo server -D

# 本地预览（不含草稿）
hugo server

# 创建新文章
hugo new posts/ai/2026-02-25-article-slug/index.md

# 生产构建
hugo --minify

# 更新主题子模块
git submodule update --remote
```

## 内容策略

### 文章类型（优先级）
1. **指南** — "How to set up X"、"Complete guide to Y"（设置指南、教程、最佳实践）
2. **安装说明** — 分步安装和配置
3. **对比** — "X vs Y: Which is better for Z?"（工具对比、价格、基准测试）
4. **最佳工具** — "Top 10 tools for X in 2026"（2026 年 X 领域的顶级工具）
5. **工作流程** — "My AI development workflow"（AI 开发工作流程）
6. **评测** — 深度工具/框架评测

### 禁止的内容类型
- 个人日志条目
- 无搜索意图的日志式帖子
- 无商业或信息价值的内容

### 主题集群

围绕高流量主题持续产出，形成搜索权威（每个集群 10+ 篇）。不预设固定集群——从 GSC 数据中动态发现当前的头部主题。

## Skill 生态

博客运营通过以下 skill 形成完整闭环：

| Skill | 用途 | 触发方式 |
|-------|------|---------|
| `blog-growth` | 诊断 + 选题 + 决策 | `/blog-growth` 或 "运营博客" |
| `blog-writer` | 研究 + 写作 + 检查 | `/blog-writer` |
| `blog-cover-image` | 封面图生成 | `/blog-cover-image` |
| `blog-illustrator` | 文章配图 | `/blog-illustrator` |
| `blog-diagram` | 架构图/信息图 | `/blog-diagram` |
| `blog-distributor` | 分发到 dev.to/掘金/HN | `/distribute` |

**Skill 编写规则**：纯中文撰写，代码放 references/ 目录，不在 SKILL.md 中写大段代码。

## 目录结构

```
content/
├── posts/
│   ├── _index.zh.md # 中文文章列表页面
│   ├── ai/          # AI 文章（新：英文，旧：中文）
│   │   └── 2026-xx-xx-slug/
│   │       ├── index.md      # 英文（必须）
│   │       ├── index.zh.md   # 中文（可选）
│   │       └── cover.webp    # 共享封面图片
│   ├── java/        # Java（归档，中文）
│   ├── go/          # Go（归档，中文）
│   ├── docker/      # Docker（归档，中文）
│   ├── linux/       # Linux（归档，中文）
│   └── macos/       # macOS（归档，中文）
├── about.md         # About 页面（英文）
├── about.zh.md      # About 页面（中文）
└── privacy.md       # 隐私政策（英文）
i18n/
├── en.toml          # 英文 UI 字符串
└── zh.toml          # 中文 UI 字符串
static/              # 静态资源（图片、favicon 等）
themes/hermit-V2/    # 主题（git 子模块）
hugo.toml            # Hugo 配置（多语言）
```

## 文章格式

### 前置元数据模板（英文文章 — `index.md`）

所有文章使用 Markdown 格式，TOML 前置元数据（`+++`）：

```toml
+++
date = '2026-02-25T10:00:00+08:00'
draft = false
title = 'Article Title (50-60 字符，主要关键词优先)'
description = 'SEO 描述，用于搜索结果和社交分享（120-160 字符）'
toc = true
tags = ['Claude Code', 'AI Agent', 'specific-tag']
keywords = ['search keyword 1', 'search keyword 2']
+++
```

### 前置元数据模板（中文文章 — `index.zh.md`，默认创建）

```toml
+++
date = '2026-02-25T10:00:00+08:00'
draft = false
title = '中文标题（自然表达，非逐字翻译）'
description = '中文 SEO 描述，面向中文搜索用户（120-160 字符）'
toc = true
tags = ['Claude Code', 'AI Agent', 'specific-tag']
keywords = ['中文搜索关键词1', '中文搜索关键词2']
+++
```

**关键差异**：`title`、`description`、`keywords` 为中文；`tags` 保持英文。

| 字段 | 必需 | 说明 |
|------|------|------|
| `date` | 是 | ISO 8601 格式，带时区 |
| `title` | 是 | 50-60 字符，关键词优先 |
| `description` | 是 | 120-160 字符，包含主要关键词 |
| `tags` | 是 | 3-5 个标签 |
| `categories` | 否 | 新文章默认不使用；仅在维护旧文章或用户明确要求时保留/添加 |
| `toc` | 推荐 | 长文章设置为 `true` |
| `keywords` | 推荐 | SEO 补充关键词 |
| `draft` | 可选 | 默认 `false` |

### FAQ 结构化数据（必须）

每篇文章必须在 front matter 中添加 3-5 个 FAQ，提升搜索结果 CTR：

```toml
[[params.faqItems]]
question = "用户常搜的问题？"
answer = "简洁直接的回答，1-3 句话。"
```

### 页面包结构

包含图片的文章使用页面包：

```
content/posts/ai/2026-02-25-article-slug/
├── index.md      # 文章内容
├── cover.webp    # 封面图片（必须命名为 cover.webp）
└── other.webp    # 其他图片
```

**命名**：`<date>-<english-slug>/`，例如 `2026-02-25-claude-code-mcp-guide/`

### 图片指南

| 项目 | 标准 |
|------|------|
| **格式** | 仅 WebP（尺寸小，质量好） |
| **封面图片** | 必须命名为 `cover.webp` |
| **尺寸** | 封面：1200×630px（社交媒体分享最佳尺寸） |
| **引用** | `![alt text](cover.webp)` 或 `![alt text](filename.webp)` |
| **ALT 文本** | 必需，用英文描述图片内容 |
| **生成方式** | 统一用英文提示词生成（AI 中文文字容易乱码） |
| **中英文共用** | 同一张图片，index.md 和 index.zh.md 共享引用 |

### 嵌套代码块

当在 Markdown 代码块中显示代码块时，使用不同的反引号数量：

`````markdown
# 外层块使用 4+ 个反引号
```python
# 内层块使用 3 个反引号
print("Hello World")
```
`````

## 部署

- 推送到 `code` 分支会触发 GitHub Actions
- 自动构建并部署到 GitHub Pages
- 配置：`.github/workflows/hugo.yml`

## 主题定制

- 主要配置：`hugo.toml`
- 自定义样式：`assets/scss/`（覆盖主题样式）
- 自定义布局：`layouts/`（覆盖主题模板）
