"""Build the Techne Hora design tokens from one source (this file).

Writes:
    tokens.css               the site's custom properties, light + dark, type classes, @font-face
    ds/project/tokens.json   the same tokens for the Design System page
    ds/project/tokens.css    that page's first compiled stylesheet (the page rewrites it on save)
and prints every contrast pair the system relies on. The build fails if a pair misses its floor.

    python3 _build_tokens.py
"""
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

# name: (light, dark, usage)
COLORS = [
    ('bg',               '#FAF7F0', '#111B31', 'Page background.'),
    ('surface',          '#FFFFFF', '#1B2A4A', 'Cards, inputs, the price card: anything that sits on `bg`.'),
    ('surface-sunken',   '#F1ECE1', '#0C1426', 'Alternate section bands and table header rows.'),
    ('tint',             '#F3D3C8', '#3A2630', 'Blush highlight: the "two hours back" wedge, callouts, a selected row. `ink` text only.'),
    ('inverse',          '#1B2A4A', '#0B1220', 'Navy bands: footer, closing call-to-action band.'),
    ('ink',              '#1B2A4A', '#FAF7F0', 'Headings and body text on `bg`, `surface`, `surface-sunken`, `tint`.'),
    ('ink-muted',        '#5C6170', '#B8BFCC', 'Secondary text, captions, help text on `bg`, `surface`, `surface-sunken`.'),
    ('on-inverse',       '#FAF7F0', '#FAF7F0', 'Text and links on `inverse` (links stay underlined).'),
    ('on-inverse-muted', '#B8BFCC', '#B8BFCC', 'Secondary text on `inverse`.'),
    ('primary',          '#A63D2A', '#A63D2A', 'Brick: the primary button fill. One primary button per view.'),
    ('primary-hover',    '#8C3222', '#8C3222', 'Primary button on hover and press.'),
    ('on-primary',       '#FFFFFF', '#FFFFFF', 'Text and icons on `primary` and `primary-hover`.'),
    ('link',             '#A63D2A', '#F2A08A', 'Inline links on `bg`, `surface`, `surface-sunken`. Always underlined.'),
    ('link-hover',       '#8C3222', '#FFC2B2', 'Inline links on hover.'),
    ('accent',           '#E07A5F', '#E07A5F', 'Ember: the rewind arrow and decorative marks only. Never text, never on `bg` as a meaningful mark.'),
    ('sage',             '#4E7060', '#8DB5A2', 'Secondary accent: step numerals, small icons, the "included" checks.'),
    ('border',           '#E2DCCF', '#2C3D63', 'Decorative dividers and card edges that carry no meaning.'),
    ('border-strong',    '#7A7F8C', '#7C869A', 'Input and checkbox borders, secondary button outline: 3:1 on `bg` and `surface`.'),
    ('focus',            '#1B2A4A', '#F2A08A', 'Focus ring: 2px solid, 2px offset, on every interactive element.'),
    ('success',          '#2F5D4A', '#8DB5A2', 'Success text and icon, always with a word ("Sent").'),
    ('danger',           '#9B1C1C', '#FF9C94', 'Error text, error border, `[[PROOF NEEDED]]` frames. Always with an icon and a word.'),
]

# Text pairs need 4.5:1; marks (borders, focus, icons) need 3:1.
TEXT_PAIRS = [('ink', g) for g in ('bg', 'surface', 'surface-sunken', 'tint')] + \
    [('ink-muted', g) for g in ('bg', 'surface', 'surface-sunken')] + \
    [('link', g) for g in ('bg', 'surface', 'surface-sunken')] + \
    [('link-hover', g) for g in ('bg', 'surface')] + \
    [('on-primary', 'primary'), ('on-primary', 'primary-hover'),
     ('on-inverse', 'inverse'), ('on-inverse-muted', 'inverse'),
     ('success', 'bg'), ('success', 'surface'), ('danger', 'bg'), ('danger', 'surface'),
     ('sage', 'bg'), ('sage', 'surface')]
MARK_PAIRS = [('border-strong', 'bg'), ('border-strong', 'surface'), ('focus', 'bg'), ('focus', 'surface'),
              ('focus', 'surface-sunken'), ('accent', 'inverse')]

FONTS = [  # family, file, weight, style
    ('IBM Plex Serif', 'fonts/IBMPlexSerif-600.woff2', '600', 'normal'),
    ('IBM Plex Sans', 'fonts/IBMPlexSans-Variable.woff2', '100 700', 'normal'),
    ('IBM Plex Sans', 'fonts/IBMPlexSans-400Italic.woff2', '400', 'italic'),
    ('IBM Plex Mono', 'fonts/IBMPlexMono-500.woff2', '500', 'normal'),
]
FAMILIES = {
    'serif': "'IBM Plex Serif', Georgia, 'Times New Roman', serif",
    'sans': "'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif",
    'mono': "'IBM Plex Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace",
}
# name, family, weight, (mobile px, desktop px), line height, letter spacing, usage, sample
TYPE = [
    ('Headings', 'serif', [
        ('text-display', 600, (36, 56), 1.08, '-0.015em', 'Page H1, one per page.', 'Missed calls are missed jobs.'),
        ('text-h2', 600, (28, 38), 1.15, '-0.01em', 'Section headings.', 'Five things to fix, in order.'),
        ('text-h3', 600, (21, 25), 1.25, '0', 'Card and step titles.', 'Answer every call, even at 9pm.'),
    ]),
    ('Text', 'sans', [
        ('text-lede', 400, (19, 21), 1.5, '0', 'The paragraph under an H1 or H2. Max 2 sentences.', 'We find where your hours go and give them back.'),
        ('text-body', 400, (17, 18), 1.6, '0', 'All running text. Max 68 characters a line.', 'A 90-minute visit, a written roadmap, and a 30-minute walkthrough.'),
        ('text-strong', 600, (17, 18), 1.6, '0', 'Subheads inside cards, table headers, emphasis.', 'Included in the audit'),
        ('text-small', 400, (15, 15), 1.47, '0', 'Captions, help text, footer. Never for paragraphs.', 'Fee credited if you book within 30 days.'),
        ('text-button', 600, (17, 17), 1.4, '0.005em', 'Button and nav labels.', 'Book a free 20-minute call'),
    ]),
    ('Data', 'mono', [
        ('text-label', 500, (13, 13), 1.3, '0.09em', 'Eyebrows and tags, set in capitals by the component.', 'HVAC · ROCHESTER, NY'),
        ('text-data', 500, (16, 16), 1.5, '0', 'Prices, hours, and table figures (tabular numbers).', '$750 · 17.0 hrs'),
    ]),
]
SPACING = [(1, 4, 'Icon to label gap.'), (2, 8, 'Tight stacks: label to input.'), (3, 12, 'List item gaps.'),
           (4, 16, 'Mobile side gutter, card padding on phones.'), (5, 24, 'Card padding, gaps in a grid.'),
           (6, 32, 'Between a heading block and its content.'), (7, 48, 'Section padding on phones.'),
           (8, 64, 'Between related sections.'), (9, 96, 'Section padding on desktop.')]
RADIUS = [('radius-sm', '4px', 'Inputs, tags, table cells.'), ('radius-md', '6px', 'Buttons, callouts.'),
          ('radius-lg', '10px', 'Cards and the price card.'), ('radius-pill', '999px', 'The clock mark container and status dots only.')]
SHADOW = [('shadow-1', '0 1px 2px rgba(27,42,74,0.08)', '0 1px 2px rgba(0,0,0,0.4)', 'Resting cards on `bg`.'),
          ('shadow-2', '0 8px 24px rgba(27,42,74,0.12)', '0 8px 24px rgba(0,0,0,0.45)', 'The price card and an open mobile menu.')]
SIZE = [('control-md', '48px', 'Default button and input height.'), ('control-sm', '40px', 'Compact buttons in tables and the header on desktop.'),
        ('target-min', '44px', 'Smallest tap target on any device (above the 24px WCAG 2.2 floor).'),
        ('container', '1120px', 'Max content width.'), ('measure', '68ch', 'Max running-text line length.'),
        ('bp-sm', '640px', 'Breakpoint: large phones and up.'), ('bp-md', '960px', 'Breakpoint: tablets landscape and up: desktop nav appears.'),
        ('bp-lg', '1200px', 'Breakpoint: wide desktop.')]
MOTION = [('motion-fast', '150ms'), ('motion-base', '250ms'), ('ease-out', 'cubic-bezier(0.2, 0.7, 0.2, 1)')]


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    a, b = sorted((lum(a), lum(b)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def check():
    val = {n: (l, d) for n, l, d, _ in COLORS}
    rows, bad = [], []
    for pairs, floor in ((TEXT_PAIRS, 4.5), (MARK_PAIRS, 3.0)):
        for fg, bg in pairs:
            r = [ratio(val[fg][t], val[bg][t]) for t in (0, 1)]
            rows.append((fg, bg, floor, *r))
            if min(r) < floor:
                bad.append(f'{fg} on {bg}: {min(r):.2f} < {floor}')
    return rows, bad


def fluid(lo, hi):
    if lo == hi:
        return f'{lo / 16:g}rem'
    # lo at 360px viewport, hi at 1200px
    slope = (hi - lo) / (1200 - 360)
    return f'clamp({lo / 16:g}rem, {(lo - slope * 360) / 16:.4f}rem + {slope * 100:.4f}vw, {hi / 16:g}rem)'


def css():
    light = '\n'.join(f'  --{n}: {l};' for n, l, d, _ in COLORS)
    dark = '\n'.join(f'  --{n}: {d};' for n, l, d, _ in COLORS if d != l)
    sh_l = '\n'.join(f'  --{n}: {l};' for n, l, d, _ in SHADOW)
    sh_d = '\n'.join(f'  --{n}: {d};' for n, l, d, _ in SHADOW)
    fam = '\n'.join(f'  --font-{k}: {v};' for k, v in FAMILIES.items())
    sp = '\n'.join(f'  --space-{n}: {v}px;' for n, v, _ in SPACING)
    rd = '\n'.join(f'  --{n}: {v};' for n, v, _ in RADIUS)
    sz = '\n'.join(f'  --{n}: {v};' for n, v, _ in SIZE)
    mo = '\n'.join(f'  --{n}: {v};' for n, v in MOTION)
    faces = '\n'.join(
        f"@font-face {{ font-family: '{f}'; src: url('{p}') format('woff2'); font-weight: {w}; font-style: {s}; font-display: swap; }}"
        for f, p, w, s in FONTS)
    classes = []
    for _, family, styles in TYPE:
        for n, w, (lo, hi), lh, ls, *_ in styles:
            extra = ' font-variant-numeric: tabular-nums;' if n == 'text-data' else ''
            extra += ' text-transform: uppercase;' if n == 'text-label' else ''
            extra += ' text-wrap: balance;' if family == 'serif' else ''
            classes.append(f'.{n} {{ font-family: var(--font-{family}); font-weight: {w}; font-size: {fluid(lo, hi)}; '
                           f'line-height: {lh}; letter-spacing: {ls};{extra} }}')
    return f"""/* Techne Hora — generated by _build_tokens.py. Edit that file, not this one. */
{faces}

:root {{
{light}
{sh_l}
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{dark}
{sh_d}
    color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
{dark}
{sh_d}
  color-scheme: dark;
}}
:root {{
{fam}
{sp}
{rd}
{sz}
{mo}
}}
@media (prefers-reduced-motion: reduce) {{
  :root {{ --motion-fast: 0ms; --motion-base: 0ms; }}
}}

{chr(10).join(classes)}
"""


def ds_css():
    """tokens.css as the Design System page compiles it (data-theme only, no media query)."""
    light = '\n'.join(f'  --{n}: {l.lower()};' for n, l, d, _ in COLORS) + '\n' + '\n'.join(f'  --{n}: {l};' for n, l, d, _ in SHADOW)
    dark = '\n'.join(f'  --{n}: {d.lower()};' for n, l, d, _ in COLORS if d != l) + '\n' + '\n'.join(f'  --{n}: {d};' for n, l, d, _ in SHADOW)
    other = [f'  --space-{n}: {v}px;' for n, v, _ in SPACING] + [f'  --{n}: {v};' for n, v, _ in RADIUS] + \
        [f'  --{n}: {v};' for n, v, _ in SIZE] + [f'  --{n}: {v};' for n, v in MOTION] + \
        [f'  --font-{k}: {v};' for k, v in FAMILIES.items()]
    site = css()
    faces = site[site.index('@font-face'):site.index(':root')]
    classes = site[site.index('.text-display'):]
    return ('/* Techne Hora — generated from tokens.json */\n'
            f':root, [data-theme="light"] {{\n{light}\n}}\n[data-theme="dark"] {{\n{dark}\n  color-scheme: dark;\n}}\n'
            f':root {{\n' + '\n'.join(other) + '\n}\n' + classes + faces)


def tokens_json():
    groups = []
    for gname, family, styles in TYPE:
        groups.append({'name': gname, 'family': family, 'styles': [
            {'name': n, 'fontSize': f'{hi}px', 'lineHeight': lh, 'fontWeight': w, 'letterSpacing': ls,
             'usage': f'{u} {lo}px on phones, {hi}px on desktop.' if lo != hi else u, 'sample': s}
            for n, w, (lo, hi), lh, ls, u, s in styles]})
    return {
        'name': 'Techne Hora', 'version': 1, 'meta': {'source': 'stages/03_design-system/output/_build_tokens.py'},
        'color': {'themes': [{'id': 'light', 'name': 'Light'}, {'id': 'dark', 'name': 'Dark'}],
                  'tokens': [{'name': n, 'value': {'light': l.lower(), 'dark': d.lower()}, 'usage': u} for n, l, d, u in COLORS]},
        'type': {'fonts': [{'family': f, 'file': p, 'weight': w, 'style': s} for f, p, w, s in FONTS],
                 'families': {k: v.replace("'", '"') for k, v in FAMILIES.items()}, 'groups': groups},
        'spacing': {'tokens': [{'name': f'space-{n}', 'value': f'{v}px', 'usage': u} for n, v, u in SPACING]},
        'radius': {'tokens': [{'name': n, 'value': v, 'usage': u} for n, v, u in RADIUS]},
        'shadow': {'tokens': [{'name': n, 'value': {'light': l, 'dark': d}, 'usage': u} for n, l, d, u in SHADOW]},
        'size': {'note': 'Control heights, layout widths, and breakpoints (breakpoints are documentation: CSS media queries cannot read custom properties).',
                 'tokens': [{'name': n, 'value': v, 'usage': u} for n, v, u in SIZE]},
    }


if __name__ == '__main__':
    rows, bad = check()
    print(f"{'pair':38} floor  light   dark")
    for fg, bg, floor, l, d in rows:
        print(f'{fg + " on " + bg:38} {floor:>4}  {l:5.2f}  {d:5.2f}')
    if bad:
        raise SystemExit('contrast failures:\n  ' + '\n  '.join(bad))
    with open(os.path.join(OUT, 'tokens.css'), 'w') as fh:
        fh.write(css())
    os.makedirs(os.path.join(OUT, 'ds', 'project'), exist_ok=True)
    with open(os.path.join(OUT, 'ds', 'project', 'tokens.json'), 'w') as fh:
        json.dump(tokens_json(), fh, indent=2)
        fh.write('\n')
    with open(os.path.join(OUT, 'ds', 'project', 'tokens.css'), 'w') as fh:
        fh.write(ds_css())
    print('wrote tokens.css, ds/project/tokens.json, ds/project/tokens.css')
