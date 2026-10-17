# The pipeline

The flow in one line: decide who we serve, give it an identity, systematize the look, map the site, write it, build it, ship it.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| `01_positioning` | define audience, offers, angle | `docs/` | `output/positioning.md` | would an SMB owner say "that's me"? |
| `02_brand` | name, logo, color, type, voice | 01 | `output/brand-spec.md` + `output/logo/` | pick one direction |
| `03_design-system` | turn brand into tokens/components | 02 | `output/design-system.md` | view the token preview page |
| `04_sitemap` | pages, sections, site functions | 01, 03 | `output/sitemap.md` | walk the visitor journey to "book a call" |
| `05_content` | write every page's copy | 01, 02, 04 | `output/pages/*.md` | read each page aloud |
| `06_build` | stack choice + implement | 03, 04, 05 | `site/` + `output/build-notes.md` | click through on phone and desktop |
| `07_launch` | domain, SEO, analytics, go-live | 06 | `output/launch-checklist.md` | every box checked on the live URL |

Approved outputs become reference material for the stages after them; nothing upstream is rewritten from downstream. If a later stage reveals that an earlier decision was wrong, reopen that stage (set `status: draft`) and flow forward again.

Factory (every stage): `_shared/rules.md`
Status: each output file's frontmatter `status: draft | approved`. A stage with no output file has not started.
