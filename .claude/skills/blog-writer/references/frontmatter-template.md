# Front Matter 模板

## 英文版（`index.md`，必须创建）

```toml
+++
date = '2026-01-26T10:00:00+08:00'
draft = false
title = 'Article Title (50-60 chars, primary keyword first)'
description = 'SEO description for search results and social sharing (120-160 chars)'
toc = true
tags = ['Claude Code', 'AI Agent', 'specific-tag']
keywords = ['search keyword 1', 'search keyword 2']
+++

![Descriptive ALT text with primary keyword](cover.webp)
```

## 中文版（`index.zh.md`，默认必须创建）

```toml
+++
date = '2026-01-26T10:00:00+08:00'
draft = false
title = '中文标题（自然表达，非逐字翻译，含核心关键词）'
description = '中文 SEO 描述，面向中文搜索用户（120-160 字符）'
toc = true
tags = ['Claude Code', 'AI Agent', 'specific-tag']
keywords = ['中文搜索关键词1', '中文搜索关键词2']
+++

![中文 ALT 描述，含核心关键词](cover.webp)
```

## FAQ 结构化数据（必须）

每篇文章必须在 front matter 中添加 3-5 个 FAQ：

```toml
[[params.faqItems]]
question = "用户最常搜索的问题？"
answer = "直接回答，1-3 句话，包含核心关键词。"

[[params.faqItems]]
question = "另一个常见问题？"
answer = "简洁准确的回答。"
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `date` | 是 | ISO 8601 格式，含时区 `+08:00` |
| `title` | 是 | 50-60 字符，关键词前置 |
| `description` | 是 | 120-160 字符，包含核心关键词 |
| `tags` | 是 | 3-5 个标签（英文） |
| `categories` | 否 | 新文章默认不使用；仅在维护旧文章或用户明确要求时保留/添加 |
| `toc` | 推荐 | 长文设为 `true` |
| `keywords` | 推荐 | SEO 补充关键词 |
| `draft` | 否 | 默认 `false` |

## 关键规则

- 封面图必须在正文中引用：Front Matter 后第一行必须是 `![ALT](cover.webp)`
- 中文版的 `title`、`description`、`keywords` 必须用中文自然表达
- 两个版本的 `tags` 保持英文一致
- 新文章默认不添加 `categories`
