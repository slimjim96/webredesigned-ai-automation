"""Three Plex logo concepts where "Hora" is the clock, fades, or hides on the dial.

Needs fontTools + brotli and the Plex woff2 files in stages/03_design-system/output/fonts/:
    python _concepts.py
Writes A-/B-/C- SVGs next to this file and prints nothing else.
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(HERE, '../../../../../03_design-system/output/fonts'))
N, NL, P, B, E, BL = '#1B2A4A', '#2B4374', '#FAF7F0', '#A63D2A', '#E07A5F', '#F3D3C8'
DARK_BG = '#111B31'

def load(name, wght=None):
    f = TTFont(os.path.join(FONTS, name))
    return instantiateVariableFont(f, {'wght': wght}) if wght else f
SERIF, SANS_L, MONO = load('IBMPlexSerif-600.woff2'), load('IBMPlexSans-Variable.woff2', 300), load('IBMPlexMono-500.woff2')

def text(font, s, size, x, base, track=0.0, fill=N, per_char=None):
    """Outline text; returns (svg, advance width). per_char: list of fills, None skips a glyph (leaves its space)."""
    gs, cmap, hmtx, upm = font.getGlyphSet(), font.getBestCmap(), font['hmtx'], font['head'].unitsPerEm
    k = size / upm; out = []; cx = x
    for i, ch in enumerate(s):
        g = cmap[ord(ch)]; col = per_char[i] if per_char else fill
        if col is not None:
            pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, base)))
            out.append(f'<path d="{pen.getCommands()}" fill="{col}"/>')
        cx += hmtx[g][0] * k + track * size
    return ''.join(out), cx - x - track * size

def glyph_bounds(font, ch, size):
    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font['head'].unitsPerEm
    bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp); k = size / upm
    return [v * k for v in bp.bounds], font['hmtx'][cmap[ord(ch)]][0] * k

def cap(font, size): return font['OS/2'].sCapHeight * size / font['head'].unitsPerEm
def xh(font, size): return font['OS/2'].sxHeight * size / font['head'].unitsPerEm

def pt(cx, cy, deg, r):
    a = math.radians(deg); return cx + r * math.sin(a), cy - r * math.cos(a)
f2 = lambda p: f'{p[0]:.2f} {p[1]:.2f}'
def line(a, b, col, w): return f'<path d="M{f2(a)}L{f2(b)}" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round"/>'

def taper_arc(cx, cy, a0, a1, r, w0, w1, head):
    outer, inner, steps = [], [], 48
    for i in range(steps + 1):
        t = i / steps; a = a0 + (a1 - a0) * t; w = w0 + (w1 - w0) * t
        outer.append(pt(cx, cy, a, r + w / 2)); inner.append(pt(cx, cy, a, r - w / 2))
    tip = pt(cx, cy, a1 - head * 360 / (2 * math.pi * r), r); hw = w1 * 1.25 + head * .25
    d = 'M' + f2(outer[0]) + ''.join('L' + f2(p) for p in outer[1:])
    d += 'L' + f2(pt(cx, cy, a1, r + hw)) + 'L' + f2(tip) + 'L' + f2(pt(cx, cy, a1, r - hw))
    return d + ''.join('L' + f2(p) for p in reversed(inner)) + 'Z'

def sector(cx, cy, a0, a1, r):
    s, e = pt(cx, cy, a0, r), pt(cx, cy, a1, r)
    return f'M{cx:.2f} {cy:.2f}L{f2(s)}A{r:.2f} {r:.2f} 0 0 1 {f2(e)}Z'

def dial(cx, cy, R, dark=False, arrow=False, ring=True, signature=None, ticks12=True):
    """Clock of outer radius R. ring: navy bezel around a cream face. signature: tiny mono word on the lower face."""
    ringc = NL if dark else N
    face = R * (0.72 if ring else 1.0)
    o = []
    if ring: o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R:.2f}" fill="{ringc}"/>')
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face:.2f}" fill="{P}"/>')
    o.append(f'<path d="{sector(cx, cy, 300, 360, face * .82)}" fill="{BL}"/>')
    for a in range(0, 360, 30 if ticks12 else 90):
        major = a % 90 == 0
        o.append(line(pt(cx, cy, a, face * (.80 if major else .86)), pt(cx, cy, a, face * .93), N, face * (.075 if major else .045)))
    if signature:
        s = face * .17
        _, w = text(MONO, signature, s, 0, 0, track=.18)
        t, _ = text(MONO, signature, s, cx - w / 2, cy + face * .52, track=.18, fill=N)
        o.append(t)
    o.append(line((cx, cy), pt(cx, cy, 300, face * .50), B, face * .13))
    o.append(line((cx, cy), pt(cx, cy, 0, face * .70), N, face * .09))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face * .12:.2f}" fill="{N}"/><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face * .05:.2f}" fill="{P}"/>')
    if arrow:
        o.append(f'<path d="{taper_arc(cx, cy, 55, -95, R * .85, R * .03, R * .12, R * .2)}" fill="{E}"/>')
    return ''.join(o)

def svg(w, h, body, label, bg=None):
    rect = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{label}">{rect}{body}</svg>\n'

# ---------- A: the clock is the word ----------
def concept_a(dark=False):
    size, pad = 100, 8
    ink = P if dark else N
    capH = cap(SERIF, size); base = pad + capH + 6
    t, w = text(SERIF, 'Techne', size, pad, base, track=.01, fill=ink)
    R = capH * .62; gap = size * .26
    cx = pad + w + gap + R; cy = base - capH / 2
    return svg(cx + R + pad, base + 14, t + dial(cx, cy, R, dark), 'Techne Hora')

def icon_a():
    return svg(64, 64, dial(32, 32, 30), 'Techne Hora icon')

# ---------- B: the hour slipping away ----------
FADE_L = [N, '#5C6170', '#9AA0AC', '#C9CCD2']
FADE_D = [P, '#B8BFCC', '#7C869A', '#4A5674']
def concept_b(dark=False):
    size, pad = 100, 8
    ink = P if dark else N; fade = FADE_D if dark else FADE_L
    capH = cap(SERIF, size); base = pad + capH + 6
    t, w = text(SERIF, 'Techne', size, pad, base, track=.01, fill=ink)
    x = pad + w + size * .30
    hs = size * .92
    # "Hora" in light sans, wide tracking, each letter fainter; the o is a hairline clock
    (ox0, oy0, ox1, oy1), oadv = glyph_bounds(SANS_L, 'o', hs)
    h, _ = text(SANS_L, 'Hora', hs, x, base, track=.10, per_char=[fade[0], None, fade[2], fade[3]])
    _, hadv = glyph_bounds(SANS_L, 'H', hs)
    ocx = x + hadv + .10 * hs + (ox0 + ox1) / 2; ocy = base - (oy0 + oy1) / 2; r = (ox1 - ox0) / 2
    sw = hs * .045
    clock = (f'<circle cx="{ocx:.2f}" cy="{ocy:.2f}" r="{r - sw / 2:.2f}" fill="none" stroke="{fade[1]}" stroke-width="{sw:.2f}"/>'
             + line((ocx, ocy), pt(ocx, ocy, 300, r * .45), B, sw * 1.1) + line((ocx, ocy), pt(ocx, ocy, 0, r * .62), fade[1], sw))
    _, hw = text(SANS_L, 'Hora', hs, 0, 0, track=.10)
    return svg(x + hw + pad, base + 14, t + h + clock, 'Techne Hora')

def icon_b():
    # the fading set reduced to an icon: T plus a hairline clock
    size = 46; capH = cap(SERIF, size)
    t, w = text(SERIF, 'T', size, 6, 32 + capH / 2, fill=N)
    r = 11; cx, cy = 6 + w + 2 + r, 32 + capH / 2 - r
    c = (f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="none" stroke="#5C6170" stroke-width="2"/>'
         + line((cx, cy), pt(cx, cy, 300, r * .45), B, 2.4) + line((cx, cy), pt(cx, cy, 0, r * .62), '#5C6170', 2))
    return svg(64, 64, f'<rect width="64" height="64" rx="12" fill="{P}"/>' + t + c, 'Techne Hora icon')

# ---------- C: signed on the dial ----------
def concept_c(dark=False, stacked=False):
    ink = P if dark else N
    if stacked:
        size = 64; R = 70; W = 300
        capH = cap(SERIF, size)
        _, w = text(SERIF, 'Techne', size, 0, 0, track=.01)
        t, _ = text(SERIF, 'Techne', size, (W - w) / 2, 2 * R + 26 + capH, track=.01, fill=ink)
        return svg(W, 2 * R + 26 + capH + 12, dial(W / 2, R + 4, R, dark, arrow=True, signature='HORA') + t, 'Techne Hora')
    size, pad = 100, 8
    capH = cap(SERIF, size); R = capH * 1.05
    cy = pad + R + 2; cx = pad + R
    base = cy + capH / 2
    t, w = text(SERIF, 'Techne', size, cx + R + size * .28, base, track=.01, fill=ink)
    return svg(cx + R + size * .28 + w + pad, cy + R + pad, dial(cx, cy, R, dark, arrow=True, signature='HORA') + t, 'Techne Hora')

def icon_c():
    return svg(64, 64, dial(32, 32, 26, arrow=True, signature='HORA'), 'Techne Hora icon')

if __name__ == '__main__':
    out = {
        'A-horizontal-light.svg': concept_a(), 'A-horizontal-dark.svg': concept_a(True), 'A-icon.svg': icon_a(),
        'B-horizontal-light.svg': concept_b(), 'B-horizontal-dark.svg': concept_b(True), 'B-icon.svg': icon_b(),
        'C-horizontal-light.svg': concept_c(), 'C-horizontal-dark.svg': concept_c(True), 'C-icon.svg': icon_c(),
        'C-stacked-light.svg': concept_c(stacked=True), 'C-stacked-dark.svg': concept_c(True, True),
    }
    for name, s in out.items():
        with open(os.path.join(HERE, name), 'w') as fh:
            fh.write(s)
