+++
date = '2026-01-23T20:20:00+08:00'
draft = false
title = 'Cloudflare Workers 完全指南：从入门到实战的边缘计算部署手册'
description = 'Cloudflare Workers 是部署无服务器应用的最佳选择之一。本文详解 Workers 的核心概念、免费额度、适用场景、开发部署流程，并提供 API 代理、短链接服务等实战案例，助你快速掌握边缘计算开发。'
toc = true
images = ['cover.webp']
tags = ['Cloudflare', 'Workers', 'Serverless', 'Edge Computing', 'CDN']
categories = ['Docker']
keywords = ['Cloudflare Workers', '边缘计算', 'Serverless', '无服务器', 'API代理', 'Wrangler']
+++

![Cloudflare Workers 快速无服务器平台官方封面图](cover.webp)

**Cloudflare Workers** 是 Cloudflare 推出的边缘计算平台，它让你无需管理服务器，就能在全球 300+ 个数据中心运行代码。相比传统云服务器，Workers 的部署速度更快、冷启动更低、全球延迟更均匀，而且**免费额度非常慷慨**。

本文将从零开始，带你全面了解 Cloudflare Workers：它是什么、适合什么场景、如何开发部署，以及多个可直接使用的实战案例。无论你是刚接触云计算的新手，还是想优化现有架构的老手，都能从中获得实用价值。

---

## 一、什么是 Cloudflare Workers

### 1. 基本概念

Cloudflare Workers 是一种 **Serverless（无服务器）** 计算平台。你只需要写代码，Cloudflare 负责运行、扩展和维护。

传统部署方式：
```
用户请求 → 某个机房的服务器 → 处理 → 返回
```

Workers 部署方式：
```
用户请求 → 最近的边缘节点（全球 300+） → 处理 → 返回
```

**核心优势**：代码运行在离用户最近的节点上，延迟极低。

### 2. 技术架构

Workers 基于 **V8 isolates** 技术（Chrome 浏览器的 JavaScript 引擎），而不是传统的容器或虚拟机。

| 对比项 | 传统 Serverless（如 AWS Lambda） | Cloudflare Workers |
|--------|----------------------------------|-------------------|
| 启动方式 | 启动容器/VM | 启动 V8 isolate |
| 冷启动时间 | 100ms - 数秒 | **< 5ms** |
| 部署位置 | 区域性（如 us-east-1） | **全球 300+ 节点** |
| 资源隔离 | 容器级别 | V8 沙箱 |
| 支持语言 | 多种 | JavaScript/TypeScript/WASM |

### 3. 与 Vercel、Netlify 的对比

| 平台 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| **Cloudflare Workers** | 冷启动最快、全球延迟最低、免费额度大 | 内存限制 128MB、不支持完整 Node.js | API、边缘处理、轻量服务 |
| **Vercel** | Next.js 深度集成、开发体验好 | 免费额度有限、冷启动较慢 | Next.js 项目、前端为主 |
| **Netlify** | Jamstack 生态完善、部署简单 | 性能不如 Workers | 静态站点、简单函数 |

**选择建议**：
- 如果你用 Next.js → 选 Vercel
- 如果你需要极致性能和全球低延迟 → 选 **Cloudflare Workers**
- 如果你做静态站点 + 简单后端 → 选 Netlify 或 Cloudflare Pages

---

## 二、免费额度与定价详解

这是大家最关心的部分。Cloudflare Workers 的免费额度非常慷慨，个人项目基本不用花钱。

### 1. 免费计划

| 资源 | 免费额度 | 说明 |
|------|----------|------|
| **请求数** | 每天 100,000 次 | 约每月 300 万次 |
| **CPU 时间** | 每次请求 10ms | 足够大多数场景 |
| **Workers KV（键值存储）** | 读取 10 万/天、写入 1000/天、存储 1GB | 轻量缓存足够 |
| **D1 数据库** | 读取 500 万行/天、写入 10 万行/天、存储 5GB | 小型应用足够 |
| **静态资源** | **无限制** | 图片、CSS、JS 等不计费 |
| **子请求** | 不计费 | 从 Worker 发起的请求免费 |

**重点**：每天 10 万次请求 = 每月约 300 万次，对于个人博客、小工具、API 代理等场景绑绑有余。

### 2. 付费计划

| 资源 | 付费版（$5/月起） |
|------|------------------|
| 请求数 | 每月 1000 万次，超出 $0.30/百万 |
| CPU 时间 | 每次请求最高 **5 分钟** |
| Workers KV | 读取 1000 万/月，写入 100 万/月 |
| D1 数据库 | 读取 25 亿行/月，写入 5000 万行/月 |

**什么时候需要付费**：
- 日请求量超过 10 万
- 单次请求需要超过 10ms CPU 时间
- 需要更多数据库读写

### 3. 费用计算示例

假设你做一个 API 代理服务：

| 场景 | 日均请求 | 月费用 |
|------|----------|--------|
| 个人使用 | 1,000 | **$0**（免费） |
| 小型项目 | 50,000 | **$0**（免费） |
| 中型项目 | 500,000 | **$5**（基础付费） |
| 大型项目 | 5,000,000 | **$5 + $1.50** |

**结论**：除非你的服务有大量流量，否则免费计划足够用。

---

## 三、Workers 适用场景

### 1. 最适合的场景

| 场景 | 说明 | 示例 |
|------|------|------|
| **API 代理/网关** | 转发请求、添加 CORS 头、处理跨域 | OpenAI API 代理 |
| **URL 短链接** | 轻量级的短链服务 | 自建 bit.ly |
| **边缘计算处理** | 图片裁剪、A/B 测试、地理位置路由 | 根据用户位置返回不同内容 |
| **API 服务** | 轻量级 REST API | 个人博客后端 |
| **Webhook 处理** | 接收并处理第三方通知 | GitHub/Stripe Webhook |
| **静态资源加速** | CDN + 简单处理逻辑 | 图片处理、缓存控制 |
| **认证鉴权** | JWT 验证、OAuth 中转 | 统一认证网关 |

### 2. 不太适合的场景

| 场景 | 原因 | 替代方案 |
|------|------|----------|
| 长时间计算（> 30s） | CPU 时间限制 | 使用 Queues + Durable Objects |
| 大内存应用（> 128MB） | 内存限制 | 使用传统云服务器 |
| 需要完整 Node.js 环境 | 不支持所有 Node API | Vercel Functions |
| 数据库密集型应用 | KV/D1 有读写限制 | 使用外部数据库 |
| WebSocket 长连接 | 需要 Durable Objects | 付费功能 |

### 3. 一句话判断

**适合 Workers**：请求处理时间短、无状态或轻状态、需要全球低延迟

**不适合 Workers**：重计算、大内存、复杂数据库操作

---

## 四、开发环境搭建

### 1. 前置条件

- 注册 [Cloudflare 账号](https://dash.cloudflare.com/sign-up)（免费）
- 安装 [Node.js](https://nodejs.org/) 16.17.0 或更高版本

### 2. 安装 Wrangler CLI

Wrangler 是 Cloudflare 官方的命令行工具，用于开发、测试和部署 Workers。

```bash
# 全局安装
npm install -g wrangler

# 或使用 npx（推荐，无需全局安装）
npx wrangler --version
```

### 3. 登录 Cloudflare

```bash
npx wrangler login
```

执行后会自动打开浏览器，登录你的 Cloudflare 账号并授权。

### 4. 创建第一个项目

```bash
# 使用官方脚手架创建项目
npm create cloudflare@latest -- my-first-worker

# 按提示选择：
# - 选择 "Hello World" example
# - 选择 "Worker only"
# - 选择 JavaScript 或 TypeScript
# - 是否启用 git：Yes
# - 是否立即部署：No（先本地测试）
```

### 5. 项目结构

```
my-first-worker/
├── src/
│   └── index.js      # Worker 代码
├── wrangler.toml     # 配置文件（或 wrangler.jsonc）
├── package.json
└── node_modules/
```

### 6. 核心配置文件 wrangler.toml

```toml
name = "my-first-worker"        # Worker 名称，也是访问路径
main = "src/index.js"           # 入口文件
compatibility_date = "2024-01-01"  # 兼容日期

# 可选：绑定 KV 存储
# [[kv_namespaces]]
# binding = "MY_KV"
# id = "xxxxxxxx"

# 可选：绑定 D1 数据库
# [[d1_databases]]
# binding = "DB"
# database_name = "my-db"
# database_id = "xxxxxxxx"

# 可选：环境变量
# [vars]
# API_KEY = "your-api-key"
```

---

## 五、Hello World 完整示例

### 1. 默认代码解析

`src/index.js`：

```javascript
export default {
  async fetch(request, env, ctx) {
    return new Response("Hello World!");
  },
};
```

**代码解读**：
- `fetch` 是处理 HTTP 请求的入口函数
- `request`：请求对象，包含 URL、方法、头部等
- `env`：环境变量和绑定的资源（如 KV、D1）
- `ctx`：执行上下文
- 返回 `Response` 对象

### 2. 本地开发测试

```bash
cd my-first-worker
npx wrangler dev
```

输出：
```
⎔ Starting local server...
[wrangler] Ready on http://localhost:8787
```

打开浏览器访问 `http://localhost:8787`，看到 "Hello World!" 就成功了。

**开发模式特性**：
- 保存代码自动重载
- 支持 console.log 调试
- 本地模拟 Cloudflare 环境

### 3. 部署到生产环境

```bash
npx wrangler deploy
```

输出：
```
Uploaded my-first-worker (1.23 sec)
Published my-first-worker (0.45 sec)
  https://my-first-worker.your-subdomain.workers.dev
```

访问返回的 URL，你的 Worker 就上线了！

---

## 六、核心 API 详解

### 1. Request 对象

```javascript
export default {
  async fetch(request, env, ctx) {
    // 获取请求信息
    const url = new URL(request.url);
    const method = request.method;           // GET, POST, etc.
    const path = url.pathname;               // /api/users
    const params = url.searchParams;         // ?id=123
    const headers = request.headers;         // 请求头

    // 获取 POST 请求体
    if (method === 'POST') {
      const body = await request.json();     // JSON 格式
      // 或 await request.text()             // 文本格式
      // 或 await request.formData()         // 表单格式
    }

    // 获取客户端信息
    const ip = request.headers.get('CF-Connecting-IP');
    const country = request.cf?.country;     // 国家代码
    const city = request.cf?.city;           // 城市

    return new Response('OK');
  },
};
```

### 2. Response 对象

```javascript
// 简单文本响应
return new Response('Hello');

// JSON 响应
return new Response(JSON.stringify({ message: 'OK' }), {
  headers: { 'Content-Type': 'application/json' },
});

// 自定义状态码
return new Response('Not Found', { status: 404 });

// 重定向
return Response.redirect('https://example.com', 302);

// 带 CORS 头的响应
return new Response(data, {
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  },
});
```

### 3. 发起子请求（fetch）

```javascript
export default {
  async fetch(request, env, ctx) {
    // 代理请求到其他服务
    const response = await fetch('https://api.example.com/data', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + env.API_KEY,
      },
    });

    // 返回代理结果
    return response;
  },
};
```

### 4. 使用 Workers KV（键值存储）

首先创建 KV 命名空间：

```bash
npx wrangler kv:namespace create "MY_CACHE"
```

在 `wrangler.toml` 中绑定：

```toml
[[kv_namespaces]]
binding = "MY_CACHE"
id = "输出的 ID"
```

代码中使用：

```javascript
export default {
  async fetch(request, env, ctx) {
    // 写入
    await env.MY_CACHE.put('key', 'value');

    // 读取
    const value = await env.MY_CACHE.get('key');

    // 删除
    await env.MY_CACHE.delete('key');

    // 写入带过期时间（秒）
    await env.MY_CACHE.put('session', 'data', { expirationTtl: 3600 });

    return new Response(value);
  },
};
```

### 5. 使用 D1 数据库

创建数据库：

```bash
npx wrangler d1 create my-database
```

在 `wrangler.toml` 中绑定：

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "输出的 ID"
```

初始化表结构（创建 `schema.sql`）：

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

执行迁移：

```bash
npx wrangler d1 execute my-database --file=./schema.sql
```

代码中使用：

```javascript
export default {
  async fetch(request, env, ctx) {
    // 查询所有用户
    const { results } = await env.DB.prepare(
      'SELECT * FROM users'
    ).all();

    // 带参数查询（防 SQL 注入）
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(1).first();

    // 插入数据
    await env.DB.prepare(
      'INSERT INTO users (name, email) VALUES (?, ?)'
    ).bind('张三', 'zhangsan@example.com').run();

    return Response.json(results);
  },
};
```

---

## 七、实战案例：API 代理服务

这是最常用的场景之一：将国外 API（如 OpenAI）代理到 Workers，解决网络访问问题。

### 完整代码

```javascript
// src/index.js

// 配置目标 API
const TARGET_HOST = 'api.openai.com';

// 允许代理的路径前缀（安全考虑）
const ALLOWED_PATHS = ['/v1/chat', '/v1/models', '/v1/embeddings'];

export default {
  async fetch(request, env, ctx) {
    // 处理 CORS 预检请求
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

    // 安全检查：只代理允许的路径
    const isAllowed = ALLOWED_PATHS.some(p => path.startsWith(p));
    if (!isAllowed) {
      return new Response(JSON.stringify({ error: 'Path not allowed' }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // 构建代理请求
    const targetUrl = `https://${TARGET_HOST}${path}${url.search}`;

    // 复制原始请求头，移除不需要的
    const headers = new Headers(request.headers);
    headers.delete('host');
    headers.delete('cf-connecting-ip');
    headers.delete('cf-ipcountry');

    // 发起代理请求
    const response = await fetch(targetUrl, {
      method: request.method,
      headers: headers,
      body: request.body,
    });

    // 复制响应，添加 CORS 头
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Access-Control-Allow-Origin', '*');

    return newResponse;
  },
};
```

### 使用方式

部署后，将原本的 API 地址：
```
https://api.openai.com/v1/chat/completions
```

替换为：
```
https://your-worker.your-subdomain.workers.dev/v1/chat/completions
```

---

## 八、实战案例：URL 短链接服务

使用 Workers + KV 实现一个简单的短链接服务。

### 完整代码

```javascript
// src/index.js

// 生成短码
function generateCode(length = 6) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// 验证 URL 格式
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

    // CORS 处理
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    // 创建短链接 POST /create
    if (path === '/create' && request.method === 'POST') {
      try {
        const { url: targetUrl } = await request.json();

        if (!targetUrl || !isValidUrl(targetUrl)) {
          return Response.json({ error: 'Invalid URL' }, { status: 400 });
        }

        // 生成唯一短码
        let code = generateCode();
        let existing = await env.LINKS.get(code);
        while (existing) {
          code = generateCode();
          existing = await env.LINKS.get(code);
        }

        // 存储映射关系（90 天过期）
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

    // 短链接跳转 GET /:code
    if (path.length > 1 && request.method === 'GET') {
      const code = path.slice(1); // 移除开头的 /
      const targetUrl = await env.LINKS.get(code);

      if (targetUrl) {
        return Response.redirect(targetUrl, 302);
      } else {
        return new Response('Short link not found', { status: 404 });
      }
    }

    // 首页
    return new Response(`
      <h1>URL Shortener</h1>
      <p>POST /create with {"url": "https://example.com"}</p>
    `, {
      headers: { 'Content-Type': 'text/html' },
    });
  },
};
```

### wrangler.toml 配置

```toml
name = "url-shortener"
main = "src/index.js"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "LINKS"
id = "你的 KV namespace ID"
```

### 使用方式

创建短链接：
```bash
curl -X POST https://your-worker.workers.dev/create \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very-long-path"}'
```

响应：
```json
{
  "shortUrl": "https://your-worker.workers.dev/abc123",
  "code": "abc123",
  "originalUrl": "https://www.example.com/very-long-path"
}
```

---

## 九、使用 Hono 框架开发

对于复杂项目，推荐使用 [Hono](https://hono.dev/) 框架。它是专为边缘计算设计的轻量级框架，API 类似 Express。

### 1. 创建 Hono 项目

```bash
npm create hono@latest my-api
# 选择 cloudflare-workers 模板
cd my-api
npm install
```

### 2. 基本路由

```javascript
// src/index.js
import { Hono } from 'hono';
import { cors } from 'hono/cors';

const app = new Hono();

// 全局中间件
app.use('*', cors());

// 路由定义
app.get('/', (c) => c.text('Hello Hono!'));

app.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id, name: 'User ' + id });
});

app.post('/users', async (c) => {
  const body = await c.req.json();
  return c.json({ created: true, data: body });
});

// 404 处理
app.notFound((c) => c.json({ error: 'Not Found' }, 404));

// 错误处理
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: 'Internal Server Error' }, 500);
});

export default app;
```

### 3. 集成 D1 数据库

```javascript
import { Hono } from 'hono';

// 定义环境类型
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

## 十、部署与运维

### 1. 部署命令

```bash
# 部署到生产环境
npx wrangler deploy

# 部署到预览环境
npx wrangler deploy --env preview

# 查看部署日志
npx wrangler tail
```

### 2. 环境变量管理

敏感信息不要写在代码里，使用 Secret：

```bash
# 添加 Secret
npx wrangler secret put API_KEY
# 然后输入密钥值

# 在代码中使用
const apiKey = env.API_KEY;
```

### 3. 自定义域名

1. 在 Cloudflare Dashboard 添加你的域名
2. 进入 Workers 页面，选择你的 Worker
3. 点击 "Triggers" → "Custom Domains"
4. 添加 `api.yourdomain.com`

### 4. 监控与日志

```bash
# 实时查看日志
npx wrangler tail

# 带过滤器
npx wrangler tail --format pretty --status error
```

在 Dashboard 中可以查看：
- 请求量统计
- 错误率
- CPU 使用情况
- 地理分布

### 5. GitHub Actions 自动部署

创建 `.github/workflows/deploy.yml`：

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

在 GitHub 仓库 Settings → Secrets 中添加 `CF_API_TOKEN`（从 Cloudflare Dashboard 获取）。

---

## 十一、常见问题与面试要点

### 1. 常见问题

**Q: Workers 的冷启动时间是多少？**

A: Workers 的冷启动时间通常 < 5ms，因为使用 V8 isolates 而非容器。这是相比 AWS Lambda（100ms-数秒）的巨大优势。

**Q: Workers 支持 WebSocket 吗？**

A: 基础 Workers 支持 WebSocket 的透传（代理），但如果需要在 Worker 中维持 WebSocket 连接状态，需要使用 Durable Objects（付费功能）。

**Q: 如何处理大文件上传？**

A: Workers 请求体限制为 100MB（付费版）。对于大文件，建议使用 R2 存储的直传 URL（Presigned URL）。

**Q: Workers 和 Pages Functions 有什么区别？**

A: Pages Functions 是 Cloudflare Pages 的一部分，主要用于为静态站点添加后端功能。底层也是 Workers，但部署方式和使用场景不同。

### 2. 面试要点

**边缘计算相关**：
- 解释什么是边缘计算，与传统云计算的区别
- Workers 使用 V8 isolates 而非容器的优势
- 冷启动优化的原理

**Serverless 架构**：
- 无服务器架构的优缺点
- 适合和不适合 Serverless 的场景
- 如何处理 Serverless 的状态管理

**实际应用**：
- 如何设计一个高可用的 API 代理
- Workers 的限制（CPU 时间、内存）及应对方案
- 如何监控和排查 Workers 问题

---

## 十二、最佳实践总结

### 1. 性能优化

- 使用 `ctx.waitUntil()` 处理非关键异步任务
- 合理使用 KV 缓存，减少外部请求
- 避免在热路径上做复杂计算

### 2. 安全建议

- 敏感信息使用 Secret，不要硬编码
- 实现请求限流，防止滥用
- 验证所有用户输入
- 使用 CORS 限制来源域名

### 3. 代码组织

- 复杂项目使用 Hono 等框架
- 按功能拆分模块
- 统一错误处理和响应格式

### 4. 成本控制

- 善用免费额度，合理设计架构
- 监控使用量，设置告警
- 静态资源使用 R2 或 Pages 托管

---

## 总结

Cloudflare Workers 是一个强大且经济实惠的边缘计算平台。它的核心优势是：

1. **极低延迟**：全球 300+ 节点，代码运行在离用户最近的位置
2. **极快冷启动**：V8 isolates 技术，< 5ms 启动
3. **慷慨免费额度**：每天 10 万次请求，个人项目基本免费
4. **简单易用**：几分钟就能部署上线

**适合场景**：API 代理、短链接、边缘处理、轻量 API、Webhook 等

**下一步建议**：
1. 注册 Cloudflare 账号，部署你的第一个 Worker
2. 尝试本文的 API 代理或短链接案例
3. 了解 Workers KV 和 D1 的高级用法
4. 探索 Durable Objects 实现有状态应用

**参考资料**：
- [Cloudflare Workers 官方文档](https://developers.cloudflare.com/workers/)
- [Workers 定价详情](https://developers.cloudflare.com/workers/platform/pricing/)
- [Hono 框架文档](https://hono.dev/docs/getting-started/cloudflare-workers)
- [Cloudflare D1 数据库指南](https://developers.cloudflare.com/d1/)
