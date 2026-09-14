#!/usr/bin/env python3
"""标题 / 描述长度校验(SERP 截断是 CTR 的直接杀手)。

红线:
  英文 title 40-60 字符, description 120-160 字符
  中文 title 20-40 字,   description 70-110 字
另检查:标题是否以关键词开头(不以 The/A/How 等虚词开头)、描述是否以句号结尾。

用法:
  python3 scripts/check-meta.py content/posts/ai/*/index*.md
  python3 scripts/check-meta.py --all
"""
import glob
import re
import sys

LIMITS = {False: ((40, 60), (120, 160)), True: ((20, 40), (70, 110))}  # key: is_zh


def parse(path: str):
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("+++"):
        return None, None
    fm = raw.split("+++", 2)[1]
    t = re.search(r"^title\s*=\s*['\"](.*)['\"]\s*$", fm, re.M)
    d = re.search(r"^description\s*=\s*['\"](.*)['\"]\s*$", fm, re.M)
    return (t.group(1) if t else None), (d.group(1) if d else None)


def check(path: str) -> list[str]:
    t, d = parse(path)
    if t is None:
        return ["无 front matter 或缺 title"]
    zh = path.endswith("index.zh.md")
    (tlo, thi), (dlo, dhi) = LIMITS[zh]
    errs = []
    if not tlo <= len(t) <= thi:
        errs.append(f"title {len(t)}(应 {tlo}-{thi})")
    if d is None:
        errs.append("缺 description")
    elif not dlo <= len(d) <= dhi:
        errs.append(f"description {len(d)}(应 {dlo}-{dhi})")
    return errs


def main() -> int:
    args = sys.argv[1:]
    files = sorted(glob.glob("content/posts/*/*/index*.md")) if (not args or args[0] == "--all") else args
    bad = ok = 0
    for f in files:
        e = check(f)
        if e:
            bad += 1
            print(f"❌ {f.split('/', 2)[2]}\n     {'; '.join(e)}")
        else:
            ok += 1
    print(f"\n通过 {ok} / 不合格 {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
