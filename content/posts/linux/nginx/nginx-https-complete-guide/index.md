+++
date = '2020-07-03T13:19:44+08:00'
draft = false
title = 'Nginx HTTPS Configuration Guide: Self-Signed Certs, Mixed Sites, and Reverse Proxy Pitfalls'
description = 'Practical guide to Nginx HTTPS covering self-signed SSL certificates with OpenSSL, selective HTTPS for mixed HTTP/HTTPS sites, and fixing DNS caching issues when reverse proxying to AWS ELB'
toc = true
tags = ['Nginx', 'HTTPS', 'SSL', 'AWS', '反向代理']
categories = ['Linux']
keywords = ['nginx https configuration', 'self-signed ssl certificate', 'nginx reverse proxy aws elb', 'nginx mixed http https', 'nginx dns cache fix']
+++

Configuring HTTPS on Nginx is a core skill for any backend engineer working in production. This article covers three real-world scenarios I have dealt with in actual projects: setting up self-signed certificates, running a mixed HTTP/HTTPS site, and debugging a nasty DNS caching issue when reverse proxying to AWS ELB.

## 1. Self-Signed SSL Certificates with OpenSSL

In development and testing environments, self-signed certificates let you enable HTTPS without purchasing a certificate from a third-party CA.

### 1.1 Install OpenSSL

Check if OpenSSL is already installed:

```bash
openssl version -a
```

If not, install it:

```bash
sudo apt-get install openssl
sudo apt-get install openssl-devel
```

### 1.2 Generate the Private Key and Certificate

The process has four steps:

**Step 1: Generate a private key**

```bash
openssl genrsa -des3 -out app.key 1024
```

You will be prompted to set a passphrase.

**Step 2: Create a Certificate Signing Request (CSR)**

```bash
openssl req -new -key app.key -out app.csr
```

Fill in the requested fields (country, state, organization, etc.).

**Step 3: Generate a passphrase-free server key**

```bash
openssl rsa -in app.key -out app_server.key
```

**Step 4: Sign the certificate**

```bash
openssl req -new -x509 -days 3650 -key app_server.key -out app_server.crt
```

**Make sure the Common Name matches your domain name** — this is the most common mistake.

You now have four files. The two you need are `app_server.crt` (certificate) and `app_server.key` (private key).

### 1.3 Configure Nginx

Copy the certificate files to the Nginx configuration directory:

```bash
cp app_server.crt app_server.key /etc/nginx/conf.d/
```

Enable SSL in your Nginx config:

```nginx
server {
    listen       443 ssl;
    server_name  www.example.com;

    ssl_certificate     /etc/nginx/conf.d/app_server.crt;
    ssl_certificate_key /etc/nginx/conf.d/app_server.key;

    # Recommended SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    location / {
        root   /var/www/html;
        index  index.html;
    }
}
```

Test and restart Nginx:

```bash
sudo nginx -t
sudo service nginx restart
```

> **Note:** Self-signed certificates are for development and testing only. For production, use Let's Encrypt or a commercial CA.

## 2. Selective HTTPS: Running a Mixed HTTP/HTTPS Site

Sometimes you only need HTTPS on specific pages — a checkout flow, a login page — while the rest of the site stays on HTTP.

### 2.1 Requirements

- Default to HTTP for the entire site
- Force HTTPS on sensitive paths like `/checkout`
- Automatically redirect requests that do not match the rules

### 2.2 How It Works

- **HTTP server (port 80):** If the path matches a sensitive route, 301 redirect to HTTPS
- **HTTPS server (port 443):** If the path does NOT match a sensitive route, 301 redirect back to HTTP

The implementation relies on Nginx `location` blocks combined with `proxy_pass`.

### 2.3 Full Configuration

```nginx
# Redirect bare domain to www
server {
    server_name example.com;
    rewrite ^/(.*) http://www.example.com/$1 permanent;
}

# HTTP server (port 80)
server {
    listen       80;
    server_name  www.example.com;

    # Enable Gzip compression
    gzip on;
    gzip_min_length 1k;
    gzip_buffers 16 64k;
    gzip_http_version 1.1;
    gzip_comp_level 4;
    gzip_types text/plain application/javascript text/css application/xml;
    gzip_vary on;

    access_log  /var/log/nginx/access.log;
    error_log   /var/log/nginx/error.log;

    # Sensitive pages: force redirect to HTTPS
    location ~* /checkout/* {
        return 301 https://$host$request_uri;
    }

    # Everything else: proxy over HTTP
    location / {
        proxy_pass         http://backend;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        proxy_buffer_size  64k;
        proxy_buffers      4 32k;
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_redirect     off;
    }
}

# HTTPS server (port 443)
server {
    listen       443 ssl;
    server_name  www.example.com;

    ssl_certificate     /etc/nginx/ssl/website_ssl.crt;
    ssl_certificate_key /etc/nginx/ssl/website_ssl.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log  /var/log/nginx/sslaccess.log;
    error_log   /var/log/nginx/sslerror.log;

    # Sensitive pages: proxy over HTTPS
    location ~* /checkout/* {
        proxy_pass        http://backend;
        proxy_read_timeout 300;
        proxy_set_header  Host $host;
        proxy_set_header  X-Real-IP $remote_addr;
        proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_redirect    off;
    }

    # Static assets: serve over HTTPS to prevent mixed content warnings
    location ~ \.(css|js|gif|jpg|woff|woff2|png|ico)$ {
        proxy_pass http://backend;
    }

    # Non-sensitive pages: redirect back to HTTP
    location / {
        return 301 http://$server_name$request_uri;
    }
}
```

### 2.4 Key Points

- `location ~*` performs case-insensitive regex matching
- Static assets on HTTPS pages must also be served over HTTPS — otherwise browsers will show **Mixed Content** warnings
- The `X-Forwarded-Proto` header tells the backend whether the original request was HTTP or HTTPS

> **Side note:** Full-site HTTPS with HSTS headers is the standard recommendation today. Selective HTTPS is mainly relevant for legacy systems with specific constraints.

## 3. Reverse Proxying to AWS ELB: The DNS Caching Trap

This was a real production incident that took a long time to diagnose.

### 3.1 Symptoms

Architecture: `User -> Nginx Proxy -> Internal hostname (CNAME) -> AWS ELB`

After running for a while, the site would randomly become unreachable. Restarting Nginx on every proxy server would restore service, but the problem kept recurring.

Error log:

```
2020/06/08 16:31:20 [error] 13741#0: *116374839 connect() failed
(113: No route to host) while connecting to upstream,
client: 2607:xxxx:969:f1f0:c3d:70ec:178f:fd24,
server: localhost,
request: "POST /v1.4/source HTTP/1.1",
upstream: "http://172.31.xx.xx:80/v1.4/source",
host: "api.xxxx.com"
```

### 3.2 Investigation

1. **Ruled out firewalls** — most online resources pointed to firewall issues, but that was not the cause
2. **Correlated with monitoring** — the outage timestamps matched exactly with ELB IP address changes
3. **Confirmed with AWS SA** — AWS ELB IPs are dynamic, not static (a common misconception)

### 3.3 Root Cause

**Nginx resolves upstream domain names to IP addresses at startup and caches the results indefinitely.** It does not re-resolve DNS during normal operation.

When the ELB IP changes:
1. DNS records update to point to the new IP
2. Nginx continues using the cached old IP
3. The old IP is no longer valid, so connections fail with "No route to host"

This explains why restarting Nginx temporarily fixed the problem — a restart triggers a fresh DNS lookup.

### 3.4 The Fix

Use the Nginx **jdomain module** for periodic DNS re-resolution:

```nginx
upstream backend {
    jdomain api.example.com interval=10 port=80;
}
```

The `jdomain` module re-resolves the domain name at the specified interval (in seconds), keeping the IP cache up to date.

Reference: [Nginx jdomain module](https://www.nginx.com/resources/wiki/modules/domain_resolve/)

**Alternative approach** using the `resolver` directive with a variable:

```nginx
server {
    resolver 169.254.169.253 valid=10s;  # AWS internal DNS

    location / {
        set $backend "http://api.example.com";
        proxy_pass $backend;
    }
}
```

Placing the domain in a variable forces Nginx to re-resolve DNS on every request.

### 3.5 Lessons Learned

- AWS ELB IPs are **not static** — they change during scaling events and health checks
- Nginx only resolves DNS at startup by default and **never refreshes** the cache
- Any upstream pointing to a domain name (rather than a fixed IP) should use dynamic DNS resolution
- This issue also applies to NLB (Network Load Balancer)

## Summary

| Scenario | Solution | Key Config |
|----------|----------|-----------|
| Dev/test HTTPS | OpenSSL self-signed certificate | `openssl req -new -x509` |
| Selective HTTPS | Location matching + 301 redirects | `return 301 https://` |
| Dynamic IP upstream | jdomain or resolver-based DNS | `jdomain` / `resolver` |

These three scenarios cover the most common HTTPS configuration needs and pitfalls when working with Nginx.