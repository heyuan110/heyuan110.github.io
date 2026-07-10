#!/usr/bin/env python3
"""把博客英文文章发布到 dev.to(官方 REST API,替代已弃用的 Rube MCP)。

用法:
  python3 scripts/devto-publish.py content/posts/ai/2026-07-10-claude-fable-5-guide          # 存草稿
  python3 scripts/devto-publish.py content/posts/ai/2026-07-10-claude-fable-5-guide --publish # 直接发布

API key 放 ~/.config/devto/api_key(dev.to → Settings → Extensions → Generate API Key)。
处理:TOML front matter → dev.to 元数据;相对图片/内链 → 绝对 URL;mermaid 块 → 回原文链接;
自动附 canonical_url + "Originally published" 尾注。
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

SITE = "https://www.heyuan110.com"
KEY_FILE = Path.home() / ".config/devto/api_key"


def die(msg):
    print(f"✗ {msg}")
    sys.exit(1)


def parse_front_matter(text):
    m = re.match(r"^\+\+\+\n(.*?)\n\+\+\+\n(.*)$", text, re.S)
    if not m:
        die("没找到 TOML front matter(+++)")
    fm_raw, body = m.groups()
    fm = {}
    for line in fm_raw.splitlines():
        kv = re.match(r"^(\w+)\s*=\s*(.+)$", line.strip())
        if not kv:
            continue
        k, v = kv.groups()
        if v.startswith("["):
            fm[k] = re.findall(r"['\"]([^'\"]+)['\"]", v)
        else:
            fm[k] = v.strip().strip("'\"")
    return fm, body


def article_url(article_dir):
    slug = Path(article_dir).name
    section = Path(article_dir).parent.name
    return f"{SITE}/posts/{section}/{slug}/"


def transform(body, url, slug_dir):
    # 相对图片 → 线上绝对 URL(Hugo page bundle 图与文章同目录)
    body = re.sub(r"!\[([^\]]*)\]\((?!http)([^)]+)\)", rf"![\1]({url}\2)", body)
    # 站内链接 → 绝对 URL
    body = re.sub(r"\]\((/(?:zh/)?posts/[^)]+)\)", rf"]({SITE}\1)", body)
    # mermaid 块 dev.to 不渲染 → 回原文
    body = re.sub(
        r"```mermaid\n.*?\n```",
        f"*(interactive diagram — [view it on the original post]({url}))*",
        body, flags=re.S)
    # Hugo shortcode 清理
    body = re.sub(r"\{\{<[^>]*>\}\}", "", body)
    return body.strip()


def main():
    if len(sys.argv) < 2:
        die("用法: devto-publish.py <文章目录> [--publish]")
    art_dir = Path(sys.argv[1])
    publish = "--publish" in sys.argv
    md = art_dir / "index.md"
    if not md.exists():
        die(f"{md} 不存在(只发英文版)")
    if not KEY_FILE.exists():
        die(f"缺 API key:去 dev.to Settings → Extensions 生成,存到 {KEY_FILE}")
    key = KEY_FILE.read_text().strip()

    fm, body = parse_front_matter(md.read_text())
    url = article_url(art_dir)
    body = transform(body, url, art_dir.name)
    body += f"\n\n---\n\n*Originally published at [heyuan110.com]({url})*\n"

    tags = [re.sub(r"[^a-z0-9]", "", t.lower()) for t in fm.get("tags", [])][:4]
    payload = {"article": {
        "title": fm["title"],
        "body_markdown": body,
        "published": publish,
        "canonical_url": url,
        "tags": tags,
        "description": fm.get("description", "")[:150],
    }}
    req = urllib.request.Request(
        "https://dev.to/api/articles",
        data=json.dumps(payload).encode(),
        headers={"api-key": key, "Content-Type": "application/json",
                 "User-Agent": "heyuan110-distributor/1.0"},
        method="POST")
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        die(f"dev.to API {e.code}: {e.read().decode()[:300]}")
    state = "已发布" if publish else "草稿"
    print(f"✓ {state} → {resp.get('url', '(见 dev.to dashboard)')}")


if __name__ == "__main__":
    main()
