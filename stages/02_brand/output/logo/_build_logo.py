"""Build the Techne Hora logo set: the C3 "dial label" design (owner's pick, 2026-10-18).

The mark is a navy-rimmed clock at 10:00 with the last two hours tinted; the name is "Techne" in IBM Plex Serif
with H·O·R·A set under it in Plex Mono, spaced like hour marks. The C1 rewind arrow is kept as a separate motion
asset (`technehora-rewind*.svg`), never part of the logo itself.

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
G, GD = '#5C6170', '#B8BFCC'  # graphite for HORA: on light backgrounds, and its pair on navy


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

def hora_label(x, base, width, size, fill):
    """H · O · R · A in mono, spread to `width`, with round ticks between the letters like hour marks."""
    advs = [text(MONO, ch, size, 0, 0, fill)[1] for ch in 'HORA']
    step = (width - advs[-1]) / 3; capS = cap(MONO, size)
    out = ''.join(text(MONO, ch, size, x + i * step, base, fill)[0] for i, ch in enumerate('HORA'))
    for i in range(3):
        mx = x + i * step + advs[i] + (step - advs[i]) / 2
        out += f'<circle cx="{mx:.2f}" cy="{base - capS / 2:.2f}" r="{size * .07:.2f}" fill="{fill}"/>'
    return out


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

def name_block(x, top, ink, mute):
    """Techne over H·O·R·A. Returns (svg, width, height)."""
    capH = cap(SERIF, SIZE); small = SIZE * .34; capS = cap(MONO, small); lead = capH * .42
    t, w = text(SERIF, 'Techne', SIZE, x, top + capH, ink, track=.01)
    t += hora_label(x + 2, top + capH + lead + capS, w - 4, small, mute)
    return t, w, capH + lead + capS

def horizontal(dark=False, pad=10):
    ink, mute = (P, GD) if dark else (N, G)
    _, _, block = name_block(0, 0, ink, mute)
    R = block * .62; cx = cy = pad + R; x = cx + R + SIZE * .28
    t, w, _ = name_block(x, cy - block / 2, ink, mute)
    return x + w + pad, 2 * R + 2 * pad, dial(cx, cy, R, f'h{int(dark)}', dark) + t

def stacked(dark=False):
    ink, mute = (P, GD) if dark else (N, G)
    size = 64; R = 70; scale = size / SIZE
    _, w, block = name_block(0, 0, ink, mute)
    W = max(w * scale, 2 * R) + 40
    t, _, _ = name_block(0, 0, ink, mute)
    top = 2 * R + 34
    body = (dial(W / 2, R + 6, R, f's{int(dark)}', dark)
            + f'<g transform="translate({(W - w * scale) / 2:.2f} {top:.2f}) scale({scale:.4f})">{t}</g>')
    return W, top + block * scale + 14, body

def wordmark(dark=False, pad=4):
    ink, mute = (P, GD) if dark else (N, G)
    t, w, block = name_block(pad, pad, ink, mute)
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
