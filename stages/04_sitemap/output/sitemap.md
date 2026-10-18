---
status: approved
updated: 2026-10-18
---

# Sitemap: technehora.ai

15 pages at launch, plus `/book/thanks` and the 404. Three more go live when their content is ready: `/examples` (2+ real demos) and the Buffalo, Syracuse and Finger Lakes area pages (150+ words true only of that area). Each page has one primary action: **Book a free 20-minute call** (`/book`). Headlines below are working labels; `05_content` writes the real copy. Component names are from the design system (`03_design-system`).

## Structure

```
/                         Home
├── /audit                The AI audit ($750)             ← the offer everything points to
├── /services             Training & builds (hub)
│   ├── /services/training        Workshops & team training
│   └── /services/custom-builds   Custom skills & builds
├── /industries           Who we help (hub)
│   ├── /industries/hvac          HVAC, plumbing & electrical   (lead vertical)
│   ├── /industries/restaurants   Restaurants
│   └── /industries/local-services  Other local businesses (TODO: third vertical; generic until chosen, then 301 to its own slug)
├── /areas/rochester      Rochester & Monroe County       (footer + local search only; at launch)
├── /areas/buffalo        Buffalo                         (when ready)
├── /areas/syracuse       Syracuse                        (when ready)
├── /areas/finger-lakes   Finger Lakes                    (when ready)
├── /about                About (the owner, how we work, "by Web Redesigned")
├── /examples             Examples of our builds          (launches only with 2+ real demos)
├── /faq                  Questions owners ask
├── /book                 Book a free 20-minute call
│   └── /book/thanks      You're booked (not indexed)
├── /privacy              Privacy
└── /accessibility        Accessibility statement
```

**Header nav (4 links + button):** The audit · Training & builds · Who we help · About · [Book a call]
**Footer:** Contact (phone, email, Rochester NY) · Where we work (the area pages that are live, the other regions as plain text, + "Remote, anywhere") · Site (Services, Industries, Examples, FAQ, Privacy, Accessibility) · "© Techne Hora, by Web Redesigned"
**Phones:** `CallBar` on every page except `/book`, with "Call" and "Book a call".

## Pages

### Home `/`
- **For:** any owner arriving from a referral, the van, a business card, or a search for the brand.
- **Job:** in 5 seconds say who it's for and what happens next; send them to the audit or straight to booking.
- **Search:** "AI consultant Rochester NY", "AI help for small business Rochester"
- **Sections:**
  1. `Hero`: who it's for and the problem (calls, quotes, paperwork), primary button, service-area note
  2. `SectionHeading` + `ServiceCard` ×3: Find the time leaks (audit) · Train your team · Build what pays back
  3. `SectionHeading` + `ServiceCard` ×3: Who we help: HVAC · Restaurants · Local businesses
  4. `Steps`: Book a free call → Get your roadmap → Fix it, then run it
  5. `PriceCard`: the audit, $750, with the credit note
  6. `ProofSlot`: left out at launch; added when a real client quote exists (see Proof below)
  7. `FAQ` (4 questions, linking to `/faq` for more)
  8. `CTABand`

### The AI audit `/audit`
- **For:** an owner who is interested and wants to know exactly what they get and what it costs.
- **Job:** remove every reason not to book: what happens, how long, what they receive, the price, the credit.
- **Search:** "AI audit small business", "AI assessment Rochester"
- **Sections:**
  1. `Hero` (no art): "Five things to fix, in order." + primary button
  2. `Steps`: the free call → 90-minute visit → written roadmap → 30-minute walkthrough (4 steps)
  3. `SectionHeading` + `RoadmapTable`: what the roadmap looks like ("Sample · not a client")
  4. `PriceCard`
  5. `Callout`: the fee is credited toward a workshop or build within 30 days
  6. `SectionHeading` + short list: what we look at (calls, scheduling, quoting, invoices, the tools you already pay for)
  7. `FAQ`: audit-specific (what if you find nothing, on-site vs video, what to prepare)
  8. `CTABand`

### Training & builds `/services`
- **For:** owners who already know what they need, or who come back after the audit.
- **Job:** show the whole path in one look, so an owner sees where training and builds fit and why the audit comes first.
- **Sections:** `Hero` (no art) · `Steps`: the path, Audit → Train your team → Build what pays back, each step one line on what you get and how it's priced ($750 / quoted from your roadmap / quoted from your roadmap) · `ServiceCard` ×2 (Training, Custom builds) linking down · `Callout` "The audit fee is credited toward training or a build booked within 30 days" · `CTABand`

### Workshops & team training `/services/training`
- **Search:** "Copilot training small business", "ChatGPT Claude training for staff Rochester"
- **Sections:** `Hero` · what a workshop covers, using your real tasks (estimates, emails, schedules, menus) · formats (half-day on-site, remote sessions, follow-up office hours; TODO: owner confirms formats) · `Steps` (pick tasks → hands-on session → cheat sheets + follow-up) · "Quoted from your roadmap" note (no public price) · `FAQ` · `CTABand`

### Custom skills & builds `/services/custom-builds`
- **Search:** "custom AI tools small business", "AI automation HVAC"
- **Sections:** `Hero` · `ServiceCard` ×3–6 kinds of build (missed-call text-back, quote drafts, intake forms, directories, follow-ups) described as outcomes · `Steps` (scope from the roadmap → build → train the team → hand over) · link to `/examples` once live · "Quoted from your roadmap" · `FAQ` · `CTABand`

### Who we help `/industries`
- **For:** an owner who isn't sure we work with businesses like theirs.
- **Job:** let them recognize their own week in under 10 seconds, then go to their page or straight to booking.
- **Sections:** `Hero` (no art) · per vertical, a short "Is this you?" block: 3 problems from that vertical's `ProblemList` + a link to its page (HVAC, Restaurants, Other local businesses) · one line for everyone else: "Not on the list? If your phone, quotes or schedule eat your week, the free call will tell us both in 20 minutes." · `CTABand`

### HVAC, plumbing & electrical `/industries/hvac`
- **For:** the lead buyer. A trades owner who answers the phone from a crawlspace and writes quotes at 10pm.
- **Search:** "AI for HVAC companies", "HVAC answering automation", "plumbing business AI Rochester"
- **Sections:**
  1. `Hero`: "Missed calls are missed jobs." + primary button
  2. **Problems we fix** list (new section, see gaps): missed calls, after-hours quotes, scheduling, invoice chasing, seasonal rushes
  3. `RoadmapTable`: a sample HVAC roadmap ("Sample · not a client")
  4. `Steps`: how an engagement runs
  5. `PriceCard`
  6. `ProofSlot`: left out at launch; added when real
  7. `FAQ`: trade-specific (works with ServiceTitan/Housecall Pro? TODO: owner confirms which tools are supported; no promises)
  8. `CTABand`

### Restaurants `/industries/restaurants`
- **Search:** "AI for restaurants", "restaurant scheduling automation Rochester"
- Same skeleton as HVAC. Problems: phone orders and reservations during the rush, staff scheduling, supplier orders, reviews and replies, menu and allergen updates. Sample roadmap marked as a sample.

### Other local businesses `/industries/local-services`
- TODO: becomes the third vertical's page once chosen (candidates: home services, auto repair, salons). Until then, generic "local service business" copy in the same skeleton.

### Area pages `/areas/rochester`, `/areas/buffalo`, `/areas/syracuse`, `/areas/finger-lakes`
- **For:** local search ("AI consultant Buffalo"). Linked from the footer and `/about`, not the header.
- **Job:** prove we're really local: on-site visits, travel area, what an on-site audit looks like there.
- **Sections:** `Hero` (no art) · on-site details (towns covered, travel, how visits work) · `ServiceCard` ×3 offers · `ProofSlot` (only once a local client result is real) · `FAQ` · `CTABand`
- **Rule:** each page needs at least 150 words that are true only of that area. Four near-identical pages read to Google as doorway pages and can hurt the whole site. If a page can't meet that at launch, keep it in drafts and list the area on `/about` instead. **Decided 2026-10-18:** only Rochester launches; the other three follow as each meets the rule.

### About `/about`
- **For:** the owner checking who they'd be letting into their business.
- **Sections:** `Hero` (photo of the owner when available, else the mark) · the story and why the name (the Techne/Hora line from the brand spec) · how we work (train, don't just install) · background (TODO: years, roles, wording owner is comfortable with) · where we work (links to area pages) · "Techne Hora is a service of Web Redesigned" · `CTABand`

### Examples `/examples` (launch only with 2+ real demos)
- Real things the owner built: e.g. the employee and client directory (described generically, no employer name or data unless cleared), 2–3 GitHub projects (TODO: pick). Each as a `ServiceCard`: the problem, what was built, the hours or errors it saved (real numbers only).
- If fewer than 2 are ready at launch, the page and its links stay out; `/services/custom-builds` describes build types instead.

### FAQ `/faq`
- 10–15 questions grouped (The call · The audit · Training · Builds · Cost & data). `FAQ` component per group, then `CTABand`. FAQPage markup is optional: since 2023 Google shows FAQ rich results only for government and health sites, so it won't add search visibility.
- Must include: "What happens to my data?" (plain answer about which tools see what; TODO: owner confirms practices).

### Book a call `/book`
- **Job:** the finish line. Nothing else competes on this page: no `CTABand`, no `CallBar`.
- **Sections:** short `SectionHeading` ("20 minutes, no pitch deck") · scheduler embed (new section, see gaps) · fallback `FormField` form (name, business, phone or email, "What eats most of your week?") · phone number and email as plain text · what happens next (3 bullets)
- `/book/thanks`: confirms the time, says what to expect, and offers one optional prep question. `noindex`.

### Privacy `/privacy` and Accessibility `/accessibility`
- Plain-language privacy (what the form and analytics collect, who sees it). TODO: owner reviews before launch.
- Accessibility statement: WCAG 2.2 AA target, how to report a problem.
- Both end with a small `CTABand`.

### 404
- One line, links to Home, The audit, and Book a call.

## Visitor journeys (each ends at `/book` within 3 clicks)

| Visitor | Arrives at | Path | Clicks to book |
|---|---|---|---|
| HVAC owner searching on a phone at 9pm | `/industries/hvac` | reads problems → sample roadmap → `CallBar` "Book a call" | 1 |
| Referred by a friend, types technehora.ai | `/` | Hero → `/audit` → price card button | 2 |
| Restaurant owner from a Facebook post | `/industries/restaurants` | problems → `PriceCard` button | 1 |
| Cautious owner who wants to know who you are | `/` | About → `CTABand` | 2 |
| Rochester owner searching locally | `/areas/rochester` | on-site details → `CTABand` | 1 |
| Owner unsure we serve their kind of business | `/industries` | "Is this you?" → their vertical page → `CallBar` | 2 |
| Past audit client ready for training | `/services/training` | `CTABand` (or calls the number) | 1 |
| Owner who would rather call than click | any page | `CallBar` "Call" / footer number | 0 (phone) |

## Site functions

| Function | Recommendation | Why |
|---|---|---|
| Booking | **Cal.com** (free plan) with a 20-minute event type, linked to the owner's calendar; Calendly as the alternative | can be embedded or linked; open source; no forced branding at the free tier. TODO: confirm in 06 |
| Fallback form | the site's own form → email to the owner, honeypot + Cloudflare Turnstile against spam | some owners won't use a scheduler |
| Click to call | `tel:` link in `CallBar` and footer | most trades owners call |
| Analytics | **Plausible** or Cloudflare Web Analytics (no cookie banner needed) | counts visits and bookings without tracking people; keeps the privacy page simple |
| Conversion events | "booking started", "booking completed", "form sent", "call tapped" | the only numbers that matter |
| Structured data | `ProfessionalService` (LocalBusiness) with service area on every page; `Service` on offer pages | local search; `ProfessionalService` with `areaServed` is what feeds local results |
| SEO basics | unique title and description per page, `sitemap.xml`, `robots.txt`, canonical URLs, Open Graph images (mark + page title) | |
| Google Business Profile | link from footer and `/about`; same name, address area, and phone everywhere | the strongest local signal |
| Email | hello@technehora.ai (TODO: set up mail on the domain) | used in footer, form, booking emails |
| Redirect | technehora.com → technehora.ai (carried from 02) | |

Out of scope at launch: a blog, client login, live chat, newsletter, pricing for training and builds.

## Gaps in the design system (built in 06 from existing tokens)
- **ProblemList:** the "problems we fix" list on vertical pages: a short problem in bold, one line of what changes. A styled `<ul>` using `text-strong`, `ink-muted`, `space-*`, `border`.
- **BookingEmbed:** a container for the scheduler on `/book` that sizes the embed, holds a loading state, and shows the fallback form if the embed fails.
- **Breadcrumbs:** on child pages (`/services/…`, `/industries/…`, `/areas/…`), text-small with `link`.
None of these need new tokens, so 03 stays approved.

## Proof (decided 2026-10-18)
No client results exist yet, so every `ProofSlot` is **left out at launch**, not shown as a placeholder. The pages lean on what is true today: the free call, the credited audit fee, and the sample roadmap marked "Sample · not a client". Each slot comes back when a real quote or result exists (`_shared/rules.md` #2).

## Open items
- TODO: third vertical
- TODO: which demos can go on `/examples`
- TODO: workshop formats; tools supported for trades (e.g. ServiceTitan, Housecall Pro) without overpromising
- TODO: owner photo for Hero/About
- TODO: data-handling answer for the FAQ and privacy page
- TODO: business phone number for the `CallBar`, footer and structured data (the design-system previews use a 555 sample)
