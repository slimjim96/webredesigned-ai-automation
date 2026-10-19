"""Build preview/: every page in pages/*.md laid out with the real design system, as one clickable site.

A review aid for 05_content (read the copy where it will live), not the site itself: `06_build` makes that.
Pure standard library:
    python _build_preview.py
Writes preview/index.html and copies tokens.css, components.css, the fonts and three logo files beside it.
Pages link to each other by #<slug>; [[OWNER: …]] and [[BUILD: …]] items show as highlighted marks.
"""
import html, os, re, shutil

OUT = os.path.dirname(os.path.abspath(__file__))
STAGES = os.path.normpath(os.path.join(OUT, '../..'))
DS = os.path.join(STAGES, '03_design-system/output')
LOGO = os.path.join(STAGES, '02_brand/output/logo')
PREVIEW = os.path.join(OUT, 'preview')

ORDER = ['home', 'audit', 'services', 'services-training', 'services-custom-builds', 'industries', 'industries-hvac',
         'industries-restaurants', 'industries-local-services', 'areas-rochester', 'about', 'faq', 'book', 'book-thanks',
         'privacy', 'accessibility', '404']

# Lucide outline icons (ISC), the design system's set
ICONS = {
    'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'wrench': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    'calendar': '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'chevron': '<path d="m6 9 6 6 6-6"/>',
    'menu': '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
}
def icon(name): return f'<svg class="th-icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


# ---------------------------------------------------------------- reading the page files
def load(slug):
    text = open(os.path.join(OUT, 'pages', f'{slug}.md')).read()
    fm, body = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S).groups()
    meta = dict(re.findall(r'^(\w+): (.*)$', fm, re.M))
    title = re.search(r'^# (.*)$', body, re.M).group(1)
    pre, *chunks = re.split(r'^## ', body, flags=re.M)
    notes = [l for l in pre.splitlines() if l.strip() and not l.startswith('# ')]
    sections = []
    for chunk in chunks:
        head, _, rest = chunk.partition('\n')
        sections.append((head.strip(), parse(rest)))
    return dict(slug=slug, meta=meta, title=title, notes=notes, sections=sections)

def parse(block):
    """A section's lines -> fields (**Key:** value), lists under a key, tables, numbered items, bullets, text."""
    s = dict(fields={}, lists={}, tables=[], items=[], bullets=[], text=[])
    lines = block.splitlines(); i = 0; cur_list = None; table = []
    while i < len(lines):
        l = lines[i]
        if l.startswith('|'):
            table.append(l); i += 1
            if i == len(lines) or not lines[i].startswith('|'):
                rows = [[c.strip() for c in r.strip('|').split('|')] for r in table if not re.match(r'^\|[\s:|-]+\|$', r)]
                s['tables'].append(rows); table = []
            continue
        m = re.match(r'^- \*\*(.+?):\*\*\s*(.*)$', l)
        if m:
            key, val = m.groups(); cur_list = None
            if val: s['fields'][key] = val
            else: cur_list = s['lists'].setdefault(key, [])
            i += 1; continue
        m = re.match(r'^\s{2,}- (.*)$', l)
        if m and cur_list is not None:
            cur_list.append(m.group(1)); i += 1; continue
        m = re.match(r'^\d+\. \*\*(.+?)\*\*\s*(.*)$', l)
        if m:
            t, rest = m.groups(); i += 1; extra = []
            while i < len(lines) and re.match(r'^\s{3,}\S', lines[i]):
                extra.append(lines[i].strip()); i += 1
            s['items'].append((t, rest, ' '.join(extra))); cur_list = None; continue
        m = re.match(r'^- (.*)$', l)
        if m:
            s['bullets'].append(m.group(1)); cur_list = None; i += 1; continue
        if l.strip():
            s['text'].append(l.strip())
        i += 1
    return s


# ---------------------------------------------------------------- inline formatting
URLS = {}  # url -> slug, filled once every page is loaded

def href(url):
    url = url.strip().strip('`').strip()
    if url in URLS: return '#' + URLS[url]
    return '#missing'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[\[(OWNER|BUILD): (.*?)\]\]', lambda m: f'<mark class="rv rv--{m.group(1).lower()}"><b>{m.group(1).title()}:</b> {m.group(2)}</mark>', t)
    t = re.sub(r'\[([^\]]+)\]\((/[^)]*)\)', lambda m: f'<a href="{href(m.group(2))}">{m.group(1)}</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)\*(?!\w)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t

def action(val):
    """'Label → `/url`' -> (label, href)."""
    label, _, url = val.partition('→')
    return label.strip(), href(url)

def btn(val, kind='primary', block=False):
    label, h = action(val)
    return f'<a class="th-btn th-btn--{kind}{" th-btn--block" if block else ""}" href="{h}">{inline(label)}</a>'

def head(f, level=2, eyebrow=True):
    """Section head from the fields H1/H2/Eyebrow/Lede (and the 'SectionHeading H2' shorthand)."""
    parts = []
    if eyebrow and f.get('Eyebrow'): parts.append(f'<span class="th-eyebrow">{inline(f["Eyebrow"])}</span>')
    h1 = f.get('H1') or f.get('H1 (styled as H2)')
    h2 = f.get('H2') or f.get('SectionHeading H2')
    if h1: parts.append(f'<h1 class="{"text-h2" if "H1 (styled as H2)" in f else "text-display"}">{inline(h1)}</h1>')
    elif h2: parts.append(f'<h{level} class="text-h2">{inline(h2)}</h{level}>')
    if f.get('Lede'): parts.append(f'<p class="text-lede">{inline(f["Lede"])}</p>')
    return f'<div class="th-section-head">{"".join(parts)}</div>' if parts else ''


# ---------------------------------------------------------------- sections
def hero(s, kind, page):
    f = s['fields']; art = f.get('Art', '')
    acts = []
    if f.get('Primary button'): acts.append(btn(f['Primary button']))
    if f.get('Quiet link'): acts.append(btn(f['Quiet link'], 'quiet'))
    copy = [f'<span class="th-eyebrow">{inline(f["Eyebrow"])}</span>' if f.get('Eyebrow') else '',
            f'<h1 class="text-display">{inline(f["H1"])}</h1>', f'<p class="text-lede">{inline(f["Lede"])}</p>' if f.get('Lede') else '',
            f'<div class="th-hero__actions">{"".join(acts)}</div>' if acts else '',
            f'<p class="th-hero__note">{inline(f["Note"])}</p>' if f.get('Note') else '']
    art_html = ''
    if art and '(no art)' not in kind:
        owner = inline(art) if '[[' in art else ''
        art_html = f'<div class="th-hero__art"><img src="technehora-rewind.svg" alt="" width="320" height="320">{owner}</div>'
    return f'<section class="th-hero"><div class="th-container"><div class="th-hero__grid"><div class="th-hero__copy">{"".join(copy)}</div>{art_html}</div></div></section>'

def cta(s, kind, page):
    f = s['fields']
    line = f'<p class="text-lede">{inline(f["Line"])}</p>' if f.get('Line') else ''
    note = f'<p>{inline(f["Owner note"])}</p>' if f.get('Owner note') else ''
    return (f'<section class="th-cta-band"><div class="th-container th-cta-band__inner"><div><h2 class="text-h2">{inline(f["H2"])}</h2>{line}{note}</div>'
            f'{btn(f["Button"])}</div></section>')

PRICE = {}
def price_card(s):
    f = s['fields'] if s['fields'] else PRICE
    if not f.get('Price'): f = PRICE
    items = ''.join(f'<li>{icon("check")}<span>{inline(x)}</span></li>' for x in (s['lists'].get('Included') or PRICE.get('_included', [])))
    small = f'<p class="pv-small">{inline(f["Small print under button"])}</p>' if f.get('Small print under button') else ''
    return (f'<div class="th-price"><div class="th-price__head"><h3 class="text-h3">{inline(f["Name"])}</h3><span class="th-price__unit">Fixed price</span></div>'
            f'<div class="th-price__amount">{inline(f["Price"])}</div><p>{inline(f.get("One line", ""))}</p><ul class="th-price__list">{items}</ul>'
            f'<p class="th-price__credit">{inline(f["Credit note"])}</p>{btn(f["Button"], block=True)}{small}</div>')

def cards(s):
    rows = s['tables'][0]; hdr = [h.lower() for h in rows[0]]; out = []
    for r in rows[1:]:
        d = dict(zip(hdr, r)); ic = d.get('icon', '').strip('`')
        text = inline(d.get('text', ''))
        if ' · ' in d.get('text', ''):  # "Is this you?" problems become a short list
            text = '<ul class="pv-mini">' + ''.join(f'<li>{inline(x)}</li>' for x in d['text'].split(' · ')) + '</ul>'
        else:
            text = f'<p>{text}</p>'
        link = ''
        if d.get('link'):
            label, h = action(d['link'])
            link = f'<a class="th-card__link" href="{h}">{inline(label)}{icon("arrow")}</a>'
        out.append(f'<article class="th-card"><span class="th-card__icon">{icon(ic) if ic in ICONS else ""}</span><h3 class="text-h3">{inline(d.get("h3", ""))}</h3>{text}{link}</article>')
    return f'<div class="th-card-grid">{"".join(out)}</div>'

def steps(s):
    return '<ol class="th-steps">' + ''.join(f'<li><h3 class="text-h3">{inline(t.rstrip("."))}</h3><p>{inline(rest)}</p></li>' for t, rest, _ in s['items']) + '</ol>'

def faq(s):
    out = []
    for n, (q, rest, ans) in enumerate(s['items']):
        out.append(f'<details{" open" if n == 0 else ""}><summary>{inline(q)}{icon("chevron")}</summary><div><p>{inline((rest + " " + ans).strip())}</p></div></details>')
    link = ''
    if s['fields'].get('Link under the list'):
        label, h = action(s['fields']['Link under the list'])
        link = f'<p class="pv-after"><a href="{h}">{inline(label)}</a></p>'
    return f'<div class="th-faq">{"".join(out)}</div>{link}'

ROADMAP = {}
def roadmap(s):
    rows = s['tables'][0] if s['tables'] else ROADMAP.get('rows')
    cap = s['fields'].get('Caption') or ROADMAP.get('caption', '')
    note = s['fields'].get('Note under table') or ROADMAP.get('note', '')
    hdr, body = rows[0], rows[1:]
    th = ''.join(f'<th scope="col"{" class=num" if i == 1 else ""}>{inline(h)}</th>' for i, h in enumerate(hdr))
    def row(r):
        return '<tr>' + ''.join(f'<td{" class=num" if i == 1 else ""} data-label="{html.escape(hdr[i])}">{inline(c)}</td>' for i, c in enumerate(r)) + '</tr>'
    total = [r for r in body if r[0].startswith('**Total')]
    rest = [r for r in body if r not in total]
    tfoot = f'<tfoot>{"".join(row([c.replace("**", "") for c in r]) for r in total)}</tfoot>' if total else ''
    return (f'<div class="th-table-wrap"><table class="th-table th-table--stack"><caption>{inline(cap)}</caption><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(row(r) for r in rest)}</tbody>{tfoot}</table></div>' + (f'<p class="pv-after pv-small">{inline(note)}</p>' if note else ''))

def problems(s):
    rows = s['tables'][0][1:]
    return '<ul class="pv-problems">' + ''.join(f'<li><p class="pv-problem">{inline(p)}</p><p>{inline(c)}</p></li>' for p, c in rows) + '</ul>'

def callout(s, kind):
    f = s['fields']; plain = '(plain)' in kind
    return (f'<div class="th-callout{" th-callout--plain" if plain else ""}">{icon("info")}<p><strong>{inline(f["Bold start"])}</strong> {inline(f["Rest"])}</p></div>')

def form(s):
    f = s['fields']; rows = s['tables'][0]; hdr = [h.lower() for h in rows[0]]; out = []
    for r in rows[1:]:
        d = dict(zip(hdr, r)); fid = f'f-{d["field"]}'
        hint = f'<span class="th-field__hint" id="{fid}-h">{inline(d["hint"])}</span>' if d.get('hint') else ''
        req = '' if d.get('required') == 'yes' else ' <span class="pv-opt">(optional)</span>'
        ctl = (f'<textarea class="th-input" id="{fid}"></textarea>' if d['field'] == 'question'
               else f'<input class="th-input" id="{fid}"{" aria-describedby=" + chr(34) + fid + "-h" + chr(34) if hint else ""}>')
        err = f'<p class="pv-small pv-err pv-ro">Error text: {inline(d["error"])}</p>' if d.get('error') else ''
        out.append(f'<div class="th-field"><label for="{fid}">{inline(d["label"])}{req}</label>{hint}{ctl}{err}</div>')
    states = ''.join(f'<li><b>{k}:</b> {inline(f[k])}</li>' for k in ('Sending state', 'Success message', 'Failure message') if f.get(k))
    return (f'<form class="pv-form" onsubmit="event.preventDefault()">{"".join(out)}<button class="th-btn th-btn--primary" type="submit">{inline(f.get("Button", "Send"))}</button></form>'
            + (f'<ul class="pv-states pv-ro">{states}</ul>' if states else ''))

def embed(s):
    f = s['fields']
    return (f'<div class="pv-embed"><p class="text-strong">{inline(f.get("Label above the scheduler", ""))}</p>'
            f'<div class="pv-embed__slot"><img src="technehora-rewind-spinner.svg" alt="" width="48" height="48"><span>{inline(f.get("Loading state", ""))}</span>'
            f'<span class="pv-small">The scheduler is embedded here in <code>06_build</code>.</span></div>'
            f'<p class="pv-small"><b>If it fails to load:</b> {inline(f.get("If the scheduler fails to load", ""))}</p></div>')

def generic(s):
    """Lists with bold leads, paragraphs, plain bullets, text, remaining fields."""
    out = []
    for key, items in s['lists'].items():
        if key == 'Paragraphs':
            out.extend(f'<p>{inline(x)}</p>' for x in items)
        elif key != 'Included':
            out.append('<ul class="pv-list">' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>')
    if s['bullets']: out.append('<ul class="pv-list">' + ''.join(f'<li>{inline(x)}</li>' for x in s['bullets']) + '</ul>')
    out.extend(f'<p>{inline(t)}</p>' for t in s['text'])
    for k in ('Line', 'Phone', 'Email', 'Based in', 'Owner note'):
        if k in s['fields']:
            out.append(f'<p>{"<b>" + k + ":</b> " if k in ("Phone", "Email", "Based in") else ""}{inline(s["fields"][k])}</p>')
    for k in ('Link', 'Button'):
        if k in s['fields']:
            out.append(f'<p class="pv-after">{btn(s["fields"][k], "secondary") if k == "Button" else ""}'
                       f'{"" if k == "Button" else "<a href=" + chr(34) + action(s["fields"][k])[1] + chr(34) + ">" + inline(action(s["fields"][k])[0]) + "</a>"}</p>')
    return f'<div class="pv-prose">{"".join(out)}</div>'

def section(kind, s, page, sunken):
    k = kind.lower()
    if k.startswith('hero'): return hero(s, kind, page)
    if k.startswith('ctaband'): return cta(s, kind, page)
    if k.startswith('breadcrumbs'):
        trail = s['text'][0].split('→')
        parent = '/' + page['meta']['url'].strip('/').split('/')[0]
        crumbs = f'<a href="{href(parent) if parent in URLS else "#home"}">{inline(trail[0].strip())}</a> <span aria-hidden="true">/</span> <span aria-current="page">{inline(trail[-1].strip())}</span>'
        return f'<nav class="pv-crumbs th-container" aria-label="Breadcrumb">{crumbs}</nav>'
    f = s['fields']
    if k.startswith('pricecard'): inner = price_card(s)
    elif 'servicecard' in k: inner = head(f) + cards(s)
    elif k.startswith('steps'): inner = head(f) + steps(s)
    elif k.startswith('faq'): inner = head(f) + faq(s)
    elif k.startswith('roadmaptable') or 'roadmaptable' in k: inner = head(f) + roadmap(s)
    elif k.startswith('problemlist'): inner = head(f) + problems(s)
    elif k.startswith('callout'): inner = callout(s, kind)
    elif k.startswith('bookingembed'): inner = embed(s)
    elif 'form' in k: inner = head(f) + (f'<p class="pv-after">{inline(f["Line"])}</p>' if f.get('Line') else '') + form(s)
    else:
        if not any(k_ in f for k_ in ('H1', 'H2', 'H1 (styled as H2)', 'SectionHeading H2')) and not k.startswith('sectionheading'):
            f = dict(f, H2=re.sub(r'\s*\(.*?\)', '', kind))  # a descriptive section title doubles as its heading
        inner = head(f) + generic(s)
    return f'<section class="th-section{" th-section--sunken" if sunken else ""}" data-kind="{html.escape(kind)}"><div class="th-container">{inner}</div></section>'


# ---------------------------------------------------------------- chrome: header, footer, call bar
NAV = [('The audit', '/audit'), ('Training & builds', '/services'), ('Who we help', '/industries'), ('About', '/about')]

def header(page):
    cur = '/' + page['meta']['url'].strip('/').split('/')[0] if page['meta']['url'].startswith('/') else ''
    links = ''.join(f'<li><a href="{href(u)}"{" aria-current=page" if u == cur else ""}>{n}</a></li>' for n, u in NAV)
    return (f'<header class="th-header"><div class="th-container"><div class="th-header__bar">'
            f'<a class="th-header__logo" href="#home"><img class="logo-light" src="technehora-lockup-horizontal-light.svg" alt="Techne Hora" height="48">'
            f'<img class="logo-dark" src="technehora-lockup-horizontal-dark.svg" alt="Techne Hora" height="48"></a>'
            f'<nav class="th-header__nav" aria-label="Main"><ul>{links}</ul></nav>'
            f'<a class="th-header__cta th-btn th-btn--primary th-btn--sm" href="#book">Book a call</a>'
            f'<button class="th-header__menu-btn" type="button" aria-expanded="false" aria-controls="menu-{page["slug"]}"><span class="th-visually-hidden">Menu</span>{icon("menu")}</button>'
            f'</div><div class="th-header__panel" id="menu-{page["slug"]}" hidden><ul>{links}</ul><a class="th-btn th-btn--primary th-btn--block" href="#book">Book a free 20-minute call</a></div></div></header>')

def footer():
    return ('<footer class="th-footer"><div class="th-container"><div class="th-footer__grid">'
            '<div><h2>Contact</h2><ul><li><mark class="rv rv--owner"><b>Owner:</b> phone</mark></li><li><a href="#book">hello@technehora.ai</a></li><li>Rochester, NY</li></ul></div>'
            '<div><h2>Where we work</h2><ul><li><a href="#areas-rochester">Rochester &amp; Monroe County</a></li><li>Buffalo · Syracuse</li><li>Finger Lakes</li><li>Remote, anywhere</li></ul></div>'
            '<div><h2>Site</h2><ul><li><a href="#services">Training &amp; builds</a></li><li><a href="#industries">Who we help</a></li><li><a href="#faq">FAQ</a></li>'
            '<li><a href="#privacy">Privacy</a></li><li><a href="#accessibility">Accessibility</a></li></ul></div></div>'
            '<div class="th-footer__base"><span class="th-footer__brand"><img src="technehora-lockup-horizontal-dark.svg" alt="Techne Hora" height="48"></span>'
            '<span>© 2026 Techne Hora</span></div></div></footer>')

CALLBAR = '<div class="th-callbar"><a class="th-btn th-btn--secondary" href="#call">Call</a><a class="th-btn th-btn--primary" href="#book">Book a call</a></div>'


def render(page):
    body, n = [], 0
    for kind, s in page['sections']:
        plain = kind.lower().startswith(('hero', 'ctaband', 'breadcrumbs'))
        body.append(section(kind, s, page, sunken=(not plain and n % 2 == 1)))
        if not plain: n += 1
    owners = sum(len(re.findall(r'\[\[OWNER:', str(s))) for _, s in page['sections'])
    notes = ''.join(f'<p>{inline(x)}</p>' for x in page['notes'])
    review = (f'<aside class="pv-review" aria-label="Review notes"><span><b>{inline(page["title"])}</b> · <code>{page["meta"]["url"]}</code> · '
              f'<code>pages/{page["slug"]}.md</code> · {page["meta"]["status"]}{f" · {owners} owner item" + ("s" if owners != 1 else "") if owners else ""}</span>'
              f'<span class="pv-meta"><b>Title tag:</b> {inline(page["meta"]["title"])}<br><b>Description:</b> {inline(page["meta"]["description"])}</span>{notes}</aside>')
    bar = '' if page['slug'] == 'book' else CALLBAR
    return f'<div class="pv-page" id="p-{page["slug"]}" data-slug="{page["slug"]}" data-title="{html.escape(page["meta"]["title"])}">{review}{header(page)}<main>{"".join(body)}</main>{footer()}{bar}</div>'


PAGE_CSS = '''
/* Preview-only: the review strip, the three sections the sitemap names as gaps (ProblemList, BookingEmbed, Breadcrumbs),
   and the hash router. Everything else is the design system's own CSS, unchanged. */
body { margin: 0; background: var(--bg); }
.pv-page { display: none; }
.pv-page.is-current { display: block; padding-bottom: 88px; }
@media (min-width: 960px) { .pv-page.is-current { padding-bottom: 0; } }
.logo-dark { display: none; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .logo-light { display: none; } :root:not([data-theme="light"]) .logo-dark { display: inline; } }
:root[data-theme="dark"] .logo-light { display: none; } :root[data-theme="dark"] .logo-dark { display: inline; }
.th-header__logo img { height: 48px; width: auto; }
.th-footer__brand img { height: 48px; width: auto; }
.th-hero__art img { width: 100%; height: auto; display: block; }

.pv-switch { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 30; display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center;
  padding: 8px max(16px, env(safe-area-inset-right, 0px)) 8px max(16px, env(safe-area-inset-left, 0px));
  background: var(--inverse); color: var(--on-inverse); font: 500 0.8125rem/1.3 var(--font-mono); letter-spacing: .04em; }
.pv-switch label { text-transform: uppercase; letter-spacing: .09em; color: var(--on-inverse-muted); }
.pv-switch select { font: inherit; min-height: 36px; max-width: 100%; border-radius: var(--radius-sm); border: 1px solid var(--on-inverse-muted); background: var(--surface); color: var(--ink); padding: 0 8px; }
.pv-switch button { font: inherit; min-height: 36px; padding: 0 12px; border-radius: var(--radius-sm); border: 1px solid var(--on-inverse-muted); background: transparent; color: var(--on-inverse); cursor: pointer; }
.pv-switch button[aria-pressed="true"] { background: var(--on-inverse); color: var(--ink); }
.pv-switch :focus-visible { outline: 2px solid var(--on-inverse); outline-offset: 2px; }
.pv-review { display: none; gap: 6px; padding: 12px max(16px, env(safe-area-inset-left, 0px)); background: var(--surface-sunken); border-bottom: 1px dashed var(--border-strong);
  color: var(--ink-muted); font: 400 0.875rem/1.45 var(--font-sans); }
.pv-review p { margin: 0; max-width: 80ch; }
.pv-ro { display: none; }
.show-review .pv-ro { display: block; }
.show-review .pv-review { display: grid; }
.pv-meta { color: var(--ink); }
mark.rv { background: #FFF1B8; color: #3D2E00; border-radius: 3px; padding: 0 4px; font-size: .9em; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
mark.rv--build { background: #DDE8FF; color: #14284B; }
.hide-marks mark.rv { background: transparent; color: inherit; outline: 1px dashed currentColor; }

.pv-crumbs { padding-block: 12px 0; font: 400 0.9375rem/1.4 var(--font-sans); color: var(--ink-muted); }
.pv-crumbs a { color: var(--link); }
.pv-problems { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; max-width: 46rem; border-top: 1px solid var(--border); }
.pv-problems li { display: grid; gap: 4px; padding-block: 16px; border-bottom: 1px solid var(--border); }
.pv-problem { font: 600 1.0625rem/1.45 var(--font-sans); color: var(--ink); }
.pv-problems li p:last-child { color: var(--ink-muted); }
.pv-list { margin: 0; padding-left: 20px; display: grid; gap: 10px; max-width: var(--measure); }
.pv-mini { margin: 0; padding-left: 18px; display: grid; gap: 4px; color: var(--ink-muted); }
.pv-prose { display: grid; gap: 14px; }
.pv-after { margin-top: 20px !important; }
.pv-small { font-size: 0.9375rem; color: var(--ink-muted); }
.pv-err { color: var(--danger); }
.pv-opt { font-weight: 400; color: var(--ink-muted); }
.pv-form { display: grid; gap: 20px; max-width: 34rem; margin-top: 20px; }
.pv-states { margin: 16px 0 0; padding-left: 20px; color: var(--ink-muted); font-size: 0.9375rem; display: grid; gap: 4px; }
.pv-embed { display: grid; gap: 12px; max-width: 46rem; }
.pv-embed__slot { display: grid; place-items: center; gap: 8px; min-height: 260px; padding: 24px; text-align: center; border: 1px dashed var(--border-strong); border-radius: var(--radius-lg); background: var(--surface); }
.th-price p { max-width: none; }
code { font-family: var(--font-mono); font-size: .875em; }
'''

SCRIPT = '''
(function () {
  var pages = Array.prototype.slice.call(document.querySelectorAll('.pv-page'));
  var pick = document.getElementById('pv-pick');
  function show() {
    var id = (location.hash || '#home').slice(1);
    if (id === 'call' || id === 'missing') { return; }
    var target = document.getElementById('p-' + id) || document.getElementById('p-404');
    pages.forEach(function (p) { p.classList.toggle('is-current', p === target); });
    pick.value = target.getAttribute('data-slug');
    document.title = target.getAttribute('data-title');
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', show);
  pick.addEventListener('change', function () { location.hash = pick.value; });
  function toggle(id, cls) {
    var b = document.getElementById(id);
    b.addEventListener('click', function () {
      var on = b.getAttribute('aria-pressed') !== 'true';
      b.setAttribute('aria-pressed', String(on));
      document.getElementById('pv-app').classList.toggle(cls, cls === 'hide-marks' ? !on : on);
    });
  }
  toggle('pv-notes', 'show-review');
  toggle('pv-marks', 'hide-marks');
  document.querySelectorAll('.th-header__menu-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      b.setAttribute('aria-expanded', String(!open));
      document.getElementById(b.getAttribute('aria-controls')).hidden = open;
    });
  });
  show();
})();
'''


def main():
    pages = [load(s) for s in ORDER]
    for p in pages:
        if p['meta']['url'].startswith('/'): URLS[p['meta']['url']] = p['slug']
    home = pages[0]
    for kind, s in home['sections']:
        if kind.startswith('PriceCard'): PRICE.update(s['fields'], _included=s['lists']['Included'])
    audit = pages[1]
    for kind, s in audit['sections']:
        if 'RoadmapTable' in kind: ROADMAP.update(rows=s['tables'][0], caption=s['fields']['Caption'], note=s['fields']['Note under table'])
    options = ''.join(f'<option value="{p["slug"]}">{html.escape(p["title"])} ({p["meta"]["url"] if p["meta"]["url"].startswith("/") else "404"})</option>' for p in pages)
    total = sum(len(re.findall(r'\[\[OWNER:', open(os.path.join(OUT, 'pages', f'{p["slug"]}.md')).read())) for p in pages)
    doc = (f'<title>Techne Hora Site Preview</title>\n<meta name="robots" content="noindex">\n<link rel="stylesheet" href="tokens.css">\n<link rel="stylesheet" href="components.css">\n<style>{PAGE_CSS}</style>\n'
           f'<div class="th-root" id="pv-app">\n<div class="pv-switch" role="region" aria-label="Preview controls"><label for="pv-pick">Page</label><select id="pv-pick">{options}</select>'
           f'<button id="pv-notes" type="button" aria-pressed="false">Review notes</button><button id="pv-marks" type="button" aria-pressed="true">Owner items ({total})</button></div>\n'
           + '\n'.join(render(p) for p in pages) + f'\n</div>\n<script>{SCRIPT}</script>\n')
    os.makedirs(os.path.join(PREVIEW, 'fonts'), exist_ok=True)
    with open(os.path.join(PREVIEW, 'index.html'), 'w') as fh: fh.write(doc)
    shutil.copy(os.path.join(DS, 'tokens.css'), PREVIEW); shutil.copy(os.path.join(DS, 'components.css'), PREVIEW)
    for f in os.listdir(os.path.join(DS, 'fonts')): shutil.copy(os.path.join(DS, 'fonts', f), os.path.join(PREVIEW, 'fonts'))
    for f in ('technehora-lockup-horizontal-light.svg', 'technehora-lockup-horizontal-dark.svg', 'technehora-rewind.svg', 'technehora-rewind-spinner.svg'):
        shutil.copy(os.path.join(LOGO, f), PREVIEW)
    print(f'{len(pages)} pages, {total} owner items -> {os.path.relpath(PREVIEW, STAGES)}/index.html')

if __name__ == '__main__':
    main()
