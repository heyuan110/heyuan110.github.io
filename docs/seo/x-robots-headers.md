# X-Robots-Tag 分层策略（非 HTML 资源）

Hugo 仅生成文件，无法直接为特定目录添加响应头。以下需在 Nginx/CDN 层配置。

## Nginx 配置示例

```nginx
# 低价值文档与临时目录
location ^~ /docs/ {
  add_header X-Robots-Tag "noindex, follow" always;
}

location ^~ /tmp/ {
  add_header X-Robots-Tag "noindex, nofollow" always;
}

# 非 HTML 资源（可选）
location ~* \.(pdf|txt|json)$ {
  add_header X-Robots-Tag "noindex, follow" always;
}
```

## Cloudflare Transform Rules（可选）

- 条件：URI Path starts with `/docs/` 或 `/tmp/`
- 动作：Set response header `X-Robots-Tag`
  - `/docs/` -> `noindex, follow`
  - `/tmp/` -> `noindex, nofollow`

## 验证

```bash
curl -I https://www.heyuan110.com/docs/xxx.pdf
curl -I https://www.heyuan110.com/tmp/test.txt
```

确认返回头中存在 `X-Robots-Tag`。
