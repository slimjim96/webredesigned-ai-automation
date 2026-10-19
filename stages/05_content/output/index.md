---
status: approved
updated: 2026-10-18
---

# Content index

Every page in the approved sitemap, its copy file, and its status. The stage is approved when every launch page is `approved` here and the owner items below are answered.

**See it laid out:** `preview/` (built by `_build_preview.py` from the page files, with the design system's real CSS). Published copy: https://claude.ai/artifact/7DxEjNufEXRMMzHa5tqzca. The "Review notes" button shows each page's title tag, description and builder notes; open owner items are highlighted yellow, build items blue.

## Pages

| Page | URL | File | Status |
|---|---|---|---|
| Home | `/` | `pages/home.md` | approved |
| The AI audit | `/audit` | `pages/audit.md` | approved |
| Training & builds | `/services` | `pages/services.md` | approved |
| Workshops & team training | `/services/training` | `pages/services-training.md` | approved |
| Custom skills & builds | `/services/custom-builds` | `pages/services-custom-builds.md` | approved |
| Who we help | `/industries` | `pages/industries.md` | approved |
| HVAC, plumbing & electrical | `/industries/hvac` | `pages/industries-hvac.md` | approved |
| Restaurants | `/industries/restaurants` | `pages/industries-restaurants.md` | approved |
| Other local businesses | `/industries/local-services` | `pages/industries-local-services.md` | approved (placeholder until the third vertical) |
| Rochester & Monroe County | `/areas/rochester` | `pages/areas-rochester.md` | approved (local block: 169 words, rule is 150+) |
| About | `/about` | `pages/about.md` | approved |
| FAQ | `/faq` | `pages/faq.md` | approved |
| Book a call | `/book` | `pages/book.md` | approved |
| You're booked | `/book/thanks` | `pages/book-thanks.md` | approved |
| Privacy | `/privacy` | `pages/privacy.md` | approved (owner review; not legal advice) |
| Accessibility | `/accessibility` | `pages/accessibility.md` | approved |
| 404 | (any missing page) | `pages/404.md` | approved |
| Later, when ready: Examples, Buffalo, Syracuse, Finger Lakes | | | not started (sitemap: only when content is real) |

## Where the copy differs from the sitemap
- `/services` shows **3** cards (audit, training, builds), not 2: the design system's ServiceCard rule says "never 2 lonely cards".
- `/about` bio is in first person ("I'm Jim") while the rest of the site says "we": owner's choice, 2026-10-18. Keep it.
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
| 2 | About bio | Jim (once "Slim"); grew up in Rochester; 25 years building software end to end; now applying AI to business processes and training teams. Employer not named | `about` |
| 15 | Sample roadmap hours | Keep, labeled "Sample · not a client" | `audit`, `industries-hvac`, `industries-restaurants` |

### Placeholder until launch
- **#1 Phone:** the pages use **(585) 555-0100**, a number from the 555-01xx range set aside for fiction, so it never reaches a real person. It appears on `book`, `privacy` and `accessibility`, plus the footer; `06_build` also needs it for the `CallBar` and structured data. The real number must replace it before launch: carry this into the launch checklist when `06_build`/`07_launch` are set up.

### Later, not blocking
- **#3 Photo:** About launches with the rewind mark; swap in a photo of you at work when you have one.
- **#16 Examples:** link `/examples` from the builds FAQ once 2+ real demos are live.

Build items (`[[BUILD: …]]`, settled in `06_build`): booking tool, analytics tool, launch date (privacy page). The placeholder phone number shows blue in the preview too.

## Small humor, on purpose
Light touches the owner may keep or cut: the 404 ("This page took the day off."), restaurants ("The phone always rings at 6:45."), the pronunciation line on About, "We've seen a desk." and the garbage-plate nod on Rochester ("You don't even have to buy us a plate."), "Will a robot be answering my phone? No robots." in the FAQ.
