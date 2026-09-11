#!/usr/bin/env python3
"""把中文正文里的 ASCII / 弯引号统一成站点风格的直角引号「」。

站点风格:中文引用一律用「」(全站 54 篇如此,只有 3 篇例外)。
Agent 改写中文时常把它退化成 " 或 “”,这个脚本负责纠回来。

只动正文,不动:front matter(TOML 用 " 定界)、围栏代码块、行内代码、Markdown 链接的 URL 部分。
只转换「引号内含有汉字」的片段,英文术语的引号保持原样。

用法:
  python3 scripts/normalize-zh-quotes.py content/posts/ai/*/index.zh.md
  python3 scripts/normalize-zh-quotes.py --check <file>   # 只报告不改写
"""
import re
import sys

CJK = r"一-鿿"
PAT = re.compile(rf'["“]([^"“”\n]*[{CJK}][^"“”\n]*)["”]')


def process(path: str, write: bool = True) -> int:
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("+++"):
        return 0
    _, fm, body = raw.split("+++", 2)

    stash: list[str] = []

    def keep(m: re.Match) -> str:
        stash.append(m.group(0))
        return f"\x00{len(stash) - 1}\x00"

    guarded = re.sub(r"```.*?```", keep, body, flags=re.S)   # 围栏代码块
    guarded = re.sub(r"`[^`\n]+`", keep, guarded)            # 行内代码
    guarded = re.sub(r"\]\([^)\s]+\)", keep, guarded)        # 链接 URL

    n = len(PAT.findall(guarded))
    if write and n:
        guarded = PAT.sub(r"「\1」", guarded)
        for i, chunk in enumerate(stash):
            guarded = guarded.replace(f"\x00{i}\x00", chunk)
        open(path, "w", encoding="utf-8").write("+++" + fm + "+++" + guarded)
    return n


def main() -> int:
    args = sys.argv[1:]
    check = args and args[0] == "--check"
    files = args[1:] if check else args
    if not files:
        print("用法: normalize-zh-quotes.py [--check] <index.zh.md ...>")
        return 1
    total = 0
    for f in files:
        n = process(f, write=not check)
        total += n
        if n:
            verb = "待转换" if check else "已转换"
            print(f"{verb} {n:>3} 处  {f.split('/')[3]}")
    print(f"合计 {total} 处" + ("(未写入)" if check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
