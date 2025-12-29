# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 Hugo 的个人技术博客，使用 hermit-V2 主题，部署在 GitHub Pages。

- **网站地址**: https://www.heyuan110.com/
- **Hugo 版本**: v0.153.2+ (需要 Extended 版本)
- **主题**: hermit-V2

## 常用命令

```bash
# 本地预览（包含草稿）
hugo server -D

# 本地预览（不含草稿）
hugo server

# 创建新文章
hugo new posts/<分类>/<文章名>.md

# 构建生产版本
hugo --minify

# 更新主题子模块
git submodule update --remote
```

## 目录结构

```
content/
├── posts/           # 博客文章目录
│   ├── ai/          # AI 系列
│   ├── java/        # Java 系列
│   ├── go/          # Go 系列
│   ├── docker/      # Docker 系列
│   ├── linux/       # Linux 系列
│   └── ...          # 其他分类
├── about.md         # 关于页面
└── *-categories.md  # 各系列的分类页面
static/              # 静态资源（图片、favicon 等）
themes/hermit-V2/    # 主题（作为 git submodule）
hugo.toml            # Hugo 主配置文件
```

## 文章格式

文章使用 Markdown 格式，Front Matter 使用 TOML 格式（`+++`）：

```markdown
+++
date = '2024-01-01'
draft = false
title = '文章标题'
tags = ['tag1', 'tag2']
+++

文章内容...
```

带图片的文章应使用 Page Bundle 结构：
```
content/posts/<分类>/<日期>-<文章名>/
├── index.md
└── image.png
```

## 部署流程

- 推送到 `code` 分支会自动触发 GitHub Actions
- 自动构建并部署到 GitHub Pages
- 配置文件：`.github/workflows/hugo.yml`

## 主题定制

- 主配置：`hugo.toml`
- 自定义样式：在 `assets/scss/` 目录创建对应的 scss 文件覆盖主题样式
- 自定义布局：在 `layouts/` 目录创建对应文件覆盖主题模板
