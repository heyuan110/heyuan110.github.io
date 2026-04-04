# AGENTS.md

本文档为所有 AI 代理（Claude Code、Cursor、Windsurf、Copilot、Cline 等）提供项目上下文和协作指南。

## 交互指南

- **语言**：代理用户交互默认使用中文；所有**新增内容**必须使用英文撰写
- **Git 分支**：工作分支为 `code`。推送到 `code` 会触发自动部署
- **提交信息**：使用中文提交信息

## 项目概述

一个基于 Hugo 的 AI 工程博客，托管在 GitHub Pages 上。

- **网址**：https://www.heyuan110.com/
- **Hugo 版本**：v0.153.2+（需要 Extended 版本）
- **主题**：hermit-V2

## 关键规则（违反会造成实际损害）

### 双语要求

- 每篇新文章必须同时创建 `index.md`（英文）和 `index.zh.md`（中文）
- 中英文角度可以不同，但都必须是高质量的本土写作，不是机器翻译
- `tags` 两个版本保持英文一致；`keywords` 各自用本语言搜索词
- **写文章必须用 `/blog-writer` skill**——模板、SEO 规范、检查清单都在里面

### URL 稳定性

- **禁止更改已索引的 URL**（中文或英文）
- 新文章默认不添加 `categories`
- 文章目录命名：`<date>-<english-slug>/`

### 图片规范

- 仅 WebP 格式，封面必须命名为 `cover.webp`（1200×630px）
- 统一用英文提示词生成，中英文共用同一张图

## 常用命令

```bash
hugo server -D          # 本地预览（含草稿）
hugo server              # 本地预览
hugo --minify            # 生产构建
git submodule update --remote  # 更新主题
```

## 部署

- 推送到 `code` 分支 → GitHub Actions 自动构建部署到 GitHub Pages
- 配置：`.github/workflows/hugo.yml`

## 主题定制

- 主要配置：`hugo.toml`
- 自定义样式：`assets/scss/`
- 自定义布局：`layouts/`
