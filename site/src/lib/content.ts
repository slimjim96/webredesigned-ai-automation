// Reads the approved page files from stages/05_content at build time.
// Same format the 05 preview reads: frontmatter, then one `## <Component>` block per section holding
// `- **Key:** value` fields, lists under a key, tables, numbered `1. **Title.** text` items, bullets and text.
import fs from 'node:fs';
import path from 'node:path';
import { ORDER } from '../site.config';

const PAGES_DIR = path.resolve(process.cwd(), '../stages/05_content/output/pages');

export interface Item { title: string; rest: string; extra: string }
export interface Section {
  kind: string;
  fields: Record<string, string>;
  lists: Record<string, string[]>;
  tables: string[][][];
  items: Item[];
  bullets: string[];
  text: string[];
}
export interface Page {
  slug: string;
  url: string; // '/audit'; the 404 page has '' here
  meta: Record<string, string>;
  title: string;
  sections: Section[];
}

function parse(kind: string, block: string): Section {
  const s: Section = { kind, fields: {}, lists: {}, tables: [], items: [], bullets: [], text: [] };
  const lines = block.split('\n');
  let curList: string[] | null = null;
  let table: string[] = [];
  let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (l.startsWith('|')) {
      table.push(l); i++;
      if (i === lines.length || !lines[i].startsWith('|')) {
        s.tables.push(table.filter((r) => !/^\|[\s:|-]+\|$/.test(r)).map((r) => r.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim())));
        table = [];
      }
      continue;
    }
    let m = l.match(/^- \*\*(.+?):\*\*\s*(.*)$/);
    if (m) {
      const [, key, val] = m; curList = null;
      if (val) s.fields[key] = val;
      else curList = s.lists[key] ??= [];
      i++; continue;
    }
    m = l.match(/^\s{2,}- (.*)$/);
    if (m && curList) { curList.push(m[1]); i++; continue; }
    m = l.match(/^\d+\. \*\*(.+?)\*\*\s*(.*)$/);
    if (m) {
      i++; const extra: string[] = [];
      while (i < lines.length && /^\s{3,}\S/.test(lines[i])) extra.push(lines[i++].trim());
      s.items.push({ title: m[1], rest: m[2], extra: extra.join(' ') }); curList = null; continue;
    }
    m = l.match(/^- (.*)$/);
    if (m) { s.bullets.push(m[1]); curList = null; i++; continue; }
    if (l.trim()) s.text.push(l.trim());
    i++;
  }
  return s;
}

function load(slug: string): Page {
  const text = fs.readFileSync(path.join(PAGES_DIR, `${slug}.md`), 'utf8');
  const [, fm, body] = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)!;
  const meta = Object.fromEntries([...fm.matchAll(/^(\w+): (.*)$/gm)].map((m) => [m[1], m[2]]));
  if (meta.status !== 'approved') throw new Error(`pages/${slug}.md is not approved (status: ${meta.status})`);
  const title = body.match(/^# (.*)$/m)![1];
  const [, ...chunks] = body.split(/^## /m);
  const sections = chunks.map((c) => {
    const nl = c.indexOf('\n');
    return parse(c.slice(0, nl).trim(), c.slice(nl + 1));
  });
  return { slug, url: meta.url.startsWith('/') ? meta.url : '', meta, title, sections };
}

export const pages: Page[] = ORDER.map(load);
export const urls = new Set(pages.map((p) => p.url).filter(Boolean));
export const byUrl = new Map(pages.map((p) => [p.url, p]));

// Sections that say "Same card as Home" / "Same table and note as /audit" borrow these.
const home = pages.find((p) => p.slug === 'home')!;
const audit = pages.find((p) => p.slug === 'audit')!;
export const sharedPrice = home.sections.find((s) => s.kind.startsWith('PriceCard'))!;
export const sharedRoadmap = audit.sections.find((s) => s.kind.includes('RoadmapTable'))!;
