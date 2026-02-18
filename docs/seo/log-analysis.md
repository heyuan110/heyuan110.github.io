# 抓取日志分析基础设施（可执行）

若当前无法直接拿到服务器日志，可先按本文件定义字段并接入脚本。

## 1) 期望日志格式（Nginx combined 示例）

```nginx
log_format seo_combined '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        'rt=$request_time';
access_log /var/log/nginx/access.log seo_combined;
```

## 2) 分析脚本

`python3 scripts/seo/analyze_crawl_logs.py /path/to/access.log`

输出：
- 抓取量 Top bots
- 状态码分布
- 404 Top URL
- 按目录抓取分布

## 3) 抓取目标字段

- 时间戳
- 请求路径
- 状态码
- UA（含 bot 分类）
- Referer
- 耗时（request_time）

## 4) 用途

- 识别被高频抓取但低价值目录（可配 noindex / robots）
- 识别 canonical/重定向链问题（301/302 异常高峰）
- 识别 404 热点，回补内容或定向 301
