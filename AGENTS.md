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

## Migration Rules (MUST follow)

### DO NOT:
- Batch-translate old Chinese articles
- Overwrite or modify existing Chinese articles
- Change already-indexed Chinese URLs
- Mix Chinese and English on the same page

### MUST DO:
- All new articles must be written in **English**
- All site-level text is in English (menu, footer, about, meta)
- Internal links should gradually point to English content
- Old Chinese content remains as archived legacy

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
│   ├── ai/          # AI articles (new: English, legacy: Chinese)
│   ├── java/        # Java (archived, Chinese)
│   ├── go/          # Go (archived, Chinese)
│   ├── docker/      # Docker (archived, Chinese)
│   ├── linux/       # Linux (archived, Chinese)
│   └── macos/       # macOS (archived, Chinese)
├── about.md         # About page (English)
└── privacy.md       # Privacy policy (English)
static/              # Static assets (images, favicon, etc.)
themes/hermit-V2/    # Theme (git submodule)
hugo.toml            # Hugo config
```

## Article Format

### Front Matter Template (English articles)

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
