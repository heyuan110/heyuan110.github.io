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
- [ ] 2. 默认深色主题，配色遵循设计规范
- [ ] 3. 响应式布局（PC + 平板 + 手机适配）
- [ ] 4. JavaScript 使用 IIFE 模式避免全局污染
- [ ] 5. 引入 `common/common.css` 和 `common/common.js`（由 common.js 注入 header/footer）

### 多语言（强制，common.js 统管）
- [ ] 6. 支持 4 种语言：English (en)、中文 (zh-CN)、Français (fr)、Español (es)
- [ ] 7. HTML 元素使用 `data-i18n="key"` 属性标记
- [ ] 8. 输入框 placeholder 使用 `data-i18n-placeholder="key"` 属性
- [ ] 9. 翻译对象必须包含 `tool_name` 键（面包屑工具名多语言）
- [ ] 10. 翻译对象通过 `window._translations = translations;` 暴露
- [ ] 11. 工具内部 `t()` 函数使用 `WebToolbox.getCurrentLang()` 获取当前语言
- [ ] 12. 禁止手写语言切换器 HTML/JS，由 common.js 自动注入
- [ ] 13. 默认语言为 English

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
  <button class="faq-question">
    <span data-i18n="faq_free_q">Is this tool really free with no ads?</span>
    <span class="arrow">▼</span>
  </button>
  <div class="faq-answer"><p data-i18n="faq_free_a">
    Yes, 100% free with no ads, no registration, no watermark, and no usage limits. All processing happens locally in your browser — your data is never uploaded to any server.
  </p></div>
</div>
```
> FAQ 交互由 common.js `bindFaqAccordion()` 自动绑定，禁止手写 `onclick` 或 `toggleFaq`。

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

> 注意：语言切换器、FAQ 手风琴交互、header/footer 均由 common.js 自动注入，**禁止手写**。
> 所有可见内容（trust-bar、features、faq、related-tools）必须在 `.container` 内部。

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

    <!-- B1. WebApplication -->
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

    <!-- B2. BreadcrumbList -->
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

    <!-- B3. HowTo -->
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

    <!-- B4. FAQPage -->
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

    <!-- 公共样式（必须引入） -->
    <link rel="stylesheet" href="common/common.css">

    <style>
        /* ========== 基础样式 ========== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px; }

        /* ========== 工具主体区域样式 ========== */
        /* ... 根据工具需要自定义 ... */

        /* ========== Trust Bar ========== */
        /* 使用 common.css 的 .trust-bar / .trust-item 类名即可 */

        /* ========== 功能特点区域 ========== */
        .features-section { max-width: 1000px; margin: 40px auto; padding: 0 20px; }
        .features-section h2 { text-align: center; font-size: 24px; margin-bottom: 24px; color: #fff; }
        .features-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .feature-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px; padding: 24px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .feature-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3); }
        .feature-card .icon { font-size: 32px; margin-bottom: 12px; }
        .feature-card h3 { color: #a78bfa; margin-bottom: 8px; font-size: 16px; }
        .feature-card p { color: #9ca3af; font-size: 14px; line-height: 1.5; }

        /* ========== FAQ 手风琴 ========== */
        .faq-section { max-width: 800px; margin: 40px auto; padding: 0 20px; }
        .faq-section h2 { text-align: center; font-size: 24px; margin-bottom: 24px; color: #fff; }
        .faq-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px; margin-bottom: 12px; overflow: hidden;
        }
        .faq-question {
            width: 100%; background: none; border: none;
            padding: 16px 20px; cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
            font-weight: 500; color: #e0e0e0; font-size: inherit;
        }
        .faq-question:hover { background: rgba(124, 58, 237, 0.1); }
        .faq-question .arrow { transition: transform 0.3s; font-size: 14px; color: #7c3aed; }
        .faq-item.active .faq-question .arrow { transform: rotate(180deg); }
        .faq-answer { max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }
        .faq-item.active .faq-answer { max-height: 200px; }
        .faq-answer p { padding: 0 20px 16px; color: #9ca3af; font-size: 14px; line-height: 1.6; }

        /* ========== 响应式 ========== */
        @media (max-width: 768px) {
            .container { padding: 20px; }
            .features-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
<!-- ===== 所有可见内容在 .container 内 ===== -->
<div class="container">

    <!-- ==================== 工具主体区域 ==================== -->
    <h1 data-i18n="title">{工具标题}</h1>
    <!-- 工具功能 HTML -->

    <!-- ==================== Trust Bar ==================== -->
    <div class="trust-bar">
        <span class="trust-item" data-i18n="trust_users">🌍 Used by 50,000+ users</span>
        <span class="trust-item" data-i18n="trust_rating">⭐ 4.9/5 rating</span>
        <span class="trust-item" data-i18n="trust_privacy">🔒 100% Private</span>
        <span class="trust-item" data-i18n="trust_free">🚫 No Ads, No Signup</span>
    </div>

    <!-- ==================== 功能特点区域 ==================== -->
    <section class="features-section">
        <h2 data-i18n="features_title">Key Features</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="icon">🔒</div>
                <h3 data-i18n="feature1_title">100% Free & Private</h3>
                <p data-i18n="feature1_desc">No ads, no signup, no watermark. Everything runs locally in your browser.</p>
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

    <!-- ==================== FAQ 区域（交互由 common.js 自动绑定） ==================== -->
    <section class="faq-section">
        <h2 data-i18n="faq_title">Frequently Asked Questions</h2>
        <div class="faq-item">
            <button class="faq-question">
                <span data-i18n="faq1_q">{问题1}?</span>
                <span class="arrow">▼</span>
            </button>
            <div class="faq-answer"><p data-i18n="faq1_a">{回答1}</p></div>
        </div>
        <div class="faq-item">
            <button class="faq-question">
                <span data-i18n="faq2_q">{问题2}?</span>
                <span class="arrow">▼</span>
            </button>
            <div class="faq-answer"><p data-i18n="faq2_a">{回答2}</p></div>
        </div>
        <div class="faq-item">
            <button class="faq-question">
                <span data-i18n="faq3_q">{问题3}?</span>
                <span class="arrow">▼</span>
            </button>
            <div class="faq-answer"><p data-i18n="faq3_a">{回答3}</p></div>
        </div>
        <div class="faq-item">
            <button class="faq-question">
                <span data-i18n="faq4_q">{问题4}?</span>
                <span class="arrow">▼</span>
            </button>
            <div class="faq-answer"><p data-i18n="faq4_a">{回答4}</p></div>
        </div>
        <div class="faq-item">
            <button class="faq-question">
                <span data-i18n="faq_free_q">Is this tool really free with no ads?</span>
                <span class="arrow">▼</span>
            </button>
            <div class="faq-answer"><p data-i18n="faq_free_a">Yes, 100% free with no ads, no registration, no watermark, and no usage limits.</p></div>
        </div>
    </section>

    <!-- ==================== 相关工具推荐（样式由 common.css 控制） ==================== -->
    <section class="related-tools">
        <h3 data-i18n="related_title">Related Tools</h3>
        <div class="related-grid">
            <a href="{工具1链接}" class="related-card">
                <div>{emoji}</div>
                <h4 data-i18n="related1_name">{相关工具1名称}</h4>
                <p data-i18n="related1_desc">{相关工具1描述}</p>
            </a>
            <a href="{工具2链接}" class="related-card">
                <div>{emoji}</div>
                <h4 data-i18n="related2_name">{相关工具2名称}</h4>
                <p data-i18n="related2_desc">{相关工具2描述}</p>
            </a>
            <a href="{工具3链接}" class="related-card">
                <div>{emoji}</div>
                <h4 data-i18n="related3_name">{相关工具3名称}</h4>
                <p data-i18n="related3_desc">{相关工具3描述}</p>
            </a>
        </div>
    </section>

</div><!-- .container end -->

<!-- ===== 脚本区（在 container 外部） ===== -->
<script>
(function() {
    'use strict';

    // ========== 翻译对象 ==========
    var translations = {
        en: {
            tool_name: '{Tool Name}',  // 必须：面包屑工具名
            title: '{Tool Title}',
            // 工具功能区翻译...
            trust_users: '🌍 Used by 50,000+ users',
            trust_rating: '⭐ 4.9/5 rating',
            trust_privacy: '🔒 100% Private',
            trust_free: '🚫 No Ads, No Signup',
            features_title: 'Key Features',
            feature1_title: '100% Free & Private',
            feature1_desc: 'No ads, no signup, no watermark. Everything runs locally in your browser.',
            // ... 其余翻译键 ...
            faq_free_q: 'Is this tool really free with no ads?',
            faq_free_a: 'Yes, 100% free with no ads, no registration, no watermark, and no usage limits.',
            related_title: 'Related Tools',
            related1_name: '{Related Tool 1}', related1_desc: '{Description}'
        },
        'zh-CN': {
            tool_name: '{工具中文名}',
            title: '{工具标题}',
            // ... 中文翻译 ...
        },
        fr: {
            tool_name: '{Nom de l\'outil}',
            title: '{Titre}',
            // ... 法文翻译 ...
        },
        es: {
            tool_name: '{Nombre de la herramienta}',
            title: '{Título}',
            // ... 西文翻译 ...
        }
    };

    // 获取当前语言（由 common.js 管理）
    function t(key) {
        var lang = typeof WebToolbox !== 'undefined' ? WebToolbox.getCurrentLang() : 'en';
        return (translations[lang] && translations[lang][key]) || translations.en[key] || key;
    }

    // ========== 工具核心逻辑 ==========
    // ... 工具功能代码 ...

    // 暴露翻译对象供 common.js 使用
    window._translations = translations;
})();
</script>
<!-- common.js 集成（禁止修改 common 目录） -->
<script src="common/common.js"
    data-tool-id="{tool-id}"
    data-tool-name="{Tool Name}"
    data-category="{category}"></script>
<script>WebToolbox.init(window._translations);</script>
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
| 默认主题 | **深色（夜晚模式）** |
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
| 主题切换 | 默认隐藏，需 `data-show-theme-toggle="true"` 启用 |
