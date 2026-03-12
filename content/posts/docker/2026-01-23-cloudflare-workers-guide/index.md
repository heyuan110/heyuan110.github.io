+++
date = '2026-01-23T20:20:00+08:00'
draft = false
title = 'Cloudflare Workers Complete Guide: Edge Computing from Setup to Production'
description = 'Learn how to build and deploy serverless applications with Cloudflare Workers. Covers core concepts, free tier limits, use cases, development workflow, and hands-on projects including an API proxy and URL shortener.'
toc = true
images = ['cover.webp']
tags = ['Cloudflare', 'Workers', 'Serverless', 'Edge Computing', 'CDN']
categories = ['Docker']
keywords = ['Cloudflare Workers', 'edge computing', 'serverless', 'API proxy', 'Wrangler', 'Workers KV', 'D1 database']
+++

![Cloudflare Workers serverless platform official cover](cover.webp)

**Cloudflare Workers** is an edge computing platform that lets you run code across 300+ data centers worldwide without managing any servers. Compared to traditional cloud hosting, Workers deploys faster, cold-starts in under 5 milliseconds, delivers consistently low latency globally, and comes with a **remarkably generous free tier**.

This guide takes you from zero to production-ready: what Workers is, where it shines, how to develop and deploy, and several real-world projects you can use right away. Whether you are new to serverless or looking to optimize an existing architecture, you will find actionable takeaways here.

---

## What Is Cloudflare Workers

### The Core Idea

Cloudflare Workers is a **serverless** computing platform. You write code; Cloudflare handles running, scaling, and maintaining it.

Traditional deployment:
```
User request → A server in one data center → Process → Respond
```

Workers deployment:
```
User request → Nearest edge node (300+ worldwide) → Process → Respond
```

**Key advantage**: your code runs on the node closest to the user, minimizing latency.

### Technical Architecture

Workers runs on **V8 isolates** (the JavaScript engine behind Chrome) rather than traditional containers or virtual machines.

| Aspect | Traditional Serverless (e.g., AWS Lambda) | Cloudflare Workers |
|--------|------------------------------------------|-------------------|
| Startup mechanism | Spin up container/VM | Spin up V8 isolate |
| Cold start | 100 ms to several seconds | **< 5 ms** |
| Deployment scope | Regional (e.g., us-east-1) | **300+ global nodes** |
| Isolation | Container-level | V8 sandbox |
| Languages | Many | JavaScript/TypeScript/WASM |

### Workers vs. Vercel vs. Netlify

| Platform | Strengths | Weaknesses | Best For |
|----------|-----------|------------|----------|
| **Cloudflare Workers** | Fastest cold start, lowest global latency, large free tier | 128 MB memory cap, no full Node.js API | APIs, edge processing, lightweight services |
| **Vercel** | Deep Next.js integration, great DX | Limited free tier, slower cold starts | Next.js projects, frontend-heavy apps |
| **Netlify** | Strong Jamstack ecosystem, simple deploys | Performance trails Workers | Static sites, simple functions |

**How to choose**:
- Building with Next.js? Go with Vercel.
- Need ultra-low latency at the edge? Pick **Cloudflare Workers**.
- Static site with light backend logic? Netlify or Cloudflare Pages.

---

## Free Tier and Pricing Breakdown

This is the part most people care about. The free tier is generous enough that personal projects rarely cost anything.

### Free Plan

| Resource | Free Allowance | Notes |
|----------|---------------|-------|
| **Requests** | 100,000 / day | ~3 million / month |
| **CPU time** | 10 ms per request | Sufficient for most workloads |
| **Workers KV** | 100K reads/day, 1K writes/day, 1 GB storage | Plenty for light caching |
| **D1 Database** | 5M row reads/day, 100K row writes/day, 5 GB storage | Enough for small apps |
| **Static assets** | **Unlimited** | Images, CSS, JS are free |
| **Sub-requests** | Not billed | Outbound fetches from your Worker are free |

**Bottom line**: 100K requests per day covers personal blogs, small tools, and API proxies with room to spare.

### Paid Plan

| Resource | Paid ($5/month base) |
|----------|---------------------|
| Requests | 10 million / month, then $0.30 per additional million |
| CPU time | Up to **5 minutes** per request |
| Workers KV | 10M reads/month, 1M writes/month |
| D1 Database | 2.5B row reads/month, 50M row writes/month |

**When you need to pay**:
- Daily requests exceed 100K
- A single request needs more than 10 ms of CPU time
- You need higher database throughput

### Cost Examples

For an API proxy service:

| Scenario | Daily Requests | Monthly Cost |
|----------|---------------|-------------|
| Personal use | 1,000 | **$0** (free) |
| Small project | 50,000 | **$0** (free) |
| Medium project | 500,000 | **$5** (base paid) |
| Large project | 5,000,000 | **~$6.50** |

**Takeaway**: unless you are handling serious traffic, the free plan is more than enough.

---

## Ideal Use Cases for Workers

### Where Workers Excels

| Use Case | Description | Example |
|----------|------------|---------|
| **API proxy / gateway** | Forward requests, add CORS headers, handle cross-origin | OpenAI API proxy |
| **URL shortener** | Lightweight short-link service | Self-hosted bit.ly alternative |
| **Edge processing** | Image resizing, A/B testing, geo-routing | Serve different content by location |
| **Lightweight REST APIs** | Simple CRUD backends | Personal blog API |
| **Webhook handler** | Receive and process third-party notifications | GitHub / Stripe webhooks |
| **Static asset acceleration** | CDN with custom logic | Image transforms, cache control |
| **Auth gateway** | JWT validation, OAuth relay | Centralized authentication |

### Where Workers Is Not the Best Fit

| Scenario | Reason | Alternative |
|----------|--------|-------------|
| Long-running compute (> 30 s) | CPU time limits | Queues + Durable Objects |
| Memory-heavy apps (> 128 MB) | Memory cap | Traditional cloud VMs |
| Full Node.js runtime needed | Incomplete Node API support | Vercel Functions |
| Database-intensive workloads | KV/D1 read/write caps | External managed database |
| Persistent WebSocket connections | Requires Durable Objects | Paid feature |

### Quick Rule of Thumb

**Good fit**: short-lived requests, stateless or light state, global low-latency requirement.

**Not ideal**: heavy computation, large memory footprint, complex database operations.

---

## Setting Up Your Development Environment

### Prerequisites

- A free [Cloudflare account](https://dash.cloudflare.com/sign-up)
- [Node.js](https://nodejs.org/) 16.17.0 or later

### Install the Wrangler CLI

Wrangler is the official CLI for developing, testing, and deploying Workers.

```bash
# Global install
npm install -g wrangler

# Or use npx (recommended — no global install needed)
npx wrangler --version
```

### Authenticate with Cloudflare

```bash
npx wrangler login
```

This opens your browser so you can sign in and authorize the CLI.

### Create Your First Project

```bash
# Scaffold a new project
npm create cloudflare@latest -- my-first-worker

# Follow the prompts:
# - Select "Hello World" example
# - Choose "Worker only"
# - Pick JavaScript or TypeScript
# - Enable git: Yes
# - Deploy now: No (test locally first)
```

### Project Structure

```
my-first-worker/
├── src/
│   └── index.js      # Worker source code
├── wrangler.toml     # Configuration (or wrangler.jsonc)
├── package.json
└── node_modules/
```

### Key Configuration: wrangler.toml

```toml
name = "my-first-worker"           # Worker name and URL path
main = "src/index.js"              # Entry file
compatibility_date = "2024-01-01"  # Compatibility date

# Optional: bind KV storage
# [[kv_namespaces]]
# binding = "MY_KV"
# id = "xxxxxxxx"

# Optional: bind D1 database
# [[d1_databases]]
# binding = "DB"
# database_name = "my-db"
# database_id = "xxxxxxxx"

# Optional: environment variables
# [vars]
# API_KEY = "your-api-key"
```

---

## Hello World: A Complete Walkthrough

### The Default Code

`src/index.js`:

```javascript
export default {
  async fetch(request, env, ctx) {
    return new Response("Hello World!");
  },
};
```

**What each parameter does**:
- `fetch` — the entry point for handling HTTP requests
- `request` — the incoming request (URL, method, headers, body)
- `env` — environment variables and bound resources (KV, D1, etc.)
- `ctx` — execution context (e.g., `ctx.waitUntil()`)
- Returns a `Response` object

### Local Development

```bash
cd my-first-worker
npx wrangler dev
```

Output:
```
⎔ Starting local server...
[wrangler] Ready on http://localhost:8787
```

Open `http://localhost:8787` in your browser. If you see "Hello World!", you are all set.

**Dev mode features**:
- Hot reload on file save
- `console.log` debugging support
- Local simulation of the Cloudflare runtime

### Deploy to Production

```bash
npx wrangler deploy
```

Output:
```
Uploaded my-first-worker (1.23 sec)
Published my-first-worker (0.45 sec)
  https://my-first-worker.your-subdomain.workers.dev
```

Visit the URL and your Worker is live.

---

## Core API Reference

### The Request Object

```javascript
export default {
  async fetch(request, env, ctx) {
    // Parse the request
    const url = new URL(request.url);
    const method = request.method;           // GET, POST, etc.
    const path = url.pathname;               // /api/users
    const params = url.searchParams;         // ?id=123
    const headers = request.headers;

    // Read POST body
    if (method === 'POST') {
      const body = await request.json();     // JSON
      // or await request.text()             // Plain text
      // or await request.formData()         // Form data
    }

    // Client metadata (Cloudflare-specific)
    const ip = request.headers.get('CF-Connecting-IP');
    const country = request.cf?.country;     // Country code
    const city = request.cf?.city;

    return new Response('OK');
  },
};
```

### The Response Object

```javascript
// Plain text
return new Response('Hello');

// JSON
return new Response(JSON.stringify({ message: 'OK' }), {
  headers: { 'Content-Type': 'application/json' },
});

// Custom status code
return new Response('Not Found', { status: 404 });

// Redirect
return Response.redirect('https://example.com', 302);

// Response with CORS headers
return new Response(data, {
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  },
});
```

### Making Sub-requests (fetch)

```javascript
export default {
  async fetch(request, env, ctx) {
    // Proxy a request to another service
    const response = await fetch('https://api.example.com/data', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + env.API_KEY,
      },
    });

    return response;
  },
};
```

### Workers KV (Key-Value Storage)

Create a KV namespace:

```bash
npx wrangler kv:namespace create "MY_CACHE"
```

Bind it in `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "MY_CACHE"
id = "your-namespace-id"
```

Use it in code:

```javascript
export default {
  async fetch(request, env, ctx) {
    // Write
    await env.MY_CACHE.put('key', 'value');

    // Read
    const value = await env.MY_CACHE.get('key');

    // Delete
    await env.MY_CACHE.delete('key');

    // Write with TTL (in seconds)
    await env.MY_CACHE.put('session', 'data', { expirationTtl: 3600 });

    return new Response(value);
  },
};
```

### D1 Database (SQLite at the Edge)

Create a database:

```bash
npx wrangler d1 create my-database
```

Bind it in `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"
```

Define your schema (`schema.sql`):

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

Run the migration:

```bash
npx wrangler d1 execute my-database --file=./schema.sql
```

Use it in code:

```javascript
export default {
  async fetch(request, env, ctx) {
    // Query all users
    const { results } = await env.DB.prepare(
      'SELECT * FROM users'
    ).all();

    // Parameterized query (prevents SQL injection)
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(1).first();

    // Insert a row
    await env.DB.prepare(
      'INSERT INTO users (name, email) VALUES (?, ?)'
    ).bind('Jane Doe', 'jane@example.com').run();

    return Response.json(results);
  },
};
```

---

## Hands-On Project: API Proxy

One of the most popular Workers use cases is proxying external APIs — adding CORS support, rate limiting, or routing traffic through Cloudflare's network.

### Full Source Code

```javascript
// src/index.js

// Target API host
const TARGET_HOST = 'api.openai.com';

// Allowed path prefixes (security measure)
const ALLOWED_PATHS = ['/v1/chat', '/v1/models', '/v1/embeddings'];

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // Only proxy allowed paths
    const isAllowed = ALLOWED_PATHS.some(p => path.startsWith(p));
    if (!isAllowed) {
      return new Response(JSON.stringify({ error: 'Path not allowed' }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Build the proxied request
    const targetUrl = `https://${TARGET_HOST}${path}${url.search}`;

    // Clone headers and strip Cloudflare-specific ones
    const headers = new Headers(request.headers);
    headers.delete('host');
    headers.delete('cf-connecting-ip');
    headers.delete('cf-ipcountry');

    // Forward the request
    const response = await fetch(targetUrl, {
      method: request.method,
      headers: headers,
      body: request.body,
    });

    // Add CORS headers to the response
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Access-Control-Allow-Origin', '*');

    return newResponse;
  },
};
```

### How to Use It

After deploying, replace the original API endpoint:
```
https://api.openai.com/v1/chat/completions
```

With your Worker URL:
```
https://your-worker.your-subdomain.workers.dev/v1/chat/completions
```

---

## Hands-On Project: URL Shortener

Build a simple URL shortener with Workers and KV.

### Full Source Code

```javascript
// src/index.js

// Generate a random short code
function generateCode(length = 6) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Validate URL format
function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    // Create a short link: POST /create
    if (path === '/create' && request.method === 'POST') {
      try {
        const { url: targetUrl } = await request.json();

        if (!targetUrl || !isValidUrl(targetUrl)) {
          return Response.json({ error: 'Invalid URL' }, { status: 400 });
        }

        // Generate a unique code
        let code = generateCode();
        let existing = await env.LINKS.get(code);
        while (existing) {
          code = generateCode();
          existing = await env.LINKS.get(code);
        }

        // Store the mapping (expires in 90 days)
        await env.LINKS.put(code, targetUrl, { expirationTtl: 90 * 24 * 60 * 60 });

        const shortUrl = `${url.origin}/${code}`;
        return Response.json({
          shortUrl,
          code,
          originalUrl: targetUrl
        }, {
          headers: { 'Access-Control-Allow-Origin': '*' },
        });
      } catch (e) {
        return Response.json({ error: 'Invalid request' }, { status: 400 });
      }
    }

    // Redirect: GET /:code
    if (path.length > 1 && request.method === 'GET') {
      const code = path.slice(1);
      const targetUrl = await env.LINKS.get(code);

      if (targetUrl) {
        return Response.redirect(targetUrl, 302);
      } else {
        return new Response('Short link not found', { status: 404 });
      }
    }

    // Landing page
    return new Response(`
      <h1>URL Shortener</h1>
      <p>POST /create with {"url": "https://example.com"}</p>
    `, {
      headers: { 'Content-Type': 'text/html' },
    });
  },
};
```

### wrangler.toml Configuration

```toml
name = "url-shortener"
main = "src/index.js"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "LINKS"
id = "your-kv-namespace-id"
```

### Usage

Create a short link:
```bash
curl -X POST https://your-worker.workers.dev/create \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very-long-path"}'
```

Response:
```json
{
  "shortUrl": "https://your-worker.workers.dev/abc123",
  "code": "abc123",
  "originalUrl": "https://www.example.com/very-long-path"
}
```

---

## Building with the Hono Framework

For more complex projects, [Hono](https://hono.dev/) is a lightweight framework purpose-built for edge runtimes. Its API feels familiar if you have used Express.

### Create a Hono Project

```bash
npm create hono@latest my-api
# Select the cloudflare-workers template
cd my-api
npm install
```

### Basic Routing

```javascript
// src/index.js
import { Hono } from 'hono';
import { cors } from 'hono/cors';

const app = new Hono();

// Global middleware
app.use('*', cors());

// Routes
app.get('/', (c) => c.text('Hello Hono!'));

app.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id, name: 'User ' + id });
});

app.post('/users', async (c) => {
  const body = await c.req.json();
  return c.json({ created: true, data: body });
});

// 404 handler
app.notFound((c) => c.json({ error: 'Not Found' }, 404));

// Error handler
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: 'Internal Server Error' }, 500);
});

export default app;
```

### Integrating D1

```javascript
import { Hono } from 'hono';

// Type bindings
type Bindings = {
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/users', async (c) => {
  const { results } = await c.env.DB.prepare(
    'SELECT * FROM users LIMIT 100'
  ).all();
  return c.json(results);
});

app.get('/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await c.env.DB.prepare(
    'SELECT * FROM users WHERE id = ?'
  ).bind(id).first();

  if (!user) {
    return c.json({ error: 'User not found' }, 404);
  }
  return c.json(user);
});

export default app;
```

---

## Deployment and Operations

### Deploy Commands

```bash
# Deploy to production
npx wrangler deploy

# Deploy to a preview environment
npx wrangler deploy --env preview

# Stream live logs
npx wrangler tail
```

### Managing Secrets

Never hardcode sensitive values. Use Wrangler secrets instead:

```bash
# Add a secret
npx wrangler secret put API_KEY
# Enter the value when prompted

# Access it in code
const apiKey = env.API_KEY;
```

### Custom Domains

1. Add your domain to Cloudflare Dashboard.
2. Go to Workers and select your Worker.
3. Click **Triggers** then **Custom Domains**.
4. Add `api.yourdomain.com`.

### Monitoring and Logging

```bash
# Stream logs in real time
npx wrangler tail

# Filter by error status
npx wrangler tail --format pretty --status error
```

The Cloudflare Dashboard also shows:
- Request volume
- Error rates
- CPU usage
- Geographic distribution

### CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Workers

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Deploy
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
```

Add `CF_API_TOKEN` in your repository's Settings under Secrets (get it from Cloudflare Dashboard).

---

## Frequently Asked Questions

**Q: How fast is Workers' cold start?**

Workers typically cold-starts in under 5 ms thanks to V8 isolates. Compare that with AWS Lambda, which can take 100 ms to several seconds.

**Q: Does Workers support WebSocket?**

Basic Workers can pass through (proxy) WebSocket connections. If you need to maintain WebSocket state inside the Worker, you will need Durable Objects (a paid feature).

**Q: How do I handle large file uploads?**

The request body limit is 100 MB on the paid plan. For larger files, use R2 Storage with presigned upload URLs.

**Q: What is the difference between Workers and Pages Functions?**

Pages Functions are part of Cloudflare Pages and designed to add backend logic to static sites. Under the hood they run on Workers, but the deployment model and typical use cases differ.

---

## Best Practices

### Performance

- Use `ctx.waitUntil()` for non-critical async work (analytics, logging).
- Cache aggressively with KV to reduce outbound fetches.
- Keep the hot path simple — avoid expensive computation in the request chain.

### Security

- Store secrets with `wrangler secret`, never in source code.
- Implement rate limiting to prevent abuse.
- Validate all user input.
- Restrict CORS to specific origins in production.

### Code Organization

- Use a framework like Hono for anything beyond a simple handler.
- Split logic into modules by feature.
- Standardize error handling and response formats.

### Cost Management

- Design around the free tier — it covers more than you think.
- Monitor usage and set up alerts before you hit paid thresholds.
- Host static assets on R2 or Pages instead of serving them from Workers.

---

## Summary

Cloudflare Workers is a powerful and cost-effective edge computing platform. Its main advantages:

1. **Ultra-low latency** — code runs on 300+ nodes closest to the user.
2. **Near-instant cold starts** — V8 isolates boot in under 5 ms.
3. **Generous free tier** — 100K requests/day is enough for most personal and small projects.
4. **Dead-simple deployment** — go from code to production in minutes.

**Best for**: API proxies, URL shorteners, edge processing, lightweight APIs, and webhook handlers.

**Next steps**:
1. Sign up for a free Cloudflare account and deploy your first Worker.
2. Try the API proxy or URL shortener projects from this guide.
3. Explore Workers KV and D1 for data persistence.
4. Look into Durable Objects for stateful applications.

**References**:
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- [Hono Framework Docs](https://hono.dev/docs/getting-started/cloudflare-workers)
- [Cloudflare D1 Database Guide](https://developers.cloudflare.com/d1/)
