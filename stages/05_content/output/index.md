---
status: draft
updated: 2026-10-18
---

# Content index

Every page in the approved sitemap, its copy file, and its status. The stage is approved when every launch page is `approved` here and the owner items below are answered.

**See it laid out:** `preview/` (built by `_build_preview.py` from the page files, with the design system's real CSS). Published copy: https://claude.ai/artifact/7DxEjNufEXRMMzHa5tqzca. The "Review notes" button shows each page's title tag, description and builder notes; owner items are highlighted yellow, build items blue.

## Pages

| Page | URL | File | Status |
|---|---|---|---|
| Home | `/` | `pages/home.md` | draft |
| The AI audit | `/audit` | `pages/audit.md` | draft |
| Training & builds | `/services` | `pages/services.md` | draft |
| Workshops & team training | `/services/training` | `pages/services-training.md` | draft |
| Custom skills & builds | `/services/custom-builds` | `pages/services-custom-builds.md` | draft |
| Who we help | `/industries` | `pages/industries.md` | draft |
| HVAC, plumbing & electrical | `/industries/hvac` | `pages/industries-hvac.md` | draft |
| Restaurants | `/industries/restaurants` | `pages/industries-restaurants.md` | draft |
| Other local businesses | `/industries/local-services` | `pages/industries-local-services.md` | draft (placeholder until the third vertical) |
| Rochester & Monroe County | `/areas/rochester` | `pages/areas-rochester.md` | draft (local block: 169 words, rule is 150+) |
| About | `/about` | `pages/about.md` | draft |
| FAQ | `/faq` | `pages/faq.md` | draft |
| Book a call | `/book` | `pages/book.md` | draft |
| You're booked | `/book/thanks` | `pages/book-thanks.md` | draft |
| Privacy | `/privacy` | `pages/privacy.md` | draft (owner review; not legal advice) |
| Accessibility | `/accessibility` | `pages/accessibility.md` | draft |
| 404 | (any missing page) | `pages/404.md` | draft |
| Later, when ready: Examples, Buffalo, Syracuse, Finger Lakes | | | not started (sitemap: only when content is real) |

## Where the copy differs from the sitemap
- `/services` shows **3** cards (audit, training, builds), not 2: the design system's ServiceCard rule says "never 2 lonely cards".
- `/services/custom-builds` cards have no links: each describes a kind of build, and there's no page per build yet.
- `/industries` "Is this you?" blocks are ServiceCards whose text is a 3-item problem list.

## Open owner items
Answer once; the same answer fills every page listed.

| # | Item | Pages |
|---|---|---|
| 1 | Business phone number | `book`, `privacy`, `accessibility` (+ `CallBar`, footer, structured data) |
| 2 | Your name, and 2–3 sentences of background you're comfortable publishing | `about` |
| 3 | A photo of you at work (until then, the rewind mark) | `about` |
| 4 | Plain answer on client data: what you look at, keep, where, how long, who else sees it, how to ask for deletion | `audit` FAQ 4, `faq`, `privacy`, `services-training` FAQ 4 |
| 5 | Refund or partial credit if the audit finds nothing worth fixing? | `audit` FAQ 1, `faq` |
| 6 | How soon the roadmap arrives after the session | `audit` step 3 |
| 7 | Reply time for the fallback form ("within one business day"?) | `book` |
| 8 | Response times for privacy requests and accessibility reports | `privacy`, `accessibility` |
| 9 | Who owns builds; what happens to accounts and logins at handover | `services-custom-builds`, `faq` |
| 10 | Support or maintenance after handover | `services-custom-builds` |
| 11 | Workshop formats you'll offer | `services-training` |
| 12 | Software you've actually worked with: field-service (trades), POS/reservations (restaurants), or keep it general | `industries-hvac`, `industries-restaurants` |
| 13 | Travel: the area you'll cover without a fee; "at your door the week after"? | `areas-rochester` |
| 14 | One sentence on Web Redesigned, if wanted | `about` |
| 15 | Sample roadmap figures (12.0 and 10.0 hours/week): comfortable showing them as illustrations? | `audit`, `industries-hvac`, `industries-restaurants` |
| 16 | Link `/examples` from builds once 2+ real demos are live | `services-custom-builds` |

Build items (`[[BUILD: …]]`, settled in `06_build`): booking tool, analytics tool, launch date (privacy page).

## Small humor, on purpose
Light touches the owner may keep or cut: the 404 ("This page took the day off."), restaurants ("The phone always rings at 6:45."), the pronunciation line on About, "We've seen a desk." and the garbage-plate nod on Rochester ("You don't even have to buy us a plate."), "Will a robot be answering my phone? No robots." in the FAQ.
