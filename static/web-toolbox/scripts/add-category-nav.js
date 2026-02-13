#!/usr/bin/env node
/**
 * 批量为所有工具页面添加类目导航，替换 back-link
 */
const fs = require('fs');
const path = require('path');

const BASE = path.resolve(__dirname, '..');

// 工具 → 类目映射
const CATEGORY_MAP = {
  pdf: ['pdf-merge', 'pdf-split', 'pdf-compress', 'pdf-to-image', 'image-to-pdf', 'pdf-protect', 'e-sign'],
  image: ['image-compressor', 'image-converter', 'image-editor', 'ico-maker', 'id-photo-tool', 'paint-board', 'color-palette', 'qr-code-generator', 'ocr-tool', 'bg-remover', 'watermark-tool'],
  developer: ['json-viewer', 'sqlite-viewer', 'crypto-tools', 'websocket-tester', 'regex-tester', 'ip-lookup', 'whois-query', 'timestamp-converter', 'base64-tool', 'url-encoder', 'csv-json', 'cron-generator', 'api-tester', 'hex-viewer', 'code-formatter', 'yaml-editor'],
  text: ['markdown-editor', 'text-diff', 'word-counter', 'lorem-ipsum', 'chinese-converter'],
  media: ['m3u8-downloader', 'audio-cutter', 'screen-recorder', 'social-video-downloader', 'file-converter'],
  utility: ['calculator', 'unit-converter', 'password-generator', 'world-clock', 'pomodoro', 'page-refresher', 'file-renamer', 'relative-calculator', 'handheld-danmaku', 'metronome', 'invoice-generator', 'claude-history-viewer', 'angel-number', 'numerology']
};

// 反转映射：工具名 → 类目
const TOOL_TO_CAT = {};
for (const [cat, tools] of Object.entries(CATEGORY_MAP)) {
  for (const tool of tools) {
    TOOL_TO_CAT[tool] = cat;
  }
}

// 类目导航 HTML 生成
function genNavHTML(activeCat) {
  const cats = [
    { key: 'home', emoji: '🏠', label: 'Magic ToolBox', href: 'index.html' },
    { key: 'pdf', emoji: '📄', label: 'PDF', href: 'pdf-tools.html' },
    { key: 'image', emoji: '🖼️', label: 'Image', href: 'image-tools.html' },
    { key: 'developer', emoji: '💻', label: 'Dev', href: 'developer-tools.html' },
    { key: 'text', emoji: '📝', label: 'Text', href: 'text-tools.html' },
    { key: 'media', emoji: '🎬', label: 'Media', href: 'media-tools.html' },
    { key: 'utility', emoji: '⚡', label: 'Utility', href: 'utility-tools.html' },
  ];
  const items = cats.map(c => {
    const cls = c.key === activeCat ? ' active' : '';
    return `<a href="${c.href}" class="cat-nav-item${cls}">${c.emoji} ${c.label}</a>`;
  }).join('\n        ');
  return `\n    <!-- 类目导航 -->\n    <nav class="category-nav">\n        ${items}\n    </nav>\n`;
}

// 类目导航 CSS
const NAV_CSS = `
        /* === 类目导航 === */
        .category-nav {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 4px;
            padding: 12px 16px;
            margin: 0 -24px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }
        .cat-nav-item {
            color: #71717a;
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.82rem;
            transition: all 0.2s;
            white-space: nowrap;
        }
        .cat-nav-item:hover {
            color: #c4b5fd;
            background: rgba(124, 58, 237, 0.1);
        }
        .cat-nav-item.active {
            color: #a78bfa;
            background: rgba(124, 58, 237, 0.15);
            font-weight: 600;
        }
        [data-theme="light"] .category-nav {
            border-bottom-color: #e4e4e7;
        }
        [data-theme="light"] .cat-nav-item { color: #71717a; }
        [data-theme="light"] .cat-nav-item:hover {
            color: #7c3aed;
            background: rgba(124, 58, 237, 0.06);
        }
        [data-theme="light"] .cat-nav-item.active {
            color: #7c3aed;
            background: rgba(124, 58, 237, 0.1);
        }
        @media (max-width: 768px) {
            .category-nav { gap: 2px; padding: 8px 8px; margin: 0 -16px 16px; }
            .cat-nav-item { padding: 5px 10px; font-size: 0.78rem; }
        }
`;

// back-link 相关的 HTML 模式（要移除的）
const BACK_LINK_HTML_PATTERNS = [
  // 模式1: <a href="index.html" class="back-link"...>...</a>
  /\s*<a[^>]*class="back-link"[^>]*>[\s\S]*?<\/a>\s*/g,
  // 模式2: <a href="index.html" class="back-home"...>...</a>
  /\s*<a[^>]*class="back-home"[^>]*>[\s\S]*?<\/a>\s*/g,
  // 模式3: <a class="back" href="index.html">...</a>
  /\s*<a[^>]*class="back"[^>]*>[\s\S]*?<\/a>\s*/g,
  // 模式4: <a href="./" class="home-link"...>...</a>
  /\s*<a[^>]*class="home-link"[^>]*>[\s\S]*?<\/a>\s*/g,
  // 注释：<!-- 返回链接 --> 或 <!-- Back link -->
  /\s*<!--\s*返回链接\s*-->\s*/g,
  /\s*<!--\s*Back\s*(to\s*)?link\s*-->\s*/g,
  /\s*<!--\s*返回\s*-->\s*/g,
  /\s*<!--\s*返回首页\s*-->\s*/g,
];

// back-link CSS 模式（要移除的）
const BACK_LINK_CSS_PATTERNS = [
  // .back-link {...} 和 .back-link:hover {...} 和 .back-link svg {...}
  /\s*\/\*[^*]*返回[^*]*\*\/\s*/g,
  /\s*\.back-link\s*\{[^}]*\}\s*/g,
  /\s*\.back-link:hover\s*\{[^}]*\}\s*/g,
  /\s*\.back-link\s+svg\s*\{[^}]*\}\s*/g,
  /\s*\.back-link\s+span\s*\{[^}]*\}\s*/g,
  /\s*\.back-home\s*\{[^}]*\}\s*/g,
  /\s*\.back-home:hover\s*\{[^}]*\}\s*/g,
  /\s*\.back-home\s+svg\s*\{[^}]*\}\s*/g,
  /\s*a\.back\s*\{[^}]*\}\s*/g,
  /\s*\.back\s*\{[^}]*\}\s*/g,
  /\s*\.back:hover\s*\{[^}]*\}\s*/g,
  /\s*\.home-link\s*\{[^}]*\}\s*/g,
  /\s*\.home-link:hover\s*\{[^}]*\}\s*/g,
];

// 排除的文件（首页和分类页不处理）
const EXCLUDE = ['index.html', 'pdf-tools.html', 'image-tools.html', 'developer-tools.html', 'text-tools.html', 'media-tools.html', 'utility-tools.html'];

// 获取所有工具 HTML 文件
function getToolFiles() {
  const files = [];
  // 根目录 .html 文件
  for (const f of fs.readdirSync(BASE)) {
    if (f.endsWith('.html') && !EXCLUDE.includes(f)) {
      files.push({ file: path.join(BASE, f), name: f.replace('.html', '') });
    }
  }
  // 子目录 index.html（如 screen-recorder-app/index.html）
  for (const d of fs.readdirSync(BASE)) {
    const dirPath = path.join(BASE, d);
    if (fs.statSync(dirPath).isDirectory() && !d.startsWith('.') && d !== 'scripts' && d !== 'docs' && d !== 'screenshots') {
      const indexFile = path.join(dirPath, 'index.html');
      if (fs.existsSync(indexFile)) {
        files.push({ file: indexFile, name: d });
      }
    }
  }
  return files;
}

function processFile(filePath, toolName) {
  let html = fs.readFileSync(filePath, 'utf8');
  const category = TOOL_TO_CAT[toolName] || 'utility';

  // 1. 移除 back-link HTML
  for (const pat of BACK_LINK_HTML_PATTERNS) {
    html = html.replace(pat, '\n');
  }

  // 2. 移除 back-link CSS（在 <style> 标签内）
  for (const pat of BACK_LINK_CSS_PATTERNS) {
    html = html.replace(pat, '\n');
  }

  // 3. 清理 media query 中残留的 .back-link 规则
  // 匹配 @media 块中的 .back-link 相关规则
  html = html.replace(/\s*\.back-link\s*\{[^}]*\}\s*/g, '\n');
  html = html.replace(/\s*\.back-home\s*\{[^}]*\}\s*/g, '\n');

  // 4. 检查是否已经有 category-nav（避免重复注入）
  if (html.includes('category-nav')) {
    console.log(`  [跳过] ${toolName} - 已有 category-nav`);
    return;
  }

  // 5. 注入 category-nav CSS（在 </style> 前）
  const styleCloseIdx = html.lastIndexOf('</style>');
  if (styleCloseIdx > -1) {
    html = html.slice(0, styleCloseIdx) + NAV_CSS + '\n    ' + html.slice(styleCloseIdx);
  }

  // 6. 注入 category-nav HTML
  // 策略：在面包屑之前、或 <body> 之后的第一个容器内
  const navHTML = genNavHTML(category);

  // 尝试多种注入位置
  let injected = false;

  // 方案A: 在 breadcrumb 之前注入
  const breadcrumbMatch = html.match(/<nav[^>]*class="breadcrumb[^"]*"[^>]*>/);
  if (breadcrumbMatch && !injected) {
    const idx = html.indexOf(breadcrumbMatch[0]);
    html = html.slice(0, idx) + navHTML + '\n    ' + html.slice(idx);
    injected = true;
  }

  // 方案B: 在 .container 开始标签之后
  if (!injected) {
    const containerMatch = html.match(/<div[^>]*class="container"[^>]*>/);
    if (containerMatch) {
      const idx = html.indexOf(containerMatch[0]) + containerMatch[0].length;
      html = html.slice(0, idx) + navHTML + html.slice(idx);
      injected = true;
    }
  }

  // 方案C: 在 <body> 之后的第一个 div 内
  if (!injected) {
    const bodyIdx = html.indexOf('<body');
    if (bodyIdx > -1) {
      // 找到 <body...> 后的第一个 >
      const bodyCloseIdx = html.indexOf('>', bodyIdx) + 1;
      // 找到下一个开标签
      const nextTagMatch = html.slice(bodyCloseIdx).match(/(<div[^>]*>|<main[^>]*>)/);
      if (nextTagMatch) {
        const insertIdx = bodyCloseIdx + html.slice(bodyCloseIdx).indexOf(nextTagMatch[0]) + nextTagMatch[0].length;
        html = html.slice(0, insertIdx) + navHTML + html.slice(insertIdx);
        injected = true;
      }
    }
  }

  if (!injected) {
    console.log(`  [警告] ${toolName} - 未找到注入位置`);
    return;
  }

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`  [完成] ${toolName} → ${category}`);
}

// 主流程
console.log('=== 批量添加类目导航 ===\n');
const files = getToolFiles();
console.log(`找到 ${files.length} 个工具页面\n`);

let count = 0;
for (const { file, name } of files) {
  processFile(file, name);
  count++;
}

console.log(`\n=== 完成! 处理了 ${count} 个文件 ===`);
