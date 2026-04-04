"""
图片下载并转换为 WebP 格式。
用于将 AI 生图（Gemini）返回的 S3 URL 下载并转换为博客规范的 WebP 格式。

用法：
  # 封面图（固定 1200x630）
  python3 convert-to-webp.py --url "<s3url>" --output "path/to/cover.webp" --resize 1200x630

  # 配图（限制最大宽度 1200，高度按比例）
  python3 convert-to-webp.py --url "<s3url>" --output "path/to/01-type-slug.webp" --max-width 1200

  # 本地文件转换（不下载）
  python3 convert-to-webp.py --input "raw.png" --output "cover.webp" --resize 1200x630
"""

import argparse
import os
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    print("错误：缺少 Pillow 库。请运行以下命令安装：")
    print(f"  {sys.executable} -m pip install Pillow")
    print("\n或者使用 pip3：")
    print("  pip3 install Pillow")
    sys.exit(1)


def download(url, temp_path):
    """从 URL 下载图片到本地临时文件"""
    result = subprocess.run(
        ['curl', '-sL', '-o', temp_path, url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"下载失败: {result.stderr}")
    if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
        raise RuntimeError("下载文件为空")


def convert(input_path, output_path, resize=None, max_width=None, quality=85):
    """将图片转换为 WebP 格式"""
    img = Image.open(input_path)

    if resize:
        w, h = resize
        img = img.resize((w, h), Image.LANCZOS)
    elif max_width and img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

    img.save(output_path, 'WEBP', quality=quality)
    size_kb = os.path.getsize(output_path) / 1024
    print(f'已生成: {output_path} ({size_kb:.1f} KB, {img.width}x{img.height})')


def main():
    parser = argparse.ArgumentParser(description='下载并转换图片为 WebP 格式')
    parser.add_argument('--url', help='图片 URL（从 Gemini S3 下载）')
    parser.add_argument('--input', help='本地图片路径（不需要下载时使用）')
    parser.add_argument('--output', required=True, help='输出 WebP 文件路径')
    parser.add_argument('--resize', help='固定尺寸，格式：WxH（如 1200x630）')
    parser.add_argument('--max-width', type=int, default=1200, help='最大宽度（默认 1200）')
    parser.add_argument('--quality', type=int, default=85, help='WebP 质量（默认 85）')
    args = parser.parse_args()

    if not args.url and not args.input:
        parser.error('必须指定 --url 或 --input')

    # 解析 resize 参数
    resize = None
    if args.resize:
        parts = args.resize.lower().split('x')
        resize = (int(parts[0]), int(parts[1]))

    # 下载或使用本地文件
    temp_path = args.input
    need_cleanup = False
    if args.url:
        temp_path = args.output.rsplit('.', 1)[0] + '_raw.png'
        download(args.url, temp_path)
        need_cleanup = True

    try:
        convert(temp_path, args.output, resize=resize, max_width=args.max_width, quality=args.quality)
    finally:
        if need_cleanup and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    main()
