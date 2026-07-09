#!/usr/bin/env python3
"""拉指定页面的 GSC 逐页 top 搜索词(近 28 天),用于 CTR 标题优化。
用: SA_KEY=~/.config/blog-metrics/sa.json python3 scripts/page-queries.py"""
import os, sys
from datetime import date, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

SITE = "sc-domain:heyuan110.com"
KEY = os.environ["SA_KEY"]
creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

end = date.today() - timedelta(days=2)
start = end - timedelta(days=27)

PAGES = [
    "/posts/ai/2026-04-14-hermes-agent-guide/",
    "/posts/ai/2026-02-25-claude-code-pricing/",
    "/posts/ai/2026-02-15-draw-things-ultimate-guide/",
    "/posts/ai/2026-02-15-mac-mini-local-image-generation/",
]
for p in PAGES:
    url = "https://www.heyuan110.com" + p
    body = {
        "startDate": str(start), "endDate": str(end),
        "dimensions": ["query"], "rowLimit": 15, "dataState": "final",
        "dimensionFilterGroups": [{"filters": [
            {"dimension": "page", "operator": "equals", "expression": url}]}],
    }
    rows = svc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])
    print(f"\n=== {p} ===")
    for r in rows:
        q = r["keys"][0]
        print(f"  {r['impressions']:>7.0f}i {r['clicks']:>4.0f}c {r['ctr']*100:>5.2f}% pos{r['position']:>5.1f}  {q}")
