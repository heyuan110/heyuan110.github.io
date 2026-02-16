# 工具开发完整指南

> 新建/修改工具时的完整参考。规则权威来源：AGENTS.md
>
> 文件组织：工具页 `xxx.html`（简单）或 `xxx/index.html`（复杂）— 详见 AGENTS.md 项目范围

## 开发 Checklist

> R# 引用对应下方"规则详解"章节

### 基础功能
- [ ] 1. 创建工具文件 → AGENTS.md 项目范围
- [ ] 2. 深色主题 + 响应式 + IIFE → R1
- [ ] 3. 引入 `common/common.css` + `common/common.js` → R0
- [ ] 4. CSS reset `* { margin:0; padding:0; box-sizing:border-box }` → R1
- [ ] 5. body 背景渐变 + container max-width:1200px → R1
- [ ] 6. features-grid/feature-card/faq-section/faq-item 样式自定义 → R1
- [ ] 7. 如需主题切换：`data-show-theme-toggle="true"` + 完整浅色覆写 → R13

### 多语言
- [ ] 8. 4 语言翻译对象（en/zh-CN/fr/es），含 `tool_name` 键 → R2
- [ ] 9. HTML 用 `data-i18n="key"`，placeholder 用 `data-i18n-placeholder="key"` → R2
- [ ] 10. `window._translations = translations;` 暴露翻译对象
- [ ] 11. `t()` 函数用 `WebToolbox.getCurrentLang()`，禁止自定义 currentLang
- [ ] 12. 禁止手写语言切换器 → R0

### SEO
- [ ] 13. Head Meta 齐全（title/desc/keywords/robots/canonical/hreflang/OG/Twitter） → R3
- [ ] 14. JSON-LD 四件套（WebApplication/BreadcrumbList/HowTo/FAQPage） → R4
- [ ] 15. 痛点关键词 6 层埋词 → R6

### 页面区块
- [ ] 16. Trust Bar（4 项文案键）→ R7
- [ ] 17. features-section（4 卡，首卡 "100% Free & Private"）→ R5 R9
- [ ] 18. faq-section（≥5 问答，末条 faq_free_q/a，禁止手写 onclick）→ R8
- [ ] 19. related-tools（3-5 内链，样式由 common.css 控制）→ R0 R5

### 集成
- [ ] 20. 截图：`cwebp -q 80 screenshot.png -o screenshots/xxx.webp` → R12
- [ ] 21. index.html 添加工具卡片 + JSON-LD hasPart → R11
- [ ] 22. sitemap.xml + ROADMAP.md + 分类页 → R11

---

## 规则详解

> 以下为 AGENTS.md 各规则的完整实现细节与代码示例

### R0) 公共结构详解

**Header（common.js 自动注入，禁止手写）：**
- 面包屑导航（左）：
  - 工具页（4 级）：`Home › Web Toolbox › {Category} › {ToolName}`
  - 分类页（3 级）：`Home › Web Toolbox › {CategoryName}`（末项不可点击）
- 面包屑中的 Home、Web Toolbox、Category 由 common.js 内置 `COMMON_I18N` 提供 4 语翻译
- 面包屑最后一项（工具名/分类名）使用 `data-i18n="tool_name"` 自动翻译
- 语言切换器（右）：4 语下拉菜单
- 主题切换按钮（右，默认隐藏）：仅当 `data-show-theme-toggle="true"` 时显示
- 禁止在 HTML 中手写 `<nav>` 返回链接、`lang-dropdown`、`lang-switcher`、`theme-toggle` 等元素
- 禁止在 JS 中手写 `langDropdown`、`langCurrent`、`themeToggle` 相关事件绑定

**Footer（common.js 自动注入，禁止手写）：**
- 工具页：类目导航栏（`category-nav`）+ 版权行（`site-footer`）
- 分类页（`data-page-type="category"`）：仅版权行（跳过类目导航）
- 版权文案：`© 2024-2026 heyuan110.com`，由 `COMMON_I18N` 提供 4 语翻译
- 禁止在 HTML 中手写 `<footer>` 或版权信息

**Related Tools（工具自写 HTML，样式 common.css 控制）：**
- 固定结构：`.related-tools` > `h3` + `.related-grid` > `.related-card`（`<a>` 标签）
- 每张卡片内部：`<div>`（emoji 图标）+ `<h4>`（工具名）+ `<p>`（描述）
- 3-5 个相关工具内链，内容因工具而异
- common.css 已处理深色/浅色主题下的字体颜色、背景、hover 效果
- 禁止对 `.related-card`、`h4`、`p` 添加任何 inline style

**FAQ 手风琴交互（common.js 自动绑定）：**
- common.js 的 `bindFaqAccordion()` 自动绑定 `.faq-question` 点击事件
- 工具只需按 `.faq-item` > `.faq-question` + 答案内容结构编写 HTML
- 禁止在工具 JS 中手写 FAQ 展开/收起逻辑

**Container 对齐规则：**
- `.container` 必须 `max-width: 1200px; padding: 40px;`
- 与 header 的 `bc-nav`（`max-width: 1200px; padding: 12px 40px`）左右对齐
- 所有内容区块（features、faq、related-tools）必须在 `.container` 内部

**工具页集成（固定模式）：**
```html
<link rel="stylesheet" href="common/common.css">
</head>
<body>
<div class="container">
  <!-- 工具主体内容 -->
  <!-- trust-bar -->
  <!-- features-section -->
  <!-- faq-section -->
  <!-- related-tools -->
</div>
<script>/* 工具 IIFE，翻译对象暴露到 window._translations */</script>
<script src="common/common.js"
  data-tool-id="{tool-id}"
  data-tool-name="{Tool Name}"
  data-category="{category}"></script>
<script>WebToolbox.init(window._translations);</script>
</body>
```

**分类页集成（固定模式）：**
```html
<link rel="stylesheet" href="../common/common.css">
</head>
<body>
<div class="container">
  <!-- 分类页内容（hero、tools-grid、features、faq、related-tools） -->
</div>
<script>/* 分类页 IIFE，翻译对象暴露到 window._translations */</script>
<script src="../common/common.js"
  data-page-type="category"
  data-show-theme-toggle="true"
  data-category="{category}"
  data-tool-name="{Category Name}"></script>
<script>WebToolbox.init(window._translations);</script>
</body>
```
> 分类页在 `category/` 子目录，引用 common 资源需加 `../` 前缀。

**翻译对象暴露规则：**
- 翻译定义在 IIFE 内部时，必须通过 `window._translations = translations;` 暴露
- 工具内部 `t()` 函数使用 `WebToolbox.getCurrentLang()` 获取当前语言，禁止自定义 `currentLang` 变量

**工具翻译 `tool_name` 键：**
- 每个工具的 4 语言翻译对象中必须包含 `tool_name` 键，用于面包屑工具名的多语言显示
- `tool_name` 值为工具短名称（不含副标题/营销语），如：`'File Converter'` / `'文件格式转换'`
- `data-tool-name` 属性值作为英文默认值，`tool_name` 提供各语言翻译覆盖

### R1) 页面基础要求

- 默认深色主题（夜晚模式），支持浅色/深色切换（通过 `data-show-theme-toggle="true"` 启用切换按钮），响应式设计（桌面/平板/手机）。
- JavaScript 必须使用 IIFE 或等价作用域隔离，避免全局污染。
- 新增/重构工具默认采用 **shadcn/ui 视觉语言**（卡片、边框、层次、间距、控件风格一致）。
- 关键交互区必须包含**有意义的动效设计**（至少 2 类）：如首屏入场动画 + 状态反馈动画（进度、切换、完成反馈），做到"第一眼有吸引力、交互时有反馈"，禁止纯静态工具页。
- UI/UX 必须同时满足"**美观有质感** + **首次使用可直觉完成**"：核心流程应步骤清晰（推荐 1-2-3），主操作按钮突出，参数输入必须有明确标签/含义（禁止只放裸数字输入框让用户猜）。

**CSS 基础（强制，每个工具页必须包含）：**
- `* { margin: 0; padding: 0; box-sizing: border-box; }` — 全局 reset，**禁止遗漏 `box-sizing`**
- `body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #e0e0e0; min-height: 100vh; }` — common.css **不提供** body 背景
- `.container { max-width: 1200px; margin: 0 auto; padding: 40px; }` — common.css **不提供** container 布局

**common.css 样式职责边界（重要）：**
- common.css **提供**：面包屑、语言切换器、主题按钮、类目导航、版权页脚、Trust Bar、Related Tools、入场动画
- common.css **不提供**（必须在工具页 `<style>` 中自行定义）：body 背景、container 布局、features-section / features-grid / feature-card、faq-section / faq-item / faq-question / faq-answer

### R2) 多语言（4 语）

每个工具必须支持：`en`、`zh-CN`、`fr`、`es`。

**工具翻译职责：**
- 文本元素：`data-i18n="key"` → common.js 的 `applyTranslations()` 自动替换 innerHTML
- placeholder：`data-i18n-placeholder="key"` → 自动替换 placeholder 属性
- 翻译对象必须包含 `tool_name` 键（详见 R0）
- 默认语言：English (`en`)

**由 common.js 统管（禁止手写）：**
- 语言切换器 UI 及交互事件
- `localStorage` 键名 `toolbox_lang` 的读写
- 公共 UI 翻译（面包屑、类目导航、版权）通过 `COMMON_I18N` 内置
- 语言检测与旧键名迁移

### R3) SEO Head

每个工具页必须包含完整 SEO 头部标签：

- `title` / `description` / `keywords` / `author`
- `robots` / `googlebot` / `bingbot`
- `revisit-after` / `rating` / `distribution` / `language`
- `canonical`
- `alternate hreflang`：`en`、`zh-CN`、`fr`、`es`、`x-default`
- Open Graph 全套
- Twitter Card 全套

### R4) JSON-LD（4 种）

必须同时包含：

1. `WebApplication`（必须含 `alternateName`、`publisher`、`featureList`、`screenshot`）
2. `BreadcrumbList`（3 级）
3. `HowTo`（3 步）
4. `FAQPage`（至少 5 个问答）

### R5) 页面可见 SEO 区块

在主体功能区后，必须有（均在 `.container` 内部）：

1. `features-section`（4 张卡，grid，自适应）
2. `faq-section`（≥5 问答，手风琴交互由 common.js 自动绑定）
3. `related-tools`（3-5 个相关工具内链）

### R6) 痛点关键词埋词

必须围绕用户痛点埋词：`No Ads`、`No Signup/No Login`、`No Watermark`、`No Upload`、`browser-based`、`free unlimited` 等。

必须覆盖 6 层位置：

1. `<title>`（含 `No Ads` + 核心卖点）
2. `meta description`
3. `meta keywords`
4. JSON-LD `WebApplication.featureList`
5. `og:title` 与 `twitter:title`
6. 页面可见内容（features + FAQ）

### R7) Trust Bar

功能区与 features 之间必须有 Trust Bar，使用 common.css 类名 `.trust-bar` > `.trust-item`。

包含 4 项文案键：`trust_users`、`trust_rating`、`trust_privacy`、`trust_free`

### R8) FAQ 深度与热词

- HTML 结构：`.faq-item` > `.faq-question`（按钮）+ 答案容器，手风琴交互由 common.js 自动绑定
- 每条 FAQ 答案必须有解释深度（建议 3-8 句），不能是空泛一句话
- 至少 1 条 FAQ 必须是基础科普（What is X / X 是什么，有什么用）
- FAQ 与 JSON-LD FAQPage 必须语义一致
- FAQ 文案必须自然包含 Google 热词，禁止机械堆砌
- FAQ 最后一条必须是免费隐私问答，键名固定：`faq_free_q` / `faq_free_a`

### R9) 免费隐私卖点卡

features 第一张卡必须是"100% Free & Private"卖点（含无广告、无需注册、本地处理等核心信息），4 语言翻译。

### R10) 合规禁止项

- 禁止在 JSON-LD 中伪造 `aggregateRating`
- Trust Bar 仅作页面可见信任元素，不写入结构化评分数据

### R11) 上线集成

每个新工具上线必须同步更新：

1. `index.html` 工具卡片
2. `index.html` JSON-LD `hasPart`
3. 对应分类页 `category/xxx-tools.html`（添加工具卡片到该分类）
4. `sitemap.xml`
5. `docs/ROADMAP.md`
6. `screenshots/{tool}.webp`

### R12) 截图规范

- 截图必须为 `webp`，文件名与工具文件名一致
- 转换命令：`cwebp -q 80 screenshot.png -o screenshots/xxx.webp`

### R13) 浅色主题 CSS

启用主题切换后（`data-show-theme-toggle="true"`），工具页必须提供完整的浅色主题覆写。

**选择器规则（关键）：**
- common.js 将 `data-theme="light"` 设置在 `<body>` 元素上
- body 自身的样式必须用 `body[data-theme="light"]`（属性在 body 上，不能用后代选择器）
- 其他元素用 `[data-theme="light"] .class-name`（标准后代选择器）

**必须覆写的组件清单：**
1. `body` — 背景色 `#fafafa`、文字色 `#09090b`
2. 工具主体区域 — 所有自定义卡片、输入框、按钮
3. 工具特有面板 — 背景、边框、文字色
4. `.features-section .feature-card` — 白色背景 `#ffffff`、浅灰边框 `#e4e4e7`
5. `.faq-section` — `.faq-item` 白色背景、`.faq-question` 深色文字
6. 统计卡片、进度条等装饰性组件

**标准配色表（浅色模式）：**
| 用途 | 色值 |
|------|------|
| 页面背景 | `#fafafa` |
| 卡片/面板背景 | `#ffffff` |
| 边框 | `#e4e4e7` |
| 主文字 | `#09090b` |
| 次要文字 | `#71717a` |
| 交互强调色 | `#7c3aed`（保持与深色主题一致） |

---

## 速用片段（复制后改词）

> 规则详情见上方对应 R# 编号

### 痛点埋词 → R6
```html
<title>{Tool Name} - Free Online {Type} | No Ads, No Signup | {中文名} | Web Toolbox</title>
<meta name="description" content="{核心描述}. ✅ No ads ✅ No signup ✅ No limits. Runs entirely in your browser.">
<meta name="keywords" content="{核心关键词},no ads,no signup,no login,no watermark,free unlimited,browser-based,no installation,local processing">
<meta property="og:title" content="{Tool Name} - Free Online {Type} | No Ads, No Signup">
<meta name="twitter:title" content="{Tool Name} - Free Online {Type} | No Ads, No Signup">
```

### featureList → R4 R6
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

### Trust Bar → R7
```html
<div class="trust-bar">
  <span class="trust-item" data-i18n="trust_users">🌍 Used by 50,000+ users</span>
  <span class="trust-item" data-i18n="trust_rating">⭐ 4.9/5 rating</span>
  <span class="trust-item" data-i18n="trust_privacy">🔒 100% Private</span>
  <span class="trust-item" data-i18n="trust_free">🚫 No Ads, No Signup</span>
</div>
```

### FAQ 末条 → R8
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

### FAQ 深度示例 → R8
```text
Q: What is JSON and what is it used for?
A: JSON (JavaScript Object Notation) is a lightweight data format used by modern APIs and web apps. In CSV to JSON workflows, JSON is often used as API-ready structured payload.
```

---

## HTML 完整模板

> 语言切换器、FAQ 手风琴交互、header/footer 均由 common.js 自动注入，**禁止手写**。
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

        /* ========== 浅色主题覆写 ========== */
        /* 注意：data-theme 属性在 <body> 上，body 自身样式用 body[data-theme="light"] */
        body[data-theme="light"] { background: #fafafa !important; color: #09090b; }

        /* 工具主体 */
        [data-theme="light"] .container { color: #09090b; }

        /* Features */
        [data-theme="light"] .features-section h2 { color: #09090b; }
        [data-theme="light"] .feature-card { background: #ffffff; border-color: #e4e4e7; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        [data-theme="light"] .feature-card:hover { border-color: #d4d4d8; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        [data-theme="light"] .feature-card h3 { color: #09090b; }
        [data-theme="light"] .feature-card p { color: #71717a; }

        /* FAQ */
        [data-theme="light"] .faq-section h2 { color: #09090b; }
        [data-theme="light"] .faq-item { background: #ffffff; border-color: #e4e4e7; }
        [data-theme="light"] .faq-question { color: #09090b; }
        [data-theme="light"] .faq-answer p { color: #71717a; }

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
| box-sizing | **`border-box`（全局 `*` 必须设置，禁止遗漏）** |
| common.css 不提供 | body 背景、container、features-grid/card、faq-section/item |
| 浅色主题 body 选择器 | **`body[data-theme="light"]`**（不是 `[data-theme="light"] body`） |
| 浅色主题页面背景 | `#fafafa` |
| 浅色主题卡片背景 | `#ffffff` |
| 浅色主题边框 | `#e4e4e7` |
| 浅色主题主文字 | `#09090b` |
| 浅色主题次文字 | `#71717a` |
