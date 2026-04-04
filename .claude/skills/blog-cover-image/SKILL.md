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

按优先级尝试两种方案：

#### 方案 A（首选）：Rube MCP + Gemini AI 生图

**第一步：搜索工具**

```
调用 RUBE_SEARCH_TOOLS：
  query: "generate an AI image from a text prompt"
  session: {generate_id: true}
```

**第二步：构造提示词并生成**

```
调用 RUBE_MULTI_EXECUTE_TOOL：
  tool_slug: GEMINI_GENERATE_IMAGE
  arguments:
    prompt: <英文提示词，见下方模板>
    model: "gemini-2.5-flash-image"
    aspect_ratio: "16:9"
  sync_response_to_workbench: false
```

**提示词构造规则**：
- 必须用**英文**（Gemini 对英文效果更好）
- 描述具体画面内容、视觉元素、色彩氛围
- 结尾加 `No text, no watermarks, no logos.`
- 根据风格维度调整描述：
  - tech → "futuristic, digital, glowing circuits, holographic"
  - minimal → "clean, geometric, whitespace, simple shapes"
  - conceptual → "metaphorical, symbolic, abstract representation"
  - diagram → "isometric, blueprint style, technical illustration"
  - cinematic → "dramatic lighting, depth of field, atmospheric"

**提示词模板**（根据文章内容填充）：

```
A [style] illustration for a technical blog article about [topic].
Visual elements: [elements description based on article content].
Color scheme: [palette description].
Style: [rendering style], professional, suitable for a tech blog cover.
No text, no watermarks, no logos.
```

**第三步：下载并转换**

```bash
# 从返回结果的 data.image.s3url 下载（URL 有时效，尽快下载）
curl -sL -o cover_raw.png "<s3url>"

# 转换为 WebP 并调整尺寸
python3 -c "
from PIL import Image
img = Image.open('cover_raw.png').resize((1200, 630), Image.LANCZOS)
img.save('cover.webp', 'WEBP', quality=85)
import os; os.remove('cover_raw.png')
size_kb = os.path.getsize('cover.webp') / 1024
print(f'封面图已生成: cover.webp ({size_kb:.1f} KB)')
"
```

如果 AI 生图失败（连接不可用、安全过滤拦截等），使用方案 B。

#### 方案 B（兜底）：Python/Pillow 程序化生成

当 AI 生图不可用时，用 Pillow 程序化生成：

```python
python3 -c "
from PIL import Image, ImageDraw, ImageFont

# 从文章 front matter 提取
TITLE = '<文章标题>'
SUBTITLE = '<文章描述前 50 字>'
TAGS = ['<标签1>', '<标签2>', '<标签3>']
OUTPUT = '<文章目录>/cover.webp'

WIDTH, HEIGHT = 1200, 630
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# 深色渐变背景
for y in range(HEIGHT):
    r = int(15 + (25 - 15) * y / HEIGHT)
    g = int(23 + (35 - 23) * y / HEIGHT)
    b = int(42 + (60 - 42) * y / HEIGHT)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# 顶部装饰线
for x in range(WIDTH):
    alpha = int(255 * (1 - abs(x - WIDTH/2) / (WIDTH/2)))
    draw.line([(x, 0), (x, 3)], fill=(100, 149, 237, alpha))

# 加载字体（按优先级尝试多个 macOS 系统字体）
FONT_PATHS = [
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    '/System/Library/Fonts/PingFang.ttc',
]
def load_font(size):
    for path in FONT_PATHS:
        try: return ImageFont.truetype(path, size)
        except: continue
    return ImageFont.load_default()

ft, fs, fg = load_font(52), load_font(28), load_font(20)

# 标题自动换行
lines, cur = [], ''
for ch in TITLE:
    test = cur + ch
    if draw.textbbox((0,0), test, font=ft)[2] > WIDTH - 120:
        lines.append(cur); cur = ch
    else: cur = test
if cur: lines.append(cur)

y = 180 if len(lines) <= 2 else 140
for line in lines:
    w = draw.textbbox((0,0), line, font=ft)[2] - draw.textbbox((0,0), line, font=ft)[0]
    draw.text(((WIDTH-w)//2, y), line, fill='white', font=ft); y += 70

# 副标题
if SUBTITLE:
    w = draw.textbbox((0,0), SUBTITLE, font=fs)[2] - draw.textbbox((0,0), SUBTITLE, font=fs)[0]
    draw.text(((WIDTH-w)//2, y+20), SUBTITLE, fill=(180,180,200), font=fs)

# 标签
ty = HEIGHT - 80
tw = sum(draw.textbbox((0,0), f' {t} ', font=fg)[2] + 24 for t in TAGS) + 12*(len(TAGS)-1)
tx = (WIDTH - tw) // 2
for t in TAGS:
    txt = f' {t} '
    bb = draw.textbbox((0,0), txt, font=fg)
    bw, bh = bb[2]-bb[0], bb[3]-bb[1]
    draw.rounded_rectangle([(tx, ty), (tx+bw+20, ty+bh+14)], radius=6, fill=(40,60,100), outline=(80,120,180))
    draw.text((tx+10, ty+7), txt, fill=(160,200,255), font=fg)
    tx += bw + 32

img.save(OUTPUT, 'WEBP', quality=85)
import os
print(f'封面图已生成: {OUTPUT} ({os.path.getsize(OUTPUT)/1024:.1f} KB)')
"
```

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
