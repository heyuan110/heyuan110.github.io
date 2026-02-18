# URL 规范化与重定向（生产可执行）

目标：统一到 `https://www.heyuan110.com/`，并保持末尾斜杠策略（目录 URL 使用 trailing slash）。

## 1) Nginx（推荐）

```nginx
# 80 -> https
server {
  listen 80;
  server_name heyuan110.com www.heyuan110.com;
  return 301 https://www.heyuan110.com$request_uri;
}

# https non-www -> https www
server {
  listen 443 ssl http2;
  server_name heyuan110.com;
  # ssl_certificate ...
  # ssl_certificate_key ...
  return 301 https://www.heyuan110.com$request_uri;
}

# canonical host
server {
  listen 443 ssl http2;
  server_name www.heyuan110.com;
  # ... your root / static config

  # 如需强制目录 URL trailing slash（仅无扩展名路径）
  rewrite ^([^.]*[^/])$ $1/ permanent;
}
```

## 2) Cloudflare Rules（如使用）

- Always Use HTTPS: ON
- Single Redirect Rule:
  - If hostname equals `heyuan110.com`
  - Then 301 to `https://www.heyuan110.com/${uri}`

## 3) 验证命令

```bash
curl -I http://heyuan110.com/
curl -I https://heyuan110.com/
curl -I https://www.heyuan110.com/posts/
```

期望：前两条均 301 到 `https://www.heyuan110.com/...`；最后一条 200。

## 4) 说明

仓库层已统一 canonical 输出为 `https + www + trailing slash`，但**域名规范化 301 仍必须在服务器/CDN 层生效**。
