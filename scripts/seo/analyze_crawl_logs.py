#!/usr/bin/env python3
import re
import sys
from collections import Counter
from urllib.parse import urlparse

LOG_RE = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) \S+ "(?P<referer>[^"]*)" "(?P<ua>[^"]*)"')
BOT_HINTS = ["googlebot", "bingbot", "baiduspider", "yandexbot", "duckduckbot", "petalbot", "bytespider", "gptbot", "claudebot", "applebot"]


def is_bot(ua: str) -> bool:
    u = ua.lower()
    return any(h in u for h in BOT_HINTS) or "bot" in u or "spider" in u or "crawl" in u


def normalize_path(raw: str) -> str:
    if raw.startswith("http://") or raw.startswith("https://"):
        return urlparse(raw).path or "/"
    return raw.split("?")[0]


def top_dir(path: str) -> str:
    parts = [p for p in path.split("/") if p]
    return "/" + parts[0] + "/" if parts else "/"


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_crawl_logs.py /path/to/access.log")
        sys.exit(1)

    f = sys.argv[1]
    bots = Counter()
    status = Counter()
    not_found = Counter()
    dirs = Counter()

    with open(f, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            m = LOG_RE.match(line.strip())
            if not m:
                continue
            ua = m.group("ua")
            if not is_bot(ua):
                continue
            path = normalize_path(m.group("path"))
            sc = m.group("status")
            status[sc] += 1
            dirs[top_dir(path)] += 1
            bots[ua.split("/")[0][:80]] += 1
            if sc == "404":
                not_found[path] += 1

    print("== Top Bots ==")
    for k, v in bots.most_common(15):
        print(f"{v:>6}  {k}")

    print("\n== Status Codes ==")
    for k, v in sorted(status.items(), key=lambda x: (-x[1], x[0])):
        print(f"{v:>6}  {k}")

    print("\n== Top Directories ==")
    for k, v in dirs.most_common(20):
        print(f"{v:>6}  {k}")

    print("\n== 404 URLs ==")
    for k, v in not_found.most_common(30):
        print(f"{v:>6}  {k}")


if __name__ == "__main__":
    main()
