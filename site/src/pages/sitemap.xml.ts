import { pages } from '../lib/content';
import { NOINDEX, SITE_URL } from '../site.config';

export function GET() {
  const locs = pages.filter((p) => p.url && !NOINDEX.includes(p.url)).map((p) => SITE_URL + (p.url === '/' ? '/' : p.url));
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${locs.map((l) => `  <url><loc>${l}</loc></url>`).join('\n')}
</urlset>
`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
