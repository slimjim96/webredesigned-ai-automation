---
status: draft
updated: 2026-10-20
---

# Brand spec: Techne Hora

Palette, type, and voice from direction C; logo is the C3 "dial label" (picked 2026-10-18), with HORA redrawn as Doric columns (reopened 2026-10-20, round 3 "F"). Name chosen in round 5 (after Lake Effect, Millrace, Hourback, Mainspring, Kairos and others). Earlier directions and marks are archived in `logo/_explorations/` (reference only).

## Name and lines
- **Name:** Techne Hora. Two words, both capitalized. Never "TechneHora", "Techne-Hora", or "Techne Hora AI" in the logo
- **Say it:** TEK-nee OR-ah, with a soft, almost silent H. The distinct sound is part of the brand. Use this one pronunciation in calls, videos, and voicemail. On the phone, spell it: "Techne, T-E-C-H-N-E, Hora"
- **Meaning:** *techne* is Greek for craft or skill; *hora* is the hour
- **Tagline:** "The craft of getting your hours back." TODO: owner confirms (alternates: "Skilled work. Hours back." / "Crafted for your hours.")
- **Descriptor** (under the name on vans, cards, social bios): "AI help for local businesses"
- **About-page line:** "Techne is the Greek word for craft; hora means the hour. We craft AI tools that give your hours back."
- **Parent company:** may appear as "by Web Redesigned" on the About page and in the footer; not part of the logo

## Domains
- **technehora.ai**: registered (owner, 2026-10-17). Primary site
- TODO: technehora.com: register and redirect to .ai (owners type ".com" by habit)

## Logo
**Mark:** a navy-rimmed clock at ten o'clock. The face sits just below the rim (one faint shadow, the only soft touch), and the last two hours, 10 to 12, are tinted: the hours given back.
**Name:** "Techne" in IBM Plex Serif 600, standing on HORA. HORA is drawn from scratch, no font, as Doric columns in full navy: tapered shafts with one flute each and no bases, a cushion-and-slab capital on every upright, an R whose bowl is a single Ionic scroll, and an A of two columns leaning into a pediment. The letters stand on a temple's three steps, the base the name is built on. Craft (techne) standing on the hour (hora).
**Small versions** (`-small`, under 60px tall): no flutes, heavier shafts, a plain round bowl on the R, a solid pediment on the A, and one step instead of three, so nothing fills in at header size.
**Motion only:** the ember rewind arrow (round 5, C1) is not part of the logo. It appears where movement makes sense: the site hero, loading states, the first slide of a pitch.

| File (`logo/`) | Use |
|---|---|
| `technehora-lockup-horizontal-light.svg` / `-dark.svg` | default at 60px tall and up: invoices, signage, van doors, title slides |
| `technehora-lockup-horizontal-small-light.svg` / `-small-dark.svg` | under 60px: site header and footer, email signature, social banners at small sizes |
| `technehora-lockup-stacked-light.svg` / `-dark.svg` | mark centered over the name: shirts, signage, title slides, square avatars with name |
| `technehora-wordmark-light.svg` / `-dark.svg` | name only, where the mark already appears nearby |
| `technehora-mark.svg` | the mark with its soft touch: social avatar, app icon, hero |
| `technehora-mark-flat.svg` | no shadow: print, signage, anything that can't reproduce soft effects |
| `technehora-mark-mono-navy.svg` / `-white.svg` | one ink, face left open: embroidery, vinyl cut, stamps, photocopies |
| `favicon.svg`, `png/favicon-16/32/48.png` | browser tab (flat, heavier ticks and hands) |
| `png/apple-touch-icon.png` (180, on paper), `png/technehora-mark-512/1024.png` | phone home screen, social uploads |
| `technehora-rewind.svg` | motion asset: the mark with the ember rewind arc (static) |
| `technehora-rewind-spinner.svg` | motion asset: the arc turning counter-clockwise; stops under reduced motion |

- Every letter is outlined to paths, so no font needs to be installed
- `_build_logo.py` regenerates every SVG; `_render_png.py` regenerates the PNGs. See their docstrings
- **Sizes:** the full lockups from 60px / 20mm tall; the `-small` lockup from 32px to 60px (the site header uses it at 48px). Below 32px, use the mark alone; below 24px, use `favicon.svg`
- **Clear space:** keep the rim's width (about 14% of the mark's height) empty on all sides
- **Don't:** recolor the mark, rotate it, set HORA in color or in a font, use the fluted full lockup under 60px, put the rewind arrow in the static logo, or put the full-color mark on busy photos (use mono-white on a dark scrim instead)
- Rounds explored before this pick are in `logo/_explorations/` (reference only)

## Color
Every text pair passes WCAG 2.2 AA (`_shared/rules.md` #5).

| Token | Hex | Role | Contrast |
|---|---|---|---|
| Ink navy | `#1B2A4A` | text, header, mark disc | 13.3:1 on paper |
| Paper | `#FAF7F0` | page background, clock face | |
| Brick | `#A63D2A` | primary button (white text), links | white on brick 6.3:1; brick on paper 5.9:1 |
| Ember | `#E07A5F` | the arrow; decorative accents on navy only, never text on paper | graphic use only |
| Sage | `#4E7060` | secondary accent | 5.2:1 on paper |
| Graphite | `#5C6170` | muted text | 5.8:1 on paper |

## Type
Direction: "Engineered" from `type-studies.html` (owner's starting pick, 2026-10-17).
- **Headings:** IBM Plex Serif, 600 / 700. Sentence case
- **Body and UI:** IBM Plex Sans, 400 / 600
- **Details** (numbers in roadmaps, badges, small labels): IBM Plex Mono
- All on Google Fonts (OFL)
- The logo's "Techne" is Plex Serif 600, outlined to paths; HORA is drawn, not set in a font

## Voice
A straight-talking advisor. Plain words, short sentences, outcomes before tools (`_shared/rules.md` #3). The Greek name is the one fancy thing; the copy around it stays plain.

| Do | Don't |
|---|---|
| "Missed calls are missed jobs." | "Leverage AI-powered omnichannel engagement." |
| "Five things to fix, in order." | "A comprehensive transformation roadmap." |
| "We'll train your team to run it." | "Seamless change management enablement." |
| Say "hours" and "calls" and "quotes" | Say "agents", "LLMs", "MCP" unless the reader already does |

## Owner checks (approved 2026-10-17 with these open; each must be done before `07_launch`)
- [x] technehora.ai registered
- TODO: technehora.com registered and redirecting
- TODO: tagline confirmed
- TODO: handles: LinkedIn, Google Business Profile, Facebook, Instagram (@technehora)
- TODO: quick USPTO search for "Techne Hora" in classes 35 (consulting) and 41 (training)
