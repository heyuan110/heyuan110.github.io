# 生图方案

> 2026-07 起：**弃用 Rube MCP，一律直连 Gemini 图片 API。** 密钥用环境变量
> `GOOGLE_API_KEY`（配在 `~/.zshrc`，跑脚本前 `source ~/.zshrc` 或确保已导出）。

## 方案 A+（技术博客文字封面首选）：无头 Chrome 渲染 HTML 编辑级封面

AI 生图搞不定清晰文字，做出来常是"漂亮但看不懂主题"的抽象雕塑。技术博客封面
**一眼看懂 + 有逼格**的正解是 Stripe/Vercel/Linear 那种**排版驱动**的编辑级封面：
大标题钩子 + 分类标签 + 副题观点 + 主题色 + 克制 motif + 品牌页脚。

用 [render-cover.mjs](render-cover.mjs)（无头 Chrome 渲染 HTML → 2x 截图 → Pillow 转 1200x630 WebP）：

```bash
node .claude/skills/blog-cover-image/references/render-cover.mjs '{
  "output":"content/posts/ai/2026-xx-xx-slug/cover.webp",
  "tag":"AI · CLAUDE", "kicker":"副题·2026", "title":"核心概念(英文短词最佳)",
  "sub":"一句观点钩子", "accent":"#2dd4bf", "motif":"{ }"
}'
# 批量：--file spec.json（数组）。waitUntil 用 domcontentloaded + 400ms 等字体。
```

- 每篇一个 accent 主题色 + 一个切题 motif（`>_` 终端 / `◔` 用量 / `⚙` 工作流 / `↻` 循环 / `{ }` 上下文）。
- title 用英文短概念最清晰、跨中英双语通用；sub/kicker 用中文抛观点。
- 渲染后必须 Read 确认排版不溢出、motif 符号正常。

**何时用 A+ vs A**：概念/方法论/对比/清单类文章 → A+（文字讲得清）；
需要强场景感/情绪/产品实物的文章 → 方案 A（Gemini 生图，但隐喻必须一眼可读，别抽象）。

## 方案 A（备选）：直连 Gemini 生图

用 [gemini-generate.py](gemini-generate.py)，它直接调用
`generativelanguage.googleapis.com` 的 `:generateContent` 接口，内置：
先按 `imageConfig` 出 **4K 16:9** 源图 → Pillow 高质量降采样/中心裁剪到目标尺寸 → 存 WebP(q85)。

```bash
# 封面（4K 源 → 1200x630 中心裁剪）
python3 .claude/skills/blog-cover-image/references/gemini-generate.py \
  --prompt "<英文提示词>" \
  --output content/posts/ai/2026-xx-xx-slug/cover.webp \
  --resize 1200x630 --image-size 4K

# 配图（限制最大宽度，高按比例）
python3 .claude/skills/blog-cover-image/references/gemini-generate.py \
  --prompt "<英文提示词>" \
  --output content/posts/ai/2026-xx-xx-slug/01-diagram.webp \
  --max-width 1200
```

- 默认模型 `gemini-3.1-flash-image`，失败自动回退 `gemini-3-pro-image-preview`。
  可用 `--model` 覆盖（`gemini-2.5-flash-image` / `imagen-4.0-generate-001` 等）。
- 4K 源图单张约 30s，比 1K 慢但降采样后明显更锐利、更高级。批量时注意别让
  单次 shell 调用超时（每张单独跑，或后台跑）。
- 提示词先读 [base-prompt.md](base-prompt.md) 取系统级构图/图标规范。

**高级感封面提示词配方（实测有效）**：`Premium high-end tech editorial cover
illustration, 16:9` + 单一 hero 主体 + `clean modern 3D + refined studio
lighting + soft shadows + rim light` + `deep charcoal-navy background + subtle
gradient + depth-of-field bokeh` + 克制色板(`midnight blue + 一个 electric-teal
强调色 + 一丝 warm amber`) + `photorealistic material (glass, brushed metal, soft
matte)` + `No text, no watermarks, no logos.` 参照 Apple keynote / Stripe 品牌图。

生成后**必须**用 Read 工具查看图片确认质量（构图、切题、无乱码文字）。

## 方案 B（兜底）：Python/Pillow 程序化生成

仅当 Gemini API 不可用（网络/额度/安全过滤）时用 [pillow-fallback.py](pillow-fallback.py)：

```bash
python3 .claude/skills/blog-cover-image/references/pillow-fallback.py \
  --title "文章标题" --subtitle "文章描述前50字" \
  --tags "tag1,tag2,tag3" \
  --output content/posts/ai/2026-xx-xx-slug/cover.webp
```

深色渐变 + 自动换行标题 + 标签气泡，中英文字体自适应。生成后同样要 Read 确认无乱码。
