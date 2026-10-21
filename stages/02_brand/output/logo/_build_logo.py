"""Build the Techne Hora logo set: the C3 "dial label" design (owner's pick, 2026-10-18).

The mark is a navy-rimmed clock at 10:00 with the last two hours tinted; the name is "Techne" in IBM Plex Serif
standing on HORA, drawn from scratch as Doric columns on a temple's three steps (round 3 "F", owner's pick
2026-10-20). Small lockups (`-small`, for under 60px) drop the flutes, thicken the shafts and use one step.
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



# ---------------------------------------------------------------- HORA: Doric columns, no font
# Drawn in a 100-unit-tall box. Doric: tapered shafts with no bases, a cushion (echinus) under a square slab (abacus),
# standing straight on the platform. FULL is fluted on three steps; SMALL is plain, heavier and on one step.
FULL = dict(C=17, flute=2.2, steps=3, gap=.34)
SMALL = dict(C=20, flute=0, steps=1, gap=.40)
DH, ABA, ECH = 100, 5, 5

def _r(x, y, w, h): return f'M{x:.2f} {y:.2f}h{w:.2f}v{h:.2f}h{-w:.2f}Z'
def _poly(pts): return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'

def _shaft(xb, xt, y0, y1, wb, wt, flute):
    """Tapered shaft: foot from xb, wb wide; top from xt, wt wide; split by one groove when flute > 0."""
    if not flute: return _poly([(xt, y0), (xt + wt, y0), (xb + wb, y1), (xb, y1)])
    hb, ht = (wb - flute) / 2, (wt - flute) / 2
    return (_poly([(xt, y0), (xt + ht, y0), (xb + hb, y1), (xb, y1)])
            + _poly([(xt + ht + flute, y0), (xt + wt, y0), (xb + wb, y1), (xb + hb + flute, y1)]))

def _column(x, s):
    C = s['C']; wt = C - 3; cx = x + C / 2; aw = wt + 9
    cap = _r(cx - aw / 2, 0, aw, ABA) + _poly([(cx - aw / 2 + 1, ABA), (cx + aw / 2 - 1, ABA), (cx + wt / 2, ABA + ECH), (cx - wt / 2, ABA + ECH)])
    return cap + _shaft(x, x + 1.5, ABA + ECH, DH, C, wt, s['flute'])

def _H(s):
    C = s['C']; W = 52 + (C - 17) * 1.5
    return _column(0, s) + _column(W - C, s) + _r(C - 1, 46, W - 2 * C + 2, 9 + (C - 17) * .5), W

def _O(s):
    """A tall ring with straight sides; one evenodd path, so a flute is just another hole."""
    C = s['C']; W = 48 + (C - 17) * 1.5; sw = C - 3; r = W / 2; ri = r - sw; tb = sw - 3
    stad = lambda x0, y0, x1, y1, rr: (f'M{x0:.2f} {y0 + rr:.2f}A{rr:.2f} {rr:.2f} 0 0 1 {x1:.2f} {y0 + rr:.2f}'
                                       f'V{y1 - rr:.2f}A{rr:.2f} {rr:.2f} 0 0 1 {x0:.2f} {y1 - rr:.2f}Z')
    o = stad(0, 0, W, DH, r) + stad(sw, tb, W - sw, DH - tb, ri)
    if s['flute']:
        for gx in (sw / 2 - s['flute'] / 2, W - sw / 2 - s['flute'] / 2):
            o += _r(gx, r, s['flute'], DH - 2 * r)
    return o, W

def _R(s):
    """A column whose bowl is a single Ionic scroll (small: a plain bowl with an eye); a strut for the leg."""
    C = s['C']; W = 52 + (C - 17) * 1.5; bw = 11 + (C - 17) * .6; r0 = 19; cx, cy = C + 13, r0 + bw / 2
    if s['flute']:
        n = 70; outer, inner = [], []
        for i in range(n + 1):
            t = i / n; a = math.radians(-90 + 360 * 1.08 * t); rr = r0 + (5 - r0) * t; ww = bw * (1 - .4 * t)
            outer.append((cx + (rr + ww / 2) * math.cos(a), cy + (rr + ww / 2) * math.sin(a)))
            inner.append((cx + (rr - ww / 2) * math.cos(a), cy + (rr - ww / 2) * math.sin(a)))
        bowl = _poly(outer + inner[::-1])
    else:
        ro = r0 + bw / 2; ri = r0 - bw / 2
        bowl = (f'M{cx:.2f} 0A{ro:.2f} {ro:.2f} 0 0 1 {cx:.2f} {2 * ro:.2f}H{C - 2:.2f}V{2 * ro - bw:.2f}H{cx:.2f}'
                f'A{ri:.2f} {ri:.2f} 0 0 0 {cx:.2f} {bw:.2f}Z')
    o = _column(0, s) + bowl + _r(C - 2, 0, cx - C + 2.5, bw)
    o += _poly([(C - 1, 54), (C + 11, 54), (W, DH), (W - 13, DH)])
    return o, W

def _A(s):
    """Two columns leaning into a pediment. Small: the pediment and its cornice are one solid piece."""
    C = s['C']; W = 58 + (C - 17) * 1.5; peak, lean = 24, 12
    if s['flute']:
        o = _poly([(W / 2, 0), (W + 2, peak), (-2, peak)]) + _r(-2, peak + 1.8, W + 4, 4.5); y0 = peak + 8.1
    else:
        o = _poly([(W / 2, 0), (W + 2, peak), (W + 2, peak + 6), (-2, peak + 6), (-2, peak)]); y0 = peak + 6
    o += _shaft(0, lean, y0, DH, C, C - 3, s['flute']) + _shaft(W - C, W - C + 3 - lean, y0, DH, C, C - 3, s['flute'])
    o += _r(C + 1, 66, W - 2 * C - 2, 8 + (C - 17) * .5)
    return o, W

def hora(x, y, width, h, fill, s):
    """H O R A centred over `width`, `h` tall, on the platform. Returns (svg, height including the steps)."""
    k = h / DH; gap = h * s['gap']; gl = [f(s) for f in (_H, _O, _R, _A)]
    rules = ['nonzero', 'evenodd', 'nonzero', 'nonzero']                        # only the O's counter and flutes are holes
    total = sum(w for _, w in gl) * k + 3 * gap; left = x + (width - total) / 2; cx = left; out = ''
    for (d, w), rule in zip(gl, rules):
        out += f'<path transform="translate({cx:.2f} {y:.2f}) scale({k:.4f})" fill="{fill}" fill-rule="{rule}" d="{d}"/>'
        cx += w * k + gap
    st = h * (.07 if s['steps'] == 3 else .1); d = ''
    for i in range(s['steps']):
        ext = total * .04 + i * h * .1
        d += _r(left - ext, y + h + i * st, total + 2 * ext, st - (.01 if s['steps'] > 1 else 0))
    return out + f'<path fill="{fill}" d="{d}"/>', h + s['steps'] * st

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

def name_block(x, top, ink, s=FULL):
    """Techne standing on HORA. Returns (svg, width, height)."""
    capH = cap(SERIF, SIZE); gap = capH * .24
    g = SERIF['glyf'][SERIF.getBestCmap()[ord('h')]]
    asc = max(capH, g.yMax * SIZE / SERIF['head'].unitsPerEm)                    # the h rises above the caps
    t, w = text(SERIF, 'Techne', SIZE, x, top + asc, ink, track=.01)
    lab, hh = hora(x, top + asc + gap, w, capH, ink, s)
    return t + lab, w, asc + gap + hh

def horizontal(dark=False, pad=12, s=FULL):
    ink = P if dark else N
    _, _, block = name_block(0, 0, ink, s)
    R = block * .56; cx = cy = pad + R; x = cx + R + SIZE * .3
    t, w, _ = name_block(x, cy - block / 2, ink, s)
    return x + w + pad, 2 * R + 2 * pad, dial(cx, cy, R, f'h{int(dark)}{s["steps"]}', dark, soft=s is FULL) + t

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
        write(f'{SLUG}-lockup-horizontal-small-{theme}.svg', *horizontal(dark, s=SMALL))
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
