#!/bin/sh
# 每月 1 号自动生成对账清单(由 crontab 调用)
OUT="/Users/bruce/heyuan110.github.io/plans/reports/monthly-review-$(date +%Y-%m).md"
cat > "$OUT" << MD
# 月度对账清单 — $(date +%Y-%m-01)

> 把本文件丢给 Claude 说「月度对账」,按 plans/roadmap-3000usd.md §6 模板走。

## 你要看的后台数字(截图或抄给 Claude)
- [ ] AdSense:上月总收入 + 按广告单元(in-article-en / multiplex-en)拆分
- [ ] **Amazon Associates:点击数 + 成交笔数 ← ⚠️ 出现首笔佣金 → 立即启动 Payoneer 找回**(QQ 邮箱直连重置→不行找微信公众号「Payoneer派安盈」客服;姓名 Yuan He;180 天窗口至 2027-01-06)
- [ ] Bing WMT「AI Performance」:总引用次数(基线 2026-07: 348.4K/3mo)

## Claude 自动跑的
- [ ] 拉最新 GSC+GA → 填 §6 模板 → 更新作战手册 KPI 与排产
- [ ] 刷新 llms.txt Key Articles
MD
echo "$(date): generated $OUT" >> /Users/bruce/heyuan110.github.io/plans/reports/cron.log
