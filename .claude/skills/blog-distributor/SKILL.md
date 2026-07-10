---
name: blog-distributor
description: "文章发布后自动分发到外部平台（dev.to、掘金、V2EX、HN）。使用此 skill 当用户需要：(1) 将刚发布的文章同步到 dev.to (2) 生成掘金/V2EX 格式的转发内容 (3) 生成 HN 投稿标题 (4) 批量分发多篇文章"
---

# 博客文章分发助手

## 概述

将博客文章自动/半自动分发到外部平台，建立外链，扩大文章影响力。

**核心原则**：
- 不转载全文，生成**摘要版 + 原文链接**
- 设置 `canonical_url` 指回原文（避免 SEO 重复内容惩罚）
- 中文文章 → 掘金/V2EX 格式
- 英文文章 → dev.to 自动发布
- 高质量深度文章 → HN 投稿建议

## 触发方式

用户说以下任何一种：
- `/distribute`
- "分发文章"、"同步到 dev.to"、"发到掘金"
- "distribute"、"cross-post"、"syndicate"

## 工作流程

### Step 0: 确认分发目标

询问用户要分发哪篇文章（或自动检测最近一次 commit 中的新文章）：

```bash
# 自动检测最近新增的文章
git log --diff-filter=A --name-only -1 --pretty=format: -- 'content/posts/ai/*/index.md'
```

### Step 1: 读取文章内容

读取英文版（`index.md`）和中文版（`index.zh.md`），提取：
- title
- description
- tags
- 正文前 500 字（摘要用）
- 文章 URL（基于目录名推算，域名从 `hugo.toml` 的 `baseURL` 动态获取）

### Step 2: 生成分发内容

#### 2.1 dev.to 版本（英文文章）

用 `scripts/devto-publish.py` 走 dev.to 官方 REST API（⚠️ 旧版走 Rube MCP `DEVTO_CREATE_ARTICLE`，Rube 已弃用，禁止再用）：

```bash
python3 scripts/devto-publish.py content/posts/ai/<文章目录>            # 存草稿
python3 scripts/devto-publish.py content/posts/ai/<文章目录> --publish  # 直接公开发布
```

**准备工作（一次性）**：dev.to → Settings → Extensions → DEV Community API Keys → Generate，key 存入 `~/.config/devto/api_key`（⛔ 不入仓库）。

**脚本自动处理**：TOML front matter → 标题/描述/标签（≤4 个）；相对图片和站内链接 → 绝对 URL；mermaid 块 → 替换为回原文的链接（dev.to 不渲染 mermaid）；自动设置 `canonical_url` 指回原文并附 "Originally published" 尾注——发的是**全文**（canonical 保护下全文比摘要在 dev.to 上表现更好）。

**发布策略**：默认存草稿给用户过目；用户明确说"直接发"时才用 `--publish`。发布后把 dev.to URL 回报给用户。

#### 2.2 掘金/V2EX 版本（中文文章）

暂无 API，生成可直接复制粘贴的 Markdown：

**掘金格式**：
```markdown
# <中文标题>

> 本文首发于 [我的博客](<原文URL>)，转载请注明出处。

<中文文章前500字>

---

**👉 [阅读完整文章](<原文URL>)**

本文涵盖：
- <要点1>
- <要点2>
- <要点3>

更多 AI 工程实战文章，欢迎访问 [我的博客](<博客首页URL>)。
```

**V2EX 格式**：
```
<中文标题>

<2-3句摘要>

原文链接：<原文URL>
```

输出后提示用户：
- 掘金：打开 https://juejin.cn/editor/drafts/new 粘贴
- V2EX：打开 https://www.v2ex.com/new 选择合适的节点粘贴

#### 2.3 Hacker News 投稿建议

仅为深度技术文章生成投稿建议：

```
标题建议：<简洁、技术性、不clickbait的标题>
URL：<英文原文URL>
投稿链接：https://news.ycombinator.com/submit
最佳投稿时间：美国东部时间上午 9-11 点（北京时间晚上 9-11 点）
```

**判断是否适合投 HN 的标准**：
- 有原创技术洞察（不是纯教程）
- 有数据支撑（benchmark、对比测试）
- 话题在 HN 有讨论热度（AI tools、开源项目、工程方法论）

### Step 3: 汇总报告

分发完成后输出汇总：

```
## 分发完成

| 平台 | 状态 | 链接 |
|------|------|------|
| dev.to | ✅ 草稿已创建 | <链接> |
| 掘金 | 📋 内容已生成 | 请手动粘贴 |
| V2EX | 📋 内容已生成 | 请手动粘贴 |
| HN | 💡 建议投稿 | <投稿链接> |
```

## 批量分发

如果用户要求批量分发（如"把今天写的文章都分发了"），循环执行以上流程：

```bash
# 获取今天commit中的所有新文章
git log --since="today" --diff-filter=A --name-only --pretty=format: -- 'content/posts/ai/*/index.md'
```

## 注意事项

1. **canonical_url 必须设置** — 告诉 Google 原文在你的博客，dev.to 版本是转载
2. **不要全文转载** — 只发摘要 + 链接，引导读者回到原站
3. **标签限制** — dev.to 最多 4 个标签，选最相关的
4. **发布时机** — dev.to 和 HN 最佳发布时间是美国工作日上午（北京时间晚上）
5. **先存草稿** — dev.to 先 `published: false`，用户确认后再公开
