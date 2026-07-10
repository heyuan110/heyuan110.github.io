#!/usr/bin/env python3
"""每日热点雷达:Google Trends(US) + HN 头版 + GSC 突涨词 → 一页简报。
crontab 每天中午跑;手动: SA_KEY=~/.config/blog-metrics/sa.json python3 scripts/daily-trends-radar.py"""
import json
import os
import re
import ssl
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / f"plans/reports/daily-radar-{date.today()}.md"
CTX = ssl.create_default_context()

AI_KW = re.compile(
    r"\b(ai|gpt|claude|openai|anthropic|llm|agent|copilot|cursor|gemini|deepseek|"
    r"mcp|coding|developer|programming|python|rust|javascript|github|model|api|"
    r"stable diffusion|midjourney|sora|veo|seedance|hugging ?face|nvidia|vibe)\b", re.I)


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 radar/1.0"})
    return urllib.request.urlopen(req, timeout=timeout, context=CTX).read().decode("utf-8", "ignore")


def google_trends():
    try:
        xml = fetch("https://trends.google.com/trending/rss?geo=US")
        items = re.findall(r"<title>(.*?)</title>.*?<ht:approx_traffic>(.*?)</ht:approx_traffic>", xml, re.S)
        hits = [(t.strip(), tr) for t, tr in items if AI_KW.search(t)]
        return hits[:8], len(items)
    except Exception as e:
        return [(f"(拉取失败: {e})", "")], 0


def hn_front():
    try:
        ids = json.loads(fetch("https://hacker-news.firebaseio.com/v0/topstories.json"))[:30]
        hits = []
        for i in ids:
            try:
                it = json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{i}.json", 10))
            except Exception:
                continue
            title, score = it.get("title", ""), it.get("score", 0)
            if score >= 80 and AI_KW.search(title):
                hits.append((score, title, it.get("url", f"https://news.ycombinator.com/item?id={i}")))
        return sorted(hits, reverse=True)[:8]
    except Exception as e:
        return [(0, f"(拉取失败: {e})", "")]


def gsc_risers():
    """近 3 天 vs 前 7 天,展示翻倍且 ≥30 的查询词"""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        key = os.environ.get("SA_KEY", str(Path.home() / ".config/blog-metrics/sa.json"))
        creds = service_account.Credentials.from_service_account_file(
            key, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
        svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        end = date.today() - timedelta(days=2)

        def q(s, e):
            body = {"startDate": str(s), "endDate": str(e), "dimensions": ["query"],
                    "rowLimit": 2000, "dataState": "all"}
            rows = svc.searchanalytics().query(siteUrl="sc-domain:heyuan110.com", body=body).execute().get("rows", [])
            return {r["keys"][0]: r["impressions"] for r in rows}

        cur = q(end - timedelta(days=2), end)              # 近3天
        base = q(end - timedelta(days=9), end - timedelta(days=3))  # 前7天
        risers = []
        for k, v in cur.items():
            b = base.get(k, 0) * 3 / 7  # 折算成3天基线
            if v >= 30 and v > max(b * 2, 15):
                risers.append((v, round(b), k))
        return sorted(risers, reverse=True)[:10]
    except Exception as e:
        return [(0, 0, f"(拉取失败: {e})")]


gt, gt_total = google_trends()
hn = hn_front()
risers = gsc_risers()

hot = bool([1 for _, t, _ in hn if t and "失败" not in t]) or bool([1 for t, _ in gt if "失败" not in t])
verdict = "⚡ 有热点候选,见下表" if hot else "😴 无 AI 相关热点,按选题池走"

L = [f"# 每日热点雷达 — {date.today()}", "", f"**结论:{verdict}**", "",
     "## Google Trends(US 24h,AI/开发相关)", ""]
L += [f"- {tr:>6} {t}" for t, tr in gt] or ["- (无命中)"]
L += ["", f"## Hacker News 头版(≥80 分,AI/开发相关)", ""]
L += [f"- {s:>4}⬆ [{t}]({u})" for s, t, u in hn] or ["- (无命中)"]
L += ["", "## GSC 突涨词(近3天 vs 前7天,翻倍且≥30展示)", ""]
L += [f"- {v}i(基线 {b})`{k}`" for v, b, k in risers] or ["- (无突涨)"]
L += ["", "---", "丢给 Claude:「看雷达,今天写什么」"]

OUT.write_text("\n".join(L))
print(f"✓ {OUT}")
print(verdict)
