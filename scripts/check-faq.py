#!/usr/bin/env python3
"""FAQ 结构化数据质量校验(FAQPage schema 是 GEO 最值钱的块,不能敷衍)。

红线:
  1. 条数 3-7
  2. 问题必须是疑问句(中文含 ？/吗/怎么/为什么/哪/多少/能不能;英文含 ? )
  3. 答案长度:英文 180-700 字符,中文 60-300 字
  4. 整组答案里至少半数(且≥2条)含具体信息:数字/版本号/命令/价格。定义型问答可以没有
  5. 同一篇内问题不得重复,答案不得雷同(前 40 字符相同即判重)
  6. 语言必须与文件匹配(index.md 英文 / index.zh.md 中文)

用法:
  python3 scripts/check-faq.py content/posts/ai/*/index*.md
  python3 scripts/check-faq.py --all          # 全站
  python3 scripts/check-faq.py --missing      # 只列出缺 FAQ 的文件
"""
import glob
import re
import sys

CJK = re.compile(r"[一-鿿]")
ZH_Q = re.compile(r"[？?]|吗|怎么|如何|为什么|哪|多少|能不能|是什么|要不要|值不值")
HAS_FACT = re.compile(r"\d|`[^`]+`|v\d|\$")


def parse(path: str):
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("+++"):
        return None
    fm = raw.split("+++", 2)[1]
    items = []
    for blk in re.split(r"\[\[params\.faqItems\]\]", fm)[1:]:
        q = re.search(r'^question\s*=\s*"(.*)"\s*$', blk, re.M)
        a = re.search(r'^answer\s*=\s*"(.*)"\s*$', blk, re.M)
        if q and a:
            items.append((q.group(1), a.group(1)))
    return items


def check(path: str) -> list[str]:
    items = parse(path)
    if items is None:
        return ["无 front matter"]
    if not items:
        return ["缺 FAQ"]
    zh = path.endswith("index.zh.md")
    errs = []
    if not 3 <= len(items) <= 7:
        errs.append(f"条数 {len(items)}(应 3-7)")
    facts = sum(1 for _, a in items if HAS_FACT.search(a))
    if facts < max(2, (len(items) + 1) // 2):
        errs.append(f"仅 {facts}/{len(items)} 条答案含具体信息(应≥半数且≥2)")
    qs, heads = set(), set()
    for i, (q, a) in enumerate(items, 1):
        if zh and not CJK.search(q):
            errs.append(f"Q{i} 非中文")
        if not zh and CJK.search(q):
            errs.append(f"Q{i} 混入中文")
        if zh and not ZH_Q.search(q):
            errs.append(f"Q{i} 不像疑问句")
        if not zh and "?" not in q:
            errs.append(f"Q{i} 缺问号")
        lo, hi = (60, 300) if zh else (180, 700)
        if not lo <= len(a) <= hi:
            errs.append(f"A{i} 长度 {len(a)}(应 {lo}-{hi})")
        if q in qs:
            errs.append(f"Q{i} 与前文重复")
        qs.add(q)
        h = a[:40]
        if h in heads:
            errs.append(f"A{i} 与前文雷同")
        heads.add(h)
    return errs


def main() -> int:
    args = sys.argv[1:]
    missing_only = args and args[0] == "--missing"
    if missing_only:
        args = args[1:]
    files = sorted(glob.glob("content/posts/*/*/index*.md")) if (not args or args[0] == "--all") else args
    bad = ok = 0
    for f in files:
        errs = check(f)
        if missing_only:
            if errs == ["缺 FAQ"]:
                print(f)
            continue
        if errs:
            bad += 1
            print(f"❌ {f.split('/', 2)[2]}\n     {'; '.join(errs[:6])}")
        else:
            ok += 1
    if not missing_only:
        print(f"\n通过 {ok} / 不合格 {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
