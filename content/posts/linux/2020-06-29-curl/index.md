+++
title = 'curl Command Guide (2026): HTTP Requests, File Transfers, and API Debugging'
date = '2020-06-29'
draft = false
toc = true
description = 'Complete curl tutorial covering GET/POST/PUT/DELETE requests, JSON payloads, file uploads and downloads, authentication, proxy setup, and performance timing.'
tags = ['curl', 'Linux', 'HTTP', 'API', 'CLI']
categories = ['Linux']
keywords = ['curl command guide', 'curl tutorial', 'curl examples', 'curl post request', 'curl get request', 'curl download file', 'curl json', 'curl proxy', 'curl certificate', 'curl linux', 'curl cheat sheet', 'curl command 2026']
+++

If there is one [command-line](/posts/linux/2020-03-19-linux-mac-commands/) tool every developer should master, it is **curl**. Supporting HTTP, HTTPS, FTP, and 20+ other protocols, curl handles everything from quick API tests and POST requests to large file downloads and network diagnostics — all from a single command.

This guide walks through every major curl feature: HTTP methods (GET, POST, PUT, DELETE, PATCH), JSON payloads, file uploads and downloads, Bearer Token authentication, proxy configuration, and request timing. If you also need to trace network paths, pair it with [traceroute](/posts/linux/2020-06-28-traceroute/).

<!--more-->

## Why Learn curl?

| Use Case | Why curl Excels |
|----------|-----------------|
| API debugging | Fire off any HTTP request instantly, no extra tools needed |
| Automation | Drops right into shell scripts and CI/CD pipelines |
| Network diagnostics | Inspect full request/response details with `-v` |
| File transfers | Resume interrupted downloads, throttle bandwidth |
| Cross-platform | Works on Linux, macOS, and Windows out of the box |

> Master curl and you have a Swiss Army knife for anything that speaks HTTP.

## Basic Usage

### Sending a GET Request

The simplest form — just pass a URL:

```bash
# Fetch a web page
curl https://httpbin.org/get

# Save the response to a file
curl -o response.json https://httpbin.org/get

# Save using the remote filename
curl -O https://example.com/file.zip
```

### Viewing Detailed Output

The most useful flags for debugging:

```bash
# -v shows the full request/response exchange
curl -v https://httpbin.org/get

# -i includes response headers in the output
curl -i https://httpbin.org/get

# -I fetches headers only (HEAD request)
curl -I https://httpbin.org/get

# -s enables silent mode (no progress bar)
curl -s https://httpbin.org/get
```

**Reading `-v` output**:
- Lines starting with `>` — what curl sent
- Lines starting with `<` — what the server returned
- Lines starting with `*` — curl's own status messages

### Following Redirects

Many URLs return 301/302 redirects. Use `-L` to follow them automatically:

```bash
# Follow redirects
curl -L https://github.com

# Limit the maximum number of redirects
curl -L --max-redirs 5 https://example.com
```

## HTTP Request Methods

### POST Requests

```bash
# Send form data (application/x-www-form-urlencoded)
curl -X POST -d "name=john&email=john@example.com" https://httpbin.org/post

# Send a JSON payload
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"john","email":"john@example.com"}' \
  https://httpbin.org/post

# Read JSON from a file
curl -X POST \
  -H "Content-Type: application/json" \
  -d @data.json \
  https://httpbin.org/post
```

### PUT Requests

```bash
# Replace a resource
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"id":1,"name":"john","status":"active"}' \
  https://httpbin.org/put
```

### DELETE Requests

```bash
# Delete a resource
curl -X DELETE https://httpbin.org/delete

# Delete with authentication
curl -X DELETE \
  -H "Authorization: Bearer your_token" \
  https://api.example.com/users/123
```

### PATCH Requests

```bash
# Partial update
curl -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"status":"inactive"}' \
  https://httpbin.org/patch
```

## Headers and Authentication

### Custom Headers

```bash
# Add a single header
curl -H "Authorization: Bearer token123" https://api.example.com

# Add multiple headers
curl -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "X-Custom-Header: value" \
     https://api.example.com

# Set the User-Agent string
curl -A "Mozilla/5.0 (Macintosh)" https://example.com

# Set the Referer header
curl -e "https://google.com" https://example.com
```

### Basic Authentication

```bash
# Supply username and password inline
curl -u username:password https://api.example.com

# Prompt for the password interactively (more secure)
curl -u username https://api.example.com
```

### Bearer Token Authentication

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  https://api.example.com/users
```

### Cookie Handling

```bash
# Send a cookie
curl -b "session_id=abc123" https://example.com

# Load cookies from a file
curl -b cookies.txt https://example.com

# Save cookies from the response
curl -c cookies.txt https://example.com

# Load and save cookies (simulate a browser session)
curl -b cookies.txt -c cookies.txt https://example.com
```

## File Uploads and Downloads

### Downloading Files

```bash
# Download and rename
curl -o myfile.zip https://example.com/file.zip

# Keep the remote filename
curl -O https://example.com/file.zip

# Resume a partial download
curl -C - -O https://example.com/largefile.zip

# Limit download speed to 100 KB/s
curl --limit-rate 100k -O https://example.com/file.zip

# Show a progress bar instead of the default meter
curl -# -O https://example.com/file.zip
```

### Uploading Files

```bash
# Upload a single file (multipart/form-data)
curl -F "file=@/path/to/file.jpg" https://httpbin.org/post

# Upload multiple files
curl -F "file1=@file1.jpg" -F "file2=@file2.jpg" https://httpbin.org/post

# Specify the MIME type explicitly
curl -F "file=@photo.jpg;type=image/jpeg" https://httpbin.org/post

# Upload a file alongside other form fields
curl -F "file=@document.pdf" -F "description=My Document" https://httpbin.org/post
```

## HTTPS and Certificates

### Skipping Certificate Verification

```bash
# Ignore SSL certificate errors (testing only!)
curl -k https://self-signed.example.com

# Long form
curl --insecure https://self-signed.example.com
```

### Specifying Certificates

```bash
# Use a custom CA certificate
curl --cacert /path/to/ca.crt https://example.com

# Authenticate with a client certificate
curl --cert /path/to/client.crt --key /path/to/client.key https://example.com
```

### Forcing a TLS Version

```bash
# Require TLS 1.2
curl --tlsv1.2 https://example.com

# Require TLS 1.3
curl --tlsv1.3 https://example.com
```

## Proxy Configuration

### HTTP Proxies

```bash
# Route through an HTTP proxy
curl -x http://proxy.example.com:8080 https://target.com

# Proxy with authentication
curl -x http://user:pass@proxy.example.com:8080 https://target.com

# Set via environment variables (persistent)
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080
curl https://target.com
```

### SOCKS Proxies

```bash
# SOCKS5 proxy
curl --socks5 127.0.0.1:1080 https://example.com

# SOCKS5 with remote DNS resolution
curl --socks5-hostname 127.0.0.1:1080 https://example.com
```

## Timeouts and Retries

```bash
# Connection timeout in seconds
curl --connect-timeout 10 https://example.com

# Total request timeout in seconds
curl -m 30 https://example.com
curl --max-time 30 https://example.com

# Retry up to 3 times on transient failures
curl --retry 3 https://example.com

# Wait 5 seconds between retries
curl --retry 3 --retry-delay 5 https://example.com
```

## Targeting a Specific IP

Invaluable when debugging CDN or load-balancer behavior:

```bash
# HTTP: route via a specific IP using proxy syntax
curl -x 192.168.1.100:80 "http://example.com/api"

# HTTPS: set the Host header manually
curl -H "Host: example.com" "https://192.168.1.100/api" -k

# Best approach: resolve the domain to a chosen IP
curl --resolve example.com:443:192.168.1.100 https://example.com/api

# Discard the body, just watch the handshake
curl -vo /dev/null --resolve example.com:443:192.168.1.100 https://example.com
```

## Practical Tips

### Pretty-Print JSON Output

```bash
# Pipe through jq for formatted JSON
curl -s https://httpbin.org/get | jq .

# Extract a specific field
curl -s https://httpbin.org/get | jq '.headers'
```

### Measure Request Timing

```bash
# Print timing breakdown for each phase
curl -w "\n--- Timing ---\n\
DNS Lookup:    %{time_namelookup}s\n\
TCP Connect:   %{time_connect}s\n\
TLS Handshake: %{time_appconnect}s\n\
First Byte:    %{time_starttransfer}s\n\
Total:         %{time_total}s\n" \
  -o /dev/null -s https://example.com
```

### Mimic a Browser Request

```bash
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     -H "Accept: text/html,application/xhtml+xml" \
     -H "Accept-Language: en-US,en;q=0.9" \
     -e "https://google.com" \
     https://example.com
```

### Request Compressed Responses

```bash
# Automatically decompress gzip/br responses
curl --compressed https://example.com
```

## Quick Reference Table

| Flag | Purpose | Example |
|------|---------|---------|
| `-X` | Set HTTP method | `-X POST` |
| `-d` | Send request body | `-d '{"key":"value"}'` |
| `-H` | Add a header | `-H "Content-Type: application/json"` |
| `-o` | Write output to file | `-o file.txt` |
| `-O` | Save with remote filename | `-O` |
| `-L` | Follow redirects | `-L` |
| `-v` | Verbose output | `-v` |
| `-s` | Silent mode | `-s` |
| `-i` | Include response headers | `-i` |
| `-I` | Headers only (HEAD) | `-I` |
| `-k` | Skip SSL verification | `-k` |
| `-u` | Basic auth credentials | `-u user:pass` |
| `-b` | Send cookies | `-b "name=value"` |
| `-c` | Save cookies to file | `-c cookies.txt` |
| `-F` | Upload file (multipart) | `-F "file=@path"` |
| `-x` | Use a proxy | `-x proxy:port` |
| `-m` | Max request time | `-m 30` |
| `-A` | Set User-Agent | `-A "Mozilla/5.0"` |
| `-e` | Set Referer | `-e "https://ref.com"` |

## curl vs. wget

| Feature | curl | wget |
|---------|------|------|
| Protocol support | 20+ (HTTP, FTP, SMTP, etc.) | HTTP, HTTPS, FTP |
| Default output | stdout | File on disk |
| Recursive download | No | Yes (`-r`) |
| HTTP methods | All (GET/POST/PUT/DELETE/PATCH) | GET and POST only |
| Upload support | Yes | No |
| Pipe-friendly | Excellent (pairs well with jq) | Limited |
| Best for | API testing, scripting, data transfer | Bulk downloads, site mirroring |

**Rule of thumb: use curl to talk to APIs, use wget to mirror websites.**

## Frequently Asked Questions

### Q1: curl returns garbled output. How do I fix it?

The server is probably returning compressed data. Add `--compressed` so curl decompresses it automatically:

```bash
curl --compressed https://example.com
```

### Q2: How do I send a JSON request with curl?

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"test","value":123}' \
  https://httpbin.org/post
```

The key is the `Content-Type: application/json` header combined with `-d` for the JSON body.

### Q3: How do I ignore SSL certificate errors?

Use `-k` or `--insecure` — but only in non-production environments:

```bash
curl -k https://self-signed.example.com
```

### Q4: How do I see the full request and response?

Pass `-v` (verbose) to see everything curl sends and receives:

```bash
curl -v https://example.com
```

### Q5: How do I set a timeout?

Use `--connect-timeout` for the TCP connection phase and `-m` (or `--max-time`) for the entire operation:

```bash
# 5-second connection timeout, 30-second total timeout
curl --connect-timeout 5 -m 30 https://example.com
```

### Q6: curl vs. Postman — when should I use which?

curl is a lightweight CLI tool that fits naturally into scripts and CI/CD pipelines. Postman is a GUI application with a richer visual interface, team collaboration features, and test collection management. They complement each other well — Postman can even export requests as curl commands.

### Q7: How do I measure a website's response time?

Use the `-w` flag to print timing data for each phase of the request:

```bash
curl -w "DNS: %{time_namelookup}s\nTCP: %{time_connect}s\nFirst Byte: %{time_starttransfer}s\nTotal: %{time_total}s\n" -o /dev/null -s https://example.com
```

---

## Summary

curl is one of the most versatile tools in any developer's toolkit. This guide covered the essentials:

1. **HTTP methods** — GET, POST, PUT, DELETE, PATCH
2. **Authentication** — Basic Auth, Bearer Tokens, cookies
3. **File transfers** — uploads, downloads, resume support
4. **HTTPS** — certificate handling, TLS version control
5. **Debugging** — target specific IPs, measure timing, format output

Consider saving your most-used commands as shell aliases or functions. For advanced features, check the [official documentation](https://curl.se/docs/).

## Further Reading

- [Traceroute Explained: Route Tracing and Network Troubleshooting](/posts/linux/2020-06-28-traceroute/) - Locate network latency bottlenecks alongside curl
- [Linux/macOS Command Cheat Sheet](/posts/linux/2020-03-19-linux-mac-commands/) - Essential command reference for developers
- [Linux Ops Basics Hub](/posts/linux/linux-ops-basics-hub/) - System administration knowledge base
- [AWS CLI Complete Guide](/posts/linux/2020-07-04-aws-cli/) - Cloud service management from the terminal
- [Oh My Zsh Setup Guide](/posts/linux/2015-06-17-shell-zsh/) - Build a productive shell environment

## References

- [curl Official Documentation](https://curl.se/docs/)
- [curl Man Page](https://curl.se/docs/manpage.html)
- [Test a REST API with curl - Baeldung](https://www.baeldung.com/curl-rest)
- [httpbin.org](https://httpbin.org/) - HTTP request testing service
