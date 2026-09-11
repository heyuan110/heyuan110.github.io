#!/usr/bin/env python3
"""中文版「AI 味 / 翻译腔」量化体检。

用法:
  python3 scripts/check-zh-prose.py content/posts/ai/*/index.zh.md
  python3 scripts/check-zh-prose.py --all          # 全站中文文章

红线(见 memory: zh-prose-red-flags):破折号是最灵的单一指标,超过 10 基本可判翻译腔。
"""
import glob
import re
import sys

LIMITS = {
    "dash": 10,        # —— 总数
    "semi": 5,         # ；总数
    "para_avg": 120,   # 段落平均字数
    "para_long": 40,   # 超 120 字段落占比 %
    "sent_avg": 55,    # 平均句长
    "sent_long": 30,   # 超 60 字长句占比 %
}
VAGUE = ["那个东西", "这件事", "那件事", "这一点", "那一点", "这种东西", "上面那个"]
SKIP_PREFIX = ("#", "|", "!", ">", "-", "*", "```")


def measure(path: str) -> dict:
    raw = open(path, encoding="utf-8").read()
    body = raw.split("+++", 2)[2] if raw.startswith("+++") else raw
    body = re.sub(r"```.*?```", "", body, flags=re.S)          # 代码/mermaid
    body = re.sub(r"^\s*\d+\.\s.*$", "", body, flags=re.M)     # 有序列表(系列导航)
    paras = [p.strip() for p in body.split("\n\n")
             if p.strip() and not p.strip().startswith(SKIP_PREFIX)]
    if not paras:
        return {}
    lens = [len(p) for p in paras]
    sents = [x for p in paras for x in re.split(r"[。！？]", p) if x.strip()]
    slens = [len(x) for x in sents] or [0]
    return {
        "dash": body.count("——"),
        "semi": body.count("；"),
        "para_avg": sum(lens) // len(lens),
        "para_long": sum(1 for x in lens if x > 120) * 100 // len(lens),
        "sent_avg": sum(slens) // len(slens),
        "sent_long": sum(1 for x in slens if x > 60) * 100 // len(slens),
        "vague": sum(body.count(v) for v in VAGUE),
        "_paras": len(paras),
    }


def main() -> int:
    args = sys.argv[1:]
    files = sorted(glob.glob("content/posts/*/*/index.zh.md")) if args == ["--all"] else args
    if not files:
        print("用法: check-zh-prose.py <index.zh.md ...> | --all")
        return 1
    hdr = f'{"文章":<46}{"破折号":>7}{"分号":>6}{"段均":>6}{"长段%":>7}{"句均":>6}{"长句%":>7}{"虚指":>6}  判定'
    print(hdr)
    print("-" * len(hdr))
    failed = 0
    for f in files:
        m = measure(f)
        if not m:
            continue
        bad = [k for k, v in LIMITS.items() if m[k] > v]
        if bad:
            failed += 1
        name = f.split("/")[3][:44]
        flag = "❌ " + ",".join(bad) if bad else "✅"
        print(f'{name:<46}{m["dash"]:>7}{m["semi"]:>6}{m["para_avg"]:>6}'
              f'{m["para_long"]:>7}{m["sent_avg"]:>6}{m["sent_long"]:>7}{m["vague"]:>6}  {flag}')
    print(f"\n{len(files)} 篇中 {failed} 篇超标")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
