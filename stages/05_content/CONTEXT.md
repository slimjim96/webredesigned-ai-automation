# 05_content — every page's copy

One job: write the words for every page in the sitemap, section by section, so `06_build` only has to pour them into components. Every page reads like the straight-talking advisor from the brand spec and ends at "Book a free 20-minute call."

## Inputs
- Reference (every run): ../01_positioning/output/positioning.md (approved): offers, prices, service area, what proof exists
- Reference (every run): ../02_brand/output/brand-spec.md (approved): name, pronunciation, voice do/don't
- Reference (every run): ../04_sitemap/output/sitemap.md (approved): pages, URLs, sections in order, component per section, search phrases
- Reference (every run): ../03_design-system/output/ds/project/README.md, "Content fundamentals" (CTA labels, numbers, casing, no emoji)
- Reference (every run): ../../_shared/rules.md

Do NOT load: `docs/` (rule #1: nothing from it reaches the site as fact); layout, CSS, or component code.

## Process
1. Write the pages that set the voice first: Home, The audit, HVAC, Book (+ thanks). Owner reads those aloud before the rest are written.
2. Then the rest, in sitemap order. Each page is one file: `output/pages/<slug>.md` (`home.md`, `audit.md`, `industries-hvac.md`, `areas-rochester.md` …).
3. Each file: frontmatter (`status`, `url`, `title` ≤60 chars, `description` ≤155 chars, `search`), then one `##` block per sitemap section, named by its component, holding the exact copy: headings, body, button labels, link targets.
4. Facts only the owner can supply are marked `[[OWNER: what's needed]]`. Proof is never written; sitemap says proof slots are left out until real.
5. Sample data (the roadmap tables) carries "Sample · not a client" in the copy itself.

## Writing rules
- Outcomes before tools: "calls answered", "quotes out the same day", not "AI agents".
- Short sentences. Read it aloud: if you'd stumble, cut it.
- Numbers as numerals ("20 minutes", "$750", "5 fixes"). Hours in sample tables with one decimal.
- Primary button: "Book a free 20-minute call" (short form "Book a call" in the header and `CallBar`). Never "Submit", "Learn more", "Get started".
- "We" for Techne Hora, "you" for the owner. No emoji, no exclamation marks in headings.
- No promises the owner hasn't made: no hour counts, no guarantees, no named software support until confirmed.

## Outputs
- pages/*.md → output/ (each with frontmatter `status: draft | approved`)
- index.md → output/ (frontmatter `status`), lists every page file, its status, and the open `[[OWNER: …]]` items in one place

## Human check
Read each page aloud. Would you say it that way to an owner across their counter? Is every claim something you can stand behind on the call?
