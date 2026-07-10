#!/usr/bin/env python3
"""HTML 级扫描:正文里可见的字面 ** = Markdown 加粗解析断裂(CJK 标点紧贴 ** 的坑)。
先 hugo --minify 再跑。发布前必查,同 check-mermaid.mjs。"""
import re, glob, sys
bad = []
for f in glob.glob('public/**/posts/**/index.html', recursive=True):
    html = open(f, encoding='utf-8', errors='ignore').read()
    body = re.sub(r'<(pre|code|script|style)[^>]*>.*?</\1>', '', html, flags=re.S)
    body = re.sub(r'<div class="mermaid[^"]*"[^>]*>.*?</div>', '', body, flags=re.S)
    hits = re.findall(r'[^\s>]{0,20}\*\*[^\s<]{0,20}', body)
    if hits: bad.append((f.replace('public/','').replace('/index.html',''), hits[0][:50]))
if bad:
    print(f"❌ {len(bad)} 页有加粗断裂:")
    for p, h in bad: print(f"  {p}  例: {h}")
    sys.exit(1)
print("✅ 全站加粗渲染正常")
