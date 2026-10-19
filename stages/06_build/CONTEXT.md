# 06_build — the site itself

One job: turn the approved design system, sitemap and copy into a working site in `../../site/`, so `07_launch` only has to point a domain at it.

## Inputs
- Reference (every run): ../03_design-system/output/ (approved): `tokens.css`, `components.css`, `fonts/`, component READMEs
- Reference (every run): ../04_sitemap/output/sitemap.md (approved): pages, URLs, site functions, the three gap components
- Reference (every run): ../05_content/output/pages/*.md (approved): every word on the site
- Reference (every run): ../02_brand/output/logo/ (approved): logo files, favicons
- Reference (every run): ../../_shared/rules.md

Do NOT load: `docs/`; the 05 preview (a review aid, not the site).

## Decisions (owner, 2026-10-18)
- **Stack:** Astro, static output. No UI framework; a few lines of plain JS for the menu, the booking embed and the form.
- **Hosting:** Cloudflare Pages, with one Pages Function for the fallback form.
- **Booking:** Cal.com, a 20-minute event embedded on `/book`.
- **Analytics:** Cloudflare Web Analytics (no cookies).

## Process
1. The site reads the 05 page files at build time (`site/src/lib/content.ts`). Copy is never retyped into the site; change a page in 05 (reopening it) and rebuild.
2. `[[BUILD: …]]` markers in the copy are settled in `site/src/site.config.ts`. Any `[[OWNER: …]]`, `[[PROOF NEEDED]]` or unknown `[[BUILD: …]]` stops the build.
3. Design-system CSS, fonts and logos are copied in by `site/scripts/sync.mjs` before every dev or build run, never edited in `site/`. Styles the design system doesn't have (the sitemap's gap components) live in `site/src/styles/site.css`, from tokens only.
4. Check with `npm run check` in `site/`: builds, then verifies every internal link, every page's title and description, and that no marker reached the HTML.

## Outputs
- `site/` → repo root: the Astro project
- build-notes.md → output/ (frontmatter `status: draft | approved`): what was built, settings and accounts launch needs, known gaps

## Human check
Click through every page on a phone and on a desktop, in light and dark mode. Book a test call and send the fallback form once the accounts exist.
