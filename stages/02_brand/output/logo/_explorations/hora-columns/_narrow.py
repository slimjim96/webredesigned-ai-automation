"""Round 5 (owner, 2026-10-22: "not as building like, more just narrow and tall; readable in smaller versions").
HORA drawn from scratch as plain, narrow, even strokes (letters about half as wide as tall), spread to the width of
"Techne" so the gaps carry it at small sizes. No roofs or capitals; the column idea is reduced to a hint:
L: plain strokes.
M: L with short flat ends on the stems, top and bottom (a slab under and over each, like a column's foot and top).
N: L on a thin line, the last of the temple step.
    ~/.cache/th-logo-venv/bin/python _narrow.py
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '../..')))
import _build_logo as L

DH = 100
T = 15                  # stroke
BAR = 13                # horizontal strokes are a little lighter, as in drawn capitals
WIDTH = dict(H=46, O=46, R=46, A=52)

def poly(pts): return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'
def rect(x, y, w, h): return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])        # clockwise
def arc(cx, cy, r, a0, a1, n=24):
    """Points on a circle from a0 to a1 degrees (0 = right, 90 = down: the SVG y-axis)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def hole(pts): return poly(pts[::-1])                                                    # counter-clockwise: cut out under nonzero

def stadium(x0, y0, x1, y1):
    r = (x1 - x0) / 2; cx = x0 + r
    return arc(cx, y0 + r, r, 180, 360) + arc(cx, y1 - r, r, 0, 180)

def feet(x, s, top=True, bottom=True):
    """M only: a short slab over and under a stem whose foot is x .. x + T."""
    if not s.get('slabs'): return ''
    e, h = 3.5, 4
    return (rect(x - e, 0, T + 2 * e, h) if top else '') + (rect(x - e, DH - h, T + 2 * e, h) if bottom else '')

def H(s):
    W = WIDTH['H']
    return rect(0, 0, T, DH) + rect(W - T, 0, T, DH) + rect(T, 47, W - 2 * T, BAR) + feet(0, s) + feet(W - T, s), W

def O(s):
    W = WIDTH['O']
    return poly(stadium(0, 0, W, DH)) + hole(stadium(T, BAR, W - T, DH - BAR)), W

def R(s):
    W = WIDTH['R']; bh = 56; rb = bh / 2; ri = rb - BAR; xc = W - rb
    bowl = poly([(T - 1, 0)] + arc(xc, rb, rb, -90, 90) + [(T - 1, bh)])
    counter = hole([(T, BAR)] + arc(xc, rb, ri, -90, 90) + [(T, bh - BAR)])
    # leg: from under the bowl to the foot at the right, T wide measured across the stroke
    x0, y0, x1, y1 = W * .40, bh - BAR, W - T * .55, DH
    hw = T / 2 / math.sin(math.atan2(y1 - y0, x1 - x0))
    leg = poly([(x0 - hw, y0), (x0 + hw, y0), (x1 + hw, y1), (x1 - hw, y1)])
    return rect(0, 0, T, DH) + bowl + counter + leg + feet(0, s), W

def A(s):
    W = WIDTH['A']; ap = 7                                                      # a flat apex, ap wide
    lx = math.atan2(DH, W / 2 - ap / 2); hw = T / math.sin(lx)                   # horizontal width of a leg
    out = [(0, DH), (W / 2 - ap / 2, 0), (W / 2 + ap / 2, 0), (W, DH), (W - hw, DH)]
    yi = DH - (W / 2 - hw) * math.tan(lx)                                         # where the inner edges meet
    out += [(W / 2, yi), (hw, DH)]
    y = 64; xl = (DH - y) / math.tan(lx); bar = rect(xl, y, W - 2 * xl, BAR)
    o = poly(out) + bar
    if s.get('slabs'):
        e, h = 3, 4; o += rect(-e, DH - h, hw + 2 * e, h) + rect(W - hw - e, DH - h, hw + 2 * e, h)
    return o, W

def hora(x, y, width, h, fill, s):
    """HORA spread to `width` (the width of "Techne"), `h` tall. Returns (svg, height including the line)."""
    k = h / DH; gl = [f(s) for f in (H, O, R, A)]
    letters = sum(w for _, w in gl) * k; gap = (width - letters) / 3; cx = x; out = ''
    for d, w in gl:
        out += f'<path transform="translate({cx:.2f} {y:.2f}) scale({k:.4f})" fill="{fill}" d="{d}"/>'
        cx += w * k + gap
    if not s.get('line'): return out, h
    lh = h * .09; g = h * .12
    return out + f'<path fill="{fill}" d="{rect(x - h * .08, y + h + g, width + h * .16, lh)}"/>', h + g + lh

L.hora = hora                                                                     # name_block() looks it up at call time
VARIANTS = dict(L=dict(steps=0), M=dict(steps=0, slabs=True), N=dict(steps=0, line=True))

def write(name, w, h, body):
    with open(os.path.join(HERE, name), 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Techne Hora">{body}</svg>\n')

for key, s in VARIANTS.items():
    for theme, dark in (('light', False), ('dark', True)):
        write(f'{key}-horizontal-{theme}.svg', *L.horizontal(dark, s=s))
    d, hh = hora(10, 10, 300, 100, L.N, s)
    write(f'{key}-letters.svg', 320, hh + 20, d)
print('ok')
