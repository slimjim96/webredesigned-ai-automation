Techne Hora is a one-person AI consultancy in Rochester, NY, that helps owners of HVAC, plumbing, electrical and restaurant businesses get hours back. The site has one job: get a busy owner to **book a free 20-minute call**. Everything here serves that: plain words, one obvious button, pages that work on a phone in a truck.

Load `tokens.css`, then `components/bundle.css`, and put `class="th-root"` on `<body>`. Every component class starts with `th-`; every type style is a `text-*` class.

## Content fundamentals

- **Voice:** a straight-talking advisor. Short sentences, plain words, outcomes before tools. "Missed calls are missed jobs.", not "Leverage AI-powered omnichannel engagement."
- **Person:** "we" for Techne Hora, "you" for the owner. Name the reader's world: calls, quotes, jobs, crews, invoices, the dinner rush.
- **Casing:** sentence case for headings, buttons and nav. Capitals only through `text-label` (eyebrows, tags), which the component sets.
- **Jargon:** say "hours", "calls", "quotes". Avoid "agents", "LLMs", "MCP", "workflow automation" unless the reader already uses the word.
- **Numbers:** write them as numbers ("5 fixes", "20 minutes", "$750"). Hours with one decimal in tables ("4.5").
- **Proof:** real or absent. A missing testimonial is a visible `[[PROOF NEEDED]]` frame (`ProofSlot`), never a placeholder that looks real. Sample data says "Sample · not a client".
- **Primary action label:** "Book a free 20-minute call" (short form "Book a call"). Never "Submit", "Learn more", "Get started".
- **No emoji** anywhere on the site.

## Color

The brand is navy and cream with one brick action color. Each theme reads the same tokens; dark mode follows the visitor's system setting.

- `bg` is the page; `surface` lifts cards and inputs off it; `surface-sunken` bands every other section; `inverse` is the navy footer and closing band.
- Text: `ink` for headings and body, `ink-muted` for secondary text. On `inverse`, use `on-inverse` and `on-inverse-muted`.
- `primary` (brick) fills the one primary button and nothing else. Inline links use `link` and are always underlined, so color is never the only cue.
- `accent` (ember) is graphic only: the rewind arrow, the eyebrow dot, the active nav underline. Never text.
- `tint` (blush) marks something good to notice: the credit note, a callout, an icon tile. `ink` text only.
- `sage` is the quiet second accent: step numerals and "included" checks.
- `success` and `danger` always come with a word and an icon, never color alone.
- Every text pair meets WCAG 2.2 AA (4.5:1) in both themes, and borders, focus rings and icons meet 3:1. `_build_tokens.py` checks every pair and refuses to build if one fails.

## Type

IBM Plex in three cuts. It reads as engineered but warm, matching an owner who builds things.

- **IBM Plex Serif 600** for headings: `text-display` (the H1, once per page), `text-h2`, `text-h3`.
- **IBM Plex Sans** (variable, 400 and 600) for everything people read: `text-lede`, `text-body`, `text-strong`, `text-small`, `text-button`.
- **IBM Plex Mono 500** for details: `text-label` (eyebrows, tags) and `text-data` (prices, hours, table figures, always tabular numerals).
- Body text is 17px on phones and 18px on desktop, never smaller for paragraphs; captions are 15px. Running text stops at `measure` (68 characters).
- Headings scale fluidly between phone and desktop sizes and balance their line breaks.
- Self-host the four `.woff2` files in `fonts/` (about 105 KB total, Latin only), with `font-display: swap`.

## Spacing and layout

- A 4px base: `space-1` (4) through `space-9` (96). Gaps between siblings come from `gap`, not margins.
- Content sits in `th-container`: up to `container` (1120px) wide with a `space-4` (16px) gutter on phones and `space-6` (32px) from `bp-sm`.
- Sections pad `space-7` on phones and `space-9` on desktop. Alternate `bg` and `surface-sunken` bands to separate them; don't stack rules.
- Breakpoints: `bp-sm` 640px, `bp-md` 960px (desktop nav, three-column steps), `bp-lg` 1200px. Design at 360px first.
- Left-aligned text everywhere; nothing centered except the stacked logo.

## Shape, borders and depth

- Small radii: `radius-sm` (4px) for inputs and tags, `radius-md` (6px) for buttons and callouts, `radius-lg` (10px) for cards. `radius-pill` only for round marks.
- `border` draws decorative edges; `border-strong` draws edges that mean something (inputs, the secondary button), at 3:1.
- Two shadows only: `shadow-1` for resting cards, `shadow-2` for the price card and an open menu.
- No gradients in UI. The full-color clock mark keeps its own subtle shading.

## Motion

- `motion-fast` (150ms) for hover and color changes, `motion-base` (250ms) for the FAQ chevron and the menu, both on `ease-out`.
- Nothing moves on its own. With `prefers-reduced-motion`, both durations drop to 0.

## States and accessibility

- **Focus:** a 2px solid `focus` ring with a 2px offset on every interactive element (`on-inverse` on navy bands). Never remove it.
- **Targets:** at least `target-min` (44px) on every tap target; buttons and inputs are `control-md` (48px).
- **Hover:** the primary button darkens to `primary-hover`, the secondary button's border turns `ink`, links thicken their underline.
- **Disabled:** 55% opacity with a "not allowed" cursor and a label that says why ("Sending…").
- **Errors:** `danger` border, an alert icon, and a sentence that says how to fix the input.
- Everything works at 360px wide with no sideways scroll; tables scroll inside `th-table-wrap` or stack.

## Iconography

- **Lucide** (ISC license), outline style: 24px grid, `stroke-width` 1.75, round caps and joins, `currentColor`. Install `lucide-static` or copy the SVGs in `06_build`; the previews inline the same paths.
- Icons used now: `clock`, `calendar`, `check`, `arrow-right`, `chevron-down`, `menu`, `info`, `circle-alert`, `users`, `wrench`, `search`.
- Icons beside text are decorative (`aria-hidden="true"`). An icon-only button carries a visually hidden label (the Menu button does).
- No emoji, no robots, brains, circuit boards or sparkle icons.

## Logo

- The mark is the clock wound back: hands at 10 and 12, the last two hours tinted, a counter-clockwise ember arrow. Files are in the **Logos** asset group.
- In the header use the mark at 36px plus "Techne Hora" in Plex Serif 600, until the redesigned lockup arrives (see `stages/02_brand/output/logo-design-brief.md`). The current lockup files still use the older Fraunces lettering.
- Clear space: the clock face's radius on every side. Minimum 24px; below that use `favicon.svg`.

## Imagery

- Real photos only: the owner, real job sites, real kitchens, with permission. No stock handshakes, no glowing AI art.
- Until photos exist, use the clock mark or no image.
