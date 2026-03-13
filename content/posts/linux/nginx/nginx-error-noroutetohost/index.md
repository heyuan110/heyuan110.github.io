+++
date = '2020-07-03T13:19:44+08:00'
draft = true
title = 'Fixing Nginx "No Route to Host" Errors When Proxying to AWS ELB'
description = 'How to fix the Nginx "No route to host" (113) error when reverse proxying to AWS ELB, caused by stale DNS cache after ELB IP changes, using the jdomain module for dynamic DNS resolution'
toc = true
tags = ['Nginx', 'AWS', 'ELB', 'DNS', '故障排查']
categories = ['Linux']
keywords = ['nginx no route to host', 'nginx aws elb proxy error', 'nginx dns cache', 'jdomain module nginx', 'nginx dynamic dns resolution']
+++

After restructuring our backend architecture to route traffic through Nginx as a reverse proxy to an internal hostname that CNAMEs to an AWS ELB (`user -> nginx proxy -> internal host --(CNAME)--> ELB`), we started seeing intermittent outages. The site would go down randomly, and restarting Nginx on every machine in the proxy cluster would bring it back — temporarily.

## The Error

The Nginx error logs showed this on some of the proxy servers:

```
2020/06/08 16:31:20 [error] 13741#0: *116374839 connect() failed (113: No route to host) while connecting to upstream, client: 2607:xxxx:969:f1f0:c3d:70ec:178f:fd24, server: localhost, request: "POST /v1.4/source HTTP/1.1", upstream: "http://172.31.xx.xx:80/v1.4/source", host: "api.xxxx.com"
```

## What Most Articles Get Wrong

Searching online, almost every result pointed to firewall issues. After thorough investigation, we ruled that out completely.

## The Real Cause

By correlating our monitoring data with the timing of the outages, we noticed a clear pattern: every outage coincided with an AWS ELB IP address change. After discussing the issue with our AWS Solutions Architect, we learned that **ELB IP addresses are not static** — they change during scaling events and health checks.

Here is what was happening:

1. Nginx resolves the upstream domain name to an IP address **at startup** and caches it
2. AWS ELB changes its IP address as part of normal operations
3. Nginx keeps sending traffic to the old, now-invalid IP
4. The connection fails with "No route to host"
5. Restarting Nginx forces a fresh DNS lookup, which temporarily fixes the problem

## The Fix: Dynamic DNS Resolution with jdomain

The solution was to install the Nginx **jdomain module**, which periodically re-resolves domain names and updates the cached IP addresses.

Reference: [Nginx jdomain module documentation](https://www.nginx.com/resources/wiki/modules/domain_resolve/)

After deploying Nginx with the jdomain module enabled, the problem never reappeared.

## The Takeaway

When Nginx proxies traffic to a domain name (as opposed to a hardcoded IP), it only resolves DNS once at startup and caches the result indefinitely. If the target IP changes — which is routine for AWS ELB, NLB, and many other cloud services — Nginx will keep sending traffic to a dead IP. Always use dynamic DNS resolution (via `jdomain` or the `resolver` directive with a variable-based `proxy_pass`) when proxying to services with dynamic IPs.