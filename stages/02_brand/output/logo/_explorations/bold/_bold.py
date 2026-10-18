"""Bold round: five dimensional Techne Hora marks, drawn as pure vector geometry.

Needs fontTools + brotli and the Plex woff2 files in stages/03_design-system/output/fonts/ (only for the
engraved bezel lettering and the lockups):
    python _bold.py
Writes <n>-<name>-3d.svg, -flat.svg and -lockup.svg next to this file.
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(HERE, '../../../../../03_design-system/output/fonts'))
SERIF = TTFont(os.path.join(FONTS, 'IBMPlexSerif-600.woff2'))
MONO = TTFont(os.path.join(FONTS, 'IBMPlexMono-500.woff2'))

N, NL, NLL, ND, NDD = '#1B2A4A', '#2B4374', '#3D5A92', '#111B31', '#0A1120'
P, P2, P3 = '#FAF7F0', '#EDE5D3', '#D9CDB4'
B, BL, BD = '#A63D2A', '#C4553E', '#7E2C1D'
E, EL, ED = '#E07A5F', '#F29A80', '#B8573E'
BLUSH = '#F3D3C8'

f2 = lambda p: f'{p[0]:.2f} {p[1]:.2f}'
def pt(cx, cy, deg, r):
    a = math.radians(deg); return cx + r * math.sin(a), cy - r * math.cos(a)
def poly(pts): return 'M' + 'L'.join(f2(p) for p in pts) + 'Z'


class Doc:
    """Collects gradient/filter defs; in flat mode every gradient collapses to its middle stop."""
    def __init__(self, pid, flat=False):
        self.pid, self.flat, self.defs, self.n = pid, flat, [], 0

    def _id(self):
        self.n += 1; return f'{self.pid}{self.n}'

    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, flat=None):
        if self.flat: return flat or stops[len(stops) // 2][1]
        i = self._id()
        s = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else '') + '/>' for o, c, *r in stops for a in [r[0] if r else 1])
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return f'url(#{i})'

    def rad(self, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None, flat=None):
        if self.flat: return flat or stops[len(stops) // 2][1]
        i = self._id()
        s = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else '') + '/>' for o, c, *r_ in stops for a in [r_[0] if r_ else 1])
        fxy = f' fx="{fx}" fy="{fy}"' if fx is not None else ''
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"{fxy}>{s}</radialGradient>')
        return f'url(#{i})'

    def shadow(self, dy=10, blur=14, op=.35, col=NDD):
        if self.flat: return ''
        i = self._id()
        self.defs.append(f'<filter id="{i}" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="{col}" flood-opacity="{op}"/></filter>')
        return f' filter="url(#{i})"'

    def blur(self, sd):
        if self.flat: return ''
        i = self._id()
        self.defs.append(f'<filter id="{i}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>')
        return f' filter="url(#{i})"'

    def svg(self, w, h, body, label='Techne Hora'):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{label}">'
                f'<defs>{"".join(self.defs)}</defs>{body}</svg>\n')


def glyph(font, ch, size, fill):
    """One glyph centered on x=0, baseline y=0."""
    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font['head'].unitsPerEm
    g = cmap[ord(ch)]; k = size / upm; adv = font['hmtx'][g][0] * k
    pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (k, 0, 0, -k, -adv / 2, 0)))
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', adv

def text(font, s, size, x, base, fill, track=0.0):
    out, cx = [], x
    for ch in s:
        g, adv = glyph(font, ch, size, fill)
        out.append(f'<g transform="translate({cx + adv / 2:.2f} {base:.2f})">{g}</g>'); cx += adv + track * size
    return ''.join(out), cx - x - track * size

def cap(font, size): return font['OS/2'].sCapHeight * size / font['head'].unitsPerEm

def arc_text(font, s, size, cx, cy, r, center_deg, fill, top=True, track=.12):
    advs = [glyph(font, ch, size, fill)[1] + track * size for ch in s]
    total = sum(advs) - track * size
    ang = lambda d: d / r * 180 / math.pi
    out = []; pos = -total / 2
    for ch, a in zip(s, advs):
        g, adv = glyph(font, ch, size, fill)
        mid = pos + adv / 2; pos += a
        if top:
            phi = center_deg + ang(mid); x, y = pt(cx, cy, phi, r); rot = phi
        else:
            phi = center_deg - ang(mid); x, y = pt(cx, cy, phi, r + cap(font, size)); rot = phi + 180
        out.append(f'<g transform="translate({x:.2f} {y:.2f}) rotate({rot:.2f})">{g}</g>')
    return ''.join(out)

def taper_arc(cx, cy, a0, a1, r, w0, w1, head, steps=72):
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps; a = a0 + (a1 - a0) * t; w = w0 + (w1 - w0) * t
        outer.append(pt(cx, cy, a, r + w / 2)); inner.append(pt(cx, cy, a, r - w / 2))
    dirn = -1 if a1 < a0 else 1
    tip = pt(cx, cy, a1 + dirn * head * 360 / (2 * math.pi * r), r); hw = w1 * .5 + head * .45
    return poly(outer + [pt(cx, cy, a1, r + hw), tip, pt(cx, cy, a1, r - hw)] + inner[::-1])

def faceted_hand(cx, cy, deg, length, width, tail, light, dark):
    """Dauphine hand split down its spine: one half catches the light, the other is in shade."""
    tip = pt(cx, cy, deg, length); back = pt(cx, cy, deg + 180, tail)
    l = pt(cx, cy, deg - 90, width / 2); r = pt(cx, cy, deg + 90, width / 2)
    return f'<path d="{poly([back, l, tip])}" fill="{light}"/><path d="{poly([back, r, tip])}" fill="{dark}"/>'

def sector(cx, cy, a0, a1, r):
    s, e = pt(cx, cy, a0, r), pt(cx, cy, a1, r)
    return f'M{cx:.2f} {cy:.2f}L{f2(s)}A{r:.2f} {r:.2f} 0 0 1 {f2(e)}Z'


# ---------------------------------------------------------------- 1. Enamel dial
def enamel(flat=False):
    d = Doc('en', flat); c = 256
    o = [f'<g{d.shadow(14, 18, .38)}>']
    o.append(f'<circle cx="{c}" cy="{c}" r="236" fill="{d.lin([(0, NLL), (.45, N), (1, NDD)], 0, 0, .8, 1)}"/>')
    if not flat:
        o.append(f'<circle cx="{c}" cy="{c}" r="234" fill="none" stroke="{d.lin([(0, "#FFFFFF", .55), (.5, "#FFFFFF", 0)], 0, 0, 0, 1)}" stroke-width="3"/>')
        o.append(f'<circle cx="{c}" cy="{c}" r="176" fill="none" stroke="{d.lin([(0, NDD, .9), (1, NLL, .6)], 0, 0, 0, 1)}" stroke-width="6"/>')
    o.append('</g>')
    # engraved bezel lettering
    ink = P if flat else '#E9E1CF'
    o.append(arc_text(SERIF, 'TECHNE', 40, c, c, 192, 0, ink, top=True, track=.28))
    o.append(arc_text(MONO, 'HORA', 30, c, c, 192, 180, ink, top=False, track=.5))
    # face
    o.append(f'<circle cx="{c}" cy="{c}" r="172" fill="{d.rad([(0, "#FFFFFF"), (.7, P), (1, P2)], .45, .4, .62, flat=P)}"/>')
    if not flat:
        o.append(f'<circle cx="{c}" cy="{c + 6}" r="172" fill="none" stroke="{NDD}" stroke-opacity=".22" stroke-width="10"{d.blur(5)} clip-path="circle(172px at {c}px {c}px)"/>')
    o.append(f'<path d="{sector(c, c, 300, 360, 150)}" fill="{d.rad([(0, BLUSH, .35), (1, BLUSH, 1)], .5, .5, .5, flat=BLUSH)}"/>')
    for a in range(0, 360, 6):
        if a % 30 == 0:
            major = a % 90 == 0; w, l0 = (10, 128) if major else (6, 138)
            o.append(f'<path d="{poly([pt(c, c, a - w / 30, 160), pt(c, c, a + w / 30, 160), pt(c, c, a + w / 60, l0), pt(c, c, a - w / 60, l0)])}" fill="{N}"/>')
        else:
            x, y = pt(c, c, a, 158); o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.6" fill="{N}" fill-opacity=".45"/>')
    # rewind arrow sitting on the face edge, faceted
    o.append(f'<g{d.shadow(4, 4, .3)}><path d="{taper_arc(c, c, 52, -96, 180, 4, 18, 26)}" fill="{d.lin([(0, EL), (.5, E), (1, ED)], 0, 0, 1, 1)}"/></g>')
    # hands with a cast shadow
    if not flat:
        o.append(f'<g opacity=".22" transform="translate(6 9)"{d.blur(3)}>' + faceted_hand(c, c, 300, 92, 26, 22, NDD, NDD) + faceted_hand(c, c, 0, 138, 20, 26, NDD, NDD) + '</g>')
    o.append(faceted_hand(c, c, 300, 92, 26, 22, BL, BD))
    o.append(faceted_hand(c, c, 0, 138, 20, 26, NLL, ND))
    o.append(f'<circle cx="{c}" cy="{c}" r="14" fill="{d.rad([(0, EL), (1, BD)], .35, .35, .7, flat=B)}"/><circle cx="{c}" cy="{c}" r="5" fill="{P}"/>')
    if not flat:  # domed crystal highlight
        o.append(f'<path d="M{c - 150} {c - 40}A160 160 0 0 1 {c + 70} {c - 150}A190 190 0 0 0 {c - 150} {c - 40}Z" fill="#FFFFFF" fill-opacity=".35"/>')
        o.append(f'<ellipse cx="{c - 70}" cy="{c - 95}" rx="70" ry="34" transform="rotate(-35 {c - 70} {c - 95})" fill="#FFFFFF" fill-opacity=".10"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora enamel dial')


# ---------------------------------------------------------------- 2. Rewind ribbon (extruded arrow ring)
def ribbon(flat=False):
    d = Doc('rb', flat); c = 256; cy = 240
    o = []
    if not flat:
        o.append(f'<ellipse cx="{c}" cy="470" rx="170" ry="22" fill="{NDD}" fill-opacity=".28"{d.blur(10)}/>')
    band = taper_arc(c, cy, 40, -275, 196, 30, 64, 46, steps=140)
    depth = 0 if flat else 18
    side = d.lin([(0, BD), (1, '#5E1F14')], 0, 0, 0, 1, flat=B)
    for dy in range(depth, 0, -2):
        o.append(f'<path d="{band}" transform="translate(0 {dy})" fill="{side}"/>')
    o.append(f'<path d="{band}" fill="{d.lin([(0, EL), (.55, E), (1, B)], 0, 0, .3, 1)}"/>')
    if not flat:  # specular stripe along the ribbon
        o.append(f'<path d="{taper_arc(c, cy, 32, -250, 206, 2, 10, 0, steps=140)}" fill="#FFFFFF" fill-opacity=".28"/>')
    # dial puck in the middle, with its own thickness
    if not flat:
        o.append(f'<circle cx="{c}" cy="{cy + 14}" r="128" fill="{NDD}"/>')
    o.append(f'<circle cx="{c}" cy="{cy}" r="128" fill="{d.lin([(0, NLL), (.6, N), (1, ND)], 0, 0, .6, 1)}"/>')
    o.append(f'<circle cx="{c}" cy="{cy}" r="96" fill="{d.rad([(0, "#FFFFFF"), (.75, P), (1, P2)], .45, .4, .6, flat=P)}"/>')
    o.append(f'<path d="{sector(c, cy, 300, 360, 84)}" fill="{BLUSH}"/>')
    for a in range(0, 360, 30):
        major = a % 90 == 0
        o.append(f'<path d="M{f2(pt(c, cy, a, 74 if major else 80))}L{f2(pt(c, cy, a, 88))}" stroke="{N}" stroke-width="{7 if major else 4}" stroke-linecap="round"/>')
    o.append(faceted_hand(c, cy, 300, 52, 18, 12, BL, BD))
    o.append(faceted_hand(c, cy, 0, 74, 14, 14, NLL, ND))
    o.append(f'<circle cx="{c}" cy="{cy}" r="9" fill="{N}"/><circle cx="{c}" cy="{cy}" r="3.5" fill="{P}"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora rewind ribbon')


# ---------------------------------------------------------------- 3. T-hand app tile
def thand(flat=False):
    d = Doc('th', flat); c = 256
    o = [f'<g{d.shadow(16, 20, .4)}><rect x="24" y="24" width="464" height="464" rx="108" fill="{d.lin([(0, NLL), (.5, N), (1, NDD)], 0, 0, .5, 1)}"/></g>']
    if not flat:
        o.append(f'<rect x="26" y="26" width="460" height="460" rx="106" fill="none" stroke="{d.lin([(0, "#FFFFFF", .35), (.4, "#FFFFFF", 0)], 0, 0, 0, 1)}" stroke-width="3"/>')
        o.append(f'<circle cx="{c}" cy="{c + 5}" r="176" fill="{NDD}" fill-opacity=".6"{d.blur(6)}/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="172" fill="{d.rad([(0, "#FFFFFF"), (.8, P), (1, P3)], .5, .42, .6, flat=P)}"/>')
    o.append(f'<path d="{sector(c, c, 300, 360, 150)}" fill="{BLUSH}"/>')
    for a in range(0, 360, 30):
        if a == 0: continue
        x, y = pt(c, c, a, 150); o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{8 if a % 90 == 0 else 5}" fill="{N}"/>')
    # rewind arrow raised off the face
    o.append(f'<g{d.shadow(5, 5, .35)}><path d="{taper_arc(c, c, 50, -98, 186, 6, 22, 30)}" fill="{d.lin([(0, EL), (1, ED)], 0, 0, 1, 1)}"/></g>')
    # hour hand
    o.append(f'<g{d.shadow(6, 5, .3)}>' + faceted_hand(c, c, 300, 96, 30, 22, BL, BD) + '</g>')
    # the minute hand is a T: stem from the hub, crossbar at twelve
    stem_l, stem_r = d.lin([(0, NLL), (1, N)], 0, 0, 1, 0, flat=N), d.lin([(0, N), (1, NDD)], 0, 0, 1, 0, flat=N)
    t = (f'<path d="M{c - 14} {c}L{c - 14} {c - 112}L{c} {c - 112}L{c} {c}Z" fill="{stem_l}"/>'
         f'<path d="M{c} {c}L{c} {c - 112}L{c + 14} {c - 112}L{c + 14} {c}Z" fill="{stem_r}"/>'
         f'<rect x="{c - 62}" y="{c - 142}" width="124" height="30" rx="4" fill="{d.lin([(0, NLL), (1, ND)], 0, 0, 0, 1, flat=N)}"/>')
    o.append(f'<g{d.shadow(7, 6, .3)}>{t}</g>')
    o.append(f'<circle cx="{c}" cy="{c}" r="20" fill="{d.rad([(0, EL), (1, BD)], .35, .35, .7, flat=B)}"/><circle cx="{c}" cy="{c}" r="7" fill="{P}"/>')
    if not flat:
        o.append(f'<path d="M{c - 160} {c - 30}A170 170 0 0 1 {c + 40} {c - 166}A200 200 0 0 0 {c - 160} {c - 30}Z" fill="#FFFFFF" fill-opacity=".4"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora T-hand')


# ---------------------------------------------------------------- 4. Sundial (hora began as a shadow)
YAW, ELEV = math.radians(-24), math.radians(36)
SX, SY = 256, 300
def proj(x, y, z):
    xr = x * math.cos(YAW) - y * math.sin(YAW); yr = x * math.sin(YAW) + y * math.cos(YAW)
    return SX + xr, SY + yr * math.sin(ELEV) - z * math.cos(ELEV)
def depth(x, y): return x * math.sin(YAW) + y * math.cos(YAW)

def box(d, x0, x1, y0, y1, z0, z1, top, light, dark):
    faces = []
    P8 = lambda x, y, z: proj(x, y, z)
    for nx, ny, quad in (((0, 1), None, [(x0, y1), (x1, y1)]), ((0, -1), None, [(x1, y0), (x0, y0)]),
                         ((1, 0), None, [(x1, y1), (x1, y0)]), ((-1, 0), None, [(x0, y0), (x0, y1)])):
        n = nx
        if depth(*n) <= 0: continue
        (ax, ay), (bx, by) = quad
        shade = light if n[0] + n[1] * .3 > 0 else dark
        faces.append(f'<path d="{poly([P8(ax, ay, z0), P8(bx, by, z0), P8(bx, by, z1), P8(ax, ay, z1)])}" fill="{shade}"/>')
    faces.append(f'<path d="{poly([P8(x0, y0, z1), P8(x1, y0, z1), P8(x1, y1, z1), P8(x0, y1, z1)])}" fill="{top}"/>')
    return ''.join(faces)

def sundial(flat=False):
    d = Doc('sd', flat); R, T = 200, 26
    circ = lambda r, z, a0=0, a1=360, n=120: [proj(r * math.sin(math.radians(a)), -r * math.cos(math.radians(a)), z) for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]
    o = []
    if not flat:
        o.append(f'<ellipse cx="{SX}" cy="{SY + 70}" rx="230" ry="70" fill="{NDD}" fill-opacity=".3"{d.blur(14)}/>')
    # plate rim: the near half of the cylinder wall
    top_ring, bot_ring = circ(R, 0), circ(R, -T)
    near = [p for p in range(121)]
    rim = poly(top_ring + bot_ring[::-1])
    o.append(f'<path d="{rim}" fill="{d.lin([(0, NL), (.5, N), (1, NDD)], 0, 0, 1, 0, flat=N)}"/>')
    o.append(f'<path d="{poly(bot_ring)}" fill="{d.lin([(0, NL), (.5, N), (1, NDD)], 0, 0, 1, 0, flat=N)}"/>')
    o.append(f'<path d="{poly(top_ring)}" fill="{d.lin([(0, "#FFFFFF"), (.6, P), (1, P2)], 0, 0, .3, 1, flat=P)}"/>')
    # inner navy ring on the plate face
    o.append(f'<path d="{poly(circ(R - 6, 0) + circ(R - 30, 0)[::-1])}" fill="{N}" fill-rule="evenodd"/>')
    # blush wedge from 10 to 12
    wedge = [proj(0, 0, 0)] + circ(150, 0, 300, 360, 30)
    o.append(f'<path d="{poly(wedge)}" fill="{BLUSH}"/>')
    # hour ticks
    for a in range(0, 360, 30):
        major = a % 90 == 0; w = 4 if major else 2.4
        r0 = 150 if major else 158
        a0, a1 = a - w / 2 * 360 / (2 * math.pi * 170) * 2, a + w / 2 * 360 / (2 * math.pi * 170) * 2
        q = [(r0, a0), (r0, a1), (166, a1), (166, a0)]
        o.append(f'<path d="{poly([proj(r * math.sin(math.radians(t)), -r * math.cos(math.radians(t)), 0) for r, t in q])}" fill="{N}"/>')
    # rewind arrow painted on the navy ring, counter-clockwise
    arc = []
    a0, a1, steps = 60, -105, 80
    for side in (1, -1):
        seq = range(steps + 1) if side == 1 else range(steps, -1, -1)
        for i in seq:
            t = i / steps; a = math.radians(a0 + (a1 - a0) * t); w = (3 + 9 * t) * side
            r = 188 + w
            arc.append(proj(r * math.sin(a), -r * math.cos(a), .5))
    ah = math.radians(a1); tip = math.radians(a1 - 9)
    head = [proj(201 * math.sin(ah), -201 * math.cos(ah), .5), proj(188 * math.sin(tip), -188 * math.cos(tip), .5), proj(175 * math.sin(ah), -175 * math.cos(ah), .5)]
    pts = arc[:steps + 1] + head + arc[steps + 1:]
    o.append(f'<path d="{poly(pts)}" fill="{E}"/>')
    # the T gnomon's shadow falls on ten o'clock, and is itself a T
    sd = (math.sin(math.radians(300)), -math.cos(math.radians(300)))
    L = 128; ex, ey = sd[0] * L, sd[1] * L; px, py = -sd[1], sd[0]
    stem = [(px * 11, py * 11), (ex + px * 11, ey + py * 11), (ex - px * 11, ey - py * 11), (-px * 11, -py * 11)]
    bar = [(ex - 56, ey - 2), (ex + 56, ey - 2), (ex + 56 + sd[0] * 24, ey + sd[1] * 24 - 2), (ex - 56 + sd[0] * 24, ey + sd[1] * 24 - 2)]
    sh = NDD
    op = 1 if flat else .5
    o.append(f'<g opacity="{op}"><path d="{poly([proj(x, y, .8) for x, y in stem])}" fill="{sh}"/><path d="{poly([proj(x, y, .8) for x, y in bar])}" fill="{sh}"/></g>')
    light = d.lin([(0, NLL), (1, NL)], 0, 0, 1, 0, flat=NL)
    o.append(box(d, -11, 11, -11, 11, 0, 132, NLL, light, NDD))
    o.append(box(d, -58, 58, -12, 12, 132, 156, NLL, light, ND))
    o.append(f'<path d="{poly(circ(17, .9, 0, 360, 24))}" fill="{B}"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora sundial')


# ---------------------------------------------------------------- 5. Hourglass H
def hourglass(flat=False, w=512):
    d = Doc('hg', flat); c = 256
    o = []
    if not flat:
        o.append(f'<ellipse cx="{c}" cy="472" rx="170" ry="16" fill="{NDD}" fill-opacity=".3"{d.blur(10)}/>')
    post = d.lin([(0, ND), (.25, NLL), (.55, N), (1, NDD)], 0, 0, 1, 0, flat=N)
    for x in (96, 360):
        o.append(f'<rect x="{x}" y="40" width="56" height="420" rx="18" fill="{post}"/>')
        if not flat:
            o.append(f'<rect x="{x + 12}" y="52" width="8" height="396" rx="4" fill="#FFFFFF" fill-opacity=".25"/>')
    # glass bulbs between the posts (the H's counters), neck at the crossbar
    top = f'M152 78C152 78 360 78 360 78C360 170 278 214 268 250L244 250C234 214 152 170 152 78Z'
    bot = f'M244 262C234 298 152 342 152 434L360 434C360 342 278 298 268 262Z'
    glass = d.lin([(0, NLL, .30), (.5, '#FFFFFF', .25), (1, NLL, .40)], 0, 0, 1, 0, flat=P)
    o.append(f'<path d="{top}" fill="{glass}" stroke="{N}" stroke-width="5"/>')
    o.append(f'<path d="{bot}" fill="{glass}" stroke="{N}" stroke-width="5"/>')
    # sand: a little left on top, a full mound below = the hours you banked
    o.append(f'<path d="M226 226C238 238 248 246 256 250C264 246 274 238 286 226Z" fill="{d.lin([(0, EL), (1, E)], flat=E)}"/>')
    o.append(f'<path d="M252 252L260 252L259 372L253 372Z" fill="{E}"/>')
    o.append(f'<path d="M162 430C176 378 220 360 256 356C292 360 336 378 350 430Z" fill="{d.lin([(0, EL), (.5, E), (1, B)], flat=E)}"/>')
    # the H crossbar: a brass collar at the neck
    o.append(f'<rect x="138" y="240" width="236" height="32" rx="10" fill="{d.lin([(0, BL), (.5, B), (1, BD)], 0, 0, 0, 1, flat=B)}"/>')
    if not flat:
        o.append('<rect x="146" y="244" width="220" height="6" rx="3" fill="#FFFFFF" fill-opacity=".3"/>')
        o.append(f'<path d="M172 96C176 150 210 188 234 214" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="6" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M172 418C176 380 196 340 228 306" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="6" fill="none" stroke-linecap="round"/>')
    return d.svg(512, 512, ''.join(o), 'Techne Hora hourglass H')


# ---------------------------------------------------------------- lockups (mark + Plex name)
def lockup(mark_svg, word='Techne Hora', dark=False):
    inner = mark_svg.split('>', 1)[1].rsplit('</svg>', 1)[0]
    ink = P if dark else N
    size = 150; capH = cap(SERIF, size)
    t, w = text(SERIF, word, size, 560, 256 + capH / 2, ink, track=.01)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {560 + w + 30:.0f} 512" role="img" aria-label="Techne Hora">{inner}{t}</svg>\n'

def hora_lockup(dark=False):
    """Techne + the hourglass standing in for the H of Hora."""
    ink = P if dark else N; size = 150; capH = cap(SERIF, size)
    base = 256 + capH / 2
    t1, w1 = text(SERIF, 'Techne', size, 30, base, ink, track=.01)
    s = capH * 1.02 / 420; mx = 30 + w1 + size * .30  # posts span y 40..460 of the mark
    mark = hourglass(flat=True).split('>', 1)[1].rsplit('</svg>', 1)[0]
    g = f'<g transform="translate({mx - 96 * s:.2f} {base - 460 * s:.2f}) scale({s:.4f})">{mark}</g>'
    t2, w2 = text(SERIF, 'ora', size, mx + 320 * s + size * .04, base, ink, track=.01)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {mx + 320 * s + size * .04 + w2 + 30:.0f} 512" role="img" aria-label="Techne Hora">{g}{t1}{t2}</svg>\n'


if __name__ == '__main__':
    marks = {'1-enamel': enamel, '2-ribbon': ribbon, '3-thand': thand, '4-sundial': sundial, '5-hourglass': hourglass}
    for name, fn in marks.items():
        full = fn(); open(os.path.join(HERE, f'{name}-3d.svg'), 'w').write(full)
        open(os.path.join(HERE, f'{name}-flat.svg'), 'w').write(fn(flat=True))
        if name != '5-hourglass':
            open(os.path.join(HERE, f'{name}-lockup.svg'), 'w').write(lockup(full))
    open(os.path.join(HERE, '5-hourglass-lockup.svg'), 'w').write(hora_lockup())
