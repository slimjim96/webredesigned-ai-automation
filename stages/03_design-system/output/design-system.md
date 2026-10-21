---
status: approved
updated: 2026-10-17
---

# Design system: Techne Hora

**Preview page:** https://claude.ai/artifact/TK9xxob6Pc3Wof2v6esks9 (private to the owner until shared)

The brand book with full usage rules is `ds/project/README.md`; each component's rules are in `ds/project/components/<Name>/README.md`. This file records what was decided and what is still open.

## What `06_build` uses
| File | What it is |
|---|---|
| `tokens.css` | every color, type size, spacing step, radius, shadow and size as CSS custom properties, light and dark; `text-*` type classes; `@font-face` |
| `components.css` | the 16 components as `th-*` classes |
| `fonts/` | IBM Plex Serif 600, Plex Sans (variable 100–700) + italic, Plex Mono 500; Latin, about 105 KB total |

Load `tokens.css`, then `components.css`, and put `class="th-root"` on `<body>`. Plain HTML/CSS: it works with any stack chosen in 06.

## Decisions
- **Type:** IBM Plex ("Engineered" from the type studies). Serif 600 for headings, Sans for reading, Mono for labels and numbers. Body is 17px on phones and 18px on desktop.
- **Color:** the brand palette plus derived UI tokens (surface, borders, focus, success, danger, a light ember link color for dark mode). Brick is reserved for the one primary button and links. Ember stays graphic-only.
- **Dark mode:** the site follows the visitor's system setting. Every pair passes AA in both themes (checked by `_build_tokens.py`).
- **Shape:** small radii (4/6/10px), two shadows, no UI gradients. It reads as precise and practical.
- **Accessibility:** 44px minimum tap targets, a 2px focus ring everywhere, errors with an icon and a sentence, works at 360px.
- **Icons:** Lucide outline at 1.75 stroke (ISC license).
- **Proof:** `ProofSlot` renders a visible red `[[PROOF NEEDED]]` frame until real, permitted proof exists (`_shared/rules.md` #2).

## Components (16)
Button · Eyebrow and Tag · SiteHeader (with phone menu) · Hero · SectionHeading · ServiceCard · Steps · PriceCard ($750 audit) · RoadmapTable (stacks on phones) · FAQ · FormField · Callout · ProofSlot · CTABand · SiteFooter · CallBar (phones only)

These are the standard set for a small service site. 04_sitemap may ask for more, such as a vertical page's "problems we fix" list or a booking embed wrapper. Add them here when it does.

## Open items
- The header and footer use `technehora-lockup-horizontal-small-light.svg` / `-small-dark.svg` at 48px tall (HORA redrawn as Doric columns 2026-10-20; the small lockup drops the flutes and two of the steps so it stays clean at that size)
- TODO: the sample copy in previews (FAQ answers, audit lead time, refund wording) is layout text. Real copy is written in `05_content`
- TODO: booking tool (Cal.com, Calendly, or a form) is chosen in `06_build`; FormField covers a plain form
- Brand checks carried from 02 (`.com` redirect, tagline, handles, trademark search) still block `07_launch`

## Human check
Open the preview page. Click through every component in light and dark mode, and narrow the window to phone width. Then set `status: approved` here, or say what to change.
