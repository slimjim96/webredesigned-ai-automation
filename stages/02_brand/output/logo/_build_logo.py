"""Build the Techne Hora logo set: the C3 "dial label" design (owner's pick, 2026-10-18).

The mark is a navy-rimmed clock at 10:00 with the last two hours tinted; the name is "Techne" in IBM Plex Serif
standing on HORA, drawn from scratch as narrow, tall letters on a thin line (round 6 "N2", owner's pick 2026-10-22;
earlier rounds in `_explorations/hora-columns/`). One drawing at every size, so there is no separate small lockup.
The C1 rewind arrow is kept as a separate motion asset (`technehora-rewind*.svg`), never part of the logo itself.

Needs fontTools + brotli and the Plex woff2 files in stages/03_design-system/output/fonts/:
    python -m venv .venv && .venv/bin/pip install fonttools brotli
    .venv/bin/python _build_logo.py
PNGs come from `_render_png.py` (needs pillow and google-chrome).
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(OUT, '../../../03_design-system/output/fonts'))
SERIF = TTFont(os.path.join(FONTS, 'IBMPlexSerif-600.woff2'))
MONO = TTFont(os.path.join(FONTS, 'IBMPlexMono-500.woff2'))
NAME, SLUG = 'Techne Hora', 'technehora'

N, NL, P, B, E, BLUSH = '#1B2A4A', '#2B4374', '#FAF7F0', '#A63D2A', '#E07A5F', '#F3D3C8'


# ---------------------------------------------------------------- geometry
def pt(cx, cy, deg, r):
    a = math.radians(deg); return cx + r * math.sin(a), cy - r * math.cos(a)
f2 = lambda p: f'{p[0]:.2f} {p[1]:.2f}'
def line(a, b, col, w): return f'<path d="M{f2(a)}L{f2(b)}" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
def sector(cx, cy, a0, a1, r):
    s, e = pt(cx, cy, a0, r), pt(cx, cy, a1, r)
    return f'M{cx:.2f} {cy:.2f}L{f2(s)}A{r:.2f} {r:.2f} 0 0 1 {f2(e)}Z'
def ring(cx, cy, r0, r1):
    """Annulus as one evenodd path."""
    c = lambda r: f'M{cx - r:.2f} {cy:.2f}a{r:.2f} {r:.2f} 0 1 0 {2 * r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2 * r:.2f} 0Z'
    return c(r1) + c(r0)

def taper_arc(cx, cy, a0, a1, r, w0, w1, head, steps=48):
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps; a = a0 + (a1 - a0) * t; w = w0 + (w1 - w0) * t
        outer.append(pt(cx, cy, a, r + w / 2)); inner.append(pt(cx, cy, a, r - w / 2))
    tip = pt(cx, cy, a1 - head * 360 / (2 * math.pi * r), r); hw = w1 * 1.25 + head * .25
    return ('M' + 'L'.join(f2(p) for p in outer) + f'L{f2(pt(cx, cy, a1, r + hw))}L{f2(tip)}L{f2(pt(cx, cy, a1, r - hw))}'
            + ''.join('L' + f2(p) for p in reversed(inner)) + 'Z')


# ---------------------------------------------------------------- type
def text(font, s, size, x, base, fill, track=0.0):
    """Outline text to paths; returns (svg, advance width)."""
    gs, cmap, hmtx, k = font.getGlyphSet(), font.getBestCmap(), font['hmtx'], size / font['head'].unitsPerEm
    out, cx = [], x
    for ch in s:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, base)))
        out.append(f'<path d="{pen.getCommands()}" fill="{fill}"/>')
        cx += hmtx[g][0] * k + track * size
    return ''.join(out), cx - x - track * size

def cap(font, size): return font['OS/2'].sCapHeight * size / font['head'].unitsPerEm



# ---------------------------------------------------------------- HORA: narrow, tall letters on a line, no font
# Drawn in a 100-unit-tall box (round 6 "N2", owner's pick 2026-10-22): even strokes, each letter about half as
# wide as it is tall, spread over the middle 80% of "Techne" and standing on a thin line as wide as "Techne".
# The same drawing at every size; the spacing is what keeps it readable small.
DH, T, BAR = 100, 15, 13                         # height, stroke, horizontal strokes (a little lighter)
SPAN = .8                                        # HORA's share of the width of "Techne", centred

def _poly(pts): return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'
def _r(x, y, w, h): return _poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])             # clockwise
def _hole(pts): return _poly(pts[::-1])                                                        # counter-clockwise: a counter under nonzero
def _arc(cx, cy, r, a0, a1, n=24):
    """Points on a circle from a0 to a1 degrees (0 = right, 90 = down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def _stadium(x0, y0, x1, y1):
    r = (x1 - x0) / 2; cx = x0 + r
    return _arc(cx, y0 + r, r, 180, 360) + _arc(cx, y1 - r, r, 0, 180)

def _H():
    W = 46
    return _r(0, 0, T, DH) + _r(W - T, 0, T, DH) + _r(T, 47, W - 2 * T, BAR), W

def _O():
    W = 46
    return _poly(_stadium(0, 0, W, DH)) + _hole(_stadium(T, BAR, W - T, DH - BAR)), W

def _R():
    W = 46; bh = 56; rb = bh / 2; xc = W - rb
    bowl = _poly([(T - 1, 0)] + _arc(xc, rb, rb, -90, 90) + [(T - 1, bh)])
    counter = _hole([(T, BAR)] + _arc(xc, rb, rb - BAR, -90, 90) + [(T, bh - BAR)])
    x0, y0, x1, y1 = W * .40, bh - BAR, W - T * .55, DH                          # the leg, T wide across the stroke
    hw = T / 2 / math.sin(math.atan2(y1 - y0, x1 - x0))
    return _r(0, 0, T, DH) + bowl + counter + _poly([(x0 - hw, y0), (x0 + hw, y0), (x1 + hw, y1), (x1 - hw, y1)]), W

def _A():
    W = 52; ap = 7                                                                 # a flat apex, ap wide
    lean = math.atan2(DH, W / 2 - ap / 2); hw = T / math.sin(lean)                 # a leg's width along the foot
    yi = DH - (W / 2 - hw) * math.tan(lean)                                        # where the inner edges meet
    xl = (DH - 64) / math.tan(lean)
    return _poly([(0, DH), (W / 2 - ap / 2, 0), (W / 2 + ap / 2, 0), (W, DH), (W - hw, DH), (W / 2, yi), (hw, DH)]) + _r(xl, 64, W - 2 * xl, BAR), W

def hora(x, y, width, h, fill):
    """HORA over the middle SPAN of `width` (the width of "Techne"), `h` tall, on a line `width` wide.
    Returns (svg, height including the line)."""
    k = h / DH; gl = [f() for f in (_H, _O, _R, _A)]
    letters = sum(w for _, w in gl) * k; gap = (width * SPAN - letters) / 3; cx = x + width * (1 - SPAN) / 2; out = ''
    for d, w in gl:
        out += f'<path transform="translate({cx:.2f} {y:.2f}) scale({k:.4f})" fill="{fill}" d="{d}"/>'
        cx += w * k + gap
    lh, g = h * .09, h * .12
    return out + f'<path fill="{fill}" d="{_r(x - h * .08, y + h + g, width + h * .16, lh)}"/>', h + g + lh

# ---------------------------------------------------------------- the mark
def dial(cx, cy, R, uid, dark=False, soft=True, favicon=False, arrow=False):
    """Rim + face, four ticks, hands at 10:00, last two hours tinted.
    soft: the one soft touch, a faint shadow inside the top of the face so it sits just below the rim.
    favicon: heavier ticks and hands for 16-32px. arrow: the C1 rewind arc on the rim (motion asset only)."""
    face = R * .72; k = 1.3 if favicon else 1
    o = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R:.2f}" fill="{NL if dark else N}"/>',
         f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face:.2f}" fill="{P}"/>']
    if soft:
        o.append(f'<defs><clipPath id="f{uid}"><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face:.2f}"/></clipPath>'
                 f'<filter id="b{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{face * .05:.2f}"/></filter></defs>'
                 f'<g clip-path="url(#f{uid})"><circle cx="{cx:.2f}" cy="{cy + face * .06:.2f}" r="{face * 1.04:.2f}" fill="none" '
                 f'stroke="{N}" stroke-opacity=".22" stroke-width="{face * .12:.2f}" filter="url(#b{uid})"/></g>')
    o.append(f'<path d="{sector(cx, cy, 300, 360, face * .82)}" fill="{BLUSH}"/>')
    for a in (0, 90, 180, 270):
        o.append(line(pt(cx, cy, a, face * (.74 if favicon else .78)), pt(cx, cy, a, face * .92), N, face * .08 * k))
    o.append(line((cx, cy), pt(cx, cy, 300, face * .50), B, face * .13 * k))
    o.append(line((cx, cy), pt(cx, cy, 0, face * .70), N, face * .09 * k))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face * .11 * k:.2f}" fill="{N}"/>')
    if arrow:
        o.append(f'<path d="{taper_arc(cx, cy, 62, -48, R * .86, R * .025, R * .075, R * .14)}" fill="{E}"/>')
    return ''.join(o)

def dial_mono(cx, cy, R, ink):
    """One ink: the rim, ticks, and hands; the face and the tint are left open."""
    face = R * .72
    o = [f'<path d="{ring(cx, cy, face, R)}" fill="{ink}" fill-rule="evenodd"/>']
    for a in (0, 90, 180, 270):
        o.append(line(pt(cx, cy, a, face * .78), pt(cx, cy, a, face * .92), ink, face * .08))
    o.append(line((cx, cy), pt(cx, cy, 300, face * .50), ink, face * .13))
    o.append(line((cx, cy), pt(cx, cy, 0, face * .70), ink, face * .09))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face * .11:.2f}" fill="{ink}"/>')
    return ''.join(o)


# ---------------------------------------------------------------- lockups
SIZE = 100  # Techne set at 100 units; everything else is proportional

def name_block(x, top, ink):
    """Techne standing on HORA. Returns (svg, width, height)."""
    capH = cap(SERIF, SIZE); gap = capH * .24
    g = SERIF['glyf'][SERIF.getBestCmap()[ord('h')]]
    asc = max(capH, g.yMax * SIZE / SERIF['head'].unitsPerEm)                    # the h rises above the caps
    t, w = text(SERIF, 'Techne', SIZE, x, top + asc, ink, track=.01)
    lab, hh = hora(x, top + asc + gap, w, capH, ink)
    return t + lab, w, asc + gap + hh

def horizontal(dark=False, pad=12):
    ink = P if dark else N
    _, _, block = name_block(0, 0, ink)
    R = block * .56; cx = cy = pad + R; x = cx + R + SIZE * .3
    t, w, _ = name_block(x, cy - block / 2, ink)
    return x + w + pad, 2 * R + 2 * pad, dial(cx, cy, R, f'h{int(dark)}', dark) + t

def stacked(dark=False):
    ink = P if dark else N
    size = 64; R = 70; scale = size / SIZE
    t, w, block = name_block(0, 0, ink)
    W = max(w * scale, 2 * R) + 40
    top = 2 * R + 30
    body = (dial(W / 2, R + 6, R, f's{int(dark)}', dark)
            + f'<g transform="translate({(W - w * scale) / 2:.2f} {top:.2f}) scale({scale:.4f})">{t}</g>')
    return W, top + block * scale + 14, body

def wordmark(dark=False, pad=4):
    ink = P if dark else N
    t, w, block = name_block(pad, pad, ink)
    return w + 2 * pad, block + 2 * pad, t


# ---------------------------------------------------------------- motion assets (C1 arrow)
def rewind_spinner():
    """The rewind arc turning counter-clockwise around a still face. For loading states; stops for reduced motion."""
    c, R = 32, 30
    arc = f'<path d="{taper_arc(c, c, 62, -48, R * .86, R * .025, R * .075, R * .14)}" fill="{E}"/>'
    style = ('<style>.th-rw{transform-origin:32px 32px;animation:th-rw 1.6s cubic-bezier(.45,0,.25,1) infinite}'
             '@keyframes th-rw{to{transform:rotate(-360deg)}}'
             '@media (prefers-reduced-motion:reduce){.th-rw{animation:none}}</style>')
    return style + dial(c, c, R, 'sp', soft=False) + f'<g class="th-rw">{arc}</g>'


def write(name, w, h, body, label=NAME):
    with open(os.path.join(OUT, name), 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{label}">{body}</svg>\n')

def main():
    for theme, dark in (('light', False), ('dark', True)):
        write(f'{SLUG}-lockup-horizontal-{theme}.svg', *horizontal(dark))
        write(f'{SLUG}-lockup-stacked-{theme}.svg', *stacked(dark))
        write(f'{SLUG}-wordmark-{theme}.svg', *wordmark(dark))
    write(f'{SLUG}-mark.svg', 64, 64, dial(32, 32, 30, 'm'), f'{NAME} mark')
    write(f'{SLUG}-mark-flat.svg', 64, 64, dial(32, 32, 30, 'mf', soft=False), f'{NAME} mark')
    write(f'{SLUG}-mark-mono-navy.svg', 64, 64, dial_mono(32, 32, 30, N), f'{NAME} mark')
    write(f'{SLUG}-mark-mono-white.svg', 64, 64, dial_mono(32, 32, 30, '#FFFFFF'), f'{NAME} mark')
    write('favicon.svg', 64, 64, dial(32, 32, 31, 'fv', soft=False, favicon=True), f'{NAME} icon')
    write(f'{SLUG}-rewind.svg', 64, 64, dial(32, 32, 30, 'rw', arrow=True), f'{NAME}: time wound back')
    write(f'{SLUG}-rewind-spinner.svg', 64, 64, rewind_spinner(), 'Loading')

if __name__ == '__main__':
    main()
