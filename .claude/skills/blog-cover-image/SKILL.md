---
name: blog-cover-image
description: "博客封面图生成器。根据文章内容自动生成 1200×630 的 WebP 封面图。支持 AI 生图（Gemini）和程序化生成两种方案。使用此 skill 当用户需要：(1) 为文章生成封面图 (2) 重新生成封面图 (3) 批量生成封面图"
---

# 博客封面图生成器

根据文章内容自动生成符合博客规范的封面图。

## 使用方式

```bash
# 为指定文章生成封面图
/blog-cover-image content/posts/ai/2026-04-04-article-slug/

# 为最近一次 commit 的新文章生成封面图
/blog-cover-image --latest

# 指定风格
/blog-cover-image content/posts/ai/2026-04-04-article-slug/ --style tech

# 快速模式（跳过确认）
/blog-cover-image content/posts/ai/2026-04-04-article-slug/ --quick

# 批量为缺少封面图的文章生成
/blog-cover-image --batch
```

## 输出规范

| 项目 | 标准 |
|------|------|
| 文件名 | `cover.webp`（固定） |
| 尺寸 | 1200 × 630 px |
| 格式 | WebP |
| 质量 | 85 |
| 大小 | < 200KB |
| 位置 | 文章目录下（与 index.md 同级） |

## 风格维度

参考 [base-prompt.md](references/base-prompt.md) 获取完整的生图系统指令。

### 五个维度

| 维度 | 可选值 | 默认 |
|------|--------|------|
| **类型** | hero、conceptual、typography、metaphor、scene、minimal | 自动推断 |
| **色板** | warm、cool、dark、vivid、mono、retro | 自动推断 |
| **渲染** | flat-vector、hand-drawn、painterly、digital、pixel、chalk | 自动推断 |
| **文字** | none、title-only | none（AI 生图文字不准确） |
| **情绪** | subtle、balanced、bold | balanced |

### 自动推断

参考 [auto-selection.md](references/auto-selection.md) 获取完整的信号→维度映射表和兼容性矩阵。

每次生成时，先读取文章的 title、tags、description，根据内容信号动态选择最佳维度组合。信号表只是参考，不要机械套用。

### 快捷风格预设

常用的维度组合可以用 `--style` 一键指定：

| 预设 | 色板 | 渲染 | 适用场景 |
|------|------|------|---------|
| `blueprint` | cool | digital | 架构、技术设计 |
| `minimal` | mono | flat-vector | 极简、核心概念 |
| `dark-tech` | dark | digital | AI 工具、开发工具 |
| `warm-sketch` | warm | hand-drawn | 个人经验、社区 |
| `retro` | retro | digital | 复古、经典话题 |
| `poster` | vivid | flat-vector | 产品发布、公告 |

## 工作流

### 进度清单

```
封面图生成进度：
- [ ] 步骤 1：分析文章内容（标题、标签、主题）
- [ ] 步骤 2：确认风格选项（除非 --quick）
- [ ] 步骤 3：生成图片
- [ ] 步骤 4：验证并保存
```

### 步骤 1：分析文章内容

读取文章的 front matter，提取：
- `title` — 用于判断主题
- `tags` — 用于判断领域
- `description` — 用于理解文章核心

```bash
# 提取 front matter
head -30 <文章目录>/index.md
```

### 步骤 2：确认风格选项

除非用户指定了 `--quick` 或通过参数指定了所有维度，否则用 `AskUserQuestion` 展示推荐选项让用户选择：

- 展示推荐的风格组合及理由
- 提供 2-3 个备选方案
- 用户可以选择或自定义

### 步骤 3：生成图片

按优先级尝试两种方案。详细的 API 调用代码和 Pillow 兜底脚本见 [references/generation-methods.md](references/generation-methods.md)。

**方案 A（首选）**：直连 Gemini 生图（已弃用 Rube MCP）
- 读取 [base-prompt.md](references/base-prompt.md) 获取系统级生图指令
- 根据文章内容和选定维度构造英文提示词
- 跑 `references/gemini-generate.py`（用 `GOOGLE_API_KEY`，先出 4K 再降采样存 WebP）

**方案 B（兜底）**：Python/Pillow 程序化生成
- 当 AI 生图失败时使用
- 深色渐变背景 + 文章标题 + 标签

提示词构造要点：
- 必须用**英文**
- 先描述视觉结构，再描述内容主题
- 结尾加 `No text, no watermarks, no logos.`
- 根据选定的维度加入对应的风格修饰词（参考 [auto-selection.md](references/auto-selection.md)）

### 步骤 4：验证并保存

生成后必须验证：

```
验证清单：
- [ ] 文件名为 cover.webp
- [ ] 尺寸 1200×630
- [ ] 大小 < 200KB
- [ ] 用 Read 工具查看图片，确认无乱码/无文字错误
- [ ] 内容与文章主题相关
```

验证方法：
```bash
# 检查文件大小
ls -la <文章目录>/cover.webp

# 用 Read 工具查看图片内容
# Read <文章目录>/cover.webp
```

如果图片有问题（乱码、文字错误、主题不符），重新生成。

## 批量模式

`--batch` 模式下，扫描所有缺少 cover.webp 的文章目录：

```bash
# 找出缺少封面图的文章
for dir in content/posts/ai/*/; do
  if [ -f "${dir}index.md" ] && [ ! -f "${dir}cover.webp" ]; then
    echo "缺少封面图: $(basename $dir)"
  fi
done
```

逐个用 `--quick` 模式生成，风格自动推断。

## 重新生成

如果需要重新生成已有封面图：

1. 备份旧图：`mv cover.webp cover.webp.bak`
2. 重新生成
3. 确认满意后删除备份：`rm cover.webp.bak`

## 与其他 skill 的关系

- **blog-writer** 的步骤 3 调用本 skill 生成封面图
- **blog-growth** 的并行生产阶段通过 blog-writer 间接使用
- 也可以**独立使用**——为已有文章补充或更换封面图
