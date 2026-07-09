#!/usr/bin/env python3
"""IndexNow 推送:把 URL 秒级提交给 Bing/DuckDuckGo/Naver 等(Google 不支持,走 sitemap)。

用法:
  python3 scripts/indexnow.py <url> [url ...]          # 指定 URL
  python3 scripts/indexnow.py --recent [N]             # 最近 N 个 commit 里新增/修改的文章(默认 5)
"""
import json
import re
import subprocess
import sys
import urllib.request

HOST = "www.heyuan110.com"
KEY = "648e8f4eda5b4f50b41efd08709c12fe"
BASE = f"https://{HOST}"


def recent_article_urls(n: int) -> list[str]:
    out = subprocess.run(
        ["git", "log", f"-{n}", "--name-only", "--pretty=format:"],
        capture_output=True, text=True).stdout
    urls = set()
    for line in out.splitlines():
        m = re.match(r"content/posts/(.+)/index(\.zh)?\.md$", line.strip())
        if m:
            slug, zh = m.group(1), m.group(2)
            urls.add(f"{BASE}/zh/posts/{slug}/" if zh else f"{BASE}/posts/{slug}/")
    return sorted(urls)


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] == "--recent":
        urls = recent_article_urls(int(args[1]) if len(args) > 1 else 5)
    else:
        urls = args
    if not urls:
        print("no urls"); return 1
    body = json.dumps({"host": HOST, "key": KEY,
                       "keyLocation": f"{BASE}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow HTTP {r.status} — submitted {len(urls)} urls")
        for u in urls: print(" ", u)
    return 0


if __name__ == "__main__":
    sys.exit(main())
