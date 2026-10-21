"""HORA drawn as architecture, no font (owner, 2026-10-20: "use your creativity and build from scratch").
H: two fluted columns tied by a lintel. O: a ring whose sides are fluted shafts. R: a column whose bowl is an
Ionic volute. A: two columns leaning into a pediment. All four stand on a stepped stylobate, the base "Techne" sits on.
Drawn in a 100-unit-tall design space, then scaled into the lockup.
    ~/.cache/th-logo-venv/bin/python _temple.py
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '../..')))
import _build_logo as L

H = 100            # letter height in design units
C = 24             # column (shaft) width
CAP, BASE = 9, 9   # capital and base block heights
F = 2.6            # flute (gap) width
FLUTES = True      # off for the small-size version: flutes turn to noise under ~60px

def R(x, y, w, h): return f'M{x:.2f} {y:.2f}h{w:.2f}v{h:.2f}h{-w:.2f}Z'
def poly(pts): return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'

def shaft(x0b, x0t, y0, y1, w, flutes=None):
    """A shaft from y0 (top) to y1 (bottom), left edge at x0t on top and x0b at the foot, split by two flutes."""
    if flutes is None: flutes = FLUTES
    if not flutes: return poly([(x0t, y0), (x0t + w, y0), (x0b + w, y1), (x0b, y1)])
    strip = (w - 2 * F) / 3; out = ''
    for i in range(3):
        o = i * (strip + F)
        out += poly([(x0t + o, y0), (x0t + o + strip, y0), (x0b + o + strip, y1), (x0b + o, y1)])
    return out

def column(x, top=0, bottom=H, cap=True, base=True, flutes=None):
    """Upright column: abacus + echinus on top, plinth at the foot, fluted shaft between."""
    o = ''; y0 = top; y1 = bottom
    if cap:
        o += R(x - 5, top, C + 10, CAP * .55)                                    # abacus
        o += poly([(x - 3, top + CAP * .55), (x + C + 3, top + CAP * .55), (x + C, top + CAP), (x, top + CAP)])  # echinus
        y0 = top + CAP + 1.6
    if base:
        o += R(x - 5, bottom - BASE * .5, C + 10, BASE * .5)                     # plinth
        o += R(x - 2.5, bottom - BASE, C + 5, BASE * .5 - 1.2)                   # torus
        y1 = bottom - BASE - 1.6
    return o + shaft(x, x, y0, y1, C, flutes)

def letter_H():
    W = 78
    beam = R(C - 1, 44, W - 2 * C + 2, 12)
    return column(0) + column(W - C) + beam, W

def letter_O():
    """Two fluted shafts joined by a shallow arch above and an inverted arch below."""
    W = 76; rx = W / 2; ry = 27; ix = rx - C; iy = ry - 13
    def arch(y, up):
        s, d = (1, -1) if up else (0, 1)
        return (f'M0 {y:.2f}A{rx:.2f} {ry:.2f} 0 0 {s} {W:.2f} {y:.2f}H{W - C:.2f}'
                f'A{ix:.2f} {iy:.2f} 0 0 {1 - s} {C:.2f} {y:.2f}Z')
    o = arch(ry, True) + arch(H - ry, False)
    for x in (0, W - C):                                                         # collars where shaft meets arch
        o += R(x - 2, ry + 1.6, C + 4, 3.4) + R(x - 2, H - ry - 5, C + 4, 3.4)
        o += shaft(x, x, ry + 6.6, H - ry - 6.6, C)
    return o, W

def volute(cx, cy, r0, r1, turns, w):
    """A spiral band (Ionic volute) as a filled path: outer edge out to r0, tapering to an eye of radius r1."""
    n = 90; outer, inner = [], []
    for i in range(n + 1):
        t = i / n; a = math.radians(-90 + 360 * turns * t); r = r0 + (r1 - r0) * t; ww = w * (1 - .45 * t)
        outer.append((cx + (r + ww / 2) * math.cos(a), cy + (r + ww / 2) * math.sin(a)))
        inner.append((cx + (r - ww / 2) * math.cos(a), cy + (r - ww / 2) * math.sin(a)))
    eye = f'M{cx + r1 * .9:.2f} {cy:.2f}a{r1 * .9:.2f} {r1 * .9:.2f} 0 1 0 0 .01Z'
    return poly(outer + inner[::-1]), (cx, cy, r1)

def letter_R():
    W = 76; bw = 14                                                              # bowl band width
    o = column(0, base=True)
    # bowl: a band leaves the capital and curls clockwise into an Ionic volute
    r0 = 24; cx, cy = 46, r0 + bw / 2
    band, _ = volute(cx, cy, r0, 6, 1.3, bw)
    o += band + R(C, 0, cx - C + .5, bw) + f'M{cx + 4.5:.2f} {cy:.2f}a4.5 4.5 0 1 0 0 .01Z'
    # leg: a strut from under the bowl down to its own plinth
    o += poly([(C - 1, 50), (C + 15, 50), (W - 2, H - BASE), (W - 18, H - BASE)])
    o += R(W - 24, H - BASE * .5, 27, BASE * .5) + R(W - 21, H - BASE, 21, BASE * .5 - 1.2)
    return o, W

def letter_A():
    W = 90; peak = 34  # pediment height
    lean = 12
    o = ''
    # pediment: a gable over the two columns, with a cornice under it
    o += poly([(W / 2, 0), (W + 1, peak), (-1, peak)])
    o += R(-1, peak + 2.4, W + 2, 6.5)                                          # cornice / architrave
    # columns leaning in toward the gable
    y0, y1 = peak + 11, H - BASE - 1.6
    o += shaft(2, 2 + lean, y0, y1, C)
    o += shaft(W - C - 2, W - C - 2 - lean, y0, y1, C)
    # crossbar
    o += R(2 + lean * .5 + C - 3, 68, W - 2 * (2 + lean * .5 + C - 3), 10)
    # bases
    for x in (2, W - C - 2):
        o += R(x - 5, H - BASE * .5, C + 10, BASE * .5) + R(x - 2.5, H - BASE, C + 5, BASE * .5 - 1.2)
    return o, W

def hora(x, y, width, h, fill, bg, dots=True):
    """The four letters, spread across `width`, on a two-step stylobate. Returns (svg, total height)."""
    k = h / H
    glyphs = [letter_H(), letter_O(), letter_R(), letter_A()]
    total = sum(w for _, w in glyphs) * k
    gap = (width - total) / 3
    out = ''; cx = x
    for i, (g, w) in enumerate(glyphs):
        g = g if g.startswith('<') else f'<path d="{g}"/>'
        g = g.replace('<path data-cut="1"', f'<path fill="{bg}"')
        out += f'<g transform="translate({cx:.2f} {y:.2f}) scale({k:.4f})" fill="{fill}">{g}</g>'
        if dots and i < 3:
            d = cx + w * k + gap / 2
            out += f'<path fill="{fill}" d="M{d:.2f} {y + h * .40:.2f}l{h * .07:.2f} {h * .07:.2f}l{-h * .07:.2f} {h * .07:.2f}l{-h * .07:.2f} {-h * .07:.2f}Z"/>'
        cx += w * k + gap
    s1, s2 = h * .075, h * .06
    out += f'<rect x="{x - h * .06:.2f}" y="{y + h + h * .05:.2f}" width="{width + h * .12:.2f}" height="{s1:.2f}" fill="{fill}"/>'
    out += f'<rect x="{x - h * .16:.2f}" y="{y + h + h * .05 + s1 + h * .035:.2f}" width="{width + h * .32:.2f}" height="{s2:.2f}" fill="{fill}"/>'
    return out, h * (1 + .05 + .035) + s1 + s2

def name_block(x, top, ink, bg, scale=.62, dots=True):
    capH = L.cap(L.SERIF, L.SIZE); h = capH * scale; gap = capH * .26
    t, w = L.text(L.SERIF, 'Techne', L.SIZE, x, top + capH, ink, track=.01)
    lab, hh = hora(x + 6, top + capH + gap, w - 12, h, ink, bg, dots)
    return t + lab, w, capH + gap + hh

def horizontal(dark=False, pad=12, **kw):
    ink, bg = (L.P, L.N) if dark else (L.N, L.P)
    _, _, block = name_block(0, 0, ink, bg, **kw)
    Rr = block * .58; cx = cy = pad + Rr; x = cx + Rr + L.SIZE * .3
    t, w, _ = name_block(x, cy - block / 2, ink, bg, **kw)
    return x + w + pad, 2 * Rr + 2 * pad, L.dial(cx, cy, Rr, f't{int(dark)}', dark) + t

def big():
    """The four letters alone, large, for judging the drawing."""
    out = ''; cx = 10
    for g, w in (letter_H(), letter_O(), letter_R(), letter_A()):
        g = g if g.startswith('<') else f'<path d="{g}"/>'
        g = g.replace('<path data-cut="1"', f'<path fill="{L.P}"')
        out += f'<g transform="translate({cx} 10)" fill="{L.N}">{g}</g>'; cx += w + 26
    return cx - 16, H + 20, out

def write(name, w, h, body):
    with open(os.path.join(HERE, name), 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Techne Hora">{body}</svg>\n')

for theme, dark in (('light', False), ('dark', True)):
    write(f'D-horizontal-{theme}.svg', *horizontal(dark))
    write(f'E-horizontal-{theme}.svg', *horizontal(dark, scale=.9, dots=False))
write('D-letters.svg', *big())
FLUTES = False
for theme, dark in (('light', False), ('dark', True)):
    write(f'E-small-{theme}.svg', *horizontal(dark, scale=.9, dots=False))
print('ok')
