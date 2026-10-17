---
status: draft
updated: 2026-10-17
---

# Brand spec: Hourback

Chosen after three rounds: palette, type, and voice from direction C; name from round 3; mark is the R2 wall-clock dial. Earlier directions and marks are archived in `logo/_explorations/` (reference only).

## Name and lines
- **Name:** Hourback. Always one word, capital H only. Not "HourBack", "Hour Back", or "Hourback AI" in the logo; "Hourback AI" is fine in plain text where context needs it (e.g. a Google Business Profile category line)
- **Tagline:** "Get your hours back."
- **Descriptor** (under the name on vans, cards, social bios): "AI help for local businesses"
- **Name story** (one line for the About page): the outcome is the name. We find the hours your week is losing and give them back.

## Logo
**Mark:** a cream clock face set slightly above a navy disc, hands at 10 and 12, the last two hours tinted, and a brick arrow wrapping the dial counter-clockwise: time wound back.

| File (`logo/`) | Use |
|---|---|
| `hourback-lockup-horizontal-light.svg` / `-dark.svg` | default: site header, invoices, email signature |
| `hourback-lockup-stacked-light.svg` / `-dark.svg` | square spaces: social avatars with name, van doors, shirts |
| `hourback-wordmark-light.svg` / `-dark.svg` | where the mark already appears nearby |
| `hourback-mark.svg` | the full-color mark: social avatar, app icon |
| `hourback-mark-flat.svg` | no gradients: print, signage, anything that can't reproduce shading |
| `hourback-mark-mono-navy.svg` / `-white.svg` | one ink: embroidery, vinyl cut, stamps, fax/photocopy |
| `favicon.svg`, `png/favicon-16/32/48.png` | browser tab (simplified: four ticks, heavier hands) |
| `png/apple-touch-icon.png` (180), `png/hourback-mark-512/1024.png` | phone home screen, social uploads |

- Wordmark: Fraunces Bold (opsz 144), outlined to paths, so the files need no font installed
- `_build_logo.py` regenerates every file; see its docstring
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
- **Headings:** Fraunces, 700 (600 for subheads). Sentence case
- **Body and UI:** Source Sans 3, 400 / 600
- Both on Google Fonts (OFL)

## Voice
A straight-talking advisor. Plain words, short sentences, outcomes before tools (`_shared/rules.md` #3).

| Do | Don't |
|---|---|
| "Missed calls are missed jobs." | "Leverage AI-powered omnichannel engagement." |
| "Five things to fix, in order." | "A comprehensive transformation roadmap." |
| "We'll train your team to run it." | "Seamless change management enablement." |
| Say "hours" and "calls" and "quotes" | Say "agents", "LLMs", "MCP" unless the reader already does |

## Before approval (person checks; record results here)
- TODO: domain: hourback.com (and .ai / .co if wanted)
- TODO: NY DOS business name search for "Hourback"
- TODO: handles: LinkedIn, Google Business Profile, Facebook, Instagram
- TODO: USPTO search for "Hourback" in class 35 (business consulting) and 41 (training)
