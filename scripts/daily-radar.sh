#!/bin/sh
cd /Users/bruce/heyuan110.github.io
V=$(env -u GOOGLE_APPLICATION_CREDENTIALS SA_KEY=/Users/bruce/.config/blog-metrics/sa.json /opt/miniconda3/bin/python3 scripts/daily-trends-radar.py 2>>plans/reports/cron.log | tail -1)
osascript -e "display notification \"$V\" with title \"📡 每日热点雷达\" sound name \"Glass\"" 2>/dev/null
