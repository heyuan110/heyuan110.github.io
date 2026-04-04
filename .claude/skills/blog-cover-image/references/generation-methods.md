# 生图方案

## 方案 A（首选）：Rube MCP + Gemini AI 生图

### 第一步：搜索工具

```
调用 RUBE_SEARCH_TOOLS：
  query: "generate an AI image from a text prompt"
  session: {generate_id: true}
```

### 第二步：构造提示词并生成

先读取 [base-prompt.md](base-prompt.md) 获取系统级指令，然后根据文章内容和选定的维度构造提示词。

```
调用 RUBE_MULTI_EXECUTE_TOOL：
  tool_slug: GEMINI_GENERATE_IMAGE
  arguments:
    prompt: <英文提示词>
    model: "gemini-2.5-flash-image"
    aspect_ratio: "16:9"
  sync_response_to_workbench: false
```

### 第三步：下载并转换

图片 URL 在返回结果的 `data.image.s3url` 中（URL 有时效，需尽快下载）：

```bash
curl -sL -o cover_raw.png "<s3url>"

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

---

## 方案 B（兜底）：Python/Pillow 程序化生成

当 AI 生图不可用时，用 Pillow 程序化生成。根据文章 front matter 中的 title、description、tags 填充参数：

```python
python3 -c "
from PIL import Image, ImageDraw, ImageFont

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

# 加载字体
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

⚠️ 方案 B 生成后必须用 Read 工具查看图片，确认无乱码。
