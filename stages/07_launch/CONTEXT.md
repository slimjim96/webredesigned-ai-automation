# 07_launch — go live

One job: put the approved site on technehora.ai, prove every part of it works there, and get it in front of search and maps. The stage is done when every box in the checklist is checked **on the live URL**, not on a laptop or a preview.

## Inputs
- Reference (every run): ../06_build/output/build-notes.md (approved): accounts, environment variables, launch blockers, known gaps
- Reference (every run): ../../site/: the site as built
- Reference (every run): ../02_brand/output/brand-spec.md (approved): the open owner checks, which block this stage
- Reference (every run): ../04_sitemap/output/sitemap.md (approved): site functions, SEO basics, Google Business Profile
- Reference (every run): ../../_shared/rules.md

Do NOT load: `docs/`; the 05 and 06 preview artifacts (review aids, not the site).

## Who does what
- **The owner** creates every account, enters every secret, touches DNS and presses deploy. Nothing outward-facing (accounts, DNS, deploys, submissions to Google) is done for them.
- **Claude** makes the changes in the repo once the owner supplies the values (the real phone number, launch month, the CSP after booking is tested), runs the checks and keeps the checklist current.

## Process
1. Clear the blockers carried in from 02, 05 and 06.
2. Accounts and the Cloudflare Pages project; the first deploy goes to the `*.pages.dev` address.
3. Test booking, the form and analytics end to end on `*.pages.dev`.
4. Put the launch values in the repo; `LAUNCH=1 npm run check` passes.
5. Point the domain; run the live checks on https://technehora.ai.
6. Search Console, Bing, Google Business Profile, handles.

If a check fails because of copy or a page design, reopen that stage (`status: draft`) instead of patching it here. Launch values that 06 left as config (`site.config.ts`, `public/_headers`) are this stage's to set.

## Outputs
- launch-checklist.md → output/ (frontmatter `status: draft | approved`): every step, who does it, and how it was checked

## Human check
Every box checked on the live URL. The owner books one real test call and sends the form once, from a phone.
