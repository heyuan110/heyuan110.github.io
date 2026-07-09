#!/usr/bin/env python3
"""直连 Gemini 图片 API 生成博客封面 / 配图（替代已停服的 Rube MCP）。

依赖：环境变量 GOOGLE_API_KEY（在 ~/.zshrc 中配置），Pillow。

用法：
  # 封面（固定 1200x630，中心裁剪）
  python3 gemini-generate.py --prompt "<英文提示词>" \
      --output content/posts/ai/2026-xx-xx-slug/cover.webp --resize 1200x630

  # 配图（限制最大宽度，高按比例）
  python3 gemini-generate.py --prompt "<英文提示词>" \
      --output content/posts/ai/2026-xx-xx-slug/01-diagram.webp --max-width 1200

模型默认 gemini-3-pro-image-preview，可用 --model 覆盖
（可选：gemini-2.5-flash-image / gemini-3.1-flash-image / imagen-4.0-generate-001）。
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import urllib.request

from PIL import Image

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"


def generate(prompt: str, model: str, key: str, image_size: str = "4K",
             aspect_ratio: str = "16:9") -> bytes:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect_ratio, "imageSize": image_size},
        },
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        API.format(model=model, key=key),
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    if "error" in data:
        raise RuntimeError(data["error"].get("message", "unknown error"))
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError(f"no image in response: {json.dumps(data)[:300]}")


def save(raw: bytes, output: str, resize: str | None, max_width: int | None) -> None:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    if resize:
        tw, th = (int(x) for x in resize.lower().split("x"))
        sw, sh = img.size
        scale = max(tw / sw, th / sh)  # cover
        img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
        left, top = (img.width - tw) // 2, (img.height - th) // 2
        img = img.crop((left, top, left + tw, top + th))
    elif max_width and img.width > max_width:
        img = img.resize((max_width, round(img.height * max_width / img.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    img.save(output, "WEBP", quality=85, method=6)
    print(f"✓ {output}  {img.size[0]}x{img.size[1]}  {os.path.getsize(output)//1024}KB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--model", default="gemini-3.1-flash-image")
    ap.add_argument("--resize", help="WxH, center-crop cover, e.g. 1200x630")
    ap.add_argument("--max-width", type=int)
    ap.add_argument("--fallback-model", default="gemini-3-pro-image-preview")
    ap.add_argument("--image-size", default="4K", help="1K / 2K / 4K (source render before downscale)")
    args = ap.parse_args()

    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("ERROR: GOOGLE_API_KEY 未设置（检查 ~/.zshrc / source 一下）", file=sys.stderr)
        return 2

    for model in [args.model, args.fallback_model]:
        try:
            raw = generate(args.prompt, model, key, image_size=args.image_size)
            save(raw, args.output, args.resize, args.max_width)
            if model != args.model:
                print(f"  (used fallback model {model})", file=sys.stderr)
            return 0
        except Exception as e:
            print(f"  {model} failed: {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
