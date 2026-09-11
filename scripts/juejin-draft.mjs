// 掘金半自动填稿:连用户已登录的 Chrome(9222),打开编辑器自动填标题+正文存草稿。
// 用法: node scripts/juejin-draft.mjs <spec.json>
// spec.json: [{"title": "...", "body": "markdown 正文"}]
// 只填稿不发布——用户在 https://juejin.cn/creator/content/article/drafts 里补标签后手动点发布。
import puppeteer from '/Users/bruce/.claude/plugins/cache/claude-plugins-official/chrome-devtools-mcp/1.5.0/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import fs from 'node:fs';

const specs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222', defaultViewport: null });

for (const [i, spec] of specs.entries()) {
  const page = await browser.newPage();
  await page.goto('https://juejin.cn/editor/drafts/new?v=2', { waitUntil: 'networkidle2', timeout: 45000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 3000));

  // 标题输入框
  const titleSel = 'input.title-input, input[placeholder*="标题"], .title-input input';
  await page.waitForSelector(titleSel, { timeout: 15000 });
  await page.click(titleSel);
  await page.keyboard.type(spec.title, { delay: 30 });

  // 正文:bytemd/CodeMirror 编辑区
  const bodySel = '.bytemd-editor .CodeMirror, .CodeMirror';
  await page.waitForSelector(bodySel, { timeout: 15000 });
  await page.click(bodySel);
  await new Promise(r => setTimeout(r, 500));
  // 逐行敲入(markdown 编辑器对粘贴事件支持不一,键入最稳)
  for (const line of spec.body.split('\n')) {
    await page.keyboard.type(line, { delay: 8 });
    await page.keyboard.press('Enter');
  }

  await new Promise(r => setTimeout(r, 4000)); // 等自动保存
  console.log(`✓ [${i + 1}/${specs.length}] 草稿已填:${spec.title}(URL: ${page.url()})`);
  // 不关 tab,留给用户直接检查
}
browser.disconnect();
console.log('全部完成 → 打开 https://juejin.cn/creator/content/article/drafts 补标签并发布');
