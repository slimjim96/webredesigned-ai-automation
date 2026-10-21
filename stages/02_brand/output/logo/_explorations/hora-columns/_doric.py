"""Round 3 (owner, 2026-10-20: "narrower, simpler for smaller versions, more Greek"). HORA drawn from scratch in the
Doric order: plain tapered shafts with no bases, a cushion capital (echinus) under a square slab (abacus), standing
straight on the platform the way Greek columns do. Letters are about half as wide as they are tall.
F: three-step platform (a Greek temple's crepidoma). G: a meander (Greek key) band. H: unfluted, one step: the
simplest, and the small version of all three.
    ~/.cache/th-logo-venv/bin/python _doric.py
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '../..')))
import _build_logo as L

H = 100                 # letter height
C = 17                  # shaft width at the foot; it tapers to C - 3 under the capital
FLUTE = 2.2             # groove width; one groove per shaft, and only when fluted
ABA, ECH = 5, 5         # abacus and echinus heights

def R(x, y, w, h): return f'M{x:.2f} {y:.2f}h{w:.2f}v{h:.2f}h{-w:.2f}Z'
def poly(pts): return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'

def shaft(xb, xt, y0, y1, wb, wt, fluted):
    """Tapered shaft: foot from xb, wb wide; top from xt, wt wide. Fluted: split by one groove down the middle."""
    if not fluted: return poly([(xt, y0), (xt + wt, y0), (xb + wb, y1), (xb, y1)])
    hb, ht, g = (wb - FLUTE) / 2, (wt - FLUTE) / 2, FLUTE
    return (poly([(xt, y0), (xt + ht, y0), (xb + hb, y1), (xb, y1)])
            + poly([(xt + ht + g, y0), (xt + wt, y0), (xb + wb, y1), (xb + hb + g, y1)]))

def capital(cx, top, wt):
    """Abacus slab over an echinus that flares from the shaft top; centred on cx."""
    aw = wt + 9
    return R(cx - aw / 2, top, aw, ABA) + poly([(cx - aw / 2 + 1, top + ABA), (cx + aw / 2 - 1, top + ABA),
                                                (cx + wt / 2, top + ABA + ECH), (cx - wt / 2, top + ABA + ECH)])

def column(x, fluted, top=0, bottom=H, cap=True):
    """Doric column whose foot spans x .. x + C. No base: it stands on the platform."""
    wt = C - 3; xt = x + 1.5; y0 = top + (ABA + ECH if cap else 0)
    return (capital(x + C / 2, top, wt) if cap else '') + shaft(x, xt, y0, bottom, C, wt, fluted)

def letter_H(f):
    W = 52
    return column(0, f) + column(W - C, f) + R(C - 1, 46, W - 2 * C + 2, 9), W

def letter_O(f):
    """A tall, narrow ring: straight shafts for sides, round ends. One evenodd path, so a groove is just another hole."""
    W = 48; sw = C - 3; r = W / 2; ri = r - sw; tb = sw - 3                     # side and end thickness
    stad = lambda x0, y0, x1, y1, rr: (f'M{x0:.2f} {y0 + rr:.2f}A{rr:.2f} {rr:.2f} 0 0 1 {x1:.2f} {y0 + rr:.2f}'
                                       f'V{y1 - rr:.2f}A{rr:.2f} {rr:.2f} 0 0 1 {x0:.2f} {y1 - rr:.2f}Z')
    o = stad(0, 0, W, H, r) + stad(sw, tb, W - sw, H - tb, ri)
    if f:
        for gx in (sw / 2 - FLUTE / 2, W - sw / 2 - FLUTE / 2):
            o += R(gx, r, FLUTE, H - 2 * r)
    return f'__EVENODD__{o}', W

def letter_R(f):
    """A column whose bowl is a single Ionic scroll; a straight strut for the leg."""
    W = 52; bw = 11; r0 = 19; cx, cy = 30, r0 + bw / 2
    n = 70; outer, inner = [], []
    for i in range(n + 1):
        t = i / n; a = math.radians(-90 + 360 * 1.08 * t); rr = r0 + (5 - r0) * t; ww = bw * (1 - .4 * t)
        outer.append((cx + (rr + ww / 2) * math.cos(a), cy + (rr + ww / 2) * math.sin(a)))
        inner.append((cx + (rr - ww / 2) * math.cos(a), cy + (rr - ww / 2) * math.sin(a)))
    o = column(0, f, cap=True) + poly(outer + inner[::-1]) + R(C - 2, 0, cx - C + 2.5, bw)
    o += poly([(C - 1, 54), (C + 10, 54), (W, H), (W - 12, H)])
    return o, W

def letter_A(f):
    """Two columns leaning into a pediment."""
    W = 58; peak = 24; lean = 12
    o = poly([(W / 2, 0), (W + 2, peak), (-2, peak)]) + R(-2, peak + 1.8, W + 4, 4.5)
    y0 = peak + 1.8 + 4.5 + 1.8
    o += shaft(0, lean, y0, H, C, C - 3, f) + shaft(W - C, W - C + 3 - lean, y0, H, C, C - 3, f)
    o += R(C + 1, 66, W - 2 * C - 2, 8)
    return o, W

LETTERS = (letter_H, letter_O, letter_R, letter_A)

def meander(x, y, width, h, ink):
    """Greek key band: one hooked unit repeated, as filled strokes; h tall."""
    s = h / 5; unit = h * 2; n = max(1, round(width / unit)); unit = width / n; out = ''
    for i in range(n):
        ux = x + i * unit; k = unit / 6
        out += R(ux, y + h - s, unit, s)                                         # running bottom line
        out += R(ux, y, s, h)                                                    # rise
        out += R(ux, y, k * 4, s)                                                # top run
        out += R(ux + k * 4 - s, y, s, h * .62)                                  # drop
        out += R(ux + k * 2, y + h * .62 - s, k * 2, s)                          # back
        out += R(ux + k * 2, y + h * .38, s, h * .24)                            # hook up
    out += R(x + width - s, y, s, h)
    return f'<path fill="{ink}" d="{"".join(o for o in [out])}"/>'.replace('<path fill', '<g><path fill', 1).replace('/>', '/></g>', 1) if False else out

def hora(x, y, width, h, ink, fluted, base):
    """The four letters, centred over `width`, on a platform. Returns (svg, total height)."""
    k = h / H; gap = h * .34
    gl = [fn(fluted) for fn in LETTERS]
    total = sum(w for _, w in gl) * k + 3 * gap
    cx = x + (width - total) / 2; out = ''
    for g, w in gl:
        rule = ' fill-rule="evenodd"' if g.startswith('__EVENODD__') else ''
        out += f'<path transform="translate({cx:.2f} {y:.2f}) scale({k:.4f})" fill="{ink}"{rule} d="{g.replace('__EVENODD__', '')}"/>'
        cx += w * k + gap
    by = y + h
    if base == 'steps':                                                          # three steps, each a little wider
        d = ''; st = h * .07
        for i in range(3):
            ext = (total * .04) + i * h * .1
            d += R(x + (width - total) / 2 - ext, by + i * st, total + 2 * ext, st - .01)
        out += f'<path fill="{ink}" d="{d}"/>'; hh = h + 3 * st
    elif base == 'meander':
        mh = h * .2; bx = x + (width - total) / 2 - h * .12; bw = total + h * .24
        out += f'<path fill="{ink}" d="{R(bx, by, bw, h * .05)}{meander(bx, by + h * .09, bw, mh, ink)}"/>'
        hh = h + h * .09 + mh
    else:                                                                        # one plain step
        st = h * .09; ext = h * .1
        out += f'<path fill="{ink}" d="{R(x + (width - total) / 2 - ext, by, total + 2 * ext, st)}"/>'; hh = h + st
    return out, hh

def name_block(x, top, ink, fluted, base, scale):
    capH = L.cap(L.SERIF, L.SIZE); h = capH * scale; gap = capH * .24
    t, w = L.text(L.SERIF, 'Techne', L.SIZE, x, top + capH, ink, track=.01)
    lab, hh = hora(x, top + capH + gap, w, h, ink, fluted, base)
    return t + lab, w, capH + gap + hh

def horizontal(dark, fluted, base, scale=1.0, pad=12):
    ink = L.P if dark else L.N
    _, _, block = name_block(0, 0, ink, fluted, base, scale)
    Rr = block * .56; cx = cy = pad + Rr; x = cx + Rr + L.SIZE * .3
    t, w, _ = name_block(x, cy - block / 2, ink, fluted, base, scale)
    return x + w + pad, 2 * Rr + 2 * pad, L.dial(cx, cy, Rr, f'{base}{int(dark)}{int(fluted)}', dark) + t

def letters_sheet(fluted):
    out = ''; cx = 10
    for fn in LETTERS:
        g, w = fn(fluted); rule = ' fill-rule="evenodd"' if g.startswith('__EVENODD__') else ''
        out += f'<path transform="translate({cx} 10)" fill="{L.N}"{rule} d="{g.replace('__EVENODD__', '')}"/>'; cx += w + 30
    return cx - 20, H + 20, out

def write(name, w, h, body):
    with open(os.path.join(HERE, name), 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Techne Hora">{body}</svg>\n')

write('doric-letters-fluted.svg', *letters_sheet(True))
write('doric-letters-plain.svg', *letters_sheet(False))
for theme, dark in (('light', False), ('dark', True)):
    write(f'F-horizontal-{theme}.svg', *horizontal(dark, True, 'steps'))
    write(f'G-horizontal-{theme}.svg', *horizontal(dark, True, 'meander'))
    write(f'H-horizontal-{theme}.svg', *horizontal(dark, False, 'step'))
    write(f'small-horizontal-{theme}.svg', *horizontal(dark, False, 'step'))
print('ok')
