---
status: approved
updated: 2026-10-17
---

# Brand spec: Techne Hora

Palette, type, and voice from direction C; mark is the R2 wall-clock dial. Name chosen in round 5 (after Lake Effect, Millrace, Hourback, Mainspring, Kairos and others). Earlier directions and marks are archived in `logo/_explorations/` (reference only).

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
**Mark:** a cream clock face set slightly above a navy disc, hands at 10 and 12, the last two hours tinted, and a brick arrow wrapping the dial counter-clockwise: time wound back.

| File (`logo/`) | Use |
|---|---|
| `technehora-lockup-horizontal-light.svg` / `-dark.svg` | default: site header, invoices, email signature |
| `technehora-lockup-compact-light.svg` / `-dark.svg` | name on two lines beside the mark: van doors, social avatars with name, business cards |
| `technehora-lockup-stacked-light.svg` / `-dark.svg` | mark centered over the name: shirts, signage, title slides |
| `technehora-wordmark-light.svg` / `-dark.svg` | where the mark already appears nearby |
| `technehora-mark.svg` | the full-color mark: social avatar, app icon |
| `technehora-mark-flat.svg` | no gradients: print, signage, anything that can't reproduce shading |
| `technehora-mark-mono-navy.svg` / `-white.svg` | one ink: embroidery, vinyl cut, stamps, fax/photocopy |
| `favicon.svg`, `png/favicon-16/32/48.png` | browser tab (simplified: four ticks, heavier hands) |
| `png/apple-touch-icon.png` (180), `png/technehora-mark-512/1024.png` | phone home screen, social uploads |

- Wordmark: currently Fraunces Bold (opsz 144), outlined to paths so the files need no font installed. A redesign is in progress via `logo-design-brief.md`
- `_build_logo.py` regenerates every SVG; see its docstring
- **Clear space:** keep the radius of the clock face (about 30% of the mark's height) empty on all sides
- **Minimum size:** full mark 24px / 8mm; below 24px use `favicon.svg`
- **Don't:** recolor the mark, rotate it, add effects, put the full-color mark on busy photos (use mono-white on a dark scrim instead)

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
- TODO: the current wordmark files are still outlined in Fraunces. They get replaced when the logo redesign in `logo-design-brief.md` comes back

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
