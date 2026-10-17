# 02_brand — name, logo, color, type, voice

One job: give the positioning an identity an HVAC owner in Rochester would trust and remember.

## Inputs
- Reference (every run): ../01_positioning/output/positioning.md (approved)
- Reference (every run): ../../_shared/rules.md
- Working: owner's pick between directions, recorded directly into the output

Do NOT load: `docs/` (positioning already distilled it); layout, pages, or components (those belong in 03 and 04).

## Process
1. Propose three distinct directions, each with: name + alternates, tagline, logo concept, palette, type pairing, voice samples.
2. Every palette pair used for text passes WCAG 2.2 AA (`_shared/rules.md` #5); list the ratios.
3. Owner picks one direction (or mixes parts); collapse the spec to that direction and delete the others.
4. Name availability (domain, NY business name, social handles) is checked by a person before approval; record results as lines, not assumptions.

## Outputs
- brand-spec.md → output/ (frontmatter `status: draft | approved`)
- logo/ → output/ (SVG: mark, horizontal lockup; light and dark), rebuilt by `logo/_build_logo.py`
- brand-sheet.html → output/ (visual reference of the final brand)

## Human check
Pick one direction. Then imagine the logo on a van door and an invoice: would you put your name next to it?
