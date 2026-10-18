"""Build brand-sheet.html: the one-page visual reference of the approved brand.

Inlines the SVGs from logo/ (run logo/_build_logo.py first), so the sheet always shows the current files:
    python _build_sheet.py
Pure standard library.
"""
import base64, os

OUT = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(OUT, 'logo')

def svg(name):
    path = os.path.join(LOGO, name)
    if name.endswith('.png'):
        data = base64.b64encode(open(path, 'rb').read()).decode()
        return f'<img src="data:image/png;base64,{data}" width="90" height="90" alt="">'
    return open(path).read().strip()

TILES = [  # file, stage, title, use
    ('technehora-lockup-horizontal-light.svg', 'light', 'Horizontal lockup', 'Default: site header, invoices, email signature, van doors'),
    ('technehora-lockup-horizontal-dark.svg', 'dark', 'Horizontal lockup, dark', 'Navy surfaces, dark footers'),
    ('technehora-lockup-stacked-light.svg', 'light', 'Stacked lockup', 'Shirts, signage, title slides, square avatars with name'),
    ('technehora-lockup-stacked-dark.svg', 'dark', 'Stacked lockup, dark', 'Navy shirts and signs'),
    ('technehora-wordmark-light.svg', 'light', 'Wordmark', 'Name only, where the mark is already nearby'),
    ('technehora-wordmark-dark.svg', 'dark', 'Wordmark, dark', 'Name only, on navy'),
    ('technehora-mark.svg', 'light', 'Mark', 'Social avatar, app icon, hero'),
    ('technehora-mark-flat.svg', 'light', 'Mark, flat', 'Print and signage: no shadow'),
    ('technehora-mark-mono-navy.svg', 'light', 'Mark, one ink', 'Embroidery, vinyl, stamps'),
    ('technehora-mark-mono-white.svg', 'dark', 'Mark, one ink reversed', 'On navy, and on photos with a dark scrim'),
    ('favicon.svg', 'light', 'Favicon', 'Browser tabs at 16–32px: flat, heavier ticks and hands'),
    ('png/apple-touch-icon.png', 'light', 'Phone icon', 'Home-screen bookmark: the mark on paper, 180px'),
]
MOTION = [
    ('technehora-rewind.svg', 'Rewind', 'The ember arc winding the clock back. Hero art, pitch title slides'),
    ('technehora-rewind-spinner.svg', 'Rewind spinner', 'Loading states. The arc turns counter-clockwise and stops for reduced motion'),
]
SWATCHES = [
    ('#1B2A4A', 'Ink navy', 'Text, header, clock rim', '13.3:1 on paper'),
    ('#FAF7F0', 'Paper', 'Background, clock face', ''),
    ('#A63D2A', 'Brick', 'Primary button, links, hour hand', 'White on it 6.3:1'),
    ('#E07A5F', 'Ember', 'The rewind arc; accents on navy', 'Graphic only'),
    ('#4E7060', 'Sage', 'Secondary accent', '5.2:1 on paper'),
    ('#5C6170', 'Graphite', 'Muted text, H·O·R·A', '5.8:1 on paper'),
]

def tile(name, stage, title, use):
    return (f'<figure class="lt"><div class="stage {stage}">{svg(name)}</div>'
            f'<figcaption><b>{title}</b><span>{use}</span><code>{name}</code></figcaption></figure>')

def swatch(hexv, name, role, note):
    code = f'{hexv} · {note}' if note else hexv
    return f'<div class="sw"><i style="background:{hexv}"></i><div><b>{name}</b><span>{role}</span><code>{code}</code></div></div>'

PAGE = '''<title>Techne Hora Brand Sheet</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Serif:wght@600;700&display=swap">
<style>
/* Layout: a single-column brand sheet; logo files on true light/dark stages, then motion, color, type, voice */
:root{
  --bg:#FAF7F0; --fg:#1B2A4A; --muted:#5C6170; --line:#E4DFD3; --panel:#F3EFE5; --accent:#A63D2A;
  --head:"IBM Plex Serif",Georgia,serif; --body:"IBM Plex Sans",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121A2C;--fg:#F1EDE3;--muted:#A9AFBD;--line:#2A3550;--panel:#1A2438;--accent:#F29A80;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121A2C;--fg:#F1EDE3;--muted:#A9AFBD;--line:#2A3550;--panel:#1A2438;--accent:#F29A80;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.label{font:500 .72rem/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
header.top{padding-block:44px 32px;display:flex;flex-direction:column;gap:18px}
.hero-lock{background:#FAF7F0;border:1px solid #E4DFD3;border-radius:12px;padding:clamp(24px,5vw,48px);display:flex;flex-direction:column;gap:18px;align-items:flex-start}
.hero-lock svg{height:clamp(72px,12vw,128px);width:auto;max-width:100%}
.hero-lock p{margin:0;font:600 clamp(1.1rem,2.4vw,1.4rem)/1.3 var(--head);color:#5C6170}
header.top .meta{color:var(--muted);max-width:66ch;margin:0}
section{padding-block:28px;border-top:1px solid var(--line)}
section h2{font:700 1.6rem/1.1 var(--head);margin:0 0 6px}
section h3{font:600 1.15rem/1.2 var(--head);margin:22px 0 10px}
section > .wrap > p{margin:0 0 18px;color:var(--muted);max-width:66ch}
.logos{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px}
.lt{margin:0;display:flex;flex-direction:column;border:1px solid var(--line);border-radius:10px;overflow:hidden;min-width:0}
.stage{height:150px;display:grid;place-items:center;padding:20px}
.stage svg{max-height:100%;max-width:100%;width:auto;height:auto}
.stage.light{background:#FAF7F0} .stage.dark{background:#1B2A4A}
.lt figcaption{padding:12px 14px;display:flex;flex-direction:column;gap:2px;background:var(--panel);flex:1}
.lt figcaption span{color:var(--muted);font-size:.92rem}
.lt code{font:.75rem var(--mono);color:var(--muted);overflow-wrap:anywhere}
.rules{margin:0;padding-left:20px;display:grid;gap:4px;max-width:70ch}
.rules b{font-weight:600}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr));gap:12px}
.sw{display:flex;gap:12px;align-items:center;min-width:0}
.sw i{width:56px;height:56px;border-radius:8px;flex:none;border:1px solid var(--line)}
.sw div{display:flex;flex-direction:column;min-width:0}
.sw span{color:var(--muted);font-size:.92rem}
.sw code{font:.75rem var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}
.type{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.type.three{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:720px){.type,.type.three{grid-template-columns:minmax(0,1fr)}}
.spec{background:var(--panel);border-radius:10px;padding:20px;display:flex;flex-direction:column;gap:8px;min-width:0}
.spec .big{font:700 clamp(1.8rem,4.4vw,2.6rem)/1.08 var(--head);text-wrap:balance}
.spec .bodytxt{font:400 1.05rem/1.55 var(--body);max-width:52ch;margin:0}
.spec .bodytxt b{font-weight:600}
.spec .monotxt{font:500 1rem/1.5 var(--mono);font-variant-numeric:tabular-nums}
.voice{width:100%;border-collapse:collapse}
.voice th{text-align:left;padding:8px 10px;border-bottom:2px solid var(--line)}
.voice td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}
.voice td:first-child{font-weight:600}
.voice td:last-child{color:var(--muted);text-decoration:line-through;text-decoration-color:var(--accent)}
.tablewrap{overflow-x:auto}
.checks{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:4px}
footer{padding-block:24px 48px;border-top:1px solid var(--line);color:var(--muted);font-size:.9rem;display:grid;gap:8px}
</style>

<div class="wrap"><header class="top">
  <div class="label">Stage 02 · Brand · approved</div>
  <div class="hero-lock">{{hero}}<p>The craft of getting your hours back.</p></div>
  <p class="meta">The brand for the Rochester AI consultancy: name, logo set, color, type, and voice. Approved 2026-10-17; logo picked 2026-10-18. The owner checks at the bottom must be done before launch.</p>
</header></div>

<section><div class="wrap">
  <h2>Name</h2>
  <p><i>Techne</i> is Greek for craft or skill; <i>hora</i> is the hour. Two words, both capitalized. Never “TechneHora”, “Techne-Hora”, or “Techne Hora AI” in the logo.</p>
  <div class="type">
    <div class="spec"><span class="label">Say it</span><span class="big">TEK-nee OR-ah</span><p class="bodytxt">A soft, almost silent H. On the phone: “Techne, T-E-C-H-N-E, Hora.”</p></div>
    <div class="spec"><span class="label">About-page line</span><p class="bodytxt">Techne is the Greek word for craft; hora means the hour. We craft AI tools that give your hours back.</p><span class="label">Site · technehora.ai</span></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Logo set</h2>
  <p>A navy-rimmed clock at ten o’clock, the last two hours tinted: the hours given back. “Techne” is set in Plex Serif, with H·O·R·A under it in Plex Mono, spaced like hour marks the way a watch prints small text on its dial. The whole name stays readable, and Hora stays quiet.</p>
  <div class="logos">{{tiles}}</div>
  <h3>Rules</h3>
  <ul class="rules">
    <li><b>Minimum size:</b> lockups at least 48px / 16mm tall, so H·O·R·A reads. Smaller than that, use the mark alone; below 24px, the favicon.</li>
    <li><b>Clear space:</b> the rim’s width (about 14% of the mark’s height) on every side.</li>
    <li><b>Don’t:</b> recolor or rotate the mark, set HORA heavier or in color, add the rewind arc to the static logo, or put the full-color mark on a busy photo.</li>
  </ul>
</div></section>

<section><div class="wrap">
  <h2>Motion</h2>
  <p>The ember rewind arc is the clearest picture of “time back”, so it is kept for moments that move, never inside the logo.</p>
  <div class="logos">{{motion}}</div>
</div></section>

<section><div class="wrap">
  <h2>Color</h2>
  <p>Every text pair passes WCAG 2.2 AA. Ember is for graphics on navy only, never for text on paper.</p>
  <div class="swatches">{{swatches}}</div>
</div></section>

<section><div class="wrap">
  <h2>Type</h2>
  <p>IBM Plex, the “Engineered” pick. All three are free on Google Fonts, and the logo uses the same faces.</p>
  <div class="type three">
    <div class="spec"><span class="label">Headings · Plex Serif 600 / 700</span><span class="big">Five things to fix, in order.</span></div>
    <div class="spec"><span class="label">Body · Plex Sans 400 / 600</span><p class="bodytxt">A $750 audit looks at how your calls, quotes, and scheduling work today, then gives you a written plan: <b>the five changes that save the most hours</b>, with rough costs, in the order we’d do them.</p></div>
    <div class="spec"><span class="label">Details · Plex Mono 500</span><span class="monotxt">STEP 1 · AUDIT<br>STEP 2 · PLAN<br>STEP 3 · BUILD</span><p class="bodytxt">Numbers in roadmaps, badges, small labels.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Voice</h2>
  <p>A straight-talking advisor. Plain words, short sentences, outcomes before tools.</p>
  <div class="tablewrap"><table class="voice"><thead><tr><th>Say</th><th>Not</th></tr></thead><tbody>
  <tr><td>Missed calls are missed jobs.</td><td>Leverage AI-powered omnichannel engagement.</td></tr>
  <tr><td>Five things to fix, in order.</td><td>A comprehensive transformation roadmap.</td></tr>
  <tr><td>We’ll train your team to run it.</td><td>Seamless change management enablement.</td></tr>
  <tr><td>Hours, calls, quotes</td><td>Agents, LLMs, MCP (unless the reader already says them)</td></tr>
  </tbody></table></div>
</div></section>

<div class="wrap"><footer>
  <span class="label">Owner checks before launch</span>
  <ol class="checks"><li>technehora.ai registered ✓</li><li>Register technehora.com and redirect it to .ai</li><li>Confirm the tagline</li><li>Claim @technehora on LinkedIn, Google Business Profile, Facebook, Instagram</li><li>Quick USPTO search, classes 35 (consulting) and 41 (training)</li></ol>
</footer></div>
'''

if __name__ == '__main__':
    parts = dict(hero=svg('technehora-lockup-horizontal-light.svg'),
                 tiles=''.join(tile(*t) for t in TILES),
                 motion=''.join(tile(n, 'light', t, u) for n, t, u in MOTION),
                 swatches=''.join(swatch(*s) for s in SWATCHES))
    html = PAGE
    for k, v in parts.items():
        html = html.replace('{{' + k + '}}', v)
    with open(os.path.join(OUT, 'brand-sheet.html'), 'w') as fh:
        fh.write(html)
