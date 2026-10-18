# RoadmapTable

A data table for roadmap figures: the fix, hours back per week, rough cost, difficulty, and a total row.

## Use
- Numbers right-aligned in Plex Mono tabular figures (`.num`), so columns line up.
- Always a `<caption>`. Any example data says so in the caption ("Sample roadmap · not a client"); real client numbers appear only with permission (`_shared/rules.md` #2).
- Below `bp-sm` add `th-table--stack`: rows become cards and each cell shows its `data-label`.
- Wrap in `th-table-wrap` so a wide table scrolls inside itself, never the page.
