// 用无头 Chrome 渲染 HTML 封面 → 1200x630 WebP。逃离 AI 生图的"无字/无厘头"困境。
// 用法: node render-cover.mjs '<json-spec>'  或  node render-cover.mjs --file spec.json
import fs from 'node:fs';
import path from 'node:path';
// Resolve puppeteer-core from the newest installed chrome-devtools-mcp plugin (version dir changes on upgrade)
const PLUGIN_DIR = '/Users/bruce/.claude/plugins/cache/claude-plugins-official/chrome-devtools-mcp';
const PUPPETEER = fs.readdirSync(PLUGIN_DIR)
  .filter(v => /^\d+\.\d+\.\d+$/.test(v))
  .sort((a, b) => b.localeCompare(a, undefined, { numeric: true }))
  .map(v => path.join(PLUGIN_DIR, v, 'node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js'))
  .find(p => fs.existsSync(p));
if (!PUPPETEER) throw new Error('puppeteer-core not found under ' + PLUGIN_DIR);
const puppeteer = (await import(PUPPETEER)).default;

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const arg = process.argv[2];
const spec = arg === '--file' ? JSON.parse(fs.readFileSync(process.argv[3], 'utf8')) : JSON.parse(arg);
// spec: [{output, tag, kicker, title, sub, accent, motif}]
const items = Array.isArray(spec) ? spec : [spec];

function html({ tag, kicker, title, sub, accent = '#2dd4bf', motif = '' }) {
  return `<!doctype html><html><head><meta charset="utf8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1200px;height:630px;overflow:hidden}
  body{font-family:"SF Pro Display","PingFang SC","Helvetica Neue",Arial,sans-serif;
    background:radial-gradient(120% 130% at 12% 8%, #16203a 0%, #0b1020 55%, #070a14 100%);
    color:#fff;position:relative}
  .grid{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);
    background-size:26px 26px;mask-image:linear-gradient(120deg,#000,transparent 70%)}
  .glow{position:absolute;width:620px;height:620px;right:-160px;top:-160px;border-radius:50%;
    background:radial-gradient(circle, ${accent}44 0%, transparent 62%);filter:blur(8px)}
  .motif{position:absolute;right:64px;top:50%;transform:translateY(-50%);font-size:300px;line-height:1;
    color:${accent};opacity:.13;font-weight:800}
  .wrap{position:absolute;inset:0;padding:74px 80px;display:flex;flex-direction:column;justify-content:center}
  .tag{display:inline-flex;align-items:center;gap:8px;align-self:flex-start;
    font:600 20px/1 "SF Mono",Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;
    color:${accent};border:1.5px solid ${accent}66;background:${accent}14;padding:9px 16px;border-radius:999px}
  .kicker{margin-top:30px;font-size:26px;font-weight:600;color:#93a3c4;letter-spacing:.01em}
  .title{margin-top:14px;font-size:76px;font-weight:800;line-height:1.05;letter-spacing:-.02em;max-width:880px;
    background:linear-gradient(180deg,#fff 60%,#c7d2e8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .sub{margin-top:26px;font-size:30px;font-weight:500;color:#aab6d0;max-width:820px;line-height:1.35}
  .bar{position:absolute;left:80px;bottom:70px;width:56px;height:5px;border-radius:3px;background:${accent}}
  .foot{position:absolute;left:150px;bottom:60px;font:500 22px/1 "SF Mono",Menlo,monospace;color:#7c88a8}
  .foot b{color:#c7d2e8;font-weight:600}
  </style></head><body>
  <div class="grid"></div><div class="glow"></div>
  <div class="motif">${motif}</div>
  <div class="wrap">
    <span class="tag">${tag}</span>
    ${kicker ? `<div class="kicker">${kicker}</div>` : ''}
    <h1 class="title">${title}</h1>
    ${sub ? `<div class="sub">${sub}</div>` : ''}
  </div>
  <div class="bar"></div><div class="foot"><b>Bruce's Blog</b> · www.heyuan110.com</div>
  </body></html>`;
}

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true,
  args: ['--force-device-scale-factor=2', '--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 2 });
for (const it of items) {
  await page.setContent(html(it), { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 400)); // let fonts settle
  const png = it.output.replace(/\.webp$/, '.png');
  await page.screenshot({ path: png, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  // PNG(2x) → WebP 1200x630 via Pillow (可靠,sips 不支持 webp)
  const { execSync } = await import('node:child_process');
  const conv = new URL('./convert-to-webp.py', import.meta.url).pathname;
  execSync(`python3 "${conv}" --input "${png}" --output "${it.output}" --resize 1200x630 >/dev/null 2>&1 && rm -f "${png}"`);
  console.log('✓', it.output, fs.statSync(it.output).size / 1024 | 0, 'KB');
}
await browser.close();
