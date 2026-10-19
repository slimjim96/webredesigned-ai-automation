// Facts the whole site shares, and how the copy's [[BUILD: …]] markers are settled.
// Accounts and keys come from environment variables (set in Cloudflare Pages), never from this file.

export const SITE_URL = 'https://technehora.ai';
export const NAME = 'Techne Hora';
export const EMAIL = 'hello@technehora.ai';

// Placeholder from the 555-01xx range set aside for fiction, so it never rings a real person.
// Replace before launch: `LAUNCH=1 npm run check` fails while it is still here.
export const PHONE = '(585) 555-0100';
export const PHONE_TEL = '+15855550100';
export const PHONE_IS_PLACEHOLDER = PHONE.includes('555-01');

// The Cal.com event, as "<user>/<event>" (e.g. "technehora/20min"). Empty: /book shows its fallback.
export const CAL_LINK: string = import.meta.env.PUBLIC_CAL_LINK ?? '';
// Cloudflare Turnstile site key for the fallback form. Empty: the form sends without the check.
export const TURNSTILE_SITE_KEY: string = import.meta.env.PUBLIC_TURNSTILE_SITE_KEY ?? '';
// Cloudflare Web Analytics beacon token. Empty: no analytics script on the page.
export const CF_BEACON_TOKEN: string = import.meta.env.PUBLIC_CF_BEACON_TOKEN ?? '';

// Shown as "Last updated …" on /privacy. Set to the launch month.
export const PRIVACY_UPDATED = 'October 2026';

// Each [[BUILD: …]] in the copy, word for word, and what the site says instead.
// A marker missing from this list stops the build.
export const BUILD: Record<string, string> = {
  'booking tool': 'Cal.com',
  'Cal.com, if chosen': 'Cal.com',
  'Plausible or Cloudflare Web Analytics, whichever is chosen': 'We use Cloudflare Web Analytics for this.',
  'launch date': PRIVACY_UPDATED,
};

// Page files in stages/05_content/output/pages, in sitemap order.
export const ORDER = [
  'home', 'audit', 'services', 'services-training', 'services-custom-builds', 'industries', 'industries-hvac',
  'industries-restaurants', 'industries-local-services', 'areas-rochester', 'about', 'faq', 'book', 'book-thanks',
  'privacy', 'accessibility', '404',
];

// Pages kept out of search and the sitemap.
export const NOINDEX = ['/book/thanks'];

export const NAV = [
  { label: 'The audit', href: '/audit' },
  { label: 'Training & builds', href: '/services' },
  { label: 'Who we help', href: '/industries' },
  { label: 'About', href: '/about' },
];

// Structured data: where we work (positioning).
export const AREA_SERVED = [
  { '@type': 'City', name: 'Rochester, NY' },
  { '@type': 'AdministrativeArea', name: 'Monroe County, NY' },
  { '@type': 'City', name: 'Buffalo, NY' },
  { '@type': 'City', name: 'Syracuse, NY' },
  { '@type': 'Place', name: 'Finger Lakes, NY' },
];
