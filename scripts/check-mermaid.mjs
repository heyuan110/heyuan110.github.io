// 用站点自带的 mermaid.min.js 验证所有文章的 mermaid 块语法
import puppeteer from '/Users/bruce/.claude/plugins/cache/claude-plugins-official/chrome-devtools-mcp/1.5.0/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = '/Users/bruce/heyuan110.github.io';
const DIRS = fs.readdirSync(path.join(ROOT, 'content/posts/ai'))
  .filter(d => !d.startsWith("."));

// 提取 (file, index, code)
const blocks = [];
for (const d of DIRS) {
  for (const f of ['index.md', 'index.zh.md']) {
    const p = path.join(ROOT, 'content/posts/ai', d, f);
    if (!fs.existsSync(p)) continue;
    const src = fs.readFileSync(p, 'utf8');
    const re = /```mermaid\n([\s\S]*?)```/g;
    let m, i = 0;
    while ((m = re.exec(src))) blocks.push({ file: `${d}/${f}`, idx: i++, code: m[1] });
  }
}
console.error(`checking ${blocks.length} mermaid blocks from ${DIRS.length} dirs...`);

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage();
const mermaidJs = fs.readFileSync(path.join(ROOT, 'static/js/mermaid.min.js'), 'utf8');
await page.setContent('<html><body></body></html>');
await page.evaluate(mermaidJs);
await page.evaluate(() => mermaid.initialize({ startOnLoad: false }));

const bad = [];
for (const b of blocks) {
  const r = await page.evaluate(async (code) => {
    try { await mermaid.parse(code); return null; }
    catch (e) { return String(e.message || e).slice(0, 200); }
  }, b.code);
  if (r) { bad.push({ ...b, err: r }); console.log(`❌ ${b.file} [块${b.idx}]: ${r.replace(/\n/g, ' ⏎ ')}`); }
}
console.log(bad.length ? `\n${bad.length} broken` : '\n✅ all blocks parse OK');
await browser.close();
