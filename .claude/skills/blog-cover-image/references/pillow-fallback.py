"""
封面图 Pillow 兜底方案
当 AI 生图（Gemini）不可用时，用此脚本程序化生成封面图。

用法：
  python3 pillow-fallback.py --title "文章标题" --subtitle "描述前50字" --tags "tag1,tag2,tag3" --output "path/to/cover.webp"
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("错误：缺少 Pillow 库。请运行以下命令安装：")
    print(f"  {sys.executable} -m pip install Pillow")
    print("\n或者使用 pip3：")
    print("  pip3 install Pillow")
    sys.exit(1)

# macOS 字体路径（其他平台需调整）
# Linux: '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
# Windows: 'C:/Windows/Fonts/msyh.ttc'
FONT_PATHS = [
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    '/System/Library/Fonts/PingFang.ttc',
]

WIDTH, HEIGHT = 1200, 630


def load_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_cover(title, subtitle, tags, output):
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
        alpha = int(255 * (1 - abs(x - WIDTH / 2) / (WIDTH / 2)))
        draw.line([(x, 0), (x, 3)], fill=(100, 149, 237, alpha))

    ft, fs, fg = load_font(52), load_font(28), load_font(20)

    # 标题自动换行
    lines, cur = [], ''
    for ch in title:
        test = cur + ch
        if draw.textbbox((0, 0), test, font=ft)[2] > WIDTH - 120:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)

    y = 180 if len(lines) <= 2 else 140
    for line in lines:
        w = draw.textbbox((0, 0), line, font=ft)[2] - draw.textbbox((0, 0), line, font=ft)[0]
        draw.text(((WIDTH - w) // 2, y), line, fill='white', font=ft)
        y += 70

    # 副标题
    if subtitle:
        w = draw.textbbox((0, 0), subtitle, font=fs)[2] - draw.textbbox((0, 0), subtitle, font=fs)[0]
        draw.text(((WIDTH - w) // 2, y + 20), subtitle, fill=(180, 180, 200), font=fs)

    # 标签
    if tags:
        ty = HEIGHT - 80
        tw = sum(draw.textbbox((0, 0), f' {t} ', font=fg)[2] + 24 for t in tags) + 12 * (len(tags) - 1)
        tx = (WIDTH - tw) // 2
        for t in tags:
            txt = f' {t} '
            bb = draw.textbbox((0, 0), txt, font=fg)
            bw, bh = bb[2] - bb[0], bb[3] - bb[1]
            draw.rounded_rectangle(
                [(tx, ty), (tx + bw + 20, ty + bh + 14)],
                radius=6, fill=(40, 60, 100), outline=(80, 120, 180)
            )
            draw.text((tx + 10, ty + 7), txt, fill=(160, 200, 255), font=fg)
            tx += bw + 32

    img.save(output, 'WEBP', quality=85)
    size_kb = os.path.getsize(output) / 1024
    print(f'封面图已生成: {output} ({size_kb:.1f} KB)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成博客封面图（Pillow 兜底方案）')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--subtitle', default='', help='文章描述前50字')
    parser.add_argument('--tags', default='', help='标签，逗号分隔')
    parser.add_argument('--output', required=True, help='输出路径')
    args = parser.parse_args()

    tag_list = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []
    generate_cover(args.title, args.subtitle, tag_list, args.output)
