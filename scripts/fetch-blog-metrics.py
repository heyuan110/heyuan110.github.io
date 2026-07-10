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

import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    OrderBy,
    RunReportRequest,
)

GSC_SITE = os.environ.get("GSC_SITE", "sc-domain:heyuan110.com")
GA4_PROPERTY = os.environ.get("GA4_PROPERTY_ID", "519433466")
# 该 GA4 属性同时收 usemagictools.com 等自有站点的数据(约占 27% PV),
# 外加若干抄走 Measurement ID 的 blogspot 镜像站。不过滤则本站数字虚高。
# 设为空字符串可关闭过滤(拉全属性数据)。
GA4_HOST = os.environ.get("GA4_HOST", "www.heyuan110.com")
SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]
# Prefer a service-account key (bypasses OAuth restricted-scope blocking).
# Set SA_KEY env to a PERSONAL service-account key; falls back to ADC.
# Do NOT default to a work/company key here.
SA_KEY = os.environ.get("SA_KEY")


def get_credentials():
    if SA_KEY and os.path.exists(SA_KEY):
        print(f"→ Auth: service account {SA_KEY}", file=sys.stderr)
        creds = service_account.Credentials.from_service_account_file(SA_KEY, scopes=SCOPES)
        return creds, getattr(creds, "project_id", None)
    print("→ Auth: application default credentials", file=sys.stderr)
    return google.auth.default(scopes=SCOPES)


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


def host_filter() -> FilterExpression | None:
    """把结果限定在本站 hostName，排除同属性下的其它站点与镜像站。"""
    if not GA4_HOST:
        return None
    return FilterExpression(
        filter=Filter(field_name="hostName", string_filter=Filter.StringFilter(value=GA4_HOST))
    )


def run_ga4_report(client, *, start: str, end: str, dimensions: list[str], metrics: list[str],
                    order_by_metric: str | None = None, limit: int = 10000) -> list[dict]:
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        dimension_filter=host_filter(),
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

    creds, project = get_credentials()
    print(f"→ Auth project: {project}", file=sys.stderr)

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
    print(f"→ Fetching GA4... (hostName filter: {GA4_HOST or 'NONE — 含其它站点数据'})", file=sys.stderr)
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
