// Inline formatting for copy from the page files: escape, settle markers, then links, bold, italics, code.
import { BUILD, EMAIL, PHONE, PHONE_TEL } from '../site.config';
import { urls } from './content';

const escape = (t: string) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** An internal URL from the copy ('`/audit`', ' / ') as a checked href. Unknown pages stop the build. */
export function href(raw: string): string {
  const url = raw.trim().replace(/^`|`$/g, '').trim();
  if (!urls.has(url)) throw new Error(`Link to a page that isn't in the sitemap: ${url}`);
  return url;
}

/** 'Book a free 20-minute call → `/book`' -> { label, href } */
export function action(val: string) {
  const [label, url] = val.split('→');
  return { label: label.trim(), href: href(url ?? '') };
}

export function inline(t: string): string {
  let out = escape(t);
  out = out.replace(/\[\[(OWNER|BUILD|PROOF NEEDED)(?::\s*(.*?))?\]\]/g, (_, kind: string, what = '') => {
    if (kind === 'BUILD' && what in BUILD) return escape(BUILD[what]);
    throw new Error(`[[${kind}${what ? ': ' + what : ''}]] reached the site. Settle it in site.config.ts or in the 05 page file.`);
  });
  out = out.replace(/\[([^\]]+)\]\((\/[^)]*)\)/g, (_, text: string, url: string) => `<a href="${href(url)}">${text}</a>`);
  out = out.replaceAll(PHONE, `<a href="tel:${PHONE_TEL}">${PHONE}</a>`);
  out = out.replaceAll(EMAIL, `<a href="mailto:${EMAIL}">${EMAIL}</a>`);
  out = out.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/(?<![\w*])\*(?!\s)(.+?)\*(?!\w)/g, '<em>$1</em>');
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  return out;
}

/** Plain text (for titles, aria labels, structured data): markers settled, formatting dropped. */
export function plain(t: string): string {
  return inline(t).replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}
