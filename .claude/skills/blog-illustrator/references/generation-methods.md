# 配图生成方案

> 2026-07 起：**弃用 Rube MCP（已停服），一律直连 Gemini 图片 API。**
> 密钥用环境变量 `GOOGLE_API_KEY`（配在 `~/.zshrc`）。

## 方案 A（首选）：直连 Gemini 生图

复用 blog-cover-image 的 [gemini-generate.py](../../blog-cover-image/references/gemini-generate.py)
（直接调 `generativelanguage.googleapis.com`，先按 4K 出图 → Pillow 降采样 → WebP q85）。

### 第一步：构造提示词

根据文章内容和选定的类型/风格构造**英文**提示词，参考 [prompt-templates.md](prompt-templates.md) 获取各类型模板。

### 第二步：生成（一条命令完成生成+转换）

```bash
python3 .claude/skills/blog-cover-image/references/gemini-generate.py \
  --prompt "<英文提示词>" \
  --output "content/posts/ai/2026-xx-xx-slug/01-type-slug.webp" \
  --max-width 1200 --image-size 4K
```

- 默认模型 `gemini-3.1-flash-image`，失败自动回退 `gemini-3-pro-image-preview`
- 4K 源图单张约 30s，批量时每张单独跑或后台跑，别让单次 shell 调用超时

## 重要说明

- **提示词必须用英文**——英文提示词生成效果更好
- **图片中英文版共用**——同一篇文章的中英文版共享所有配图
- 命名格式：`NN-<类型>-<简短描述>.webp`（如 `01-comparison-tool-matrix.webp`）
- 最大宽度 1200px，质量 85，WebP 格式
- 生成后必须用 Read 工具查看图片，确认内容与文章主题相关
