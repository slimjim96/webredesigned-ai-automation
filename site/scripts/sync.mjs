// Copy the design system and logo files into public/ before every dev or build run.
// They are edited only in their stages (03_design-system, 02_brand); public/ copies are gitignored.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const STAGES = path.resolve(ROOT, '../stages');
const DS = path.join(STAGES, '03_design-system/output');
const LOGO = path.join(STAGES, '02_brand/output/logo');
const PUB = path.join(ROOT, 'public');

function copy(from, to) {
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
}

copy(path.join(DS, 'tokens.css'), path.join(PUB, 'css/tokens.css'));
copy(path.join(DS, 'components.css'), path.join(PUB, 'css/components.css'));
for (const f of fs.readdirSync(path.join(DS, 'fonts'))) copy(path.join(DS, 'fonts', f), path.join(PUB, 'css/fonts', f));

for (const f of fs.readdirSync(LOGO)) if (f.endsWith('.svg') && f !== 'favicon.svg') copy(path.join(LOGO, f), path.join(PUB, 'logo', f));
for (const f of ['technehora-mark-512.png', 'technehora-mark-1024.png']) copy(path.join(LOGO, 'png', f), path.join(PUB, 'logo', f));
copy(path.join(LOGO, 'favicon.svg'), path.join(PUB, 'favicon.svg'));
for (const f of ['favicon-16.png', 'favicon-32.png', 'favicon-48.png', 'apple-touch-icon.png']) copy(path.join(LOGO, 'png', f), path.join(PUB, f));

// favicon.ico for old browsers and crawlers that ask for it by name: an ICO may hold PNGs as-is.
const sizes = [16, 32, 48];
const pngs = sizes.map((s) => fs.readFileSync(path.join(LOGO, 'png', `favicon-${s}.png`)));
const header = Buffer.alloc(6 + 16 * pngs.length);
header.writeUInt16LE(0, 0); header.writeUInt16LE(1, 2); header.writeUInt16LE(pngs.length, 4);
let offset = header.length;
pngs.forEach((png, i) => {
  const e = 6 + 16 * i;
  header.writeUInt8(sizes[i], e); header.writeUInt8(sizes[i], e + 1);
  header.writeUInt16LE(1, e + 4); header.writeUInt16LE(32, e + 6);
  header.writeUInt32LE(png.length, e + 8); header.writeUInt32LE(offset, e + 12);
  offset += png.length;
});
fs.writeFileSync(path.join(PUB, 'favicon.ico'), Buffer.concat([header, ...pngs]));

console.log('synced design system and logos into public/');
