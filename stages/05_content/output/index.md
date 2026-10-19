---
status: draft
updated: 2026-10-18
---

# Content index

Every page in the approved sitemap, its copy file, and its status. The stage is approved when every launch page is `approved` here and the owner items below are answered.

**See it laid out:** `preview/` (built by `_build_preview.py` from the page files, with the design system's real CSS). Published copy: https://claude.ai/artifact/7DxEjNufEXRMMzHa5tqzca. The "Review notes" button shows each page's title tag, description and builder notes; open owner items are highlighted yellow, build items blue.

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
- `/industries` "Which one sounds like you?" blocks are ServiceCards whose text is a 3-item problem list.

## Owner items
Answered by the owner on 2026-10-18, and written into every page listed.

| # | Item | Answer | Pages |
|---|---|---|---|
| 4 | Client data | We look at tools with you, on your screen. We take no copies of customer data, and never sell or share anything. Builds live in your accounts. We keep notes and the roadmap, and delete them on request or 12 months after the work ends | `audit`, `faq`, `privacy`, `services-training` |
| 5 | Audit finds nothing worth fixing | Full refund of the $750 | `audit`, `faq` |
| 6 | Roadmap timing | Within 2 business days of the session | `audit` |
| 7 | Form reply time | Within one business day | `book` |
| 8 | Privacy and accessibility requests | Reply within 2 business days; privacy requests finished within 30 days | `privacy`, `accessibility` |
| 9 | Build ownership | Yours: in your accounts, billed to you; every login handed over and our access removed | `services-custom-builds`, `faq` |
| 10 | Support after handover | 30 days of fixes included, then an optional monthly plan or pay per fix (plan price decided later, not on the site) | `services-custom-builds` |
| 11 | Workshop formats | Half-day on-site, owner 1-on-1, short team sessions, group classes | `services-training` |
| 12 | Named software | None; kept general | `industries-hvac`, `industries-restaurants` |
| 13 | Travel | No travel fee anywhere in Western NY; "at your door soon after" (softened from "the week after") | `areas-rochester` |
| 14 | Web Redesigned on About and in the footer | Left out of both (still named as the operator on `privacy`) | `about`, footer |
| 15 | Sample roadmap hours | Keep, labeled "Sample · not a client" | `audit`, `industries-hvac`, `industries-restaurants` |

### Still open (these block approval)
| # | Item | Pages |
|---|---|---|
| 1 | Business phone number | `book`, `privacy`, `accessibility` (+ `CallBar`, footer, structured data) |
| 2 | Your name, and 2–3 sentences of background you're comfortable publishing | `about` |

### Later, not blocking
- **#3 Photo:** About launches with the rewind mark; swap in a photo of you at work when you have one.
- **#16 Examples:** link `/examples` from the builds FAQ once 2+ real demos are live.

Build items (`[[BUILD: …]]`, settled in `06_build`): booking tool, analytics tool, launch date (privacy page).

## Small humor, on purpose
Light touches the owner may keep or cut: the 404 ("This page took the day off."), restaurants ("The phone always rings at 6:45."), the pronunciation line on About, "We've seen a desk." and the garbage-plate nod on Rochester ("You don't even have to buy us a plate."), "Will a robot be answering my phone? No robots." in the FAQ.
