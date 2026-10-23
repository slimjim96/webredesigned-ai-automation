---
status: draft
updated: 2026-10-20
---

# Launch checklist

Each box says who does it. **You** = the owner (accounts, secrets, DNS, deploys, anything sent to an outside service). **Claude** = changes in the repo and the checks. A box is checked only when it has been seen working, and from step 5 on, only on https://technehora.ai.

## 1. Blockers carried in
From 02_brand (open owner checks):
- [ ] **You:** register technehora.com (the redirect itself is step 5)
- [x] **You:** confirm the tagline, "The craft of getting your hours back." (or pick an alternate in `02_brand/output/brand-spec.md`)
- [ ] **You:** claim the @technehora handles: LinkedIn, Facebook, Instagram (Google Business Profile is step 6)
- [ ] **You:** quick USPTO search for "Techne Hora" in classes 35 (consulting) and 41 (training); anything close → stop and reopen 02

From 05_content and 06_build:
- [ ] **You:** read the privacy page (`/privacy`). It's a plain-language draft, not legal advice
- [ ] **You:** get the real business phone number (a Google Voice or similar line is fine)

## 2. Accounts and the Pages project
- [ ] **You:** Cal.com: a 20-minute event linked to your calendar. In the event's settings, send people who book outside the embed to `https://technehora.ai/book/thanks`. Note the link (`<user>/<event>`)
- [ ] **You:** Resend: add technehora.ai and add the DNS records it gives you (do this with step 5 if the domain isn't on Cloudflare yet); create an API key
- [ ] **You:** Cloudflare Turnstile: a widget for technehora.ai (and the `*.pages.dev` address while testing); note the site key and secret
- [ ] **You:** Cloudflare Pages: connect the GitHub repo. Root directory `site`, build command `npm run build`, output `dist`
- [ ] **You:** Pages environment variables (Production and Preview):
  - build: `PUBLIC_CAL_LINK`, `PUBLIC_TURNSTILE_SITE_KEY`
  - secrets: `RESEND_API_KEY`, `TURNSTILE_SECRET`
  - plain: `CONTACT_TO` (where form notes go), `CONTACT_FROM` (e.g. `Techne Hora <site@technehora.ai>`)
- [ ] **You:** Web Analytics: switch it on for the Pages project (then no `PUBLIC_CF_BEACON_TOKEN` is needed)
- [ ] **You:** first deploy; it lands on `<project>.pages.dev`

## 3. Test on `*.pages.dev`
- [ ] **You:** book a test call from a phone: the calendar loads, the booking finishes on "You're booked", the invite reaches your calendar. Cancel it after
- [ ] **You:** send the form once with an email and once with a phone number: both notes arrive at `CONTACT_TO`, and replying to the email one goes to the sender
- [ ] **You:** send the form empty: the field errors show
- [ ] **Claude:** check the function refuses a filled honeypot and a missing Turnstile token (curl against the `pages.dev` address)
- [ ] **You:** Web Analytics shows the visits from the tests

## 4. Launch values in the repo
- [ ] **Claude:** the real number into `site/src/site.config.ts` (`PHONE`, `PHONE_TEL`); the phone goes back into the structured data automatically
- [ ] **Claude:** `PRIVACY_UPDATED` set to the launch month
- [ ] **Claude:** Content-Security-Policy in `site/public/_headers`, sent as `Content-Security-Policy-Report-Only` first, then enforced once booking, the form and analytics show no violations. Starting point:
  `default-src 'self'; script-src 'self' 'unsafe-inline' https://app.cal.com https://challenges.cloudflare.com https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://app.cal.com; font-src 'self'; connect-src 'self' https://app.cal.com https://cloudflareinsights.com; frame-src https://app.cal.com https://cal.com https://challenges.cloudflare.com; form-action 'self'; base-uri 'self'; frame-ancestors 'none'`
- [ ] **Claude:** `LAUNCH=1 npm run check` passes in `site/`
- [ ] **You:** redeploy, then repeat the step 3 booking test with the CSP on

## 5. Domain
- [ ] **You:** technehora.ai on Cloudflare DNS (move the nameservers if it's registered elsewhere)
- [ ] **You:** add technehora.ai as the Pages project's custom domain; `www.technehora.ai` redirects to it
- [ ] **You:** technehora.com → `https://technehora.ai` with a permanent (301) redirect that keeps the path
- [ ] **You:** email on the domain: `hello@technehora.ai` receives mail (Cloudflare Email Routing to your inbox is enough), and the Resend records from step 2 show verified
- [ ] **Claude:** live checks on https://technehora.ai:
  - every page in `sitemap.xml` returns 200; a made-up address returns the 404 page with a 404 status
  - `http://`, `www.` and technehora.com all end on `https://technehora.ai/…`
  - `/robots.txt` and `/sitemap.xml` load; canonical URLs point at technehora.ai
  - security headers present (nosniff, referrer policy, frame options, CSP)
  - Lighthouse on Home, `/audit` and `/book` (phone): accessibility 100, SEO 100, performance 90+
  - an Open Graph preview of Home and `/audit` shows the share image
- [ ] **You:** click through on a phone and a desktop, light and dark, on the live address
- [ ] **You:** one real booking and one form note from a phone on the live address

## 6. Search and maps
- [ ] **You:** Google Search Console: verify technehora.ai (DNS record), submit `https://technehora.ai/sitemap.xml`
- [ ] **You:** Bing Webmaster Tools: import from Search Console
- [ ] **You:** Google Business Profile: service-area business (no street address shown), area = Western NY; name, phone and website exactly as on the site. Verification can take days
- [ ] **Claude:** once the profile exists, its link into the footer and `/about` (sitemap: "the strongest local signal")

## After launch (not blocking)
- [ ] Form sends and call taps aren't counted (Web Analytics counts page views only). Decide in a month whether that matters; Plausible is the option
- [ ] `/examples` once 2+ real demos exist; the Buffalo, Syracuse and Finger Lakes area pages as each has 150+ words true only of that area
- [ ] The 03 header-button fix (build notes) next time 03 is reopened

## Checked
- 2026-10-22: tagline confirmed as written by the owner; recorded in `02_brand/output/brand-spec.md`
