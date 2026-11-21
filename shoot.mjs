// shoot.mjs — maker's tool for NEWS TOWERS: renders scene.html in headless
// Chrome (file:// only) and captures scene.png (2048x1044, transparent) plus
// anchors.json (hero tower front-face rects for the Pillow composite).
// Run: node shoot.mjs
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const require = createRequire('/home/hatch/workspace/shots-tool/package.json');
const puppeteer = require('puppeteer');
const here = fileURLToPath(new URL('.', import.meta.url));

const browser = await puppeteer.launch({
  args: ['--no-sandbox', '--use-gl=swiftshader', '--enable-unsafe-swiftshader'],
});
const page = await browser.newPage();
await page.setViewport({ width: 2048, height: 1044 });
page.on('pageerror', e => console.log('PAGEERROR:', e.message));
await page.goto('file://' + here + 'scene.html');
await page.waitForFunction('window.__done === true', { timeout: 30000 });
const anchors = await page.evaluate('window.__anchors');
writeFileSync(here + 'anchors.json', JSON.stringify(anchors, null, 1));
await page.screenshot({ path: here + 'scene.png', omitBackground: true });
await browser.close();
console.log('SCENE SHOT OK — anchors for', Object.keys(anchors).length, 'towers');
