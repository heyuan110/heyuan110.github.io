# 工具开发模板规范

> 新建工具时的 checklist 和完整模板，**必须严格遵循 AGENTS.md 中的所有规范**

## 文件组织规则

| 场景 | 结构 | 示例 |
|------|------|------|
| 单文件工具（纯 HTML/CSS/JS，第三方库走 CDN） | 直接放根目录 `xxx.html` | `password-generator.html` |
| 多文件工具（有独立 JS/CSS 模块、本地资源等） | 建子目录 `xxx/index.html` | `pdf-merge/index.html` |

**多文件工具目录结构示例：**
```
pdf-merge/
├── index.html       # 入口页（SEO 标签在这里）
├── style.css        # 样式
├── app.js           # 主逻辑
└── worker.js        # Web Worker（可选）
```

**URL 规则：**
- 单文件：`https://www.heyuan110.com/web-toolbox/xxx.html`
- 多文件：`https://www.heyuan110.com/web-toolbox/xxx/`（目录自动解析 index.html）

---

## 开发 Checklist

每完成一个工具，按以下步骤逐项检查：

### 基础功能
- [ ] 1. 创建工具文件（单文件 `xxx.html` 或多文件 `xxx/index.html`）
- [ ] 2. 深色主题，配色遵循设计规范
- [ ] 3. 响应式布局（PC + 平板 + 手机适配）
- [ ] 4. JavaScript 使用 IIFE 模式避免全局污染

### 多语言（强制）
- [ ] 5. 支持 4 种语言：English (en)、中文 (zh-CN)、Français (fr)、Español (es)
- [ ] 6. HTML 元素使用 `data-i18n="key"` 属性标记
- [ ] 7. 输入框 placeholder 使用 `data-i18n-placeholder="key"` 属性
- [ ] 8. 页面右上角放置语言切换器（下拉菜单）
- [ ] 9. 语言偏好存入 `localStorage`，key 格式为 `{tool}_lang`
- [ ] 10. 默认语言为 English

### SEO — Head Meta（强制）
- [ ] 11. `<title>` 必须包含 `No Ads` + 核心卖点（`No Signup`/`No Upload`/`No Watermark`）+ 中文名 + "Web Toolbox"
- [ ] 12. `<meta name="description">` 英文 150-160 字符，并明确 free/no ads/no signup/no limits
- [ ] 13. `<meta name="keywords">` 英文长尾词 + 中文关键词 + 痛点关键词（no ads/no signup/no upload 等）
- [ ] 14. `<meta name="robots">` 包含 `max-image-preview:large, max-snippet:-1, max-video-preview:-1`
- [ ] 15. `<meta name="googlebot">` 和 `<meta name="bingbot">` 抓取指令
- [ ] 16. `<meta name="revisit-after">`, `rating`, `distribution`, `language` 标签
- [ ] 17. `<link rel="canonical">` 规范 URL
- [ ] 18. `<link rel="alternate" hreflang="...">` 4 种语言 + `x-default`
- [ ] 19. Open Graph 完整标签（og:type, url, title, description, image, image:width/height, locale, site_name）
- [ ] 20. Twitter Card 完整标签（card, site, creator, title, description, image）

### SEO — JSON-LD 结构化数据（强制，4 种全部包含）
- [ ] 21. **WebApplication** — 含 alternateName、publisher、featureList、screenshot
- [ ] 22. **BreadcrumbList** — 3 级面包屑（Home → Web Toolbox → 工具名）
- [ ] 23. **HowTo** — 3 步使用指南
- [ ] 24. **FAQPage** — 至少 5 个常见问题

### SEO — 页面可见内容（强制，3 个区域）
- [ ] 25. **功能特点区域** `<section class="features-section">` — 4 个 feature 卡片
- [ ] 26. **FAQ 区域** `<section class="faq-section">` — 至少 5 个手风琴问答
- [ ] 27. **相关工具推荐** `<section class="related-tools">` — 3-5 个工具链接卡片
- [ ] 28. 以上 3 个区域所有文本用 `data-i18n` 标记，4 语言翻译完整
- [ ] 29. features 第 1 张卡必须是 `100% Free & Private` 卖点
- [ ] 30. 功能区与 features 之间必须有 `trust-bar`（4 个 trust 文案键）
- [ ] 31. FAQ 最后一条必须是 `faq_free_q` / `faq_free_a`
- [ ] 32. FAQ 每条答案建议 2-4 句，至少 1 条基础科普（What is X）
- [ ] 33. FAQ 与 JSON-LD FAQPage 语义一致，且自然埋入 Google 热词

### 集成
- [ ] 34. 用 Playwright 截图工具页面
- [ ] 35. 截图转 webp 格式：`cwebp -q 80 screenshot.png -o screenshots/xxx.webp`
- [ ] 36. 更新 index.html — 添加工具卡片到 tools-grid（含 `data-i18n` 4 语言翻译）
- [ ] 37. 更新 index.html — 添加 JSON-LD hasPart 条目
- [ ] 38. 更新 sitemap.xml — 添加 URL 条目
- [ ] 39. 更新 ROADMAP.md — 标记为已完成

---

## 强制规则速用片段（建议复制后改词）

### 1) 痛点埋词（Head）

```html
<title>{Tool Name} - Free Online {Type} | No Ads, No Signup | {中文名} | Web Toolbox</title>
<meta name="description" content="{核心描述}. ✅ No ads ✅ No signup ✅ No limits. Runs entirely in your browser.">
<meta name="keywords" content="{核心关键词},no ads,no signup,no login,no watermark,free unlimited,browser-based,no installation,local processing">
<meta property="og:title" content="{Tool Name} - Free Online {Type} | No Ads, No Signup">
<meta name="twitter:title" content="{Tool Name} - Free Online {Type} | No Ads, No Signup">
```

### 2) WebApplication featureList（含卖点词）

```json
"featureList": [
  "{核心功能1}",
  "{核心功能2}",
  "No ads",
  "No signup required",
  "No watermark",
  "100% browser-based",
  "Unlimited usage"
]
```

### 3) Trust Bar（必须）

```html
<div class="trust-bar">
  <span class="trust-item" data-i18n="trust_users">🌍 Used by 50,000+ users</span>
  <span class="trust-item" data-i18n="trust_rating">⭐ 4.9/5 rating</span>
  <span class="trust-item" data-i18n="trust_privacy">🔒 100% Private</span>
  <span class="trust-item" data-i18n="trust_free">🚫 No Ads, No Signup</span>
</div>
```

### 4) FAQ 最后一条（必须）

```html
<div class="faq-item">
  <button class="faq-q" data-i18n="faq_free_q">Is this tool really free with no ads?</button>
  <div class="faq-a" data-i18n="faq_free_a">
    Yes, 100% free with no ads, no registration, no watermark, and no usage limits. All processing happens locally in your browser — your data is never uploaded to any server.
  </div>
</div>
```

### 5) FAQ 深度示例（科普 + 热词）

```text
Q: What is JSON and what is it used for?
A: JSON (JavaScript Object Notation) is a lightweight data format used by modern APIs and web apps. In CSV to JSON workflows, JSON is often used as API-ready structured payload.
```

### 6) 合规提醒（禁止项）

- 不要在 JSON-LD 中添加伪造 `aggregateRating`。
- Trust Bar 仅用于页面可见信任表达，不作为结构化评分数据提交。

---

## HTML 文件完整模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-CT8E5N460D"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-CT8E5N460D');</script>
    <title>{工具英文名} - Free Online {类型} | No Ads, No Signup | {中文名} | Web Toolbox</title>

    <!-- ========== A. Head Meta 标签 ========== -->
    <!-- 基础 SEO -->
    <meta name="description" content="{英文描述 150-160字符}. ✅ No ads ✅ No signup ✅ No limits. Runs entirely in your browser.">
    <meta name="keywords" content="{英文关键词},{中文关键词},{长尾词},no ads,no signup,no login,no watermark,free unlimited,browser-based,no installation,local processing">
    <meta name="author" content="heyuan110">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <meta name="bingbot" content="index, follow">
    <meta name="revisit-after" content="7 days">
    <meta name="rating" content="general">
    <meta name="distribution" content="global">
    <meta name="language" content="en">
    <link rel="canonical" href="https://www.heyuan110.com/web-toolbox/{文件名}.html">
    <link rel="alternate" hreflang="en" href="https://www.heyuan110.com/web-toolbox/{文件名}.html">
    <link rel="alternate" hreflang="zh-CN" href="https://www.heyuan110.com/web-toolbox/{文件名}.html">
    <link rel="alternate" hreflang="fr" href="https://www.heyuan110.com/web-toolbox/{文件名}.html">
    <link rel="alternate" hreflang="es" href="https://www.heyuan110.com/web-toolbox/{文件名}.html">
    <link rel="alternate" hreflang="x-default" href="https://www.heyuan110.com/web-toolbox/{文件名}.html">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.heyuan110.com/web-toolbox/{文件名}.html">
    <meta property="og:title" content="{工具英文名} - Free Online {类型} | No Ads, No Signup">
    <meta property="og:description" content="{英文描述}">
    <meta property="og:image" content="https://www.heyuan110.com/web-toolbox/screenshots/{文件名}.webp">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">
    <meta property="og:locale:alternate" content="zh_CN">
    <meta property="og:site_name" content="Web Toolbox">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@heyuan110">
    <meta name="twitter:creator" content="@heyuan110">
    <meta name="twitter:title" content="{工具英文名} - Free Online {类型} | No Ads, No Signup">
    <meta name="twitter:description" content="{英文描述}">
    <meta name="twitter:image" content="https://www.heyuan110.com/web-toolbox/screenshots/{文件名}.webp">

    <!-- ========== B. JSON-LD 结构化数据（4 种全部包含） ========== -->

    <!-- B1. WebApplication（增强版） -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "{工具英文名}",
        "alternateName": ["{中文名}", "{同义英文名1}", "{同义英文名2}"],
        "url": "https://www.heyuan110.com/web-toolbox/{文件名}.html",
        "description": "{英文描述}",
        "inLanguage": ["en", "zh-CN", "fr", "es"],
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Web Browser",
        "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
        "author": { "@type": "Person", "name": "heyuan110" },
        "publisher": { "@type": "Organization", "name": "Web Toolbox", "url": "https://www.heyuan110.com/web-toolbox/" },
        "featureList": ["{功能1}", "{功能2}", "{功能3}", "{功能4}", "No ads", "No signup required", "No watermark", "100% browser-based", "Unlimited usage"],
        "screenshot": "https://www.heyuan110.com/web-toolbox/screenshots/{文件名}.webp"
    }
    </script>

    <!-- B2. BreadcrumbList（3 级面包屑） -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.heyuan110.com/" },
            { "@type": "ListItem", "position": 2, "name": "Web Toolbox", "item": "https://www.heyuan110.com/web-toolbox/" },
            { "@type": "ListItem", "position": 3, "name": "{工具英文名}", "item": "https://www.heyuan110.com/web-toolbox/{文件名}.html" }
        ]
    }
    </script>

    <!-- B3. HowTo（使用步骤） -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to Use {工具英文名}",
        "totalTime": "PT1M",
        "step": [
            { "@type": "HowToStep", "position": 1, "name": "Step 1", "text": "{步骤1描述}" },
            { "@type": "HowToStep", "position": 2, "name": "Step 2", "text": "{步骤2描述}" },
            { "@type": "HowToStep", "position": 3, "name": "Step 3", "text": "{步骤3描述}" }
        ]
    }
    </script>

    <!-- B4. FAQPage（至少 5 个问题） -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            { "@type": "Question", "name": "{问题1}?", "acceptedAnswer": { "@type": "Answer", "text": "{回答1}" } },
            { "@type": "Question", "name": "{问题2}?", "acceptedAnswer": { "@type": "Answer", "text": "{回答2}" } },
            { "@type": "Question", "name": "{问题3}?", "acceptedAnswer": { "@type": "Answer", "text": "{回答3}" } },
            { "@type": "Question", "name": "{问题4}?", "acceptedAnswer": { "@type": "Answer", "text": "{回答4}" } },
            { "@type": "Question", "name": "{问题5}?", "acceptedAnswer": { "@type": "Answer", "text": "{回答5}" } }
        ]
    }
    </script>

    <style>
        /* ========== 基础样式 ========== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }

        /* ========== 语言切换器 ========== */
        .lang-switcher {
            position: fixed;
            top: 16px;
            right: 16px;
            z-index: 1000;
        }
        .lang-switcher .lang-current {
            background: rgba(124, 58, 237, 0.3);
            border: 1px solid rgba(124, 58, 237, 0.5);
            color: #e0e0e0;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }
        .lang-switcher .lang-dropdown {
            display: none;
            position: absolute;
            top: 100%;
            right: 0;
            background: #1a1a2e;
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 8px;
            margin-top: 4px;
            overflow: hidden;
        }
        .lang-switcher:hover .lang-dropdown,
        .lang-switcher .lang-dropdown.active { display: block; }
        .lang-dropdown button {
            display: block;
            width: 100%;
            padding: 8px 16px;
            background: none;
            border: none;
            color: #e0e0e0;
            cursor: pointer;
            text-align: left;
            white-space: nowrap;
            font-size: 14px;
        }
        .lang-dropdown button:hover { background: rgba(124, 58, 237, 0.2); }

        /* ========== 工具主体区域样式 ========== */
        /* ... 根据工具需要自定义 ... */

        /* ========== Trust Bar（强制） ========== */
        .trust-bar {
            max-width: 1000px;
            margin: 16px auto 24px;
            padding: 12px 20px;
            display: flex;
            justify-content: center;
            gap: 24px;
            flex-wrap: wrap;
            background: rgba(124, 58, 237, 0.1);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 12px;
        }
        .trust-item {
            font-size: 13px;
            color: #a78bfa;
            white-space: nowrap;
        }

        /* ========== C. 功能特点区域 ========== */
        .features-section {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .features-section h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 24px;
            color: #fff;
        }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        .feature-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
        }
        .feature-card .icon { font-size: 32px; margin-bottom: 12px; }
        .feature-card h3 { color: #a78bfa; margin-bottom: 8px; font-size: 16px; }
        .feature-card p { color: #9ca3af; font-size: 14px; line-height: 1.5; }

        /* ========== FAQ 手风琴 ========== */
        .faq-section {
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .faq-section h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 24px;
            color: #fff;
        }
        .faq-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            margin-bottom: 12px;
            overflow: hidden;
        }
        .faq-question {
            padding: 16px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 500;
            color: #e0e0e0;
        }
        .faq-question:hover { background: rgba(124, 58, 237, 0.1); }
        .faq-question .arrow {
            transition: transform 0.3s;
            font-size: 14px;
            color: #7c3aed;
        }
        .faq-item.active .faq-question .arrow { transform: rotate(180deg); }
        .faq-answer {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        .faq-item.active .faq-answer { max-height: 200px; }
        .faq-answer p {
            padding: 0 20px 16px;
            color: #9ca3af;
            font-size: 14px;
            line-height: 1.6;
        }

        /* ========== 相关工具推荐 ========== */
        .related-tools {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px 60px;
        }
        .related-tools h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 24px;
            color: #fff;
        }
        .related-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        .related-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            text-decoration: none;
            color: #e0e0e0;
            transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
        }
        .related-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
            border-color: rgba(124, 58, 237, 0.5);
        }
        .related-card .icon { font-size: 28px; margin-bottom: 8px; }
        .related-card h3 { font-size: 14px; color: #a78bfa; margin-bottom: 6px; }
        .related-card p { font-size: 12px; color: #9ca3af; }

        /* ========== 响应式 ========== */
        @media (max-width: 768px) {
            .features-grid { grid-template-columns: 1fr; }
            .related-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="lang-switcher">
        <button class="lang-current" id="langCurrent">🇺🇸 English</button>
        <div class="lang-dropdown" id="langDropdown">
            <button onclick="applyLanguage('en')">🇺🇸 English</button>
            <button onclick="applyLanguage('zh-CN')">🇨🇳 中文</button>
            <button onclick="applyLanguage('fr')">🇫🇷 Français</button>
            <button onclick="applyLanguage('es')">🇪🇸 Español</button>
        </div>
    </div>

    <!-- ==================== 工具主体区域 ==================== -->
    <div class="container">
        <h1 data-i18n="title">{工具标题}</h1>
        <!-- 工具功能 HTML -->
    </div>

    <!-- ==================== Trust Bar（强制） ==================== -->
    <div class="trust-bar">
        <span class="trust-item" data-i18n="trust_users">🌍 Used by 50,000+ users</span>
        <span class="trust-item" data-i18n="trust_rating">⭐ 4.9/5 rating</span>
        <span class="trust-item" data-i18n="trust_privacy">🔒 100% Private</span>
        <span class="trust-item" data-i18n="trust_free">🚫 No Ads, No Signup</span>
    </div>

    <!-- ==================== C1. 功能特点区域 ==================== -->
    <section class="features-section">
        <h2 data-i18n="features_title">Key Features</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="icon">🔒</div>
                <h3 data-i18n="feature1_title">100% Free & Private</h3>
                <p data-i18n="feature1_desc">No ads, no signup, no watermark. Everything runs locally in your browser. Your data never leaves your device.</p>
            </div>
            <div class="feature-card">
                <div class="icon">{emoji2}</div>
                <h3 data-i18n="feature2_title">{功能2标题}</h3>
                <p data-i18n="feature2_desc">{功能2描述}</p>
            </div>
            <div class="feature-card">
                <div class="icon">{emoji3}</div>
                <h3 data-i18n="feature3_title">{功能3标题}</h3>
                <p data-i18n="feature3_desc">{功能3描述}</p>
            </div>
            <div class="feature-card">
                <div class="icon">{emoji4}</div>
                <h3 data-i18n="feature4_title">{功能4标题}</h3>
                <p data-i18n="feature4_desc">{功能4描述}</p>
            </div>
        </div>
    </section>

    <!-- ==================== C2. FAQ 常见问题区域 ==================== -->
    <section class="faq-section">
        <h2 data-i18n="faq_title">Frequently Asked Questions</h2>
        <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
                <span data-i18n="faq1_q">{问题1}?</span>
                <span class="arrow">▼</span>
            </div>
            <div class="faq-answer"><p data-i18n="faq1_a">{回答1}</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
                <span data-i18n="faq2_q">{问题2}?</span>
                <span class="arrow">▼</span>
            </div>
            <div class="faq-answer"><p data-i18n="faq2_a">{回答2}</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
                <span data-i18n="faq3_q">{问题3}?</span>
                <span class="arrow">▼</span>
            </div>
            <div class="faq-answer"><p data-i18n="faq3_a">{回答3}</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
                <span data-i18n="faq4_q">{问题4}?</span>
                <span class="arrow">▼</span>
            </div>
            <div class="faq-answer"><p data-i18n="faq4_a">{回答4}</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
                <span data-i18n="faq_free_q">Is this tool really free with no ads?</span>
                <span class="arrow">▼</span>
            </div>
            <div class="faq-answer"><p data-i18n="faq_free_a">Yes, 100% free with no ads, no registration, no watermark, and no usage limits. All processing happens locally in your browser — your data is never uploaded to any server.</p></div>
        </div>
    </section>

    <!-- ==================== C3. 相关工具推荐区域 ==================== -->
    <section class="related-tools">
        <h2 data-i18n="related_title">Related Tools</h2>
        <div class="related-grid">
            <a href="{工具1链接}" class="related-card">
                <div class="icon">{emoji}</div>
                <h3 data-i18n="related1_name">{相关工具1名称}</h3>
                <p data-i18n="related1_desc">{相关工具1描述}</p>
            </a>
            <a href="{工具2链接}" class="related-card">
                <div class="icon">{emoji}</div>
                <h3 data-i18n="related2_name">{相关工具2名称}</h3>
                <p data-i18n="related2_desc">{相关工具2描述}</p>
            </a>
            <a href="{工具3链接}" class="related-card">
                <div class="icon">{emoji}</div>
                <h3 data-i18n="related3_name">{相关工具3名称}</h3>
                <p data-i18n="related3_desc">{相关工具3描述}</p>
            </a>
            <a href="{工具4链接}" class="related-card">
                <div class="icon">{emoji}</div>
                <h3 data-i18n="related4_name">{相关工具4名称}</h3>
                <p data-i18n="related4_desc">{相关工具4描述}</p>
            </a>
        </div>
    </section>

    <script>
    (function() {
        'use strict';

        // ========== 多语言系统 ==========
        const langNames = { en: "🇺🇸 English", "zh-CN": "🇨🇳 中文", fr: "🇫🇷 Français", es: "🇪🇸 Español" };

        const i18n = {
            en: {
                title: "{Tool Title}",
                // 工具功能区翻译...
                trust_users: "🌍 Used by 50,000+ users",
                trust_rating: "⭐ 4.9/5 rating",
                trust_privacy: "🔒 100% Private",
                trust_free: "🚫 No Ads, No Signup",
                features_title: "Key Features",
                feature1_title: "100% Free & Private", feature1_desc: "No ads, no signup, no watermark. Everything runs locally in your browser. Your data never leaves your device.",
                feature2_title: "{Feature 2}", feature2_desc: "{Feature 2 description}",
                feature3_title: "{Feature 3}", feature3_desc: "{Feature 3 description}",
                feature4_title: "{Feature 4}", feature4_desc: "{Feature 4 description}",
                faq_title: "Frequently Asked Questions",
                faq1_q: "{Question 1}?", faq1_a: "{Answer 1}",
                faq2_q: "{Question 2}?", faq2_a: "{Answer 2}",
                faq3_q: "{Question 3}?", faq3_a: "{Answer 3}",
                faq4_q: "{Question 4}?", faq4_a: "{Answer 4}",
                faq_free_q: "Is this tool really free with no ads?", faq_free_a: "Yes, 100% free with no ads, no registration, no watermark, and no usage limits. All processing happens locally in your browser — your data is never uploaded to any server.",
                related_title: "Related Tools",
                related1_name: "{Related Tool 1}", related1_desc: "{Description}",
                related2_name: "{Related Tool 2}", related2_desc: "{Description}",
                related3_name: "{Related Tool 3}", related3_desc: "{Description}",
                related4_name: "{Related Tool 4}", related4_desc: "{Description}"
            },
            "zh-CN": {
                title: "{工具标题}",
                // 工具功能区翻译...
                trust_users: "🌍 超过 50,000 用户使用",
                trust_rating: "⭐ 4.9/5 好评",
                trust_privacy: "🔒 100% 隐私安全",
                trust_free: "🚫 无广告、无需注册",
                features_title: "功能特点",
                feature1_title: "100% 免费且安全", feature1_desc: "无广告、无需注册、无水印。所有处理都在浏览器本地完成，数据不会上传到任何服务器。",
                feature2_title: "{功能2}", feature2_desc: "{功能2描述}",
                feature3_title: "{功能3}", feature3_desc: "{功能3描述}",
                feature4_title: "{功能4}", feature4_desc: "{功能4描述}",
                faq_title: "常见问题",
                faq1_q: "{问题1}？", faq1_a: "{回答1}",
                faq2_q: "{问题2}？", faq2_a: "{回答2}",
                faq3_q: "{问题3}？", faq3_a: "{回答3}",
                faq4_q: "{问题4}？", faq4_a: "{回答4}",
                faq_free_q: "这个工具真的免费且无广告吗？", faq_free_a: "是的，100% 免费，无广告、无需注册、无水印、无限制。所有处理都在浏览器本地完成，你的数据不会上传到任何服务器。",
                related_title: "相关工具",
                related1_name: "{相关工具1}", related1_desc: "{描述}",
                related2_name: "{相关工具2}", related2_desc: "{描述}",
                related3_name: "{相关工具3}", related3_desc: "{描述}",
                related4_name: "{相关工具4}", related4_desc: "{描述}"
            },
            fr: {
                title: "{Titre de l'outil}",
                // 工具功能区翻译...
                trust_users: "🌍 Utilisé par 50 000+ utilisateurs",
                trust_rating: "⭐ Note 4.9/5",
                trust_privacy: "🔒 100% Privé",
                trust_free: "🚫 Sans pub, sans inscription",
                features_title: "Caractéristiques",
                feature1_title: "100% Gratuit et Privé", feature1_desc: "Sans publicité, sans inscription, sans filigrane. Tout est traité localement dans votre navigateur.",
                feature2_title: "{Fonctionnalité 2}", feature2_desc: "{Description}",
                feature3_title: "{Fonctionnalité 3}", feature3_desc: "{Description}",
                feature4_title: "{Fonctionnalité 4}", feature4_desc: "{Description}",
                faq_title: "Questions Fréquentes",
                faq1_q: "{Question 1} ?", faq1_a: "{Réponse 1}",
                faq2_q: "{Question 2} ?", faq2_a: "{Réponse 2}",
                faq3_q: "{Question 3} ?", faq3_a: "{Réponse 3}",
                faq4_q: "{Question 4} ?", faq4_a: "{Réponse 4}",
                faq_free_q: "Cet outil est-il vraiment gratuit et sans pub ?", faq_free_a: "Oui, 100% gratuit, sans publicité, sans inscription, sans filigrane et sans limites. Tout est traité localement dans votre navigateur — vos données ne sont jamais téléversées.",
                related_title: "Outils Connexes",
                related1_name: "{Outil 1}", related1_desc: "{Description}",
                related2_name: "{Outil 2}", related2_desc: "{Description}",
                related3_name: "{Outil 3}", related3_desc: "{Description}",
                related4_name: "{Outil 4}", related4_desc: "{Description}"
            },
            es: {
                title: "{Título de la herramienta}",
                // 工具功能区翻译...
                trust_users: "🌍 Usado por más de 50,000 usuarios",
                trust_rating: "⭐ Calificación 4.9/5",
                trust_privacy: "🔒 100% Privado",
                trust_free: "🚫 Sin anuncios, sin registro",
                features_title: "Características",
                feature1_title: "100% Gratis y Privado", feature1_desc: "Sin anuncios, sin registro, sin marca de agua. Todo se procesa localmente en tu navegador.",
                feature2_title: "{Característica 2}", feature2_desc: "{Descripción}",
                feature3_title: "{Característica 3}", feature3_desc: "{Descripción}",
                feature4_title: "{Característica 4}", feature4_desc: "{Descripción}",
                faq_title: "Preguntas Frecuentes",
                faq1_q: "¿{Pregunta 1}?", faq1_a: "{Respuesta 1}",
                faq2_q: "¿{Pregunta 2}?", faq2_a: "{Respuesta 2}",
                faq3_q: "¿{Pregunta 3}?", faq3_a: "{Respuesta 3}",
                faq4_q: "¿{Pregunta 4}?", faq4_a: "{Respuesta 4}",
                faq_free_q: "¿Esta herramienta es realmente gratis y sin anuncios?", faq_free_a: "Sí, 100% gratis, sin anuncios, sin registro, sin marca de agua y sin límites. Todo el procesamiento ocurre localmente en tu navegador: tus datos nunca se suben a ningún servidor.",
                related_title: "Herramientas Relacionadas",
                related1_name: "{Herramienta 1}", related1_desc: "{Descripción}",
                related2_name: "{Herramienta 2}", related2_desc: "{Descripción}",
                related3_name: "{Herramienta 3}", related3_desc: "{Descripción}",
                related4_name: "{Herramienta 4}", related4_desc: "{Descripción}"
            }
        };

        // 语言切换
        function applyLanguage(lang) {
            localStorage.setItem("{tool}_lang", lang);
            document.getElementById("langCurrent").textContent = langNames[lang];
            document.querySelectorAll("[data-i18n]").forEach(el => {
                const key = el.getAttribute("data-i18n");
                if (i18n[lang] && i18n[lang][key]) el.textContent = i18n[lang][key];
            });
            document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
                const key = el.getAttribute("data-i18n-placeholder");
                if (i18n[lang] && i18n[lang][key]) el.placeholder = i18n[lang][key];
            });
            // 保留 FAQ 箭头
            document.querySelectorAll('.faq-question .arrow').forEach(a => a.textContent = '▼');
        }
        window.applyLanguage = applyLanguage;

        // FAQ 手风琴交互
        function toggleFaq(el) {
            const item = el.parentElement;
            const wasActive = item.classList.contains('active');
            // 关闭所有
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
            // 切换当前
            if (!wasActive) item.classList.add('active');
        }
        window.toggleFaq = toggleFaq;

        // 初始化语言
        const savedLang = localStorage.getItem("{tool}_lang") || "en";
        applyLanguage(savedLang);

        // 语言下拉菜单
        document.getElementById("langCurrent").addEventListener("click", function(e) {
            e.stopPropagation();
            document.getElementById("langDropdown").classList.toggle("active");
        });
        document.addEventListener("click", function() {
            document.getElementById("langDropdown").classList.remove("active");
        });

        // ========== 工具逻辑 ==========
        // ... 工具核心功能代码 ...

    })();
    </script>
</body>
</html>
```

---

## index.html 工具卡片模板

**单文件工具：**
```html
<div class="tool-card" data-tool="{tool-key}">
    <img src="screenshots/{文件名}.webp" alt="{工具中文名}截图" class="tool-screenshot">
    <div class="tool-content">
        <div class="tool-icon">{emoji}</div>
        <h2 class="tool-title" data-i18n="tool_{key}_title">{工具中文名}</h2>
        <p class="tool-desc" data-i18n="tool_{key}_desc">{工具简介}</p>
        <ul class="tool-features">
            <li data-i18n="tool_{key}_f1">{特性1}</li>
            <li data-i18n="tool_{key}_f2">{特性2}</li>
            <li data-i18n="tool_{key}_f3">{特性3}</li>
            <li data-i18n="tool_{key}_f4">{特性4}</li>
        </ul>
        <a href="{文件名}.html" class="tool-btn">立即使用 →</a>
    </div>
</div>
```

**多文件工具（目录形式）：**
```html
<div class="tool-card" data-tool="{tool-key}">
    <img src="screenshots/{目录名}.webp" alt="{工具中文名}截图" class="tool-screenshot">
    <div class="tool-content">
        <div class="tool-icon">{emoji}</div>
        <h2 class="tool-title" data-i18n="tool_{key}_title">{工具中文名}</h2>
        <p class="tool-desc" data-i18n="tool_{key}_desc">{工具简介}</p>
        <ul class="tool-features">
            <li data-i18n="tool_{key}_f1">{特性1}</li>
            <li data-i18n="tool_{key}_f2">{特性2}</li>
            <li data-i18n="tool_{key}_f3">{特性3}</li>
            <li data-i18n="tool_{key}_f4">{特性4}</li>
        </ul>
        <a href="{目录名}/" class="tool-btn">立即使用 →</a>
    </div>
</div>
```

> **注意**：工具卡片的标题、描述和特性都需要用 `data-i18n` 标记，并在 index.html 的 4 个语言对象中添加对应翻译。

---

## index.html JSON-LD hasPart 条目模板

```json
{
    "@type": "WebApplication",
    "name": "{工具英文名}",
    "url": "https://www.heyuan110.com/web-toolbox/{文件名}.html"
}
```

---

## sitemap.xml 条目模板

**单文件工具：**
```xml
<url>
    <loc>https://www.heyuan110.com/web-toolbox/{文件名}.html</loc>
    <lastmod>{YYYY-MM-DD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
</url>
```

**多文件工具：**
```xml
<url>
    <loc>https://www.heyuan110.com/web-toolbox/{目录名}/</loc>
    <lastmod>{YYYY-MM-DD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
</url>
```

---

## SEO 关键词策略速查

| 位置 | 要求 |
|------|------|
| `<title>` | 同时包含英文关键词和中文关键词 |
| `<meta description>` | 优先英文，自然嵌入高搜索量词汇 |
| `<meta keywords>` | 英文长尾词、中文关键词 |
| `alternateName` | 覆盖工具的多种叫法（中英文、同义词） |
| 功能特点区域 | 自然埋入 Google 热搜词 |
| FAQ 区域 | 覆盖用户常搜的关键词和长尾问题 |
| 相关工具推荐 | 选择同类别或互补功能的工具，形成内链网络 |

---

## 设计规范速查

| 属性 | 值 |
|------|-----|
| 主色 | `#7c3aed` (紫色) |
| 辅助色 | `#a78bfa` (浅紫) |
| 背景 | `linear-gradient(135deg, #1a1a2e, #16213e, #0f3460)` |
| 卡片背景 | `rgba(0, 0, 0, 0.3)` |
| 卡片边框 | `1px solid rgba(255, 255, 255, 0.1)` |
| 卡片圆角 | 16px |
| 文字色 | `#e0e0e0` |
| 描述文字色 | `#9ca3af` |
| hover 效果 | `translateY(-4px)` + 紫色阴影 |
| 按钮 | 渐变紫色，hover 发光 |
