import { chromium } from 'playwright';

const URL = 'http://localhost:3000';
const SIZES = [
  { name: 'mobile-390', width: 390, height: 844 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'desktop-1440', width: 1440, height: 900 },
];

async function run() {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (err) => consoleErrors.push(`PAGE ERROR: ${err.message}`));

  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2200);

  const rootHtml = await page.evaluate(() => {
    const r = document.getElementById('root');
    return r ? r.innerHTML.slice(0, 420) : null;
  });
  console.log('ROOT PRESENT:', !!rootHtml, '| sample:', rootHtml ? rootHtml.replace(/\s+/g, ' ').slice(0, 240) : 'none');

  const imgs = await page.evaluate(() => {
    return [...document.querySelectorAll('img')].map((img) => ({
      src: img.currentSrc,
      alt: img.getAttribute('alt'),
      naturalWidth: img.naturalWidth,
      naturalHeight: img.naturalHeight,
    }));
  });
  const broken = imgs.filter((i) => (i.naturalWidth === 0 || i.naturalHeight === 0) && i.src && !i.src.includes('data:'));
  const missingAlt = imgs.filter((i) => !i.alt && !i.src.includes('data:') && i.src);
  console.log('IMAGES:', imgs.length, '| BROKEN(natural dims 0, no data:):', broken.length, broken.map(b => b.src));
  console.log('MISSING ALT:', missingAlt.length, missingAlt.map(a => a.src));

  for (const size of SIZES) {
    const view = await browser.newContext({ viewport: { width: size.width, height: size.height } });
    const p = await view.newPage();
    await p.goto(URL, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1200);
    const safe = size.name.replace(/[^a-z0-9]/gi, '_');
    await p.screenshot({ path: `screenshot-${safe}.png`, fullPage: true });
    console.log(`screenshot ${size.name} -> screenshot-${safe}.png`);
  }

  console.log('CONSOLE ERRORS:', consoleErrors.length ? consoleErrors : 'none');

  await browser.close();
}

run().catch((e) => { console.error(e); process.exit(1); });
