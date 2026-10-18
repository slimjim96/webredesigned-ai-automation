# Handoff — 2026-10-17

Where the work stopped, so a fresh session can pick it up. Stage status always comes from the `status:` frontmatter in `stages/*/output/*.md`; this file only adds context. Delete it once it's out of date.

## Stage status
| Stage | Status | Notes |
|---|---|---|
| 01_positioning | approved | |
| 02_brand | approved | Owner checks still open, and they block `07_launch`: technehora.com redirect, tagline, social handles, USPTO search |
| 03_design-system | approved | Preview: https://claude.ai/artifact/TK9xxob6Pc3Wof2v6esks9 |
| 04_sitemap | **draft: awaiting owner review** | `stages/04_sitemap/output/sitemap.md`. Next step: owner walks the visitor journeys and approves, then `05_content` |

## Decisions made this session
- **Name:** Techne Hora, said **TEK-nee OR-ah** (soft, almost silent H). technehora.ai is registered.
- **Type:** IBM Plex Serif / Sans / Mono (the "Engineered" pick from `02_brand/output/type-studies.html`).
- **Design system:** tokens are built by `03_design-system/output/_build_tokens.py`, which checks contrast. The 16 components are in `components.css`.

## Open thread: the logo (not blocking anything)
The current logo files in `02_brand/output/logo/` still use the old R2 clock with **Fraunces** lettering. The design system's header uses the clock plus live "Techne Hora" text until a new logo is chosen. Swapping it later is a file change.

Rounds explored, newest first:
1. **Bold round:** 5 dimensional vector marks. Page: https://claude.ai/artifact/9SnufmUkcS4a99hVPwBYfM; source: `logo/_explorations/bold/_bold.py`
   - Enamel Dial (name engraved on the bezel) · Rewind Ribbon (3D arrow) · **T-Hand** (the minute hand is a T) · **Sundial** (a T gnomon whose shadow is the hour hand) · Hourglass H
   - Recommended: **T-Hand as the logo, Sundial as the hero illustration.** The owner hasn't picked yet.
2. **Plex round:** 3 concepts where "Hora" steps back. Page: https://claude.ai/artifact/SmEJnfodr52nXDtGR43MRf; source: `logo/_explorations/plex/_concepts.py`
   - A: the clock replaces "Hora" · B: "Hora" fades letter by letter · C: "HORA" signed small on the dial (recommended in that round)
3. **Prompt pack for other tools:** `02_brand/output/logo-design-brief.md`, including a short prompt under 1,024 characters
   - Adobe Firefly declined that prompt, probably over the brand name "IBM Plex" or the description of a person's age. A Firefly-safe version was given in chat, with no brand names, people, or "no X" lists.
   - Ludo.ai produced the owner's favorite outside result (a clock as the O in "Hora"). Ludo has a REST API (beta) and an MCP server, not an official CLI. Setting it up was offered: an API key, or adding the MCP server.

The owner's direction: Hora can be subdued, replaced by the clock, or "lost in a good way." The owner also said the logo is the last thing to worry about.

**Next for the logo:** the owner picks a concept (or sets up Ludo for a comparison). Then refine it and build the full set: horizontal, stacked, icon, badge, light/dark, one-color, favicon, PNGs. After that, update `brand-spec.md` (Logo section; this reopens 02 only if the owner wants it recorded as a brand change) and the design system's Logos asset group.

## Uncommitted at handoff
- `stages/04_sitemap/` (new)
- `03_design-system/output/design-system.md` (status set to approved)
- `02_brand/output/logo-design-brief.md` (short prompt added)
- `02_brand/output/logo-pitches.html`, `logo-bold-round.html`, `logo/_explorations/plex/`, `logo/_explorations/bold/`

## Tooling notes
- The logo scripts need fontTools + brotli (to read the woff2 files). The Plex woff2 files are in `03_design-system/output/fonts/`.
- The old `_build_logo.py` needs the Fraunces variable font (not in the repo).
- Render checks use headless Chrome with an isolated `--user-data-dir`. Pages that load Google Fonts can hang headless Chrome here, so use local font files when rendering.
- Run `git config core.fileMode false` before trusting `git status`.
