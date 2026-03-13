+++
date = '2016-04-22T20:33:37+08:00'
draft = true
title = 'Nginx Partial HTTPS: Serving Mixed HTTP/HTTPS Sites with Location-Based Routing'
description = 'How to configure Nginx for selective HTTPS on specific pages using location blocks and proxy_pass, with automatic HTTP/HTTPS redirects and full config example'
toc = true
tags = ['Nginx', 'HTTPS', 'SSL', '反向代理']
categories = ['Linux']
keywords = ['nginx partial https', 'nginx mixed http https', 'nginx location https redirect', 'selective https nginx']
+++

For a project I was working on, the checkout page needed to be served over HTTPS while the rest of the site stayed on plain HTTP. I had done full-site HTTPS before, but selective HTTPS was a different challenge. After comparing several approaches — hardcoding URLs in the application code vs. handling it at the server level — I decided Nginx was the right place to manage this.

## The Requirement

- The entire site runs on HTTP by default
- The `/checkout` page (and its subpaths) must be served over HTTPS
- Any request that violates these rules should be automatically redirected

## The Approach

The logic is straightforward:

1. **On the HTTP server (port 80):** If the request path matches `/checkout`, issue a 301 redirect to the HTTPS version
2. **On the HTTPS server (port 443):** If the request path does NOT match `/checkout`, issue a 301 redirect back to HTTP

The tricky part was implementing the "not checkout" logic cleanly in Nginx. I ended up using `proxy_pass` to handle the routing, which worked well.

## Full Nginx Configuration

Replace `server_name` with your own domain. This setup uses `proxy_pass` to forward traffic to a backend load balancer.

```nginx
# Redirect bare domain to www
server {
    server_name heyuan110.com;
    rewrite ^/(.*) http://www.heyuan110.com/$1 permanent;
}

# HTTP server (port 80)
server {
    listen       80;
    server_name  www.heyuan110.com;

    gzip on;
    gzip_min_length 1k;
    gzip_buffers 16 64k;
    gzip_http_version 1.1;
    gzip_comp_level 4;
    gzip_types text/plain application/javascript application/x-javascript text/css application/xml;
    gzip_vary on;

    access_log  /var/log/nginx/access.log;
    error_log   /var/log/nginx/error.log;

    # Force HTTPS for sensitive pages
    location ~* /news/show/* {
        return  301 https://$host$request_uri;
    }

    # Everything else proxied over HTTP
    location / {
           proxy_pass        http://web;
           proxy_connect_timeout 600;
           proxy_read_timeout 600;
           proxy_send_timeout 600;
           proxy_buffer_size 64k;
           proxy_buffers  4 32k;
           proxy_busy_buffers_size 64k;
           proxy_temp_file_write_size 64k;
           proxy_set_header   Host             $host;
           proxy_set_header   X-Real-IP        $remote_addr;
           proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
           proxy_redirect     off;
    }

    location = /robots.txt {
        return 200 "User-agent: *\nDisallow:";
    }

    location ~ ^/nginx_status/ {
        stub_status on;
        access_log off;
    }
}

# HTTPS server (port 443)
server {
    listen       443 ssl;
    server_name  www.heyuan110.com;

    access_log  /var/log/nginx/sslaccess.log;
    error_log   /var/log/nginx/sslerror.log;

    ssl on;
    ssl_prefer_server_ciphers on;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ALL:!ADH:!EXP:!LOW:!RC2:!3DES:!SEED:!RC4:+HIGH:+MEDIUM;
    ssl_certificate /usr/local/nginx/conf/ssl/website_ssl.crt;
    ssl_certificate_key /usr/local/nginx/conf/ssl/website_ssl.key;

    # Sensitive pages served over HTTPS
    location ~* /news/show/* {
        proxy_pass http://web;
        proxy_read_timeout 300;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect     off;

        # Tell the backend the original protocol
        proxy_set_header X-Forwarded-Proto  $scheme;
    }

    # Static assets also served over HTTPS to avoid mixed content warnings
    location ~ \.(css|js|gif|jpg|woff|woff2|png|ico)$ {
        proxy_pass  http://web;
    }

    # All other paths redirect back to HTTP
    location / {
      return  301 http://$server_name$request_uri;
    }
}
```

## Key Takeaways

- Use `location ~*` for case-insensitive regex matching of URL paths
- Static assets on HTTPS pages must also be served over HTTPS, otherwise browsers will show **Mixed Content** warnings
- The `X-Forwarded-Proto` header lets your backend application know whether the original request was HTTP or HTTPS

> **Note:** Today, full-site HTTPS with HSTS is the recommended approach for most sites. Selective HTTPS like this is mainly useful for legacy projects with specific constraints.