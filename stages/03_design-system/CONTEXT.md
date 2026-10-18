# 03_design-system — tokens and components

One job: turn the approved brand into tokens and components that `06_build` can use as-is, so no page invents its own colors, sizes, or buttons.

## Inputs
- Reference (every run): ../02_brand/output/brand-spec.md (approved)
- Reference (every run): ../01_positioning/output/positioning.md (approved): the primary action, the audit offer, service area
- Reference (every run): ../../_shared/rules.md
- Working: ../02_brand/output/type-studies.html ("Engineered" pick), ../02_brand/output/logo/ (mark files)

Do NOT load: `docs/`; page lists or page copy (those belong in 04 and 05).

## Process
1. Edit tokens only in `output/_build_tokens.py`, then run `python3 output/_build_tokens.py`. It checks every contrast pair (text 4.5:1, marks 3:1, both themes) and refuses to write if one fails.
2. Component styles live in `output/components.css`; every value comes from a token (`var(--…)`).
3. Each component has a preview and guidelines in `output/ds/project/components/<Name>/`. The brand book is `output/ds/project/README.md`.
4. Publish the Design System page from `output/` (`project/components/bundle.css` → `components.css`, `project/fonts/*` → `fonts/*`, the rest from `ds/project/`). Send the index `ds/project/design-system.json` with `root` set to `output/ds`, so it lands at `project/design-system.json`.

## Outputs
- design-system.md → output/ (frontmatter `status: draft | approved`): summary, decisions, open items
- tokens.css → output/ (generated: the site's custom properties, light + dark, type classes, @font-face)
- components.css → output/ (the site's component styles)
- fonts/ → output/ (IBM Plex woff2, Latin)
- ds/project/ → output/ (the Design System page's source: README, tokens.json, component previews, cover)

## Human check
Open the Design System page. Click through the components in light and dark mode and on a phone. Would an HVAC owner know what to tap?
