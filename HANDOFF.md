# Handoff — 2026-10-22

Where the work stopped, so a fresh session can pick it up. Stage status always comes from the `status:` frontmatter in `stages/*/output/*.md`; this file only adds context. Delete it once it's out of date.

## Stage status
| Stage | Status | Notes |
|---|---|---|
| 01_positioning | approved | |
| 02_brand | approved | Re-approved 2026-10-22: HORA redrawn as plain narrow, tall letters on a thin line (round 6 "N2": letters over the middle 80% of "Techne", line as wide as "Techne"; rounds 1–6 in `logo/_explorations/hora-columns/`). One lockup at every size: the `-small` lockups are retired. Set, brand spec and brand sheet rebuilt; the 03 design system, site header/footer and site preview already use it. Owner checks still open and block `07_launch`: technehora.com redirect, social handles, USPTO search (tagline confirmed 2026-10-22) |
| 03_design-system | approved | Preview: https://claude.ai/artifact/TK9xxob6Pc3Wof2v6esks9 |
| 04_sitemap | approved | Approved 2026-10-18: hubs earn their place, proof slots left out until real, only Rochester's area page at launch |
| 05_content | approved | Re-approved 2026-10-22 with the tagline as the home page's closing band heading. Owner answers in `output/index.md`. Phone is the placeholder (585) 555-0100 until launch |
| 06_build | approved | Approved 2026-10-20 after the owner clicked through the preview (https://claude.ai/artifact/USHrT6yZZyS5DDKxhzby3k). `site/` is Astro 7.3.5 for Cloudflare Pages; `stages/06_build/output/build-notes.md` lists the accounts and env vars launch needs (Cal.com, Resend, Turnstile, Web Analytics) |
| 07_launch | draft: checklist written | `stages/07_launch/output/launch-checklist.md`; next is the owner's accounts and blockers. Carries: the real phone number, `PRIVACY_UPDATED`, owner privacy review, CSP, Google Business Profile, 02's open owner checks |

## Decisions made this session
- **Name:** Techne Hora, said **TEK-nee OR-ah** (soft, almost silent H). technehora.ai is registered.
- **Type:** IBM Plex Serif / Sans / Mono (the "Engineered" pick from `02_brand/output/type-studies.html`).
- **Build (06):** Astro static on Cloudflare Pages; Cal.com booking; Cloudflare Web Analytics; fallback form via a Pages Function + Resend. The site reads the 05 page files at build time, so copy is never retyped.
- **Design system:** tokens are built by `03_design-system/output/_build_tokens.py`, which checks contrast. The 16 components are in `components.css`.

## Logo (C3 2026-10-18; HORA redrawn 2026-10-22)
The owner picked **C3, "the dial label"**: a navy-rimmed clock at 10:00 with the last two hours tinted, "Techne" in Plex Serif, and HORA under it. HORA was Plex Mono, then drawn from scratch: Doric columns (rounds 1–4, "F" briefly approved), then plain narrow, tall letters on a thin line (round 6 "N2", approved 2026-10-22). The owner asked for letters that read at small sizes and aren't building-like. The ember rewind arrow (C1) is kept as a motion-only asset for the hero, loading states, and pitch slides.
- Set built by `02_brand/output/logo/_build_logo.py` (SVGs) and `_render_png.py` (PNGs). The compact lockups were dropped, because the horizontal lockup already puts the name on two lines
- `brand-spec.md` Logo section and the design system's Logos README / header height (now 48px) are updated
- Rounds explored, for reference: `logo/_explorations/rewind/` (3D puzzle marks, rejected as too complex) and `logo/_explorations/plex-refined/` (C1–C3)
- Brand sheet redone and built by `02_brand/output/_build_sheet.py` (inlines the logo SVGs): https://claude.ai/artifact/2TeB3biugnrhD6XmtHaGP5
- Design-system preview updated (Logos group, header, footer, hero, cover). The old Fraunces logo uploads are still in its asset store, unlisted. `logo-design-brief.md` (status: draft) is now moot

## Next session
1. `07_launch`: the owner's blockers and accounts in `stages/07_launch/output/launch-checklist.md`.

## Git
Everything is committed and pushed to main.

## Tooling notes
- The logo scripts need fontTools + brotli (to read the woff2 files). The Plex woff2 files are in `03_design-system/output/fonts/`.
- `_render_png.py` also needs pillow.
- Render checks use headless Chrome with an isolated `--user-data-dir`. Pages that load Google Fonts can hang headless Chrome here, so use local font files when rendering.
- Run `git config core.fileMode false` before trusting `git status`.
- Headless Chrome here can't load `http://localhost` pages (hangs, even outside the sandbox). To screenshot the built site, copy `site/dist` and rewrite its root-relative links to relative file paths, then open it with `file://`.
- `site/`: `npm run check` builds and checks every page; `node scripts/og.mjs` remakes the share images after copy changes.
