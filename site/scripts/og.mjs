// Social share images (1200×630), one per page: the mark, the page's headline, and the name.
// Needs Google Chrome; run by hand after copy changes (`node scripts/og.mjs`) and commit public/og/.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const ROOT = path.resolve(import.meta.dirname, '..');
const PAGES = path.resolve(ROOT, '../stages/05_content/output/pages');
const FONTS = path.resolve(ROOT, '../stages/03_design-system/output/fonts');
const MARK = path.resolve(ROOT, '../stages/02_brand/output/logo/technehora-mark.svg');
const OUT = path.join(ROOT, 'public/og');
const CHROME = process.env.CHROME ?? 'google-chrome';

const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const clean = (t) => t.replace(/\*\*|`/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');

fs.mkdirSync(OUT, { recursive: true });
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'th-og-'));
const profile = path.join(tmp, 'profile');
const mark = fs.readFileSync(MARK, 'utf8');

for (const file of fs.readdirSync(PAGES).filter((f) => f.endsWith('.md'))) {
  const slug = file.replace(/\.md$/, '');
  const md = fs.readFileSync(path.join(PAGES, file), 'utf8');
  const name = md.match(/^# (.*)$/m)[1];
  const headline = clean((md.match(/^- \*\*H1(?: \(styled as H2\))?:\*\* (.*)$/m) ?? [, name])[1]);
  const label = slug === 'home' ? 'AI help for local businesses · Rochester, NY' : `${clean(name)} · Techne Hora`;
  const html = `<!doctype html><meta charset="utf-8"><style>
    @font-face { font-family: OGSerif; src: url('file://${FONTS}/IBMPlexSerif-600.woff2'); font-weight: 600; }
    @font-face { font-family: OGMono; src: url('file://${FONTS}/IBMPlexMono-500.woff2'); font-weight: 500; }
    html, body { margin: 0; width: 1200px; height: 630px; background: #FAF7F0; }
    .card { box-sizing: border-box; width: 1200px; height: 630px; padding: 72px 80px; display: grid; grid-template-rows: auto 1fr auto; border-bottom: 16px solid #A63D2A; }
    .mark { width: 104px; height: 104px; }
    h1 { align-self: center; margin: 0; max-width: 980px; font: 600 76px/1.08 OGSerif; color: #1B2A4A; text-wrap: balance; }
    p { margin: 0; font: 500 26px/1 OGMono; letter-spacing: 0.08em; text-transform: uppercase; color: #5C6170; }
  </style><div class="card"><div class="mark">${mark}</div><h1>${esc(headline)}</h1><p>${esc(label)}</p></div>`;
  const page = path.join(tmp, `${slug}.html`);
  fs.writeFileSync(page, html);
  execFileSync(CHROME, ['--headless=new', `--user-data-dir=${profile}`, '--hide-scrollbars', '--force-device-scale-factor=1',
    '--window-size=1200,630', '--virtual-time-budget=2000', `--screenshot=${path.join(OUT, slug + '.png')}`, `file://${page}`], { stdio: 'ignore' });
  console.log(`og/${slug}.png  ${headline}`);
}
fs.rmSync(tmp, { recursive: true, force: true });
