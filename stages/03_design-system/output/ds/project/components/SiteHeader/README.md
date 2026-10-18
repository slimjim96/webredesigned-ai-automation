# SiteHeader

The top bar on every page: the logo (links home), up to four nav links, and one "Book a call" button.

## Use
- Below 960px (`bp-md`) the nav collapses to a **Menu** button (`target-min` square) that opens a panel with the links and a full-width primary button. Shown open in this preview.
- The menu button carries `aria-expanded` and `aria-controls`; the panel toggles with the `hidden` attribute.
- Mark `aria-current="page"` on the current link: it gets the ember underline.
- Nav labels here are samples; the real list comes from `04_sitemap`.

## Provides
`th-header` › `th-container` › `th-header__bar` with `th-header__logo`, `th-header__nav`, `th-header__cta`, `th-header__menu-btn`; then `th-header__panel`. The consumer supplies the logo (`technehora-lockup-horizontal-light.svg` at 48px tall) and the links.

## Don't
- Don't add a second button, a search box, or a phone number in the bar. The phone number lives in `CallBar` and the footer.
- Don't make it sticky on phones: the `CallBar` already keeps the action in reach.
