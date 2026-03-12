# AGENTS.md

This file provides project context and collaboration guidelines for all AI agents (Claude Code, Cursor, Windsurf, Copilot, Cline, etc.).

## Interaction Guidelines

- **Language**: Default to Chinese for agent-user interaction; ALL new content must be written in English
- **Git branch**: Working branch is `code`. Pushing to `code` triggers automatic deployment
- **Commit messages**: Use Chinese for commit messages

## Project Overview

A Hugo-based AI engineering blog on GitHub Pages, currently transitioning from Chinese to English.

- **URL**: https://www.heyuan110.com/
- **Hugo version**: v0.153.2+ (Extended required)
- **Theme**: hermit-V2

## Multilingual Setup

The blog supports **English (default)** and **Chinese** via Hugo's built-in i18n system.

### URL Structure

| Language | URL Pattern | Example |
|----------|-------------|---------|
| English (default) | `/posts/ai/slug/` | `/posts/ai/2026-03-11-ai-development-methodologies-compared/` |
| Chinese | `/zh/posts/ai/slug/` | `/zh/posts/ai/2026-03-11-ai-development-methodologies-compared/` |

### File Naming

```
content/posts/ai/2026-03-11-article-slug/
├── index.md       # English article (default, always required)
├── index.zh.md    # Chinese article (optional, only when requested)
└── cover.webp     # Shared cover image
```

### Key Config Files

| File | Purpose |
|------|---------|
| `hugo.toml` | Language definitions (`[languages.en]`, `[languages.zh]`), per-language menus |
| `i18n/en.toml` | English UI translations (TOC, Newer, Older, etc.) |
| `i18n/zh.toml` | Chinese UI translations |
| `layouts/_partials/lang-switcher.html` | Language switch dropdown (fixed top-right) |
| `content/about.zh.md` | Chinese About page |
| `content/posts/_index.zh.md` | Chinese posts section index |

### Writing Rules

- **Default**: All new articles are written in **English only** (`index.md`)
- **Chinese version**: Only created when user explicitly requests it (says "中文版", "多语言", "同时输出中文")
- **Chinese version is NOT a machine translation**: It must be a natural, high-quality rewrite that reads natively in Chinese. Google penalizes low-quality translations
- **SEO priority is English**: The English version is the canonical content. Chinese is supplementary

### When Creating Chinese Versions (`index.zh.md`)

1. Front matter `title` and `description` must be in Chinese, naturally written (not translated word-by-word)
2. Front matter `tags` and `categories` stay in English (same as English version) for taxonomy consistency
3. Front matter `keywords` should be Chinese search terms
4. Content must read naturally in Chinese — use native expressions, not translationese
5. Cover image is shared (same `cover.webp`), reference it the same way
6. Internal links point to the same paths (Hugo resolves language automatically)

### Language Switcher Behavior

- **Homepage**: Always shows language switch button (top-right dropdown)
- **Article with translation**: Shows language switch → links to translated version
- **Article without translation**: No language switch button (avoids redirecting to homepage)

### SEO for Multilingual

Hugo automatically generates:
- `<link rel="alternate" hreflang="en">` and `<link rel="alternate" hreflang="zh">` tags
- Separate sitemaps per language
- Proper `lang` attribute on `<html>` tag

This tells Google the two versions are related, not duplicate content.

## Bilingual Content Rules (MUST follow)

### Goal: All articles should have both English and Chinese versions

### DO NOT:
- Change already-indexed URLs (Chinese or English)
- Create low-quality machine translations — both languages must read naturally
- Overwrite existing content when adding the other language version

### MUST DO:
- **New articles**: Write English (`index.md`) first, then add Chinese (`index.zh.md`)
- **Old Chinese-only articles**: Keep original Chinese, add English version (`index.md`)
- **Old English-only articles**: Keep original English, add Chinese version (`index.zh.md`)
- Both versions must be **high-quality native writing**, not word-for-word translations
- All site-level text is in English (menu, footer, about, meta); Chinese UI via i18n files
- `tags` and `categories` stay in English across both versions for taxonomy consistency

## Common Commands

```bash
# Local preview (with drafts)
hugo server -D

# Local preview (without drafts)
hugo server

# Create new article
hugo new posts/ai/2026-02-25-article-slug/index.md

# Production build
hugo --minify

# Update theme submodule
git submodule update --remote
```

## Content Categories

### New English Categories (active)

| Category | URL | Use for |
|----------|-----|---------|
| **AI Guides** | `categories/ai-guides/` | Setup guides, tutorials, best practices, workflows |
| **Comparisons** | `categories/comparisons/` | Tool comparisons, pricing, benchmarks |

### Legacy Chinese Categories (archived, do not modify)

| Category | URL |
|----------|-----|
| AI原理 | `categories/ai原理/` |
| AI实战 | `categories/ai实战/` |
| Linux | `categories/linux/` |
| Docker | `categories/docker/` |

### Category Assignment for New Articles

```toml
# Guides, tutorials, how-tos, reviews
categories = ['AI Guides']

# Tool comparisons, pricing, benchmarks
categories = ['Comparisons']
```

## Content Strategy

### Article Types (priority order)
1. **Guide** — "How to set up X", "Complete guide to Y"
2. **Setup** — Step-by-step installation and configuration
3. **Comparison** — "X vs Y: Which is better for Z?"
4. **Best Tools** — "Top 10 tools for X in 2026"
5. **Workflow** — "My AI development workflow"
6. **Review** — In-depth tool/framework evaluation

### Prohibited Content Types
- Personal journal entries
- Log-style posts with no search intent
- Content without commercial or informational value

### Topic Clusters (each needs 10+ articles)
- Claude Code
- AI Agent Frameworks
- AI Coding Tools
- AI Engineering Workflows
- Tool Comparisons

## Directory Structure

```
content/
├── posts/
│   ├── _index.zh.md # Chinese posts section index
│   ├── ai/          # AI articles (new: English, legacy: Chinese)
│   │   └── 2026-xx-xx-slug/
│   │       ├── index.md      # English (always required)
│   │       ├── index.zh.md   # Chinese (optional)
│   │       └── cover.webp    # Shared cover image
│   ├── java/        # Java (archived, Chinese)
│   ├── go/          # Go (archived, Chinese)
│   ├── docker/      # Docker (archived, Chinese)
│   ├── linux/       # Linux (archived, Chinese)
│   └── macos/       # macOS (archived, Chinese)
├── about.md         # About page (English)
├── about.zh.md      # About page (Chinese)
└── privacy.md       # Privacy policy (English)
i18n/
├── en.toml          # English UI strings
└── zh.toml          # Chinese UI strings
static/              # Static assets (images, favicon, etc.)
themes/hermit-V2/    # Theme (git submodule)
hugo.toml            # Hugo config (multilingual)
```

## Article Format

### Front Matter Template (English articles — `index.md`)

All articles use Markdown with TOML front matter (`+++`):

```toml
+++
date = '2026-02-25T10:00:00+08:00'
draft = false
title = 'Article Title (50-60 chars, primary keyword first)'
description = 'SEO description for search results and social sharing (120-160 chars)'
toc = true
tags = ['Claude Code', 'AI Agent', 'specific-tag']
categories = ['AI Guides']
keywords = ['search keyword 1', 'search keyword 2']
+++
```

### Front Matter Template (Chinese articles — `index.zh.md`, only when requested)

```toml
+++
date = '2026-02-25T10:00:00+08:00'
draft = false
title = '中文标题（自然表达，非逐字翻译）'
description = '中文 SEO 描述，面向中文搜索用户（120-160 字符）'
toc = true
tags = ['Claude Code', 'AI Agent', 'specific-tag']
categories = ['AI Guides']
keywords = ['中文搜索关键词1', '中文搜索关键词2']
+++
```

**Key differences**: `title`, `description`, `keywords` in Chinese; `tags` and `categories` stay English.

| Field | Required | Notes |
|-------|----------|-------|
| `date` | Yes | ISO 8601 with timezone |
| `title` | Yes | 50-60 chars, keyword-first |
| `description` | Yes | 120-160 chars, include primary keyword |
| `categories` | Yes | `AI Guides` or `Comparisons` |
| `tags` | Yes | 3-5 tags |
| `toc` | Recommended | Set `true` for long articles |
| `keywords` | Recommended | SEO supplementary keywords |
| `draft` | Optional | Default `false` |

### Page Bundle Structure

Articles with images use Page Bundle:

```
content/posts/ai/2026-02-25-article-slug/
├── index.md      # Article content
├── cover.webp    # Cover image (must be named cover.webp)
└── other.webp    # Additional images
```

**Naming**: `<date>-<english-slug>/`, e.g. `2026-02-25-claude-code-mcp-guide/`

### Image Guidelines

| Item | Standard |
|------|----------|
| **Format** | WebP only (smaller size, good quality) |
| **Cover image** | Must be named `cover.webp` |
| **Dimensions** | Cover: 1200×630px (optimal for social sharing) |
| **Reference** | `![alt text](cover.webp)` or `![alt text](filename.webp)` |
| **ALT text** | Required, describe image content in English |

### Nested Code Blocks

When showing code blocks inside Markdown code blocks, use different backtick counts:

`````markdown
# Outer block uses 4+ backticks
```python
# Inner block uses 3 backticks
print("Hello World")
```
`````

## Deployment

- Push to `code` branch triggers GitHub Actions
- Auto-builds and deploys to GitHub Pages
- Config: `.github/workflows/hugo.yml`

## Theme Customization

- Main config: `hugo.toml`
- Custom styles: `assets/scss/` (override theme styles)
- Custom layouts: `layouts/` (override theme templates)
