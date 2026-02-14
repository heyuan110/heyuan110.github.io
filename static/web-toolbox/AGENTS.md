# AGENTS.md

本文件是 **Web Toolbox 的规范性规则文档**，适用于所有 AI Agent（Claude Code、Codex、Gemini CLI、Cursor、Copilot、Cline 等）。

## 文档分层（重要）

- `AGENTS.md`：只放**规则、约束、验收标准**（What & Must）。
- `docs/TOOL-TEMPLATE.md`：放**实现模板、代码片段、操作步骤**（How）。
- `docs/ROADMAP.md`：放**规划与进度**（When & Status）。

若文档冲突：`AGENTS.md` > `docs/TOOL-TEMPLATE.md` > 其他文档。

## 协作规范

- 默认使用中文沟通。
- Git 工作分支为 `code`，推送 `code` 会触发部署。
- commit message 使用中文、简洁描述变更。

## 项目范围

- 站点：`https://www.heyuan110.com/web-toolbox/`
- 技术栈：纯前端 HTML/CSS/JavaScript（无后端）
- 组织方式：
  - 简单工具：`xxx.html`
  - 复杂工具：`xxx/index.html` + `style.css` + `app.js`

## 强制规则

### 0) 公共结构（common.js / common.css 统管，禁止手写）

每个工具页必须引入 `common/common.css` 和 `common/common.js`，由它们统一注入和管理以下公共 UI：

**Header（common.js 自动注入，禁止手写）：**
- 面包屑导航（左）：`Home › Web Toolbox › {Category} › {ToolName}`
- 面包屑中的 Home、Web Toolbox、Category 由 common.js 内置 `COMMON_I18N` 提供 4 语翻译
- 面包屑最后一项（工具名）使用 `data-i18n="tool_name"` 自动翻译，需工具翻译中提供 `tool_name` 键
- 语言切换器（右）：4 语下拉菜单
- 禁止在 HTML 中手写 `<nav>` 返回链接、`lang-dropdown`、`lang-switcher` 等元素
- 禁止在 JS 中手写 `langDropdown`、`langCurrent` 相关事件绑定

**Footer（common.js 自动注入，禁止手写）：**
- 类目导航栏（`category-nav`）：7 类入口，当前类目高亮，标签文案由 `COMMON_I18N` 提供 4 语翻译
- 版权行（`site-footer`）：`© 2024-2026 heyuan110. All rights reserved.`，由 `COMMON_I18N` 提供 4 语翻译
- 禁止在 HTML 中手写 `<footer>` 或版权信息

**Related Tools（各工具自己写 HTML，所有样式来自 common.css，禁止 inline style）：**
- 固定结构：`.related-tools` > `h3` + `.related-grid` > `.related-card`（`<a>` 标签）
- 每张卡片内部：`<div>`（emoji 图标）+ `<h4>`（工具名）+ `<p>`（描述）
- 3-5 个相关工具内链，内容因工具而异
- common.css 已处理深色/浅色主题下的字体颜色、背景、hover 效果
- 禁止对 `.related-card`、`h4`、`p` 添加任何 inline style，统一由 common.css 控制

**FAQ 手风琴交互（common.js 自动绑定，禁止手写）：**
- common.js 的 `bindFaqAccordion()` 自动绑定 `.faq-question` 点击事件
- 工具只需按 `.faq-item` > `.faq-question` + 答案内容结构编写 HTML
- 禁止在工具 JS 中手写 FAQ 展开/收起逻辑

**Container 对齐规则：**
- `.container` 必须 `max-width: 1200px; padding: 40px;`
- 与 header 的 `bc-nav`（`max-width: 1200px; padding: 12px 40px`）左右对齐
- 所有内容区块（features、faq、related-tools）必须在 `.container` 内部

**集成方式（固定模式）：**
```html
<!-- </head> 之前 -->
<link rel="stylesheet" href="common/common.css">
</head>
<body>
<div class="container">
  <!-- 工具主体内容 -->
  <!-- features-section -->
  <!-- faq-section -->
  <!-- related-tools -->
</div>
<!-- 脚本区（在 container 外部） -->
<script>/* 工具 IIFE，翻译对象暴露到 window */</script>
<script src="common/common.js"
  data-tool-id="{tool-id}"
  data-tool-name="{Tool Name}"
  data-category="{category}"></script>
<script>WebToolbox.init(window._translations);</script>
</body>
```

**翻译对象暴露规则：**
- 翻译定义在 IIFE 内部时，必须通过 `window._xxxI18n = translations;` 暴露
- 工具内部 `t()` 函数使用 `WebToolbox.getCurrentLang()` 获取当前语言，禁止自定义 `currentLang` 变量

**工具翻译必须包含 `tool_name` 键（强制）：**
- 每个工具的 4 语言翻译对象中必须包含 `tool_name` 键，用于面包屑工具名的多语言显示
- `tool_name` 值为工具短名称（不含副标题/营销语），如：`'File Converter'` / `'文件格式转换'`
- `data-tool-name` 属性值作为英文默认值，`tool_name` 提供各语言翻译覆盖

### 1) 页面基础要求

- 必须为支持浅色和深色主题、默认是浅色、响应式设计（桌面/平板/手机）。
- JavaScript 必须使用 IIFE 或等价作用域隔离，避免全局污染。
- 新增/重构工具默认采用 **shadcn/ui 视觉语言**（卡片、边框、层次、间距、控件风格一致）。
- 关键交互区必须包含**有意义的动效设计**（至少 2 类）：如首屏入场动画 + 状态反馈动画（进度、切换、完成反馈），做到“第一眼有吸引力、交互时有反馈”，禁止纯静态工具页。
- UI/UX 必须同时满足“**美观有质感** + **首次使用可直觉完成**”：核心流程应步骤清晰（推荐 1-2-3），主操作按钮突出，参数输入必须有明确标签/含义（禁止只放裸数字输入框让用户猜）。

### 2) 多语言（必须 4 语）

每个工具必须支持：`en`、`zh-CN`、`fr`、`es`。

**工具翻译职责（工具开发者负责）：**
- 文本元素：`data-i18n="key"` → common.js 的 `applyTranslations()` 自动替换 innerHTML
- placeholder：`data-i18n-placeholder="key"` → 自动替换 placeholder 属性
- 翻译对象必须包含 `tool_name` 键（详见规则 0）
- 默认语言：English (`en`)

**以下由 common.js 统管（禁止工具手写）：**
- 语言切换器 UI 及交互事件
- `localStorage` 键名 `toolbox_lang` 的读写
- 公共 UI 翻译（面包屑、类目导航、版权）通过 `COMMON_I18N` 内置
- 语言检测与旧键名迁移

### 3) SEO Head（强制）

每个工具页必须包含完整 SEO 头部标签：

- `title` / `description` / `keywords` / `author`
- `robots` / `googlebot` / `bingbot`
- `revisit-after` / `rating` / `distribution` / `language`
- `canonical`
- `alternate hreflang`：`en`、`zh-CN`、`fr`、`es`、`x-default`
- Open Graph 全套
- Twitter Card 全套

### 4) JSON-LD（强制 4 种）

必须同时包含：

1. `WebApplication`（必须含 `alternateName`、`publisher`、`featureList`、`screenshot`）
2. `BreadcrumbList`（3 级）
3. `HowTo`（3 步）
4. `FAQPage`（至少 5 个问答）

### 5) 页面可见 SEO 区块（强制）

在主体功能区后，必须有（均在 `.container` 内部）：

1. `features-section`（4 张卡，grid，自适应）
2. `faq-section`（≥5 问答，手风琴交互由 common.js 自动绑定）
3. `related-tools`（3-5 个相关工具内链，结构与样式详见规则 0 Related Tools）

### 6) 痛点关键词埋词（强制）

必须围绕用户痛点埋词：`No Ads`、`No Signup/No Login`、`No Watermark`、`No Upload`、`browser-based`、`free unlimited` 等。

必须覆盖 6 层位置：

1. `<title>`（含 `No Ads` + 核心卖点）
2. `meta description`
3. `meta keywords`
4. JSON-LD `WebApplication.featureList`
5. `og:title` 与 `twitter:title`
6. 页面可见内容（features + FAQ）

### 7) Trust Bar（强制）

功能区与 features 之间必须有 Trust Bar，使用 common.css 类名 `.trust-bar` > `.trust-item`。

包含 4 项文案键（工具翻译中提供 4 语）：

- `trust_users`
- `trust_rating`
- `trust_privacy`
- `trust_free`

### 8) FAQ 深度与热词（强制）

- HTML 结构：`.faq-item` > `.faq-question`（按钮）+ 答案容器，手风琴交互由 common.js 自动绑定
- 每条 FAQ 答案必须有解释深度（建议 3-8 句），不能是空泛一句话。
- 至少 1 条 FAQ 必须是基础科普（What is X / X 是什么，有什么用）。
- FAQ 与 JSON-LD FAQPage 必须语义一致。
- FAQ 文案必须自然包含 Google 热词，禁止机械堆砌。
- FAQ 最后一条必须是免费隐私问答，键名固定：`faq_free_q` / `faq_free_a`。

### 9) 免费隐私卖点卡（强制）

features 第一张卡必须是“100% Free & Private”卖点（含无广告、无需注册、本地处理等核心信息），并完成 4 语言翻译。

### 10) 合规禁止项

- 禁止在 JSON-LD 中伪造 `aggregateRating`。
- Trust Bar 仅作页面可见信任元素，不写入结构化评分数据。

### 11) 上线集成（强制）

每个新工具上线必须同步更新：

1. `index.html` 工具卡片
2. `index.html` JSON-LD `hasPart`
3. `sitemap.xml`
4. `docs/ROADMAP.md`
5. `screenshots/{tool}.webp`

### 12) 截图规范（强制）

- 截图必须为 `webp`
- 文件名与工具文件名一致
- 推荐使用 `cwebp` 转换

## 最小验收清单（PR/提交前）

- [ ] **公共结构**：无手写 header/footer/语言切换器，全部由 common.js 注入
- [ ] **公共结构**：container `max-width:1200px; padding:40px`，与 header 对齐
- [ ] **公共结构**：related-tools 使用 common.css class（禁止 inline style）
- [ ] **公共结构**：翻译对象包含 `tool_name` 键（4 语），面包屑工具名可翻译
- [ ] 4 语言完整，语言切换与持久化正常（含公共 UI：面包屑、类目导航、版权）
- [ ] SEO Head 标签齐全
- [ ] JSON-LD 四件套齐全
- [ ] features/faq/related 三个可见区块齐全
- [ ] Trust Bar 存在且翻译完整
- [ ] 痛点关键词 6 层埋词完成
- [ ] FAQ 深度、科普、热词、`faq_free_q/a` 完成
- [ ] 首卡为"100% Free & Private"
- [ ] UI/UX 达标：界面美观统一、首次使用路径清晰、核心参数有明确标签与说明
- [ ] `index.html` 卡片与 `hasPart` 已更新
- [ ] `sitemap.xml`、`docs/ROADMAP.md` 已更新
- [ ] 截图为 `screenshots/*.webp`

## 实现参考

- 详细模板与代码片段：`docs/TOOL-TEMPLATE.md`
- 项目进度：`docs/ROADMAP.md`
