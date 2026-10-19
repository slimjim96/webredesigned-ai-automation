// After `astro build`: every internal link and image resolves, every page has a unique title and a description,
// and no copy marker reached the HTML. `LAUNCH=1` also fails on launch blockers (the placeholder phone number).
import fs from 'node:fs';
import path from 'node:path';

const DIST = path.resolve(import.meta.dirname, '../dist');
const launch = process.env.LAUNCH === '1';
const errors = [];
const warnings = [];

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]));
}
// How Cloudflare Pages resolves a path: the file itself, <path>.html, or <path>/index.html.
function exists(url) {
  const p = decodeURIComponent(url.split(/[?#]/)[0]);
  const base = path.join(DIST, p);
  return [base, base + '.html', path.join(base, 'index.html')].some((f) => fs.existsSync(f) && fs.statSync(f).isFile());
}

const pages = walk(DIST).filter((f) => f.endsWith('.html'));
const titles = new Map();
for (const file of pages) {
  const rel = path.relative(DIST, file);
  const html = fs.readFileSync(file, 'utf8');
  const title = html.match(/<title>([^<]*)<\/title>/)?.[1];
  if (!title) errors.push(`${rel}: no <title>`);
  else if (titles.has(title)) errors.push(`${rel}: same title as ${titles.get(title)}`);
  else titles.set(title, rel);
  if (!/<meta name="description" content="[^"]+"/.test(html)) errors.push(`${rel}: no meta description`);
  if ((html.match(/<h1[\s>]/g) ?? []).length !== 1) errors.push(`${rel}: needs exactly one <h1>`);
  if (/\[\[|\]\]/.test(html.replace(/<script[\s\S]*?<\/script>/g, ''))) errors.push(`${rel}: a [[…]] marker reached the page`);
  for (const [, attr, url] of html.matchAll(/\s(href|src|srcset)="(\/[^"]*)"/g)) {
    if (url.startsWith('//')) continue;
    if (!exists(url)) errors.push(`${rel}: ${attr} ${url} goes nowhere`);
  }
  for (const [, id] of html.matchAll(/href="#([^"]+)"/g)) {
    if (!html.includes(`id="${id}"`)) errors.push(`${rel}: #${id} has no target on the page`);
  }
  if (html.includes('555-01')) (launch ? errors : warnings).push(`${rel}: placeholder phone number (585) 555-0100`);
}

const unique = (a) => [...new Set(a)];
for (const w of unique(warnings.map((w) => w.split(': ').slice(1).join(': ')))) {
  console.warn(`warning: ${w} on ${warnings.filter((x) => x.endsWith(w)).length} pages (replace before launch)`);
}
if (errors.length) {
  console.error(errors.map((e) => `error: ${e}`).join('\n'));
  console.error(`\n${errors.length} problem(s) in ${pages.length} pages.`);
  process.exit(1);
}
console.log(`ok: ${pages.length} pages, every link and image resolves, no markers left.`);
