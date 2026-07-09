#!/usr/bin/env python3
"""每周选题报告:拉最新 GSC+GA 数据 → 挖机会 → 写 plans/reports/weekly-YYYY-MM-DD.md。

crontab 每周一早自动跑;手动跑:
  SA_KEY=~/.config/blog-metrics/sa.json python3 scripts/weekly-topic-report.py [--skip-fetch]
"""
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / "plans/reports/latest-metrics.json"
OUT = ROOT / f"plans/reports/weekly-{date.today()}.md"


def cn(s: str) -> bool:
    return any("一" <= ch <= "鿿" for ch in s)


def main() -> int:
    if "--skip-fetch" not in sys.argv:
        env = {**os.environ}
        env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
        env.setdefault("SA_KEY", str(Path.home() / ".config/blog-metrics/sa.json"))
        subprocess.run([sys.executable, str(ROOT / "scripts/fetch-blog-metrics.py"),
                        "--days", "28", "--out", str(METRICS)], env=env, check=True)

    d = json.loads(METRICS.read_text())
    g, ga = d["gsc"], d["ga4"]
    Q = [{"k": r["keys"][0], "c": r["clicks"], "i": r["impressions"],
          "ctr": r["ctr"], "p": r["position"]} for r in g["queries"]]
    pages = {r["keys"][0]: r for r in g["pages_current"]}
    prior = {r["keys"][0]: r for r in g["pages_prior"]}

    tot_c = sum(p["clicks"] for p in pages.values())
    tot_i = sum(p["impressions"] for p in pages.values())
    prev_c = sum(p["clicks"] for p in prior.values())

    L = [f"# 每周选题报告 — {date.today()}", "",
         f"窗口:{d['window']['current'][0]} ~ {d['window']['current'][1]}(vs 上一个 28 天)", "",
         "## 大盘", "",
         f"- GSC 点击 **{tot_c}**(上期 {prev_c},{(tot_c-prev_c)/max(prev_c,1)*100:+.0f}%)"
         f" | 展示 {tot_i:,} | CTR {tot_c/max(tot_i,1)*100:.2f}%"]
    oc = ga["overview_current"][0]
    op = ga["overview_prior"][0]
    L.append(f"- GA4 PV **{float(oc['screenPageViews']):.0f}**(上期 {float(op['screenPageViews']):.0f})"
             f" | 用户 {float(oc['activeUsers']):.0f} | 互动率 {float(oc['engagementRate'])*100:.0f}%")

    # 涨跌页面
    L += ["", "## 涨跌 Top 5(按点击变化)", ""]
    delta = []
    for url, r in pages.items():
        pc = prior.get(url, {}).get("clicks", 0)
        if r["clicks"] + pc >= 15:
            delta.append((r["clicks"] - pc, r["clicks"], pc, url))
    for sign, arr in [("📈", sorted(delta, reverse=True)[:5]), ("📉", sorted(delta)[:5])]:
        for dv, c, pc, url in arr:
            slug = url.replace("https://www.heyuan110.com", "")
            L.append(f"- {sign} {dv:+d}({pc}→{c}) `{slug}`")

    # 机会词:有排名、有展示、没点透
    junk = re.compile(r"referral|since:|after:|\"")
    opp = [q for q in Q if q["i"] >= 120 and 5 <= q["p"] <= 30
           and q["ctr"] < 0.03 and not junk.search(q["k"])]
    L += ["", "## 🎯 机会词(展示≥120 / pos 5-30 / CTR<3% / 非垃圾)", ""]
    for q in sorted(opp, key=lambda x: -x["i"])[:15]:
        L.append(f"- {q['i']:>5}i {q['c']:>3}c {q['ctr']*100:4.1f}% pos{q['p']:4.1f}"
                 f" {'🀄' if cn(q['k']) else 'EN'} `{q['k'][:60]}`")

    # 高 CTR 长尾:已命中,可系列深耕
    hot = [q for q in Q if q["ctr"] > 0.10 and q["i"] > 50 and not junk.search(q["k"])]
    L += ["", "## 🔥 高 CTR 长尾(CTR>10% / 展示>50)→ 系列深耕候选", ""]
    for q in sorted(hot, key=lambda x: -x["c"])[:10]:
        L.append(f"- {q['c']:>3}c {q['i']:>5}i {q['ctr']*100:4.1f}%"
                 f" {'🀄' if cn(q['k']) else 'EN'} `{q['k'][:60]}`")

    # 词根簇
    stop = {"the", "for", "with", "claude", "code", "2026", "how", "what", "best"}
    root: dict = defaultdict(lambda: [0, 0])
    for q in Q:
        for t in set(re.findall(r"[a-z0-9]{4,}|[一-鿿]{2,}", q["k"].lower())):
            if t not in stop:
                root[t][0] += q["i"]
                root[t][1] += 1
    L += ["", "## 🧲 搜索引力词根 Top 15(总展示 / 查询数)", ""]
    for t, (imp, n) in sorted(root.items(), key=lambda x: -x[1][0])[:15]:
        if n >= 4:
            L.append(f"- {imp:>7,}i × {n:>4} 词 — **{t}**")

    L += ["", "---", "",
          "**下一步**:把本报告发给 Claude(`/blog-growth` 或直接问\"本周写什么\"),"
          "结合外部热点(Google Trends / HN)定 2-3 个选题并行开写。",
          "写文铁律:中英双版 / blog-writer skill / 英文优先变现。"]

    OUT.write_text("\n".join(L))
    print(f"✓ {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
