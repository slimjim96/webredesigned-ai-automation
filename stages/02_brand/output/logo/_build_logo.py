"""Build the final Hourback logo set (R2 wall-clock dial).

Needs fontTools and the Fraunces variable font (Google Fonts, OFL):
    python -m venv .venv && .venv/bin/pip install fonttools
    .venv/bin/python _build_logo.py path/to/Fraunces[SOFT,WONK,opsz,wght].ttf
"""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

N, ND, NL, P, B, BL = '#1B2A4A', '#111B31', '#2B4374', '#FAF7F0', '#A63D2A', '#E07A5F'
OUT = os.path.dirname(os.path.abspath(__file__))

def pt(deg, r, c=32):
    a = math.radians(deg); return (c + r * math.sin(a), c - r * math.cos(a))
f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"
def sector(a0, a1, r):
    s, e = pt(a0, r), pt(a1, r)
    return f"M32 32L{f(s)}A{r} {r} 0 {1 if (a1-a0) % 360 > 180 else 0} 1 {f(e)}Z"
def taper_arc(a_start, a_end, r, w0, w1, head=6, steps=48):
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps; a = a_start + (a_end - a_start) * t; w = w0 + (w1 - w0) * t
        outer.append(pt(a, r + w / 2)); inner.append(pt(a, r - w / 2))
    tip = pt(a_end - head * 360 / (2 * math.pi * r), r); hw = w1 * 1.25 + 1.5
    d = "M" + f(outer[0]) + "".join("L" + f(p) for p in outer[1:])
    d += "L" + f(pt(a_end, r + hw)) + "L" + f(tip) + "L" + f(pt(a_end, r - hw))
    return d + "".join("L" + f(p) for p in reversed(inner)) + "Z"
def line(p0, p1, col, w, op=1):
    return f'<path d="M{f(p0)}L{f(p1)}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"' + (f' stroke-opacity="{op}"' if op < 1 else '') + '/>'

ARROW = taper_arc(55, -95, 25.5, 1, 3.6)
def ticks(col, op=.75, every=30):
    return "".join(line(pt(a, 15.8 if a % 90 == 0 else 16.6), pt(a, 17.6), col, 1.6 if a % 90 == 0 else 1, op) for a in range(0, 360, every))
def hands(mcol, hcol, mw=2.6, hw=3.6):
    return line((32, 32), pt(300, 9.5), hcol, hw) + line((32, 32), pt(0, 13), mcol, mw)
def pin(col, ring): return f'<circle cx="32" cy="32" r="3.2" fill="{ring}"/><circle cx="32" cy="32" r="1.4" fill="{col}"/>'

def mark_full(id):
    return (f'<defs><radialGradient id="{id}g" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="{NL}"/><stop offset=".55" stop-color="{N}"/><stop offset="1" stop-color="{ND}"/></radialGradient>'
            f'<linearGradient id="{id}f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9E1D0"/></linearGradient></defs>'
            f'<circle cx="32" cy="32" r="30" fill="url(#{id}g)"/><circle cx="32" cy="32" r="29.4" fill="none" stroke="#FFFFFF" stroke-opacity=".10" stroke-width="1.2"/>'
            f'<circle cx="33.4" cy="34" r="19" fill="{ND}" opacity=".7"/><circle cx="32" cy="32" r="19" fill="url(#{id}f)"/>'
            f'<circle cx="32" cy="32" r="19" fill="none" stroke="{N}" stroke-opacity=".15" stroke-width="1"/>'
            f'<path d="{sector(300, 360, 15.5)}" fill="{BL}" fill-opacity=".28"/>' + ticks(N) + hands(N, B) +
            f'<path d="{ARROW}" fill="{BL}"/>' + pin(P, N))
def mark_flat():
    return (f'<circle cx="32" cy="32" r="30" fill="{N}"/><circle cx="32" cy="32" r="19" fill="{P}"/>'
            f'<path d="{sector(300, 360, 15.5)}" fill="#F3D3C8"/>' + ticks(N, 1) + hands(N, B) +
            f'<path d="{ARROW}" fill="{BL}"/>' + pin(P, N))
def mark_mono(col, id):
    # one ink: disc with the face and arrow knocked out; ticks/hands in ink inside the face
    return (f'<defs><mask id="{id}m"><rect width="64" height="64" fill="#fff"/><circle cx="32" cy="32" r="19" fill="#000"/>'
            f'<path d="{ARROW}" fill="#000"/></mask></defs>'
            f'<circle cx="32" cy="32" r="30" fill="{col}" mask="url(#{id}m)"/>' + ticks(col, 1) + hands(col, col) +
            f'<circle cx="32" cy="32" r="3" fill="{col}"/>')
def mark_favicon():
    # tuned for 16-32px: no tint, four ticks, heavier hands and arrow
    arrow = taper_arc(55, -95, 25, 2.2, 4.6, head=7)
    return (f'<circle cx="32" cy="32" r="30" fill="{N}"/><circle cx="32" cy="32" r="18.5" fill="{P}"/>' +
            "".join(line(pt(a, 14.5), pt(a, 17), N, 2.6) for a in (0, 90, 180, 270)) +
            line((32, 32), pt(300, 9), B, 5) + line((32, 32), pt(0, 12.5), N, 4) + f'<path d="{arrow}" fill="{BL}"/>')

def wordmark(font_path):
    vf = TTFont(font_path)
    font = instantiateVariableFont(vf, {"wght": 700, "opsz": 144, "SOFT": 0, "WONK": 0})
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    upm, cap = font['head'].unitsPerEm, font['OS/2'].sCapHeight
    hmtx = font['hmtx']
    pen = SVGPathPen(gs); x = 0
    for ch in "Hourback":
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        x += hmtx[g][0]
    bp = BoundsPen(gs); x2 = 0
    for ch in "Hourback":
        g = cmap[ord(ch)]; gs[g].draw(TransformPen(bp, (1, 0, 0, 1, x2, 0))); x2 += hmtx[g][0]
    return pen.getCommands(), bp.bounds, cap  # path in font units, y down, baseline at 0

def write(name, w, h, body, label="Hourback"):
    with open(os.path.join(OUT, name), 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{label}">{body}</svg>\n')

def main(font_path):
    d, (xmin, ymin, xmax, ymax), cap = wordmark(font_path)
    # horizontal: cap height = 30/64 of the mark, vertically centered on it
    s = 30 / cap; ww = (xmax - xmin) * s
    gap = 14; hx = 64 + gap - xmin * s; hy = 32 + 15
    word = lambda col, sc, tx, ty: f'<path transform="translate({tx:.2f} {ty:.2f}) scale({sc:.5f})" d="{d}" fill="{col}"/>'
    for theme, col in (('light', N), ('dark', P)):
        write(f'hourback-lockup-horizontal-{theme}.svg', 64 + gap + ww + 2, 64, f'<g>{mark_full("h" + theme[0])}</g>' + word(col, s, hx, hy))
        # stacked: mark 64 centered over wordmark with cap 22
        s2 = 22 / cap; ww2 = (xmax - xmin) * s2; W = max(64, ww2) + 4
        write(f'hourback-lockup-stacked-{theme}.svg', W, 64 + 14 + 22 + 2 + (-ymin * s2 if ymin < 0 else 0),
              f'<g transform="translate({(W - 64) / 2:.2f} 0)">{mark_full("s" + theme[0])}</g>' + word(col, s2, (W - ww2) / 2 - xmin * s2, 64 + 14 + 22))
        write(f'hourback-wordmark-{theme}.svg', ww + 2, (ymax - min(ymin, 0)) * s + 2, word(col, s, 1 - xmin * s, ymax * s + 1))
    write('hourback-mark.svg', 64, 64, mark_full('m'), "Hourback mark")
    write('hourback-mark-flat.svg', 64, 64, mark_flat(), "Hourback mark")
    write('hourback-mark-mono-navy.svg', 64, 64, mark_mono(N, 'n'), "Hourback mark")
    write('hourback-mark-mono-white.svg', 64, 64, mark_mono('#FFFFFF', 'w'), "Hourback mark")
    write('favicon.svg', 64, 64, mark_favicon(), "Hourback")

if __name__ == '__main__':
    main(sys.argv[1])
