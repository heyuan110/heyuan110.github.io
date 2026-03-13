+++
date = '2020-07-03T13:19:44+08:00'
draft = false
title = 'Nginx HTTPS 配置完全指南：自签名证书、混合站点与反向代理踩坑'
description = 'Nginx HTTPS 配置实战合集：OpenSSL 自签名 SSL 证书生成、部分页面 HTTPS 混合站点配置、反向代理 AWS ELB 时 DNS 动态解析踩坑与解决方案'
toc = true
tags = ['Nginx', 'HTTPS', 'SSL', 'AWS', '反向代理']
categories = ['Linux']
keywords = ['Nginx HTTPS 配置', 'SSL 证书', '自签名证书', 'Nginx 反向代理', 'AWS ELB']
+++

在生产环境中配置 Nginx HTTPS 是后端工程师的必备技能。本文整合了我在实际项目中遇到的三个典型场景：自签名证书配置、HTTP/HTTPS 混合站点、以及反向代理 AWS ELB 时的 DNS 解析踩坑，一次性讲清楚。

## 一、OpenSSL 自签名 SSL 证书

在开发测试环境中，我们通常使用自签名证书来启用 HTTPS，不需要购买第三方证书。

### 1.1 安装 OpenSSL

先检查是否已安装：

```bash
openssl version -a
```

如未安装：

```bash
sudo apt-get install openssl
sudo apt-get install openssl-devel
```

### 1.2 生成私钥和证书

整个流程分四步：

**第一步：生成私钥**

```bash
openssl genrsa -des3 -out app.key 1024
```

执行后会提示输入密码，这个密码后面会用到。

**第二步：生成签署申请（CSR）**

```bash
openssl req -new -key app.key -out app.csr
```

执行后需要填写一些信息（国家、省份、组织名等），密码可以都输同一个。

**第三步：生成服务器私钥**

```bash
openssl rsa -in app.key -out app_server.key
```

**第四步：签署证书**

```bash
openssl req -new -x509 -days 3650 -key app_server.key -out app_server.crt
```

填写信息时，**Common Name 一定要填写你的域名**，这是最容易出错的地方。

完成后得到四个文件，我们需要的是 `app_server.crt`（证书）和 `app_server.key`（私钥）。

### 1.3 配置 Nginx

将证书文件拷贝到 Nginx 配置目录：

```bash
cp app_server.crt app_server.key /etc/nginx/conf.d/
```

在 Nginx 配置中启用 SSL：

```nginx
server {
    listen       443 ssl;
    server_name  www.example.com;

    ssl_certificate     /etc/nginx/conf.d/app_server.crt;
    ssl_certificate_key /etc/nginx/conf.d/app_server.key;

    # 推荐的 SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    location / {
        root   /var/www/html;
        index  index.html;
    }
}
```

重启 Nginx 使配置生效：

```bash
sudo nginx -t          # 先检查配置语法
sudo service nginx restart
```

> **注意**：自签名证书仅用于开发测试。生产环境建议使用 Let's Encrypt 免费证书或购买商业证书。

## 二、部分页面 HTTPS：HTTP/HTTPS 混合站点

有时候我们不需要全站 HTTPS，只需要特定页面（比如支付页面、登录页面）走 HTTPS 加密。

### 2.1 需求

- 全站默认 HTTP 访问
- `/checkout` 等敏感页面强制 HTTPS
- 不符合规则的请求自动跳转

### 2.2 实现思路

- HTTP 访问时：判断路径包含 `/checkout`，强制 301 跳转到 HTTPS
- HTTPS 访问时：判断非敏感路径，强制 301 跳转回 HTTP

核心是利用 Nginx 的 `location` 匹配和 `proxy_pass` 反向代理。

### 2.3 完整配置

```nginx
# 裸域名跳转到 www
server {
    server_name example.com;
    rewrite ^/(.*) http://www.example.com/$1 permanent;
}

# HTTP 服务（端口 80）
server {
    listen       80;
    server_name  www.example.com;

    # 开启 Gzip 压缩
    gzip on;
    gzip_min_length 1k;
    gzip_buffers 16 64k;
    gzip_http_version 1.1;
    gzip_comp_level 4;
    gzip_types text/plain application/javascript text/css application/xml;
    gzip_vary on;

    access_log  /var/log/nginx/access.log;
    error_log   /var/log/nginx/error.log;

    # 敏感页面强制跳转 HTTPS
    location ~* /checkout/* {
        return 301 https://$host$request_uri;
    }

    # 其他页面正常代理
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

# HTTPS 服务（端口 443）
server {
    listen       443 ssl;
    server_name  www.example.com;

    ssl_certificate     /etc/nginx/ssl/website_ssl.crt;
    ssl_certificate_key /etc/nginx/ssl/website_ssl.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log  /var/log/nginx/sslaccess.log;
    error_log   /var/log/nginx/sslerror.log;

    # 敏感页面走 HTTPS 代理
    location ~* /checkout/* {
        proxy_pass        http://backend;
        proxy_read_timeout 300;
        proxy_set_header  Host $host;
        proxy_set_header  X-Real-IP $remote_addr;
        proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_redirect    off;
    }

    # 静态资源走 HTTPS 代理（避免混合内容警告）
    location ~ \.(css|js|gif|jpg|woff|woff2|png|ico)$ {
        proxy_pass http://backend;
    }

    # 非敏感页面跳回 HTTP
    location / {
        return 301 http://$server_name$request_uri;
    }
}
```

### 2.4 要点总结

- `location ~*` 使用正则匹配，不区分大小写
- HTTPS 下的静态资源也要走 HTTPS 代理，否则浏览器会报**混合内容（Mixed Content）**警告
- `X-Forwarded-Proto` 头让后端知道原始请求是 HTTP 还是 HTTPS

> **补充**：如今大多数场景推荐全站 HTTPS，配合 HSTS 头部使用。部分 HTTPS 的方案适用于特定的历史遗留项目。

## 三、反向代理 AWS ELB 的 DNS 踩坑

这是一个在生产环境中遇到的真实问题，排查了很久才定位到根因。

### 3.1 问题现象

架构链路：`用户 → Nginx Proxy → 内部域名 (CNAME) → AWS ELB`

运行一段时间后，访问时不时挂掉。重启 Nginx Proxy 集群里所有机器的 Nginx 就能恢复，但过一段时间又会出现。

错误日志：

```
2020/06/08 16:31:20 [error] 13741#0: *116374839 connect() failed
(113: No route to host) while connecting to upstream,
client: 2607:xxxx:969:f1f0:c3d:70ec:178f:fd24,
server: localhost,
request: "POST /v1.4/source HTTP/1.1",
upstream: "http://172.31.xx.xx:80/v1.4/source",
host: "api.xxxx.com"
```

### 3.2 排查过程

1. **排除防火墙** — 网上大量资料指向防火墙，但经过仔细排查确认不是
2. **分析监控** — 发现异常时间点和 AWS ELB 的 IP 变化高度吻合
3. **与 AWS SA 沟通** — 确认 AWS ELB 的 IP 是会动态变化的（之前误以为是固定的）

### 3.3 根因分析

**Nginx 在启动时会解析 upstream 中域名对应的 IP，并缓存这个 IP。** 后续请求都会直接转发到缓存的 IP，不会重新解析 DNS。

当 AWS ELB 的 IP 发生变化时：
1. DNS 记录已更新指向新 IP
2. 但 Nginx 仍然使用缓存的旧 IP
3. 旧 IP 已失效，请求转发失败 → `No route to host`

这就解释了为什么重启 Nginx 能临时解决问题 — 重启会重新解析 DNS。

### 3.4 解决方案

使用 Nginx 的 **jdomain 模块**实现 DNS 动态解析：

```nginx
# 安装 jdomain 模块后，在 upstream 中配置
upstream backend {
    jdomain api.example.com interval=10 port=80;
}
```

`jdomain` 模块会按照指定的 `interval`（秒）定期重新解析域名，确保 IP 缓存始终是最新的。

参考文档：[Nginx jdomain 模块](https://www.nginx.com/resources/wiki/modules/domain_resolve/)

**另一种方案**：使用 `resolver` 指令配合变量：

```nginx
server {
    resolver 169.254.169.253 valid=10s;  # AWS 内部 DNS

    location / {
        set $backend "http://api.example.com";
        proxy_pass $backend;
    }
}
```

将域名放在变量中，Nginx 会在每次请求时重新解析。

### 3.5 经验总结

- AWS ELB 的 IP **不是固定的**，会随着扩缩容和健康检查变化
- Nginx 默认只在启动时解析域名，**不会**动态刷新 DNS 缓存
- 任何 upstream 指向域名（而非固定 IP）的场景，都应该考虑 DNS 动态解析
- 这个问题在使用 NLB（Network Load Balancer）时同样存在

## 总结

| 场景 | 方案 | 关键配置 |
|------|------|---------|
| 开发测试 HTTPS | OpenSSL 自签名证书 | `openssl req -new -x509` |
| 部分页面 HTTPS | location 匹配 + 301 跳转 | `return 301 https://` |
| 代理动态 IP 服务 | jdomain 或 resolver 动态解析 | `jdomain` / `resolver` |

这三个场景覆盖了 Nginx HTTPS 配置中最常见的需求和踩坑点。遇到类似问题时，希望这篇文章能帮你少走弯路。