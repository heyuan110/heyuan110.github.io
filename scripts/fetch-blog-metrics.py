#!/usr/bin/env python3
"""Fetch GSC + GA4 metrics for blog diagnostics.

Uses Application Default Credentials (ADC) — run once:
    gcloud auth application-default login \\
        --scopes='openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/analytics.readonly'
    gcloud auth application-default set-quota-project <YOUR_GCP_PROJECT>

Usage:
    python3 scripts/fetch-blog-metrics.py [--days 30] [--out plans/reports/latest.json]

Outputs a single JSON with GSC queries/pages/dates + GA4 overview/pages/channels/daily/devices,
ready to feed into the blog-growth skill for analysis.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

# Force ADC — ignore any pre-set GOOGLE_APPLICATION_CREDENTIALS pointing at
# unrelated service accounts.
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)

import google.auth
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    OrderBy,
    RunReportRequest,
)

GSC_SITE = os.environ.get("GSC_SITE", "sc-domain:heyuan110.com")
GA4_PROPERTY = os.environ.get("GA4_PROPERTY_ID", "519433466")
SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]


def gsc_query(svc, start: str, end: str, dims: list[str], row_limit: int = 5000) -> list[dict]:
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": dims,
        "rowLimit": row_limit,
        "dataState": "final",
    }
    rsp = svc.searchanalytics().query(siteUrl=GSC_SITE, body=body).execute()
    return rsp.get("rows", [])


def run_ga4_report(client, *, start: str, end: str, dimensions: list[str], metrics: list[str],
                    order_by_metric: str | None = None, limit: int = 10000) -> list[dict]:
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), desc=True)]
            if order_by_metric else [],
        limit=limit,
    )
    rsp = client.run_report(req)
    return [
        {
            **{d.name: r.dimension_values[i].value for i, d in enumerate(rsp.dimension_headers)},
            **{m.name: r.metric_values[i].value for i, m in enumerate(rsp.metric_headers)},
        }
        for r in rsp.rows
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30, help="当期窗口天数，默认 30")
    ap.add_argument("--lag", type=int, default=2, help="GSC 数据延迟天数 buffer，默认 2")
    ap.add_argument("--out", type=Path, default=Path("plans/reports/latest-metrics.json"))
    args = ap.parse_args()

    end_cur = date.today() - timedelta(days=args.lag)
    start_cur = end_cur - timedelta(days=args.days - 1)
    end_prev = start_cur - timedelta(days=1)
    start_prev = end_prev - timedelta(days=args.days - 1)

    print(f"→ Current: {start_cur} to {end_cur}", file=sys.stderr)
    print(f"→ Prior:   {start_prev} to {end_prev}", file=sys.stderr)

    creds, project = google.auth.default(scopes=SCOPES)
    print(f"→ ADC project: {project}", file=sys.stderr)

    out: dict = {"window": {"current": [str(start_cur), str(end_cur)],
                              "prior": [str(start_prev), str(end_prev)]},
                 "gsc": {}, "ga4": {}}

    # ---------- GSC ----------
    print("→ Fetching GSC...", file=sys.stderr)
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    out["gsc"]["queries"] = gsc_query(gsc, str(start_cur), str(end_cur), ["query"], row_limit=25000)
    out["gsc"]["pages_current"] = gsc_query(gsc, str(start_cur), str(end_cur), ["page"], row_limit=5000)
    out["gsc"]["dates"] = gsc_query(gsc, str(start_cur), str(end_cur), ["date"], row_limit=50)
    out["gsc"]["pages_prior"] = gsc_query(gsc, str(start_prev), str(end_prev), ["page"], row_limit=5000)
    print(f"  GSC: {len(out['gsc']['queries'])} queries, {len(out['gsc']['pages_current'])} pages, "
          f"{len(out['gsc']['pages_prior'])} prior pages", file=sys.stderr)

    # ---------- GA4 ----------
    print("→ Fetching GA4...", file=sys.stderr)
    ga = BetaAnalyticsDataClient(credentials=creds)

    out["ga4"]["overview_current"] = run_ga4_report(
        ga, start=str(start_cur), end=str(end_cur), dimensions=[],
        metrics=["activeUsers", "sessions", "screenPageViews", "engagementRate", "averageSessionDuration"])
    out["ga4"]["overview_prior"] = run_ga4_report(
        ga, start=str(start_prev), end=str(end_prev), dimensions=[],
        metrics=["activeUsers", "sessions", "screenPageViews", "engagementRate", "averageSessionDuration"])
    out["ga4"]["top_pages"] = run_ga4_report(
        ga, start=str(start_cur), end=str(end_cur), dimensions=["pagePath"],
        metrics=["screenPageViews", "activeUsers", "engagementRate", "averageSessionDuration"],
        order_by_metric="screenPageViews", limit=100)
    out["ga4"]["channels"] = run_ga4_report(
        ga, start=str(start_cur), end=str(end_cur), dimensions=["sessionDefaultChannelGroup"],
        metrics=["sessions", "activeUsers", "engagementRate"], order_by_metric="sessions")
    out["ga4"]["daily"] = run_ga4_report(
        ga, start=str(start_cur), end=str(end_cur), dimensions=["date"],
        metrics=["activeUsers", "sessions", "screenPageViews"])
    out["ga4"]["devices"] = run_ga4_report(
        ga, start=str(start_cur), end=str(end_cur), dimensions=["deviceCategory"],
        metrics=["sessions", "activeUsers", "engagementRate"])
    print(f"  GA4: overview + {len(out['ga4']['top_pages'])} pages + "
          f"{len(out['ga4']['channels'])} channels + {len(out['ga4']['daily'])} days", file=sys.stderr)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"✓ Saved → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
