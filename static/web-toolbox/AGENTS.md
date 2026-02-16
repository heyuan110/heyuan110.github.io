# AGENTS.md

Web Toolbox 规范性规则文档，适用于 Claude Code 和 Codex。

## 文档体系

| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `AGENTS.md` | 规则索引与核心约束 | 每次对话自动加载 |
| `docs/TOOL-GUIDE.md` | 完整开发指南（规则详解 + 模板 + 代码片段） | 新建/修改工具时读取 |
| `docs/ROADMAP.md` | 项目规划与进度 | 查看进度时读取 |

若冲突：`AGENTS.md` > `docs/TOOL-GUIDE.md`

## 协作规范

- 中文沟通，Git 分支 `code`，推送触发部署，commit message 中文简洁
- 品牌：**魔法工具箱** (Magic Toolbox)
- Slogan：免安装、即开即用的在线工具箱 / No install. Just use.

## 项目范围

- 站点：`https://www.heyuan110.com/web-toolbox/`
- 纯前端 HTML/CSS/JS，无后端
- 工具页：`xxx.html`（简单）或 `xxx/index.html` + `style.css` + `app.js`（复杂）
- 分类页：`category/xxx-tools.html`（6 个分类）
- 公共资源：`common/common.js` + `common/common.css`
- 首页：`index.html`

## 强制规则

### R-1) common 目录保护（最高优先级）

`common/` 影响全站 60+ 页面，**日常工具开发中禁止修改**。
- 特殊样式 → 工具页自身 CSS 覆写
- 发现 bug → 必须先与用户确认，修改后回归验证 3+ 不同类目工具页
- 允许场景：用户明确要求 / 全站统一重构 / 全站公共 bug

### R0) 公共结构（common.js 统管）

common.js 自动注入：面包屑、语言切换器、主题按钮、类目导航、版权页脚、FAQ 手风琴交互。
- **禁止手写**：导航链接、`lang-dropdown`、`theme-toggle`、`<footer>`、FAQ `onclick`
- **工具自写**：related-tools HTML（样式 common.css 控制，禁止 inline style）
- **Container**：`max-width:1200px; padding:40px`，所有可见区块在 `.container` 内
- **翻译**：`window._translations` 暴露，`WebToolbox.getCurrentLang()` 获取语言，必须含 `tool_name` 键
- **集成代码与详细结构**：见 `docs/TOOL-GUIDE.md`

### R1–R13) 工具开发规则

> 每条规则的详细要求、CSS 代码与模板见 `docs/TOOL-GUIDE.md`

| # | 规则 | 要点 |
|---|------|------|
| 1 | 页面基础 | 深色主题 + 响应式 + IIFE + shadcn/ui + ≥2 类动效 |
| 2 | 多语言 | 4 语（en/zh-CN/fr/es），`data-i18n` 属性标记 |
| 3 | SEO Head | title/desc/keywords/robots/canonical/hreflang/OG/Twitter |
| 4 | JSON-LD | WebApplication + BreadcrumbList + HowTo + FAQPage |
| 5 | 页面区块 | features(4卡) + faq(≥5问) + related-tools(3-5链) |
| 6 | 痛点埋词 | No Ads/Signup/Watermark 等覆盖 6 层位置 |
| 7 | Trust Bar | 功能区与 features 之间，4 项信任文案 |
| 8 | FAQ 深度 | 3-8 句/条 + 科普 + 热词 + 末条 faq_free_q/a |
| 9 | 首卡 | features 第一张 = "100% Free & Private" |
| 10 | 合规 | 禁止伪造 aggregateRating |
| 11 | 上线集成 | index.html 卡片+hasPart + 分类页 + sitemap + ROADMAP |
| 12 | 截图 | webp 格式，文件名与工具一致 |
| 13 | 浅色主题 | `body[data-theme="light"]` 选择器，完整覆写 |

## 验收清单

- [ ] 无手写 header/footer/语言切换器/FAQ onclick
- [ ] container 1200px/40px，related-tools 无 inline style
- [ ] 翻译 4 语完整，含 `tool_name` 键
- [ ] SEO Head 齐全 + JSON-LD 四件套
- [ ] features + faq + related-tools 三区块齐全
- [ ] Trust Bar + 首卡 Free & Private + faq_free_q/a
- [ ] 痛点关键词 6 层埋词
- [ ] CSS: `* { box-sizing: border-box }` + body 渐变 + container
- [ ] 浅色主题覆写完整（如启用）
- [ ] index.html + sitemap + ROADMAP + 截图 webp 已更新
