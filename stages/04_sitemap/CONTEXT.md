# 04_sitemap — pages, sections, site functions

One job: decide every page the site has, what each one is for, which sections it holds (from the design system's components), and what the site has to *do*, so that every path a visitor takes ends at "Book a free 20-minute call."

## Inputs
- Reference (every run): ../01_positioning/output/positioning.md (approved): audience, verticals, offers, service area, primary action
- Reference (every run): ../03_design-system/output/design-system.md (approved) and its component list (`ds/project/components/`)
- Reference (every run): ../../_shared/rules.md

Do NOT load: `docs/`; page copy (that is `05_content`). Headlines in the sitemap are working labels, not final copy.

## Process
1. List the pages with their URLs, purpose, main visitor, and the search phrase each one targets.
2. For each page, list its sections in order, naming the component each uses. Every page ends at the primary action (`_shared/rules.md` #4).
3. Write the visitor journeys from the first visit to a booked call, and check that each one takes 3 clicks or fewer.
4. List site functions (booking, forms, analytics, structured data) with a recommended tool. The final choice is made in `06_build`.
5. Name any section the design system lacks. Small additions are built from existing tokens in 06; anything that changes tokens reopens 03.

## Outputs
- sitemap.md → output/ (frontmatter `status: draft | approved`)

## Human check
Walk each journey as that visitor, on your phone. Is the next step always obvious? Is any page there just to exist?
