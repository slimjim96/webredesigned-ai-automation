"""HORA as columns (owner's tweak, 2026-10-20): the same C3 lockup, with H·O·R·A drawn from upright stems in full
navy, as the base "Techne" stands on. Three takes: A columns, B columns on a plinth, C columns with caps and bases.
    ~/.cache/th-logo-venv/bin/python _columns.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '../..')))
import _build_logo as L

def rect(x, y, w, h, fill): return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"/>'

def letters(x, y, cw, h, s, fill, slabs=False):
    """Four column letters in cells of cw x h, stems s wide. Returns {letter: svg}."""
    r = cw / 2; ri = r - s; bar = s * .85
    out = {}
    out['H'] = rect(x, y, s, h, fill) + rect(x + cw - s, y, s, h, fill) + rect(x, y + h * .46 - bar / 2, cw, bar, fill)
    out['O'] = (f'<path fill-rule="evenodd" fill="{fill}" d="M{x:.2f} {y + r:.2f}A{r:.2f} {r:.2f} 0 0 1 {x + cw:.2f} {y + r:.2f}'
                f'V{y + h - r:.2f}A{r:.2f} {r:.2f} 0 0 1 {x:.2f} {y + h - r:.2f}Z'
                f'M{x + s:.2f} {y + r:.2f}A{ri:.2f} {ri:.2f} 0 0 1 {x + cw - s:.2f} {y + r:.2f}'
                f'V{y + h - r:.2f}A{ri:.2f} {ri:.2f} 0 0 1 {x + s:.2f} {y + h - r:.2f}Z"/>')
    hb = h * .56; rb = min(hb / 2, cw * .5); rbi = rb - s * .9
    out['R'] = (rect(x, y, s, h, fill)
                + f'<path fill-rule="evenodd" fill="{fill}" d="M{x:.2f} {y:.2f}H{x + cw - rb:.2f}A{rb:.2f} {rb:.2f} 0 0 1 {x + cw:.2f} {y + rb:.2f}'
                  f'V{y + hb - rb:.2f}A{rb:.2f} {rb:.2f} 0 0 1 {x + cw - rb:.2f} {y + hb:.2f}H{x:.2f}Z'
                  f'M{x + s:.2f} {y + s * .9:.2f}H{x + cw - rb:.2f}A{rbi:.2f} {rbi:.2f} 0 0 1 {x + cw - s:.2f} {y + rb:.2f}'
                  f'V{y + hb - rb:.2f}A{rbi:.2f} {rbi:.2f} 0 0 1 {x + cw - rb:.2f} {y + hb - s * .9:.2f}H{x + s:.2f}Z"/>'
                + f'<path fill="{fill}" d="M{x + cw * .42:.2f} {y + hb - s * .9:.2f}H{x + cw * .42 + s * 1.1:.2f}L{x + cw:.2f} {y + h:.2f}H{x + cw - s * 1.15:.2f}Z"/>')
    out['A'] = (f'<path fill="{fill}" d="M{x:.2f} {y + h:.2f}V{y + r:.2f}A{r:.2f} {r:.2f} 0 0 1 {x + cw:.2f} {y + r:.2f}V{y + h:.2f}'
                f'H{x + cw - s:.2f}V{y + r:.2f}A{ri:.2f} {ri:.2f} 0 0 0 {x + s:.2f} {y + r:.2f}V{y + h:.2f}Z"/>'
                + rect(x, y + h * .6 - bar / 2, cw, bar, fill))
    if slabs:  # a base under every stem foot, a cap on every flat stem top
        sw, sh = s * 1.9, s * .42; o = (sw - s) / 2
        base = lambda sx: rect(sx - o, y + h - sh, sw, sh, fill)
        top = lambda sx: rect(sx - o, y, sw, sh, fill)
        out['H'] += base(x) + base(x + cw - s) + top(x) + top(x + cw - s)
        out['O'] = out['O']
        out['R'] += base(x) + top(x)
        out['A'] += base(x) + base(x + cw - s)
    return out

def hora(x, y, width, h, fill, slabs=False, dots=True):
    s = h * .19; cw = h * .56; gap = (width - 4 * cw) / 3
    ls = letters(0, 0, cw, h, s, fill, slabs)
    out = ''
    for i, ch in enumerate('HORA'):
        lx = x + i * (cw + gap)
        out += letters(lx, y, cw, h, s, fill, slabs)[ch]
        if dots and i < 3:
            out += f'<circle cx="{lx + cw + gap / 2:.2f}" cy="{y + h / 2:.2f}" r="{s * .5:.2f}" fill="{fill}"/>'
    return out, s

def name_block(x, top, ink, take):
    capH = L.cap(L.SERIF, L.SIZE); h = capH * .56; gap = capH * .28
    t, w = L.text(L.SERIF, 'Techne', L.SIZE, x, top + capH, ink, track=.01)
    hy = top + capH + gap
    lab, s = hora(x + 2, hy, w - 4, h, ink, slabs=(take == 'C'))
    height = capH + gap + h
    if take == 'B':
        lab += rect(x, hy + h + s * .6, w, s * 1.1, ink); height += s * 1.7
    return t + lab, w, height

def horizontal(take, dark=False, pad=10):
    ink = L.P if dark else L.N
    _, _, block = name_block(0, 0, ink, take)
    R = block * .62; cx = cy = pad + R; x = cx + R + L.SIZE * .28
    t, w, _ = name_block(x, cy - block / 2, ink, take)
    return x + w + pad, 2 * R + 2 * pad, L.dial(cx, cy, R, f'{take}{int(dark)}', dark) + t

for take in 'ABC':
    for theme, dark in (('light', False), ('dark', True)):
        w, h, body = horizontal(take, dark)
        with open(os.path.join(HERE, f'{take}-horizontal-{theme}.svg'), 'w') as fh:
            fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Techne Hora">{body}</svg>\n')
print('ok')
