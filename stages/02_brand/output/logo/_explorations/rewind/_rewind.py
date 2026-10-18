"""Rewind round: three quiet Techne Hora marks, each hiding one small "time back" puzzle.

Every proportion is a power of phi (PHI below); the construction notes in NOTES say which.
Reuses the drawing helpers in ../bold/_bold.py. Needs fontTools + brotli and the Plex woff2 files in
stages/03_design-system/output/fonts/:
    python _rewind.py
Writes <n>-<name>-3d.svg, -flat.svg, and -lockup-{quiet,clock-o,dial}.svg next to this file.
"""
import importlib.util, math, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('bold', os.path.join(HERE, '../bold/_bold.py'))
bold = importlib.util.module_from_spec(spec); spec.loader.exec_module(bold)
from_bold = ('Doc', 'pt', 'poly', 'f2', 'text', 'cap', 'SERIF', 'MONO', 'FONTS',
             'N', 'NL', 'NLL', 'ND', 'NDD', 'P', 'P2', 'P3', 'B', 'BL', 'BD', 'E', 'EL', 'ED', 'BLUSH')
globals().update({k: getattr(bold, k) for k in from_bold})
SANS_LIGHT = instancer.instantiateVariableFont(TTFont(os.path.join(FONTS, 'IBMPlexSans-Variable.woff2')), {'wght': 300})
G = '#5C6170'  # graphite
PHI = (1 + 5 ** .5) / 2


def xheight(font, size): return font['OS/2'].sxHeight * size / font['head'].unitsPerEm

def mix(a, b, t):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02X}' for x, y in zip(a, b))

def ramp(stops, t):
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1: return mix(c0, c1, (t - t0) / (t1 - t0) if t1 > t0 else 0)
    return stops[-1][1]

def clip(d, shape):
    i = d._id(); d.defs.append(f'<clipPath id="{i}">{shape}</clipPath>'); return f' clip-path="url(#{i})"'

def band(cx, cy, a0, a1, r_in, r_out, steps=90, tip=0):
    """Annulus segment from a0 to a1 (clock degrees); tip>0 ends it in a point that stays inside the band."""
    rc = (r_in + r_out) / 2
    ang = [a0 + (a1 - a0) * i / steps for i in range(steps + 1)]
    outer = [pt(cx, cy, a, r_out) for a in ang]; inner = [pt(cx, cy, a, r_in) for a in ang[::-1]]
    if not tip: return poly(outer + inner)
    sign = 1 if a1 > a0 else -1
    return poly(outer + [pt(cx, cy, a1 + sign * tip * 180 / (math.pi * rc), rc)] + inner)


# ---------------------------------------------------------------- 1. Back Hands
# A clock at 2:18, the one time its hands are mirror images about 3 o'clock. Together they make "<".
# Their ember echo, one hand-width-of-the-dial to the left, makes a second "<": the two read as « (rewind).
R1 = 200; FACE1 = R1 - R1 / PHI ** 5; L1 = FACE1 / PHI; HW1 = L1 / PHI ** 4
m = 120 / 6.5; H_DEG, M_DEG = 60 + m / 2, 6 * m  # 2:18.46 -> 69.2 deg and 110.8 deg
L_HOUR = L1 / PHI ** .5
ECHO = L1 * math.sin(math.radians(H_DEG))  # shift that centres « in the dial

def hands_path(cx, cy):
    return (f'M{f2(pt(cx, cy, H_DEG, L_HOUR))}L{cx:.2f} {cy:.2f}L{f2(pt(cx, cy, M_DEG, L1))}')

def back_hands(flat=False):
    d = Doc('bh', flat); c = 256
    o = [f'<g{d.shadow(12, 16, .32)}>',
         f'<circle cx="{c}" cy="{c}" r="{R1}" fill="{d.lin([(0, NLL), (.5, N), (1, NDD)], .2, 0, .8, 1)}"/>']
    if not flat:
        o.append(f'<circle cx="{c}" cy="{c}" r="{R1 - 1.5}" fill="none" stroke="{d.lin([(0, "#FFFFFF", .5), (.45, "#FFFFFF", 0)])}" stroke-width="3"/>')
    o.append('</g>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{FACE1:.2f}" fill="{d.rad([(0, "#FFFFFF"), (.7, P), (1, P2)], .42, .36, .66, flat=P)}"/>')
    if not flat:  # the face sits a little below the rim
        face = f'<circle cx="{c}" cy="{c}" r="{FACE1:.2f}"/>'
        o.append(f'<g{clip(d, face)}><circle cx="{c}" cy="{c + 7}" r="{FACE1 + 6:.2f}" fill="none" stroke="{NDD}" stroke-opacity=".28" stroke-width="16"{d.blur(6)}/></g>')
    for a in (0, 90, 180, 270):
        o.append(f'<path d="M{f2(pt(c, c, a, FACE1 - FACE1 / PHI ** 4))}L{f2(pt(c, c, a, FACE1 - FACE1 / PHI ** 6))}" stroke="{N}" stroke-width="{HW1 / PHI:.2f}" stroke-linecap="round"/>')
    sh = d.shadow(4, 3, .3)
    echo = d.lin([(0, EL), (.6, E), (1, B)], 0, 0, .4, 1, flat=E)
    o.append(f'<path d="{hands_path(c - ECHO, c)}" fill="none" stroke="{echo}" stroke-width="{HW1:.2f}" stroke-linecap="round" stroke-linejoin="round"{sh}/>')
    hand = d.lin([(0, NLL), (1, ND)], 0, 0, 0, 1, flat=N)
    o.append(f'<path d="{hands_path(c, c)}" fill="none" stroke="{hand}" stroke-width="{HW1:.2f}" stroke-linecap="round" stroke-linejoin="round"{sh}/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{HW1 / PHI ** 2:.2f}" fill="{P}"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora: clock hands that read as rewind')


# ---------------------------------------------------------------- 2. Golden Unwind
# A golden spiral (radius grows by phi every quarter turn) wound like a mainspring. It runs out from the
# pivot counter-clockwise, so the hand at its tip is sweeping backward.
R2 = 200; SWEEP = 630; K2 = 1 / PHI ** 3

def spiral(d, flat, px, py, depth):
    n = 220; tip_a = 0
    samples = []
    for i in range(n + 1):
        s = SWEEP * i / n; r = R2 * PHI ** (-s / 90); w = r * K2
        samples.append((tip_a + s, r, w, i / n))
    outer = [pt(px, py, a, r + w / 2) for a, r, w, _ in samples]
    inner = [pt(px, py, a, r - w / 2) for a, r, w, _ in samples]
    w0 = samples[0][2]; head = w0 * 1.0
    tip = pt(px, py, tip_a - head / (2 * math.pi * R2) * 360, R2)
    barb_o, barb_i = pt(px, py, tip_a, R2 + w0 / 2 + w0 / PHI ** 2), pt(px, py, tip_a, R2 - w0 / 2 - w0 / PHI ** 2)
    shape = poly([barb_o, tip, barb_i] + inner + outer[::-1])
    o = []
    if depth:
        side = d.lin([(0, BD), (1, '#4A1910')])
        for dy in range(depth, 0, -2):
            o.append(f'<path d="{shape}" transform="translate(0 {dy})" fill="{side}"/>')
    stops = [(0, EL), (.22, E), (.5, B), (.8, NL), (1, N)]
    if flat:
        o.append(f'<path d="{shape}" fill="{B}"/>')
    else:
        o.append(f'<path d="{poly([barb_o, tip, barb_i, inner[0], outer[0]])}" fill="{EL}"/>')
        for i in range(n - 1, -1, -1):  # each quad reaches into the next one, so no seams show
            col = ramp(stops, samples[i][3]); j = min(i + 2, n)
            o.append(f'<path d="{poly([outer[i], outer[j], inner[j], inner[i]])}" fill="{col}"/>')
        # a thin specular line along the outer edge, strongest at the tip
        hl = [pt(px, py, a, r + w / 2 - w / PHI ** 3) for a, r, w, _ in samples[:120]]
        o.append(f'<path d="M{"L".join(f2(p) for p in hl)}" fill="none" stroke="#FFFFFF" stroke-opacity=".32" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{R2 / PHI ** 7 * 1.6:.2f}" fill="{N}"/>')
    return ''.join(o)

def spiral_bbox():
    xs, ys = [], []
    for i in range(400):
        s = SWEEP * i / 400; r = R2 * PHI ** (-s / 90); w = r * K2
        for rr in (r + w / 2 + (w / PHI ** 2 if i == 0 else 0),):
            x, y = pt(0, 0, s, rr); xs.append(x); ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)

def unwind(flat=False):
    d = Doc('gu', flat)
    x0, x1, y0, y1 = spiral_bbox(); px, py = 256 - (x0 + x1) / 2, 248 - (y0 + y1) / 2
    o = []
    if not flat:
        o.append(f'<ellipse cx="256" cy="{248 + (y1 - y0) / 2 + 28:.2f}" rx="{(x1 - x0) / 2.4:.2f}" ry="16" fill="{NDD}" fill-opacity=".26"{d.blur(10)}/>')
    o.append(spiral(d, flat, px, py, 0 if flat else 14))
    return d.svg(512, 512, ''.join(o), 'Techne Hora: a golden spiral unwinding backward')


# ---------------------------------------------------------------- 3. Loop O
# A plain O whose ribbon laps its own tail at 11 o'clock, pointing counter-clockwise. Inner/outer radius = 1/phi.
RO3 = 200; RI3 = RO3 / PHI

def loop_o(flat=False):
    d = Doc('lo', flat); c = 256; bw = RO3 - RI3
    if flat:
        tube = B
    else:  # one gradient in page units, so the lapping end matches the ring under it exactly
        tid = d._id()
        d.defs.append(f'<radialGradient id="{tid}" gradientUnits="userSpaceOnUse" cx="{c}" cy="{c}" r="{RO3}">'
                      f'<stop offset="{RI3 / RO3:.4f}" stop-color="{BD}"/><stop offset=".74" stop-color="{E}"/>'
                      f'<stop offset=".86" stop-color="{EL}"/><stop offset="1" stop-color="{B}"/></radialGradient>')
        tube = f'url(#{tid})'
    ring = f'M{c - RO3} {c}a{RO3} {RO3} 0 1 0 {2 * RO3} 0a{RO3} {RO3} 0 1 0 {-2 * RO3} 0ZM{c - RI3:.2f} {c}a{RI3:.2f} {RI3:.2f} 0 1 1 {2 * RI3:.2f} 0a{RI3:.2f} {RI3:.2f} 0 1 1 {-2 * RI3:.2f} 0Z'
    o = [f'<g{d.shadow(12, 16, .3)}><path d="{ring}" fill="{tube}" fill-rule="evenodd"/></g>']
    # the ribbon's leading end lies on top of its own tail; only its point casts a shadow, forward along the turn
    head = band(c, c, 75, -32, RI3, RO3, steps=120, tip=bw * .9)
    if flat:
        o.append(f'<path d="{band(c, c, 20, -32, RI3, RO3, steps=60, tip=bw * .9)}" fill="none" stroke="{BD}" stroke-width="5" stroke-linejoin="round"/>')
        o.append(f'<path d="{head}" fill="{B}"/>')
    else:
        tip_only = band(c, c, 0, -32, RI3, RO3, steps=60, tip=bw * .9)
        rclip = f"<path d='{ring}' clip-rule='evenodd'/>"
        i = d._id()
        d.defs.append(f'<filter id="{i}" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="-6" dy="4" stdDeviation="3" flood-color="#3A120A" flood-opacity=".6"/></filter>')
        o.append(f'<g{clip(d, rclip)}><path d="{tip_only}" fill="{B}" filter="url(#{i})"/></g>')
        o.append(f'<path d="{head}" fill="{tube}"/>')
        o.append(f'<path d="{ring}" fill="{d.lin([(0, "#FFFFFF", .26), (.5, "#FFFFFF", 0), (1, NDD, .16)], .1, 0, .9, 1)}" fill-rule="evenodd"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{RI3 + 1:.2f}" fill="{d.rad([(0, "#FFFFFF"), (.7, P), (1, P2)], .42, .36, .66, flat=P)}"/>')
    # one hand, an hour back from 12
    hw = bw / PHI ** 3
    o.append(f'<path d="M{c} {c}L{f2(pt(c, c, -30, RI3 / PHI))}" stroke="{N}" stroke-width="{hw:.2f}" stroke-linecap="round"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{hw * .9:.2f}" fill="{N}"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora: an O that laps itself backward')


# ---------------------------------------------------------------- lockups
INK, MUTE = N, G
def inner(svg): return svg.split('>', 1)[1].rsplit('</svg>', 1)[0]

def place(mark, cx, cy, r, mcx=256, mcy=256, mr=200):
    """Scale a 512 mark so its circle (mcx, mcy, mr) lands on (cx, cy, r)."""
    s = r / mr
    return f'<g transform="translate({cx - mcx * s:.2f} {cy - mcy * s:.2f}) scale({s:.4f})">{inner(mark)}</g>'

def wrap(w, h, body, label='Techne Hora'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{label}">{body}</svg>\n'

SIZE = 150

def lockup_quiet(mark, circ):
    """Techne in Serif 600, Hora in Plex Sans Light, graphite. Mark = cap height x phi^2."""
    capH = cap(SERIF, SIZE); r = capH * PHI ** 2 / 2; h = 2 * r + 60; mid = h / 2
    gap = capH / PHI; x = 30 + 2 * r + gap; base = mid + capH / 2
    t1, w1 = text(SERIF, 'Techne', SIZE, x, base, INK, track=.01)
    t2, w2 = text(SANS_LIGHT, 'Hora', SIZE, x + w1 + SIZE * .26, base, MUTE, track=.02)
    return wrap(x + w1 + SIZE * .26 + w2 + 30, h, place(mark, 30 + r, mid, r, *circ) + t1 + t2)

def lockup_clock_o(mark, circ):
    """The mark stands in for the o of Hora; Hora set in graphite so it steps back."""
    capH = cap(SERIF, SIZE); xh = xheight(SERIF, SIZE); h = capH + 120; base = 60 + capH
    t1, w1 = text(SERIF, 'Techne', SIZE, 30, base, INK, track=.01)
    x = 30 + w1 + SIZE * .26
    tH, wH = text(SERIF, 'H', SIZE, x, base, MUTE, track=.01)
    r = xh * 1.08 / 2; ox = x + wH + SIZE * .035 + r
    tr, wr = text(SERIF, 'ra', SIZE, ox + r + SIZE * .035, base, MUTE, track=.01)
    return wrap(ox + r + SIZE * .035 + wr + 30, h, t1 + tH + place(mark, ox, base - xh / 2, r, *circ) + tr)

def lockup_dial(mark, circ):
    """Techne on top; HORA under it in Plex Mono at Techne/phi^2, spaced like hour marks to Techne's width."""
    capH = cap(SERIF, SIZE); small = SIZE / PHI ** 2; capS = cap(MONO, small)
    lead = capH / PHI ** 2; block = capH + lead + capS
    r = block * PHI / 2 * 1.0; h = max(2 * r, block) + 70; mid = h / 2
    x = 30 + 2 * r + capH / PHI
    base1 = mid - block / 2 + capH; base2 = base1 + lead + capS
    t1, w1 = text(SERIF, 'Techne', SIZE, x, base1, INK, track=.01)
    letters = 'HORA'; adv = [text(MONO, ch, small, 0, 0, MUTE)[1] for ch in letters]
    step = (w1 - adv[-1]) / 3
    t2 = ''.join(text(MONO, ch, small, x + i * step, base2, MUTE)[0] for i, ch in enumerate(letters))
    ticks = ''.join(f'<rect x="{x + i * step + adv[i] + (step - adv[i]) / 2 - 2:.2f}" y="{base2 - capS * .62:.2f}" width="4" height="{capS * .24:.2f}" rx="2" fill="{MUTE}" fill-opacity=".55"/>' for i in range(3))
    return wrap(x + w1 + 30, h, place(mark, 30 + r, mid, r, *circ) + t1 + t2 + ticks)


MARKS = {'1-back-hands': (back_hands, None), '2-golden-unwind': (unwind, 'spiral'), '3-loop-o': (loop_o, None)}

def circle_of(kind):
    if kind != 'spiral': return (256, 256, 200)
    x0, x1, y0, y1 = spiral_bbox()
    return (256, 248, max(x1 - x0, y1 - y0) / 2)

if __name__ == '__main__':
    for name, (fn, kind) in MARKS.items():
        full = fn(); circ = circle_of(kind)
        open(os.path.join(HERE, f'{name}-3d.svg'), 'w').write(full)
        open(os.path.join(HERE, f'{name}-flat.svg'), 'w').write(fn(flat=True))
        for v, lk in (('quiet', lockup_quiet), ('clock-o', lockup_clock_o), ('dial', lockup_dial)):
            open(os.path.join(HERE, f'{name}-lockup-{v}.svg'), 'w').write(lk(full, circ))
