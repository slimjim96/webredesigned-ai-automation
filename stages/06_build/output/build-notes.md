---
status: approved
updated: 2026-10-20
---

# Build notes

The site is in `site/`: Astro 7.3.5, static output for Cloudflare Pages, no UI framework. `npm run check` builds it and checks every page (links, images, titles, descriptions, one H1, no leftover markers).

## How it's put together
- **Copy:** read at build time from `stages/05_content/output/pages/*.md` (`site/src/lib/content.ts`), never retyped. A page file that isn't `status: approved` stops the build, as does any `[[OWNER: …]]`, `[[PROOF NEEDED]]` or `[[BUILD: …]]` that `site/src/site.config.ts` doesn't settle.
- **Look:** `tokens.css`, `components.css`, fonts and logos are copied from 03 and 02 on every run (`site/scripts/sync.mjs`); the copies are gitignored. `site/src/styles/site.css` holds only the sitemap's three gap components (Breadcrumbs, ProblemList, BookingEmbed) and the form's states, from tokens.
- **One component per section type:** `site/src/components/sections/`. `PageBody.astro` picks the component from each section's `##` name, the same way the 05 preview did.
- **URLs:** `/audit`, `/industries/hvac` … with no trailing slash (`build.format: 'file'`). `404.html` is Cloudflare's not-found page.

## Settled `[[BUILD: …]]` items
| In the copy | On the site |
|---|---|
| booking tool / Cal.com, if chosen | Cal.com |
| Plausible or Cloudflare Web Analytics | "We use Cloudflare Web Analytics for this." |
| launch date (privacy) | `PRIVACY_UPDATED` in `site.config.ts`, now "October 2026": set it to the launch month |

## Site functions (sitemap → what was built)
| Function | Built | Needs before launch |
|---|---|---|
| Booking | Cal.com inline embed on `/book`; a finished booking goes to `/book/thanks`. If the calendar hasn't loaded after 12 seconds, or no event is set, the copy's fallback line shows with a link to the form | A Cal.com account with a 20-minute event; `PUBLIC_CAL_LINK` = `<user>/<event>`. In Cal.com, also set the event's redirect to `https://technehora.ai/book/thanks` for people who book outside the embed |
| Fallback form | `functions/api/contact.js`: checks fields, honeypot, optional Turnstile, sends the note by email through Resend, reply-to set when they left an email. Errors and states use the copy's wording | Resend account with technehora.ai verified; `RESEND_API_KEY`, `CONTACT_TO`, `CONTACT_FROM`. A Turnstile widget: `PUBLIC_TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET` |
| Click to call | `tel:` in the call bar (phones), footer, `/book`, privacy, accessibility | **The real phone number** in `site.config.ts` (`PHONE`, `PHONE_TEL`) |
| Analytics | Cloudflare Web Analytics beacon, only when a token is set | `PUBLIC_CF_BEACON_TOKEN`, or switch on Web Analytics for the Pages project in the dashboard instead (then leave the token empty) |
| Structured data | `ProfessionalService` with `areaServed` on every page; `Service` on the audit, training and builds pages (the audit with its $750 offer); `BreadcrumbList` on child pages. The phone is left out while it's a placeholder | |
| SEO basics | Unique title and description per page, canonical URLs, `sitemap.xml` (thanks page left out), `robots.txt`, `noindex` on `/book/thanks` and the 404, Open Graph image per page (`public/og/`, made by `scripts/og.mjs`) | |
| Headers | `public/_headers`: nosniff, referrer policy, permissions policy, frame options, long caching for fonts and built assets | |

## Where the build differs from the sitemap
- **Conversion events:** the sitemap asks for "booking started / completed, form sent, call tapped". Cloudflare Web Analytics counts page views only, so the site can count **booking completed** (views of `/book/thanks`) and **booking started** (views of `/book`) but not form sends or call taps. Options if those matter: Plausible (custom events, about $9/month) or Cal.com's and Resend's own counts.
- **Fallback form email:** Resend sends it (the sitemap said "email to the owner" without naming a sender). The privacy page's line "It comes to us by email" still holds.
- **Content-Security-Policy:** not set yet; add it in 07 once the Cal.com embed is tested against it, so the policy can't silently break booking.
- **The form needs JavaScript** (so does Turnstile). Without it, the form shows the copy's failure line pointing to the phone and email.
- **Footer "Site" column** lists Training & builds, Who we help, FAQ, Privacy and Accessibility; Examples comes back when the page exists (sitemap rule).
- **Google Business Profile link:** not in the footer or About yet; there's no profile to link. Add it when it exists (07).

## Reported back to 03_design-system
- `components.css` sets `.th-header__cta` to `display: block` at 960px, which knocks the "Book a call" label off center. `site.css` overrides it with `inline-flex`; fold the fix into 03 next time it's reopened, then drop the override.
- The stacked roadmap table labels every cell from `data-label`; the site leaves the label off the first column (the fix name is already bold there).

## Accounts and settings for Cloudflare Pages
- Project: connect the GitHub repo; **root directory** `site`, **build command** `npm run build`, **output** `dist`. The build reads `../stages/`, which is in the same repo.
- Environment variables: `PUBLIC_CAL_LINK`, `PUBLIC_TURNSTILE_SITE_KEY`, `PUBLIC_CF_BEACON_TOKEN` (build time); `RESEND_API_KEY`, `TURNSTILE_SECRET` (secrets), `CONTACT_TO`, `CONTACT_FROM` (functions).
- Domain, email on the domain, and the technehora.com → technehora.ai redirect are `07_launch`.

## Launch blockers carried forward
- The phone number is the placeholder **(585) 555-0100**. `LAUNCH=1 npm run check` fails until it's replaced.
- `PRIVACY_UPDATED` set to the launch month.
- The owner reviews the privacy page text (05 note: plain-language draft, not legal advice).

## Checked
- `npm run check`: 17 pages, every internal link and image resolves, one H1 per page, unique titles, no markers.
- Screenshots (headless Chrome): Home at desktop, phone and phone dark; Audit, Book, Privacy and You're booked at desktop; HVAC and 404 on a phone. Fixed what they showed (form error icons showing early, the header button, the roadmap's first-column label, full-width heroes without art).
- Not yet tested: the Cal.com embed and the form's sending path, which need the accounts above; the form's error states in a browser.
